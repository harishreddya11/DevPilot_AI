from app.db.base import Base

import app.models

print("Tables:")
print(Base.metadata.tables.keys())