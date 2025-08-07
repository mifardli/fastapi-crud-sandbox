from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.lingkungan import DataLingkungan
from app.database.db import get_session
from fastapi.responses import JSONResponse
import math
import numpy as np
import pandas as pd

router = APIRouter()
# Helper untuk bersihin NaN / Inf dari JSON
def clean_dict(d):
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, float) and (math.isnan(d) or math.isinf(d)):
        return None
    else:
        return d

@router.get("/statistik")
def get_statistik(session: Session = Depends(get_session)):
    data = session.exec(select(DataLingkungan)).all()

    #Ekstrak data jadi list
    lst= [d.LST for d in data if d.LST is not None]
    ndvi = [d.NDVI for d in data if d.NDVI is not None]
    chirps = [d.CHIRPS for d in data if d.CHIRPS is not None]
    spi_1 = [d.SPI_1 for d in data if d.SPI_1 is not None]
    spi_3 = [d.SPI_3 for d in data if d.SPI_3 is not None]

    def get_stats(arr):
        return {
            "mean": float(np.mean(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "std": float(np.std(arr))
        }
    return {
        "LST": get_stats(lst),
        "NDVI": get_stats(ndvi),
        "CHIRPS": get_stats(chirps),
        "SPI_1": get_stats(spi_1),
        "SPI_3": get_stats(spi_3)
}

###### Statistik Bulanan #######
@router.get("/statistik/bulanan")
def statistik_bulanan(session: Session = Depends(get_session)):
    data = session.exec(select(DataLingkungan)).all()
    records = [d.dict() for d in data]
    df = pd.DataFrame(records)

    # Konversi kolom date ke datetime
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df = df.dropna(subset=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Hitung statistik per bulan
    grouped = df.groupby("month")[["LST", "NDVI", "CHIRPS", "SPI_1", "SPI_3"]].agg(["mean", "min", "max", "std"])
    grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
    grouped = grouped.reset_index()
    grouped = grouped.round(3)

    # Format JSON per bulan
    result = {}
    for _, row in grouped.iterrows():
        bulan = row["month"]
        result[bulan] = {
            "LST": {
                "mean": row["LST_mean"],
                "min": row["LST_min"],
                "max": row["LST_max"],
                "std": row["LST_std"],
            },
            "NDVI": {
                "mean": row["NDVI_mean"],
                "min": row["NDVI_min"],
                "max": row["NDVI_max"],
                "std": row["NDVI_std"],
            },
            "CHIRPS": {
                "mean": row["CHIRPS_mean"],
                "min": row["CHIRPS_min"],
                "max": row["CHIRPS_max"],
                "std": row["CHIRPS_std"],
            },
            "SPI_1": {
                "mean": row["SPI_1_mean"],
                "min": row["SPI_1_min"],
                "max": row["SPI_1_max"],
                "std": row["SPI_1_std"],
            },
            "SPI_3": {
                "mean": row["SPI_3_mean"],
                "min": row["SPI_3_min"],
                "max": row["SPI_3_max"],
                "std": row["SPI_3_std"],
            },
        }
    
    return JSONResponse(content=clean_dict(result))




####### Statistik Tahunan ########
@router.get("/statistik/tahunan")
def statistik_tahunan(session: Session = Depends(get_session)):
    data = session.exec(select(DataLingkungan)).all()
    records = [d.dict() for d in data]
    df = pd.DataFrame(records)

    # Konversi dan bersihkan tanggal
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year

    # Groupby per tahun, hitung agregat
    grouped = df.groupby("year")[["LST", "NDVI", "CHIRPS", "SPI_1", "SPI_3"]].agg(["mean", "min", "max", "std"])
    grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]  # flatten
    grouped = grouped.reset_index()
    grouped = grouped.round(3)

    # Format ke JSON
    result = {}
    for _, row in grouped.iterrows():
        year = str(int(row["year"]))
        result[year] = {
            "LST": {
                "mean": row["LST_mean"],
                "min": row["LST_min"],
                "max": row["LST_max"],
                "std": row["LST_std"],
            },
            "NDVI": {
                "mean": row["NDVI_mean"],
                "min": row["NDVI_min"],
                "max": row["NDVI_max"],
                "std": row["NDVI_std"],
            },
            "CHIRPS": {
                "mean": row["CHIRPS_mean"],
                "min": row["CHIRPS_min"],
                "max": row["CHIRPS_max"],
                "std": row["CHIRPS_std"],
            },
            "SPI_1": {
                "mean": row["SPI_1_mean"],
                "min": row["SPI_1_min"],
                "max": row["SPI_1_max"],
                "std": row["SPI_1_std"],
            },
            "SPI_3": {
                "mean": row["SPI_3_mean"],
                "min": row["SPI_3_min"],
                "max": row["SPI_3_max"],
                "std": row["SPI_3_std"],
            },
        }

    return JSONResponse(content=clean_dict(result))
