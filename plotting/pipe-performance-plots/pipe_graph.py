import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
data_out = pd.read_csv('pipe-out-experiment-results.csv')
data_in = pd.read_csv('pipe-in-experiment-purecap-results.csv')
data_benchmark = pd.read_csv('pipe-in-experiment-purecap-benchmark-results.csv')


# Determine the maximum time range for Y-axis across all graphs
max_time = max(
    data_in[['Write Time (ms)', 'Read Time (ms)']].max().max(),
    data_benchmark[['Write Time (ms)', 'Read Time (ms)']].max().max(),
    data_out[['Write Time (ms)', 'Read Time (ms)']].max().max()
)

# Create a figure with a balanced size and appropriate spacing
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 6))

# Graph for pipe-out-experiment-results.csv
ax3.plot(data_out['Test'], data_out['Write Time (ms)'], label='Write Time (ms)', color='blue', marker='o')
ax3.plot(data_out['Test'], data_out['Read Time (ms)'], label='Read Time (ms)', color='green', marker='x')
ax3.set_title('Out Compartment', fontsize=14)
#ax3.set_xlabel('Trial', fontsize=12)  # Change Test to Trial
ax3.legend(fontsize=10)
ax3.grid(True)
ax3.set_ylim(0, max_time)
ax3.tick_params(axis='y', left=False, labelleft=False)  # Remove Y-axis labels and ticks

# Graph for pipe-in-experiment-purecap-results.csv
ax1.plot(data_in['Test'], data_in['Write Time (ms)'], label='Write Time (ms)', color='blue', marker='o')
ax1.plot(data_in['Test'], data_in['Read Time (ms)'], label='Read Time (ms)', color='green', marker='x')
ax1.set_title('purecap ABI', fontsize=14)
#ax1.set_xlabel('Trial', fontsize=12)  # Change Test to Trial
ax1.set_ylabel('Time (ms)', fontsize=12, labelpad=4)
ax1.legend(fontsize=10)
ax1.grid(True)
ax1.set_ylim(0, max_time)

# Graph for pipe-in-experiment-purecap-benchmark-results.csv
ax2.plot(data_benchmark['Test'], data_benchmark['Write Time (ms)'], label='Write Time (ms)', color='blue', marker='o')
ax2.plot(data_benchmark['Test'], data_benchmark['Read Time (ms)'], label='Read Time (ms)', color='green', marker='x')
ax2.set_title('purecap-benchmark ABI', fontsize=14)
ax2.set_xlabel('Trial', fontsize=12)  # Change Test to Trial
ax2.legend(fontsize=10)
ax2.grid(True)
ax2.set_ylim(0, max_time)
ax2.tick_params(axis='y', left=False, labelleft=False)  # Remove Y-axis labels and ticks

# Adjust spacing between graphs and margins
plt.subplots_adjust(left=0.06, right=0.98, wspace=0.05, bottom=0.15)

# Display the figure
plt.show()

