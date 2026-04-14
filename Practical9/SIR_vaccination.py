import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Model parameters
N = 10000
beta = 0.3
gamma = 0.05
time_steps = 200  # Shortened steps for clear peak
vaccine_ratios = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  # Remove 1.0 (useless)

# Initialize larger figure
plt.figure(figsize=(12, 6), dpi=150)

# Simulate for each vaccination ratio
for idx, ratio in enumerate(vaccine_ratios):
    vaccinated = int(N * ratio)
    S = max(N - 1 - vaccinated, 0)
    I = 1
    R = 0
    I_history = [I]
    
    for _ in range(time_steps):
        if S > 0:
            inf_prob = beta * (I / N)
            new_inf = np.random.choice([0, 1], size=S, p=[1 - inf_prob, inf_prob]).sum()
        else:
            new_inf = 0
        
        if I > 0:
            new_rec = np.random.choice([0, 1], size=I, p=[1 - gamma, gamma]).sum()
        else:
            new_rec = 0
        
        S = max(S - new_inf, 0)
        I = max(I + new_inf - new_rec, 0)
        R = min(R + new_rec, N)
        I_history.append(I)
    
    # Plot with clear style (thick line + transparency)
    color = cm.tab10(idx)
    plt.plot(I_history, label=f'Vaccine {int(ratio*100)}%', 
             color=color, linewidth=2, alpha=0.8)

# Optimize layout
plt.xlabel('Time Step', fontsize=12)
plt.ylabel('Infected Count', fontsize=12)
plt.title('SIR Model with Vaccination (Clear Peaks)', fontsize=14)
plt.legend(bbox_to_anchor=(1, 1), loc="upper left", fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('SIR_vaccination.png')
plt.show()