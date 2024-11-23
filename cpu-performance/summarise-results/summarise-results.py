import pandas as pd

# Define relative paths for the input CSV files
cpu_in_file = '../inside-tee-execution/cpu-in-experiment-result.csv'
cpu_out_file = '../outside-tee-exection/cpu-out-experiment-result.csv'

# Read the CSV files into DataFrames
cpu_in_data = pd.read_csv(cpu_in_file)
cpu_out_data = pd.read_csv(cpu_out_file)

# Calculate the average CPU time for each test type
cpu_in_avg = cpu_in_data.groupby("Test Type")["CPU Time (ms)"].mean().round().reset_index()
cpu_out_avg = cpu_out_data.groupby("Test Type")["CPU Time (ms)"].mean().round().reset_index()

# Merge the results into a single DataFrame
result = pd.merge(cpu_out_avg, cpu_in_avg, on="Test Type", suffixes=(" - Normal", " - Secure"))

# Rename categories for proper formatting
rename_map = {
    "math": "Maths (trigon. and exp. func)",
    "int": "Int",
    "float": "Float",
    "array": "Array"
}
result["Test Type"] = result["Test Type"].replace(rename_map)

# Define the desired order of operations
order = [
    "Maths (trigon. and exp. func)",
    "Int",
    "Float",
    "Array"
]
result = result.set_index("Test Type").reindex(order).reset_index()

# Format the numeric values with commas
result["CPU Time (ms) - Normal"] = result["CPU Time (ms) - Normal"].apply(lambda x: f"{int(x):,}")
result["CPU Time (ms) - Secure"] = result["CPU Time (ms) - Secure"].apply(lambda x: f"{int(x):,}")

# Define the relative path for the output file
output_file = 'cpu_experiment_summary.csv'
result.to_csv(output_file, index=False)

# Success message
print(f"Results saved to {output_file}")
