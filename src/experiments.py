import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from scipy.stats import spearmanr


from graph.structure import generate_graph_from_df
from graph.ranking import *


def get_gradient_color(start: tuple, end: tuple, step: int, max_steps: int) -> str:
    """Compute the gradient color based on the step."""
    r_step = (end[0] - start[0]) / max_steps
    g_step = (end[1] - start[1]) / max_steps
    b_step = (end[2] - start[2]) / max_steps

    red = int(start[0] + r_step * step)
    green = int(start[1] + g_step * step)
    blue = int(start[2] + b_step * step)

    return f"rgb({red},{green},{blue})"


def compare_rankings(scores_by_year: dict, window: int = 6):

    for year, scores_by_method in scores_by_year.items():

        # Using rich for a better console display
        console = Console()
        table = Table(title=f"Year {year} Comparisons", box=box.SIMPLE)

        # The first column is the method name
        table.add_column("Method")
        for scores in scores_by_method.values():
            table.add_column(scores["humanized_name"])

        for i, scores1 in enumerate(scores_by_method.values()):
            sorted_teams_1 = [team for team, _ in scores1["scores"]]
            humanized_name1 = scores1["humanized_name"]
            row = [humanized_name1]
            for j, scores2 in enumerate(scores_by_method.values()):
                if j == i:
                    # Same method, add a placeholder like N/A
                    row.append("N/A")
                    continue
                if j < i:
                    row.append("-")
                    continue

                # Compute Spearman's Rank Correlation

                sorted_teams_2 = [team for team, _ in scores2["scores"]]
                # use 1-based index for the rank

                coefficient, _ = spearmanr(sorted_teams_1, sorted_teams_2)
                row.append(f"{coefficient:.2f}")

            table.add_row(*row)
        console.print(table)



def print_rankings(scores_by_year: dict, window: int = 6):
    """Generate graph from the dataframe"""

    for year, scores_by_method in scores_by_year.items():

        # Using rich for a better console display
        console = Console()

        table = Table(title=f"Year {year}", box=box.SIMPLE)

        for scores in scores_by_method.values():
            table.add_column(scores["humanized_name"])

        # Print top window teams with gradient
        for i in range(window):
            color = get_gradient_color((0, 0, 255), (0, 255, 255), i, window - 1)
            result = []
            for scores in scores_by_method.values():
                sorted_scores = scores["scores"]
                team, score = sorted_scores[i]
                result.append(f"{team}  {score:.2f}")
            table.add_row(*result, style=color)

        # Print bottom window
        for i in range(window):
            color = get_gradient_color((255, 192, 203), (255, 0, 0), i, window - 1)
            result = []
            for scores in scores_by_method.values():
                sorted_scores = scores["scores"]
                n_teams = len(sorted_scores)
                team, score = sorted_scores[n_teams - window + i]
                result.append(f"{team}  {score:.2f}")
            table.add_row(*result, style=color)

        console.print(table)


def get_all_rank_methods() -> dict[str, dict]:
    """Get all the ranking methods in a dictionary."""
    rank_methods = {}
    for name in globals():
        if not name.startswith("compute_rank_"):
            continue
        humanized_name = name.replace("compute_rank_", "").replace("_", " ").title()
        rank_methods[name] = {
            "name": humanized_name,
            "method": globals()[name],
            "humanized_name": humanized_name,
        }
    return rank_methods


def compute_scores_by_year(
    df_all: pd.DataFrame,
    rank_methods: dict,
    year_start: int = 2003,
    year_end: int = 2019,
) -> dict:
    years = range(year_start, year_end+1)
    scores_by_year = {year: {} for year in years}
    for year in years:
        df = df_all[df_all["season"] == year]
        g = generate_graph_from_df(df)

        scores_by_method = {}
        for name in rank_methods:
            scores_by_method[name] = {}
            method = rank_methods[name]["method"]
            humanized_name = rank_methods[name]["humanized_name"]
            scores = method(g)
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            scores_by_method[name]["scores"] = sorted_scores
            scores_by_method[name]["humanized_name"] = humanized_name
        scores_by_year[year] = scores_by_method
    return scores_by_year


def main():
    # Read CSV
    df = pd.read_csv("data/cleaned.csv")
    rank_methods = get_all_rank_methods()
    scores_by_year = compute_scores_by_year(df, rank_methods)
    # Print rankings for the specified year
    print_rankings(scores_by_year, window=6)
    compare_rankings(scores_by_year, window=6)


if __name__ == "__main__":
    main()
