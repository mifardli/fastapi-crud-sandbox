import pandas as pd
from sqlmodel import Session
from app.models.data_spi import DataSPI
from app.database.connection import engine

#Load CSV
df = pd.read_csv("spi_dummy_for_db.csv")

# Buka Sesi ke database
with Session(engine) as session:
    for _, row in df.iterrows():
        data = DataSPI(
            tanggal=row["tanggal"],
            lokasi=row["lokasi"],
            nilai_spi=row["nilai_spi"]
        )
        session.add(data)
    
    session.commit()

print("Data berhasil dimasukkan ke database")