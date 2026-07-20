import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("dataset/employee_counts.csv")

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
            INSERT INTO employee_counts(
                company_id,
                employee_count,
                follower_count,
                time_recorded
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            int(row["company_id"]),
            int(row["employee_count"]) if pd.notna(row["employee_count"]) else None,
            int(row["follower_count"]) if pd.notna(row["follower_count"]) else None,
            int(row["time_recorded"]) if pd.notna(row["time_recorded"]) else None
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