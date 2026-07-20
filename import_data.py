failed = []

for _, row in df.iterrows():
    try:
        cur.execute("""
        INSERT INTO companies
        (company_id, name, description, company_size, state, country, city, zip_code, address, url)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (company_id) DO NOTHING;
        """, (
            int(row["company_id"]),
            row["name"],
            row["description"],
            int(row["company_size"]) if pd.notna(row["company_size"]) else None,
            row["state"],
            row["country"],
            row["city"],
            str(row["zip_code"]) if pd.notna(row["zip_code"]) else None,
            row["address"],
            row["url"]
        ))
        conn.commit()

    except Exception as e:
        conn.rollback()
        failed.append((row["company_id"], str(e)))

print("Failed rows:", len(failed))
for f in failed:
    print(f)