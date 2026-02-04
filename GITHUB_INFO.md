# GitHub仓库创建信息

## 仓库信息

### 仓库名称
建议使用：`ham-radio-award-system`

### 仓库描述
```
基于Flask的业余无线电奖状申请系统，支持解析LOTW导出的ADIF日志文件并检查各种奖状的申请条件。
```

### 仓库类型
- 选择 **Public** (公开)
- 勾选 **Initialize this repository with a README** (可选)

## 初始化和推送命令

### 1. 初始化Git仓库
```bash
git init
```

### 2. 添加所有文件
```bash
git add .
```

### 3. 提交初始版本
```bash
git commit -m "Initial commit - 业余无线电奖状申请系统"
```

### 4. 添加远程仓库
```bash
git remote add origin https://github.com/[您的GitHub用户名]/ham-radio-award-system.git
```

### 5. 推送代码
```bash
git push -u origin main
```

## 其他信息

### 已包含的文件
- `.gitignore`: Python项目标准忽略文件
- `README.md`: 完整的项目文档
- 所有核心代码和资源文件

### 项目结构
```
.
├── awards/          # 奖状相关模块
├── src/             # 核心模块
├── static/          # 静态资源
├── templates/       # 网页模板
├── README.md        # 项目文档
├── app.py           # 主应用文件
├── cty.dat          # 呼号前缀数据文件
└── requirements.txt # 依赖列表
```

### 许可证
项目使用 MIT License

## 注意事项

1. 请将 `[您的GitHub用户名]` 替换为您实际的GitHub用户名
2. 确保您已经安装并配置了Git
3. 确保您有GitHub账号的推送权限