import requests
import json
import time

def fetch_data():
    # 模拟浏览器浏览器头，防止被 Reddit 拦截
    url = "https://www.reddit.com/r/UnresolvedMysteries/hot.json?limit=20"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    results = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # 如果被拦截了，我们就抓点 Wikipedia 的硬核历史作为兜底，保证不落空
        if response.status_code != 200:
            raise Exception("Reddit blocked us")
            
        posts = response.json()['data']['children']
        for post in posts:
            p = post['data']
            content = (p['title'] + p['selftext']).lower()
            category = "B"
            if any(word in content for word in ["psych", "killer", "mind", "human"]): category = "A"
            if any(word in content for word in ["space", "alien", "tech"]): category = "C"
            
            results.append({
                "type": category,
                "title": p['title'][:100],
                "desc": p['selftext'][:300] + "...",
                "source": "Reddit/Unresolved"
            })
    except Exception as e:
        print(f"Switching to backup source due to: {e}")
        # 兜底方案：抓取 Wikipedia 的硬核随机词条，确保 data.json 永远存在
        for _ in range(5):
            res = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
            results.append({
                "type": "B",
                "title": "[Backup] " + res.get('title', 'Historical Archive'),
                "desc": res.get('extract', 'Data extraction in progress...'),
                "source": "Global Archive"
            })

    # 核心：无论如何都要写出这个文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Successfully created data.json")

if __name__ == "__main__":
    fetch_data()
