import asyncio
import os
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
        
        // 填充登录表单
        const uidInput = document.querySelector('input[name="uid"]') || document.querySelector('#uid');
        const pwdInput = document.querySelector('input[name="pwd"]') || document.querySelector('#pwd');
        
        if (uidInput && pwdInput) {
            uidInput.value = '{username}';
            pwdInput.value = '{password}';
            
            // 提交表单
            const form = uidInput.closest('form');
            if (form) {
                form.submit();
            }
        }
        
        // 等待登录完成
        await new Promise(resolve => setTimeout(resolve, 5000));
    """

async def crawl_udn_news():
    """爬取UDN新闻"""
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
        print("正在登录...")
        login_config = CrawlerRunConfig(
            js_code=get_login_js(username, password),
            delay_before_return_html=5
        )
        
        login_result = await crawler.arun(
            url="https://member.udn.com/member/login",
            crawler_config=login_config
        )
        
        print("登录完成，开始爬取新闻...")
        
        # 爬取新闻列表
        list_url = UDN_MONEY_CONFIG["start_url"]
        list_config = CrawlerRunConfig(
            wait_for=UDN_MONEY_CONFIG["wait_for"],
            delay_before_return_html=3,
            js_code=UDN_MONEY_CONFIG["js_code"]
        )
        
        list_result = await crawler.arun(
            url=list_url,
            crawler_config=list_config
        )
        
        print(f"列表页爬取完成，状态: {list_result.success}")
        
        # 提取新闻链接
        # 这里需要根据实际的提取策略来实现
        print("新闻爬取完成")

if __name__ == "__main__":
    asyncio.run(crawl_udn_news())