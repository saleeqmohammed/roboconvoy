import numpy as np
import pbvi

# Problem setup
n_states = 9
n_actions = 4

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
cOmega = np.ones((n_actions, n_states, 1))

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
pbvi_gen = pbvi.generator(apbvi, V, B, 5)  # Run for 5 iterations
for i in range(5):
    V, best_as = next(pbvi_gen)
    print(f"Iteration {i + 1}: Best Actions Indices - {best_as}")

# Print the corresponding best actions
print("\nCorresponding Best Actions:")
for i, best_a in enumerate(best_as):
    action_name = actions[best_a]
    print(f"Belief State {i + 1}: Best Action - {action_name}")

import numpy as np
import pbvi
import matplotlib.pyplot as plt

# POMDP definition with 9 states and 4 actions
# Transition probabilities (cT)
cT = np.random.rand(9, 4, 9)
cT = np.apply_along_axis(lambda x: x / np.sum(x), -1, cT)

# Rewards (cR)
cR = np.random.rand(9, 4)

# Observation probabilities (cOmega)
cOmega = np.random.rand(4, 9, 2)
cOmega = np.apply_along_axis(lambda x: x / np.sum(x), -1, cOmega)

gamma = 0.9  # Discount factor

# Create PBVI object
apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)

# Initial values for belief space (B)
B = np.random.rand(3, 9)
B = np.apply_along_axis(lambda x: x / np.sum(x), -1, B)

# Run PBVI for 5 iterations
V = np.zeros((1, 9), dtype=np.float64)
pbvi_gen = pbvi.generator(apbvi, V, B, 5)

# Plot the results
fig, ax = plt.subplots()
for _ in range(5):
    V, __ = next(pbvi_gen)
for v in V:
    ax.plot(range(9), v)
plt.show()
print(V)

ax.set_xlabel('States')
ax.set_ylabel('Value')
ax.set_title('PBVI Results for POMDP with 9 States and 4 Actions')
plt.show()
# POMDP definition with 9 states and 4 actions
# Transition probabilities (cT)
cT = np.random.rand(9, 4, 9)
cT = np.apply_along_axis(lambda x: x / np.sum(x), -1, cT)

# Rewards (cR)
cR = np.random.rand(9, 4)

# Observation probabilities (cOmega)
cOmega = np.random.rand(4, 9, 2)
cOmega = np.apply_along_axis(lambda x: x / np.sum(x), -1, cOmega)

gamma = 0.9  # Discount factor

# Create PBVI object
apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)

# Initial values for belief space (B)
B = np.random.rand(3, 9)
B = np.apply_along_axis(lambda x: x / np.sum(x), -1, B)

# Run PBVI for 5 iterations
V = np.zeros((1, 9), dtype=np.float64)
pbvi_gen = pbvi.generator(apbvi, V, B, 5)

# Plot the results with straight lines
fig, ax = plt.subplots()
for _ in range(5):
    V, __ = next(pbvi_gen)
    for v in V:
        ax.plot(range(9), v, marker='o', markersize=8)

# Connect consecutive points with lines
for i in range(V.shape[0] - 1):
    ax.plot(range(9), V[i], linestyle='-', linewidth=2, color='gray')

ax.set_xlabel('States')
ax.set_ylabel('Value')
ax.set_title('PBVI Results for POMDP with 9 States and 4 Actions')
plt.show()