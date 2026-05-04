# Determina si una fila cumple los requisitos mínimos para incluirse en el análisis.
# Solo filtra por las dos métricas core (SARI y Flesch del generado);
# el resto son informativas y no deben bloquear filas.


def should_add_result(sari_score, flesch_generado):
    """Devuelve True si la fila tiene métricas core válidas (no nulas y < 100)."""
    return (
        sari_score is not None
        and flesch_generado is not None
        and sari_score < 100
        and flesch_generado < 100
    )
