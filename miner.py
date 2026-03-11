import requests
import json
import os

def fetch_reddit_mysteries():
    # 抓取 Reddit 的未解之谜版块
    url = "https://www.reddit.com/r/UnresolvedMysteries/hot.json?limit=20"
    headers = {'User-agent': 'IdeaScout Bot'}
    
    try:
        res = requests.get(url, headers=headers).json()
        posts = res['data']['children']
        
        results = []
        for post in posts:
            p = post['data']
            # 简单的分类逻辑
            content = p['title'] + p['selftext']
            category = "B" # 默认考古档案
            if "psychology" in content.lower() or "killer" in content.lower():
                category = "A" # 人性禁区
            
            results.append({
                "type": category,
                "title": p['title'][:80],
                "desc": p['selftext'][:200] + "...",
                "source": "Reddit/Unresolved"
            })
        
        # 将结果写入 data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_reddit_mysteries()