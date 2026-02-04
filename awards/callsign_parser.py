"""精简的呼号解析器 - 从 `cty.dat` 同步并使用精简前缀表示（每个 DXCC 一行）。

实现要点：
- 使用由 `src/adif_parser/callsign_parser.py` 生成的 `CONDENSED_LINES`。
- 提供 `parse_callsign()`、`enhance_record()` 和 `enhance_records()`。
"""

import sys
import os
from typing import Dict, Optional, Tuple

# 使用绝对路径添加src目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

try:
    from adif_parser.callsign_parser import CONDENSED_LINES, find_country, PREFIX_TO_DXCC
    _find_country = find_country
    _prefix_map = PREFIX_TO_DXCC
    print(f"成功导入呼号解析器，CONDENSED_LINES长度: {len(CONDENSED_LINES)}")
except ImportError as e:
    print(f"导入错误: {e}")
    CONDENSED_LINES = []
    _find_country = None
    _prefix_map = {}

# 保留简化的国家->大洲与国家->DXCC 映射（可按需扩展）。
COUNTRY_TO_CONTINENT: Dict[str, str] = {
    'USA': 'NA', 'Canada': 'NA', 'Mexico': 'NA',
    'United Kingdom': 'EU', 'France': 'EU', 'Italy': 'EU', 'Germany': 'EU',
    'Spain': 'EU', 'Netherlands': 'EU', 'Belgium': 'EU',
    'Japan': 'AS', 'China': 'AS', 'Taiwan': 'AS', 'Hong Kong': 'AS', 'Macau': 'AS', 'India': 'AS', 'Russia': 'EU',
    'Australia': 'OC', 'New Zealand': 'OC',
    'Brazil': 'SA', 'Argentina': 'SA', 'Chile': 'SA'
}

# 保留一份国家->DXCC（简化、部分）用于输出
COUNTRY_TO_DXCC: Dict[str, int] = {
    'USA': 291, 'Canada': 1, 'Mexico': 50,
    'United Kingdom': 223, 'France': 227, 'Italy': 248, 'Germany': 230,
    'Japan': 339, 'China': 318, 'Taiwan': 386, 'Hong Kong': 321, 'Macau': 152, 'India': 324, 'Russia': 15,
    'Australia': 150, 'New Zealand': 170, 'Brazil': 108, 'Argentina': 100, 'Chile': 112
}

# 生成大小写不敏感的快速查找表
_COUNTRY_TO_CONTINENT_LOWER = {k.lower(): v for k, v in COUNTRY_TO_CONTINENT.items()}
_COUNTRY_TO_DXCC_LOWER = {k.lower(): v for k, v in COUNTRY_TO_DXCC.items()}

# 导入中国呼号段与省份的映射关系
from .china_callsign_province_map import get_province_by_callsign as get_province_from_map


class CallsignParser:
    """使用精简映射解析呼号的简单解析器。"""
    def __init__(self):
        # 保留精简行以便人工查看
        self.condensed_lines = CONDENSED_LINES
        # 使用 adif_parser 中的前缀->country 映射作为准确来源（若可用）
        self._prefix_map = _prefix_map
        self._find_country = _find_country

    def parse_callsign(self, callsign: str) -> Dict[str, Optional[str]]:
        """解析呼号，返回国家（display name）、大洲和 DXCC（数字字符串或 None）。"""
        if not callsign or not isinstance(callsign, str):
            return {'country': None, 'continent': None, 'dxcc': None}

        cs = callsign.strip().upper()

        country = None
        # 首先尝试使用更完整的前缀表（如果存在）进行最长前缀匹配
        if self._find_country:
            res = self._find_country(cs)
            if res:
                _, country = res

        # 回退策略：尝试从简化的 CONDENSED_LINES 中做简单匹配（prefix text -> country）
        if not country:
            for line in self.condensed_lines:
                try:
                    parts, cname = line.split(':', 1)
                    parts = parts.split(',')
                    cname = cname.strip()
                except Exception:
                    continue
                for p in parts:
                    p = p.strip()
                    token = p.split('-')[0]
                    if cs.startswith(token):
                        country = cname
                        break
                if country:
                    break

        # 若未找到 country，则不再使用启发式回退，依赖 cty.dat 数据和前缀映射

        # 使用不区分大小写的映射来查找 continent 与 dxcc
        country_key = str(country).strip().lower() if country else None
        continent = _COUNTRY_TO_CONTINENT_LOWER.get(country_key) if country_key else None
        dxcc_val = _COUNTRY_TO_DXCC_LOWER.get(country_key) if country_key else None
        dxcc = str(dxcc_val) if dxcc_val is not None else None

        return {'country': country, 'continent': continent, 'dxcc': dxcc}

    def get_province_by_callsign(self, callsign):
        """通过呼号获取对应的省份代码
        
        Args:
            callsign: 业余无线电呼号
            
        Returns:
            str: 省份代码，如 'BJ'，若未找到则返回 None
        """
        # 使用导入的映射函数
        return get_province_from_map(callsign)
    
    def enhance_record(self, record: Dict) -> Dict:
        """增强单条记录：若缺少 country/continent/dxcc，从 `call` 字段推断并填充。"""
        enhanced = record.copy()
        callsign = enhanced.get('call') or enhanced.get('CALL')
        if not callsign:
            return enhanced

        info = self.parse_callsign(callsign)
        country_key = None
        if info['country']:
            country_key = str(info['country']).strip().lower()
            
        # 填充国家、大洲和DXCC信息
        if not enhanced.get('country') and info['country']:
            enhanced['country'] = info['country']
        if not enhanced.get('continent') and info['continent']:
            enhanced['continent'] = info['continent']
        if not enhanced.get('dxcc') and info['dxcc']:
            enhanced['dxcc'] = info['dxcc']
        
        # 填充省份信息
        if not enhanced.get('state'):
            # 检查DXCC代码
            dxcc_val = enhanced.get('dxcc')
            if dxcc_val:
                try:
                    dxcc_int = int(str(dxcc_val))
                    # 根据DXCC代码设置省份
                    if dxcc_int == 386:
                        enhanced['state'] = 'TW'  # Taiwan
                    elif dxcc_int == 321:
                        enhanced['state'] = 'HK'  # Hong Kong
                    elif dxcc_int == 152:
                        enhanced['state'] = 'MO'  # Macau
                except (ValueError, TypeError):
                    pass
            
            # 针对中国大陆呼号
            if not enhanced.get('state') and country_key == 'china':
                province = self.get_province_by_callsign(callsign)
                if province:
                    enhanced['state'] = province
        
        return enhanced

    def enhance_records(self, records: list) -> list:
        return [self.enhance_record(r) for r in records]


# 全局实例
callsign_parser = CallsignParser()


if __name__ == '__main__':
    # 打印前几行以便人工校验
    print('--- condensed prefix preview (first 50) ---')
    for i, line in enumerate(CONDENSED_LINES[:50], 1):
        print(f"{i}. {line}")