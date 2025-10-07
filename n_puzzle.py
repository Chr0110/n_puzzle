import heapq

class PuzzleNode:
    def __init__(self, puzzle, g_score, h_score,  bonus=any, parent=None, move=None):
        self.puzzle = puzzle         
        self.tuple_state = tuple(puzzle)
        self.g_score = g_score
        self.h_score = h_score
        if bonus == "greedy":
            self.f_score = h_score
        elif bonus == "uniform":
            self.f_score = g_score
        else:
            self.f_score = g_score + h_score
        self.parent = parent
        self.move = move


    def __lt__(self, other):
        if self.f_score == other.f_score:
            return self.h_score < other.h_score
        return self.f_score < other.f_score

def misplaced_tiles(s, g):
    t = 0
    for i, v in enumerate(s):
        if v and v != g[i]:
            t += 1
    return t

def create_goal_state(size):
    goal = [[0 for _ in range(size)] for _ in range(size)]
    num = 1
    top, bottom = 0, size - 1
    left, right = 0, size - 1

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            goal[top][col] = num
            num += 1
        top += 1

        for row in range(top, bottom + 1):
            goal[row][right] = num
            num += 1
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                goal[bottom][col] = num
                num += 1
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                goal[row][left] = num
                num += 1
            left += 1

    center = size // 2
    goal[center][center] = 0
    return goal


def flatten(puzzle):
    if isinstance(puzzle[0], int):
        return puzzle
    return [num for row in puzzle for num in row]

def manhattan_distance(s, n, g):
    t = 0
    for i, v in enumerate(s):
        if v:
            gi = g[v]
            t += abs(i//n - gi//n) + abs(i%n - gi%n)
    return t

def get_neighbors(flat_state, size):
    neighbors = []
    empty = flat_state.index(0)
    row, col = divmod(empty, size)

    moves = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]
    for dr, dc, move in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size:
            new_idx = nr * size + nc
            new_puzzle = list(flat_state)
            new_puzzle[empty], new_puzzle[new_idx] = new_puzzle[new_idx], new_puzzle[empty]
            neighbors.append((new_puzzle, move))
    return neighbors


def print_puzzle(puzzle, size=None):
    if isinstance(puzzle[0], list):  # 2D list
        for row in puzzle:
            print(" ".join(str(x) for x in row))
    else:
        if size is None:
            size = int(len(puzzle) ** 0.5)
        for i in range(0, len(puzzle), size):
            print(" ".join(str(x) for x in puzzle[i:i+size]))
    print()

def euclidean_distance(s, n, g):
    t = 0
    for i, v in enumerate(s):
        if v:
            gi = g[v]
            dr = i//n - gi//n
            dc = i%n - gi%n
            t += dr*dr + dc*dc 
    return t * (2 ** 0.5)

def solve_puzzle(start_flat, heuristic, bonus, goal_flat):
    size = int(len(start_flat) ** 0.5)
    goal_tuple = tuple(goal_flat)
    goal_positions = {val: idx for idx, val in enumerate(goal_flat)}
    if heuristic == "manhattan":
        h_func = lambda state: manhattan_distance(state, size, goal_positions)
    elif heuristic == "euclidean":
        h_func = lambda state: euclidean_distance(state, size, goal_positions)
    elif heuristic == "misplaced":
        h_func = lambda state: misplaced_tiles(state, goal_flat)
    start_h = h_func(start_flat)
    start_node = PuzzleNode(start_flat, 0, start_h, None)
    open_set = [start_node]
    closed_set = set()
    g_scores = {start_node.tuple_state: 0}
    states_explored = 0
    max_states_in_memory = 1

    while open_set:
        current = heapq.heappop(open_set)
        if current.tuple_state in closed_set:
            continue

        states_explored += 1
        if current.tuple_state == goal_tuple:
            print("Solution found!")
            print(f"States explored: {states_explored}")
            print(f"Max states in memory: {max_states_in_memory}")
            print("Max Moves:",current.g_score)
            return current

        closed_set.add(current.tuple_state)

        for neighbor, move in get_neighbors(current.puzzle, size):
            neighbor_tuple = tuple(neighbor)
            if neighbor_tuple in closed_set:
                continue
            new_g = current.g_score + 1
            if neighbor_tuple not in g_scores or new_g < g_scores[neighbor_tuple]:
                g_scores[neighbor_tuple] = new_g
                new_h = h_func(neighbor)
                new_node = PuzzleNode(neighbor, new_g, new_h, bonus, parent=current, move=move)
                heapq.heappush(open_set, new_node)
                max_states_in_memory = max(max_states_in_memory, len(open_set) + len(closed_set))

    print(f"No solution found. States explored: {states_explored}")
    return None
