import numpy as np
import matplotlib.pyplot as plt
import pbvi

# Define the grid world POMDP with a goal state
n_states = 9
n_actions = 4
n_observations = 1  # For simplicity, assume a fully observable grid world


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

# Transition probabilities
cT = np.zeros((n_states, n_actions, n_states))
for s in range(n_states):
    row, col = divmod(s, 3)  # 3x3 grid
    if row > 0:
        cT[s, 0, s - 3] = 1.0  # Move up
    if row < 2:
        cT[s, 1, s + 3] = 1.0  # Move down
    if col > 0:
        cT[s, 2, s - 1] = 1.0  # Move left
    if col < 2:
        cT[s, 3, s + 1] = 1.0  # Move right

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

# Print the corresponding best actions
print("Corresponding Best Actions:")
for i, best_a in enumerate(best_as):
    action_name = actions[best_a]
    print(f"Belief State {i + 1}: Best Action - {action_name}")
    visualize_moves(grid_size=3, actions=actions, best_actions_sequence=best_as)

 # Replace your existing main script with this updated version

""" import matplotlib.pyplot as plt
import numpy as np
import pbvi """

# POMDP definition
# ... (your POMDP parameters here)
""" 

apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)

V = np.zeros((1, 2), np.float64)

B = np.array([[0.5, 0.5],
              [0.5, 0.5]])

# Plot settings
fig, ax = plt.subplots()
ax.set_xlabel('State')
ax.set_ylabel('Belief')

# Plot initial belief
for i, b in enumerate(B):
    ax.plot(range(len(b)), b, label=f'Belief {i}')

# PBVI iterations
pbvi_gen = pbvi.generator(apbvi, V, B, 4)
for iteration in range(1, 6):  # Update the range based on your needs
    V, best_as = next(pbvi_gen)

    # Plot belief after each iteration
    B = apbvi.expanded_B(B)
    for i, b in enumerate(B):
        ax.plot(range(len(b)), b, label=f'Iteration {iteration}, Belief {i}')

# Add legends and show plot
ax.legend()
plt.show()
 """