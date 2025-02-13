import asyncio
from generate.variations import generate
from execute.execute import execute_prompt
from translate.translate import translate_text_to_lang
from tqdm import tqdm
import matplotlib.pyplot as plt
import ast
from collections import defaultdict
import json
from pathlib import Path

async def analyze_and_visualize_responses(question: str, original_language: str, polling_language: str):
    # Store rankings for each country
    country_rankings = defaultdict(list)
    
    # Translate question to polling language
    translated_question: str = await translate_text_to_lang(text=question, lang=polling_language)
    # print(f"translated_question: {translated_question.text}")
    
    # Collect responses
    final_answers = []
    for i in tqdm(range(10), desc="Collecting responses"):
        final_answers.append(execute_prompt(translated_question.text))

    # Translate responses back to original language
    translated_answers = []
    for answer in tqdm(final_answers, desc="Translating responses"):
        translated = await translate_text_to_lang(text=answer, lang=original_language)
        translated_answers.append(translated.text)
        # print(f"answer: {translated.text}")

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

    # Save results to JSON file
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"rankings_{polling_language}.json"
    
    results = {
        "question": question,
        "polling_language": polling_language,
        "average_rankings": avg_rankings,
        "raw_rankings": dict(country_rankings)
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Create visualization
    plt.figure(figsize=(12, 6))
    countries = sorted(avg_rankings.keys(), key=lambda x: avg_rankings[x])
    rankings = [avg_rankings[country] for country in countries]

    plt.bar(countries, rankings)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Average Ranking (lower is better)')
    plt.title(f'Countries by Average Influence Ranking ({polling_language.upper()} Responses)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    question = "In JSON array format (['country 1', 'country 2', ...]), list the top 10 countries in the world by geopolitical influence. Only respond with JSON."
    original_language = "en"
    polling_language = "es"
    
    asyncio.run(analyze_and_visualize_responses(question, original_language, polling_language))
