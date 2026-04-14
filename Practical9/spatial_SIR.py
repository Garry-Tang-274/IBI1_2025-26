import numpy as np
import matplotlib.pyplot as plt

# Pseudocode
# 1. Create 100x100 grid (0:Susceptible, 1:Infected, 2:Recovered)
# 2. Set random initial infection
# 3. Define parameters and 8-neighborhood
# 4. Simulate 100 time steps
# 5. Plot 10 results (0,10,...,90 steps) in one figure
# 6. Add axis labels and fixed coordinate range (0-100)

# Initialize 100x100 grid
grid_size = 100
population = np.zeros((grid_size, grid_size), dtype=int)

# Random initial infected position
x, y = np.random.choice(grid_size, 2)
population[x, y] = 1

# Model parameters
beta = 0.3
gamma = 0.05
time_steps = 100

# 8 neighboring cells
neighbors = [(-1,-1), (-1,0), (-1,1),
             (0,-1),          (0,1),
             (1,-1),  (1,0), (1,1)]

# Create 2x5 subplots for 10 images
fig, axes = plt.subplots(2, 5, figsize=(18, 8), dpi=150)
axes = axes.flatten()
img_index = 0

# Main simulation loop
for step in range(time_steps):
    current_grid = population.copy()
    infected_cells = np.argwhere(current_grid == 1)

    # Update infection and recovery
    for i, j in infected_cells:
        # Spread to 8 neighbors
        for dx, dy in neighbors:
            ni, nj = i + dx, j + dy
            if 0 <= ni < grid_size and 0 <= nj < grid_size:
                if current_grid[ni, nj] == 0 and np.random.rand() < beta:
                    population[ni, nj] = 1
        # Recover process
        if np.random.rand() < gamma:
            population[i, j] = 2

    # Plot every 10 steps (total 10 plots)
    if step % 10 == 0:
        ax = axes[img_index]
        ax.imshow(population, cmap="viridis", interpolation="nearest")
        
        # Set title and axis labels
        ax.set_title(f"Spatial SIR - Step {step}", fontsize=12, pad=10)
        ax.set_xlabel("X Position", fontsize=10)
        ax.set_ylabel("Y Position", fontsize=10)
        
        # Fixed coordinate range (0-100) as required
        ax.set_xlim(0, grid_size)
        ax.set_ylim(grid_size, 0)
        ax.tick_params(labelsize=8)
        
        img_index += 1

# Final layout adjustment
plt.suptitle("Spatial SIR Model (100x100 Grid)", fontsize=18, y=1.02)
plt.tight_layout()

# Save the combined figure
plt.savefig("spatial_SIR_final.png", bbox_inches="tight")
plt.show()