# UDN经济日报付费内容爬取解决方案

## 问题分析

您遇到的问题是UDN经济日报网站需要登录才能查看完整的新闻内容。普通爬虫无法获取付费墙后的内容。

## 解决方案概述

本解决方案通过以下方式解决这个问题：

1. **自动登录** - 使用浏览器自动化技术登录UDN账户
2. **会话保持** - 在登录后保持会话状态以访问付费内容
3. **内容提取** - 使用智能选择器提取新闻标题、正文等内容
4. **定时执行** - 通过GitHub Actions定期执行爬虫

## 技术实现细节

### 1. 登录机制

我们使用crawl4ai的JavaScript执行功能来自动填充登录表单：

```javascript
// 查找用户名和密码输入框
const uidInputs = document.querySelectorAll('input[name="uid"], input[type="email"], #uid');
const pwdInputs = document.querySelectorAll('input[name="pwd"], input[type="password"], #pwd');

// 填充表单
uidInputs[0].value = '用户名';
pwdInputs[0].value = '密码';

// 提交表单
const loginButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
loginButtons[0].click();
```

### 2. 付费内容处理

对于付费内容，我们使用以下策略：

1. **等待内容加载** - 增加延迟时间确保JavaScript内容加载完成
2. **点击展开按钮** - 自动点击"展开全文"按钮
3. **滚动页面** - 触发懒加载机制

```javascript
// 滚动到页面底部
window.scrollTo(0, document.body.scrollHeight);

// 点击展开按钮
const expandButtons = document.querySelectorAll('#quotaOpen');
expandButtons.forEach(button => button.click());
```

### 3. 内容提取

使用JsonCssExtractionStrategy定义提取规则：

```python
UDN_MONEY_SCHEMA = {
    "name": "UDN Money News Extraction",
    "baseSelector": "body",
    "fields": [
        {
            "name": "title",
            "selector": 'h1.article-head__title, h1#story_art_title',
            "type": "text"
        },
        {
            "name": "time_published",
            "selector": 'time.article-body__time',
            "type": "text",
        },
        {
            "name": "author",
            "selector": 'div.columnist-profile-top__name',
            "type": "text",
        },
        {
            "name": "summary",
            "selector": 'section.article-body__editor',
            "type": "list",
            "fields": [
                {
                    "name": "paragraph",
                    "type": "text"
                }
            ]
        }
    ]
}
```

## 使用步骤

### 1. Fork仓库

在GitHub上fork [udn-news-crawler](https://github.com/Kenny0404/udn-news-crawler) 仓库到您的账户。

### 2. 设置Secrets

在您的fork仓库中设置以下Secrets：

1. 进入仓库的 "Settings" → "Secrets and variables" → "Actions"
2. 添加两个Secrets:
   - `UDN_USERNAME`: 您的UDN邮箱
   - `UDN_PASSWORD`: 您的UDN密码

### 3. 启用GitHub Actions

默认情况下，fork的仓库会自动启用GitHub Actions。如果没有，请在 "Actions" 选项卡中启用。

### 4. 运行爬虫

爬虫会按计划每天运行一次，您也可以手动触发：

1. 进入 "Actions" 选项卡
2. 选择 "Crawl UDN News" 工作流
3. 点击 "Run workflow"

## 输出结果

爬虫运行后会提取以下信息：

- 新闻标题
- 发布时间
- 作者
- 正文内容

## 故障排除

### 1. 登录失败

如果登录失败，请检查：

1. 用户名和密码是否正确
2. 是否启用了双重验证（可能需要手动处理）
3. 网站是否更改了登录表单结构

### 2. 内容提取失败

如果无法提取内容，请检查：

1. 选择器是否正确（网站结构可能已更改）
2. 是否需要更长的等待时间
3. 是否需要处理其他JavaScript交互

### 3. GitHub Actions失败

如果GitHub Actions失败，请检查：

1. Secrets是否正确设置
2. 依赖包是否正确安装
3. 查看详细的错误日志

## 安全注意事项

1. **凭据安全** - 使用GitHub Secrets安全存储登录凭据
2. **访问控制** - 确保只有授权人员可以访问仓库
3. **定期更新** - 定期检查和更新登录凭据
4. **合规使用** - 遵守网站的使用条款和robots.txt

## 扩展功能

您可以根据需要扩展此解决方案：

1. **数据库存储** - 将爬取的数据存储到数据库
2. **通知系统** - 当有新新闻时发送通知
3. **多网站支持** - 添加对其他新闻网站的支持
4. **数据分析** - 对新闻内容进行情感分析或关键词提取

## 贡献

欢迎提交Issue和Pull Request来改进这个解决方案。