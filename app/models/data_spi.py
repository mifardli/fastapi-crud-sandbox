from sqlmodel import SQLModel, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime

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