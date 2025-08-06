from app.database.db import create_db_and_tables
from app.models import lingkungan  

if __name__ == "__main__":
    create_db_and_tables()
    print("Tabel berhasil dibuat")
