from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, select
from typing import Optional
from database import engine, create_db_and_tables
#Inisiasi FastAPI
app = FastAPI()

#Model tabel dummy SPI
class DataSPI(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tanggal: str
    lokasi: str
    nilai_spi: float

#Auto create DB pas server nyala
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoint POST -> tambah data
@app.post("/spi/")
def tambah_data_spi(data: DataSPI):
    with Session(engine) as session:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    
# Endpoint GET -> ambil semua data
@app.get("/spi/")
def ambil_data_spi():
    with Session(engine) as session:
        statement = select(DataSPI)
        hasil = session.exec(statement).all()
        return hasil
    
    