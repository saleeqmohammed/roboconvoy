import numpy as np
import matplotlib.pyplot as plt

# Define grid world parameters
grid_size = 5
num_particles = 100

# Define target location
target_location = (4, 4)

# Define starting location
start_location = (0, 0)

# Define transition model (assuming deterministic motion for simplicity)
def transition_model(state, action):
    x, y = state
    if action == 'up' and y < grid_size - 1:
        y += 1
    elif action == 'down' and y > 0:
        y -= 1
    elif action == 'left' and x > 0:
        x -= 1
    elif action == 'right' and x < grid_size - 1:
        x += 1
    return (x, y)

# Define observation model (noisy sensors)
def observation_model(true_state):
    true_x, true_y = true_state
    # Simulate noisy sensor readings
    noisy_x = np.random.normal(true_x, 0.5)
    noisy_y = np.random.normal(true_y, 0.5)
    return (noisy_x, noisy_y)

# Initialize particles around the starting location
particles = [(start_location[0], start_location[1]) for _ in range(num_particles)]

# Define particle filter update step
def particle_filter_update(particles, action, observation):
    new_particles = []
    for particle in particles:
        # Transition model
        new_particle = transition_model(particle, action)
        # Observation model
        predicted_observation = observation_model(new_particle)
        # Extract components and calculate likelihood
        diff_x = predicted_observation[0] - observation[0]
        diff_y = predicted_observation[1] - observation[1]
        likelihood = np.exp(-0.5 * (diff_x**2 + diff_y**2))
        # Weight particles by likelihood
        new_particles.extend([new_particle] * int(likelihood * 100))

    # Check if new_particles is empty
    if not new_particles:
        # If empty, create new particles uniformly across the grid
        new_particles = [(x, y) for x in range(grid_size) for y in range(grid_size)]

    # Resample particles
    new_particles_indices = np.random.choice(len(new_particles), size=num_particles, replace=True)
    new_particles = np.array(new_particles)[new_particles_indices]
    return new_particles

# POMDP parameters
discount_factor = 0.9

# Define reward function
def reward_function(state, action, target):
    if np.array_equal(state, target):
        return 10  # High reward for reaching the target
    elif action == 'stay':
        return -1  # Small penalty for staying in the same place
    else:
        # Calculate Euclidean distance and return its negative value
        distance = np.linalg.norm(np.array(state) - np.array(target))
        return -distance

# Define POMDP value iteration
def pomdp_value_iteration(particles, target, discount_factor):
    optimal_policy = []

    for belief_state in particles:
        optimal_action = 'stay'
        max_expected_reward = float('-inf')

        for action in ['up', 'down', 'left', 'right']:
            expected_reward = 0

            for next_particle in particles:
                # Placeholder for the transition probability (replace with your implementation)
                transition_prob = 0.8  # Assuming equal probability for all actions

                # Placeholder for the immediate reward (replace with your implementation)
                immediate_reward = reward_function(belief_state, action, target)

                # Update the expected reward based on the transition probability and immediate reward
                expected_reward += transition_prob * (immediate_reward + discount_factor * expected_reward)

            if expected_reward > max_expected_reward:
                max_expected_reward = expected_reward
                optimal_action = action

        optimal_policy.append(optimal_action)

    return optimal_policy

# Plotting parameters
def plot_grid(target_location, estimated_position, particles):
    plt.figure(figsize=(8, 8))

    # Plot grid
    for i in range(grid_size + 1):
        plt.plot([i, i], [0, grid_size], color='k', linestyle='-', linewidth=1)
        plt.plot([0, grid_size], [i, i], color='k', linestyle='-', linewidth=1)

    # Plot particles
    particles_x, particles_y = zip(*particles)
    plt.scatter(particles_x, particles_y, color='blue', alpha=0.5, label='Particles')

    # Plot estimated position
    plt.scatter(*estimated_position, color='green', marker='o', label='Estimated Position')

    # Plot target location
    plt.scatter(*target_location, color='red', marker='x', label='True Target Location')

    plt.title('Grid World with Particles and Estimated Position')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example navigation sequence
actions = ['right', 'up', 'up', 'right']

# Simulate navigation using POMDP
for action in actions:
    # True transition
    target_location = transition_model(target_location, action)
    # Noisy observation
    noisy_observation = observation_model(target_location)
    # Update particles using particle filter
    particles = particle_filter_update(particles, action, noisy_observation)
    # Perform POMDP value iteration and get the optimal policy
    optimal_policy = pomdp_value_iteration(particles, target_location, discount_factor)

    # Plot the current state
    plot_grid(target_location, np.mean(particles, axis=0).astype(int), particles)

# Print the final results
print("True Target Location:", target_location)
print("Estimated Robot Position:", np.mean(particles, axis=0).astype(int))

# Print the optimal action for a specific belief state
specific_belief_state = (2, 1)
index_closest_particle = np.argmin(np.linalg.norm(np.array(particles) - np.array(specific_belief_state), axis=1))
print(f"Optimal Action for Belief State {specific_belief_state}: {optimal_policy[index_closest_particle]}")
