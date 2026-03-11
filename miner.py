import requests
import json

def fetch_data():
    # 目标：Reddit 流量最大的三个硬核版块
    # r/UnresolvedMysteries (未解之谜), r/archaeology (考古), r/HighStrangeness (超常现象)
    subs = ["UnresolvedMysteries", "archaeology", "HighStrangeness"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36'}
    results = []

    for sub in subs:
        try:
            # 抓取每个版块最火的 25 条内容
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=25"
            res = requests.get(url, headers=headers, timeout=15).json()
            posts = res['data']['children']
            
            for post in posts:
                p = post['data']
                # 过滤条件：只要长篇讨论，不要短链接或广告
                if p.get('selftext') and len(p['selftext']) > 200:
                    title = p['title']
                    content = (title + p['selftext']).lower()
                    
                    # 流量模型分类 A/B/C
                    category = "B" # 默认考古 B
                    if any(w in content for w in ["psych", "mind", "human", "killer", "personality"]): category = "A" 
                    elif any(w in content for w in ["ufo", "alien", "tech", "cia", "theory"]): category = "C"
                    
                    results.append({
                        "type": category,
                        "title": title,
                        "desc": p['selftext'][:400] + "...", # 抓取核心背景
                        "source": f"r/{sub}",
                        "url": f"https://www.reddit.com{p['permalink']}"
                    })
        except Exception as e:
            print(f"Skipping {sub} due to network.")

    # 核心：将抓取到的 50-75 条全新素材存入，彻底覆盖掉旧的 Top 单
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Sync Complete: {len(results)} new items found.")

if __name__ == "__main__":
    fetch_data()
