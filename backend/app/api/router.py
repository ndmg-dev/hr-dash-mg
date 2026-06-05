"""
Main API router — aggregates all endpoint routers under /api prefix.
"""

from fastapi import APIRouter

from app.api.endpoints import (
    confidential,
    expectations,
    overview,
    presentation,
    roles,
    salary,
    tenure,
    benefits,
)

router = APIRouter(prefix="/api")

router.include_router(confidential.router)
router.include_router(overview.router)
router.include_router(expectations.router)
router.include_router(salary.router)
router.include_router(tenure.router)
router.include_router(roles.router)
router.include_router(presentation.router)
router.include_router(benefits.router)
