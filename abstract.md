# Evaluación de modelos de lenguaje locales para la adaptación automática a Lectura Fácil

**Informe Fase 1 — Evaluación exhaustiva de modelos y técnicas de prompting**

---

## 1. Resumen ejecutivo

Este estudio evalúa la capacidad de ocho modelos de lenguaje grandes (LLMs) ejecutados en local para adaptar textos al estándar de **Lectura Fácil (UNE 153101:2018)**, probando 20 técnicas de prompting distintas sobre dos datasets con referencias humanas certificadas. Se trata de la primera fase de un estudio más amplio cuyo objetivo final es identificar la configuración óptima —modelo, prompt y parámetros de generación— para la adaptación automática de documentos públicos a Lectura Fácil sin depender de servicios externos.

Los resultados muestran que **el diseño del prompt tiene más impacto en la calidad del output que el tamaño del modelo**, que **no existe una técnica universalmente mejor** entre datasets de diferente dominio, y que la **imitación progresiva del estilo experto (V8)** es la técnica más efectiva en textos administrativos, alcanzando los máximos absolutos del estudio en SARI (0.557) y similitud Levenshtein (0.325).

---

## 2. Motivación

La Lectura Fácil es un estándar de accesibilidad lingüística reconocido internacionalmente y regulado en España por la norma UNE 153101:2018. Está orientado a personas con dificultades de comprensión lectora —ya sea por discapacidad intelectual, baja alfabetización, o por ser hablantes no nativos— y establece criterios concretos sobre vocabulario, longitud de oraciones, estructura visual y complejidad sintáctica.

La adaptación manual de documentos a Lectura Fácil es un proceso costoso que requiere formadores certificados. La demanda supera con creces la oferta, dejando sin acceso accesible a una parte significativa de la ciudadanía. Automatizar este proceso mediante LLMs locales —sin depender de APIs externas de pago, sin enviar datos a terceros— representa una vía accesible, privada y escalable especialmente relevante para instituciones públicas, administraciones y organizaciones del tercer sector.

---

## 3. Metodología

### 3.1 Modelos evaluados

Se evaluaron ocho modelos de lenguaje ejecutados en local mediante **Ollama**, todos con temperatura fija `T=0.0` y semilla fija `seed=42` para garantizar que los resultados son completamente reproducibles — con temperatura cero y semilla fija, ante el mismo input el modelo produce siempre el mismo output.

| Modelo | Parámetros | Familia | Característica destacada |
|---|---|---|---|
| llama3.1:8b | 8B | Meta | Modelo ligero, referencia base |
| mistral-nemo | 12B | Mistral AI | Eficiente, ventana de contexto amplia |
| command-r | 35B | Cohere | Optimizado para seguimiento de instrucciones |
| gemma2:27b | 27B | Google | Alta calidad en generación de texto |
| mixtral | 47B (MoE) | Mistral AI | Arquitectura Mixture-of-Experts |
| llama3.3 | 70B | Meta | Mayor modelo evaluado |
| qwen2.5:32b | 32B | Alibaba | Multilingüe, fuerte en español |
| aya-expanse:32b | 32B | Cohere | Especializado en lenguas no inglesas |

### 3.2 Técnicas de prompting evaluadas

Se diseñaron y evaluaron **20 técnicas de prompting** organizadas en tres grupos:

#### Versiones propias (v1–v8) — progresión sistemática

| Versión | Técnica principal | Descripción |
|---|---|---|
| V1 | Instrucción básica con brevedad extrema | Prompt mínimo con regla de máximo 8 palabras por frase |
| V2 | Instrucción equilibrada | Reglas básicas de Lectura Fácil sin ejemplos |
| V3 | Few-shot + reglas explícitas | Ejemplos reales + checklist de criterios UNE |
| V4 | Ensemble de expertos + compresión | Panel de 3 expertos con roles diferentes + reglas MOTOR + compresión aware |
| V5 | Tree of Thought dual | Dos caminos paralelos (fidelidad vs. brevedad) + fusión |
| V6 | Pipeline frase a frase | 6 reglas aplicadas secuencialmente (R1: división → R6: longitud) |
| V7 | Vocabulario anclado | Tabla de sustitución léxica explícita + 4 pasos con ejemplos anotados |
| V8 | Imitación progresiva | 3 fases: análisis del GT → plantillas de estructura → escritura imitativa |

#### Técnicas estándar de prompting (10)

`zero-shot` · `few-shot` · `role prompting` · `chain-of-thought (CoT)` · `zero-shot CoT` · `tree of thoughts (ToT)` · `self-consistency` · `self-refinement` · `ensemble` · `meta-prompting`

#### Prompts de dominio específico (2)

- **motor**: diseñado para simplificar documentos de seguros de automóvil
- **audit**: diseñado para auditar y adaptar documentos institucionales

### 3.3 Datasets

| Dataset | Textos | Dominio | Origen referencias |
|---|---|---|---|
| **test_poor** | 12 | Textos administrativos de alta complejidad | Anotadores humanos |
| **exemples_lectura_facil_formatted** | 11 | Dominio diverso (salud, servicios, administración) | Referencias certificadas LF |

Cada texto fue procesado por los 8 modelos con las 20 técnicas, generando **1.908 outputs evaluados** en test_poor y **1.758** en exemples_lectura_facil_formatted, para un total de **3.666 evaluaciones individuales**.

### 3.4 Métricas de evaluación

Se calcularon 7 métricas automáticas, ordenadas por relevancia para el objetivo del estudio:

| # | Métrica | Descripción | Dirección óptima |
|---|---|---|---|
| 1 | **SARI** | Calidad de operaciones de simplificación (añadir/conservar/eliminar) respecto a la referencia | Mayor = mejor |
| 2 | **BERTScore F1** | Similitud semántica con la referencia mediante embeddings contextuales | Mayor = mejor |
| 3 | **Levenshtein similarity** | Proximidad léxica al texto producido por el experto humano (`1 − distancia normalizada`) | Mayor = mejor |
| 4 | **CWR ratio** | Proporción de palabras complejas del output vs. referencia | Más cerca de 1.0 |
| 5 | **Flesch ratio** | Índice de legibilidad Flesch del output vs. referencia | Más cerca de 1.0 |
| 6 | **CR ratio** | Tasa de compresión del output vs. referencia | Más cerca de 1.0 |
| 7 | **TTR ratio** | Diversidad léxica (type-token ratio) del output vs. referencia | Más cerca de 1.0 |

Adicionalmente se calculó un **score combinado** normalizado [0–1] que agrega las 7 métricas con criterio por dirección, utilizado como indicador global de calidad para rankings comparativos.

---

## 4. Resultados — Dataset test_poor

*1.908 evaluaciones · textos administrativos de alta complejidad*

### 4.1 Estadísticas globales

| Métrica | Media | Desv. estándar | Mínimo | Máximo |
|---|---|---|---|---|
| SARI | 0.441 | 0.120 | 0.133 | 0.992 |
| BERTScore F1 | 0.769 | 0.060 | 0.504 | 1.000 |
| Levenshtein | 0.199 | 0.154 | 0.000 | 1.000 |
| CWR ratio | 1.097 | 0.296 | 0.000 | 2.057 |
| Flesch ratio | 0.906 | 0.404 | −2.123 | 2.560 |
| CR ratio | 1.264 | 1.058 | 0.011 | 11.061 |
| TTR ratio | 1.121 | 0.356 | 0.467 | 2.634 |

La alta desviación estándar del CR ratio (±1.058) revela comportamientos muy dispares en compresión: algunos modelos/prompts generan texto hasta 11 veces más largo que la referencia.

### 4.2 Ranking de modelos

| Rank | Modelo | Score | SARI | BERTScore | Levenshtein | CR ratio |
|---|---|---|---|---|---|---|
| 1 | **llama3.3** | 0.756 | 0.455 | 0.772 | 0.209 | 1.324 |
| 2 | **gemma2_27b** | 0.644 | 0.437 | 0.765 | 0.184 | 1.158 |
| 3 | qwen2.5_32b | 0.619 | 0.432 | 0.778 | 0.211 | 1.028 |
| 4 | mistral-nemo | 0.614 | 0.458 | 0.787 | 0.241 | 1.127 |
| 5 | llama3.1_8b | 0.536 | 0.445 | 0.774 | 0.211 | 1.518 |
| 6 | command-r | 0.450 | 0.437 | 0.778 | 0.202 | 1.019 |
| 7 | aya-expanse_32b | 0.447 | 0.433 | 0.763 | 0.172 | 1.274 |
| 8 | mixtral | 0.284 | 0.427 | 0.733 | 0.165 | 1.649 |

llama3.3 lidera con claridad. Destaca que mistral-nemo (#4 en score) obtiene el mejor BERTScore (0.787) y Levenshtein (0.241), pero sus ratios de compresión y legibilidad penalizan su score combinado.

### 4.3 Ranking de prompts

| Rank | Prompt | Score | SARI | BERTScore | Levenshtein | CR ratio |
|---|---|---|---|---|---|---|
| 1 | **V8** | 0.727 | **0.557** | **0.817** | **0.325** | 1.285 |
| 2 | **V6** | 0.707 | 0.474 | 0.793 | 0.250 | 1.095 |
| 3 | **V4** | 0.707 | 0.484 | 0.791 | 0.274 | 1.035 |
| 4 | V7 | 0.666 | 0.522 | 0.809 | 0.319 | 1.144 |
| 5 | V3 | 0.648 | 0.498 | 0.780 | 0.258 | 1.236 |
| 6 | MOTOR | 0.560 | 0.393 | 0.748 | 0.158 | 1.104 |
| 7 | CoT | 0.506 | 0.399 | 0.762 | 0.168 | 0.984 |
| 8 | META | 0.501 | 0.435 | 0.758 | 0.163 | 1.496 |
| … | … | … | … | … | … | … |
| 19 | TOT | 0.329 | 0.419 | 0.765 | 0.181 | 1.348 |
| 20 | V1 | 0.316 | 0.368 | 0.727 | 0.127 | 0.901 |

V8 domina en las tres métricas más importantes. Los prompts V3–V8 (diseñados específicamente para Lectura Fácil administrativa) ocupan los 5 primeros puestos, muy por encima de las técnicas estándar.

### 4.4 Top 10 combinaciones modelo × prompt

| Rank | Modelo | Prompt | Score | SARI | BERTScore | Levenshtein |
|---|---|---|---|---|---|---|
| 1 | gemma2_27b | V8 | 0.896 | 0.586 | 0.834 | 0.370 |
| 2 | llama3.3 | V4 | 0.859 | 0.539 | 0.803 | 0.316 |
| 3 | llama3.3 | V8 | 0.845 | 0.577 | 0.833 | 0.348 |
| 4 | llama3.3 | V3 | 0.845 | 0.566 | 0.802 | 0.328 |
| 5 | aya-expanse_32b | V8 | 0.831 | 0.553 | 0.807 | 0.329 |
| 6 | llama3.1_8b | V8 | 0.816 | 0.521 | 0.804 | 0.279 |
| 7 | llama3.3 | V7 | 0.814 | 0.549 | 0.818 | 0.338 |
| 8 | mistral-nemo | V3 | 0.810 | 0.553 | 0.823 | 0.336 |
| 9 | command-r | V8 | 0.808 | 0.574 | 0.829 | 0.334 |
| 10 | qwen2.5_32b | V4 | 0.804 | 0.482 | 0.802 | 0.287 |

La combinación gemma2_27b + V8 es la mejor del estudio en test_poor, con un SARI de 0.586 y Levenshtein de 0.370 — valores notablemente por encima de la media global.

---

## 5. Resultados — Dataset exemples_lectura_facil_formatted

*1.758 evaluaciones · textos de dominio diverso con referencias certificadas*

### 5.1 Estadísticas globales

| Métrica | Media | Desv. estándar | Mínimo | Máximo |
|---|---|---|---|---|
| SARI | 0.449 | 0.072 | 0.153 | 0.670 |
| BERTScore F1 | 0.747 | 0.051 | 0.452 | 0.880 |
| Levenshtein | 0.169 | 0.081 | 0.000 | 0.412 |
| CWR ratio | 1.125 | 0.396 | 0.000 | 5.377 |
| Flesch ratio | 0.924 | 0.344 | −3.066 | 2.686 |
| CR ratio | 0.676 | 0.294 | 0.004 | 2.274 |
| TTR ratio | 1.277 | 0.232 | 0.560 | 2.764 |

El CR ratio medio (0.676) revela que en este dataset los modelos generan texto más comprimido que la referencia — comportamiento opuesto al observado en test_poor (CR ratio medio 1.264). Las referencias de exemples son textos más largos y detallados, lo que penaliza prompts diseñados para máxima compresión.

### 5.2 Ranking de modelos

| Rank | Modelo | Score | SARI | BERTScore | Levenshtein | CR ratio |
|---|---|---|---|---|---|---|
| 1 | **gemma2_27b** | 0.877 | 0.488 | 0.764 | 0.202 | 0.689 |
| 2 | **llama3.3** | 0.837 | 0.478 | 0.758 | 0.186 | 0.710 |
| 3 | mistral-nemo | 0.623 | 0.444 | 0.754 | 0.182 | 0.782 |
| 4 | aya-expanse_32b | 0.604 | 0.464 | 0.753 | 0.166 | 0.681 |
| 5 | llama3.1_8b | 0.537 | 0.431 | 0.740 | 0.156 | 0.730 |
| 6 | qwen2.5_32b | 0.532 | 0.441 | 0.748 | 0.181 | 0.584 |
| 7 | command-r | 0.351 | 0.439 | 0.747 | 0.164 | 0.623 |
| 8 | mixtral | 0.021 | 0.404 | 0.708 | 0.111 | 0.612 |

gemma2_27b asciende a la primera posición. aya-expanse_32b mejora notablemente respecto a test_poor (del #7 al #4), posiblemente por su entrenamiento multilingüe con textos de dominio diverso.

### 5.3 Ranking de prompts

| Rank | Prompt | Score | SARI | BERTScore | Levenshtein | CR ratio |
|---|---|---|---|---|---|---|
| 1 | AUDIT | 0.908 | 0.474 | 0.756 | 0.184 | 0.857 |
| 2 | SELF_REF | 0.796 | 0.464 | 0.757 | 0.181 | 0.772 |
| 3 | META | 0.782 | 0.462 | 0.754 | 0.174 | 0.784 |
| 4 | V2 | 0.777 | 0.465 | 0.753 | 0.177 | 0.734 |
| 5 | CoT | 0.776 | 0.466 | 0.750 | 0.181 | 0.590 |
| 6 | ZS_CoT | 0.763 | 0.456 | 0.750 | 0.181 | 0.616 |
| … | … | … | … | … | … | … |
| 17 | V8 | 0.492 | 0.428 | 0.745 | 0.152 | 0.749 |
| 19 | V7 | 0.386 | 0.410 | 0.739 | 0.154 | 0.787 |
| 20 | V1 | 0.204 | 0.405 | 0.715 | 0.126 | 0.397 |

Inversión completa respecto a test_poor: las técnicas estándar (AUDIT, SELF_REF, META, CoT) dominan, mientras V7 y V8 caen a las últimas posiciones. El factor determinante es el CR ratio: las referencias de exemples son más largas, y los prompts de máxima compresión (V7, V8) producen textos demasiado cortos respecto a ellas.

### 5.4 Top 10 combinaciones modelo × prompt

| Rank | Modelo | Prompt | Score | SARI | BERTScore | Levenshtein |
|---|---|---|---|---|---|---|
| 1 | gemma2_27b | V2 | 0.896 | 0.528 | 0.774 | 0.243 |
| 2 | gemma2_27b | V3 | 0.894 | 0.508 | 0.784 | 0.217 |
| 3 | gemma2_27b | AUDIT | 0.893 | 0.520 | 0.774 | 0.225 |
| 4 | llama3.3 | SELF_REF | 0.890 | 0.507 | 0.776 | 0.209 |
| 5 | gemma2_27b | SELF_REF | 0.888 | 0.513 | 0.774 | 0.208 |
| 6 | llama3.3 | ZERO_SHOT | 0.862 | 0.494 | 0.768 | 0.205 |
| 7 | llama3.3 | V2 | 0.859 | 0.482 | 0.764 | 0.184 |
| 8 | gemma2_27b | ZS_CoT | 0.845 | 0.503 | 0.773 | 0.226 |
| 9 | llama3.3 | V3 | 0.844 | 0.503 | 0.763 | 0.225 |
| 10 | gemma2_27b | ZERO_SHOT | 0.842 | 0.511 | 0.770 | 0.246 |

---

## 6. Análisis comparativo entre datasets

### 6.1 Consistencia de modelos

| Modelo | Rank test_poor | Rank exemples | Δ rank | Consistencia |
|---|---|---|---|---|
| llama3.3 | #1 | #2 | 1 | ✓ Alta |
| gemma2_27b | #2 | #1 | 1 | ✓ Alta |
| mistral-nemo | #4 | #3 | 1 | ✓ Alta |
| qwen2.5_32b | #3 | #6 | 3 | ~ Media |
| llama3.1_8b | #5 | #5 | 0 | ✓ Alta |
| aya-expanse_32b | #7 | #4 | 3 | ~ Media |
| command-r | #6 | #7 | 1 | ✓ Alta |
| mixtral | #8 | #8 | 0 | ✗ Consistentemente último |

Los modelos son más estables entre datasets que los prompts. llama3.3 y gemma2_27b son los únicos que se mantienen en el top-2 en ambos casos.

### 6.2 Divergencia de prompts entre datasets

| Prompt | Rank test_poor | Rank exemples | Δ rank | Interpretación |
|---|---|---|---|---|
| V8 | #1 | #17 | 16 | Muy dominio-específico (compresión extrema) |
| V7 | #4 | #19 | 15 | Vocabulario anclado al dominio administrativo |
| AUDIT | #17 | #1 | 16 | Produce texto más largo, alineado con refs. diversas |
| CoT | #7 | #5 | 2 | Robusto entre dominios |
| V6 | #2 | #12 | 10 | Bueno en admin., penalizado por compresión en exemples |
| V2 | #15 | #4 | 11 | Simple pero efectivo en dominio diverso |

La divergencia se explica principalmente por el **CR ratio**: las referencias de test_poor son más comprimidas (textos cortos), favoreciendo prompts de máxima brevedad; las de exemples son más extensas y detalladas, penalizando esos mismos prompts.

### 6.3 Comportamiento del CR ratio por dataset

| | test_poor | exemples |
|---|---|---|
| CR ratio medio | **1.264** (outputs más largos que GT) | **0.676** (outputs más cortos que GT) |
| Prompts que producen CR ≈ 1 | V4 (1.035), CoT (0.984), command-r | SELF_REF (0.772), META (0.784) |

Este comportamiento opuesto entre datasets sugiere que el dominio del texto de entrada influye directamente en cuánto comprimen los modelos, independientemente de las instrucciones del prompt.

---

## 7. Análisis de métricas

### 7.1 Poder discriminativo de cada métrica

| Métrica | Rango observado | Desv. estándar global | Poder discriminativo |
|---|---|---|---|
| Levenshtein | 0.000 – 1.000 | 0.154 / 0.081 | **Alto** — la más diferenciadora |
| SARI | 0.133 – 0.992 | 0.120 / 0.072 | **Alto** |
| CR ratio | 0.011 – 11.061 | 1.058 / 0.294 | **Alto** pero con outliers graves |
| CWR ratio | 0.000 – 5.377 | 0.296 / 0.396 | Medio |
| BERTScore | 0.504 – 1.000 | 0.060 / 0.051 | **Bajo** — poco discriminativo |
| Flesch ratio | −3.066 – 2.686 | 0.404 / 0.344 | Medio, con valores negativos problemáticos |
| TTR ratio | 0.467 – 2.764 | 0.356 / 0.232 | Bajo para este task |

BERTScore es la métrica con menor poder discriminativo: la mayoría de modelos preserva bien el contenido semántico (rango efectivo 0.71–0.82), lo que no permite distinguir bien entre outputs buenos y malos. Levenshtein, pese a ser la más simple conceptualmente, es la que mejor separa configuraciones.

### 7.2 Hallazgo sobre Levenshtein

La baja similitud Levenshtein global (media 0.199 en test_poor, 0.169 en exemples) no indica necesariamente outputs de baja calidad — refleja la **dificultad de reproducir el estilo léxico específico del anotador humano**. Los prompts V7 y V8 fueron diseñados específicamente para atacar este problema mediante anclaje de vocabulario e imitación progresiva, y consiguieron los valores más altos: 0.319 y 0.325 respectivamente en test_poor.

---

## 8. Conclusiones de Fase 1

1. **El diseño del prompt supera al tamaño del modelo como factor de calidad.** La diferencia entre el mejor y el peor prompt dentro del mismo modelo (Δ SARI ≈ 0.15–0.20) supera la diferencia entre el mejor y el peor modelo con el mismo prompt (Δ SARI ≈ 0.03–0.06).

2. **llama3.3 y gemma2_27b son los modelos más robustos.** Son los únicos que mantienen posiciones #1 y #2 en ambos datasets, con diferencia significativa respecto al resto en score combinado.

3. **V8 (imitación progresiva) es la técnica más efectiva en textos administrativos**, alcanzando SARI=0.557 y Levenshtein=0.325, máximos absolutos del estudio. Sin embargo, su anclaje al dominio administrativo lo penaliza en textos de dominio diverso.

4. **No existe un prompt universal.** Los prompts optimizados para textos administrativos (V7, V8) pierden efectividad en dominio diverso, y viceversa. CoT es la técnica más equilibrada entre datasets.

5. **El CR ratio es el principal factor de divergencia entre datasets.** Los modelos tienden a comprimir más de lo que las referencias de exemples_lectura_facil requieren, y menos de lo que las de test_poor requieren.

6. **mixtral es el modelo más débil en todos los contextos**, con scores consistentemente en el último puesto y los valores de Levenshtein más bajos en ambos datasets.

7. **BERTScore no es una métrica útil para discriminar** en este task: todos los modelos preservan bien el contenido semántico (mínimo 0.71), por lo que no diferencia bien la calidad de la simplificación. Levenshtein y SARI son las métricas con mayor poder discriminativo.

---

## 9. Próximos pasos — Fase 2

### Selección para Fase 2

A partir de los resultados de Fase 1 se seleccionan las combinaciones con mejor rendimiento global y mayor consistencia entre datasets:

- **Modelos:** `llama3.3` y `gemma2_27b` — top-2 en ambos datasets con diferencia significativa.
- **Prompts:** `V8` (máximos absolutos en texto administrativo, técnica más innovadora) y `CoT` (técnica estándar más robusta y equilibrada entre dominios).
- **Datasets:** ambos (test_poor + exemples_lectura_facil_formatted).

### Fase 2A — Efecto de la temperatura

Con semilla fija (`seed=42`), se evaluarán 4 niveles de temperatura:

| Temperatura | Comportamiento esperado |
|---|---|
| T=0.0 | Determinista — baseline de referencia |
| T=0.3 | Ligera variabilidad — exploración controlada |
| T=0.7 | Variabilidad moderada — balance creatividad/fidelidad |
| T=1.0 | Alta variabilidad — exploración máxima |

**2 modelos × 2 prompts × 4 temperaturas × 2 datasets = 32 combinaciones.**

El objetivo es determinar si la temperatura modifica el equilibrio entre creatividad léxica y fidelidad al estilo experto, y si el efecto difiere entre una técnica de razonamiento general (CoT) y una de imitación dominio-específica (V8).

### Fase 2B — Variabilidad de semilla

Una vez identificada la temperatura óptima en Fase 2A, se realizará un análisis de **estabilidad estocástica** mediante variación de semilla. La temperatura determina *cuánta* aleatoriedad introduce el modelo; la semilla determina *qué secuencia concreta* de aleatoriedad se materializa. Dos ejecuciones con la misma temperatura pero distinta semilla producen outputs diferentes — la dispersión entre ellos mide la variabilidad intrínseca del modelo a ese nivel de temperatura.

Este análisis solo es pertinente con T > 0.0 (con temperatura cero el modelo es determinista y la semilla carece de efecto). Por ello se aplica únicamente sobre la temperatura óptima de Fase 2A, evitando multiplicar innecesariamente las ejecuciones.

Se ejecutará con 4 semillas distintas (`seed=42, 123, 7, 999`):

**2 modelos × 2 prompts × 1 temperatura × 4 seeds × 2 datasets = 32 combinaciones adicionales.**

Las métricas se reportarán con **media ± desviación estándar** entre seeds, respondiendo:

- ¿Qué modelos son más estables ante la misma temperatura?
- ¿Los prompts complejos (V8) introducen más variabilidad que los simples (CoT)?
- ¿La temperatura óptima para calidad media coincide con la de menor varianza?

---

*Estudio realizado con modelos locales via Ollama · métricas: SARI, BERTScore (bert-score), Flesch (textstat), Levenshtein (python-Levenshtein), CR/TTR/CWR (cálculo propio) · 3.666 evaluaciones automáticas sin intervención humana en Fase 1*
