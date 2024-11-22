import copy

# Heuristic function: Manhattan distance
def manhattan_distance(state, goal):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            goal_index = goal.index(state[i])
            distance += abs(i // 3 - goal_index // 3) + abs(i % 3 - goal_index % 3)
    return distance

# Generate successors of the current state
def generate_successors(state):
    successors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    
    moves = {
        "up": (row - 1, col),
        "down": (row + 1, col),
        "left": (row, col - 1),
        "right": (row, col + 1),
    }
    
    for move, (new_row, new_col) in moves.items():
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = state[:]
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            successors.append(new_state)
    
    return successors

# Hill Climbing algorithm
def hill_climbing(initial_state, goal_state, heuristic):
    current_state = initial_state
    steps = [current_state]
    
    while True:
        successors = generate_successors(current_state)
        current_heuristic = heuristic(current_state, goal_state)
        next_state = None
        next_heuristic = float("inf")
        
        for successor in successors:
            h = heuristic(successor, goal_state)
            if h < next_heuristic:
                next_state = successor
                next_heuristic = h
        
        # If no better state is found, return the current state
        if next_heuristic >= current_heuristic:
            return current_state, steps
        
        current_state = next_state
        steps.append(current_state)

# Test the algorithm
if __name__ == "__main__":
    initial = [1, 2, 3, 4, 0, 5, 6, 7, 8]  # Initial configuration
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]     # Goal configuration
    
    solution, path = hill_climbing(initial, goal, manhattan_distance)
    
    print("Path to solution:")
    for step in path:
        for i in range(0, 9, 3):
            print(step[i:i+3])
        print()
    
    if solution == goal:
        print("Goal state reached!")
    else:
        print("Hill climbing failed to find the solution.")
