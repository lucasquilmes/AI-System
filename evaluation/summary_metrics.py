# Construye estadísticas descriptivas (media, mín, máx, desv. estándar) para todas
# las métricas numéricas del DataFrame de resultados, agrupadas por modelo.
# Se adapta automáticamente a las columnas presentes (incluidas las opcionales).
import pandas as pd

# Columnas que no son métricas y se excluyen de la agregación
_NON_METRIC_COLS = {"modelo", "row_index", "texto_original", "texto_generado", "referencias"}


def build_summary_stats(results_df: pd.DataFrame) -> pd.DataFrame:
    """Agrega todas las métricas numéricas por modelo con media, mín, máx y desv. estándar."""
    if results_df.empty:
        return pd.DataFrame(columns=["modelo", "count"])

    metric_cols = [
        col for col in results_df.columns
        if col not in _NON_METRIC_COLS
        and pd.api.types.is_numeric_dtype(results_df[col])
    ]

    rows = []
    for modelo, group in results_df.groupby("modelo"):
        row = {"modelo": modelo, "count": len(group)}
        for col in metric_cols:
            series = group[col].dropna()
            if series.empty:
                row[f"{col}_promedio"] = None
                row[f"{col}_min"] = None
                row[f"{col}_max"] = None
                row[f"{col}_std"] = None
            else:
                row[f"{col}_promedio"] = round(float(series.mean()), 4)
                row[f"{col}_min"] = round(float(series.min()), 4)
                row[f"{col}_max"] = round(float(series.max()), 4)
                row[f"{col}_std"] = round(float(series.std()), 4) if len(series) > 1 else 0.0
        rows.append(row)

    return pd.DataFrame(rows)
