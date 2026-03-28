import pandas as pd

# Load Excel file
df = pd.read_csv("customer_shopping_behavior.csv")

# Display first 5 rows
print(df.head())

# display data structure
print(df.info())

# display summary statitics 
print(df.describe(include='all'))

# checking for missing values
print(df.isnull().sum())

# replacing missing values
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

# replace columns names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")

# rename purchase name
# df.columns = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)


# feature engineering
# create  a column age group
lables = ["young_adults","adults","middle_aged","senior"]
df['age_group'] = pd.qcut(df['age'], q=4, labels= lables)
print(df[["age","age_group"]].head(5))
print(df.head())

# finding unique items in freuency_of_purchase column
print(df['frequency_of_purchases'].unique())

# create column purchase frequency days
frequency_mapping = {
    'Fortnightly' :14,
    'Weekly': 7,
    'Annually':365,
    'Quarterly' :90,
    'Bi-Weekly':14,
    'Monthly':30,
    'Every 3 Months':90,
 }

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['customer_id','frequency_of_purchases','purchase_frequency_days']].head())

# checking promo_code_used and discount used are same
print(df[["discount_applied","promo_code_used"]].head(10))

# revoming promo_code column
df = df.drop('promo_code_used',axis =1)
print(df.head(5))

# connecting to sql



from sqlalchemy import create_engine

# PostgreSQL credentials
host = "localhost"
port = "5432"
database = "customer_behavior"
username = "postgres"
password = "ZXCVBNM"

# Create engine using SQLAlchemy + psycopg2
engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# WRITE THE CLEANED DATAFRAME (NOT RAW CSV!)
df.to_sql("customer", engine, if_exists="replace", index=False)

print("Data loaded successfully!")