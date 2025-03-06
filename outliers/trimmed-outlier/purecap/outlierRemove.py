import pandas as pd
import numpy as np

# Load the original dataset
file_path = "memory-in-experiment-results.csv"
df = pd.read_csv(file_path)

# Columns to be analysed
time_columns = ["Allocation Time (ms)", "Write Time (ms)", "Read Time (ms)", "Free Time (ms)"]

# Dictionary to store indices and count of outliers per record
outlier_counts = {}

# Create a copy of the DataFrame to replace outliers with NaN
df_cleaned = df.copy()

# Dictionary to store detected outliers per column
outliers_detected = {col: [] for col in time_columns}

# Detect outliers using the Interquartile Range (IQR) method
for col in time_columns:
    data = df[col]
    
    # Calculate IQR
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    threshold_iqr = 1.5 * iqr

    # Identify outlier indices in the current column
    col_outliers = df[(data < q1 - threshold_iqr) | (data > q3 + threshold_iqr)]

    # Store detected outlier values
    outliers_detected[col] = col_outliers[col].tolist()

    # Update outlier count per record
    for index in col_outliers.index:
        if index in outlier_counts:
            outlier_counts[index] += 1  # Record already has another outlier, increment count
        else:
            outlier_counts[index] = 1  # First outlier detected for this record

    # Replace outlier values with NaN
    df_cleaned.loc[col_outliers.index, col] = np.nan

# Compute the total number of affected records and check how many have multiple outliers
total_outlier_records = len(outlier_counts)
multiple_outliers = sum(1 for count in outlier_counts.values() if count > 1)

# Display information about detected outliers
print(f"\nTotal records affected by outliers: {total_outlier_records} (expected: 250)")
print(f"Records containing multiple outliers: {multiple_outliers}")

# Display all detected outliers per column
print("\nOutliers detected per column:")
for col, values in outliers_detected.items():
    print(f"\n{col}:")
    print(values)  # Display all detected outlier values for the column

# Save the cleaned DataFrame (with outliers replaced by NaN) to a new CSV file
output_file = "memory-out-experiment-results-no-outliers-cleaned.csv"
df_cleaned.to_csv(output_file, index=False)

print(f"\nFile saved: {output_file} (outlier values replaced with NaN)")

