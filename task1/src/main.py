"""Automatic Email Reply System - FastAPI Entry Point

This module is the entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from .config import get_settings
from .api import auth, emails, replies, knowledge, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    # Startup
    settings = get_settings()
    print(f"🚀 Automatic Email Reply System v1.0.0 starting...")
    print(f"📝 Environment: {settings.app_env}")

    yield

    # Shutdown
    print("👋 Application shutting down")


# Create the FastAPI application
app = FastAPI(
    title="Automatic Email Reply System",
    description="An intelligent system to help professors efficiently process student emails",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(emails.router)
app.include_router(replies.router)
app.include_router(knowledge.router)
app.include_router(stats.router)

# UI directory path
ui_path = Path(__file__).parent.parent / "ui"


# HTML page routes
@app.get("/ui/login.html")
async def login_page():
    """Login page."""
    login_file = ui_path / "login.html"
    if login_file.exists():
        return FileResponse(str(login_file), media_type="text/html")
    return {"error": "Login page not found"}


@app.get("/ui/index.html")
async def index_page():
    """Main dashboard page."""
    index_file = ui_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file), media_type="text/html")
    return {"error": "Index page not found"}


@app.get("/ui/")
async def ui_root():
    """UI root - redirects to login page."""
    return FileResponse(str(ui_path / "login.html"), media_type="text/html")


# Root path - redirect to login page
@app.get("/")
async def root():
    """Root path - redirect to login page."""
    return RedirectResponse(url="/ui/login.html")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Mount static files (CSS, JS) - must be placed after all routes,
# otherwise mount will shadow route definitions
css_path = ui_path / "css"
js_path = ui_path / "js"

if css_path.exists():
    app.mount("/css", StaticFiles(directory=str(css_path)), name="css")
if js_path.exists():
    app.mount("/js", StaticFiles(directory=str(js_path)), name="js")


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
    )
