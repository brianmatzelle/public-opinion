from matplotlib import pyplot as plt
import json
from pprint import pprint

model = "llama3.2"
language = "es"
iterations = 50

with open(f"data/{model}/{language}_{iterations}.json", "r") as f:
    data = json.load(f)

# pprint(data)

def visualize_average_rankings():
    # Extract rankings and countries
    rankings = data["average_rankings"]
    countries = list(rankings.keys())

    # Sort countries by ranking
    countries.sort(key=lambda x: rankings[x])

    # Create bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(countries, [rankings[country] for country in countries])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Average Ranking (lower is better)')
    plt.title(f'Countries by Average Influence Ranking ({language.upper()} Responses)')
    plt.tight_layout()
    plt.show()

def visualize_weighted_rankings():
    rankings = data["weighted_rankings"]
    countries = list(rankings.keys())

    # Sort countries by ranking in descending order (higher scores first)
    countries.sort(key=lambda x: rankings[x], reverse=True)

    # Create bar plot 
    plt.figure(figsize=(12, 6))
    plt.bar(countries, [rankings[country] for country in countries])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Weighted Ranking')
    plt.title(f'Countries by Weighted Influence Ranking ({language.upper()} Responses)')
    plt.tight_layout()
    plt.show()

# visualize_average_rankings()
visualize_weighted_rankings()