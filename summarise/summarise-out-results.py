import pandas as pd

# Load the data from the cleaned CSV file
file_path = "memory-out-experiment-results.csv"
data = pd.read_csv(file_path)

# Group by "Block Size (MB)" and compute statistics, correctly handling NaN values
result = data.groupby("Block Size (MB)").agg(
    Allocation_Time_Mean=('Allocation Time (ms)', lambda x: round(x.dropna().mean(), 2) if not x.dropna().empty else 0),
    Allocation_Time_Std=('Allocation Time (ms)', lambda x: round(x.dropna().std(), 2) if not x.dropna().empty else 0),
    Write_Time_Mean=('Write Time (ms)', lambda x: round(x.dropna().mean(), 2) if not x.dropna().empty else 0),
    Write_Time_Std=('Write Time (ms)', lambda x: round(x.dropna().std(), 2) if not x.dropna().empty else 0),
    Read_Time_Mean=('Read Time (ms)', lambda x: round(x.dropna().mean(), 2) if not x.dropna().empty else 0),
    Read_Time_Std=('Read Time (ms)', lambda x: round(x.dropna().std(), 2) if not x.dropna().empty else 0),
    Free_Time_Mean=('Free Time (ms)', lambda x: round(x.dropna().mean(), 2) if not x.dropna().empty else 0),
    Free_Time_Std=('Free Time (ms)', lambda x: round(x.dropna().std(), 2) if not x.dropna().empty else 0)
).reset_index()

# Convert values to appropriate types
result['Allocation_Time_Mean'] = result['Allocation_Time_Mean']
result['Write_Time_Mean'] = result['Write_Time_Mean']
result['Read_Time_Mean'] = result['Read_Time_Mean']
result['Free_Time_Mean'] = result['Free_Time_Mean']

# Filter only block sizes between 100 MB and 1000 MB (increments of 100 MB)
valid_block_sizes = [i * 100 for i in range(1, 11)]
result = result[result["Block Size (MB)"].isin(valid_block_sizes)]

# Save the corrected results to a new CSV file using tab separation
output_file_path = "aggregated-memory-out-experiment-results.csv"
result.to_csv(output_file_path, index=False, sep="\t")

print("Corrected results saved to:", output_file_path)
print(result)
