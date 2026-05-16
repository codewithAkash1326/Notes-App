from fastapi import FastAPI
from src.user.router import api_router
from src.utils.db import Base , engine

# This will now create both User and Note tables since they are in the same module
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)