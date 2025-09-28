from fastapi import FastAPI

from .config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": f"{settings.api_name} is running.",
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
