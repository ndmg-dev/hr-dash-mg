"""
Enumerations for salary bands and tenure bands.

These enums are used both for classification logic and as labels
in API responses.
"""

from enum import Enum


class SalaryBand(str, Enum):
    """Salary classification bands (BRL)."""
    JUNIOR = "Junior"               # R$ 0 – R$ 1,621.00
    PLENO = "Pleno"                 # R$ 1,621.01 – R$ 2,593.72
    SENIOR = "Senior"               # R$ 2,593.73 – R$ 4,052.50
    ESPECIALISTA = "Especialista"   # R$ 4,052.51+


class TenureBand(str, Enum):
    """Tenure classification bands (years)."""
    NEWCOMER = "Novato (< 1 ano)"
    GROWING = "Em Crescimento (1-3 anos)"
    ESTABLISHED = "Estabelecido (3-5 anos)"
    VETERAN = "Veterano (5-10 anos)"
    LEGACY = "Longo Prazo (> 10 anos)"
