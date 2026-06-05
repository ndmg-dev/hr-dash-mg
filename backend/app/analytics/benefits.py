"""
Analytics functions for Benefits Benchmark.
"""

import pandas as pd
from typing import List, Dict, Any
from app.models.benefits import (
    CompanyBenefitScore,
    BenefitGap,
    BenefitCategorySummary,
    BenefitsOverview,
    BenefitsPresentationInsight
)

def _get_score(status: str) -> float:
    if status == "Oferece":
        return 1.0
    if status == "Parcial/Subsidiado":
        return 0.5
    return 0.0

def compute_company_scores(df: pd.DataFrame) -> List[CompanyBenefitScore]:
    """Calculate the benefits coverage score for each company."""
    # Add score column
    df_scored = df.copy()
    df_scored["score_val"] = df_scored["status_oferta"].apply(_get_score)
    
    results = []
    for empresa, group in df_scored.groupby("empresa"):
        total_benefits = len(group)
        # Exclude "Não informado" from denominator? Let's just use total
        # Or better, exclude "Não informado" for a fairer comparison:
        valid_group = group[group["status_oferta"] != "Não informado"]
        valid_total = len(valid_group)
        
        score_sum = valid_group["score_val"].sum()
        score = (score_sum / valid_total) * 100 if valid_total > 0 else 0.0
        
        is_mg = group["is_mg"].iloc[0] if "is_mg" in group.columns else False
        
        offered = len(valid_group[valid_group["status_oferta"] == "Oferece"])
        partial = len(valid_group[valid_group["status_oferta"] == "Parcial/Subsidiado"])
        not_offered = len(valid_group[valid_group["status_oferta"] == "Não oferece"])
        
        results.append(CompanyBenefitScore(
            empresa=str(empresa),
            score=round(score, 1),
            is_mg=bool(is_mg),
            total_benefits=int(valid_total),
            offered=int(offered),
            partial=int(partial),
            not_offered=int(not_offered)
        ))
        
    return sorted(results, key=lambda x: x.score, reverse=True)

def compute_overview(df: pd.DataFrame) -> BenefitsOverview:
    scores = compute_company_scores(df)
    
    mg_score_obj = next((s for s in scores if s.is_mg), None)
    mg_score = mg_score_obj.score if mg_score_obj else 0.0
    
    competitors = [s for s in scores if not s.is_mg]
    market_avg = sum(s.score for s in competitors) / len(competitors) if competitors else 0.0
    
    gaps = compute_gaps(df)
    gap_count = sum(1 for g in gaps if g.mg_status in ["Não oferece", "Parcial/Subsidiado"] and g.competitor_adoption_rate >= 50.0)
    high_impact = sum(1 for g in gaps if g.impacto_atracao == "Alto" and g.mg_status == "Não oferece")
    
    return BenefitsOverview(
        mg_score=mg_score,
        market_avg_score=round(market_avg, 1),
        gap_count=gap_count,
        high_impact_opportunities=high_impact,
        benefits_offered=mg_score_obj.offered if mg_score_obj else 0,
        benefits_not_offered=mg_score_obj.not_offered if mg_score_obj else 0
    )

def compute_gaps(df: pd.DataFrame) -> List[BenefitGap]:
    df_scored = df.copy()
    df_scored["score_val"] = df_scored["status_oferta"].apply(_get_score)
    
    mg_data = df_scored[df_scored["is_mg"] == True]
    comp_data = df_scored[df_scored["is_mg"] == False]
    
    gaps = []
    for beneficio, group in df_scored.groupby("beneficio"):
        cat = group["categoria_beneficio"].iloc[0]
        impacto = group["impacto_atracao"].iloc[0]
        ordem = group["ordem_beneficio"].iloc[0]
        
        mg_row = mg_data[mg_data["beneficio"] == beneficio]
        mg_status = mg_row["status_oferta"].iloc[0] if not mg_row.empty else "Não informado"
        mg_score = _get_score(mg_status)
        
        comp_rows = comp_data[comp_data["beneficio"] == beneficio]
        comp_valid = comp_rows[comp_rows["status_oferta"] != "Não informado"]
        
        # Competitor adoption: % of competitors that offer or partially offer it
        adoption_count = len(comp_valid[comp_valid["score_val"] > 0])
        adoption_rate = (adoption_count / len(comp_valid)) * 100 if len(comp_valid) > 0 else 0.0
        
        is_market_standard = adoption_rate >= 60.0
        
        if mg_score < 1.0 and is_market_standard:
            rec = "Prioridade: Gap em relação ao padrão de mercado" if impacto == "Alto" else "Avaliar melhoria: Gap competitivo"
        elif mg_score == 0 and impacto == "Alto":
            rec = "Atenção: Benefício de alto impacto ausente"
        elif mg_score >= 1.0 and adoption_rate < 50.0:
            rec = "Diferencial Competitivo"
        else:
            rec = "Alinhado com o mercado"
            
        gaps.append((ordem, BenefitGap(
            beneficio=str(beneficio),
            categoria_beneficio=str(cat),
            impacto_atracao=str(impacto),
            mg_status=str(mg_status),
            competitor_adoption_rate=round(adoption_rate, 1),
            is_market_standard=bool(is_market_standard),
            recommendation=rec
        )))
        
    gaps.sort(key=lambda x: x[0])
    return [g[1] for g in gaps]

def compute_categories(df: pd.DataFrame) -> List[BenefitCategorySummary]:
    df_scored = df.copy()
    df_scored["score_val"] = df_scored["status_oferta"].apply(_get_score)
    
    results = []
    for cat, group in df_scored.groupby("categoria_beneficio"):
        mg_group = group[(group["is_mg"] == True) & (group["status_oferta"] != "Não informado")]
        comp_group = group[(group["is_mg"] == False) & (group["status_oferta"] != "Não informado")]
        
        mg_score = (mg_group["score_val"].mean() * 100) if not mg_group.empty else 0.0
        market_score = (comp_group["score_val"].mean() * 100) if not comp_group.empty else 0.0
        
        results.append(BenefitCategorySummary(
            categoria_beneficio=str(cat),
            mg_score=round(mg_score, 1),
            market_score=round(market_score, 1)
        ))
    return results

def generate_insights(df: pd.DataFrame) -> tuple[List[BenefitsPresentationInsight], List[str]]:
    overview = compute_overview(df)
    gaps = compute_gaps(df)
    
    insights = []
    recommendations = []
    
    # 1. Competitive Position
    position_title = "Posicionamento de Benefícios"
    if overview.mg_score >= overview.market_avg_score + 10:
        body = "Mendonça Galvão possui uma política de benefícios superior à média dos concorrentes diretos."
        cat = "positive"
    elif overview.mg_score >= overview.market_avg_score - 10:
        body = "O pacote de benefícios da Mendonça Galvão está alinhado com a média do mercado."
        cat = "neutral"
    else:
        body = "Mendonça Galvão apresenta defasagem competitiva em seu pacote de benefícios em relação à média do mercado."
        cat = "negative"
        
    insights.append(BenefitsPresentationInsight(
        title=position_title,
        body=body,
        category=cat,
        metric="Score Competitivo",
        value=f"{overview.mg_score:.1f}%"
    ))
    
    # 2. Critical Gaps
    high_impact_gaps = [g for g in gaps if g.impacto_atracao == "Alto" and g.mg_status == "Não oferece"]
    if high_impact_gaps:
        names = ", ".join([g.beneficio for g in high_impact_gaps[:2]])
        insights.append(BenefitsPresentationInsight(
            title="Gaps Críticos",
            body=f"Benefícios de alto impacto para atração não são oferecidos atualmente (ex: {names}).",
            category="negative",
            metric="Gaps de Alto Impacto",
            value=str(len(high_impact_gaps))
        ))
        recommendations.append(f"Priorizar a estruturação dos benefícios de alto impacto: {names}.")
    
    # Recommendations
    if overview.mg_score < overview.market_avg_score:
        recommendations.append("Revisar pacote de benefícios com foco em itens padrão de mercado para fechar o gap competitivo.")
    
    market_std_gaps = [g for g in gaps if g.is_market_standard and g.mg_status != "Oferece"]
    if market_std_gaps:
        recommendations.append("Avaliar subsídio parcial para benefícios padrão de mercado que hoje não têm cobertura total.")
        
    return insights, recommendations
