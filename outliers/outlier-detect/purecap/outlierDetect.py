"""
Programmer : Carlos Molina-Jimenez
             carlos.molina@cl.cam.ac.uk

Date       : 12 Feb 2025 

Source     : https://www.askpython.com/python/examples/how-to-determine-outliers


Method 1: Z-score
            Uses the Z-score method to find outlier from
            data given as a list.
            
Method 2: Interquartile Range (IQR)
            Uses the interquartile method to find outlier from
            data given as a list.

Method 3: Tukey’s Fences
            Uses the Turkey's fences to find outlier from
            data given as a list.
"""

import pandas as pd
import numpy as np
from scipy import stats

# Load data from CSV file
file_path = "memory-in-experiment-results.csv"
df = pd.read_csv(file_path)

# Select time-related columns for analysis
time_columns = ["Allocation Time (ms)", "Write Time (ms)", "Read Time (ms)", "Free Time (ms)"]

# Create a dictionary to store detected outliers
outliers_dict = {"Z-score": {}, "IQR": {}, "Tukey’s Fences": {}}

total_outliers = {"Z-score": 0, "IQR": 0, "Tukey’s Fences": 0}

for col in time_columns:
    data = df[col]
    
    # Method 1: Z-score
    mean = np.mean(data)
    std = np.std(data)
    threshold = 3
    z_scores = np.abs((data - mean) / std)
    outliers_z = data[z_scores > threshold]
    
    # Method 2: Interquartile Range (IQR)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    threshold_iqr = 1.5 * iqr
    outliers_iqr = data[(data < q1 - threshold_iqr) | (data > q3 + threshold_iqr)]
    
    # Method 3: Tukey’s Fences
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers_tukey = data[(data < lower_fence) | (data > upper_fence)]
    
    # Store results
    outliers_dict["Z-score"][col] = list(outliers_z.values)
    outliers_dict["IQR"][col] = list(outliers_iqr.values)
    outliers_dict["Tukey’s Fences"][col] = list(outliers_tukey.values)
    
    # Count total outliers for each method
    total_outliers["Z-score"] += len(outliers_z)
    total_outliers["IQR"] += len(outliers_iqr)
    total_outliers["Tukey’s Fences"] += len(outliers_tukey)

# Convert outlier counts to DataFrame and save to CSV
outlier_counts_df = pd.DataFrame.from_dict(outliers_dict, orient='index')
outlier_counts_df.to_csv("outliers_detected.csv", index=True)

# Convert total outlier counts to DataFrame with formatted description and save to CSV
total_outliers_df = pd.DataFrame({
    "Method": list(total_outliers.keys()),
    "Total Outliers": [f"{v} outliers detected" for v in total_outliers.values()]
})
total_outliers_df.to_csv("total_outliers.csv", index=False)

# Display detected outliers
for method, outliers in outliers_dict.items():
    print(f"\nOutliers detected by {method} method:")
    for col, values in outliers.items():
        print(f"{col}: {values if values else 'No outliers detected'}")

# Display total outliers per method
print("\nTotal outliers detected by each method:")
for method, total in total_outliers.items():
    print(f"{method}: {total} outliers detected")

