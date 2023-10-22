"""This module contains function to compute the ranking of teams in a graph.

All ranking function should take the pattern of the following function:
    def compute_rank_something(G: nx.DiGraph) -> dict[str, float]:
        ...
        return ranking
"""
import networkx as nx
import numpy as np


def compute_rank_out_degree_scores(G: nx.DiGraph) -> dict[str, int]:
    """Compute the out-degree scores for each team in the graph.

    Parameters:
        G (nx.DiGraph): Directed graph representing the interactions between teams.

    Returns:
        dict: A dictionary with teams as keys and out-degree values as scores.
    """
    return dict(G.out_degree(weight='weight'))

def compute_rank_page_rank(G: nx.DiGraph) -> dict[str, float]:
    """
    Compute the PageRank scores for each team in the graph.

    Parameters:
        G (nx.DiGraph): Directed graph representing the interactions between teams.

    Returns:
        dict: A dictionary with teams as keys and PageRank values as scores.
    """
    # nx.pagerank returns a dictionary of nodes and their respective PageRank values.
    return nx.pagerank(G, weight='weight')



def pinv(M):
    """Computes the pseudo-inverse of a matrix.
    """
    return np.linalg.pinv(M)


def a2flow(A):
    """
    Dado uma matriz de adjacência calcula a matriz
    de fluxo
    Args
    ----
        A : np.array
            matriz de adjacência
    Returns
    -------
        flow : np.array
            matriz de fluxo
    """
    flow = A.T - A
    return flow


def a2sym(A):
    '''
    Dado uma matriz de adjacência não simetrica retorna
    a simetrica
    '''
    sym = A+A.T
    return sym


def applyDiv(sym, F, degrees=None):
    '''
    Dado uma matriz de fluxo, calcula a
    divergencia
    Args:
    ----
        sym: 2d matrix nxn
            simetrica
        F: 2d matrix nxn
            anti-simétrica
    Return:
        divF: 2d matrix nx1
            vetor de divergencia
    '''
    if degrees is None:
        degrees = sym.sum(axis=1)
    divF = np.multiply(sym, F)
    divF = divF.sum(axis=1)
    return divF.reshape((F.shape[0], 1))


def getLaplacian(sym, degrees=None, norm=False):
    if degrees is None:
        degrees = sym.sum(axis=1)
    D = np.diag(degrees)
    L = D - sym
    if norm:
        D12 = np.diag(np.power(degrees, -1/2))
        L = D12@L@D12
    return L


def getHelmotzPotential(L, divF):
    """Calcula o potencial de Helmholtz
    Args
    ----
        L : np.array
            matriz de laplaciana
        divF : np.array
            vetor de divergencia
    Returns
    -------
        helmotzPotential : np.array
            vetor de potencial de Helmholtz
    """
    h = -1*pinv(L)@divF
    return h

def compute_rank_hodge_rank(G):
    """Given a adjacency matrix, returns the Helmholtz potential.
    Args
    ----
        A : np.array
            adjacency matrix
    Returns
    -------
        helm : np.array
            Helmholtz potential

    """
    #return nx.eigenvector_centrality_numpy(G, weight='weight')
    A = nx.adjacency_matrix(G, weight='weight', nodelist=list(G.nodes)).todense()
    # CONVERT TO FLOAT
    A = A.astype(float)
    A /= A.shape[0]

    Ws = a2sym(A)
    F = a2flow(A)
    divF = applyDiv(Ws, F)
    L = getLaplacian(Ws)
    helmotzPotential = (getHelmotzPotential(L, divF).flatten())
    # CREATE A DICTIONARY WITH THE TEAMS AND THEIR RESPECTIVE HELMHOLTZ POTENTIAL
    teams = list(G.nodes)
    helmotzPotential = dict(zip(teams, helmotzPotential))
    return helmotzPotential
