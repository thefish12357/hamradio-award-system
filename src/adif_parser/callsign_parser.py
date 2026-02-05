"""Calls sign / DXCC mapping generated from cty.dat

此模块从仓库根的 `cty.dat` 加载国家与前缀数据，生成：
- `PREFIX_TO_DXCC`: 前缀（如 'BY','BA','3D2' 等）到国家名的映射（展开形式）
- `CONDENSED_LINES`: 每行为精简映射字符串，例如 "BA-BL,BR-BT,BY,BZ: CHINA"

提供 `find_country(callsign)` 快速按前缀匹配返回国家名或 None。
"""
from pathlib import Path
import re
from typing import Dict, Set, List, Tuple


def _load_cty(cty_path: Path) -> Dict[str, Set[str]]:
    data: Dict[str, Set[str]] = {}
    if not cty_path.exists():
        print(f"cty.dat文件不存在: {cty_path}")
        return data

    try:
        lines = cty_path.read_text(encoding='utf-8', errors='ignore').splitlines()
        current_country = None
        current_prefixes = set()
        token_re = re.compile(r"[A-Z0-9]+(?:-[A-Z0-9]+)?")

        def expand_token(tok: str) -> List[str]:
            tok = tok.upper()
            if '-' in tok:
                a, b = tok.split('-', 1)
                a = re.sub(r'[^A-Z0-9]', '', a)
                b = re.sub(r'[^A-Z0-9]', '', b)
                # handle two-letter alpha ranges like BA-BL -> BA,BB,...BL
                if len(a) == 2 and len(b) == 2 and a[0] == b[0] and a.isalpha() and b.isalpha():
                    start = ord(a[1]); end = ord(b[1])
                    if start <= end:
                        return [a[0] + chr(c) for c in range(start, end + 1)]
                # handle same-prefix numeric tail ranges like 3D2-3D4 -> 3D2,3D3,3D4
                if len(a) == len(b) and a[:-1] == b[:-1] and a[-1].isdigit() and b[-1].isdigit():
                    start = int(a[-1]); end = int(b[-1])
                    if start <= end:
                        base = a[:-1]
                        return [base + str(n) for n in range(start, end + 1)]
                # otherwise, return both endpoints cleaned
                return [a, b]
            else:
                return [re.sub(r'[^A-Z0-9]', '', tok)]

        for raw in lines:
            line = raw.rstrip('\n')
            if not line.strip():
                continue

            # 新国家条目行（不以空格开头且包含冒号）
            if ':' in line and not line.startswith(' '):
                # 保存前一个国家
                if current_country and current_prefixes:
                    data[current_country] = current_prefixes.copy()
                    current_prefixes = set()

                # 提取国家名
                parts = line.split(':', 1)
                country_name = parts[0].strip()
                current_country = country_name

                # 从同一行中提取可能的前缀 token
                for tok in token_re.findall(line.upper()):
                    for e in expand_token(tok):
                        if e and len(e) <= 6:
                            current_prefixes.add(e)

            # 前缀继续行（通常以空格开头）
            elif line.startswith(' ') and current_country:
                prefix_line = line.strip()
                # 移除末尾分号
                if prefix_line.endswith(';'):
                    prefix_line = prefix_line[:-1]

                # 找到所有 token，如 BA-BL, BG, 3D2 等
                for tok in token_re.findall(prefix_line.upper()):
                    for e in expand_token(tok):
                        if e and len(e) <= 6:
                            current_prefixes.add(e)
        
        # 保存最后一个国家
        if current_country and current_prefixes:
            data[current_country] = current_prefixes.copy()
        
        print(f"成功加载 {len(data)} 个国家的前缀数据")
        return data
        
    except Exception as e:
        print(f"解析cty.dat文件时出错: {e}")
        return {}

def _compress_prefixes(prefixes: Set[str]) -> List[str]:
    """生成精简表示：仅对两字母全字母前缀尝试合并连续序列（如 BA-BL）。
    其他前缀保持原样。
    """
    two_letter = {}
    others = []
    for p in prefixes:
        if len(p) == 2 and p.isalpha():
            two_letter.setdefault(p[0], []).append(p)
        else:
            others.append(p)

    parts: List[str] = []
    for first, lst in two_letter.items():
        seq = sorted(lst)
        # compress consecutive second letters
        run_start = run_end = None
        for s in seq:
            second = s[1]
            if run_start is None:
                run_start = run_end = second
            elif ord(second) == ord(run_end) + 1:
                run_end = second
            else:
                if run_start == run_end:
                    parts.append(first + run_start)
                else:
                    parts.append(f"{first}{run_start}-{first}{run_end}")
                run_start = run_end = second
        if run_start is not None:
            if run_start == run_end:
                parts.append(first + run_start)
            else:
                parts.append(f"{first}{run_start}-{first}{run_end}")

    # add others (sorted)
    parts.extend(sorted(others))
    return parts


# load at import
_this_file = Path(__file__).resolve()
_candidates = [
    _this_file.parents[2] / 'cty.dat',  # e.g. c:\ham text\1\cty.dat
    _this_file.parents[3] / 'cty.dat',  # e.g. c:\ham text\cty.dat
    _this_file.parents[1] / 'cty.dat',  # e.g. c:\ham text\1\src\cty.dat (unlikely)
    Path.cwd() / 'cty.dat',             # 当前工作目录下的 cty.dat
]

_CTY = None
for p in _candidates:
    if p and p.exists():
        _CTY = p
        break

if _CTY is None:
    # 最后保底：使用原来的 parents[3] 位置（以便保留原有行为）
    _ROOT = _this_file.parents[3]
    _CTY = _ROOT / 'cty.dat'

_COUNTRY_PREFIXES = _load_cty(_CTY)

# build expanded mapping prefix -> country
PREFIX_TO_DXCC: Dict[str, str] = {}
for country, prefs in _COUNTRY_PREFIXES.items():
    for p in prefs:
        PREFIX_TO_DXCC[p] = country

# build condensed lines
CONDENSED_LINES: List[str] = []
for country, prefs in sorted(_COUNTRY_PREFIXES.items(), key=lambda x: x[0].upper()):
    parts = _compress_prefixes(prefs)
    if parts:
        CONDENSED_LINES.append(f"{','.join(parts)}: {country}")


def find_country(callsign: str) -> Tuple[str, str] | None:
    """按前缀匹配给定 `callsign`，返回 (prefix, country) 或 None。

    尝试最长前缀匹配（按前缀长度降序）。
    """
    if not callsign:
        return None
    s = callsign.strip().upper()
    # try lengths from 5 down to 1
    for L in range(5, 0, -1):
        pref = s[:L]
        if pref in PREFIX_TO_DXCC:
            return pref, PREFIX_TO_DXCC[pref]
    return None


__all__ = ['PREFIX_TO_DXCC', 'CONDENSED_LINES', 'find_country']