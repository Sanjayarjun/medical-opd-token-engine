from fastapi import FastAPI
from app.api.routes import router as api_router


app = FastAPI(title="Medoc OPD Token Allocation Engine", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Medoc OPD Token Allocation Engine is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# API routes
app.include_router(api_router, prefix="/api/v1")

