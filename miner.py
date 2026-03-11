import requests
import json
import time

def fetch_data():
    # 你的账号基因：根据 TOP 案例提炼的搜索词
    # 只要 Reddit 出现这些词，脚本就会把它抓下来
    search_keywords = ["Ancient Mystery", "Unresolved", "Archaeology Discovery", "Psychology Experiment", "Forbidden History"]
    subreddits = ["UnresolvedMysteries", "archaeology", "HighStrangeness"]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36'}
    results = []

    print("Starting Global Content Hunt...")

    for sub in subreddits:
        try:
            # 抓取每个版块最热的 20 条内容
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=20"
            res = requests.get(url, headers=headers, timeout=10).json()
            posts = res['data']['children']
            
            for post in posts:
                p = post['data']
                if p['is_self'] and len(p['selftext']) > 200: # 只要长文，不要水贴
                    content = (p['title'] + p['selftext']).lower()
                    
                    # 流量模型分类逻辑
                    category = "B" # 默认考古 B
                    if any(w in content for w in ["psych", "mind", "experiment", "killer"]): category = "A" # 人性禁区 A
                    elif any(w in content for w in ["ufo", "alien", "tech", "cia"]): category = "C" # 系统阴谋 C
                    
                    results.append({
                        "type": category,
                        "title": p['title'],
                        "desc": p['selftext'][:500] + "...", # 抓取更长的描述供你写脚本
                        "source": f"r/{sub}",
                        "url": f"https://www.reddit.com{p['permalink']}"
                    })
        except Exception as e:
            print(f"Error in {sub}: {e}")

    # 只要最新的内容，并确保至少有 30-50 条
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Done! Found {len(results)} new potential topics.")

if __name__ == "__main__":
    fetch_data()
