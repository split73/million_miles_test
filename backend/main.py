from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

app = FastAPI(title="Encar Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://million-miles-test-two.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "service": "encar-backend",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
        "listings": "/api/v1/listings?page=1&per_page=20",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
