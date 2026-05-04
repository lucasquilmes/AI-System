# Índice Flesch Reading Ease: mide la legibilidad del texto.
# Rango 0-100; mayor = más fácil de leer.
# Referencia orientativa: < 30 universitario, 60-70 divulgativo, > 80 muy fácil.
import textstat


def calcular_flesch(texto):
    """Calcula el índice Flesch Reading Ease para un texto en español."""
    try:
        return round(textstat.flesch_reading_ease(texto), 2)
    except Exception as e:
        print(f"Error calculando Flesch: {e}")
        return None
