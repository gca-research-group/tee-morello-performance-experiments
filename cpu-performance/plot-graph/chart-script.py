import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data from the CSV file
input_file = '../summarise-results/cpu_experiment_summary.csv'
data = pd.read_csv(input_file)

# Extract data for plotting
test_types = data['Test Type'].tolist()
cpu_time_out = data['CPU Time (ms) - Normal'].str.replace(',', '').astype(int).tolist()
cpu_time_in = data['CPU Time (ms) - Secure'].str.replace(',', '').astype(int).tolist()

# Create positions for the bars
x = np.arange(len(test_types))
width = 0.35  # Width of the bars

# Create the bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Add bars for CPU Time (Out Compartment) and CPU Time (In Compartment)
bars_out = ax.bar(x - width/2, cpu_time_out, width, label='CPU Time (Out Compartment)', color='orange')
bars_in = ax.bar(x + width/2, cpu_time_in, width, label='CPU Time (In Compartment)', color='blue')

# Add labels, title, and legend
ax.set_xlabel('Test Type')
ax.set_ylabel('CPU Time (ms)')
ax.set_title('CPU Time Comparison Between In and Out Compartments')
ax.set_xticks(x)
ax.set_xticklabels(test_types)
ax.legend()

# Add grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
