import numpy as np
import matplotlib.pyplot as plt
import pbvi

# Visualization code
def visualize_moves(grid_size, actions, best_actions_sequence):
    grid = np.zeros((grid_size, grid_size))
    action_movement = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    current_position = (0, 0)

    def update_grid(position, action):
        movement = action_movement[actions[action]]
        new_position = (position[0] + movement[0], position[1] + movement[1])
        if 0 <= new_position[0] < grid_size and 0 <= new_position[1] < grid_size:
            return new_position
        else:
            return position

    for action in best_actions_sequence:
        current_position = update_grid(current_position, action)
        grid[current_position[0], current_position[1]] += 1

    plt.imshow(grid, cmap='Blues', origin='lower')
    plt.scatter(0, 0, color='red', marker='o', s=100, label='Start')
    plt.scatter(current_position[1], current_position[0], color='green', marker='x', s=100, label='End')
    plt.title('Agent\'s Moves on the Grid')
    plt.legend()
    plt.show()

# Define the grid world POMDP with a goal state
n_states = 9
n_actions = 4
n_observations = 1

# Transition probabilities
cT = np.zeros((n_states, n_actions, n_states))
# ... (unchanged)

# Observation probabilities (fully observable)
cOmega = np.ones((n_actions, n_states, n_observations))

# Immediate rewards (negative reward for each action)
cR = -0.1 * np.ones((n_states, n_actions))

# Set a positive reward for reaching the goal state (bottom right corner)
goal_state = 8
cR[goal_state, :] = 1.0

# Discount factor
gamma = 0.9

# Action set
actions = ['up', 'down', 'left', 'right']

# PBVI initialization
apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)

# Initial value function and belief state
V = np.zeros((1, n_states), np.float64)
B = np.ones((1, n_states)) / n_states  # Uniform initial belief state

# PBVI iteration
pbvi_gen = pbvi.generator(apbvi, V, B, 4)
for i in range(5):
    V, best_as = next(pbvi_gen)
    print(f"Iteration {i + 1}: Best Actions Indices - {best_as}")
    visualize_moves(grid_size=3, actions=actions, best_actions_sequence=best_as)
