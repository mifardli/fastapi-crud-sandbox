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
    

# Endpoint GET -> FIlter data
@app.get("/spi/filter")
def filter_spi(
    lokasi: Optional[str] = None,
    tanggal: Optional[str] = None,
    min_spi: Optional[str] = None,
    max_spi: Optional[str] = None
):
    with Session(engine) as session:
        statement = select(DataSPI)
        
        if lokasi: 
            statement = statement.where(DataSPI.lokasi == lokasi)
        if tanggal:
            statement = statement.where(DataSPI.tanggal == tanggal)
        if min_spi is not None:
            statement = statement.where(DataSPI.nilai_spi >= min_spi)
        if max_spi is not None:
            statement = statement.where(DataSPI.nilai_spi <= max_spi)
        
        hasil = session.exec(statement).all()
        return hasil