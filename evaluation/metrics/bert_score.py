# BertScore: evalúa la similitud semántica entre texto generado y referencia
# usando embeddings contextuales de un modelo BERT multilingüe.
# Se reporta el F1. Rango 0-1; mayor = mayor similitud semántica.
# Nota: descarga ~700 MB de modelo en el primer uso; se cachea automáticamente.
import evaluate

_BERTSCORE = None


def get_bertscore():
    """Carga y cachea la métrica BertScore del paquete evaluate."""
    global _BERTSCORE
    if _BERTSCORE is None:
        try:
            _BERTSCORE = evaluate.load("bertscore")
        except Exception as e:
            raise RuntimeError(f"No se pudo cargar BertScore: {e}")
    return _BERTSCORE


def calcular_bert_score(texto_generado, referencias):
    """Calcula BertScore F1 entre texto generado y referencia en español."""
    bertscore = get_bertscore()
    result = bertscore.compute(
        predictions=[texto_generado],
        references=[referencias],
        lang="es",
    )
    return round(result["f1"][0], 4)
