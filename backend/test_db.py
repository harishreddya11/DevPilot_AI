from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg://postgres:Harish@123@localhost:5432/devpilot"
)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("✅ Connected to PostgreSQL successfully!")