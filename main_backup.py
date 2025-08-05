from fastapi import FastAPI
from pydantic import field_validator
from datetime import datetime
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

class DataSPIInput(SQLModel):
    tanggal: str
    lokasi: str
    nilai_spi: float

    @field_validator("tanggal")
    def cek_format_tanggal(cls, value):
        try:
            datetime.strptime(value, "%Y-%m")
        except ValueError:
            raise ValueError("Format tanggal harus YYYY-MM (contoh: 2023-06)")
        return value

    @field_validator("nilai_spi")
    def cek_range_spi(cls, value):
        if not -2.0 <= value <= 2.0:
            raise ValueError("Nilai SPI harus antara -2.0 dan 2.0")
        return value

    @field_validator("lokasi")
    def cek_lokasi(cls, value):
        if not value.strip():
            raise ValueError("Lokasi tidak boleh kosong")
        return value
    
#Auto create DB pas server nyala
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoint POST -> tambah data
@app.post("/spi/")
def tambah_data_spi(data: DataSPIInput):
    with Session(engine) as session:
        #konversi ke mode database
        data_model = DataSPI(**data.model_dump())
        session.add(data_model)
        session.commit()
        session.refresh(data_model)
        return data_model
    
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
    min_spi: Optional[float] = None,
    max_spi: Optional[float] = None
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