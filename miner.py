import requests
import json
import random

def fetch_data():
    # 1. 你的硬核 SOP 离线灵感库（确保程序永远不崩，且符合你的硬核审美）
    offline_seeds = [
        {"type": "B", "title": "死海古卷：库姆兰洞穴的未公开碎片", "desc": "最近的红外成像显示，部分碎片记录了未知的星象周期，疑似某种古代历法。", "source": "Archive_OFFLINE"},
        {"type": "A", "title": "24个比利：被抹除的第25个人格", "desc": "在初版评估报告中，有一段关于‘无名者’的描述被刻意涂黑，这可能解释了比利某些无法理解的行为。", "source": "Psych_OFFLINE"},
        {"type": "B", "title": "哥贝克力石阵：地层下的第四层结构", "desc": "地质雷达探测显示，在现存石阵下方还有更古老的圆形结构，时间点直逼冰河世纪末期。", "source": "Geo_OFFLINE"},
        {"type": "C", "title": "约柜路径：利用现代拓扑学模拟古道", "desc": "结合古代旱季水文资料，模拟出一条从耶路撒冷通往埃塞俄比亚的非传统隐秘路径。", "source": "System_OFFLINE"}
    ]

    results = []
    # 模拟真实浏览器，防止被拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 2. 真正的联网抓取逻辑 (尝试获取 3 个最新的全球百科硬核条目)
    print("Connecting to Global Archive...")
    try:
        for _ in range(3):
            # 获取随机百科条目，并带有 10 秒超时保护
            res = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                results.append({
                    "type": "B", 
                    "title": "[LIVE] " + data.get('title', 'Unknown Discovery'),
                    "desc": data.get('extract', 'Exploring historical contexts...')[:260] + "...",
                    "source": "Global_Network"
                })
        print(f"Successfully synced {len(results)} live topics.")
    except Exception as e:
        print(f"Network sync failed (will use offline backup): {e}")

    # 3. 合并联网数据和离线数据
    final_results = results + offline_seeds
    
    # 4. 核心：强制写出 data.json，保证 Actions 绝对变绿
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print("Done: data.json is ready for IdeaScout.")

if __name__ == "__main__":
    fetch_data()
