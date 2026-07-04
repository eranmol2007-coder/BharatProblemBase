import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db
from app.routers.problems import router as problems_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")


def _ensure_data():
    try:
        from scripts.seed_db import ensure_seed_data
        inserted = ensure_seed_data(min_count=10)
        if inserted:
            logger.info(f"Auto-loaded {inserted} seed problems into database.")
    except Exception as e:
        logger.warning(f"Could not auto-seed database: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting BharatProblemBase...")
    init_db()
    logger.info("Database tables ready.")
    _ensure_data()
    yield
    logger.info("Shutting down BharatProblemBase...")


app = FastAPI(
    title="BharatProblemBase",
    description="One place for all hackathon & competition problem statements",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "BharatProblemBase"}


if os.path.isdir(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend not built. Run: cd frontend && npm run build"}
