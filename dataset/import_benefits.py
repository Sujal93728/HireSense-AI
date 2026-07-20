import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("dataset/benefits.csv")

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
        inferred = None
        if pd.notna(row["inferred"]):
            if str(row["inferred"]).lower() in ["true", "1", "t", "yes"]:
                inferred = True
            elif str(row["inferred"]).lower() in ["false", "0", "f", "no"]:
                inferred = False

        cur.execute("""
            INSERT INTO benefits(job_id, inferred, type)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            int(row["job_id"]),
            inferred,
            row["type"]
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