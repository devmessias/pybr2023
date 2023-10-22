import pandas as pd
import networkx as nx



def generate_graph_from_df(df: pd.DataFrame) -> nx.DiGraph:
    """
    Generate a directed graph from the dataframe.
    Nodes represent teams.
    Edges represent matches with weights being the total points earned over all matches.
    """
    G = nx.DiGraph()

    for _, row in df.iterrows():
        # If the edge already exists, update its weight, otherwise add a new edge with the weight
        if G.has_edge(row['home'], row['away']):
            G[row['home']][row['away']]['weight'] += row['home->away']
        else:
            G.add_edge(row['home'], row['away'], weight=row['home->away'])

        if G.has_edge(row['away'], row['home']):
            G[row['away']][row['home']]['weight'] += row['away->home']
        else:
            G.add_edge(row['away'], row['home'], weight=row['away->home'])

    return G
