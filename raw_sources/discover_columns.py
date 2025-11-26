import os
import pandas as pd

# Path to your folder
folder_path = "."

# Dictionary to store results (optional)
csv_columns = {}

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)

        try:
            df = pd.read_csv(file_path)
            columns = df.columns.tolist()

            csv_columns[filename] = columns

            print(f"\n📄 File: {filename}")
            print("   Columns:", columns)

        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Optional: print full dictionary
print("\n==============================")
print("All CSV Column Mappings:")
for file, cols in csv_columns.items():
    print(f"{file}: {cols}")
