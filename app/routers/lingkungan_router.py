from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.lingkungan import DataLingkungan
from app.database.db import get_session

router = APIRouter()

# GET all data
@router.get("/data")
def get_all_data(session: Session = Depends(get_session)):
    data = session.exec(select(DataLingkungan)).all()
    return data

# GET by lokasi koordinat
@router.get("/data/lokasi{by-koordinat}")
def get_by_koordinat(lon: float, lat: float, session: Session = Depends(get_session)):
    data = session.exec(
        select(DataLingkungan)
        .where(DataLingkungan.lon == lon)
        .where(DataLingkungan.lat == lat)
        ).all()
    return data

# GET by tanggal
@router.get("/data/by-date")
def get_by_date(date: str, session: Session = Depends(get_session)):
    data = session.exec(
        select(DataLingkungan)
        .where(DataLingkungan.date == date)
    ).all()
    return data

# POST data baru
@router.post("/data")
def create_data(data: DataLingkungan, session: Session = Depends(get_session)):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

# DELETE by id
@router.delete("/data/{id}")
def delete_data(id: int, session: Session = Depends(get_session)):
    data = session.get(DataLingkungan, id)
    if data:
        session.delete(data)
        session.commit()
        return {"message" : "Data deleted"}
    return {"error": " Data not found"}