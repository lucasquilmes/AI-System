# Métrica SARI (System for Automatic Rate of Intelligibility):
# compara original, predicción y referencia para medir la calidad
# de la simplificación. Rango 0-100; mayor = mejor simplificación.
import evaluate

_SARI_METRIC = None


def get_sari_metric():
    """Carga y cachea la métrica SARI del paquete evaluate."""
    global _SARI_METRIC
    if _SARI_METRIC is None:
        try:
            _SARI_METRIC = evaluate.load("sari", download_mode="reuse_cache_if_exists")
        except Exception as e:
            raise RuntimeError(f"No se pudo cargar la métrica SARI: {e}")
    return _SARI_METRIC


def calcular_sari(texto_original, texto_generado, referencias):
    """Calcula SARI comparando texto original, generado y referencia."""
    sari = get_sari_metric()
    results = sari.compute(
        sources=[texto_original],
        predictions=[texto_generado],
        references=[[referencias]],
    )
    return results.get("sari")
