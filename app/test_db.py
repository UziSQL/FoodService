from app.database import engine

try:
    with engine.connect() as conn:
        print("✅ Connected to DB successfully!")
except Exception as e:
    print("❌ Error:", e)