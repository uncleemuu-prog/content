import requests
import json
import time

def fetch_data():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 你的硬核扫描雷达：只有包含这些词的冷门条目才会被收入
    radar_keywords = [
        "mystery", "archaeology", "ancient", "unsolved", "psychology", 
        "forbidden", "conspiracy", "discovery", "tomb", "artifact",
        "experiment", "dark", "secret", "manuscript", "lost city"
    ]
    
    print("Searching for high-value targets...")
    
    # 循环尝试，直到抓到足够多符合调性的内容
    while len(results) < 25:
        try:
            res = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                title = data.get('title', '')
                desc = data.get('extract', '')
                full_text = (title + desc).lower()
                
                # 核心逻辑：雷达过滤
                if any(k in full_text for k in radar_keywords):
                    # 自动归类 A/B/C 流量模型
                    category = "B" 
                    if any(w in full_text for w in ["psych", "human", "killer", "mind"]): category = "A" 
                    elif any(w in full_text for w in ["secret", "cia", "space", "theory"]): category = "C"
                    
                    results.append({
                        "type": category,
                        "title": title,
                        "desc": desc[:400],
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page', '#')
                    })
                    print(f"Target Acquired: {title}")
            time.sleep(0.1)
        except:
            continue

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_data()
