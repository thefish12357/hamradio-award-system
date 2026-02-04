"""奖状条件定义"""

# 常见业余无线电奖状条件
AWARD_CONDITIONS = {
    'DXCC': {
        'name': 'DX Century Club (DXCC)',
        'description': '通联不同数量的DXCC实体',
        'conditions': [
            {
                'type': 'dxcc_count',
                'targets': [10, 50, 100],
                'phases': ['初级阶段', '中级阶段', '高级阶段']
            }
        ]
    },
    'WAPC': {
        'name': 'Worked All Chinese Provinces (WAPC)',
        'description': '通联中国所有行政区',
        'conditions': [
            {
                'type': 'state_count',
                'target': 34,
                'states': ['BJ', 'TJ', 'HE', 'SX', 'NM', 'LN', 'JL', 'HL', 'SH', 'JS', 
                          'ZJ', 'AH', 'FJ', 'JX', 'SD', 'HA', 'HB', 'HN', 'GD', 'GX',
                          'HI', 'CQ', 'SC', 'GZ', 'YN', 'XZ', 'SN', 'GS', 'QH', 'NX',
                          'XJ', 'TW', 'HK', 'MO']
            }
        ]
    },
    'WACZ': {
        'name': 'Worked All China Zones (WACZ)',
        'description': '通联中国大陆所有0-9分区',
        'conditions': [
            {
                'type': 'china_zone_count',
                'target': 10
            }
        ]
    }
}

def get_award_condition(award_name):
    """获取奖状条件"""
    return AWARD_CONDITIONS.get(award_name.upper())