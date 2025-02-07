import numpy as np
import pandas as pd
import os  # To check if the file exists

# File name
file_name = "random_trials.xlsx"

# Generate 100 random one-digit numbers
new_trial_data = np.random.randint(0, 10, 100)

# Check if the file already exists
if os.path.exists(file_name):
    # Load existing file
    with pd.ExcelWriter(file_name, mode="a", if_sheet_exists="overlay") as writer:
        df_existing = pd.read_excel(file_name, sheet_name="Trials")
        
        # Determine the next trial number
        next_trial_num = len(df_existing.columns) + 1
        next_trial_name = f"Trial {next_trial_num}"

        # Add the new column
        df_existing[next_trial_name] = new_trial_data
        df_existing.to_excel(writer, sheet_name="Trials", index=False)
        
        # Update frequency counts
        freq_df = pd.read_excel(file_name, sheet_name="Frequency", index_col=0)
        new_counts = pd.Series(new_trial_data).value_counts().sort_index()
        freq_df[next_trial_name] = new_counts.reindex(range(10), fill_value=0)
        freq_df.to_excel(writer, sheet_name="Frequency")

else:
    # Create a new DataFrame for first trial
    df_new = pd.DataFrame({ "Trial 1": new_trial_data })

    # Create frequency table for first trial
    frequency_counts = pd.Series(new_trial_data).value_counts().sort_index()
    freq_df = pd.DataFrame({"Trial 1": frequency_counts.reindex(range(10), fill_value=0)})

    # Save to a new Excel file
    with pd.ExcelWriter(file_name) as writer:
        df_new.to_excel(writer, sheet_name="Trials", index=False)
        freq_df.to_excel(writer, sheet_name="Frequency")

print(f"Excel file '{file_name}' has been updated with a new trial!")
