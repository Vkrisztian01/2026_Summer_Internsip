import matplotlib.pyplot as plt
import numpy as np

x_sizes = []
y_times = []

file_path = "results.txt"

try:
    with open(file_path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            parts = line.strip().split()
            
            if len(parts) < 5:
                continue
                
            try:
                num_nodes = int(parts[0])
                time1 = float(parts[-2])
                time2 = float(parts[-1])
                
                x_sizes.append(num_nodes)
                y_times.append(time1)
                
                x_sizes.append(num_nodes)
                y_times.append(time2)
                
            except ValueError:
                continue

except FileNotFoundError:
    print(f"Error: Could not find '{file_path}'. Place this script in the same directory.")
    exit()

plt.rcParams['font.family'] = 'serif'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=300)

ax.scatter(
    x_sizes, y_times, 
    color='#D32F2F', 
    alpha=0.6, 
    edgecolors='black', 
    linewidths=0.5,
    s=40, 
    label='Individual Solver Runs'
)

unique_sizes = sorted(list(set(x_sizes)))
mean_times = []
for sz in unique_sizes:
    subset_times = [t for x, t in zip(x_sizes, y_times) if x == sz]
    mean_times.append(np.mean(subset_times))

ax.plot(
    unique_sizes, mean_times,
    color='#D32F2F',
    linestyle='--',
    linewidth=1.2,
    alpha=0.6,
    label='Mean Runtime'
)

ax.set_title('Running Time vs Number of Nodes', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Number of Nodes ($n$)', fontsize=11)
ax.set_ylabel('Execution Time (seconds)', fontsize=11)
ax.grid(True, which="both", linestyle=':', alpha=0.6)
ax.legend(loc='upper left', frameon=True, edgecolor='none')

ax.set_yscale('log')

plt.tight_layout()
output_image = "solver_scaling_plot.png"
plt.savefig(output_image, bbox_inches='tight')
print(f"Successfully generated {output_image} with {len(x_sizes)} total run records!")