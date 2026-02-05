"""奖状条件检查器"""
from .conditions import AWARD_CONDITIONS
from .callsign_parser import callsign_parser

class AwardChecker:
    def __init__(self):
        self.awards = AWARD_CONDITIONS
        self.callsign_parser = callsign_parser
    
    def get_available_awards(self):
        """获取可申请的奖状列表"""
        return [{
            'code': code,
            'name': info['name'],
            'description': info['description']
        } for code, info in self.awards.items()]
    
    def check_single_award(self, award_name, records):
        """检查单个奖状条件"""
        award_info = self.awards.get(award_name.upper())
        if not award_info:
            return {'eligible': False, 'error': '奖状不存在'}
        
        # 增强记录信息（通过呼号推断国家、大洲等）
        enhanced_records = self.callsign_parser.enhance_records(records)
        
        results = []
        eligible = True
        
        for condition in award_info['conditions']:
            condition_result = self._check_condition(condition, enhanced_records, award_name.upper())
            results.append(condition_result)
            if not condition_result['met']:
                eligible = False
        
        # 计算增强记录数，根据不同奖状的要求
        if award_name.upper() == 'WAPC':
            # WAPC: 识别state字段，有多少条显示多少条（不去重）
            enhanced_count = len([r for r in enhanced_records if r.get('state')])
        elif award_name.upper() == 'WACZ':
            # WACZ: 识别对方的dxcc字段（不是MY_DXCC），显示有多少条dxcc为318
            enhanced_count = len([r for r in enhanced_records 
                                if str(r.get('dxcc') or r.get('DXCC')) == '318'])
        elif award_name.upper() == 'DXCC':
            # DXCC: 识别对方的dxcc字段（不是MY_DXCC），去除重复的，排除dxcc0和自己的DXCC代码
            unique_dxcc = set()
            # 获取操作者自己的DXCC代码（通常是318代表中国）
            own_dxcc = None
            for r in enhanced_records:
                my_dxcc = r.get('my_dxcc') or r.get('MY_DXCC')
                if my_dxcc:
                    own_dxcc = str(my_dxcc)
                    break
            
            for r in enhanced_records:
                # 获取对方的DXCC（忽略MY_DXCC）
                dxcc = r.get('dxcc') or r.get('DXCC')
                if dxcc:
                    dxcc_str = str(dxcc)
                    # 只接受数字形式的DXCC代码，排除dxcc0
                    if dxcc_str.isdigit() and dxcc_str != '0':
                        unique_dxcc.add(dxcc_str)
            enhanced_count = len(unique_dxcc)
        else:
            # 其他奖状保持原有逻辑
            enhanced_count = len([r for r in enhanced_records if any(r.get(k) for k in ['country', 'continent', 'dxcc'])])
        
        # 计算唯一通联记录数（按呼号和日期）
        unique_contacts = set()
        for record in records:
            call = record.get('call') or record.get('CALL')
            date = record.get('qso_date') or record.get('QSO_DATE')
            if call and date:
                unique_contacts.add(f"{call}_{date}")
        
        return {
            'award': award_info['name'],
            'eligible': eligible,
            'conditions': results,
            'records_analyzed': len(records),
            'unique_contacts': len(unique_contacts),
            'enhanced_records_count': enhanced_count,
            'basic_records_count': len(records) - enhanced_count,
        }
    
    def check_all_awards(self, records):
        """检查所有奖状条件"""
        results = {}
        for award_name in self.awards:
            results[award_name] = self.check_single_award(award_name, records)
        return results
    
    def _check_condition(self, condition, records, award_name=None):
        """检查单个条件"""
        condition_type = condition['type']
        
        if condition_type == 'state_count':
            return self._check_state_count(condition, records, award_name)
        elif condition_type == 'dxcc_count':
            return self._check_dxcc_count(condition, records)
        elif condition_type == 'china_zone_count':
            return self._check_china_zone_count(condition, records)
        else:
            return {'met': False, 'message': f'未知条件类型: {condition_type}'}
    
    def _check_state_count(self, condition, records, award_name=None):
        """检查省份/地区数量条件"""
        target_states = condition.get('states', [])
        target_count = condition.get('target', 0)
        
        unique_states = set()
        for record in records:
            state = record.get('state') or record.get('us_state')
            if state and state.upper() in target_states:
                unique_states.add(state.upper())
        
        met = len(unique_states) >= target_count
        
        # 检查是否为WAPC奖条件（根据目标省份代码列表）
        is_wapc = any(state in ['BJ', 'TJ', 'HE', 'SX', 'NM', 'LN', 'JL', 'HL', 'SH', 'JS', 
                               'ZJ', 'AH', 'FJ', 'JX', 'SD', 'HA', 'HB', 'HN', 'GD', 'GX',
                               'HI', 'CQ', 'SC', 'GZ', 'YN', 'XZ', 'SN', 'GS', 'QH', 'NX',
                               'XJ', 'TW', 'HK', 'MO'] for state in target_states)
        
        # 根据是否为WAPC奖选择合适的消息
        if is_wapc:
            message = f'已通联 {len(unique_states)}/{target_count} 个行政区'
            # 收集已通联和未通联的省份
            connected_states = sorted(list(unique_states))
            missing_states = sorted([s for s in target_states if s not in unique_states])
        else:
            message = f'已通联 {len(unique_states)}/{target_count} 个州'
            connected_states = []
            missing_states = []
        
        return {
            'met': met,
            'current': len(unique_states),
            'target': target_count,
            'message': message,
            'connected_states': connected_states,
            'missing_states': missing_states,
            'states': target_states  # 添加states字段确保模板能访问到
        }
    
    def _check_dxcc_count(self, condition, records):
        """检查DXCC实体数量条件（回退：若无 dxcc 则以 country 计数）"""
        # 获取通联的DXCC实体数量（确保只使用对方的DXCC，忽略MY_DXCC，排除dxcc0和自己的DXCC代码）
        unique_dxcc = set()
        
        # 获取操作者自己的DXCC代码（从MY_DXCC字段）
        own_dxcc = None
        for record in records:
            my_dxcc = record.get('my_dxcc') or record.get('MY_DXCC')
            if my_dxcc:
                own_dxcc = str(my_dxcc)
                break
        
        for record in records:
            # 获取对方的DXCC（优先使用直接的DXCC字段，排除MY_DXCC）
            dxcc = record.get('dxcc') or record.get('DXCC')
            if dxcc:
                dxcc_str = str(dxcc)
                # 只接受数字形式的DXCC代码，排除dxcc0
                if dxcc_str.isdigit() and dxcc_str != '0':
                    unique_dxcc.add(dxcc_str)
            else:
                # 如果没有DXCC字段，通过呼号解析获取
                callsign = record.get('call') or record.get('CALL')
                if callsign and self.callsign_parser:
                    info = self.callsign_parser.parse_callsign(callsign)
                    dxcc = info.get('dxcc')
                    if dxcc:
                        dxcc_str = str(dxcc)
                        # 只接受数字形式的DXCC代码，排除dxcc0
                        if dxcc_str.isdigit() and dxcc_str != '0':
                            unique_dxcc.add(dxcc_str)
        
        current_count = len(unique_dxcc)
        
        # 检查是否有多个目标值
        if 'targets' in condition:
            targets = sorted(condition['targets'])
            phases = condition.get('phases', [])
            
            # 找到最大的已完成目标
            met_targets = [t for t in targets if current_count >= t]
            max_met_target = max(met_targets) if met_targets else 0
            
            # 找到下一个目标
            next_targets = [t for t in targets if current_count < t]
            next_target = min(next_targets) if next_targets else max(targets)
            
            # 确定当前阶段
            current_phase = ""
            if max_met_target > 0:
                idx = targets.index(max_met_target)
                if idx < len(phases):
                    current_phase = phases[idx]
            
            # 生成消息
            message = f'已通联 {current_count} 个DXCC实体'
            if max_met_target > 0:
                message += f'，已完成{max_met_target}个实体的{current_phase}'
            message += f'，下一个目标：{next_target}个实体'
            
            result = {
                'met': len(met_targets) > 0,  # 至少完成一个阶段
                'current': current_count,
                'target': next_target,  # 显示下一个目标
                'message': message,
                'met_targets': met_targets,  # 添加已完成的目标列表
                'current_phase': current_phase,  # 添加当前阶段
                'max_met_target': max_met_target  # 添加最大已完成目标
            }
                
            return result
        else:
            # 兼容旧的单目标格式
            target_count = condition.get('target', 0)
            met = current_count >= target_count
            
            # 构建结果
            result = {
                'met': met,
                'current': current_count,
                'target': target_count,
                'message': f'已通联 {current_count}/{target_count} 个DXCC实体'
            }
            
            return result
    
    def _check_continent_count(self, condition, records):
        """检查大洲数量条件（回退：若无 continent 则基于 country/呼号推断）"""
        target_continents = condition.get('continents', [])
        target_count = condition.get('target', 0)
        
        unique_continents = set()
        for record in records:
            continent = record.get('continent')
            if not continent:
                callsign = record.get('call') or record.get('CALL')
                if callsign and self.callsign_parser:
                    info = self.callsign_parser.parse_callsign(callsign)
                    continent = info.get('continent')
                else:
                    country = record.get('country')
                    if country and self.callsign_parser:
                        info = self.callsign_parser.parse_callsign(country)
                        continent = info.get('continent')

            if continent:
                c = str(continent).upper()
                if not target_continents or c in [t.upper() for t in target_continents]:
                    unique_continents.add(c)
        
        met = len(unique_continents) >= target_count
        return {
            'met': met,
            'current': len(unique_continents),
            'target': target_count,
            'message': f'已通联 {len(unique_continents)}/{target_count} 个大洲'
        }
    
    def _check_grid_count(self, condition, records):
        """检查网格数量条件"""
        target_bands = condition.get('bands', [])
        target_count = condition.get('target', 0)
        
        unique_grids = set()
        for record in records:
            band = record.get('band')
            grid = record.get('gridsquare')
            if (band and band.upper() in target_bands) and grid:
                unique_grids.add(grid.upper())
        
        met = len(unique_grids) >= target_count
        return {
            'met': met,
            'current': len(unique_grids),
            'target': target_count,
            'message': f'在指定波段已通联 {len(unique_grids)}/{target_count} 个网格'
        }
    
    def _check_cq_zone_count(self, condition, records):
        """检查CQ区域数量条件"""
        target_bands = condition.get('bands', [])
        target_count = condition.get('target', 0)
        
        unique_zones = set()
        for record in records:
            band = record.get('band')
            cq_zone = record.get('cqzone') or record.get('cq_zone')
            if (band and band.upper() in target_bands) and cq_zone:
                unique_zones.add(str(cq_zone))
        
        met = len(unique_zones) >= target_count
        return {
            'met': met,
            'current': len(unique_zones),
            'target': target_count,
            'message': f'在指定波段已通联 {len(unique_zones)}/{target_count} 个CQ区域'
        }
    
    def _check_china_zone_count(self, condition, records):
        """检查中国大陆0-9区通联条件"""
        import re
        target_count = condition.get('target', 10)
        
        # 提取通联的中国大陆分区（B0-B9），只处理对方DXCC为318的记录
        unique_zones = set()
        for record in records:
            # 检查对方的DXCC是否为318（中国大陆）
            dxcc = record.get('dxcc') or record.get('DXCC')
            if dxcc and str(dxcc) == '318':
                call = record.get('call') or record.get('CALL')
                if call:
                    # 转换为大写便于统一处理
                    call_upper = call.upper()
                    # 使用正则表达式提取B后面的第一个数字
                    match = re.search(r'B[^\d]*(\d)', call_upper)
                    if match:
                        zone_char = match.group(1)
                        unique_zones.add(zone_char)
                        # 调试：输出识别到的分区
                        print(f"识别到分区: {zone_char}, 来自呼号: {call}, DXCC: {dxcc}")
        
        current_count = len(unique_zones)
        met = current_count >= target_count
        
        # 调试：输出最终结果
        print(f"WACZ检查结果: 当前分区数={current_count}, 目标={target_count}, 已通联分区={unique_zones}, 缺失分区={[str(z) for z in range(10) if str(z) not in unique_zones]}")
        
        return {
            'met': met,
            'current': current_count,
            'target': target_count,
            'message': f'已通联中国大陆 {current_count}/{target_count} 个分区（0-9区）',
            'connected_zones': sorted(unique_zones),
            'missing_zones': [str(z) for z in range(10) if str(z) not in unique_zones]
        }