import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("dataset/company_industries.csv")

# Connect to PostgreSQL
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
            INSERT INTO company_industries(
                company_id,
                industry
            )
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            int(row["company_id"]),
            row["industry"] if pd.notna(row["industry"]) else None
        ))

        conn.commit()
        inserted += 1

    except Exception as e:
        conn.rollback()
        failed += 1
        print(f"Failed Company ID {row['company_id']}: {e}")

print(f"✅ Inserted: {inserted}")
print(f"❌ Failed: {failed}")

cur.close()
conn.close()