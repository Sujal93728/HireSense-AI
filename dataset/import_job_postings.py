import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("dataset/job_postings.csv")

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
        INSERT INTO job_postings(
            job_id, company_id, title, description,
            max_salary, med_salary, min_salary,
            pay_period, formatted_work_type, location,
            applies, original_listed_time, remote_allowed,
            views, job_posting_url, application_url,
            application_type, expiry, closed_time,
            formatted_experience_level, skills_desc,
            listed_time, posting_domain, sponsored,
            work_type, currency, compensation_type
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s
        )
        ON CONFLICT (job_id) DO NOTHING;
        """, (
            int(row["job_id"]),
            int(row["company_id"]) if pd.notna(row["company_id"]) else None,
            row["title"],
            row["description"],
            row["max_salary"] if pd.notna(row["max_salary"]) else None,
            row["med_salary"] if pd.notna(row["med_salary"]) else None,
            row["min_salary"] if pd.notna(row["min_salary"]) else None,
            row["pay_period"],
            row["formatted_work_type"],
            row["location"],
            int(row["applies"]) if pd.notna(row["applies"]) else None,
            int(row["original_listed_time"]) if pd.notna(row["original_listed_time"]) else None,
            bool(row["remote_allowed"]) if pd.notna(row["remote_allowed"]) else None,
            int(row["views"]) if pd.notna(row["views"]) else None,
            row["job_posting_url"],
            row["application_url"],
            row["application_type"],
            int(row["expiry"]) if pd.notna(row["expiry"]) else None,
            int(row["closed_time"]) if pd.notna(row["closed_time"]) else None,
            row["formatted_experience_level"],
            row["skills_desc"],
            int(row["listed_time"]) if pd.notna(row["listed_time"]) else None,
            row["posting_domain"],
            bool(row["sponsored"]) if pd.notna(row["sponsored"]) else None,
            row["work_type"],
            row["currency"],
            row["compensation_type"]
        ))

        conn.commit()
        inserted += 1

    except Exception as e:
        conn.rollback()
        failed += 1
        print(f"Job {row['job_id']} failed: {e}")

print(f"Inserted: {inserted}")
print(f"Failed: {failed}")

cur.close()
conn.close()