import re
from typing import Tuple, List, Dict, Any
from datetime import datetime




def normalize_text(text: str) -> str:
    if text.startswith('\ufeff'):
        text = text.lstrip('\ufeff')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text


def _add_field(container: Dict[str, Any], tag: str, value: str) -> None:
    tag = tag.upper()
    if tag in container:
        existing = container[tag]
        if isinstance(existing, list):
            existing.append(value)
        else:
            container[tag] = [existing, value]
    else:
        container[tag] = value


def _first_value(v: Any) -> Any:
    if isinstance(v, list) and v:
        return v[0]
    return v


def _normalize_time_str(ts: Any) -> str | None:
    if ts is None:
        return None
    s = str(ts).strip()
    if not s:
        return None
    s2 = ''.join(ch for ch in s if ch.isdigit())
    if not s2:
        return None
    if len(s2) == 4:
        hh, mm, ss = s2[:2], s2[2:4], '00'
    elif len(s2) == 6:
        hh, mm, ss = s2[:2], s2[2:4], s2[4:6]
    elif len(s2) <= 2:
        hh, mm, ss = s2.zfill(2), '00', '00'
    else:
        return None
    try:
        hni, mni, sni = int(hh), int(mm), int(ss)
        if not (0 <= hni < 24 and 0 <= mni < 60 and 0 <= sni < 60):
            return None
    except Exception:
        return None
    return f"{hh.zfill(2)}:{mm.zfill(2)}:{ss.zfill(2)}"


def _normalize_date_str(ds: Any) -> str | None:
    if ds is None:
        return None
    s = str(ds).strip()
    s2 = ''.join(ch for ch in s if ch.isdigit())
    if len(s2) == 8:
        yyyy, mm, dd = s2[:4], s2[4:6], s2[6:8]
        try:
            datetime(int(yyyy), int(mm), int(dd))
        except Exception:
            return None
        return f"{yyyy}-{mm}-{dd}"
    try:
        dt = datetime.fromisoformat(s)
        return dt.date().isoformat()
    except Exception:
        return None


def parse_adif(text: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    解析 ADIF 文本，返回 (header_dict, records_list).

    header_dict: keys 为小写字符串，值为字符串或字符串列表（若重复）。
    records_list: 每条记录为字典，字段名小写，对应字段值（字符串或字符串列表）。

    额外：会对完全相同的 (CALL,BAND,MODE) 组合进行去重（保留首次出现），
    并尝试基于 `qso_date` + `time_on`/`time_off` 生成 `qso_datetime` / `qso_end_datetime`。
    """
    text = normalize_text(text)
    pos = 0
    seen_eoh = False
    header: Dict[str, Any] = {}
    records: List[Dict[str, Any]] = []
    current: Dict[str, Any] = {}
    length_text = len(text)

    while True:
        m = TAG_RE.search(text, pos)
        if not m:
            break
        tag = m.group('tag').upper()
        length = m.group('len')
        val_start = m.end()

        # 取值逻辑
        if length is not None:
            try:
                ln = int(length)
            except Exception:
                ln = None
            if ln is not None:
                # 优先按分号/下一个标签判定实际值长度：如果存在分号并且在下一个标签之前，按分号截取（更稳健）。
                semi = text.find(';', val_start)
                lt = text.find('<', val_start)
                if semi != -1 and (lt == -1 or semi < lt):
                    end = semi
                    value = text[val_start:end].strip()
                    pos = end
                    if pos < length_text and text[pos] == ';':
                        pos += 1
                else:
                    end_pos = min(val_start + ln, length_text)
                    value = text[val_start: end_pos]
                    pos = end_pos
                    if pos < length_text and text[pos] == ';':
                        pos += 1
            else:
                semi = text.find(';', val_start)
                lt = text.find('<', val_start)
                ends = [x for x in (semi, lt) if x != -1]
                end = min(ends) if ends else length_text
                value = text[val_start:end].strip()
                pos = end
                if pos < length_text and text[pos] == ';':
                    pos += 1
        else:
            semi = text.find(';', val_start)
            lt = text.find('<', val_start)
            candidates = [x for x in (semi, lt) if x != -1]
            if candidates:
                end = min(candidates)
            else:
                end = length_text
            value = text[val_start:end].strip()
            pos = end
            if pos < length_text and text[pos] == ';':
                pos += 1

        value = value.strip()

        if tag == 'EOH':
            seen_eoh = True
            continue
        if tag == 'EOR':
            if current:
                records.append({k.lower(): v for k, v in current.items()})
            current = {}
            continue

        # 根据是否看到 EOH 决定是 header 还是 record
        if not seen_eoh and not records:
            _add_field(header, tag, value)
        else:
            _add_field(current, tag, value)

    # 如果文件末尾没有 EOR，但 current 非空，也加入
    # 但要排除只包含结束标签的空记录或只有很少字段的无效记录
    if current:
        # 检查是否只有结束标签或无效字段
        has_valid_data = False
        for key, value in current.items():
            # 跳过结束标签和只有一个值的字段
            if key != 'app_lotw_eof' and value:
                has_valid_data = True
                break
        
        # 只有当有有效数据时才添加记录
        if has_valid_data:
            records.append({k.lower(): v for k, v in current.items()})

    header = {k.lower(): v for k, v in header.items()}

    # 对于LOTW日志，我们不应该去重，因为用户需要看到完整的记录数
    # 保留所有记录，不进行去重
    deduped = records

    # 时间解析：若存在 qso_date 与 time_on/time_off，生成 ISO8601 字符串字段
    for rec in deduped:
        date_raw = _first_value(rec.get('qso_date') or rec.get('date'))
        time_on_raw = _first_value(rec.get('time_on') or rec.get('time'))
        time_off_raw = _first_value(rec.get('time_off') or rec.get('time_off_on'))

        date_iso = _normalize_date_str(date_raw)
        time_on_iso = _normalize_time_str(time_on_raw)
        time_off_iso = _normalize_time_str(time_off_raw)

        if date_iso and time_on_iso:
            rec['qso_datetime'] = f"{date_iso}T{time_on_iso}"
        if date_iso and time_off_iso:
            rec['qso_end_datetime'] = f"{date_iso}T{time_off_iso}"

    return header, deduped


def detect_variant(text: str, header: Dict[str, Any]) -> str:
    """基于头部字段和值以及内容启发式检测导出软件的可能变体。"""
    t = text.lower()

    # 先检查头部值
    try:
        for v in header.values():
            sv = str(v).lower()
            if 'logger32' in sv:
                return 'Logger32'
            if 'n1mm' in sv or 'n1mm+' in sv:
                return 'N1MM Logger+'
            if 'hrd' in sv or 'ham radio deluxe' in sv:
                return 'Ham Radio Deluxe'
            if 'dxlog' in sv:
                return 'DXlog'
            if 'cqrlog' in sv:
                return 'CQRLOG'
            if 'logbook of the world' in sv or 'lotw' in sv:
                return 'LoTW'
    except Exception:
        pass

    # 再在全文中搜索已知标识
    patterns = {
        'Logger32': r'logger32',
        'N1MM Logger+': r'n1mm',
        'Ham Radio Deluxe': r'ham radio deluxe|\bhrd\b',
        'DXlog': r'dxlog',
        'CQRLOG': r'cqrlog',
        'LoTW': r'logbook of the world|lotw',
    }
    for name, pat in patterns.items():
        if re.search(pat, t):
            return name

    return 'Unknown'


__all__ = ['parse_adif', 'detect_variant']


__all__ = ['parse_adif', 'detect_variant']