import pandas as pd

df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

print("Missing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDataset Info:")
print(df.info())