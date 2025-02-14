import asyncio
from execute.execute import execute_prompt
from translate.translate import translate_text, bulk_translate_text
from tqdm import tqdm
import ast
from collections import defaultdict
import json
from pathlib import Path
from pprint import pprint
async def analyze_and_visualize_responses(question: str, original_language: str, polling_language: str, model: str, iterations: int):
    # Store rankings for each country
    country_rankings = defaultdict(list)
    
    # Translate question to polling language
    translated_question: str = await translate_text(text=question, dest=polling_language)
    
    # Collect responses
    final_answers = []
    for i in tqdm(range(iterations), desc="Collecting responses"):
        final_answers.append(execute_prompt(translated_question, model))

    translated_answers = await bulk_translate_text(texts=final_answers, dest=original_language)

    # Process each answer
    for answer in tqdm(translated_answers, desc="Processing answers"):
        try:
            # Parse the JSON string
            countries = ast.literal_eval(answer)
            
            # Normalize country names
            countries = [
                "United States" if c in ["USA", "United States of America"] else c
                for c in countries
            ]
            
            # Store rankings
            for rank, country in enumerate(countries, 1):
                country_rankings[country].append(rank)
        except Exception as e:
            print(f"Error parsing answer: {e}")

    # Calculate average rankings
    avg_rankings = {
        country: sum(rankings)/len(rankings) 
        for country, rankings in country_rankings.items()
    }

    # Calculate the weighted rankings (adjusted formula)
    weighted_rankings = {}
    for country, rankings in country_rankings.items():
        weighted_ranking = 0.0
        for rank in rankings:
            weighted_ranking += iterations / rank
        weighted_rankings[country] = weighted_ranking

    # Save results to JSON file in data/{model}/{polling_language}_{iterations}.json
    output_dir = Path(f"data/{model}")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file = output_dir / f"{polling_language}_{iterations}.json"
    
    results = {
        "question": question,
        "model": model,
        "polling_language": polling_language,
        "iterations": iterations,
        "average_rankings": avg_rankings,
        "weighted_rankings": weighted_rankings,
        "raw_rankings": dict(country_rankings)
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    question = "In JSON array format (['country 1', 'country 2', ...]), list the top 10 countries in the world by geopolitical influence. Only respond with JSON."
    original_language = "en"
    polling_language = "es"
    model = "llama3.2"
    iterations = 50
    
    asyncio.run(analyze_and_visualize_responses(question, original_language, polling_language, model, iterations))
