from sqlmodel import create_engine, SQLModel
#Setup koneksi SQLite
engine = create_engine("sqlite:///dummy.spi.db")

#Buat table saat startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    