# -*- coding: utf-8 -*-
"""Data Anlayst IIM Banagalore Task.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gtFstK4f0Wmj4W-wpFHs4yTZMW_EmhZg
"""

# Install necessary libraries
!pip install pandas openpyxl matplotlib seaborn

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files

# Set style for better visualizations
plt.style.use('seaborn-v0_8')

# Upload the dataset
print("Please upload the Excel file.")
uploaded = files.upload()

# Load the dataset
df = pd.read_excel(list(uploaded.keys())[0])

# Dataset Overview
print("Dataset Shape:", df.shape)
print("\
First few rows of the dataset:")
print(df.head())

# Display data info and missing values
print("\
Dataset Info:")
print(df.info())

print("\
Missing Values Count:")
print(df.isnull().sum())

# Visualize missing values using a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.show()

# Calculate price differences and their percentage
df['price_difference'] = df['metered_price'] - df['upfront_price']
df['price_difference_percentage'] = (df['price_difference'] / df['upfront_price']) * 100

# Scatter plot: Upfront Price vs Metered Price
plt.figure(figsize=(10, 6))
plt.scatter(df['upfront_price'], df['metered_price'], alpha=0.5)
plt.plot([0, df['upfront_price'].max()], [0, df['upfront_price'].max()], 'r--')  # Perfect prediction line
plt.xlabel('Upfront Price')
plt.ylabel('Metered Price')
plt.title('Upfront Price vs Metered Price')
plt.show()

# Calculate percentage of rides with >20% deviation
deviation_threshold = 20
high_deviation = df[abs(df['price_difference_percentage']) > deviation_threshold]
deviation_percentage = (len(high_deviation) / len(df)) * 100

print(f"\
Percentage of rides with >20% price deviation: {deviation_percentage:.2f}%")

# Basic statistics of price differences
print("\
Price Difference Statistics:")
print(df['price_difference'].describe())

# Investigate factors contributing to price deviations
# Analyze deviation by GPS confidence
plt.figure(figsize=(10, 6))
sns.boxplot(x='gps_confidence', y='price_difference_percentage', data=df)
plt.title('Price Deviation by GPS Confidence')
plt.xlabel('GPS Confidence')
plt.ylabel('Price Difference Percentage')
plt.show()

# Analyze deviation by destination change number
plt.figure(figsize=(10, 6))
sns.boxplot(x='dest_change_number', y='price_difference_percentage', data=df)
plt.title('Price Deviation by Destination Change Number')
plt.xlabel('Destination Change Number')
plt.ylabel('Price Difference Percentage')
plt.show()

# Analyze deviation by prediction price type
plt.figure(figsize=(10, 6))
sns.boxplot(x='prediction_price_type', y='price_difference_percentage', data=df)
plt.title('Price Deviation by Prediction Price Type')
plt.xlabel('Prediction Price Type')
plt.ylabel('Price Difference Percentage')
plt.show()





# Summarize key factors affecting price accuracy
# Group by GPS confidence and calculate mean price deviation percentage
gps_confidence_summary = df.groupby('gps_confidence')['price_difference_percentage'].mean().reset_index()
print("\
Mean Price Deviation Percentage by GPS Confidence:")
print(gps_confidence_summary)

# Group by destination change number and calculate mean price deviation percentage
dest_change_summary = df.groupby('dest_change_number')['price_difference_percentage'].mean().reset_index()
print("\
Mean Price Deviation Percentage by Destination Change Number:")
print(dest_change_summary)

# Group by prediction price type and calculate mean price deviation percentage
prediction_type_summary = df.groupby('prediction_price_type')['price_difference_percentage'].mean().reset_index()
print("\
Mean Price Deviation Percentage by Prediction Price Type:")
print(prediction_type_summary)

# Data Quality Check
# Check for duplicate rows
duplicates = df.duplicated().sum()
print("\
Number of duplicate rows:", duplicates)

# Check for missing values again
missing_values = df.isnull().sum()
print("\
Missing Values Count:")
print(missing_values)





# Address missing values by imputing or dropping rows/columns with significant missing data
# Drop rows where 'upfront_price' or 'metered_price' is missing, as these are critical for analysis
df_cleaned = df.dropna(subset=['upfront_price', 'metered_price'])

# Impute missing values in 'price_difference_percentage' with the mean of the column
df_cleaned['price_difference_percentage'].fillna(df_cleaned['price_difference_percentage'].mean(), inplace=True)

# Verify the cleaned dataset
print("\
Cleaned Dataset Shape:", df_cleaned.shape)
print("\
Missing Values Count After Cleaning:")
print(df_cleaned.isnull().sum())

# Save the cleaned dataset for further analysis
df_cleaned.to_csv('cleaned_dataset.csv', index=False)
print("\
Cleaned dataset saved as 'cleaned_dataset.csv'.")





# Here I am modifying my approach to focus on numerical columns only
numerical_columns = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = df_cleaned[numerical_columns].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True)
plt.title('Correlation Heatmap (Numerical Variables)')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate summary statistics for key metrics
print("\
Key Metrics Summary:")
metrics_summary = df_cleaned[['metered_price', 'upfront_price', 'distance', 'duration', 'predicted_distance', 'predicted_duration']].describe()
print(metrics_summary)

# Calculate accuracy metrics
df_cleaned['distance_accuracy'] = abs(df_cleaned['predicted_distance'] - df_cleaned['distance']) / df_cleaned['distance'] * 100
df_cleaned['duration_accuracy'] = abs(df_cleaned['predicted_duration'] - df_cleaned['duration']) / df_cleaned['duration'] * 100

print("\
Prediction Accuracy Metrics:")
print("\
Distance Prediction Error (%):")
print(df_cleaned['distance_accuracy'].describe())
print("\
Duration Prediction Error (%):")
print(df_cleaned['duration_accuracy'].describe())







# Analyze trends over time and identify outliers
# Convert 'calc_created' to datetime for time-based analysis
df_cleaned['calc_created'] = pd.to_datetime(df_cleaned['calc_created'], unit='ms')

# Extract year and month for trend analysis
df_cleaned['year_month'] = df_cleaned['calc_created'].dt.to_period('M')

# Analyze price deviation trends over time
price_trend = df_cleaned.groupby('year_month')['price_difference_percentage'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(price_trend['year_month'].astype(str), price_trend['price_difference_percentage'], marker='o', linestyle='-', color='b')
plt.title('Price Deviation Trends Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Average Price Difference Percentage')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Identify outliers in price deviation
plt.figure(figsize=(10, 6))
sns.boxplot(y='price_difference_percentage', data=df_cleaned)
plt.title('Outliers in Price Deviation')
plt.ylabel('Price Difference Percentage')
plt.show()

# Save the dataset with time-based features for further analysis
df_cleaned.to_csv('cleaned_dataset_with_time_features.csv', index=False)
print("\
Dataset with time-based features saved as 'cleaned_dataset_with_time_features.csv'.")









# 1. Price Prediction Accuracy Analysis

# Calculate price difference metrics
df_cleaned['absolute_price_diff'] = abs(df_cleaned['metered_price'] - df_cleaned['upfront_price'])
df_cleaned['price_accuracy'] = (1 - abs(df_cleaned['metered_price'] - df_cleaned['upfront_price'])/df_cleaned['metered_price']) * 100

# Overall price prediction accuracy metrics
print("\
Price Prediction Accuracy Statistics:")
print(df_cleaned['price_accuracy'].describe())

# Analyze accuracy by GPS confidence
gps_accuracy = df_cleaned.groupby('gps_confidence')['price_accuracy'].agg(['mean', 'count', 'std']).round(2)
print("\
Price Accuracy by GPS Confidence:")
print(gps_accuracy)

# Visualize price prediction accuracy
plt.figure(figsize=(12, 6))
plt.scatter(df_cleaned['upfront_price'], df_cleaned['metered_price'], alpha=0.5)
plt.plot([0, df_cleaned['upfront_price'].max()], [0, df_cleaned['upfront_price'].max()], 'r--')  # Perfect prediction line
plt.xlabel('Upfront Price')
plt.ylabel('Metered Price')
plt.title('Upfront vs Metered Price Comparison')
plt.tight_layout()
plt.show()

# Distribution of price differences
plt.figure(figsize=(10, 6))
sns.histplot(data=df_cleaned, x='price_accuracy', bins=50)
plt.title('Distribution of Price Prediction Accuracy')
plt.xlabel('Price Accuracy (%)')
plt.ylabel('Count')
plt.show()

# Calculate percentage of rides within different accuracy thresholds
accuracy_thresholds = {
    'Within 5%': (df_cleaned['price_accuracy'] >= 95).mean() * 100,
    'Within 10%': (df_cleaned['price_accuracy'] >= 90).mean() * 100,
    'Within 20%': (df_cleaned['price_accuracy'] >= 80).mean() * 100
}

print("\
Percentage of Rides within Accuracy Thresholds:")
for threshold, percentage in accuracy_thresholds.items():
    print(f"{threshold}: {percentage:.2f}%")





# 2. Route Analysis: Predicted vs Actual Distance and Duration

# Calculate distance and duration prediction errors
df_cleaned['distance_error'] = abs(df_cleaned['predicted_distance'] - df_cleaned['distance'])
df_cleaned['duration_error'] = abs(df_cleaned['predicted_duration'] - df_cleaned['duration'])

# Summary statistics for distance and duration errors
print("\
Distance Prediction Error Statistics:")
print(df_cleaned['distance_error'].describe())

print("\
Duration Prediction Error Statistics:")
print(df_cleaned['duration_error'].describe())

# Visualize predicted vs actual distances
plt.figure(figsize=(12, 6))
plt.scatter(df_cleaned['predicted_distance'], df_cleaned['distance'], alpha=0.5, color='g')
plt.plot([0, df_cleaned['predicted_distance'].max()], [0, df_cleaned['predicted_distance'].max()], 'r--')  # Perfect prediction line
plt.xlabel('Predicted Distance')
plt.ylabel('Actual Distance')
plt.title('Predicted vs Actual Distance')
plt.tight_layout()
plt.show()

# Visualize predicted vs actual durations
plt.figure(figsize=(12, 6))
plt.scatter(df_cleaned['predicted_duration'], df_cleaned['duration'], alpha=0.5, color='b')
plt.plot([0, df_cleaned['predicted_duration'].max()], [0, df_cleaned['predicted_duration'].max()], 'r--')  # Perfect prediction line
plt.xlabel('Predicted Duration')
plt.ylabel('Actual Duration')
plt.title('Predicted vs Actual Duration')
plt.tight_layout()
plt.show()

# Save dataset with route analysis features
df_cleaned.to_csv('cleaned_dataset_with_route_analysis.csv', index=False)
print("\
Dataset with route analysis features saved as 'cleaned_dataset_with_route_analysis.csv'.")







# 3. User Experience Analysis

# Analyze overpaid rides
print("\
Overpaid Rides Analysis:")
overpaid_rides = df_cleaned[df_cleaned['overpaid_ride_ticket'] == 1]
print("Number of Overpaid Rides:", len(overpaid_rides))
print("Percentage of Overpaid Rides:", len(overpaid_rides) / len(df_cleaned) * 100)

# Analyze user indicators and their impact on price accuracy
user_indicator_accuracy = df_cleaned.groupby('us_indicator')['price_accuracy'].agg(['mean', 'count', 'std']).round(2)
print("\
Price Accuracy by User Indicator:")
print(user_indicator_accuracy)

# Analyze app versions and their impact on price accuracy
rider_app_accuracy = df_cleaned.groupby('rider_app_version')['price_accuracy'].mean().sort_values(ascending=False).head(10)
print("\
Top 10 Rider App Versions by Price Accuracy:")
print(rider_app_accuracy)

# Visualize overpaid rides by app version
plt.figure(figsize=(12, 6))
overpaid_rides_by_app = overpaid_rides['rider_app_version'].value_counts().head(10)
overpaid_rides_by_app.plot(kind='bar', color='orange')
plt.title('Top 10 Rider App Versions with Overpaid Rides')
plt.xlabel('Rider App Version')
plt.ylabel('Count of Overpaid Rides')
plt.tight_layout()
plt.show()

# Save dataset with user experience features
df_cleaned.to_csv('cleaned_dataset_with_user_experience.csv', index=False)
print("\
Dataset with user experience features saved as 'cleaned_dataset_with_user_experience.csv'.")





import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Route Analysis
# 1. GPS Confidence Analysis
plt.figure(figsize=(10, 6))
sns.boxplot(x='gps_confidence', y='metered_price', data=df)
plt.title('Impact of GPS Confidence on Metered Price')
plt.show()

# 2. Route Efficiency Analysis
df['distance_accuracy'] = (df['predicted_distance'] - df['distance']) / df['predicted_distance'] * 100
df['duration_accuracy'] = (df['predicted_duration'] - df['duration']) / df['predicted_duration'] * 100

print("\
Route Prediction Accuracy Statistics:")
print("\
Distance Prediction Accuracy (%):")
print(df['distance_accuracy'].describe())
print("\
Duration Prediction Accuracy (%):")
print(df['duration_accuracy'].describe())

# 3. Destination Changes Analysis
plt.figure(figsize=(10, 6))
sns.boxplot(x='dest_change_number', y='metered_price', data=df)
plt.title('Impact of Destination Changes on Metered Price')
plt.show()

# Calculate average price difference by destination changes
dest_changes_analysis = df.groupby('dest_change_number').agg({
    'metered_price': 'mean',
    'upfront_price': 'mean',
    'order_id_new': 'count'
}).reset_index()
dest_changes_analysis['price_difference'] = dest_changes_analysis['metered_price'] - dest_changes_analysis['upfront_price']
dest_changes_analysis = dest_changes_analysis.rename(columns={'order_id_new': 'number_of_rides'})

print("\
Destination Changes Impact Analysis:")
print(dest_changes_analysis)







import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. App Version Analysis
plt.figure(figsize=(12, 6))
rider_app_counts = df['rider_app_version'].value_counts().head(10)
plt.bar(rider_app_counts.index, rider_app_counts.values)
plt.title('Top 10 Rider App Versions')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate average metrics by app version
app_metrics = df.groupby('rider_app_version').agg({
    'metered_price': 'mean',
    'distance': 'mean',
    'duration': 'mean',
    'order_id_new': 'count'
}).reset_index()
app_metrics = app_metrics.rename(columns={'order_id_new': 'number_of_rides'})
app_metrics = app_metrics.sort_values('number_of_rides', ascending=False).head(10)

print("\
Top 10 Rider App Versions Performance Metrics:")
print(app_metrics)

# 2. Device Analysis
device_metrics = df.groupby('device_name').agg({
    'metered_price': 'mean',
    'distance': 'mean',
    'duration': 'mean',
    'order_id_new': 'count'
}).reset_index()
device_metrics = device_metrics.rename(columns={'order_id_new': 'number_of_rides'})
device_metrics = device_metrics.sort_values('number_of_rides', ascending=False).head(10)

print("\
Top 10 Devices Performance Metrics:")
print(device_metrics)

# 3. Fraud Analysis
plt.figure(figsize=(10, 6))
sns.boxplot(x='overpaid_ride_ticket', y='metered_price', data=df)
plt.title('Metered Price Distribution by Overpaid Ride Status')
plt.show()

# Calculate fraud statistics
fraud_stats = df.groupby('overpaid_ride_ticket').agg({
    'metered_price': ['mean', 'count'],
    'fraud_score': 'mean'
}).reset_index()

print("\
Fraud Analysis Statistics:")
print(fraud_stats)







import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Calculate price difference and percentage
df['price_difference'] = df['metered_price'] - df['upfront_price']
df['price_difference_percentage'] = (df['price_difference'] / df['upfront_price']) * 100

# Create deviation category
df['significant_deviation'] = df['price_difference_percentage'].abs() > 20

# 1. Overall pricing accuracy analysis
plt.figure(figsize=(10, 6))
plt.hist(df['price_difference_percentage'].dropna(), bins=50)
plt.title('Distribution of Price Differences (%)')
plt.xlabel('Price Difference (%)')
plt.ylabel('Count')
plt.axvline(x=20, color='r', linestyle='--', label='+20%')
plt.axvline(x=-20, color='r', linestyle='--', label='-20%')
plt.legend()
plt.show()

# Summary statistics
print("Pricing Accuracy Analysis:")
print("\
Price Difference Statistics:")
print(df['price_difference'].describe())
print("\
Percentage of Rides with >20% Deviation:")
print(df['significant_deviation'].mean() * 100, "% of rides")

# 2. Analysis by GPS confidence
gps_accuracy = df.groupby('gps_confidence').agg({
    'significant_deviation': ['mean', 'count'],
    'price_difference_percentage': ['mean', 'std']
}).round(2)

print("\
GPS Confidence Impact on Pricing Accuracy:")
print(gps_accuracy)

# 3. Analysis by prediction price type
prediction_type_analysis = df.groupby('prediction_price_type').agg({
    'significant_deviation': ['mean', 'count'],
    'price_difference_percentage': ['mean', 'std']
}).round(2)

print("\
Prediction Type Impact on Pricing Accuracy:")
print(prediction_type_analysis)

# 4. Correlation with distance and duration
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(df['distance'], df['price_difference_percentage'], alpha=0.5)
plt.title('Price Difference vs Distance')
plt.xlabel('Distance')
plt.ylabel('Price Difference (%)')

plt.subplot(1, 2, 2)
plt.scatter(df['duration'], df['price_difference_percentage'], alpha=0.5)
plt.title('Price Difference vs Duration')
plt.xlabel('Duration')
plt.ylabel('Price Difference (%)')
plt.tight_layout()
plt.show()











# Deep Dive Analysis: Destination Changes and Ride Characteristics

# Analyze impact of destination changes on pricing accuracy
destination_change_analysis = df.groupby('dest_change_number').agg({
    'significant_deviation': ['mean', 'count'],
    'price_difference_percentage': ['mean', 'std']
}).round(2)

print("\
Destination Change Impact on Pricing Accuracy:")
print(destination_change_analysis)

# Correlation analysis for ride characteristics
correlation_matrix = df[['distance', 'duration', 'gps_confidence', 'price_difference_percentage']].corr()

print("\
Correlation Matrix for Ride Characteristics:")
print(correlation_matrix)

# Visualize correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix for Ride Characteristics')
plt.show()

# Business Recommendations
recommendations = """
1. Improve GPS Accuracy:
   - Focus on rides with low GPS confidence as they show higher pricing deviations.
   - Invest in better GPS tracking and error correction algorithms.

2. Handle Destination Changes Better:
   - Rides with destination changes show significant pricing deviations.
   - Implement dynamic pricing adjustments for destination changes in real-time.

3. Optimize Prediction Algorithms:
   - Enhance prediction models for distance and duration to reduce pricing errors.
   - Focus on rides with long distances and durations as they show higher deviations.

4. Monitor and Address Outliers:
   - Identify and investigate rides with extreme pricing deviations to improve accuracy.

5. Improve Communication with Customers:
   - Notify customers about potential pricing changes due to destination changes or other factors.
"""

print("\
Business Recommendations:")
print(recommendations)





















