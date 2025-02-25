import argparse
from pathlib import Path
from typing import Dict, List
import json
import matplotlib.pyplot as plt

def load_data(file_path: Path) -> Dict:
    """Load ranking data from JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def create_bar_plot(countries: List[str], rankings: Dict[str, float],
                    ylabel: str, title: str, output_path: Path) -> None:
    """Create and save a bar plot of rankings."""
    plt.figure(figsize=(12, 6))
    plt.bar(countries, [rankings[country] for country in countries])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def visualize_rankings(data: Dict, file_path: Path) -> None:
    """Visualize both average and weighted rankings for countries."""
    # Get the directory containing the results.json file
    output_dir = file_path.parent
    
    # Average rankings
    rankings = data["average_rankings"]
    countries = sorted(rankings.keys(), key=lambda x: rankings[x])
    create_bar_plot(
        countries=countries,
        rankings=rankings,
        ylabel='Average Ranking (lower is better)',
        title=f'Countries by Average Influence Ranking ({data["destination_language"].upper()} Responses) - {data["model"]}',
        output_path=output_dir / "average.png"
    )
    
    # Weighted rankings
    rankings = data["weighted_rankings"]
    countries = sorted(rankings.keys(), key=lambda x: rankings[x], reverse=True)
    create_bar_plot(
        countries=countries,
        rankings=rankings,
        ylabel='Weighted Ranking',
        title=f'Countries by Weighted Influence Ranking ({data["destination_language"].upper()} Responses) - {data["model"]}',
        output_path=output_dir / "weighted.png"
    )

def main() -> None:
    """Main function to run the visualization."""
    parser = argparse.ArgumentParser(
        description='Visualize influence rankings for different countries.'
    )
    parser.add_argument('-p', '--path', type=str, required=True,
                       help='Path to the JSON data file')
    args = parser.parse_args()

    try:
        data = load_data(Path(args.path))
        visualize_rankings(data, Path(args.path))
        print(f"Plots saved in {Path(args.path).parent}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()