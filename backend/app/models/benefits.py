"""
Pydantic schemas for the Benefits Benchmark Analytics API.
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class BenefitRecord(BaseModel):
    id_registro: str
    empresa: str
    ordem_empresa: int
    beneficio: str
    ordem_beneficio: int
    categoria_beneficio: str
    oferta_original: str
    status_oferta: str
    valor_monetario_br: float
    percentual_cobertura: float
    impacto_atracao: str
    is_mg: bool

    model_config = ConfigDict(from_attributes=True)

class CompanyBenefitScore(BaseModel):
    empresa: str
    score: float
    is_mg: bool
    total_benefits: int
    offered: int
    partial: int
    not_offered: int

class BenefitGap(BaseModel):
    beneficio: str
    categoria_beneficio: str
    impacto_atracao: str
    mg_status: str
    competitor_adoption_rate: float
    is_market_standard: bool
    recommendation: str

class BenefitCategorySummary(BaseModel):
    categoria_beneficio: str
    mg_score: float
    market_score: float

class BenefitsOverview(BaseModel):
    mg_score: float
    market_avg_score: float
    gap_count: int
    high_impact_opportunities: int
    benefits_offered: int
    benefits_not_offered: int

class BenefitsPresentationInsight(BaseModel):
    title: str
    body: str
    category: str
    metric: Optional[str] = None
    value: Optional[str] = None

class BenefitsRankingResponse(BaseModel):
    ranking: List[CompanyBenefitScore]

class BenefitsMatrixResponse(BaseModel):
    gaps: List[BenefitGap]
    categories: List[BenefitCategorySummary]

class BenefitsPresentationResponse(BaseModel):
    insights: List[BenefitsPresentationInsight]
    recommendations: List[str]
