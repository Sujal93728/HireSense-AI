import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/jobs_skills.csv")

# Show the first 5 rows
print("First 5 rows:")
print(df.head())

# Show dataset information
print("\nDataset Info:")
print(df.info())

# Show missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Show column names
print("\nColumns:")
print(df.columns.tolist())