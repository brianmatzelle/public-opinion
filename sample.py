import asyncio
from execute.execute import execute_prompt
from translate.translate import translate_text, bulk_translate_text
from tqdm import tqdm
import ast
from collections import defaultdict
import json
from pathlib import Path
from pprint import pprint
import argparse

async def analyze_and_visualize_responses(question: str, source: str, destination: str, model: str, iterations: int):
    # Parse model name and size if specified (e.g., "qwen2.5:3b" -> "qwen2.5/3b")
    model_path = model.replace(":", "/")
    
    # Store rankings for each country
    country_rankings = defaultdict(list)
    
    # Translate question to polling language
    translated_question: str = await translate_text(text=question, dest=destination)
    
    # Collect responses
    final_answers = []
    for i in tqdm(range(iterations), desc="Collecting responses"):
        answer = execute_prompt(translated_question, model)
        print(answer)
        final_answers.append(answer)

    translated_answers = await bulk_translate_text(texts=final_answers, dest=source)

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

    # Create base directory for this run
    base_dir = Path(f"data/{model_path}/{destination}_{iterations}")
    base_dir.mkdir(exist_ok=True, parents=True)
    
    # Save results to JSON file
    output_file = base_dir / "results.json"
    
    results = {
        "question": question,
        "model": model,
        "destination_language": destination,
        "source_language": source,
        "iterations": iterations,
        "average_rankings": avg_rankings,
        "weighted_rankings": weighted_rankings,
        "raw_rankings": dict(country_rankings)
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def get_existing_iterations(model: str, destination: str) -> list[str]:
    """Get existing iteration counts from directories."""
    # Parse model name and size if specified
    model_path = model.replace(":", "/")
    output_dir = Path(f"data/{model_path}")
    if not output_dir.exists():
        return []
    
    # Find all directories matching the pattern {language}_{iterations}
    existing_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
    iterations = []
    for dir in existing_dirs:
        try:
            # Extract iteration number from directory name (language_iterations)
            if dir.name.startswith(f"{destination}_"):
                iterations.append(dir.name.split('_')[1])
        except IndexError:
            continue
    return sorted(iterations)

class IterationsCompleter:
    def __init__(self, model: str, language: str):
        self.model = model
        self.language = language

    def __call__(self, prefix, **kwargs):
        return [i for i in get_existing_iterations(self.model, self.language) 
                if i.startswith(prefix)]

def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze and visualize responses.')
    parser.add_argument('-m', '--model', type=str, required=True, 
                        help='Number of iterations')
    parser.add_argument('-s', '--source', type=str, required=False,
                        help='Model name (e.g., llama3.2)')
    parser.add_argument('-d', '--destination', type=str, required=True,
                        help='Language code you wish to poll (e.g., es)')
    parser.add_argument('-i', '--iterations', type=int, required=True,
                        help='Language code you wish to poll from (e.g., en)')
    parser.add_argument('-q', '--question', type=str, required=False,
                        help='Question you wish to poll')
    parser.add_argument('-f', '--file', type=str, required=False,
                        help='File containing the question you wish to poll')
    # Enable tab completion
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    PRE_PROMPT = "Create one top 10 list for this question. Only respond with the list in JSON array format, with each entry on the list being a string.\n\nQuestion: "

    DEFAULT_ARGS = {
        "source": "en",
    }
    
    # Handle file input first
    if args.file is not None:
        with open(args.file, "r") as f:
            args.question = PRE_PROMPT + f.read()

    # Then handle other default arguments
    for key, value in DEFAULT_ARGS.items():
        if getattr(args, key) is None:
            setattr(args, key, value)

    # Format the question if it exists
    if args.question is not None and not args.question.startswith(PRE_PROMPT):
        args.question = PRE_PROMPT + args.question

    if args.question is None and args.file is None:
        raise ValueError("Either question or file must be provided")
    
    print(args.question)
    
    asyncio.run(analyze_and_visualize_responses(
        question=args.question,
        source=args.source,
        destination=args.destination,
        model=args.model,
        iterations=int(args.iterations)  # Convert to int since we defined it as str in argparse
    ))
