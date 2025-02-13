import requests
import json
import matplotlib.pyplot as plt
import ast
from collections import defaultdict
from tqdm import tqdm

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3.1",
    "prompt": "Make a top 10 list for the most powerful countries in the world by influence, in this JSON array format: ['country1', 'country2', ...]. Do not include any other text in your response.",
    "stream": False
}

# Store rankings for each country
country_rankings = defaultdict(list)

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
countries = sorted(avg_rankings.keys(), key=lambda x: avg_rankings[x])
rankings = [avg_rankings[country] for country in countries]

plt.bar(countries, rankings)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Average Ranking (lower is better)')
plt.title('Countries by Average Influence Ranking')
plt.tight_layout()
plt.show()
