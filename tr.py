import pandas as pd

# Load the CSV file (adjust the path if it's in a folder)
df = pd.read_csv("your_file.csv")

# Keep only the first 10,000 rows
df = df.head(10000)

# Overwrite the original file
df.to_csv(r"C:\Users\abhil\PycharmProjects\PythonProject\Crash_Reporting_-_Drivers_Data.csv", index=False)

print("✅ CSV file updated successfully.")
