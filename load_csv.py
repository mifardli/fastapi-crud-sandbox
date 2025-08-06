import pandas as pd
from sqlmodel import Session
from app.database.db import engine
from app.models.lingkungan import DataLingkungan

df = pd.read_csv("Lembang_Merged_SPI_CLEANED.csv")

# Ubah NaN ke None supaya bisa masuk ke SQLite
df = df.where(pd.notnull(df), None)

with Session(engine) as session:
    for _, row in df.iterrows():
        data = DataLingkungan(
            date=row['date'],
            lon=row['lon'],
            lat=row['lat'],
            LST=row['LST'],
            NDVI=row['NDVI'],
            CHIRPS=row['CHIRPS'],
            SPI_1=row['SPI_1'],
            SPI_3=row['SPI_3'] 
        )
        session.add(data)
    session.commit()

print(" Data CSV berhasil masuk ke database!")
