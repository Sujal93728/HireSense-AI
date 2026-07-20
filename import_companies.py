import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:2416@localhost:5432/hiresense_db"
)

df = pd.read_csv(r"C:\Users\sujal\OneDrive\Desktop\New folder\companies.csv")

df.to_sql("companies", engine, if_exists="append", index=False)

print("Import completed!")