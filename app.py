from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import tempfile
import shutil
import sys
import json
import uuid
from datetime import datetime
import base64

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.adif_parser.parser import parse_adif
from awards.checker import AwardChecker
import json

app = Flask(__name__)
# 配置Flask会话
app.secret_key = 'ham_awards_secret_key'
# 会话配置

# 初始化奖状检查器
award_checker = AwardChecker()

@app.route('/')
def index():
    """首页 - 显示可申请的奖状列表"""
    awards = award_checker.get_available_awards()
    return render_template('index.html', awards=awards)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """文件上传页面"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('请选择要上传的文件')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('请选择要上传的文件')
            return redirect(request.url)
        
        if file and file.filename.lower().endswith('.adi'):
            temp_dir = None
            temp_file_path = None
            try:
                # 创建临时目录来保存上传文件的副本
                temp_dir = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir, 'uploaded_file.adi')
                
                # 保存上传的文件副本（服务器端临时文件）
                file.save(temp_file_path)
                
                # 读取文件内容（同时获取所有行用于后续处理）
                with open(temp_file_path, 'r', encoding='utf-8') as f:
                    adif_lines = f.readlines()
                    adif_content = ''.join(adif_lines)
                
                # 检查是否为LOTW下载的文件
                if 'Logbook of the World' not in adif_content:
                    flash('请上传从 lotw.arrl.org 下载的ADIF日志文件。')
                    flash('LOTW日志文件通常包含 "ProgramID: Logbook of the World" 等标识信息。')
                    flash('您可以访问 https://lotw.arrl.org 下载您的日志文件。')
                    return redirect(url_for('upload_file'))
                
                # 从第三行提取申请奖状的呼号（格式：for XXX）
                import re
                own_call_from_third_line = None
                if len(adif_lines) >= 3:
                    third_line = adif_lines[2].strip()  # 索引从0开始，第三行是索引2
                    for_match = re.search(r'for\s+([A-Za-z0-9/]+)', third_line, re.IGNORECASE)
                    if for_match:
                        own_call_from_third_line = for_match.group(1).strip()
                
                # 检查是否成功从第三行提取呼号
                if not own_call_from_third_line:
                    flash('请上传LOTW导出的详细版本日志文件。')
                    flash('详细版本的第三行应该包含 "for 呼号" 格式的信息。')
                    flash('您可以在LOTW导出界面选择 "我的站台" 或 "他人站台" 的详细数据选项。')
                    return redirect(url_for('upload_file'))
                
                # 提取呼号（只使用第三行的for XXX信息）并转换为大写
                own_call_from_owncall = own_call_from_third_line.upper()
                
                # 解析ADIF文件
                header, records = parse_adif(adif_content)
                
                # 检查是否为详细日志（包含APP_LoTW_DXCC_ENTITY_STATUS字段）
                is_detailed_log = False
                for record in records:
                    if 'app_lotw_dxcc_entity_status' in record:
                        is_detailed_log = True
                        break
                
                # 如果不是详细日志，报错并提醒用户
                if not is_detailed_log:
                    flash('请上传LOTW导出的详细版本日志文件。')
                    flash('详细版本的日志记录应该包含APP_LoTW_DXCC_ENTITY_STATUS、GRIDSQUARE等详细信息。')
                    flash('您可以在LOTW导出界面选择 "详细" 或 "包含所有信息" 的导出选项。')
                    return redirect(url_for('upload_file'))
                
                # 提取主体呼号（own call sign）
                # 1. 优先使用从OWNCALL:号段提取的呼号（这是申请奖状的呼号）
                own_call = own_call_from_owncall
                
                # 2. 如果OWNCALL:提取失败，尝试使用APP_LoTW_OWNCALL（头部或记录）
                if not own_call:
                    if header.get('app_lotw_owncall'):
                        own_call = header['app_lotw_owncall']
                    elif records:
                        for record in records:
                            if record.get('app_lotw_owncall'):
                                own_call = record['app_lotw_owncall']
                                break
                
                # 3. 如果以上都没有，尝试使用STATION_CALLSIGN（头部或记录）
                if not own_call:
                    if header.get('station_callsign'):
                        own_call = header['station_callsign']
                    elif records:
                        for record in records:
                            if record.get('station_callsign'):
                                own_call = record['station_callsign']
                                break
                
                # 4. 如果以上都没有，使用MYCALL或CALL作为后备
                if not own_call:
                    if header.get('mycall'):
                        own_call = header['mycall']
                
                # 如果是列表，取第一个值
                if isinstance(own_call, list) and own_call:
                    own_call = own_call[0]
                
                # 检查奖状条件（自动增强非标准日志）
                results = award_checker.check_all_awards(records)
                
                # 将日志和结果保存到会话中
                # 使用JSON序列化来确保复杂对象能够正确存储
                try:
                    # 只保存必要的数据到会话中，避免cookie过大
                    session['records_count'] = len(records)
                    if own_call:
                        session['own_call'] = own_call
                    # 简化results对象，只保留必要信息
                    simplified_results = {}
                    for award_name, award_data in results.items():
                        simplified_results[award_name] = {
                            'award': award_data['award'],
                            'eligible': award_data['eligible'],
                            'conditions': award_data['conditions'],
                            'records_analyzed': award_data['records_analyzed'],
                            'enhanced_records_count': award_data['enhanced_records_count'],
                            'unique_contacts': award_data.get('unique_contacts', len(records))
                        }
                    # 确保数据正确序列化
                    session['results'] = json.dumps(simplified_results, default=str)
                    # 检查会话数据是否正确保存
                    print(f"会话数据已保存: records_count={session.get('records_count')}, results={session.get('results')}")
                    # 设置会话为永久会话
                    session.permanent = True
                except Exception as e:
                    print(f"保存会话数据时出错: {e}")
                
                # 显示处理结果
                return redirect(url_for('show_results'))
                
            except Exception as e:
                flash(f'文件处理错误: {str(e)}')
                return redirect(request.url)
            finally:
                # 重要：只删除服务器上的临时副本，不删除用户本地文件
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass  # 忽略删除错误
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass  # 忽略删除错误
        else:
            flash('请上传ADIF格式的文件(.adi)')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/results')
def show_results():
    """显示日志处理结果页面"""
    # 从会话中获取数据
    records_count = session.get('records_count', 0)
    results_json = session.get('results', '{}')
    
    # 调试：打印会话数据
    print(f"从会话获取数据: records_count={records_count}, results_json={results_json}")
    print(f"会话中的所有键: {list(session.keys())}")
    
    # 如果会话中没有数据，重定向到上传页面
    if not records_count or results_json == '{}':
        flash('请先上传日志文件')
        return redirect(url_for('upload_file'))
    
    # 获取省份代码映射
    from awards.china_callsign_province_map import PROVINCE_CODE_TO_NAME
    
    # 获取主体呼号
    own_call = session.get('own_call')
    
    # 反序列化JSON数据
    try:
        results = json.loads(results_json)
    except json.JSONDecodeError:
        flash('数据解析错误')
        return redirect(url_for('upload_file'))
    
    return render_template('results.html', 
                         records_count=records_count,
                         results=results,
                         province_map=PROVINCE_CODE_TO_NAME,
                         own_call=own_call)

@app.route('/design')
def design_award():
    """奖状设计页面"""
    # 传入可用奖状列表以供模板选择
    awards = award_checker.get_available_awards()
    return render_template('design.html', awards=awards)

@app.route('/get_award', methods=['GET', 'POST'])
def get_award():
    """获取奖状页面"""
    if request.method == 'POST':
        # 从表单获取选择的奖状代码
        award_code = request.form.get('award_code')
        
        # 如果选择了所有奖状
        if award_code == 'all':
            # 获取会话中的结果数据
            results_json = session.get('results', '{}')
            if results_json == '{}':
                flash('请先上传日志文件')
                return redirect(url_for('upload_file'))
            
            try:
                results = json.loads(results_json)
            except json.JSONDecodeError:
                flash('数据解析错误')
                return redirect(url_for('upload_file'))
            
            # 收集所有符合条件的奖状代码
            eligible_awards = []
            for code, result in results.items():
                if result['eligible']:
                    if code == 'DXCC':
                        # 处理DXCC的多阶段奖状
                        for condition in result['conditions']:
                            if 'met_targets' in condition:
                                for target in condition['met_targets']:
                                    eligible_awards.append(f"{code}{target}")
                    else:
                        eligible_awards.append(code)
            
            # 这里可以添加生成所有奖状的逻辑
            return render_template('get_award.html', 
                                  award_code='all',
                                  eligible_awards=eligible_awards,
                                  base_award_code='all')
        
        # 处理单个奖状选择
        elif award_code:
            # 解析奖状代码，支持带数字的格式，如DXCC10, DXCC50等
            base_award_code = award_code
            target_number = None
            
            # 检查是否为带数字的DXCC奖状
            if award_code.startswith('DXCC') and len(award_code) > 4:
                base_award_code = 'DXCC'
                try:
                    target_number = int(award_code[4:])
                except ValueError:
                    pass
            
            # 这里可以添加生成单个奖状的逻辑
            return render_template('get_award.html', 
                                  award_code=award_code,
                                  base_award_code=base_award_code,
                                  target_number=target_number)
        
    # 处理GET请求（兼容旧链接）
    award_code = request.args.get('award_code')
    if award_code:
        # 解析奖状代码，支持带数字的格式，如DXCC10, DXCC50等
        base_award_code = award_code
        target_number = None
        
        # 检查是否为带数字的DXCC奖状
        if award_code.startswith('DXCC') and len(award_code) > 4:
            base_award_code = 'DXCC'
            try:
                target_number = int(award_code[4:])
            except ValueError:
                pass
        
        # 这里可以添加生成奖状的逻辑
        return render_template('get_award.html', 
                              award_code=award_code,
                              base_award_code=base_award_code,
                              target_number=target_number)
    
    # 如果没有指定奖状代码，重定向到结果页面
    flash('请选择要获取的奖状')
    return redirect(url_for('show_results'))


    


@app.route('/api/check_award', methods=['POST'])
def api_check_award():
    """API接口：检查单个奖状条件"""
    data = request.get_json()
    award_name = data.get('award_name')
    records = data.get('records', [])
    
    result = award_checker.check_single_award(award_name, records)
    return jsonify(result)

@app.route('/save_template', methods=['POST'])
def save_template():
    """保存奖状模板"""
    try:
        # 支持 multipart/form-data 提交：包含字段 template (json字符串)、award_code，以及可选的 background_file、logo_file
        award_code = request.form.get('award_code')
        template_json = request.form.get('template')
        if not award_code:
            return jsonify({'success': False, 'message': '缺少 award_code'})
        if not template_json:
            return jsonify({'success': False, 'message': '缺少 template 数据'})

        try:
            template_data = json.loads(template_json)
        except Exception as e:
            return jsonify({'success': False, 'message': f'模板 JSON 解析错误: {e}'})

        # 创建奖状对应的文件夹
        base_dir = os.path.dirname(__file__)
        templates_dir = os.path.join(base_dir, 'award_templates')
        backgrounds_dir = os.path.join(base_dir, 'static', 'award_backgrounds')
        logos_dir = os.path.join(base_dir, 'static', 'award_logos')

        for d in (templates_dir, backgrounds_dir, logos_dir):
            if not os.path.exists(d):
                os.makedirs(d)

        # 每个奖状使用自己的子目录（按 award_code）
        award_template_dir = os.path.join(templates_dir, award_code)
        award_background_dir = os.path.join(backgrounds_dir, award_code)
        award_logo_dir = os.path.join(logos_dir, award_code)
        for d in (award_template_dir, award_background_dir, award_logo_dir):
            if not os.path.exists(d):
                os.makedirs(d)

        # 保存模板文件为 template.json
        template_path = os.path.join(award_template_dir, 'template.json')
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)

        # 处理背景文件和 logo 文件
        # 背景文件字段名: background_file
        if 'background_file' in request.files:
            bg = request.files['background_file']
            if bg and bg.filename:
                bg_filename = bg.filename
                bg_path = os.path.join(award_background_dir, bg_filename)
                bg.save(bg_path)
                # 在模板数据中保存相对路径（相对于 app 根目录）
                template_data.setdefault('background', {})
                # 使用 static 子目录可通过 url_for 访问
                template_data['background']['image'] = url_for('static', filename=f"award_backgrounds/{award_code}/{bg_filename}")
                # 更新保存后的 template.json
                with open(template_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, ensure_ascii=False, indent=2)

        # logo 文件字段名: logo_file
        if 'logo_file' in request.files:
            lg = request.files['logo_file']
            if lg and lg.filename:
                lg_filename = lg.filename
                lg_path = os.path.join(award_logo_dir, lg_filename)
                lg.save(lg_path)
                # 可在模板数据中记录 logo 路径
                template_data.setdefault('logo', {})
                template_data['logo']['path'] = url_for('static', filename=f"award_logos/{award_code}/{lg_filename}")
                with open(template_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True, 'award_code': award_code})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/generate_award/<award_code>', methods=['POST'])
def generate_award(award_code):
    """生成奖状的API接口"""
    try:
        # 获取表单数据
        format = request.form.get('format', 'html')
        
        # 获取会话中的结果数据
        results_json = session.get('results', '{}')
        if results_json == '{}':
            return jsonify({'status': 'error', 'message': '请先上传日志文件'})
        
        # 解析结果数据
        results = json.loads(results_json)
        
        # 获取主体呼号
        own_call = session.get('own_call')
        
        # 获取当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # 生成唯一的奖状编号
        award_number = f'AWARD-{str(uuid.uuid4())[:8].upper()}'
        
        # 获取对应奖状的模板数据（按 award_code 子目录查找 template.json）
        base_dir = os.path.dirname(__file__)
        template_path = os.path.join(base_dir, 'award_templates', award_code, 'template.json')
        template_data = None
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
        
        # 生成HTML奖状
        html_content = generate_award_html(award_code, own_call, award_number, current_date, template_data)
        
        # 生成临时文件路径
        temp_dir = tempfile.gettempdir()
        filename = f'award_{award_code}_{own_call}.html'
        filepath = os.path.join(temp_dir, filename)
        
        # 保存HTML文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 返回奖状文件路径
        return jsonify({'status': 'success', 'message': '奖状生成成功', 'award_code': award_code, 'file_path': filepath})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/delete_asset', methods=['POST'])
def delete_asset():
    """删除已保存的模板资产（背景或 logo）"""
    try:
        data = request.get_json()
        award_code = data.get('award_code')
        asset_type = data.get('asset_type')  # 'background' or 'logo'
        filename = data.get('filename')
        if not award_code or not asset_type or not filename:
            return jsonify({'success': False, 'message': '缺少参数'})

        base_dir = os.path.dirname(__file__)
        if asset_type == 'background':
            path = os.path.join(base_dir, 'static', 'award_backgrounds', award_code, filename)
            static_rel = f"award_backgrounds/{award_code}/{filename}"
        elif asset_type == 'logo':
            path = os.path.join(base_dir, 'static', 'award_logos', award_code, filename)
            static_rel = f"award_logos/{award_code}/{filename}"
        else:
            return jsonify({'success': False, 'message': '未知的 asset_type'})

        if os.path.exists(path):
            os.remove(path)
        else:
            return jsonify({'success': False, 'message': '文件不存在'})

        # 如果模板存在，尝试更新 template.json 去除引用
        template_path = os.path.join(base_dir, 'award_templates', award_code, 'template.json')
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                changed = False
                if asset_type == 'background' and template_data.get('background'):
                    img = template_data['background'].get('image','')
                    if static_rel in img:
                        template_data['background']['image'] = ''
                        changed = True
                if asset_type == 'logo' and template_data.get('logo'):
                    lp = template_data['logo'].get('path','')
                    if static_rel in lp:
                        template_data['logo']['path'] = ''
                        changed = True
                if changed:
                    with open(template_path, 'w', encoding='utf-8') as f:
                        json.dump(template_data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


def generate_award_html(award_code, recipient, award_number, date, template_data):
    """生成HTML格式的奖状"""
    # 默认背景设置
    background_color = '#ffffff'
    background_image = ''
    
    # 如果有模板数据，使用模板数据
    if template_data and template_data['background']:
        background_color = template_data['background'].get('color', '#ffffff')
        background_image = template_data['background'].get('image', '')
    
    # 生成元素HTML
    elements_html = ''
    if template_data and template_data['elements']:
        for element in template_data['elements']:
            # 替换占位符内容
            text = element['text']
            if element['type'] == 'recipient' and recipient:
                text = recipient
            elif element['type'] == 'award-number':
                text = award_number
            elif element['type'] == 'date':
                text = date
            elif element['type'] == 'project':
                text = award_code
            
            # 设置样式
            font = element.get('font', 'Arial')
            font_size = element.get('size', '16')
            color = element.get('color', '#000000')
            bold = 'bold' if element.get('bold', False) else 'normal'
            italic = 'italic' if element.get('italic', False) else 'normal'
            underline = 'underline' if element.get('underline', False) else 'none'
            
            # 设置位置
            x = element['x']
            y = element['y']
            
            # 生成元素HTML
            elements_html += f'''<div style="position: absolute; left: {x}px; top: {y}px; font-family: {font}; font-size: {font_size}px; color: {color}; font-weight: {bold}; font-style: {italic}; text-decoration: {underline};">{text}</div>'''
    else:
        # 默认元素布局
        elements_html = f'''<div style="position: absolute; left: 200px; top: 100px; font-family: 'Microsoft YaHei'; font-size: 48px; color: #333; font-weight: bold; text-align: center; width: 400px;">奖状</div>
        <div style="position: absolute; left: 150px; top: 200px; font-family: 'Microsoft YaHei'; font-size: 24px; color: #666; text-align: center; width: 500px;">祝贺</div>
        <div style="position: absolute; left: 200px; top: 250px; font-family: 'Microsoft YaHei'; font-size: 36px; color: #d35400; font-weight: bold; text-align: center; width: 400px;">{recipient}</div>
        <div style="position: absolute; left: 150px; top: 320px; font-family: 'Microsoft YaHei'; font-size: 24px; color: #666; text-align: center; width: 500px;">获得</div>
        <div style="position: absolute; left: 200px; top: 370px; font-family: 'Microsoft YaHei'; font-size: 32px; color: #27ae60; font-weight: bold; text-align: center; width: 400px;">{award_code}</div>
        <div style="position: absolute; left: 150px; top: 430px; font-family: 'Microsoft YaHei'; font-size: 18px; color: #666; text-align: center; width: 500px;">奖状编号：{award_number}</div>
        <div style="position: absolute; left: 150px; top: 460px; font-family: 'Microsoft YaHei'; font-size: 18px; color: #666; text-align: center; width: 500px;">颁发日期：{date}</div>'''
    
    # 生成完整的HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>奖状 - {award_code}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }}
        #award-container {{
            width: 842px;
            height: 595px;
            margin: 0 auto;
            padding: 20px;
            background-color: {background_color};
            {f'background-image: {background_image};' if background_image else ''}
            background-size: cover;
            background-position: center;
            position: relative;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <div id="award-container">
        {elements_html}
    </div>
</body>
</html>'''
    
    return html_content

if __name__ == '__main__':
    # 确保模板目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 确保奖状模板目录存在
    template_dir = os.path.join(os.path.dirname(__file__), 'award_templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    # 确保用于存放背景和 logo 的 static 子目录存在
    static_bg = os.path.join(os.path.dirname(__file__), 'static', 'award_backgrounds')
    static_logo = os.path.join(os.path.dirname(__file__), 'static', 'award_logos')
    for d in (static_bg, static_logo):
        if not os.path.exists(d):
            os.makedirs(d)
    
    app.run(debug=True, host='127.0.0.1', port=5000)