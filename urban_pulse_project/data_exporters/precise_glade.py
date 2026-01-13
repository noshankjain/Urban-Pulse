@data_exporter
def export_data(df, *args, **kwargs):
    from sqlalchemy import create_engine

    # 1. Connection
    db_url = "postgresql://admin:password123@urbanpulse_db:5432/urban_pulse_db"
    engine = create_engine(db_url)

    # 2. Force Replace (Deletes old table, creates new one with city_tag)
    if not df.empty:
        df.to_sql('sensor_readings', engine, if_exists='append', index=False)
        print(f"✅ SUCCESS! Table replaced. Saved {len(df)} rows.")
    else:
        print("⚠️ STILL EMPTY - Did not update table.")