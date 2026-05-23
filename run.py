import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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

#create a function to check for outliers in the dataset using the IQR method

def check_outliers(df, column):
    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found. Available columns: {df.columns.tolist()}"
        )
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers


# Check for outliers in the 'age' column
outliers_age = check_outliers(df, 'Age')    
print("\n--- OUTLIERS IN AGE ---")
if outliers_age.empty:
    print("No outliers detected in Age.")
else:
    print(outliers_age)  

# Check for outliers in the 'years at company' column
outliers_years = check_outliers(df, 'Years at Company')    
print("\n--- OUTLIERS IN YEARS AT COMPANY ---")
if outliers_years.empty:
    print("No outliers detected in Years At Company.")
else:
    print(outliers_years)  

#post outlier check on years at company, checking if the outliers are valid or not by checking the age of the employee and the years at company, if the age is less than 18 or greater than 65 and the years at company is greater than 40 then it is considered as invalid outlier

invalid_outliers = outliers_years[
    (outliers_years['Age'] < 18) |
    (outliers_years['Age'] > 65) |
    (outliers_years['Years at Company'] > 40)
]

invalid_outliers['Starting Age'] = invalid_outliers['Age'] - invalid_outliers['Years at Company']

print("\n--- INVALID OUTLIERS IN YEARS AT COMPANY ---") 
if invalid_outliers.empty:
    print("No invalid outliers detected in Years at Company.")
else:
    print(invalid_outliers[['Employee ID', 'Age', 'Years at Company', 'Starting Age']])

#removing the invalid outliers from Years at Company from the dataset

df['Starting Age'] = df['Age'] - df['Years at Company']
valid_df = df[
    (df['Starting Age'] >= 18) &
    (df['Starting Age'] <= 65) &
    (df['Years at Company'] <= 40)
]

df = valid_df.copy()
print("\n--- DATAFRAME AFTER REMOVING INVALID OUTLIERS ---")
print(df.head())

# Check for outliers in the 'Monthly Income' column
outliers_monthly_income = check_outliers(df, 'Monthly Income')
print("\n--- OUTLIERS IN MONTHLY INCOME ---")
if outliers_monthly_income.empty:
    print("No outliers detected in Monthly Income.")
else:
    print(outliers_monthly_income[['Employee ID','Job Role','Years at Company','Number of Promotions', 'Monthly Income']])

#checking category columns for unique values to identify any inconsistencies or errors in the data

for col in df.select_dtypes(include='object'):
    print(col, df[col].unique())

#checking for duplicates in the dataset based on Employee ID column
duplicates = df[df.duplicated(subset='Employee ID', keep=False)]
print("\n--- DUPLICATES BASED ON EMPLOYEE ID ---")
if duplicates.empty:
    print("No duplicates found based on Employee ID.")     
else:    print(duplicates[['Employee ID', 'Age', 'Job Role', 'Years at Company']])

#check for negative values in the dataset for columns that should not have negative values such as Age, Monthly Income, Years at Company, Number of Promotions  
negative_values = df[
    (df['Age'] < 0) |
    (df['Monthly Income'] < 0) |
    (df['Years at Company'] < 0) |
    (df['Number of Promotions'] < 0)
]
print("\n--- NEGATIVE VALUES IN THE DATASET ---")
if negative_values.empty:
    print("No negative values found in the dataset.")   
else:    print(negative_values[['Employee ID', 'Age', 'Monthly Income', 'Years at Company', 'Number of Promotions']])

#RELATIONSHIP VALIDATION

numeric_cols = ["Age", "Starting Age", "Years at Company"]

# Age vs Starting Age
plt.figure(figsize=(7, 5))
sns.scatterplot(x=df["Starting Age"], y=df["Age"])
plt.title("Scatter: Age vs Starting Age")
plt.show()

# Age vs Years at Company
plt.figure(figsize=(7, 5))
sns.scatterplot(x=df["Age"], y=df["Years at Company"])
plt.title("Scatter: Age vs Years at Company")
plt.show()

# Starting Age vs Years at Company
plt.figure(figsize=(7, 5))
sns.scatterplot(x=df["Starting Age"], y=df["Years at Company"])
plt.title("Scatter: Starting Age vs Years at Company")
plt.show()



categorical_cols = [
    "Gender", "Job Role", "Innovation Opportunities",
    "Company Reputation", "Employee Recognition", "Attrition"
]

# 2 rows × 3 columns grid
fig, axes = plt.subplots(2, 3, figsize=(20, 12), constrained_layout=True)

axes = axes.flatten()

for i, col in enumerate(categorical_cols):
    sns.countplot(x=df[col], ax=axes[i])
    axes[i].set_title(f"Category Counts: {col}", fontsize=13)
    axes[i].tick_params(axis='x', rotation=45)

# Hide any unused axes (safety)
for j in range(len(categorical_cols), len(axes)):
    fig.delaxes(axes[j])

plt.show()
