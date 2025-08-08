from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.models.lingkungan import DataLingkungan
from fastapi.responses import JSONResponse
import pandas as pd
import math


router = APIRouter()

def clean_data(obj):
    if isinstance(obj, dict):
        return {k: clean_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_data(v) for v in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj

#fungsi helper klasifikasi
def classify_spi(value):
    if pd.isna(value) or math.isinf(value):
        return None
    if value >= 2.0:
        return "Extremely Wet"
    elif value >= 1.5:
        return "Very Wet"
    elif value >= 1.0:
        return "Moderately Wet"
    elif value >= -1.0:
        return "Near Normal"
    elif value >= -1.5:
        return "Moderately Dry"
    elif value >= -2.0:
        return "Severely Dry"
    else:
        return "Extremely Dry"
    
@router.get("/spi/classification")
def classify_spi_data(page: int = 1, limit: int = 1000, session: Session = Depends(get_session)):
    offset = (page - 1) * limit
    data = session.query(DataLingkungan).offset(offset).limit(limit).all()
    df = pd.DataFrame([d.__dict__ for d in data])
    df = df.drop(columns=["id", "_sa_instance_state"])
    df["SPI_1 Category"] = df["SPI_1"].apply(classify_spi)
    df["SPI_3 Category"] = df["SPI_3"].apply(classify_spi)
    result = clean_data(df.to_dict(orient="records"))
    return JSONResponse(content=result)

