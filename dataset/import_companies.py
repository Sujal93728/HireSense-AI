import pandas as pd
import psycopg2

df = pd.read_csv("dataset/companies.csv")

conn = psycopg2.connect(
    host="localhost",
    database="hiresense_db",
    user="postgres",
    password="2416"
)

cur = conn.cursor()

inserted = 0
failed = 0

for _, row in df.iterrows():
    try:
        cur.execute("""
        INSERT INTO companies(
            company_id,
            name,
            description,
            company_size,
            state,
            country,
            city,
            zip_code,
            address,
            url
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (company_id) DO NOTHING;
        """, (
            int(row["company_id"]),
            row["name"] if pd.notna(row["name"]) else None,
            row["description"] if pd.notna(row["description"]) else None,
            int(row["company_size"]) if pd.notna(row["company_size"]) else None,
            row["state"] if pd.notna(row["state"]) else None,
            row["country"] if pd.notna(row["country"]) else None,
            row["city"] if pd.notna(row["city"]) else None,
            str(row["zip_code"]) if pd.notna(row["zip_code"]) else None,
            row["address"] if pd.notna(row["address"]) else None,
            row["url"] if pd.notna(row["url"]) else None
        ))

        conn.commit()
        inserted += 1

    except Exception as e:
        conn.rollback()
        failed += 1
        print(f"Company {row['company_id']} failed: {e}")

print(f"✅ Inserted: {inserted}")
print(f"❌ Failed: {failed}")

cur.close()
conn.close()