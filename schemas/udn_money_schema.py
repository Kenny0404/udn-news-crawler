UDN_MONEY_SCHEMA = {
    "name": "UDN Money News Extraction",
    "baseSelector": "body",
    "fields": [
        {
            "name": "title",
            "selector": 'h1.article-head__title, h1#story_art_title, h1.article-body__headline, h1',
            "type": "text"
        },
        {
            "name": "time_published",
            "selector": 'time.article-body__time, time, .article-body__time',
            "type": "text",
        },
        {
            "name": "author",
            "selector": 'div.columnist-profile-top__name, .columnist-profile__name, .columnist-profile-top__name',
            "type": "text",
        },
        {
            "name": "summary",
            "selector": 'section.article-body__editor, div#article_body, div#article-body, div.article-body__editor, p',
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

# UDN经济日报新闻列表提取 Schema
UDN_MONEY_LIST_SCHEMA = {
    "name": "UDN Money News List Extraction",
    "baseSelector": "body",
    "fields": [
        {
            "name": "news_items",
            "selector": "div.story__content, div.story-content, .story__content, .story-content, div[class*='story'], article",
            "type": "list",
            "fields": [
                {
                    "name": "title",
                    "selector": "a",
                    "type": "text"
                },
                {
                    "name": "link",
                    "selector": "a",
                    "type": "attribute",
                    "attribute": "href"
                }
            ]
        }
    ]
}