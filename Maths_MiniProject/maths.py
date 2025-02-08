import numpy as np
import pandas as pd
import os

# File name
file_name = "random_trials.xlsx"

# Number of trials
num_trials = 1000  # 1000 trials
num_digits = 100  # Each trial has 100 random digits

# Generate 200 trials of 100 one-digit numbers (0-9)
trial_data = {f"Trial {i+1}": np.random.randint(0, 10, num_digits) for i in range(num_trials)}

# Create a DataFrame
df_trials = pd.DataFrame(trial_data)

# Calculate the count of even numbers in each trial
df_trials.loc["Even Count"] = df_trials.apply(lambda col: (col % 2 == 0).sum())

# Calculate frequency of digits (0-9) across all trials
digit_counts = {f"Trial {i+1}": pd.Series(trial_data[f"Trial {i+1}"]).value_counts().reindex(range(10), fill_value=0)
                for i in range(num_trials)}

df_freq = pd.DataFrame(digit_counts)

# Compute total even number count across all trials
total_even_count = df_trials.loc["Even Count"].sum()
df_freq.loc["Total Even Count"] = total_even_count  # Add total even count row

# Save to Excel
with pd.ExcelWriter(file_name) as writer:
    df_trials.to_excel(writer, sheet_name="Trials", index=False)
    df_freq.to_excel(writer, sheet_name="Frequency")

print(f"Excel file '{file_name}' has been created with 1000 trials!")
