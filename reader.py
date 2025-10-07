import sys
import argparse
import random
from n_puzzle import solve_puzzle, create_goal_state, flatten, print_puzzle
import time

def split_content(content):
    size = None
    puzzle = []
    checked = 1
    zero = 0
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        row = [int(x) for x in parts]
        zero += row.count(0)
        if size is None:
            size = len(row)
        if len(row) != size:
            checked = 0
            print("Invalid puzzle row length")
            break
        puzzle.append(row)

    if len(puzzle) != size or zero != 1:
        print("Invalid puzzle: not square or missing/too many zeros")
        checked = 0
    return puzzle, size, checked, zero



def zero_pos(puzzle):
    size = len(puzzle)
    for i, row in enumerate(puzzle):
        for j, val in enumerate(row):
            if val == 0:
                return size - i, i, j  
    return None, None, None


def count_inversions(puzzle):
    numbers = [num for row in puzzle for num in row if num != 0]
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1
    return inversions


def solvable(puzzle, size, goal_puzzle):
    puzzle_inversions = count_inversions(puzzle)
    goal_inversions = count_inversions(goal_puzzle)

    if size % 2 != 0:
        return (puzzle_inversions % 2) == (goal_inversions % 2)
    else:
        zero_row_from_bottom, _, _ = zero_pos(puzzle)
        goal_zero_row, _, _ = zero_pos(goal_puzzle)
        puzzle_parity = (puzzle_inversions + zero_row_from_bottom) % 2
        goal_parity = (goal_inversions + goal_zero_row) % 2
        return puzzle_parity == goal_parity

def make_puzzle(s, solvable, iterations):
    def swap_empty(p):
        idx = p.index(0)
        poss = []
        if idx % s > 0:
            poss.append(idx - 1)
        if idx % s < s - 1:
            poss.append(idx + 1)
        if idx // s > 0:
            poss.append(idx - s)
        if idx // s < s - 1:
            poss.append(idx + s)
        swi = random.choice(poss)
        p[idx] = p[swi]
        p[swi] = 0

    p = make_goal(s)
    goal = [x for x in p]
    for i in range(iterations):
        swap_empty(p)

    if not solvable:
        if p[0] == 0 or p[1] == 0:
            p[-1], p[-2] = p[-2], p[-1]
        else:
            p[0], p[1] = p[1], p[0]
    return p, goal

def make_goal(s):
    ts = s * s
    puzzle = [-1 for i in range(ts)]
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while True:
        puzzle[x + y * s] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * s] != -1):
            iy = ix
            ix = 0
        elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * s] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if cur == s * s:
            cur = 0

    return puzzle

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("heuristic", choices=['manhattan', 'euclidean', 'misplaced'], help="Heuristic to use")
    parser.add_argument("-sz", "--size", type=int,default=3, help="Size of the puzzle's side. Must be >3.")
    parser.add_argument("-f", "--file", default=False, help="Need a file to parse.")
    parser.add_argument("-b", "--bonus", choices=['greedy', 'uniform'], default=None, help="Bonus search type (optional)")
    parser.add_argument("-s", "--solvable", action="store_true", default=False, help="Forces generation of a solvable puzzle. Overrides -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=100, help="Number of passes")
    args = parser.parse_args()
    if args.file:
        with open(args.file, "r") as file:
            content = file.read()
        if not content:
            print("File is empty")
        else:
            if args.bonus:
                bonus = args.bonus
            else:
                bonus = ''
            puzzle_2d, size, checked, zero = split_content(content)
            if checked == 1 and zero == 1:
                goal_2d = create_goal_state(size)
                if solvable(puzzle_2d, size, goal_2d):
                    start_flat = flatten(puzzle_2d)
                    start_time = time.time()
                    solution = solve_puzzle(start_flat, args.heuristic,bonus, flatten(goal_2d))
                    end_time = time.time()
                    if solution:
                        print_puzzle(flatten(goal_2d), len(goal_2d))
                        print(f"Solved in {end_time - start_time:.4f} seconds")
                else:
                    print("UNSOLVABLE")
    else:
        random.seed()
        if args.solvable and args.unsolvable:
            print("Can't be both solvable AND unsolvable, dummy!")
            sys.exit(1)
        if args.size < 3:
            print("Can't generate a puzzle with size lower than 2. It says so in the help. Dummy.")
            sys.exit(1)
        if not args.solvable and not args.unsolvable:
            solv = random.choice([True, False])
        elif args.solvable:
            solv = True
        elif args.unsolvable:
            solv = False
        s = args.size
        if solv:
            puzzle, goal = make_puzzle(s, solvable=solv, iterations=args.iterations)
            if args.bonus:
                bonus = args.bonus
            else:
                bonus = ''
            start_time = time.time()
            solution = solve_puzzle(puzzle, args.heuristic,bonus, goal)
            end_time = time.time()
            if solution:
                w = len(str(s * s))
                print("# This puzzle is %s" % ("solvable" if solv else "unsolvable"))
                print_puzzle(goal)
                print(f"Solved in {end_time - start_time:.4f} seconds")
        else:
            print("Puzzle is unsolvable. Try again!")