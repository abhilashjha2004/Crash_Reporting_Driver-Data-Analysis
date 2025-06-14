import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('Crash_Reporting_-_Drivers_Data.xlsx')
print(df.head())

print(df.tail())
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

# Convert 'Crash Date/Time' to datetime
df['Crash Date/Time'] = pd.to_datetime(df['Crash Date/Time'], errors='coerce')

# Extract useful time features
df['Crash Date'] = df['Crash Date/Time'].dt.date
df['Crash Hour'] = df['Crash Date/Time'].dt.hour
df['Crash Weekday'] = df['Crash Date/Time'].dt.day_name()

# Step 2: Select only numerical columns
numerical_df = df.select_dtypes(include='number')

# Step 3: Drop rows with missing values
cleaned_df = numerical_df.dropna()

# Step 4: Calculate IQR for each column
Q1 = cleaned_df.quantile(0.25)
Q3 = cleaned_df.quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Step 5: Detect outliers
outliers = (cleaned_df < lower_bound) | (cleaned_df > upper_bound)
outlier_summary = outliers.sum()

# Step 6: Remove rows with any outliers
non_outliers_df = cleaned_df[~outliers.any(axis=1)]

# Step 7: Compute covariance matrix
cov_matrix = non_outliers_df.cov()

# Step 8: Save cleaned data to Excel
non_outliers_df.to_excel("Cleaned_Crash_Data.xlsx", index=False)

# Print summary
print("Lower Bound:\n", lower_bound)
print("\nUpper Bound:\n", upper_bound)
print("\nOutliers Detected (count):\n", outlier_summary)
print("\nCovariance Matrix:\n", cov_matrix)


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

# 3. Crashes by hour
plt.figure(figsize=(10, 4))
sns.histplot(df['Crash Hour'].dropna(), bins=24, kde=True)
plt.title('Crashes by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Crashes')
plt.tight_layout()
plt.show()

# 4. Light conditions
plt.figure(figsize=(8, 4))
sns.countplot(data=df, y='Light', order=df['Light'].value_counts().index)
plt.title('Crashes by Light Condition')
plt.tight_layout()
plt.show()

# 5. Injury severity
plt.figure(figsize=(8, 4))
sns.countplot(data=df, y='Injury Severity', order=df['Injury Severity'].value_counts().index)
plt.title('Crash Injury Severity Distribution')
plt.tight_layout()
plt.show()

# 6. Crash locations on map (scatterplot of lat/long)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Longitude', y='Latitude', data=df, hue='ACRS Report Type', palette='Set1')
plt.title("Crash Locations (Lat vs Long)")
plt.tight_layout()
plt.show()

# --- BAR CHART: Number of crashes per weekday ---
plt.figure(figsize=(8, 4))
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.countplot(data=df, x='Crash Weekday', order=order)
plt.title("Number of Crashes per Weekday")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- BOX PLOT: Crash hour distribution per weekday ---
plt.figure(figsize=(10, 5))
sns.boxplot(x='Crash Weekday', y='Crash Hour', data=df, order=order)
plt.title("Crash Time Distribution by Weekday")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- HEATMAP: Crash frequency by Hour vs Weekday ---
# Create a pivot table
pivot = df.pivot_table(index='Crash Weekday', columns='Crash Hour', values='Crash Date/Time', aggfunc='count')
pivot = pivot.reindex(order)  # Order weekdays correctly

plt.figure(figsize=(12, 6))
sns.heatmap(pivot, cmap='Reds', linewidths=.5, annot=True, fmt=".0f")
plt.title("Heatmap of Crashes (Weekday vs Hour)")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.tight_layout()
plt.show()




