import asyncio
import os
import json
from crawl4ai.async_webcrawler import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import CrawlerRunConfig

# 导入配置
from sites.udn_money_config import UDN_MONEY_CONFIG
from schemas.udn_money_schema import UDN_MONEY_SCHEMA

def get_login_js(username, password):
    """生成登录JavaScript代码"""
    return f"""
        // 等待登录页面加载
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 查找用户名和密码输入框（多种可能的选择器）
        const uidInputs = document.querySelectorAll('input[name="uid"], input[type="email"], #uid, [placeholder*="邮箱"], [placeholder*="email"]');
        const pwdInputs = document.querySelectorAll('input[name="pwd"], input[type="password"], #pwd, [placeholder*="密码"], [placeholder*="password"]');
        
        if (uidInputs.length > 0 && pwdInputs.length > 0) {{
            // 填充表单
            uidInputs[0].value = '{username}';
            pwdInputs[0].value = '{password}';
            
            // 查找并点击登录按钮
            const loginButtons = document.querySelectorAll('button[type="submit"], input[type="submit"], .login-btn, [value*="登录"], [value*="登入"]');
            if (loginButtons.length > 0) {{
                loginButtons[0].click();
            }} else {{
                // 如果找不到按钮，尝试提交表单
                const form = uidInputs[0].closest('form');
                if (form) {{
                    form.submit();
                }}
            }}
        }}
        
        // 等待登录完成
        await new Promise(resolve => setTimeout(resolve, 5000));
    """

async def login_to_udn(crawler, username, password):
    """登录到UDN"""
    print("正在登录到UDN...")
    
    # 访问登录页面
    login_config = CrawlerRunConfig(
        js_code=get_login_js(username, password),
        delay_before_return_html=8,  # 增加等待时间确保登录完成
        wait_for="body"  # 等待页面加载
    )
    
    login_result = await crawler.arun(
        url="https://member.udn.com/member/login",
        crawler_config=login_config
    )
    
    print(f"登录请求完成，状态: {login_result.success}")
    return login_result

async def crawl_news_list(crawler):
    """爬取新闻列表"""
    print("正在爬取新闻列表...")
    
    list_config = CrawlerRunConfig(
        wait_for=UDN_MONEY_CONFIG["wait_for"],
        delay_before_return_html=5,
        js_code=UDN_MONEY_CONFIG["js_code"]
    )
    
    list_result = await crawler.arun(
        url=UDN_MONEY_CONFIG["start_url"],
        crawler_config=list_config
    )
    
    print(f"列表页爬取完成，状态: {list_result.success}")
    return list_result

async def crawl_single_news(crawler, news_url):
    """爬取单个新闻页面"""
    print(f"正在爬取新闻: {news_url}")
    
    # 使用提取策略
    extraction_strategy = JsonCssExtractionStrategy(UDN_MONEY_SCHEMA, verbose=True)
    
    news_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        wait_for="section.article-body__editor, div.article-body__editor",
        delay_before_return_html=3,
        js_code="""
            // 滚动到页面底部以确保内容加载
            window.scrollTo(0, document.body.scrollHeight);
            
            // 如果有展开按钮，点击它
            const expandButtons = document.querySelectorAll('#quotaOpen, .paywall__ouline-btn');
            expandButtons.forEach(button => {{
                if (button && typeof button.click === 'function') {{
                    button.click();
                }}
            }});
            
            // 等待内容加载
            await new Promise(resolve => setTimeout(resolve, 2000));
        """
    )
    
    news_result = await crawler.arun(
        url=news_url,
        crawler_config=news_config
    )
    
    print(f"新闻爬取完成，状态: {news_result.success}")
    return news_result

async def crawl_udn_news():
    """主爬取函数"""
    print("开始爬取UDN经济日报新闻...")
    
    # 获取登录凭据
    username = os.getenv('UDN_USERNAME')
    password = os.getenv('UDN_PASSWORD')
    
    if not username or not password:
        print("错误: 请设置UDN_USERNAME和UDN_PASSWORD环境变量")
        return
    
    # 创建爬虫实例
    async with AsyncWebCrawler() as crawler:
        # 登录
        login_result = await login_to_udn(crawler, username, password)
        if not login_result.success:
            print("登录失败")
            return
        
        # 爬取新闻列表
        list_result = await crawl_news_list(crawler)
        if not list_result.success:
            print("爬取新闻列表失败")
            return
        
        # 解析新闻链接
        # 这里需要根据实际的提取策略来实现
        print("新闻列表爬取完成，准备提取新闻链接...")
        
        # 示例：爬取特定新闻页面
        test_news_url = "https://money.udn.com/money/story/5603/9020674?from=edn_newestlist_vipbloomberg"
        news_result = await crawl_single_news(crawler, test_news_url)
        
        # 处理结果
        if news_result.success and news_result.extracted_content:
            try:
                content = json.loads(news_result.extracted_content)
                print("提取的新闻内容:")
                print(json.dumps(content, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print("原始提取内容:")
                print(news_result.extracted_content)
        else:
            print("未能提取新闻内容")
            if hasattr(news_result, 'html'):
                print(f"HTML长度: {len(news_result.html)}")

if __name__ == "__main__":
    asyncio.run(crawl_udn_news())