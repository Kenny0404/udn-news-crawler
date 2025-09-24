# UDN经济日报新闻爬虫

这个项目用于爬取UDN经济日报的新闻内容，支持登录和付费内容提取。

## 功能特性

- 自动登录UDN账户
- 爬取付费新闻内容
- 提取新闻标题、发布时间、作者和正文
- 支持定时任务执行

## 使用方法

1. 设置GitHub Secrets:
   - `UDN_USERNAME`: UDN账户用户名
   - `UDN_PASSWORD`: UDN账户密码

2. 运行爬虫:
   ```bash
   python crawler.py
   ```

## 配置

- `sites/udn_money_config.py`: 网站配置
- `schemas/udn_money_schema.py`: 数据提取规则

## 许可证

MIT