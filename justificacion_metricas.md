# Justificación de las Métricas de Evaluación
## Proyecto: Simplificación Automática de Texto Administrativo a Lectura Fácil mediante LLMs

---

## Contexto del estudio

Este proyecto evalúa la capacidad de distintos modelos de lenguaje de gran escala (LLMs) para simplificar textos administrativos en español al estándar europeo de Lectura Fácil (UNE 153101:2018 / IFLA 2010), comparando sistemáticamente diez técnicas de prompting distintas. La evaluación automática es necesaria dada la escala del experimento (7 modelos × 10+ técnicas × 12 textos), y las métricas seleccionadas se han elegido para cubrir conjuntamente las dos dimensiones inseparables de la tarea: **fidelidad al contenido original** y **accesibilidad lingüística del texto generado**.

Ninguna de las dos dimensiones es suficiente por sí sola. Un texto que preserve todo el contenido pero sea incomprensible no cumple con Lectura Fácil. Un texto muy simple pero que pierda información esencial tampoco es válido. El conjunto de métricas descrito a continuación abarca ambas dimensiones de forma complementaria.

---

## Métricas seleccionadas y justificación

### 1. SARI — System for Automatic Rate of Intelligibility
**Librería:** Hugging Face `evaluate` (`evaluate.load("sari")`)
**Rango:** 0–100 (mayor es mejor)

SARI (Xu et al., 2016) es la métrica de referencia en la literatura de simplificación de texto. A diferencia de BLEU o ROUGE, SARI no evalúa únicamente la similitud con una referencia: calcula simultáneamente tres operaciones de edición sobre el texto — **adición** de palabras nuevas útiles, **conservación** de palabras del original que deben mantenerse, y **eliminación** de palabras innecesarias — y promedia las tres puntuaciones. Esta descomposición la hace especialmente adecuada para Lectura Fácil, donde la tarea no es parafrasear libremente sino realizar operaciones de simplificación controladas sobre el texto fuente.

SARI es la métrica primaria del estudio porque es la única diseñada específicamente para medir la calidad de la simplificación, no la similitud con una referencia.

---

### 2. ROUGE-L — Recall-Oriented Understudy for Gisting Evaluation (subsecuencia más larga)
**Librería:** Hugging Face `evaluate` (`evaluate.load("rouge")`)
**Rango:** 0–1 (mayor es mejor)

ROUGE-L mide el solapamiento léxico entre el texto generado y el texto de referencia, utilizando la subsecuencia común más larga (LCS). Es complementaria a SARI porque evalúa en qué medida el vocabulario del ground truth humano está presente en la salida del modelo. En Lectura Fácil, donde los textos de referencia fueron validados por personas con discapacidad cognitiva, una alta puntuación ROUGE-L indica que el modelo tiende hacia el mismo vocabulario y estructura que los adaptadores humanos certificados. Se eligió la variante ROUGE-L (en lugar de ROUGE-1 o ROUGE-2) porque captura el orden relativo de las palabras, lo que es relevante en textos donde la estructura sintáctica es parte del criterio de accesibilidad.

---

### 3. BLEU — Bilingual Evaluation Understudy
**Librería:** `sacrebleu` (`sacrebleu.corpus_bleu`)
**Rango:** 0–1 (mayor es mejor, normalizado desde 0–100)

BLEU (Papineni et al., 2002) evalúa la precisión de n-gramas del texto generado respecto a la referencia. Aunque fue diseñado originalmente para traducción automática, su uso está ampliamente extendido en tareas de generación de texto como métrica complementaria de solapamiento lexical. En este estudio, BLEU aporta una perspectiva distinta a ROUGE-L: mientras ROUGE-L mide la cobertura del texto de referencia (cuánto de la referencia aparece en la salida), BLEU mide la precisión de la salida (cuánto de la salida coincide con la referencia). Ambas métricas juntas permiten detectar si el modelo genera texto relevante sin alucinaciones ni expansiones innecesarias.

---

### 4. BERTScore F1
**Librería:** Hugging Face `evaluate` (`evaluate.load("bertscore")`, `lang="es"`)
**Rango:** 0–1 (mayor es mejor)

BERTScore (Zhang et al., 2020) calcula la similitud semántica entre el texto generado y la referencia utilizando embeddings contextuales del modelo BERT. A diferencia de SARI, ROUGE y BLEU, que operan a nivel de solapamiento de n-gramas (similitud superficial), BERTScore captura la equivalencia semántica aunque las palabras sean distintas. Esto es especialmente relevante en Lectura Fácil, donde una simplificación correcta reemplaza terminología compleja por sinónimos o perífrasis que no comparten tokens con la referencia pero transmiten el mismo significado. BERTScore con modelo en español (`lang="es"`) permite evaluar si el texto generado es semánticamente equivalente al original incluso cuando difiere léxicamente.

*Nota: esta métrica requiere la descarga de un modelo BERT (~700 MB) y puede omitirse en ejecuciones rápidas mediante el flag `--skip-bert`.*

---

### 5. Flesch Reading Ease (adaptación al español)
**Librería:** `textstat` (`textstat.flesch_reading_ease`)
**Rango:** 0–100+ (mayor = más legible; objetivo para Lectura Fácil: 65–75)

El índice de Flesch (Flesch, 1948) es la medida de legibilidad más utilizada en la literatura internacional, basada en la longitud media de las oraciones y el número medio de sílabas por palabra. Aunque fue desarrollado para el inglés, su fórmula ha sido validada en español con resultados comparables. Es la métrica central para evaluar la **accesibilidad lingüística** del texto generado: el objetivo del proyecto es que los textos produzcan puntuaciones en la franja 65–75, que corresponde al rango "fácil de leer" según los baremos estándar. A diferencia de las métricas basadas en referencia (SARI, ROUGE, BLEU), Flesch evalúa el texto generado de forma independiente, sin necesitar compararlo con nada, lo que permite detectar si el modelo ha simplificado realmente el lenguaje o solo ha reescrito el texto con complejidad similar.

---

### 6. Compression Ratio — Ratio de Compresión
**Implementación propia:** `palabras_generado / palabras_original`
**Rango:** > 0 (< 1 = síntesis, > 1 = expansión; objetivo: 0.7–0.9)

El ratio de compresión cuantifica la capacidad de síntesis del modelo. En Lectura Fácil, el texto adaptado debe ser más breve que el original sin perder contenido esencial — un ratio entre 0.7 y 0.9 indica que el modelo ha condensado correctamente el texto. Valores muy bajos (< 0.5) sugieren eliminación excesiva de información; valores superiores a 1 indican que el modelo ha expandido el texto, lo que puede ser señal de alucinaciones o de que ha añadido explicaciones no presentes en el original. Esta métrica es necesaria porque SARI y ROUGE no penalizan directamente la expansión masiva, y el análisis del presente estudio ha detectado casos extremos (ratio > 8) en algunos modelos que distorsionan los resultados medios.

---

### 7. LMO — Longitud Media de Oración
**Implementación propia:** media de palabras por oración, segmentada por puntuación fuerte
**Rango:** palabras/oración (objetivo para Lectura Fácil: < 10)

La longitud media de oración es uno de los dos componentes de la fórmula de Flesch, pero se incluye de forma independiente porque el estándar UNE 153101:2018 de Lectura Fácil establece explícitamente un máximo de una idea por frase y frases de entre 8 y 12 palabras como criterio de accesibilidad cognitiva. LMO permite diagnosticar exactamente si el modelo está generando frases largas con múltiples subordinadas — el principal problema detectado en los modelos que producen Flesch negativo — independientemente del vocabulario empleado. Es una métrica de diagnóstico más granular que Flesch para identificar la causa concreta de los problemas de legibilidad.

---

### 8. TTR — Type-Token Ratio (Diversidad Léxica)
**Implementación propia:** `tokens_únicos / tokens_totales`
**Rango:** 0–1 (mayor = mayor diversidad léxica)

El TTR mide la riqueza del vocabulario del texto generado como proporción de palabras únicas sobre el total de palabras. En el contexto de Lectura Fácil, el TTR tiene un papel dual: por un lado, valores muy bajos indican textos con repetición excesiva de las mismas palabras, lo que puede ser señal de que el modelo ha generado contenido redundante o de baja calidad; por otro lado, valores muy altos en textos cortos pueden indicar un vocabulario demasiado variado para el lector objetivo. Se incluye como métrica auxiliar para caracterizar el estilo léxico de cada modelo y detectar patrones anómalos de generación.

---

### 9. Índice de Palabras Complejas (Complex Words Ratio)
**Librería:** `textstat` (`textstat.polysyllabcount`)
**Implementación:** `palabras_polisílabas / palabras_totales`
**Rango:** 0–1 (menor = más accesible; objetivo: < 0.20)

El segundo componente de la legibilidad en Lectura Fácil es la complejidad del vocabulario. Este índice mide la proporción de palabras con tres o más sílabas, que son las que mayor dificultad de comprensión generan en lectores con discapacidad cognitiva o bajo nivel de alfabetización. El estándar europeo de Lectura Fácil prescribe explícitamente el uso de palabras cortas y comunes, y este índice cuantifica en qué medida cada modelo cumple esa prescripción. Es complementario a LMO: un texto puede tener frases cortas pero con vocabulario técnico polisílabo, o frases largas con palabras simples — ambas dimensiones son necesarias para el diagnóstico completo.

---

### 10. NER Density — Densidad de Entidades Nombradas
**Librería:** `spaCy` (modelo `es_core_news_sm`)
**Implementación:** `entidades_nombradas / tokens_totales`
**Rango:** 0–1 (métrica de diagnóstico, no tiene dirección óptima única)

La densidad de entidades nombradas (personas, organizaciones, lugares, fechas) mide cuánta información referencial específica contiene el texto generado. En Lectura Fácil existe una tensión entre dos criterios del estándar: por un lado, se deben eliminar las enumeraciones exhaustivas de organismos y entidades; por otro, se deben conservar los nombres propios esenciales para que el texto sea informativo. Esta métrica permite diagnosticar si los modelos están eliminando correctamente las enumeraciones innecesarias o si, por el contrario, están produciendo textos con muy baja densidad de entidades (pérdida de información) o muy alta (expansión de la lista original). Se interpreta comparando la densidad del texto generado con la del texto original.

---

### 11. Levenshtein Normalizada — Distancia de Edición
**Implementación propia:** distancia de edición a nivel de palabra, normalizada por la longitud máxima
**Rango:** 0–1 (menor = más cercano a la referencia)

La distancia de Levenshtein normalizada mide el número mínimo de operaciones de edición (inserción, eliminación, sustitución de palabras) necesarias para transformar el texto generado en el texto de referencia, expresado como proporción de la longitud del texto más largo. Complementa a ROUGE-L y BLEU desde una perspectiva diferente: mientras que ROUGE y BLEU miden el solapamiento de n-gramas, la distancia de Levenshtein mide la distancia estructural global entre el texto generado y la referencia, penalizando las diferencias de orden y longitud. Una distancia baja indica que el texto generado es estructuralmente cercano al texto humano de referencia, incluso si el vocabulario es parcialmente distinto.

---

## Resumen de la selección

| Métrica | Dimensión evaluada | Base teórica | Necesita referencia |
|---|---|---|---|
| SARI | Calidad de simplificación (operaciones de edición) | Xu et al. (2016) | Sí (original + referencia) |
| ROUGE-L | Solapamiento léxico con la referencia | Lin (2004) | Sí |
| BLEU | Precisión de n-gramas respecto a la referencia | Papineni et al. (2002) | Sí |
| BERTScore F1 | Equivalencia semántica | Zhang et al. (2020) | Sí |
| Flesch Reading Ease | Legibilidad global del texto generado | Flesch (1948) | No |
| Compression Ratio | Capacidad de síntesis | Métrica de corpus | No |
| LMO | Longitud de oración (estructura sintáctica) | UNE 153101:2018 | No |
| TTR | Diversidad léxica | Lingüística computacional | No |
| Complex Words Ratio | Complejidad del vocabulario | UNE 153101:2018 | No |
| NER Density | Densidad de información referencial | NLP aplicado | No (comparativa) |
| Levenshtein normalizada | Distancia estructural a la referencia | Levenshtein (1966) | Sí |

La selección cubre las cuatro preguntas de evaluación del estudio:

1. **¿Preserva el modelo el contenido del original?** → SARI, ROUGE-L, BLEU, BERTScore, Levenshtein
2. **¿Es el texto resultante accesible para el lector objetivo?** → Flesch, LMO, Complex Words Ratio
3. **¿Sintetiza el modelo o expande el texto?** → Compression Ratio, LMO
4. **¿Mantiene el modelo la densidad informativa adecuada?** → NER Density, TTR

---

## Referencias

- Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, 32(3), 221–233.
- Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707–710.
- Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. *ACL Workshop on Text Summarization Branches Out*.
- Papineni, K., Roukos, S., Ward, T., & Zhu, W.-J. (2002). BLEU: a method for automatic evaluation of machine translation. *ACL 2002*, 311–318.
- Xu, W., Napoles, C., Pavlick, E., Chen, Q., & Callison-Burch, C. (2016). Optimizing statistical machine translation for text simplification. *TACL*, 4, 401–415.
- Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating text generation with BERT. *ICLR 2020*.
- AENOR (2018). *UNE 153101:2018 Lectura Fácil. Pautas y recomendaciones para la elaboración de documentos*. Asociación Española de Normalización.
- IFLA (2010). *Guidelines for Easy-to-Read Materials*. International Federation of Library Associations and Institutions.
