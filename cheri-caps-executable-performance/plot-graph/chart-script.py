import pandas as pd
import matplotlib.pyplot as plt

# Load data 
data = pd.read_csv('../cheri-cap-experiment-results.csv')

# Extract the necessary columns
processes = data['Number of Processes']
memory_usage = data['Memory Used (MB)']
elapsed_time = data['Time Elapsed (ms)']

# Adjust the elapsed time scale to improve visualisation (e.g. divide by 1000)
elapsed_time_scaled = elapsed_time / 1000  # Converting to seconds

# Create a figure with two Y axes
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Memory Usage on the first Y axis (left)
ax1.set_xlabel('Number of compartments')
ax1.set_ylabel('Memory Usage (MB)', color='blue')
ax1.plot(processes, memory_usage, label='Memory Usage (MB)', color='blue', marker='o')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second Y axis for Elapsed Time
ax2 = ax1.twinx()
ax2.set_ylabel('Elapsed Time (s)', color='orange')  # Using the scale set to seconds
ax2.plot(processes, elapsed_time_scaled, label='Elapsed Time (s)', color='orange', marker='s')
ax2.tick_params(axis='y', labelcolor='orange')

# Add title and grid
plt.title('Memory Usage and Elapsed Time vs Number of compartments')
plt.grid(True)

# Adjust the layout and display the graphic
plt.tight_layout()
plt.show()
