from sqlmodel import SQLModel, Field
from typing import Optional

class DataLingkungan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str  
    lon: float
    lat: float
    LST: float
    NDVI: float
    CHIRPS: float
    SPI_1: float
    SPI_3: Optional[float]  
