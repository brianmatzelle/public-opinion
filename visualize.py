import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import json
import matplotlib.pyplot as plt

@dataclass
class Config:
    """Configuration class to store command line arguments."""
    model: str
    language: str
    iterations: int
    visualization_type: str

    @classmethod
    def from_args(cls) -> 'Config':
        """Create Config from command line arguments."""
        parser = argparse.ArgumentParser(
            description='Visualize influence rankings for different countries.'
        )
        parser.add_argument('-m', '--model', type=str, required=True,
                           help='Model name (e.g., llama3.2)')
        parser.add_argument('-l', '--language', type=str, required=True,
                           help='Language code (e.g., es)')
        parser.add_argument('-i', '--iterations', type=int, required=True,
                           help='Number of iterations')
        parser.add_argument('-t', '--type', choices=['average', 'weighted'],
                           required=True, help='Type of visualization')
        args = parser.parse_args()
        return cls(args.model, args.language, args.iterations, args.type)

class RankingVisualizer:
    """Class to handle visualization of country rankings."""
    
    def __init__(self, config: Config):
        self.config = config
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load ranking data from JSON file."""
        file_path = Path("data") / self.config.model / f"{self.config.language}_{self.config.iterations}.json"
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {file_path}")

    def _create_bar_plot(self, countries: List[str], rankings: Dict[str, float],
                        ylabel: str, title: str) -> None:
        """Create and display a bar plot of rankings."""
        plt.figure(figsize=(12, 6))
        plt.bar(countries, [rankings[country] for country in countries])
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.tight_layout()
        plt.show()

    def visualize_average_rankings(self) -> None:
        """Visualize average rankings for countries."""
        rankings = self.data["average_rankings"]
        countries = sorted(rankings.keys(), key=lambda x: rankings[x])
        
        self._create_bar_plot(
            countries=countries,
            rankings=rankings,
            ylabel='Average Ranking (lower is better)',
            title=f'Countries by Average Influence Ranking ({self.config.language.upper()} Responses) - {self.config.model}'
        )

    def visualize_weighted_rankings(self) -> None:
        """Visualize weighted rankings for countries."""
        rankings = self.data["weighted_rankings"]
        countries = sorted(rankings.keys(), key=lambda x: rankings[x], reverse=True)
        
        self._create_bar_plot(
            countries=countries,
            rankings=rankings,
            ylabel='Weighted Ranking',
            title=f'Countries by Weighted Influence Ranking ({self.config.language.upper()} Responses) - {self.config.model}'
        )

def main() -> None:
    """Main function to run the visualization."""
    try:
        config = Config.from_args()
        visualizer = RankingVisualizer(config)
        
        if config.visualization_type == 'average':
            visualizer.visualize_average_rankings()
        else:
            visualizer.visualize_weighted_rankings()
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()