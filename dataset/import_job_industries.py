import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("dataset/job_industries.csv")

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
            INSERT INTO job_industries(job_id, industry_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            int(row["job_id"]),
            int(row["industry_id"])
        ))

        conn.commit()
        inserted += 1

    except Exception as e:
        conn.rollback()
        failed += 1
        print(f"Failed Job ID {row['job_id']}: {e}")

print(f"✅ Inserted: {inserted}")
print(f"❌ Failed: {failed}")

cur.close()
conn.close()