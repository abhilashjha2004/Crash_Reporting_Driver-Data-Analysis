import pandas as pd

data = pd.read_csv(r'C:\Users\abhil\PycharmProjects\PythonProject\Crash_Reporting_-_Drivers_Data.csv')
print(data.head())

# Check the shape of the dataset
print(f"Dataset Shape: {data.shape}")

# Check data types and missing values
print(data.info())

# Check summary statistics for numerical columns
print(data.describe())

# Checking for missing values
missing_data = data.isnull().sum()
print(missing_data[missing_data > 0])

# Dropping rows with missing critical columns (example)
data.dropna(subset=['Crash Date/Time', 'Latitude', 'Longitude'], inplace=True)

# Alternatively, you can fill missing values
# data['Vehicle Make'].fillna('Unknown', inplace=True)
