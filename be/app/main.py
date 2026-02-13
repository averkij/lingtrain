from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.database import Base, engine, SessionLocal
from app.seed import add_test_users
from app.routers import auth, users, documents, alignments, processing, marks, export


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        add_test_users(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Lingtrain API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(alignments.router)
app.include_router(processing.router)
app.include_router(marks.router)
app.include_router(export.router)

# Serve static files (visualization images)
static_path = Path(STATIC_DIR)
static_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
