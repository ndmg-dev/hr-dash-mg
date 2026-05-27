"""
Confidential endpoint — GET /api/confidential/employees

Returns individual employee records including names, protected by a password.
"""

from fastapi import APIRouter, Depends, Header, HTTPException

from app.config import settings
from app.etl.pipeline import get_dataframe
from app.models.metrics import ConfidentialEmployeeResponse

router = APIRouter(tags=["confidential"])


def verify_confidential_password(x_confidential_auth: str = Header(None)):
    """Dependency to check the password in the header."""
    if not x_confidential_auth or x_confidential_auth != settings.confidential_password:
        raise HTTPException(
            status_code=401,
            detail="Acesso negado: Senha confidencial inválida ou ausente.",
        )
    return True


@router.get("/confidential/employees", response_model=list[ConfidentialEmployeeResponse])
def get_confidential_employees(authorized: bool = Depends(verify_confidential_password)) -> list[ConfidentialEmployeeResponse]:
    """Return row-level employee data. Protected by password."""
    df = get_dataframe()
    
    results = []
    for _, row in df.iterrows():
        # Determine simple risk signal
        risk_signal = None
        if not bool(row["expectativa"]):
            risk_signal = "Risco de Retenção"
            
        results.append(ConfidentialEmployeeResponse(
            func=str(row["func"]),
            cargo=str(row["cargo"]),
            salario=round(float(row["salario"]), 2),
            tenure_years=round(float(row["tenure_years"]), 4),
            expectativa=bool(row["expectativa"]),
            risk_signal=risk_signal
        ))
        
    return results
