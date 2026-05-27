"""
Employee Pydantic model — represents a single employee record
after the ETL pipeline has run.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.enums import SalaryBand, TenureBand


class Employee(BaseModel):
    """A single employee record."""

    func: str = Field(..., description="Employee name / identifier")
    expectativa: bool = Field(..., description="Positive 5-year outlook (True = sim)")
    tempo_empresa: str = Field(..., description="Raw tenure string from the dataset")
    cargo: str = Field(..., description="Normalized job role / title")
    salario: float = Field(..., description="Monthly salary (BRL, raw float)")
    tenure_years: float = Field(..., description="Tenure in fractional years")

    # Derived classification fields (assigned post-construction)
    salary_band: SalaryBand | None = Field(default=None, description="Salary band classification")
    tenure_band: TenureBand | None = Field(default=None, description="Tenure band classification")

    model_config = {"from_attributes": True}
