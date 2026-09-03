from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.routes import auth, contracts, analysis, chat, compare, deadlines, reports
import os

# Ensure directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("database", exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ContractGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contracts.router)
app.include_router(analysis.router)
app.include_router(chat.router)
app.include_router(compare.router)
app.include_router(deadlines.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Welcome to ContractGuard API"}
