# Graph Coloring Optimization Solver

A Python implementation of a SAT-based optimization algorithm for graph coloring.

The program generates a random Erdős–Rényi graph and finds the largest subset of vertices that can be properly colored using at most `k` colors. The problem is encoded as a Boolean satisfiability (SAT) instance and solved using the Glucose3 SAT solver from PySAT.

## Features

- Random graph generation using NetworkX
- SAT encoding of graph coloring constraints
- Optimization by maximizing the number of colored vertices
- Uses the Glucose3 SAT solver
- Outputs both graph edges and vertex-color assignments

## Requirements

- Python 3.8+
- NetworkX
- PySAT

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/graph-coloring-optimization.git
cd graph-coloring-optimization
```

Install dependencies:

```bash
pip install networkx python-sat
```

## Usage

```bash
./solver.py N k p
```

or

```bash
python3 solver.py N k p
```

### Parameters

| Parameter | Description |
|------------|------------|
| `N` | Number of vertices |
| `k` | Number of available colors |
| `p` | Edge probability for the Erdős–Rényi random graph |

### Example

```bash
python3 solver.py 5 2 0.5
```

Example output:

```text
0-1 0-3 1-2 2-4
0:0 1:1 2:0 4:1
```

The first line lists graph edges.

The second line lists vertex-color assignments in the format:

```text
vertex:color
```

## SAT Encoding

The solver uses two types of Boolean variables:

### Coloring Variables

```text
x(v,c)
```

Vertex `v` is assigned color `c`.

### Selection Variables

```text
y(v)
```

Vertex `v` belongs to the selected colorable subset.

### Constraints

1. Selected vertices must receive at least one color.
2. Each vertex can receive at most one color.
3. Adjacent vertices cannot share the same color.
4. At least a target number of vertices must be selected.

The solver iteratively searches for the maximum feasible subset size, starting from `N` and decreasing until a satisfiable solution is found.

## Technologies

- Python
- NetworkX
- PySAT
- Glucose3 SAT Solver

## License

MIT License
