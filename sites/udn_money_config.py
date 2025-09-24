from ..schemas.udn_money_schema import UDN_MONEY_SCHEMA, UDN_MONEY_LIST_SCHEMA

UDN_MONEY_CONFIG = {
    # === UDN经济日报新闻网站设定 ===
    "name": "UDNMoney",
    "start_url": "https://money.udn.com/money/cate/5603",
    "domain": "money.udn.com",
    "url_pattern": "/money/story/",

    "crawl_type": "batch",  # "concurrent" 或 "batch"
    "mode": "scroll",
    "max_pages": 3,  # 滚动加载的页数
    "batch_size": 10,  # 批次大小
    "headless": True,

    # JavaScript代码用于滚动页面加载更多内容
    "js_code": """
        // 滚动到页面底部多次以加载更多内容
        let scrollCount = 0;
        const maxScrolls = 3;
        const scrollInterval = setInterval(() => {
            window.scrollTo(0, document.body.scrollHeight);
            scrollCount++;
            if (scrollCount >= maxScrolls) {
                clearInterval(scrollInterval);
            }
        }, 1500);
    """,
    "wait_for": "div.story__content, article, .story__content",  # 添加更多选择器选项

    "extraction_strategy": "json_css",
    "schema": UDN_MONEY_SCHEMA,  # 引用 schema 模块
    "list_schema": UDN_MONEY_LIST_SCHEMA,  # 新闻列表提取 schema

    "excluded_tags": ['nav', 'footer', 'aside', 'iframe', 'script', 'style', 'header'],

    "output_format": "json",
    "use_markdown": False,
    "save_raw": False,
    "save_fit": False,

    # === 特殊设定 ===
    "url_prefix": "https://money.udn.com",
    "extract_selector": "div.story__content a, .story__content a, article a",
    
    # === 标题翻译设定 ===
    "enable_news_title_translation": True,  # 启用新闻标题翻译功能
    
    # === LLM分析设定 ===
    "enable_llm_analysis": True,  # 启用LLM新闻内容分析功能
    "use_openai_ollama": True,  # 使用OpenAI库调用Ollama而不是原生httpx
    
    # === 数据库存储设定 ===
    "enable_database_storage": True,  # 启用数据库存储功能
}