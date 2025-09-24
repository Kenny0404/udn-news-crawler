# UDN经济日报新闻爬虫

这个项目用于爬取UDN经济日报的新闻内容，支持登录和付费内容提取。

## 功能特性

- 自动登录UDN账户
- 爬取付费新闻内容
- 提取新闻标题、发布时间、作者和正文
- 支持定时任务执行
- 使用GitHub Actions自动运行

## 使用方法

### 1. 设置GitHub Secrets

在GitHub仓库中设置以下Secrets:

1. 进入仓库页面
2. 点击 "Settings" 选项卡
3. 在左侧菜单中点击 "Secrets and variables" → "Actions"
4. 点击 "New repository secret" 按钮
5. 添加以下两个Secrets:
   - Name: `UDN_USERNAME`
     Value: 您的UDN账户邮箱地址
   - Name: `UDN_PASSWORD`
     Value: 您的UDN账户密码

### 2. 配置定时任务

默认情况下，爬虫每天运行一次。您可以修改 `.github/workflows/crawl.yml` 文件中的cron表达式来调整运行频率。

### 3. 手动触发爬虫

您可以随时手动触发爬虫运行:
1. 进入仓库页面
2. 点击 "Actions" 选项卡
3. 选择 "Crawl UDN News" 工作流
4. 点击 "Run workflow" 按钮

## 本地运行

如果您想在本地运行爬虫:

```bash
# 克隆仓库
git clone https://github.com/Kenny0404/udn-news-crawler.git
cd udn-news-crawler

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export UDN_USERNAME=您的邮箱地址
export UDN_PASSWORD=您的密码

# 运行爬虫
python crawler.py
```

## 项目结构

- `crawler.py`: 主爬虫脚本
- `sites/`: 网站配置文件
- `schemas/`: 数据提取规则
- `requirements.txt`: 依赖包列表
- `.github/workflows/crawl.yml`: GitHub Actions工作流

## 配置说明

### 网站配置 (`sites/udn_money_config.py`)

- `start_url`: 起始URL
- `wait_for`: 等待元素选择器
- `js_code`: 页面滚动JavaScript代码

### 提取规则 (`schemas/udn_money_schema.py`)

- `title`: 新闻标题选择器
- `time_published`: 发布时间选择器
- `author`: 作者选择器
- `summary`: 正文内容选择器

## 许可证

MIT