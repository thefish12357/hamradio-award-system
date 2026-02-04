# 业余无线电奖状申请系统

一个基于 Flask 的业余无线电奖状申请系统，支持解析 LOTW 导出的 ADIF 日志文件并检查各种奖状的申请条件。
使用trae生成，使用请注意代码准确

## 功能特性

- **ADIF 文件解析**：支持解析 LOTW 导出的详细版本 ADIF 日志文件，处理大文件更高效
- **奖状条件检查**：支持多种业余无线电奖状的条件检查
  - WAPC（中国各省份通联奖状）
  - WACZ（中国大陆0-9区通联奖状，显示DXCC 318标识）
  - DXCC（不同DXCC实体通联奖状，支持多阶段，排除DXCC0）
- **呼号识别**：自动识别呼号对应的国家、省份、分区等信息
- **用户友好界面**：基于 Flask 的 Web 界面，易于使用
- **近乎准确的DXCC计数**：只计算有效的数字形式DXCC代码，排除非数字值和DXCC0（某些文件会显示dxcc数量增多或减少3-5个）

## 安装和运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python app.py
```

应用将在 http://127.0.0.1:5000 启动。

## 使用说明

1. **上传日志**：在首页点击"上传日志"按钮，选择从 LOTW 导出的详细版本 ADIF 文件（导出日志时需要选择下方详细信息，没有选中会计算错误）
2. **查看结果**：系统自动解析日志并显示各奖状的申请条件满足情况
3. **申请奖状**：选择符合条件的奖状进行申请

## 日志文件要求

- 必须是从 LOTW (Logbook of the World) 导出的 ADIF 文件
- 必须是详细版本，文件第三行应包含 "for 呼号" 格式的信息
- 文件应包含实际的通联记录

## 项目结构

```
.
├── awards/          # 奖状相关模块
│   ├── callsign_parser.py       # 呼号解析器
│   ├── checker.py               # 奖状条件检查器
│   ├── china_callsign_province_map.py  # 中国呼号省份映射
│   └── conditions.py            # 奖状条件定义
├── src/             # 核心模块
│   └── adif_parser/             # ADIF 解析器
├── static/          # 静态资源
├── templates/       # 网页模板
├── app.py           # 主应用文件
├── cty.dat          # 呼号前缀数据文件
└── requirements.txt # 依赖列表
```

## 开发说明

### 主要模块

- **app.py**：Flask 应用主入口，处理 HTTP 请求和响应
- **awards/checker.py**：奖状条件检查逻辑
- **src/adif_parser/parser.py**：ADIF 文件解析逻辑
- **templates/**：Jinja2 模板文件

### 添加新奖状

1. 在 `awards/conditions.py` 中定义新奖状的条件
2. 在 `awards/checker.py` 中添加条件检查逻辑
3. 更新模板文件以显示新奖状的信息

## 注意事项

- 本系统仅用于检查奖状申请条件，不实际提交申请
- 请确保上传的日志文件符合 LOTW 详细版本的格式要求
- 系统会自动识别呼号信息，但可能存在识别错误的情况

## 鸣谢

感谢以下业余无线电爱好者提供的测试数据和支持：

- **BD4SDO**
- **BG7LFX**
- **BG7QIW**
- **BG7XWF**
- **BI4IVE**
- **BH2VSQ**
- **BH7GZB**
- **BH7HHR**

## 许可证


MIT License

