import argparse
from matplotlib import pyplot as plt
import json
from pprint import pprint

def parse_arguments():
    parser = argparse.ArgumentParser(description='Visualize influence rankings for different countries.')
    parser.add_argument('-m', '--model', type=str, required=True, help='Model name (e.g., llama3.2)')
    parser.add_argument('-l', '--language', type=str, required=True, help='Language code (e.g., es)')
    parser.add_argument('-i', '--iterations', type=int, required=True, help='Number of iterations')
    parser.add_argument('-t', '--type', choices=['average', 'weighted'], required=True, 
                       help='Type of visualization: average or weighted rankings')
    return parser.parse_args()

model = "llama3.2"
language = "es"
iterations = 50

with open(f"data/{model}/{language}_{iterations}.json", "r") as f:
    data = json.load(f)

# pprint(data)

def visualize_average_rankings(language):
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

def visualize_weighted_rankings(language):
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

def main():
    args = parse_arguments()
    
    # Load data
    with open(f"data/{args.model}/{args.language}_{args.iterations}.json", "r") as f:
        global data
        data = json.load(f)
    
    # Run visualization based on type argument
    if args.type == 'average':
        visualize_average_rankings(args.language)
    else:
        visualize_weighted_rankings(args.language)

if __name__ == "__main__":
    main()