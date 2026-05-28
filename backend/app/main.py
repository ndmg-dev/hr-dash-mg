"""
FastAPI application entry point.

Configures CORS, includes the API router, and provides a health-check
endpoint at the root.
"""

import logging

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import router
from app.config import settings

# ── Logging setup ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
)

# ── App creation ───────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
)

# ── CORS middleware ────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include API router ────────────────────────────────────────────────
app.include_router(router)


# ── Health check ───────────────────────────────────────────────────────
@app.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Health-check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_title,
        "version": settings.app_version,
    }


# ── Static Files ───────────────────────────────────────────────────────
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    logging.info("Static directory not found. Assuming local development mode.")

