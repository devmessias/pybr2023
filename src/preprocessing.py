from typing import Tuple

import pandas as pd
from rich import print


def extract_goals(score: str) -> Tuple[int, int]:
    home_goals, away_goals = map(int, score.split('x'))
    return home_goals, away_goals


def calculate_points(home_goals: int, away_goals: int) -> Tuple[int, int]:
    if home_goals > away_goals:
        return 3, 0
    elif home_goals == away_goals:
        return 1, 1
    else:
        return 0, 3

def sanitize(df: pd.DataFrame) -> pd.DataFrame:
    df.drop('id_match', axis=1, inplace=True)
    # Extract goals
    df['home goals'], df['away goals'] = zip(*df['score'].map(extract_goals))
    # drop column score
    df.drop('score', axis=1, inplace=True)

    # Calculate points
    df['home->away'], df['away->home'] = zip(*df.apply(lambda row: calculate_points(row['home goals'], row['away goals']), axis=1))

    return df


def main():
    #year = input('Please enter a year')
    df = pd.read_csv("data/raw.csv")
    # Filter the dataframe by the specified year
    df = df[df['season'] != 2023]

    df = sanitize(df)
    df.to_csv(f'data/cleaned.csv', index=False)

if __name__ == "__main__":
    main()
