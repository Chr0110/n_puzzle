# N-Puzzle

A Python solver for the N-Puzzle (sliding tile puzzle) using the **A\*** search algorithm with multiple heuristics.

## Problem

An N-Puzzle is a `N x N` grid holding tiles numbered `1` to `N²-1` and one empty space (`0`). The only allowed move is sliding a tile adjacent to the empty space into it.

The goal is to reach the **solved state** from a given starting grid, using the fewest moves possible. This project uses the snail (spiral) layout as the goal:

```
1 2 3
8 0 4
7 6 5
```

Challenges:

- **Huge search space:** a 4x4 puzzle already has ~10¹³ reachable states, so blind search (BFS) is unusable.
- **Unsolvable puzzles:** only half of all permutations can reach the goal; the program must detect the others and report them instead of searching forever.
- **Memory:** the number of states kept in memory can explode on larger grids.

## Solution

### A\* search

A\* explores states in order of `f(n) = g(n) + h(n)`:

- `g(n)`: number of moves made from the start to reach `n`
- `h(n)`: heuristic estimate of the remaining moves to the goal

Implementation:

- **Open set:** priority queue (min-heap) ordered by `f`
- **Closed set:** already-explored states (stored in a hash set to avoid revisiting)
- **Parent links:** used to rebuild the solution path once the goal is reached

With an *admissible* heuristic (never overestimates), A\* returns an optimal solution.

### Heuristics

| Heuristic | Idea | Notes |
|---|---|---|
| Hamming (misplaced tiles) | Count tiles not in their goal position | Simple, weak |
| Manhattan distance | Sum of each tile's horizontal + vertical distance to its goal cell | Standard, admissible |
| Linear conflict | Manhattan + 2 for each pair of tiles blocking each other in the same row/column | Stronger, still admissible |

Stronger heuristics expand fewer states, which reduces both time and memory.

### Solvability check

Before searching, the program counts **inversions** (pairs of tiles in the wrong order, ignoring the blank) and combines it with the blank's position and the grid size to decide whether the goal is reachable by parity. Unsolvable boards are rejected immediately.

### Input

A text file with the grid size on the first line, then the rows. `#` starts a comment:

```
# 3x3 puzzle
3
3 2 6
1 4 0
8 7 5
```

A random puzzle generator can also produce valid inputs.

### Output

- Whether the puzzle is solvable
- **Time complexity:** total number of states selected from the open set
- **Size complexity:** maximum number of states in memory at once
- **Number of moves** in the solution
- The ordered sequence of states from the initial board to the goal

## Usage

```bash
python3 npuzzle.py puzzle.txt
python3 npuzzle.py puzzle.txt --heuristic manhattan
```

> Adjust script name and options to match your repo.

## Concepts covered

- Informed search (A\*, priority queues, open/closed sets)
- Admissible and consistent heuristics
- State-space representation and hashing
- Parity-based solvability
- Time vs memory trade-offs
