import requests
import json
import time

def fetch_data():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 目标：批量抓取 50 个随机深度词条
    print("Connecting to Global Archive...")
    
    for i in range(50):
        try:
            # 使用 Wikipedia 的随机摘要接口，非常稳定
            res = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                title = data.get('title', '')
                desc = data.get('extract', '')
                
                # 避开你做过的那些旧内容（死海、24个比利等）
                if any(word in title.lower() for word in ["dead sea", "billy milligan", "gobekli", "ark of the covenant"]):
                    continue

                # 自动匹配你的流量模型
                category = "B" # 默认考古历史
                text_stack = (title + desc).lower()
                if any(w in text_stack for w in ["murder", "psychology", "killer", "death", "mind"]): category = "A" # 人性
                elif any(w in text_stack for w in ["secret", "cia", "space", "alien", "conspiracy"]): category = "C" # 系统
                
                results.append({
                    "type": category,
                    "title": title,
                    "desc": desc[:400] + "...",
                    "source": "Global_Network_V3",
                    "url": data.get('content_urls', {}).get('desktop', {}).get('page', '#')
                })
            time.sleep(0.1) # 轻微延迟
        except:
            continue

    # 强制写出文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Done! Found {len(results)} new raw topics.")

if __name__ == "__main__":
    fetch_data()
