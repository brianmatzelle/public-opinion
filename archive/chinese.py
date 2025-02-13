import requests
import json
import matplotlib.pyplot as plt
import ast
from collections import defaultdict
from tqdm import tqdm

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3.1",
    "prompt": "用这个 JSON 数组格式制作一个世界上最具影响力的前 10 个国家的列表：['国家1', '国家2', ...]。请勿在回复中包含任何其他文本。",
    "stream": False
}

# Store rankings for each country
country_rankings = defaultdict(list)

# Dictionary for Chinese to English country names
country_translations = {
    # Major Powers
    "美国": "USA",
    "中国": "China",
    "俄罗斯": "Russia",
    "德国": "Germany",
    "英国": "UK",
    "法国": "France",
    "日本": "Japan",
    "印度": "India",
    "加拿大": "Canada",
    "澳大利亚": "Australia",
    
    # European Countries
    "意大利": "Italy",
    "西班牙": "Spain",
    "葡萄牙": "Portugal",
    "荷兰": "Netherlands",
    "比利时": "Belgium",
    "瑞典": "Sweden",
    "挪威": "Norway",
    "芬兰": "Finland",
    "丹麦": "Denmark",
    "瑞士": "Switzerland",
    "奥地利": "Austria",
    "波兰": "Poland",
    "乌克兰": "Ukraine",
    "希腊": "Greece",
    "爱尔兰": "Ireland",
    
    # Asian Countries
    "韩国": "South Korea",
    "朝鲜": "North Korea",
    "越南": "Vietnam",
    "泰国": "Thailand",
    "印度尼西亚": "Indonesia",
    "马来西亚": "Malaysia",
    "新加坡": "Singapore",
    "菲律宾": "Philippines",
    "巴基斯坦": "Pakistan",
    "孟加拉国": "Bangladesh",
    "蒙古": "Mongolia",
    
    # Middle Eastern Countries
    "伊朗": "Iran",
    "伊拉克": "Iraq",
    "沙特阿拉伯": "Saudi Arabia",
    "土耳其": "Turkey",
    "以色列": "Israel",
    "阿联酋": "UAE",
    "卡塔尔": "Qatar",
    
    # American Countries
    "墨西哥": "Mexico",
    "巴西": "Brazil",
    "阿根廷": "Argentina",
    "智利": "Chile",
    "秘鲁": "Peru",
    "哥伦比亚": "Colombia",
    "委内瑞拉": "Venezuela",
    
    # African Countries
    "埃及": "Egypt",
    "南非": "South Africa",
    "尼日利亚": "Nigeria",
    "肯尼亚": "Kenya",
    "埃塞俄比亚": "Ethiopia",
    "摩洛哥": "Morocco",
    "加纳": "Ghana",
    
    # Oceania
    "新西兰": "New Zealand",
    "巴布亚新几内亚": "Papua New Guinea",
    
    # Other Notable Countries
    "白俄罗斯": "Belarus",
    "哈萨克斯坦": "Kazakhstan",
    "阿富汗": "Afghanistan",
    "叙利亚": "Syria",
    "古巴": "Cuba",
    "冰岛": "Iceland"
}

# Collect data from multiple runs
for i in tqdm(range(10), desc="Collecting rankings"):
    response = requests.post(url, json=payload)
    data = response.json()
    msg = data['response']
    print(msg)
    
    # Parse the JSON string and store rankings
    try:
        countries = ast.literal_eval(msg)
        for rank, country in enumerate(countries, 1):
            country_rankings[country].append(rank)
    except Exception as e:
        print(f"Error parsing JSON: {e}")

# Calculate average rankings
avg_rankings = {
    country: sum(rankings)/len(rankings) 
    for country, rankings in country_rankings.items()
}

# Create visualization
plt.figure(figsize=(12, 6))
# Translate country names and sort based on rankings
countries = sorted(avg_rankings.keys(), key=lambda x: avg_rankings[x])
countries = [country_translations.get(country, country) for country in countries]  # Translate to English
rankings = [avg_rankings[country] for country in sorted(avg_rankings.keys(), key=lambda x: avg_rankings[x])]

plt.bar(countries, rankings)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Average Ranking (lower is better)')
plt.title('Countries by Average Influence Ranking')
plt.tight_layout()
plt.show()
