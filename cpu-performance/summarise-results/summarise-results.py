import pandas as pd

# Define the paths to the input CSV files
cpu_in_file = '../inside-tee-execution/cpu-in-experiment-result.csv'
cpu_out_file = '../outside-tee-exection/cpu-out-experiment-result.csv'

# Load the CSV files
cpu_in_data = pd.read_csv(cpu_in_file)
cpu_out_data = pd.read_csv(cpu_out_file)

# Calculate the average CPU time for each operation type
cpu_in_avg = cpu_in_data.groupby("Test Type")["CPU Time (ms)"].mean().round().reset_index()
cpu_out_avg = cpu_out_data.groupby("Test Type")["CPU Time (ms)"].mean().round().reset_index()

# Merge the results into a single DataFrame
result = pd.merge(cpu_out_avg, cpu_in_avg, on="Test Type", suffixes=(" - Normal", " - Secure"))

# Rename columns for clarity
result.rename(columns={"Test Type": "Test Type",
                       "CPU Time (ms) - Normal": "CPU Time (ms) - Normal",
                       "CPU Time (ms) - Secure": "CPU Time (ms) - Secure"}, inplace=True)

# Save the merged results to the output CSV file
output_file = 'cpu_experiment_summary.csv'
result.to_csv(output_file, index=False)

# Success message
print(f"Results saved to {output_file}")
