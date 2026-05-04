# Levenshtein Normalizada: distancia de edición entre original y generado,
# calculada a nivel de palabras para eficiencia en textos largos.
# Rango 0-1; 0 = textos idénticos, 1 = completamente distintos.


def _levenshtein_words(seq1, seq2):
    """Distancia de Levenshtein entre dos listas de tokens (DP en O(n·m))."""
    n, m = len(seq1), len(seq2)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, m + 1):
            temp = dp[j]
            dp[j] = prev if seq1[i - 1] == seq2[j - 1] else 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[m]


def calcular_levenshtein_normalizada(texto_original, texto_generado):
    """Calcula la distancia de Levenshtein normalizada a nivel de palabras (0-1)."""
    words1 = texto_original.lower().split()
    words2 = texto_generado.lower().split()
    max_len = max(len(words1), len(words2))
    if max_len == 0:
        return 0.0
    return round(_levenshtein_words(words1, words2) / max_len, 4)
