import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data from the CSV file
input_file = 'cpu_experiment_summary.csv'
data = pd.read_csv(input_file)

# Ensure columns are correctly identified
required_columns = {'Trial Type', 'CPU Time (ms) - Normal', 'CPU Time (ms) - Secure', 'CPU Time (ms) - Secure Benchmark'}
if not required_columns.issubset(data.columns):
    raise ValueError("The required columns are not present in the input file.")

# Extract data for plotting
test_types = data['Trial Type'].tolist()
cpu_time_normal = data['CPU Time (ms) - Normal'].str.replace(',', '').astype(float).tolist()
cpu_time_secure = data['CPU Time (ms) - Secure'].str.replace(',', '').astype(float).tolist()
cpu_time_benchmark = data['CPU Time (ms) - Secure Benchmark'].str.replace(',', '').astype(float).tolist()

# Validate the data
if len(test_types) != len(cpu_time_normal) or len(cpu_time_normal) != len(cpu_time_secure) or len(cpu_time_secure) != len(cpu_time_benchmark):
    raise ValueError("Mismatch in data lengths between trial types and CPU times.")

# Create positions for the bars
x = np.arange(len(test_types))
width = 0.25  # Width of the bars

# Create the bar chart
fig, ax = plt.subplots(figsize=(12, 7))

# Add bars for each CPU time category
bars_normal = ax.bar(x - width, cpu_time_normal, width, label='CPU Time (Normal)', color='orange')
bars_secure = ax.bar(x, cpu_time_secure, width, label='CPU Time (Secure - Purecap ABI)', color='blue')
bars_benchmark = ax.bar(x + width, cpu_time_benchmark, width, label='CPU Time (Secure - Purecap Benchmark ABI)', color='green')

# Add labels, title, and legend
ax.set_xlabel('Trial Type', fontsize=12)
ax.set_ylabel('CPU Time (ms)', fontsize=12)
ax.set_title('CPU Time Comparison Between Normal, Secure Purecap Benchmark ABI, and Secure Purecap ABI', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(test_types, rotation=45, ha='right', fontsize=10)
ax.legend(fontsize=10)

# Add grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Add value annotations above each bar
for bars in [bars_normal, bars_secure, bars_benchmark]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height):,}',  # Format numbers with commas
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

# Show the plot
plt.tight_layout()

# Save the adjusted graph
plt.savefig('CPUperformance_comparasion_normal_secure_benchmark.png')

plt.show()

