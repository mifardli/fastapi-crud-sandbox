from fastapi import APIRouter
from sqlmodel import Session, select
from typing import Optional
from app.models.data_spi import DataSPI, DataSPIInput
from app.database.connection import engine

router = APIRouter()

@router.post("/spi/")
def tambah_data_spi(data: DataSPIInput):
    with Session(engine) as session:
        data_model = DataSPI(**data.model_dump())
        session.add(data_model)
        session.commit()
        session.refresh(data_model)
        return data_model
    

@router.get("/spi/")
def ambil_data_spi():
    with Session(engine) as session:
        statement = select(DataSPI)
        hasil = session.exec(statement).all()
        return hasil
    
@router.get("/spi/filter")
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
        return hasil if hasil else {"message" : "Tidak ada data yang cocok"}