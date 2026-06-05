#!/usr/bin/env python3

import sys
import random
import networkx as nx
from pysat.formula import CNF
from pysat.solvers import Solver


def var_x(v, c, k):
    # map node and color to variable
    return v * k + c + 1


def var_y(v, N, k):
    # map node selection to variable
    return N * k + v + 1


def encode(G, N, k, target_size):
    # build cnf formula
    cnf = CNF()

    # if node is selected it must have at least one color
    for v in range(N):
        yv = var_y(v, N, k)
        clause = [-yv] + [var_x(v, c, k) for c in range(k)]
        cnf.append(clause)

    # each node has at most one color
    for v in range(N):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var_x(v, c1, k), -var_x(v, c2, k)])

    # adjacent nodes cannot share the same color
    for (u, v) in G.edges():
        for c in range(k):
            cnf.append([-var_x(u, c, k), -var_x(v, c, k)])

    # enforce at least target_size selected nodes
    from itertools import combinations
    for subset in combinations(range(N), N - target_size + 1):
        cnf.append([var_y(v, N, k) for v in subset])

    return cnf


def solve(G, N, k):
    # try all sizes from max to min
    for size in range(N, 0, -1):
        cnf = encode(G, N, k, size)

        with Solver(name="glucose3") as solver:
            solver.append_formula(cnf)

            if solver.solve():
                model = solver.get_model()

                selected = []
                coloring = []

                # extract solution
                for v in range(N):
                    yv = var_y(v, N, k)
                    if yv in model:
                        selected.append(v)
                        for c in range(k):
                            if var_x(v, c, k) in model:
                                coloring.append((v, c))

                return selected, coloring

    return [], []


def main():
    # check arguments
    if len(sys.argv) != 4:
        print("Usage: ./solver N k p")
        return

    N = int(sys.argv[1])
    k = int(sys.argv[2])
    p = float(sys.argv[3])

    # generate random graph
    G = nx.erdos_renyi_graph(N, p)

    # collect edges
    edges = []
    for (u, v) in G.edges():
        if u < v:
            edges.append(f"{u}-{v}")
        else:
            edges.append(f"{v}-{u}")

    print(" ".join(edges))

    # solve problem
    selected, coloring = solve(G, N, k)

    # print coloring
    output = [f"{v}:{c}" for (v, c) in coloring]
    print(" ".join(output))


if __name__ == "__main__":
    main()
