"""
Narrative insight generation — story cards, key findings, and recommendations.

ALL insights are derived from computed data, never hardcoded.
The module reads the dataframe, computes metrics, and generates
human-readable narrative strings.
"""

from __future__ import annotations

import pandas as pd

from app.analytics.metrics import (
    add_band_columns,
    classify_salary_band,
    compute_confidence_index,
    compute_salary_stats,
    compute_tenure_stats,
)
from app.analytics.segmentation import (
    compute_retention_risk,
    compute_silent_strength,
    expectation_by_role,
    role_summary_table,
)
from app.models.metrics import StoryCard


def generate_story_cards(df: pd.DataFrame) -> list[StoryCard]:
    """
    Generate narrative story cards from the data.

    Each card has a title, body, category, and optional metric/value.
    """
    df = add_band_columns(df)
    cards: list[StoryCard] = []

    total = len(df)
    confidence = compute_confidence_index(df)
    salary_stats = compute_salary_stats(df)
    tenure_stats = compute_tenure_stats(df)

    # ── Card 1: Overall Confidence ─────────────────────────────────────
    positive_count = int(df["expectativa"].sum())
    negative_count = total - positive_count
    tone = "otimista" if confidence >= 60 else "preocupante"
    cards.append(StoryCard(
        title="Índice de Confiança Geral",
        body=(
            f"De {total} colaboradores, {positive_count} ({confidence}%) "
            f"têm expectativa positiva para os próximos 5 anos. "
            f"O cenário é {tone} para a retenção de talentos."
        ),
        category="overview",
        metric="Confiança",
        value=f"{confidence}%",
    ))

    # ── Card 2: Salary Landscape ───────────────────────────────────────
    salary_gap = round(salary_stats.max - salary_stats.min, 2)
    cards.append(StoryCard(
        title="Panorama Salarial",
        body=(
            f"O salário médio é R$ {salary_stats.avg:,.2f}, com mediana de "
            f"R$ {salary_stats.median:,.2f}. A amplitude salarial é de "
            f"R$ {salary_gap:,.2f} (de R$ {salary_stats.min:,.2f} "
            f"a R$ {salary_stats.max:,.2f})."
        ),
        category="salary",
        metric="Salário Médio",
        value=f"R$ {salary_stats.avg:,.2f}",
    ))

    # ── Card 3: Tenure Overview ────────────────────────────────────────
    cards.append(StoryCard(
        title="Tempo de Casa",
        body=(
            f"A permanência média é de {tenure_stats.avg:.1f} anos "
            f"(mediana: {tenure_stats.median:.1f} anos). "
            f"O colaborador mais antigo tem {tenure_stats.max:.1f} anos "
            f"de casa, enquanto o mais recente tem {tenure_stats.min:.1f} anos."
        ),
        category="tenure",
        metric="Permanência Média",
        value=f"{tenure_stats.avg:.1f} anos",
    ))

    # ── Card 4: Top Confidence Roles ───────────────────────────────────
    role_exp = expectation_by_role(df)
    high_conf_roles = [r for r in role_exp if r.confidence_pct == 100.0 and r.total >= 2]
    if high_conf_roles:
        role_names = ", ".join(r.role for r in high_conf_roles[:3])
        cards.append(StoryCard(
            title="Cargos com Alta Confiança",
            body=(
                f"Os cargos {role_names} apresentam 100% de expectativa positiva "
                f"entre seus colaboradores. São âncoras de estabilidade."
            ),
            category="expectations",
            metric="Cargos 100%",
            value=str(len(high_conf_roles)),
        ))

    # ── Card 5: Retention Risk ─────────────────────────────────────────
    risks = compute_retention_risk(df)
    if risks:
        top_risk = risks[0]
        total_at_risk = sum(r.count for r in risks)
        cards.append(StoryCard(
            title="Alerta de Retenção",
            body=(
                f"{total_at_risk} colaboradores expressaram expectativa negativa. "
                f"O cargo com maior risco é \"{top_risk.role}\" "
                f"({top_risk.count} pessoas, salário médio R$ {top_risk.avg_salary:,.2f})."
            ),
            category="risk",
            metric="Em Risco",
            value=str(total_at_risk),
        ))

    # ── Card 6: Silent Strength ────────────────────────────────────────
    strengths = compute_silent_strength(df)
    if strengths:
        top_strength = strengths[0]
        cards.append(StoryCard(
            title="Força Silenciosa",
            body=(
                f"O cargo \"{top_strength.role}\" tem {top_strength.confidence_pct}% "
                f"de confiança com salário médio de R$ {top_strength.avg_salary:,.2f}, "
                f"abaixo da mediana geral. São equipes engajadas e potencialmente "
                f"subvalorizadas financeiramente."
            ),
            category="insight",
            metric="Confiança",
            value=f"{top_strength.confidence_pct}%",
        ))

    # ── Card 7: Salary band distribution ───────────────────────────────
    band_counts = df["salary_band"].value_counts()
    largest_band_enum = band_counts.index[0] if len(band_counts) > 0 else "N/A"
    largest_band_str = str(largest_band_enum).replace("SalaryBand.", "").title() if "SalaryBand." in str(largest_band_enum) else str(largest_band_enum)
    if hasattr(largest_band_enum, "value"):
        largest_band_str = largest_band_enum.value
    largest_count = int(band_counts.iloc[0]) if len(band_counts) > 0 else 0
    cards.append(StoryCard(
        title="Distribuição por Faixa Salarial",
        body=(
            f"A faixa salarial mais populosa é a \"{largest_band_str}\" "
            f"com {largest_count} colaboradores ({round(largest_count / total * 100, 1)}% do total). "
            f"Isso pode indicar concentração de cargos operacionais ou de início de carreira."
        ),
        category="salary",
        metric="Maior Faixa",
        value=largest_band_str,
    ))

    return cards


def generate_key_findings(df: pd.DataFrame) -> list[str]:
    """
    Generate a list of key findings as plain-text strings.

    Each finding is a single, data-backed statement.
    """
    df = add_band_columns(df)
    findings: list[str] = []

    total = len(df)
    confidence = compute_confidence_index(df)
    salary_stats = compute_salary_stats(df)
    tenure_stats = compute_tenure_stats(df)

    # Finding 1: Overall confidence
    findings.append(
        f"{confidence}% dos colaboradores têm expectativa positiva "
        f"para os próximos 5 anos."
    )

    # Finding 2: Salary range
    findings.append(
        f"A amplitude salarial vai de R$ {salary_stats.min:,.2f} "
        f"a R$ {salary_stats.max:,.2f}, uma variação de "
        f"{round(salary_stats.max / salary_stats.min, 1)}x."
    )

    # Finding 3: Tenure average
    findings.append(
        f"A permanência média é de {tenure_stats.avg:.1f} anos, "
        f"com mediana de {tenure_stats.median:.1f} anos."
    )

    # Finding 4: Number of unique roles
    n_roles = df["cargo"].nunique()
    findings.append(
        f"A empresa possui {n_roles} cargos distintos para {total} colaboradores."
    )

    # Finding 5: Expectations by salary level
    positive_salary_avg = df[df["expectativa"] == True]["salario"].mean()  # noqa: E712
    negative_salary_avg = df[df["expectativa"] == False]["salario"].mean()  # noqa: E712
    if positive_salary_avg > negative_salary_avg:
        findings.append(
            f"Colaboradores com expectativa positiva ganham em média "
            f"R$ {positive_salary_avg:,.2f}, vs R$ {negative_salary_avg:,.2f} dos negativos."
        )
    else:
        findings.append(
            f"Curiosamente, colaboradores com expectativa negativa ganham em média "
            f"R$ {negative_salary_avg:,.2f}, acima dos positivos (R$ {positive_salary_avg:,.2f})."
        )

    # Finding 6: Retention risk count
    risks = compute_retention_risk(df)
    total_at_risk = sum(r.count for r in risks)
    findings.append(
        f"{total_at_risk} colaboradores ({round(total_at_risk / total * 100, 1)}%) "
        f"expressaram expectativa negativa, distribuídos em {len(risks)} cargos."
    )

    return findings


def generate_recommendations(df: pd.DataFrame) -> list[str]:
    """
    Generate actionable recommendations based on the data.
    """
    df = add_band_columns(df)
    recommendations: list[str] = []

    confidence = compute_confidence_index(df)
    risks = compute_retention_risk(df)
    strengths = compute_silent_strength(df)
    salary_stats = compute_salary_stats(df)

    # Recommendation 1: General retention
    if confidence < 70:
        recommendations.append(
            "Implementar programa de escuta ativa para entender as causas da "
            "insatisfação, dado que o índice de confiança está abaixo de 70%."
        )
    else:
        recommendations.append(
            "O índice de confiança é saudável. Manter as práticas atuais e "
            "investir em programas de reconhecimento para sustentar o engajamento."
        )

    # Recommendation 2: Target high-risk roles
    if risks:
        top_risks = risks[:3]
        role_names = ", ".join(r.role for r in top_risks)
        recommendations.append(
            f"Priorizar ações de retenção nos cargos: {role_names}. "
            f"Considerar revisão salarial, plano de carreira e benefícios."
        )

    # Recommendation 3: Value silent strengths
    if strengths:
        strength_names = ", ".join(s.role for s in strengths[:3])
        recommendations.append(
            f"Revisar a remuneração dos cargos {strength_names}, que mostram alto "
            f"engajamento apesar de salários abaixo da mediana. Investir aqui "
            f"pode consolidar a lealdade desses times."
        )

    # Recommendation 4: Salary equity
    if salary_stats.std > salary_stats.avg * 0.5:
        recommendations.append(
            "A dispersão salarial é significativa. Considerar uma política de "
            "faixas salariais mais transparente para reduzir percepção de inequidade."
        )

    # Recommendation 5: Career development
    recommendations.append(
        "Criar trilhas de desenvolvimento de carreira visíveis para todos os cargos, "
        "com critérios claros de progressão. Isso é especialmente importante para "
        "colaboradores nas faixas Junior e Pleno."
    )

    # Recommendation 6: Data-driven follow-up
    recommendations.append(
        "Repetir esta pesquisa semestralmente para acompanhar a evolução do "
        "índice de confiança e validar o impacto das ações implementadas."
    )

    return recommendations
