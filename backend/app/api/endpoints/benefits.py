"""
API endpoints for Benefits Benchmark Analytics.
"""

from fastapi import APIRouter
from typing import List

from app.etl.benefits_pipeline import get_benefits_dataframe
from app.analytics import benefits as benefits_analytics
from app.models.benefits import (
    BenefitsOverview,
    BenefitsRankingResponse,
    BenefitsMatrixResponse,
    BenefitsPresentationResponse
)

router = APIRouter(prefix="/benefits", tags=["benefits"])

@router.get("/overview", response_model=BenefitsOverview)
def get_benefits_overview():
    """Get high-level benefits metrics."""
    df = get_benefits_dataframe()
    return benefits_analytics.compute_overview(df)

@router.get("/ranking", response_model=BenefitsRankingResponse)
def get_benefits_ranking():
    """Get benefits coverage scores for all companies."""
    df = get_benefits_dataframe()
    scores = benefits_analytics.compute_company_scores(df)
    return BenefitsRankingResponse(ranking=scores)

@router.get("/matrix", response_model=BenefitsMatrixResponse)
def get_benefits_matrix():
    """Get detailed gap matrix and category breakdown."""
    df = get_benefits_dataframe()
    gaps = benefits_analytics.compute_gaps(df)
    categories = benefits_analytics.compute_categories(df)
    return BenefitsMatrixResponse(gaps=gaps, categories=categories)

@router.get("/presentation-insights", response_model=BenefitsPresentationResponse)
def get_benefits_presentation_insights():
    """Get strategic insights for the presentation page."""
    df = get_benefits_dataframe()
    insights, recommendations = benefits_analytics.generate_insights(df)
    return BenefitsPresentationResponse(
        insights=insights,
        recommendations=recommendations
    )
