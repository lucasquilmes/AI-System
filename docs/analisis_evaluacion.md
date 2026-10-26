# Informe de Evaluación — Técnicas de Prompting para Lectura Fácil
**Fecha:** Mayo 2026  
**Modelos evaluados:** 7 modelos Ollama (llama3.1_8b, mistral-nemo, command-r, gemma2_27b, mixtral, llama3.3, qwen2.5_32b)  
**Técnicas evaluadas:** V0, V1, V2, zero_shot, few_shot, role, cot, zs_cot, tot, self_cons, self_ref, ensemble  
**Métricas:** SARI, ROUGE-L, BLEU, Flesch Reading Ease, Compression Ratio, LMO, TTR, Complex Words Ratio, NER Density, Levenshtein normalizada

---

## 1. Advertencia Estructural: V0 no es comparable con el resto

**V0 solo evaluó las filas 1–5 del dataset (12 disponibles).** Las filas 6–12 no fueron generadas para V0. Cualquier comparación directa de V0 con otras versiones es estadísticamente inválida — sus métricas reflejan un subconjunto distinto, no la misma distribución de textos. Los rankings que incluyen V0 deben interpretarse con precaución.

---

## 2. Métricas y objetivos del proyecto

| Métrica | Dirección | Objetivo Lectura Fácil | Notas |
|---------|-----------|------------------------|-------|
| SARI | Mayor es mejor | 45–55 | Preservación semántica respecto al original y la referencia |
| ROUGE-L | Mayor es mejor | > 0.35 | Solapamiento léxico con el ground truth |
| BLEU | Mayor es mejor | > 0.12 | Precisión de n-gramas respecto a la referencia |
| Flesch generado | Mayor es mejor | 65–75 | Legibilidad del texto producido |
| Compression ratio | ~0.7–0.9 | 0.7–0.9 | < 1 = síntesis, > 1 = expansión |
| LMO generado | Menor es mejor | < 10 palabras/frase | Longitud media de oración |
| Complex words ratio | Menor es mejor | < 0.20 | Proporción de palabras polisílabas |
| Levenshtein normalizada | Menor es mejor | < 0.65 | Distancia estructural al ground truth |

---

## 3. Problema de base: algunas filas son intrínsecamente difíciles

El análisis a nivel de fila revela que los promedios por técnica o modelo esconden patrones críticos de dificultad en los textos de entrada.

| Fila | SARI media | SARI std | Flesch media | Diagnóstico |
|------|-----------|---------|-------------|-------------|
| 1 | 40.3 | 3.7 | 33.4 | Estable, dificultad moderada |
| 2 | 35.9 | 8.2 | 46.3 | Peor SARI media — difícil de simplificar |
| 4 | 36.4 | 8.9 | 44.3 | Alta varianza, muchos fallos |
| **6** | 38.5 | 3.8 | **25.5** | **Flesch más bajo del dataset.** Texto sobre trámites con siglas (Cl@ve, FNMT, Carpeta Ciudadana). Los modelos generan listas exhaustivas sin puntuación |
| **7** | **48.4** | **11.7** | **20.1** | **Mayor SARI pero también mayor varianza y peor Flesch.** Texto sobre estructura del Estado y la UE. Los modelos lo usan como excusa para enumerar toda la estructura institucional |
| **11** | 41.5 | **14.3** | 35.2 | **Fila más inestable del dataset.** "El teléfono 060" es tan corto que los modelos divergen al máximo: SARI de 15 a 70 en la misma fila |

### Diagnóstico de la fila 7

La fila 7 ("Administración Pública y Estado; la UE") es el punto de quiebre de la evaluación. Concentra la mayoría de los outliers de expansión y de Flesch negativo:

- TOT / llama3.3 / fila 7: compression ratio **5.75x** — el modelo escribe las tres ramas completas
- ENSEMBLE / llama3.1_8b / fila 7: compression ratio **5.22x**
- V2 / llama3.3 / fila 6: LMO de **137 palabras por frase** (Flesch = -103.89)

### Diagnóstico de la fila 11

"El teléfono 060 te ofrece información administrativa general..." es un texto de una sola frase simple. Esta simplicidad genera los resultados más extremos de todo el dataset. Algunos modelos producen SARI = 70 (prácticamente perfecto); otros generan respuestas de una sola palabra con SARI = 15.

---

## 4. Outliers que distorsionan los promedios

### Flesch negativos (texto más denso que el original)

Se identificaron **17 filas con Flesch < 0** en 9 versiones y 5 modelos distintos:

| Caso | Flesch | LMO | Causa |
|------|--------|-----|-------|
| V2 / llama3.3 / fila 6 | **-103.89** | 137 | Una frase de 137 palabras ininterrumpida |
| ZERO_SHOT / mistral-nemo / fila 7 | -18.06 | 29 | Enumeración institucional sin puntuación |
| V2 / llama3.1_8b / fila 7 | -17.23 | 39 | Párrafo monolítico sobre el Estado |
| V2 / llama3.1_8b / fila 5 | -17.11 | 68 | Ídem |
| ROLE / llama3.1_8b / fila 7 | -11.43 | 15 | El rol de experta no frenó la expansión |

### Expansión masiva (compression ratio > 3)

**18 filas** producen un output más de 3 veces más largo que el original. Responsables principales:

- **mixtral** aparece en 6 de las 18 instancias. En ENSEMBLE/mixtral fila 11 el ratio es **8.75x**.
- **TOT** con modelos grandes: el proceso de "explorar 3 ramas" hace que el modelo escriba las tres versiones en lugar de elegir una.
- **La fila 7 concentra la mayoría** — todos los modelos intentan ser exhaustivos con la estructura institucional.

### SARI < 20 (fallos completos)

8 filas con SARI < 20, lo que indica que el modelo no preservó ni el vocabulario básico:

| Caso | SARI | Causa probable |
|------|------|----------------|
| TOT / llama3.1_8b / fila 7 | **13.3** | Peor resultado del dataset entero |
| COT / mixtral / fila 4 | 16.2 | El modelo devolvió solo los pasos de razonamiento, sin texto final |
| V1 / mixtral / fila 11 | 15.1 | Respuesta de 1 sola palabra (compression ratio 0.05) |
| V1 / mixtral / fila 3 | 19.5 | Texto ultracorto sin relación con el original |

---

## 5. El dilema estructural: SARI vs Flesch

La correlación entre SARI (preservación semántica) y Flesch (legibilidad) es **negativa en casi todas las técnicas**, lo que confirma un trade-off fundamental: preservar más contenido produce texto más denso.

| Técnica | Correlación SARI–Flesch | Interpretación |
|---------|------------------------|----------------|
| **ROLE** | **+0.145** | Única con correlación positiva. El rol experto ayuda a mantener ambas cualidades a la vez |
| ZERO_SHOT | +0.024 | Prácticamente independientes — ni se refuerzan ni se perjudican |
| ENSEMBLE | -0.061 | Casi neutral |
| V1, V2 | -0.11 / -0.12 | Baja tensión |
| SELF_REF | -0.322 | Tensión moderada |
| SELF_CONS | -0.361 | Alta tensión — las 3 perspectivas amplifican el trade-off |
| FEW_SHOT | -0.281 | Los ejemplos sesgan hacia un estilo que sacrifica uno u otro |

**ROLE es la única técnica donde SARI y Flesch no se contraponen.** El personaje de la experta en accesibilidad cognitiva interioriza ambos objetivos simultáneamente, aunque su porcentaje de éxito global no sea el más alto.

---

## 6. Ranking compuesto (score normalizado 0–1)

El score compuesto normaliza SARI, ROUGE-L, BLEU, Flesch, LMO, palabras complejas y Levenshtein en una escala 0–1 y promedia.

### Por técnica

| Rank | Técnica | Score compuesto | Notas |
|------|---------|----------------|-------|
| 1 | **SELF_REF** | 0.544 | Más equilibrada |
| 2 | **ENSEMBLE** | 0.527 | Mejor SARI pero Flesch bajo |
| 3 | **ROLE** | 0.526 | Única correlación positiva SARI–Flesch |
| 4 | ZERO_SHOT | 0.524 | Sorprendentemente competitiva |
| 5 | V0* | 0.506 | *Solo 5 filas — no comparable |
| 6 | ZS_COT | 0.499 | — |
| 7 | COT | 0.485 | El ejemplo de razonamiento no aporta consistencia |
| 8 | SELF_CONS | 0.479 | — |
| 9 | V2 | 0.477 | Mejor de las estrategias originales |
| 10 | TOT | 0.461 | Demasiados outliers de expansión |
| 11 | FEW_SHOT | 0.447 | Los ejemplos no mejoran sobre zero_shot |
| 12 | **V1** | **0.427** | **Peor técnica — brevedad extrema es contraproducente** |

### Por modelo

| Rank | Modelo | Score compuesto | Notas |
|------|--------|----------------|-------|
| 1 | **mistral-nemo** | 0.542 | Mejor SARI promedio pero baja consistencia en Flesch |
| 2 | **llama3.3** | 0.524 | Más equilibrado y consistente |
| 3 | qwen2.5_32b | 0.508 | — |
| 4 | gemma2_27b | 0.499 | Mejor modelo para Flesch |
| 5 | llama3.1_8b | 0.486 | Outliers positivos altos en SARI pero inconsistente |
| 6 | command-r | 0.465 | — |
| 7 | **mixtral** | **0.417** | **Peor modelo — altamente impredecible** |

---

## 7. Consistencia real: % filas con SARI > 40 Y Flesch > 25

Los promedios no reflejan con qué frecuencia un modelo produce resultados usables. Esta métrica de consistencia mide el porcentaje de filas que cumplen simultáneamente ambos criterios mínimos.

### Por modelo

| Modelo | % filas buenas | SARI mediana | Flesch mediana | Diagnóstico |
|--------|---------------|-------------|---------------|-------------|
| **llama3.3** | **53%** | 41.9 | 40.3 | El más consistente. Equilibra bien ambas métricas |
| gemma2_27b | 47% | 39.9 | 43.8 | Mejor Flesch pero SARI más bajo |
| qwen2.5_32b | 45% | 40.9 | 40.0 | Equilibrado, menos estable en filas difíciles |
| mixtral | 44% | 41.3 | 34.4 | Alta varianza — muy bueno o muy malo |
| llama3.1_8b | 42% | 41.0 | 34.7 | Outliers positivos en SARI pero mediocre en Flesch |
| **mistral-nemo** | **38%** | 42.9 | 30.5 | **Paradoja**: mejor SARI promedio pero peor consistencia — sacrifica Flesch sistemáticamente |
| command-r | 36% | 40.4 | 32.4 | El más inestable. Falla con mayor frecuencia en filas difíciles |

> **mistral-nemo es engañoso en los promedios**: su SARI promedio es el más alto de todos los modelos (43.84) pero solo el 38% de sus filas cumplen el doble criterio. Prioriza preservar contenido a costa de legibilidad de forma sistemática en prácticamente todas las técnicas.

### Por técnica

| Técnica | % filas buenas | SARI mediana | SARI std | Diagnóstico |
|---------|---------------|-------------|---------|-------------|
| **ENSEMBLE** | **52.4%** | 43.81 | 9.19 | Mejor mediana SARI, alta varianza, Flesch bajo |
| **SELF_REF** | **52.4%** | 43.58 | **7.93** | Mismo % que ENSEMBLE pero **más estable** |
| SELF_CONS | 50.0% | 40.74 | 8.59 | Razonablemente consistente |
| V2 | 48.8% | 42.20 | 8.48 | Mejor de las 3 estrategias originales |
| FEW_SHOT | 47.6% | 41.73 | 9.08 | Mejor consistencia de lo esperado |
| ZERO_SHOT | 42.9% | 41.14 | **7.06** | **La más estable de todas** (menor desviación estándar) |
| ZS_COT | 41.7% | 40.38 | 8.03 | Similar a ZERO_SHOT |
| COT | 39.3% | 39.75 | 9.87 | El ejemplo de razonamiento no mejora la consistencia |
| ROLE | 39.3% | 40.99 | 7.66 | Consistente pero con umbral de calidad bajo |
| TOT | 35.7% | 41.54 | 9.39 | Demasiados outliers de expansión en fila 7 |
| **V1** | **28.6%** | 36.90 | 8.97 | **Peor de todas** |

---

## 8. Matrices de rendimiento: modelo × técnica

### SARI mediana

| Modelo | COT | ENSEMBLE | FEW_SHOT | ROLE | SELF_CONS | SELF_REF | TOT | V1 | V2 | ZERO_SHOT | ZS_COT |
|--------|-----|----------|----------|------|-----------|----------|-----|-----|-----|-----------|--------|
| command-r | 44.3 | 40.4 | 41.3 | 39.7 | 37.6 | **44.9** | 37.9 | 40.6 | 40.1 | 37.7 | 39.2 |
| gemma2_27b | 41.2 | **43.9** | 37.5 | 42.5 | 35.5 | 38.9 | 40.8 | 38.1 | 41.9 | 38.8 | 38.9 |
| llama3.1_8b | 37.4 | 44.2 | 41.0 | 38.5 | 41.6 | **44.6** | 41.4 | 37.0 | 45.3 | 40.2 | 40.4 |
| llama3.3 | 39.4 | **44.6** | 38.9 | 41.5 | 39.1 | 45.2 | 43.6 | 38.9 | 40.8 | 46.0 | 44.3 |
| mistral-nemo | 38.0 | 44.4 | 44.2 | 40.7 | 43.7 | 43.8 | **47.8** | 37.5 | 44.4 | 42.1 | 41.4 |
| mixtral | 37.8 | 39.4 | 41.6 | 41.7 | 42.1 | **43.5** | 40.8 | 31.0 | 41.1 | 45.0 | 43.7 |
| qwen2.5_32b | 41.7 | **43.8** | 40.0 | 42.3 | 42.1 | 41.1 | 40.8 | 33.8 | 43.2 | 38.7 | 33.7 |

### Flesch mediana

| Modelo | COT | ENSEMBLE | FEW_SHOT | ROLE | SELF_CONS | SELF_REF | TOT | V1 | V2 | ZERO_SHOT | ZS_COT |
|--------|-----|----------|----------|------|-----------|----------|-----|-----|-----|-----------|--------|
| command-r | **41.4** | 32.3 | 33.4 | 22.8 | 40.8 | 28.7 | 27.4 | 38.4 | 34.1 | 25.5 | 32.8 |
| gemma2_27b | **56.0** | 42.0 | 41.9 | 40.8 | 48.4 | 35.5 | 39.2 | 54.8 | 46.4 | 39.5 | 42.4 |
| llama3.1_8b | 37.9 | 25.4 | 39.8 | 21.8 | 36.5 | 36.3 | 23.7 | **42.5** | 30.5 | 37.1 | 30.9 |
| llama3.3 | 42.4 | 38.2 | **45.2** | 48.0 | 40.5 | 33.8 | 31.4 | 51.6 | 40.9 | 36.6 | 38.4 |
| mistral-nemo | 36.3 | 32.2 | **36.5** | 29.9 | 34.5 | 30.8 | 23.1 | 23.5 | 25.3 | 23.3 | 31.6 |
| mixtral | 39.3 | 28.4 | 28.0 | 25.4 | 36.8 | 30.0 | 30.3 | 36.6 | 37.6 | 33.8 | **41.1** |
| qwen2.5_32b | **46.6** | 38.1 | 42.2 | 32.3 | 44.7 | 34.0 | 38.8 | 46.6 | 38.9 | 41.9 | 37.1 |

---

## 9. Mejores resultados individuales (SARI > 50 Y Flesch > 25)

Las combinaciones donde un modelo logró simultáneamente alta preservación y legibilidad aceptable:

| Combo | Fila | SARI | Flesch | ROUGE-L | BLEU |
|-------|------|------|--------|---------|------|
| ENSEMBLE / llama3.3 / fila 11 | 11 | **70.0** | 53.6 | 0.489 | 0.304 |
| FEW_SHOT / mistral-nemo / fila 7 | 7 | 69.5 | 24.1 | 0.548 | 0.331 |
| ENSEMBLE / mixtral / fila 11 | 11 | 68.6 | 32.1 | 0.236 | 0.079 |
| COT / mistral-nemo / fila 7 | 7 | 64.3 | 26.6 | **0.675** | **0.437** |
| SELF_REF / mistral-nemo / fila 7 | 7 | 68.7 | 8.0 | 0.621 | 0.393 |
| FEW_SHOT / qwen2.5_32b / fila 5 | 5 | 56.0 | 53.8 | 0.327 | 0.174 |

---

## 10. Conclusiones Estratégicas

### 10.1 Sobre las técnicas

**SELF_REF es la técnica más robusta para producción.** Tiene el mismo porcentaje de éxito que ENSEMBLE (52.4%) pero con menor desviación estándar (7.93 vs 9.19). El ciclo borrador→revisión→final corrige activamente los problemas de vocabulario y frases largas que otras técnicas ignoran. Menos brillante en el máximo absoluto, pero menos catastrófica en los peores casos.

**ZERO_SHOT es la técnica más predecible.** Tiene la menor desviación estándar de SARI de todo el dataset (7.06). Resultados sin picos extremos hacia arriba ni hacia abajo. Es la elección correcta cuando la estabilidad importa más que optimizar el máximo.

**ENSEMBLE maximiza SARI pero no es adecuado para Lectura Fácil pura.** Los 3 expertos virtuales preservan contenido de forma óptima pero el output es sistemáticamente denso (Flesch mediana 33.7, LMO mediana 15 palabras/frase). Usar solo si el objetivo es recuperación de información, no accesibilidad cognitiva.

**TOT produce los mejores SARI individuales pero es impredecible.** TOT/mistral-nemo fila 7 alcanza SARI 47.86 de promedio — el mejor de todo el dataset — pero tiene demasiados outliers de expansión masiva. El proceso de "explorar 3 ramas" hace que modelos grandes escriban las tres versiones completas en lugar de elegir una.

**V1 (brevedad extrema) es la peor estrategia.** Solo el 28.6% de sus filas cumplen ambos criterios. Sacrifica demasiado SARI y solapamiento lexical en favor de un Flesch marginalmente mejor que otras técnicas. El resultado es texto corto pero que no refleja el contenido original.

**ROLE es la técnica con la propiedad más valiosa a largo plazo:** es la única donde SARI y Flesch se correlacionan positivamente (r = +0.145). Esto significa que, a diferencia de todas las demás técnicas, mejorar en una métrica no empeora la otra. Sin embargo, su techo actual es bajo — requiere afinar el personaje para activar todo su potencial.

**FEW_SHOT sorprende negativamente.** Proporcionar ejemplos explícitos de transformación no mejora los resultados sobre ZERO_SHOT en ninguna métrica principal. Los ejemplos que se utilizan pueden estar sesgando al modelo hacia un estilo que no generaliza bien al resto de los textos del dataset.

### 10.2 Sobre los modelos

**llama3.3 es el modelo más fiable en producción real.** Mayor porcentaje de filas que cumplen ambos criterios (53%). No domina ninguna métrica individual pero es el más equilibrado y predecible en textos difíciles (filas 6, 7, 11).

**mistral-nemo es el mejor modelo para maximizar SARI, pero no es adecuado si el objetivo principal es Lectura Fácil.** Produce los outputs más informativos pero sistemáticamente densos. Solo el 38% de sus filas alcanzan Flesch > 25. Su alto promedio de SARI (43.84) enmascara una tendencia estructural a generar texto complejo.

**gemma2_27b es el especialista en legibilidad.** Domina el Flesch en prácticamente todas las técnicas (mediana 43.76 — la más alta de todos los modelos). La combinación COT/gemma2_27b alcanza Flesch mediana 56, el mejor resultado del dataset. Sin embargo, su SARI es el segundo más bajo, lo que indica que simplifica a costa de perder contenido.

**mixtral es impredecible y problemático en producción.** Genera texto 8.75x más largo que el original en algunos casos (ENSEMBLE/mixtral fila 11) y texto de una sola palabra en otros (V1/mixtral fila 11, SARI = 15.1). Su tasa de inconsistencia lo hace inadecuado sin postprocesado que detecte y filtre sus outputs extremos.

### 10.3 Sobre el dataset

**El target Flesch 65–75 es actualmente inalcanzable.** La mejor mediana es 56 (COT/gemma2_27b). El límite práctico del sistema actual parece estar en ~50. Para superarlo se requeriría añadir restricciones duras en los prompts: longitud máxima de frase de 8 palabras, prohibición explícita de palabras de más de 2 sílabas, y posiblemente postprocesado que segmente automáticamente las frases largas.

**La fila 7 y la fila 11 necesitan tratamiento especial.** La fila 7 (texto sobre estructura del Estado) es intrínsecamente difícil — todos los modelos la inflan. La fila 11 (texto ultracorto) produce los resultados más extremos del dataset en ambas direcciones. Una estrategia de producción robusta debería detectar estas tipologías de texto y aplicar prompts distintos según la longitud y complejidad del input.

---

## 11. Recomendaciones Accionables

| Prioridad | Recomendación | Fundamento |
|-----------|--------------|-----------|
| Alta | Usar **SELF_REF + llama3.3** como combinación base de producción | Mejor consistencia (52.4% filas buenas), menor varianza |
| Alta | Regenerar V0 con las 12 filas completas para hacerla comparable | Actualmente V0 solo evaluó filas 1–5 |
| Alta | Añadir restricción de longitud de frase (<8 palabras) en todos los prompts | Ninguna técnica alcanza Flesch > 56; la causa principal son las frases largas |
| Media | Refinar el prompt ROLE con ejemplos de validación de personas reales | Es la única técnica con SARI–Flesch positivamente correlacionados |
| Media | Postprocesar outputs de mixtral (filtrar si compression_ratio > 3 o Flesch < 0) | Sus outliers contaminan los resultados de evaluación |
| Baja | Reemplazar FEW_SHOT por mejores ejemplos del propio dataset | Los ejemplos actuales sesgan sin mejorar resultados |
| Baja | Instalar BertScore para tener métrica semántica basada en embeddings | Actualmente omitido por peso (~700 MB); aportaría una dimensión semántica más profunda que SARI |
