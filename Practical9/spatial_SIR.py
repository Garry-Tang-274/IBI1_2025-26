import numpy as np
import matplotlib.pyplot as plt

# Pseudocode
# 1. Create 100x100 susceptible grid
# 2. Random initial infection
# 3. Set parameters and 8-neighbor offsets
# 4. Simulate 100 steps
# 5. Plot 10 time steps (0,10,...,90) in one 2x5 figure
# 6. Save combined figure

# Grid initialization
grid_size = 100
population = np.zeros((grid_size, grid_size), dtype=int)  # 0:S, 1:I, 2:R

# Random initial infected cell
x, y = np.random.choice(grid_size, 2)
population[x, y] = 1

# Model parameters
beta = 0.3
gamma = 0.05
time_steps = 100

# 8 neighbors direction
neighbors = [(-1,-1), (-1,0), (-1,1),
             (0,-1),          (0,1),
             (1,-1),  (1,0), (1,1)]

# Create 2x5 subplots for 10 figures
fig, axes = plt.subplots(2, 5, figsize=(15, 6), dpi=150)
axes = axes.flatten()  # flatten to 1D for easy indexing
plot_idx = 0

# Simulation loop
for step in range(time_steps):
    current = population.copy()
    infected = np.argwhere(current == 1)

    # Update infection and recovery
    for i, j in infected:
        # Infect neighbors
        for dx, dy in neighbors:
            ni, nj = i + dx, j + dy
            if 0 <= ni < grid_size and 0 <= nj < grid_size:
                if current[ni, nj] == 0 and np.random.rand() < beta:
                    population[ni, nj] = 1
        # Recover
        if np.random.rand() < gamma:
            population[i, j] = 2

    # Plot every 10 steps (total 10 plots)
    if step % 10 == 0:
        ax = axes[plot_idx]
        im = ax.imshow(population, cmap='viridis', interpolation='nearest')
        ax.set_title(f'Step {step}', fontsize=10)
        ax.axis('off')
        plot_idx += 1

# Final layout and save
plt.suptitle('Spatial SIR Model (10 Time Steps)', fontsize=16)
plt.tight_layout()
plt.savefig('spatial_SIR_combined.png')  # Save all-in-one figure
plt.show()