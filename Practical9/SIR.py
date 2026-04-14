# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# Model parameters
N = 10000
beta = 0.3
gamma = 0.05
time_steps = 200  # Shortened steps to expand the peak area

# Initial population state
S = N - 1
I = 1
R = 0

# Store time-series data
S_history = [S]
I_history = [I]
R_history = [R]

# Simulation loop
for _ in range(time_steps):
    # Compute new infections
    infection_prob = beta * (I / N)
    new_infected = np.random.choice([0, 1], size=S, p=[1 - infection_prob, infection_prob]).sum()
    
    # Compute new recoveries
    new_recovered = np.random.choice([0, 1], size=I, p=[1 - gamma, gamma]).sum()
    
    # Update population
    S -= new_infected
    I += new_infected - new_recovered
    R += new_recovered
    
    # Save current state
    S_history.append(S)
    I_history.append(I)
    R_history.append(R)

# Plot optimized results (Larger figure, thicker lines)
plt.figure(figsize=(10, 6), dpi=150)
plt.plot(S_history, label='Susceptible', color='blue', linewidth=2)
plt.plot(I_history, label='Infected', color='red', linewidth=3)  # Highlight infected peak
plt.plot(R_history, label='Recovered', color='green', linewidth=2)

plt.xlabel('Time Step')
plt.ylabel('Population Count')
plt.title('Stochastic SIR Model (Clear Peak)')
plt.legend(fontsize=12)
plt.grid(alpha=0.3)
plt.savefig('SIR.png')
plt.show()