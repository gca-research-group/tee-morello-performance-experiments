import pandas as pd

# Define relative paths for the input CSV files
cpu_in_file = 'cpu-in-experiment-results.csv'
cpu_out_file = 'cpu-out-experiment-results.csv'
cpu_benchmark_file = 'cpu-in-experiment-benchmarkABI-results.csv'

# Read the CSV files into DataFrames
cpu_in_data = pd.read_csv(cpu_in_file)
cpu_out_data = pd.read_csv(cpu_out_file)
cpu_benchmark_data = pd.read_csv(cpu_benchmark_file)

# Update column name to match the data provided
cpu_in_data.rename(columns={"Operation": "Trial Type"}, inplace=True)
cpu_out_data.rename(columns={"Operation": "Trial Type"}, inplace=True)
cpu_benchmark_data.rename(columns={"Operation": "Trial Type"}, inplace=True)

# Calculate the average CPU time for each trial type
cpu_in_avg = cpu_in_data.groupby("Trial Type")["CPU Time (ms)"].mean().round().reset_index()
cpu_out_avg = cpu_out_data.groupby("Trial Type")["CPU Time (ms)"].mean().round().reset_index()
cpu_benchmark_avg = cpu_benchmark_data.groupby("Trial Type")["CPU Time (ms)"].mean().round().reset_index()

# Merge the results into a single DataFrame
result = pd.merge(cpu_out_avg, cpu_in_avg, on="Trial Type", suffixes=(" - Normal", " - Secure"))
result = pd.merge(result, cpu_benchmark_avg, on="Trial Type")
result.rename(columns={"CPU Time (ms)": "CPU Time (ms) - Secure Benchmark"}, inplace=True)

# Rename categories for proper formatting
rename_map = {
    "math": "Maths (trigon. and exp. func)",
    "int": "Int",
    "float": "Float",
    "array": "Array"
}
result["Trial Type"] = result["Trial Type"].replace(rename_map)

# Define the desired order of operations
order = [
    "Maths (trigon. and exp. func)",
    "Int",
    "Float",
    "Array"
]
result = result.set_index("Trial Type").reindex(order).reset_index()

# Format the numeric values with commas
result["CPU Time (ms) - Normal"] = result["CPU Time (ms) - Normal"].apply(lambda x: f"{int(x):,}")
result["CPU Time (ms) - Secure"] = result["CPU Time (ms) - Secure"].apply(lambda x: f"{int(x):,}")
result["CPU Time (ms) - Secure Benchmark"] = result["CPU Time (ms) - Secure Benchmark"].apply(lambda x: f"{int(x):,}")

# Define the relative path for the output file
output_file = 'cpu_experiment_summary.csv'
result.to_csv(output_file, index=False)

# Success message
print(f"Results saved to {output_file}")

