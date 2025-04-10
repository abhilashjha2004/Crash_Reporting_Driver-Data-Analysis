import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('Crash_Reporting_-_Drivers_Data.xlsx')
print(df.head())

# Check the shape of the dataset
print(f"Dataset Shape: {df.shape}")

# Check data types and missing values
print(df.info())

# Check summary statistics for numerical columns
print(df.describe())

# Checking for missing values
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0])

# Dropping rows with missing critical columns (example)
df.dropna(subset=['Crash Date/Time', 'Latitude', 'Longitude'], inplace=True)

# Alternatively, you can fill missing values
# data['Vehicle Make'].fillna('Unknown', inplace=True)

print()
print()

# Convert 'Crash Date/Time' to datetime
df['Crash Date/Time'] = pd.to_datetime(df['Crash Date/Time'], errors='coerce')

# Extract useful time features
df['Crash Date'] = df['Crash Date/Time'].dt.date
df['Crash Hour'] = df['Crash Date/Time'].dt.hour
df['Crash Weekday'] = df['Crash Date/Time'].dt.day_name()

# --- EDA Visualizations ---

# 1. Crash counts by type
plt.figure(figsize=(10, 4))
sns.countplot(data=df, x='ACRS Report Type', order=df['ACRS Report Type'].value_counts().index)
plt.xticks(rotation=45)
plt.title('Crash Counts by Type')
plt.tight_layout()
plt.show()

# 2. Weather conditions
plt.figure(figsize=(8, 4))
sns.countplot(data=df, x='Weather', order=df['Weather'].value_counts().index)
plt.xticks(rotation=45)
plt.title('Weather Conditions during Crashes')
plt.tight_layout()
plt.show()