# NER Density (Named Entity Recognition Density): proporción de entidades
# nombradas (personas, lugares, organizaciones, fechas…) sobre el total de tokens.
# Comparar original vs. generado revela si el modelo preserva las entidades clave.
# Requiere modelo spaCy español: python -m spacy download es_core_news_sm
import spacy

_NLP = None


def get_nlp():
    """Carga y cachea el pipeline spaCy para español."""
    global _NLP
    if _NLP is None:
        try:
            _NLP = spacy.load("es_core_news_sm")
        except OSError:
            raise RuntimeError(
                "Modelo spaCy no encontrado. Instálalo con:\n"
                "  python -m spacy download es_core_news_sm"
            )
    return _NLP


def calcular_ner_density(texto):
    """Calcula la densidad de entidades nombradas (entidades / tokens no-espacio)."""
    nlp = get_nlp()
    doc = nlp(texto)
    tokens = [t for t in doc if not t.is_space]
    if not tokens:
        return 0.0
    return round(len(doc.ents) / len(tokens), 4)
