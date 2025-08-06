from fastapi import FastAPI
from app.routers import lingkungan_router
from app.database.db import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

# Include endpoint SPI
app.include_router(lingkungan_router.router)