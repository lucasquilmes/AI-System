# Métricas lingüísticas de superficie que no requieren referencia:
#
# LMO  – Longitud Media de Oración: media de palabras por oración.
#         Menor valor indica oraciones más cortas → más legible.
#
# TTR  – Type-Token Ratio: palabras únicas / total palabras.
#         Rango 0-1; mayor → mayor riqueza léxica.
#
# Palabras complejas – proporción de palabras polisílabas (> 2 sílabas).
#         Rango 0-1; menor → vocabulario más sencillo.
import re
import textstat


def calcular_lmo(texto):
    """Calcula la Longitud Media de Oración (palabras por oración)."""
    sentences = re.split(r"[.!?]+", texto)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0.0
    return round(sum(len(s.split()) for s in sentences) / len(sentences), 2)


def calcular_ttr(texto):
    """Calcula el Type-Token Ratio (palabras únicas / total palabras)."""
    words = texto.lower().split()
    if not words:
        return 0.0
    return round(len(set(words)) / len(words), 4)


def calcular_complex_words_ratio(texto):
    """Calcula la proporción de palabras polisílabas (> 2 sílabas) sobre el total."""
    words = texto.split()
    if not words:
        return 0.0
    return round(textstat.polysyllabcount(texto) / len(words), 4)
