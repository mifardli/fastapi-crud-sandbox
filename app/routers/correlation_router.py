from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.models.lingkungan import DataLingkungan
import pandas as pd
from fastapi.responses import JSONResponse
import math

router = APIRouter()

def clean_dict(d):
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, float) and (math.isnan(d) or math.isinf(d)):
        return None
    else:
        return d
    
@router.get("/correlation")
def correlation_all(session: Session = Depends(get_session)):
    data = session.query(DataLingkungan).all()
    df = pd.DataFrame([d.__dict__ for d in data])
    df = df.drop(columns=["id", "_sa_instance_state"])

    # Hitung korelasi antar variabel
    corr_spi1 = df[["SPI_1", "NDVI", "LST", "CHIRPS"]].corr().round(3).iloc[0].to_dict()
    corr_spi3 = df[["SPI_3", "NDVI", "LST", "CHIRPS"]].corr().round(3).iloc[0].to_dict()

    result = {
        "SPI_1": corr_spi1,
        "SPI_3": corr_spi3,
    }

    return JSONResponse(content=clean_dict(result))


@router.get("/correlation/monthly")
def correlation_by_month(session: Session = Depends(get_session)):
    data = session.query(DataLingkungan).all()
    df = pd.DataFrame([d.__dict__ for d in data])
    df = df.drop(columns=["id", "_sa_instance_state"])

    #Convert date to datetime & ambil bulan
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month.astype(str).str.zfill(2)

    results = {}

    for month in sorted(df['month'].unique()):
        df_month = df[df['month'] == month]

        #Korelasi SPI_1
        corr_spi1 = df_month[["SPI_1", "NDVI", "LST", "CHIRPS"]].corr().round(3)
        spi1_corr = corr_spi1.loc["SPI_1"].drop("SPI_1").to_dict()

        #Korelasi SPI_3
        corr_spi3 = df_month[["SPI_3", "NDVI", "LST", "CHIRPS"]].corr().round(3)
        spi3_corr = corr_spi3.loc["SPI_3"].drop("SPI_3").to_dict()

        results[month] = {
            "SPI_1": spi1_corr,
            "SPI_3": spi3_corr,
        }
    return JSONResponse(content=clean_dict(results))