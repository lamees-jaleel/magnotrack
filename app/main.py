import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.database import init_db
from app.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("magnotrack")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager: initialize database tables upon startup."""
    logger.info("Initializing MagnoTrack backend...")
    try:
        init_db()
        logger.info("MagnoTrack database ready.")
    except Exception as exc:
        logger.warning(
            f"Database initialization warning (will retry on first query): {exc}"
        )
    yield
    logger.info("MagnoTrack backend shutting down.")


app = FastAPI(
    title="MagnoTrack API",
    description="IoT-Based Magnetic Event Logging and Activity Monitoring System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
raw_cors = os.getenv("CORS_ORIGINS", "*")
origins = [origin.strip() for origin in raw_cors.split(",")] if raw_cors != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API routes
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse, summary="Serve MagnoTrack IoT Dashboard")
async def serve_dashboard(request: Request):
    """Serves the main single-page monitoring dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"project_name": "MagnoTrack"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
