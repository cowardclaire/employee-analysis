import pandas as pd
import numpy as np

#function to load the data file and checking the data types of columns and null values

def inspect_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Show first few rows
    print("\n--- HEAD ---")
    print(df.head())

    # Show datatypes
    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    # Show missing values
    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

    return df

df = inspect_data("data-uncleaned.csv")