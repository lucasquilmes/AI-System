# Compression Ratio: cociente palabras_generadas / palabras_originales.
# Cuantifica la capacidad de síntesis del modelo.
# < 1 → compresión (se redujo el texto); > 1 → expansión; = 1 → mismo volumen.


def calcular_compression_ratio(texto_original, texto_generado):
    """Calcula el ratio de compresión (palabras generadas / palabras originales)."""
    words_original = len(texto_original.split())
    words_generado = len(texto_generado.split())
    if words_original == 0:
        return None
    return round(words_generado / words_original, 4)
