"""中国呼号与省份映射表

该文件包含中国业余无线电呼号前缀与省份/地区的对应关系，用于WAPC奖状的省份识别。
"""

# 中国呼号段与省份/地区的映射关系
# 格式：省份代码 -> 呼号段列表
# 根据中国大陆业余无线电台呼号格式设计：B[电台种类][分区编号][呼号后缀]
CHINA_CALLSIGN_PROVINCE_MAP = {
    # 分区1：北京
    'BJ': ['BA1AA-BA1XZ', 'BB1AA-BB1XZ', 'BC1AA-BC1XZ', 'BD1AA-BD1XZ', 'BE1AA-BE1XZ',
           'BF1AA-BF1XZ', 'BG1AA-BG1XZ', 'BH1AA-BH1XZ', 'BI1AA-BI1XZ', 'BK1AA-BK1XZ',
           'BL1AA-BL1XZ'],
    
    # 分区2：黑龙江、吉林、辽宁
    'HL': ['BA2AA-BA2HZ', 'BB2AA-BB2HZ', 'BC2AA-BC2HZ', 'BD2AA-BD2HZ', 'BE2AA-BE2HZ',
           'BF2AA-BF2HZ', 'BG2AA-BG2HZ', 'BH2AA-BH2HZ', 'BI2AA-BI2HZ', 'BK2AA-BK2HZ',
           'BL2AA-BL2HZ'],
    'JL': ['BA2IA-BA2PZ', 'BB2IA-BB2PZ', 'BC2IA-BC2PZ', 'BD2IA-BD2PZ', 'BE2IA-BE2PZ',
           'BF2IA-BF2PZ', 'BG2IA-BG2PZ', 'BH2IA-BH2PZ', 'BI2IA-BI2PZ', 'BK2IA-BK2PZ',
           'BL2IA-BL2PZ'],
    'LN': ['BA2QA-BA2XZ', 'BB2QA-BB2XZ', 'BC2QA-BC2XZ', 'BD2QA-BD2XZ', 'BE2QA-BE2XZ',
           'BF2QA-BF2XZ', 'BG2QA-BG2XZ', 'BH2QA-BH2XZ', 'BI2QA-BI2XZ', 'BK2QA-BK2XZ',
           'BL2QA-BL2XZ'],
    
    # 分区3：天津、内蒙古、河北、山西
    'TJ': ['BA3AA-BA3FZ', 'BB3AA-BB3FZ', 'BC3AA-BC3FZ', 'BD3AA-BD3FZ', 'BE3AA-BE3FZ',
           'BF3AA-BF3FZ', 'BG3AA-BG3FZ', 'BH3AA-BH3FZ', 'BI3AA-BI3FZ', 'BK3AA-BK3FZ',
           'BL3AA-BL3FZ'],
    'NM': ['BA3GA-BA3LZ', 'BB3GA-BB3LZ', 'BC3GA-BC3LZ', 'BD3GA-BD3LZ', 'BE3GA-BE3LZ',
           'BF3GA-BF3LZ', 'BG3GA-BG3LZ', 'BH3GA-BH3LZ', 'BI3GA-BI3LZ', 'BK3GA-BK3LZ',
           'BL3GA-BL3LZ'],
    'HE': ['BA3MA-BA3RZ', 'BB3MA-BB3RZ', 'BC3MA-BC3RZ', 'BD3MA-BD3RZ', 'BE3MA-BE3RZ',
           'BF3MA-BF3RZ', 'BG3MA-BG3RZ', 'BH3MA-BH3RZ', 'BI3MA-BI3RZ', 'BK3MA-BK3RZ',
           'BL3MA-BL3RZ'],
    'SX': ['BA3SA-BA3XZ', 'BB3SA-BB3XZ', 'BC3SA-BC3XZ', 'BD3SA-BD3XZ', 'BE3SA-BE3XZ',
           'BF3SA-BF3XZ', 'BG3SA-BG3XZ', 'BH3SA-BH3XZ', 'BI3SA-BI3XZ', 'BK3SA-BK3XZ',
           'BL3SA-BL3XZ'],
    
    # 分区4：上海、山东、江苏
    'SH': ['BA4AA-BA4HZ', 'BB4AA-BB4HZ', 'BC4AA-BC4HZ', 'BD4AA-BD4HZ', 'BE4AA-BE4HZ',
           'BF4AA-BF4HZ', 'BG4AA-BG4HZ', 'BH4AA-BH4HZ', 'BI4AA-BI4HZ', 'BK4AA-BK4HZ',
           'BL4AA-BL4HZ'],
    'SD': ['BA4IA-BA4PZ', 'BB4IA-BB4PZ', 'BC4IA-BC4PZ', 'BD4IA-BD4PZ', 'BE4IA-BE4PZ',
           'BF4IA-BF4PZ', 'BG4IA-BG4PZ', 'BH4IA-BH4PZ', 'BI4IA-BI4PZ', 'BK4IA-BK4PZ',
           'BL4IA-BL4PZ'],
    'JS': ['BA4QA-BA4XZ', 'BB4QA-BB4XZ', 'BC4QA-BC4XZ', 'BD4QA-BD4XZ', 'BE4QA-BE4XZ',
           'BF4QA-BF4XZ', 'BG4QA-BG4XZ', 'BH4QA-BH4XZ', 'BI4QA-BI4XZ', 'BK4QA-BK4XZ',
           'BL4QA-BL4XZ'],
    
    # 分区5：浙江、江西、福建
    'ZJ': ['BA5AA-BA5HZ', 'BB5AA-BB5HZ', 'BC5AA-BC5HZ', 'BD5AA-BD5HZ', 'BE5AA-BE5HZ',
           'BF5AA-BF5HZ', 'BG5AA-BG5HZ', 'BH5AA-BH5HZ', 'BI5AA-BI5HZ', 'BK5AA-BK5HZ',
           'BL5AA-BL5HZ'],
    'JX': ['BA5IA-BA5PZ', 'BB5IA-BB5PZ', 'BC5IA-BC5PZ', 'BD5IA-BD5PZ', 'BE5IA-BE5PZ',
           'BF5IA-BF5PZ', 'BG5IA-BG5PZ', 'BH5IA-BH5PZ', 'BI5IA-BI5PZ', 'BK5IA-BK5PZ',
           'BL5IA-BL5PZ'],
    'FJ': ['BA5QA-BA5XZ', 'BB5QA-BB5XZ', 'BC5QA-BC5XZ', 'BD5QA-BD5XZ', 'BE5QA-BE5XZ',
           'BF5QA-BF5XZ', 'BG5QA-BG5XZ', 'BH5QA-BH5XZ', 'BI5QA-BI5XZ', 'BK5QA-BK5XZ',
           'BL5QA-BL5XZ'],
    
    # 分区6：安徽、河南、湖北
    'AH': ['BA6AA-BA6HZ', 'BB6AA-BB6HZ', 'BC6AA-BC6HZ', 'BD6AA-BD6HZ', 'BE6AA-BE6HZ',
           'BF6AA-BF6HZ', 'BG6AA-BG6HZ', 'BH6AA-BH6HZ', 'BI6AA-BI6HZ', 'BK6AA-BK6HZ',
           'BL6AA-BL6HZ'],
    'HA': ['BA6IA-BA6PZ', 'BB6IA-BB6PZ', 'BC6IA-BC6PZ', 'BD6IA-BD6PZ', 'BE6IA-BE6PZ',
           'BF6IA-BF6PZ', 'BG6IA-BG6PZ', 'BH6IA-BH6PZ', 'BI6IA-BI6PZ', 'BK6IA-BK6PZ',
           'BL6IA-BL6PZ'],
    'HB': ['BA6QA-BA6XZ', 'BB6QA-BB6XZ', 'BC6QA-BC6XZ', 'BD6QA-BD6XZ', 'BE6QA-BE6XZ',
           'BF6QA-BF6XZ', 'BG6QA-BG6XZ', 'BH6QA-BH6XZ', 'BI6QA-BI6XZ', 'BK6QA-BK6XZ',
           'BL6QA-BL6XZ'],
    
    # 分区7：湖南、广东、广西、海南
    'HN': ['BA7AA-BA7HZ', 'BB7AA-BB7HZ', 'BC7AA-BC7HZ', 'BD7AA-BD7HZ', 'BE7AA-BE7HZ',
           'BF7AA-BF7HZ', 'BG7AA-BG7HZ', 'BH7AA-BH7HZ', 'BI7AA-BI7HZ', 'BK7AA-BK7HZ',
           'BL7AA-BL7HZ'],
    'GD': ['BA7IA-BA7PZ', 'BB7IA-BB7PZ', 'BC7IA-BC7PZ', 'BD7IA-BD7PZ', 'BE7IA-BE7PZ',
           'BF7IA-BF7PZ', 'BG7IA-BG7PZ', 'BH7IA-BH7PZ', 'BI7IA-BI7PZ', 'BK7IA-BK7PZ',
           'BL7IA-BL7PZ'],
    'GX': ['BA7QA-BA7XZ', 'BB7QA-BB7XZ', 'BC7QA-BC7XZ', 'BD7QA-BD7XZ', 'BE7QA-BE7XZ',
           'BF7QA-BF7XZ', 'BG7QA-BG7XZ', 'BH7QA-BH7XZ', 'BI7QA-BI7XZ', 'BK7QA-BK7XZ',
           'BL7QA-BL7XZ'],
    'HI': ['BA7YA-BA7ZZ', 'BB7YA-BB7ZZ', 'BC7YA-BC7ZZ', 'BD7YA-BD7ZZ', 'BE7YA-BE7ZZ',
           'BF7YA-BF7ZZ', 'BG7YA-BG7ZZ', 'BH7YA-BH7ZZ', 'BI7YA-BI7ZZ', 'BK7YA-BK7ZZ',
           'BL7YA-BL7ZZ'],
    
    # 分区8：四川、重庆、贵州、云南
    'SC': ['BA8AA-BA8FZ', 'BB8AA-BB8FZ', 'BC8AA-BC8FZ', 'BD8AA-BD8FZ', 'BE8AA-BE8FZ',
           'BF8AA-BF8FZ', 'BG8AA-BG8FZ', 'BH8AA-BH8FZ', 'BI8AA-BI8FZ', 'BK8AA-BK8FZ',
           'BL8AA-BL8FZ'],
    'CQ': ['BA8GA-BA8LZ', 'BB8GA-BB8LZ', 'BC8GA-BC8LZ', 'BD8GA-BD8LZ', 'BE8GA-BE8LZ',
           'BF8GA-BF8LZ', 'BG8GA-BG8LZ', 'BH8GA-BH8LZ', 'BI8GA-BI8LZ', 'BK8GA-BK8LZ',
           'BL8GA-BL8LZ'],
    'GZ': ['BA8MA-BA8RZ', 'BB8MA-BB8RZ', 'BC8MA-BC8RZ', 'BD8MA-BD8RZ', 'BE8MA-BE8RZ',
           'BF8MA-BF8RZ', 'BG8MA-BG8RZ', 'BH8MA-BH8RZ', 'BI8MA-BI8RZ', 'BK8MA-BK8RZ',
           'BL8MA-BL8RZ'],
    'YN': ['BA8SA-BA8XZ', 'BB8SA-BB8XZ', 'BC8SA-BC8XZ', 'BD8SA-BD8XZ', 'BE8SA-BE8XZ',
           'BF8SA-BF8XZ', 'BG8SA-BG8XZ', 'BH8SA-BH8XZ', 'BI8SA-BI8XZ', 'BK8SA-BK8XZ',
           'BL8SA-BL8XZ'],
    
    # 分区9：陕西、甘肃、宁夏、青海
    'SN': ['BA9AA-BA9FZ', 'BB9AA-BB9FZ', 'BC9AA-BC9FZ', 'BD9AA-BD9FZ', 'BE9AA-BE9FZ',
           'BF9AA-BF9FZ', 'BG9AA-BG9FZ', 'BH9AA-BH9FZ', 'BI9AA-BI9FZ', 'BK9AA-BK9FZ',
           'BL9AA-BL9FZ'],
    'GS': ['BA9GA-BA9LZ', 'BB9GA-BB9LZ', 'BC9GA-BC9LZ', 'BD9GA-BD9LZ', 'BE9GA-BE9LZ',
           'BF9GA-BF9LZ', 'BG9GA-BG9LZ', 'BH9GA-BH9LZ', 'BI9GA-BI9LZ', 'BK9GA-BK9LZ',
           'BL9GA-BL9LZ'],
    'NX': ['BA9MA-BA9RZ', 'BB9MA-BB9RZ', 'BC9MA-BC9RZ', 'BD9MA-BD9RZ', 'BE9MA-BE9RZ',
           'BF9MA-BF9RZ', 'BG9MA-BG9RZ', 'BH9MA-BH9RZ', 'BI9MA-BI9RZ', 'BK9MA-BK9RZ',
           'BL9MA-BL9RZ'],
    'QH': ['BA9SA-BA9XZ', 'BB9SA-BB9XZ', 'BC9SA-BC9XZ', 'BD9SA-BD9XZ', 'BE9SA-BE9XZ',
           'BF9SA-BF9XZ', 'BG9SA-BG9XZ', 'BH9SA-BH9XZ', 'BI9SA-BI9XZ', 'BK9SA-BK9XZ',
           'BL9SA-BL9XZ'],
    
    # 分区0：新疆、西藏
    'XJ': ['BA0AA-BA0FZ', 'BB0AA-BB0FZ', 'BC0AA-BC0FZ', 'BD0AA-BD0FZ', 'BE0AA-BE0FZ',
           'BF0AA-BF0FZ', 'BG0AA-BG0FZ', 'BH0AA-BH0FZ', 'BI0AA-BI0FZ', 'BK0AA-BK0FZ',
           'BL0AA-BL0FZ'],
    'XZ': ['BA0GA-BA0LZ', 'BB0GA-BB0LZ', 'BC0GA-BC0LZ', 'BD0GA-BD0LZ', 'BE0GA-BE0LZ',
           'BF0GA-BF0LZ', 'BG0GA-BG0LZ', 'BH0GA-BH0LZ', 'BI0GA-BI0LZ', 'BK0GA-BK0LZ',
           'BL0GA-BL0LZ'],
    
    # 台湾、香港、澳门
    'TW': ['BV2AA-BV2XZ', 'BV9AA-BV9XZ', 'BX2AA-BX2XZ', 'BM2AA-BM2XZ'],
    'HK': ['VR2AA-VR2XZ', 'VS2AA-VS2XZ', 'VT2AA-VT2XZ'],
    'MO': ['XX9AA-XX9XZ'],
}

# 省份代码与省份名称的映射关系
PROVINCE_CODE_TO_NAME = {
    'BJ': '北京',
    'TJ': '天津',
    'HE': '河北',
    'SX': '山西',
    'NM': '内蒙古',
    'LN': '辽宁',
    'JL': '吉林',
    'HL': '黑龙江',
    'SH': '上海',
    'JS': '江苏',
    'ZJ': '浙江',
    'AH': '安徽',
    'FJ': '福建',
    'JX': '江西',
    'SD': '山东',
    'HA': '河南',
    'HB': '湖北',
    'HN': '湖南',
    'GD': '广东',
    'GX': '广西',
    'HI': '海南',
    'CQ': '重庆',
    'SC': '四川',
    'GZ': '贵州',
    'YN': '云南',
    'XZ': '西藏',
    'SN': '陕西',
    'GS': '甘肃',
    'QH': '青海',
    'NX': '宁夏',
    'XJ': '新疆',
    'TW': '台湾',
    'HK': '香港',
    'MO': '澳门',
}

# 省份名称与省份代码的映射关系
PROVINCE_NAME_TO_CODE = {
    name: code for code, name in PROVINCE_CODE_TO_NAME.items()
}


def parse_callsign_segment(segment_str):
    """解析呼号段字符串，返回起始和结束呼号
    
    Args:
        segment_str: 呼号段字符串，如 'B1A-B1X'
        
    Returns:
        tuple: (start_call, end_call)，如 ('B1A', 'B1X')
    """
    if '-' in segment_str:
        start, end = segment_str.split('-', 1)
        return start.strip(), end.strip()
    return segment_str.strip(), segment_str.strip()

def is_callsign_in_segment(callsign, start_call, end_call):
    """判断呼号是否在指定的呼号段内
    
    Args:
        callsign: 业余无线电呼号
        start_call: 呼号段起始呼号
        end_call: 呼号段结束呼号
        
    Returns:
        bool: 呼号是否在呼号段内
    """
    # 转换为大写进行比较
    callsign_upper = callsign.strip().upper()
    start_upper = start_call.upper()
    end_upper = end_call.upper()
    
    # 检查呼号是否在起始和结束呼号之间
    return start_upper <= callsign_upper <= end_upper

def get_province_by_callsign(callsign):
    """通过呼号获取对应的省份代码
    
    Args:
        callsign: 业余无线电呼号
        
    Returns:
        str: 省份代码，如 'BJ'，若未找到则返回 None
    """
    if not callsign or not isinstance(callsign, str):
        return None
    
    callsign_upper = callsign.strip().upper()
    
    # 检查是否为中国呼号（以B开头）
    if not callsign_upper.startswith('B'):
        # 检查是否为香港、澳门、台湾呼号
        if callsign_upper.startswith(('VR2', 'VS2', 'VT2')):
            return 'HK'
        elif callsign_upper.startswith(('BV', 'BX', 'BM')):
            return 'TW'
        elif callsign_upper.startswith('XX9'):
            return 'MO'
        return None
    
    # 遍历所有省份的呼号段
    for province_code, segments in CHINA_CALLSIGN_PROVINCE_MAP.items():
        for segment in segments:
            # 解析呼号段
            start_call, end_call = parse_callsign_segment(segment)
            
            # 检查呼号是否在当前呼号段内
            if is_callsign_in_segment(callsign_upper, start_call, end_call):
                return province_code
    
    return None