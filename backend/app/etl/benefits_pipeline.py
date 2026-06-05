"""
ETL pipeline for Benefits Benchmark Analytics.

Reads the new benefits spreadsheet, cleans strings, converts numeric values,
and provides a cached dataframe for the benefits API endpoints.
"""

import functools
import logging
import re
import pandas as pd

from app.config import settings

logger = logging.getLogger(__name__)

def clean_money(val) -> float:
    if pd.isna(val) or val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    # Convert string to float by stripping non-numeric chars except comma/dot
    val_str = str(val)
    # Extract digits and dots/commas
    match = re.search(r"([\d.,]+)", val_str)
    if match:
        num_str = match.group(1).replace(".", "").replace(",", ".")
        try:
            return float(num_str)
        except ValueError:
            return 0.0
    return 0.0

def clean_percentage(val) -> float:
    if pd.isna(val) or val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("%", "").strip()
    try:
        return float(val_str.replace(",", ".")) / 100.0 if float(val_str) > 1.0 else float(val_str)
    except ValueError:
        return 0.0

def normalize_status(val) -> str:
    if pd.isna(val) or val is None:
        return "Não informado"
    val_str = str(val).strip()
    
    # Handle encoding issues where "Não" might be "No"
    if "oferece" in val_str.lower():
        if "n" in val_str.lower() and "o" in val_str.lower() and "oferece" in val_str.lower():
            return "Não oferece"
        return "Oferece"
    
    if "parcial" in val_str.lower() or "subsidiado" in val_str.lower():
        return "Parcial/Subsidiado"
    
    if "informado" in val_str.lower():
        return "Não informado"
        
    return val_str

@functools.lru_cache(maxsize=1)
def run_benefits_pipeline() -> pd.DataFrame:
    """
    Execute the ETL pipeline for benefits data.
    """
    logger.info("Starting benefits ETL pipeline...")
    
    path = settings.benefits_dataset_path
    if not path.exists():
        raise FileNotFoundError(f"Benefits dataset not found at {path}")

    # Read dataset
    df = pd.read_excel(path, engine="openpyxl")
    
    # Clean column names (strip whitespace and lowercase)
    df.columns = [str(c).strip() for c in df.columns]
    
    # We might have trailing spaces in column names or encoding issues, so let's do a safe rename
    df = df.rename(columns={
        "Empresa": "empresa",
        "Ordem_Empresa": "ordem_empresa",
        "Beneficio": "beneficio",
        "Ordem_Beneficio": "ordem_beneficio",
        "Categoria_Beneficio": "categoria_beneficio",
        "Oferta_Original": "oferta_original",
        "Status_Oferta": "status_oferta",
        "Valor_Monetario_BR": "valor_monetario_br",
        "Percentual_Cobertura": "percentual_cobertura",
        "Flag_Mendonca_Galvao": "flag_mendonca_galvao",
        "Impacto_Atracao": "impacto_atracao",
        "Analise_Mendonca_Galvao": "analise_mendonca_galvao",
        "Analise_Concorrentes": "analise_concorrentes",
        "Fornecedor_Plano": "fornecedor_plano",
        "Clientes_Descricao": "clientes_descricao",
        "Clientes_Estimados": "clientes_estimados",
        "Funcionarios": "funcionarios"
    })
    
    # Strip strings
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        # Clean encoding artifacts for 'No' -> 'Não'
        df[col] = df[col].apply(lambda x: x.replace("No", "Não") if isinstance(x, str) else x)
        df[col] = df[col].apply(lambda x: x.replace("Mendona Galvo", "Mendonça Galvão") if isinstance(x, str) else x)

    # Normalize values
    if "status_oferta" in df.columns:
        df["status_oferta"] = df["status_oferta"].apply(normalize_status)
        
    if "valor_monetario_br" in df.columns:
        df["valor_monetario_br"] = df["valor_monetario_br"].apply(clean_money)
        
    if "percentual_cobertura" in df.columns:
        df["percentual_cobertura"] = df["percentual_cobertura"].apply(clean_percentage)
        
    if "flag_mendonca_galvao" in df.columns:
        df["is_mg"] = df["flag_mendonca_galvao"].apply(lambda x: "Sim" in str(x))

    logger.info("Benefits ETL pipeline finished. Loaded %d rows.", len(df))
    return df

def get_benefits_dataframe() -> pd.DataFrame:
    """Public accessor for the cached dataframe."""
    return run_benefits_pipeline().copy()
