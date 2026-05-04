# Rouge-L: mide la subsecuencia común más larga (LCS) entre texto generado
# y referencia. Captura orden y coherencia mejor que Rouge-1/2.
# Rango 0-1; mayor = mayor superposición léxica con la referencia.
import evaluate

_ROUGE = None


def get_rouge():
    """Carga y cachea la métrica Rouge del paquete evaluate."""
    global _ROUGE
    if _ROUGE is None:
        try:
            _ROUGE = evaluate.load("rouge")
        except Exception as e:
            raise RuntimeError(f"No se pudo cargar Rouge: {e}")
    return _ROUGE


def calcular_rouge_l(texto_generado, referencias):
    """Calcula Rouge-L (subsecuencia común más larga) entre generado y referencia."""
    rouge = get_rouge()
    result = rouge.compute(
        predictions=[texto_generado],
        references=[referencias],
    )
    return round(result["rougeL"], 4)
