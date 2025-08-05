from fastapi import FastAPI
from app.routers.spi import router as spi_router
from app.database.connection import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

# Include endpoint SPI
app.include_router(spi_router)