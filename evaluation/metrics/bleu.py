# BLEU (Bilingual Evaluation Understudy): mide la precisión de n-gramas
# del texto generado respecto a la referencia.
# Rango 0-1 (normalizado desde 0-100); mayor = mayor coincidencia n-grama.
import sacrebleu


def calcular_bleu(texto_generado, referencias):
    """Calcula BLEU score normalizado (0-1) entre texto generado y referencia."""
    try:
        result = sacrebleu.corpus_bleu([texto_generado], [[referencias]])
        return round(result.score / 100.0, 4)
    except Exception as e:
        print(f"Error calculando BLEU: {e}")
        return None
