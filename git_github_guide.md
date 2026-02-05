# 使用Git History扩展将文件同步到GitHub的步骤

## 前置条件
- 已安装Git History扩展
- 已在GitHub创建仓库
- 项目目录：`c:\ham text\1\`

## 步骤1：初始化Git仓库（如果尚未初始化）
1. 打开VS Code，进入项目目录
2. 按下 `Ctrl+Shift+P` 打开命令面板
3. 输入 `Git: Initialize Repository` 并回车
4. 选择当前项目目录作为仓库位置

## 步骤2：配置Git用户信息
1. 打开命令面板
2. 输入 `Git: Configure User Name` 并回车，输入你的GitHub用户名
3. 输入 `Git: Configure User Email` 并回车，输入你的GitHub邮箱

## 步骤3：添加远程仓库
1. 打开Git History扩展（左侧活动栏的Git图标）
2. 点击右上角的三个点图标（更多操作）
3. 选择 `Add Remote`
4. 输入远程名称：`origin`
5. 输入远程URL：`https://github.com/你的用户名/你的仓库名.git`
6. 点击 `Add Remote` 确认

## 步骤4：暂存并提交文件
1. 点击Git History扩展中的 `Changes` 标签
2. 你会看到所有修改过的文件
3. 点击文件旁边的 `+` 图标来暂存单个文件，或点击顶部的 `+` 图标暂存所有文件
4. 在消息框中输入提交信息（例如："Initial commit"）
5. 点击 `Commit` 按钮提交更改

## 步骤5：推送到GitHub
1. 提交完成后，点击Git History扩展中的 `Branches` 标签
2. 右键点击 `main` 或 `master` 分支
3. 选择 `Push Branch`
4. 如果提示输入GitHub凭据，输入你的GitHub用户名和密码（或个人访问令牌）

## 可选：使用SSH密钥认证（推荐）

### 生成SSH密钥
1. 打开PowerShell或Git Bash
2. 运行：`ssh-keygen -t rsa -b 4096 -C "你的GitHub邮箱"`
3. 按Enter接受默认保存位置
4. 输入密码（可选，推荐）

### 添加SSH密钥到GitHub
1. 打开 `C:\Users\你的用户名\.ssh\id_rsa.pub` 文件
2. 复制其中的内容
3. 登录GitHub，进入 `Settings` > `SSH and GPG keys`
4. 点击 `New SSH key`
5. 输入标题，粘贴密钥内容，点击 `Add SSH key`

### 更新远程URL为SSH形式
1. 在Git History扩展中，点击右上角的三个点图标
2. 选择 `Edit Remote`
3. 将URL从 `https://github.com/...` 更改为 `git@github.com:...`
4. 点击 `Save` 确认

## 常见问题解决

### 1. 推送失败 - 权限问题
- 确保使用了正确的GitHub凭据
- 如果使用HTTPS，尝试使用个人访问令牌而不是密码
- 推荐使用SSH密钥认证

### 2. 推送失败 - 远程仓库不存在
- 检查远程URL是否正确
- 确保GitHub仓库已创建

### 3. 文件没有显示在Changes中
- 检查文件是否在项目目录内
- 检查 `.gitignore` 文件是否包含了这些文件

## 命令行备选方案
如果Git History扩展遇到问题，你可以使用以下命令行步骤：

```bash
# 初始化仓库
git init

# 配置用户信息
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 暂存所有文件
git add .

# 提交更改
git commit -m "Initial commit"

# 推送到GitHub
git push -u origin master
```

## 验证同步结果
1. 登录GitHub
2. 进入你的仓库
3. 确认文件已成功上传

如果遇到任何问题，请检查GitHub仓库的权限设置和Git配置。