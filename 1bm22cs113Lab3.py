import heapq


def is_goal(state, goal_state):
    return state == goal_state

def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = divmod(index, 3)


    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for move in moves:
        new_row, new_col = row + move[0], col + move[1]

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append(tuple(new_state))
    return neighbors


def misplaced_tiles(state, goal):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])


def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal.index(state[i]), 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


def a_star(start, goal, heuristic):
    priority_queue = []
    heapq.heappush(priority_queue, (0, 0, start, []))

    visited = set()

    while priority_queue:
        f_n, g_n, current_state, path = heapq.heappop(priority_queue)

        if current_state in visited:
            continue

        visited.add(current_state)

        print(f"g(n) = {g_n}, h(n) = {heuristic(current_state, goal)}, f(n) = {f_n}")
        print_state(current_state)

        if is_goal(current_state, goal):
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                g_new = g_n + 1
                h_new = heuristic(neighbor, goal)
                f_new = g_new + h_new
                heapq.heappush(priority_queue, (f_new, g_new, neighbor, path + [current_state]))

    return None


def input_puzzle(prompt):
    print(prompt)
    puzzle = []
    for i in range(3):
        row = input(f"Enter row {i + 1} (3 numbers separated by spaces): ").split()
        puzzle.extend([int(x) for x in row])
    return tuple(puzzle)


start_state = input_puzzle("Enter the start state (use 0 for the blank space):")
goal_state = input_puzzle("Enter the goal state (use 0 for the blank space):")


print("Select Heuristic:")
print("1. Number of Misplaced Tiles")
print("2. Manhattan Distance")
choice = input("Enter 1 or 2: ")

if choice == '1':
    heuristic = misplaced_tiles
else:
    heuristic = manhattan_distance

print("\nSolving using A* Search...")
a_star_solution = a_star(start_state, goal_state, heuristic)

if a_star_solution:
    print("A* Solution found! Steps:")
    for i, step in enumerate(a_star_solution):
        print(f"Step {i + 1}:")
        print_state(step)
else:
    print("No solution found using A*.")
