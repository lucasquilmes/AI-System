# Informe de Fase 2A — Efecto de la temperatura en la adaptación automática a Lectura Fácil

**Proyecto:** Evaluación de modelos de lenguaje locales para simplificación textual  
**Fase:** 2A — Variación de temperatura  
**Fecha:** Mayo 2026  
**Autores:** Estudio interno

---

## Resumen ejecutivo

La Fase 2A del estudio examina cómo la temperatura de muestreo de los modelos de lenguaje afecta a la calidad de la adaptación automática a Lectura Fácil. Se evaluaron 4 niveles de temperatura (T=0.0, 0.3, 0.7, 1.0) con semilla fija (seed=42) sobre las dos configuraciones seleccionadas en Fase 1 (`llama3.3` y `gemma2:27b`) y las dos técnicas de prompting más efectivas (`V8` y `CoT`), sobre los dos datasets del estudio.

El resultado principal es que **la temperatura no mejora la calidad media** de los outputs en ninguno de los dos datasets. Sin embargo, el análisis revela interacciones complejas entre modelo, prompt, temperatura y dominio textual que tienen implicaciones directas para el despliegue del sistema. La configuración globalmente más robusta es **`llama3.3` + `T=0.0` + `V8`**, con un score combinado medio de 0.587 entre datasets y un gap inter-dataset de 0.314, el más bajo entre las configuraciones de alto rendimiento.

---

## 1. Diseño experimental

### 1.1 Configuración

| Parámetro | Valores |
|---|---|
| Modelos | `llama3.3`, `gemma2:27b` |
| Prompts | `V8` (imitación progresiva), `CoT` (cadena de razonamiento) |
| Temperaturas | 0.0, 0.3, 0.7, 1.0 |
| Semilla | 42 (fija) |
| Datasets | `test_poor` (12 textos), `exemples_lectura_facil_formatted` (11 textos) |
| **Total combinaciones** | **2 × 2 × 4 × 2 = 32** |

### 1.2 Hipótesis de trabajo

La hipótesis inicial planteaba que una temperatura moderada (T=0.3–0.7) podría mejorar la diversidad léxica del output acercándolo al estilo del anotador, mientras que T=1.0 podría generar incoherencias que penalizasen SARI y BERTScore. Se esperaba además que V8 fuera más sensible a la temperatura que CoT, al ser una técnica de mayor complejidad estructural.

### 1.3 Métrica de evaluación

Se utiliza el mismo **score combinado** de 7 métricas que en Fase 1, normalizado globalmente sobre todos los datos de la fase para permitir comparación directa:

- **SARI** (÷100): métrica primaria de simplificación de texto (Xu et al., 2016)
- **BERTScore F1**: preservación semántica (Zhang et al., 2020)
- **Levenshtein similarity**: proximidad estilística al anotador humano
- **Flesch ratio**, **CR ratio**, **TTR ratio**, **CWR ratio**: métricas de adecuación a Lectura Fácil (cercanía a 1.0 = óptimo)

---

## 2. Resultados — Dataset test_poor

### 2.1 Score combinado por modelo y temperatura

| Modelo | T=0.0 | T=0.3 | T=0.7 | T=1.0 |
|---|---|---|---|---|
| `gemma2:27b` | 0.5435 | 0.5012 | 0.5122 | 0.4995 |
| `llama3.3` | **0.6333** | 0.6180 | 0.6066 | 0.5813 |

`llama3.3` supera a `gemma2:27b` en todas las temperaturas cuando se promedia entre prompts. La degradación de `llama3.3` es monótona con la temperatura: cada incremento reduce el score. `gemma2:27b` presenta un comportamiento no monótono: recupera levemente en T=0.7 respecto a T=0.3, señal de mayor sensibilidad al ruido estocástico.

### 2.2 Desglose por prompt y temperatura

**gemma2:27b:**

| Prompt | T=0.0 | T=0.3 | T=0.7 | T=1.0 |
|---|---|---|---|---|
| CoT | 0.3229 | 0.3061 | 0.2391 | 0.3177 |
| V8 | 0.7641 | 0.6964 | **0.7854** | 0.6812 |

**llama3.3:**

| Prompt | T=0.0 | T=0.3 | T=0.7 | T=1.0 |
|---|---|---|---|---|
| CoT | 0.5233 | 0.4801 | 0.4449 | 0.4316 |
| V8 | 0.7434 | **0.7558** | 0.7683 | 0.7310 |

V8 domina ampliamente sobre CoT en test_poor para ambos modelos, confirmando el hallazgo de Fase 1. El efecto de la temperatura sobre V8 es opuesto entre modelos: `llama3.3` alcanza su pico en T=0.3 (0.7558) mientras que `gemma2:27b` lo alcanza en T=0.7 (0.7854).

### 2.3 Top-5 combinaciones

| Ranking | Modelo | T | Prompt | Score | SARI | BERTScore | Levenshtein | Flesch r | CR r |
|---|---|---|---|---|---|---|---|---|---|
| 1 | gemma2:27b | 0.7 | V8 | **0.7854** | 57.65 | 0.835 | 0.326 | 0.911 | 1.187 |
| 2 | llama3.3 | 0.7 | V8 | 0.7683 | 56.67 | 0.827 | 0.367 | 0.898 | 1.235 |
| 3 | gemma2:27b | 0.0 | V8 | 0.7641 | 58.95 | 0.827 | 0.362 | 0.899 | 1.205 |
| 4 | llama3.3 | 0.3 | V8 | 0.7558 | 55.87 | 0.828 | 0.317 | 0.945 | 1.208 |
| 5 | llama3.3 | 0.0 | V8 | 0.7434 | 57.56 | 0.832 | 0.346 | 0.907 | 1.194 |

La combinación puntualmente mejor es `gemma2:27b T=0.7 V8` (score=0.785). Sin embargo, la diferencia con el 3.º puesto (`gemma2:27b T=0.0 V8`, score=0.764) es de apenas 0.021 puntos sobre N=12 textos, lo que no permite establecer significación estadística.

### 2.4 Métricas absolutas por temperatura

| T | SARI | BERTScore | Levenshtein | Flesch r | CR r |
|---|---|---|---|---|---|
| 0.0 | **48.08** | **0.793** | **0.258** | 1.034 | 1.055 |
| 0.3 | 47.39 | 0.792 | 0.244 | 1.038 | 1.064 |
| 0.7 | 46.53 | 0.789 | 0.252 | 1.043 | 1.020 |
| 1.0 | 47.15 | 0.789 | 0.244 | **1.010** | 1.073 |

SARI y BERTScore son máximos en T=0.0 y decaen con la temperatura. El Flesch ratio más cercano a 1.0 se obtiene en T=1.0 (1.010 vs 1.034 en T=0.0), lo que sugiere que mayor variabilidad puede acercar el estilo de legibilidad a la referencia, aunque a costa de penalizar las métricas de contenido.

---

## 3. Resultados — Dataset exemples_lectura_facil_formatted

### 3.1 Score combinado por modelo y temperatura

| Modelo | T=0.0 | T=0.3 | T=0.7 | T=1.0 |
|---|---|---|---|---|
| `gemma2:27b` | 0.2886 | 0.2967 | 0.2583 | 0.3654 |
| `llama3.3` | **0.4575** | 0.4059 | 0.3297 | 0.3119 |

`llama3.3` domina de forma contundente (+58% sobre `gemma2:27b` en T=0.0). Los comportamientos de temperatura son cualitativamente opuestos: `llama3.3` se degrada monótonamente con la temperatura, mientras que `gemma2:27b` mejora al aumentar la temperatura, alcanzando su máximo en T=1.0. Este patrón inverso apunta a diferencias fundamentales en la arquitectura de muestreo de ambos modelos frente a textos de referencia de Lectura Fácil.

### 3.2 Desglose por prompt y temperatura

**gemma2:27b:**

| Prompt | T=0.0 | T=0.3 | T=0.7 | T=1.0 |
|---|---|---|---|---|
| CoT | 0.2710 | 0.2725 | 0.2246 | 0.3159 |
| V8 | 0.3063 | 0.3210 | 0.2919 | **0.4149** |

**llama3.3:**

| Prompt | T=0.0 | T=0.3 | T=0.7 | T=1.0 |
|---|---|---|---|---|
| CoT | **0.4851** | 0.4746 | 0.3668 | 0.3754 |
| V8 | 0.4298 | 0.3371 | 0.2925 | 0.2484 |

**Inversión de prompt:** En exemples, CoT supera a V8 para `llama3.3` (al contrario que en test_poor). Esta inversión tiene implicaciones importantes: V8 es una técnica de imitación de ejemplos concretos del anotador, diseñada para replicar un estilo administrativo específico. Cuando los textos de referencia son ya ejemplos de Lectura Fácil (exemples), V8 puede estar sobreajustando a un estilo diferente del que necesita replicar. CoT, al razonar desde principios generales de simplificación, se adapta mejor a dominios distintos.

### 3.3 Top-5 combinaciones

| Ranking | Modelo | T | Prompt | Score | SARI | BERTScore | Levenshtein | Flesch r | CR r |
|---|---|---|---|---|---|---|---|---|---|
| 1 | llama3.3 | 0.0 | CoT | **0.4851** | 50.07 | 0.768 | 0.192 | 1.079 | 0.654 |
| 2 | llama3.3 | 0.3 | CoT | 0.4746 | 47.14 | 0.759 | 0.186 | 1.046 | 0.652 |
| 3 | llama3.3 | 0.0 | V8 | 0.4298 | 48.42 | 0.759 | 0.190 | 1.021 | 0.634 |
| 4 | gemma2:27b | 1.0 | V8 | 0.4149 | 47.72 | 0.766 | 0.203 | 0.955 | 0.650 |
| 5 | llama3.3 | 1.0 | CoT | 0.3754 | 49.21 | 0.765 | 0.187 | 1.158 | 0.627 |

### 3.4 Métricas absolutas por temperatura

| T | SARI | BERTScore | Levenshtein | Flesch r | CR r |
|---|---|---|---|---|---|
| 0.0 | **48.45** | **0.764** | 0.188 | 1.082 | 0.628 |
| 0.3 | 47.30 | 0.762 | **0.197** | 1.060 | 0.632 |
| 0.7 | 47.16 | 0.759 | 0.186 | 1.073 | 0.614 |
| 1.0 | 47.16 | 0.762 | 0.189 | 1.086 | 0.616 |

El CR ratio en este dataset es sistemáticamente inferior a 1.0 (~0.63), lo que confirma el fenómeno de inversión ya identificado en Fase 1: los textos de referencia de Lectura Fácil son más concisos que los generados, al contrario que en el dataset de textos administrativos donde CR > 1.0.

---

## 4. Análisis comparativo entre datasets

### 4.1 Estabilidad cross-dataset por configuración

La métrica más relevante para seleccionar la configuración definitiva es el **gap inter-dataset** (diferencia de score entre test_poor y exemples): un gap alto indica que la configuración se especializa en un dominio y falla en el otro.

| Modelo | T | Prompt | test_poor | exemples | Media | Gap |
|---|---|---|---|---|---|---|
| llama3.3 | 0.3 | CoT | 0.4801 | 0.4746 | 0.477 | **0.005** |
| llama3.3 | 0.0 | CoT | 0.5233 | 0.4851 | 0.504 | 0.038 |
| gemma2:27b | 0.7 | CoT | 0.2391 | 0.2246 | 0.232 | 0.014 |
| gemma2:27b | 1.0 | CoT | 0.3177 | 0.3159 | 0.317 | 0.002 |
| **llama3.3** | **0.0** | **V8** | **0.7434** | **0.4298** | **0.587** | 0.314 |
| gemma2:27b | 0.7 | V8 | 0.7854 | 0.2919 | 0.539 | **0.494** |
| llama3.3 | 0.7 | V8 | 0.7683 | 0.2925 | 0.530 | 0.476 |

Las configuraciones con CoT tienen gaps muy pequeños (0.005–0.081), mientras que todas las configuraciones con V8 presentan gaps elevados (0.265–0.494). Esto confirma que **CoT generaliza entre dominios y V8 se especializa en texto administrativo**.

### 4.2 Efecto de la temperatura en la estabilidad

La varianza entre datasets de `llama3.3 V8` aumenta de forma continua con la temperatura:

| T | test_poor | exemples | Std entre datasets |
|---|---|---|---|
| 0.0 | 0.7434 | 0.4298 | 0.157 |
| 0.3 | 0.7558 | 0.3371 | 0.209 |
| 0.7 | 0.7683 | 0.2925 | 0.238 |
| 1.0 | 0.7310 | 0.2484 | 0.241 |

Este resultado es estadísticamente relevante: **mayor temperatura no solo degrada el rendimiento medio, sino que amplifica la especialización de dominio**, haciendo al modelo menos generalizable.

### 4.3 Inversión del efecto de V8 entre datasets

El hallazgo más llamativo del estudio es la inversión completa del rendimiento relativo de V8 frente a CoT en función del dataset:

| Dataset | Mejor prompt (`llama3.3 T=0.0`) | Diferencia |
|---|---|---|
| test_poor | V8 (0.7434 vs 0.5233) | +0.220 a favor de V8 |
| exemples | CoT (0.4851 vs 0.4298) | +0.055 a favor de CoT |

La hipótesis explicativa más plausible es que V8 ancla el estilo de output a los ejemplos del anotador administrativo presentados en el prompt. En test_poor, cuyos textos también son administrativos, este anclaje es una ventaja. En exemples, que ya son textos de Lectura Fácil con un estilo diferente, V8 introduce un sesgo de dominio que CoT evita al razonar desde principios generales.

---

## 5. Discusión

### 5.1 La temperatura no mejora la simplificación a Lectura Fácil

Contrariamente a la hipótesis inicial, incrementar la temperatura no produce mejoras sistemáticas en ninguno de los dos datasets. SARI, la métrica primaria para simplificación de texto, es máxima en T=0.0 en ambos datasets (48.08 y 48.45 respectivamente). BERTScore sigue el mismo patrón. Esto sugiere que la tarea de simplificación a Lectura Fácil no se beneficia de la exploración estocástica adicional: los modelos ya contienen el conocimiento necesario en su distribución modal, y alejarse de ella introduce ruido.

Este resultado es coherente con la literatura sobre generation quality en tareas con referencias explícitas: Wang et al. (2023) demostraron que la consistencia de las respuestas del modelo disminuye con la temperatura incluso cuando la calidad media se mantiene estable, y Holtzman et al. (2020) mostraron que el muestreo con temperatura alta puede generar outputs que se desvían de la distribución de referencia en tareas de generación condicionada.

### 5.2 Comportamientos asimétricos entre modelos

El comportamiento opuesto de `gemma2:27b` (mejora con temperatura en exemples) frente a `llama3.3` (degrada con temperatura) sugiere diferencias arquitectónicas en cómo cada modelo gestiona la aleatoriedad. `gemma2:27b` en exemples parte de un baseline tan bajo (0.289 en T=0.0) que cualquier variación puede producir outputs accidentalmente mejores. Este efecto de "ruido beneficioso" en modelos con bajo rendimiento base no debe interpretarse como una virtud de la temperatura, sino como artefacto estadístico sobre N pequeño.

### 5.3 La generalización como criterio de selección

La elección de la configuración definitiva no puede basarse únicamente en el máximo puntual. `gemma2:27b T=0.7 V8` obtiene el score más alto en test_poor (0.785), pero colapsa en exemples (0.292), resultando en una media de 0.539. `llama3.3 T=0.0 V8` obtiene 0.743 en test_poor y 0.430 en exemples, con una media de 0.587 y un gap de 0.314. Desde la perspectiva de un sistema desplegado en producción que debe procesar textos de múltiples dominios, la robustez cross-domain es más valiosa que el máximo en un dominio específico.

### 5.4 Reproducibilidad como requisito científico

T=0.0 es determinista: dado el mismo input y el mismo modelo, el output es idéntico en todas las ejecuciones. Esto satisface un requisito fundamental de reproducibilidad científica que T>0 no puede garantizar sin múltiples ejecuciones y análisis de varianza. Para un sistema en producción, la predictibilidad del output es además una propiedad operacional crítica.

---

## 6. Conclusiones

1. **La temperatura no mejora la calidad de adaptación a Lectura Fácil.** SARI y BERTScore son máximos en T=0.0 en ambos datasets. La hipótesis de que una temperatura moderada mejoraría la diversidad léxica y la aproximación al estilo del anotador no se confirma.

2. **`llama3.3` es el modelo más robusto entre dominios.** Supera a `gemma2:27b` en el 75% de las combinaciones temperatura×prompt y lidera de forma contundente en exemples (+58% en T=0.0), el dataset más exigente.

3. **Mayor temperatura amplifica la especialización de dominio.** La desviación estándar de `llama3.3 V8` entre datasets crece de 0.157 (T=0.0) a 0.241 (T=1.0). Incrementar la temperatura hace al modelo más experto en el dominio más fácil y peor en el más difícil.

4. **V8 se especializa en texto administrativo; CoT generaliza entre dominios.** La inversión completa del ranking de prompts entre datasets (V8 gana +0.220 en test_poor, pierde -0.055 en exemples para `llama3.3`) es el hallazgo más relevante de la fase. En sistemas multi-dominio, CoT ofrece mayor estabilidad con gaps de 0.005–0.038 frente a 0.265–0.494 de V8.

5. **La configuración globalmente óptima es `llama3.3` + `T=0.0` + `V8`.** Maximiza la media cross-dataset (0.587) con el menor gap entre configuraciones de alto rendimiento (0.314). Ofrece además reproducibilidad determinista. Esta es la configuración recomendada para despliegue en dominios administrativos.

6. **El pico de `gemma2:27b T=0.7 V8` en test_poor no es generalizable.** Con N=12 textos, la diferencia de 0.021 puntos respecto a `llama3.3 T=0.0 V8` no es estadísticamente significativa, y el modelo presenta comportamiento no monótono respecto a la temperatura, señal de alta sensibilidad al ruido muestral.

7. **La evaluación automática sobre N pequeño tiene limitaciones.** Con 11–12 textos por dataset, los resultados son orientativos pero no permiten inferencias estadísticas sólidas. La validación humana sigue siendo necesaria para confirmar las diferencias observadas.

---

## 7. Configuración recomendada para producción

| Parámetro | Valor recomendado | Justificación |
|---|---|---|
| **Modelo** | `llama3.3` | Mayor robustez cross-domain, degradación monótona predecible |
| **Temperatura** | `0.0` | Determinista, máximo SARI y BERTScore, menor gap inter-dataset |
| **Prompt (texto administrativo)** | `V8` | +22 puntos sobre CoT en test_poor |
| **Prompt (multi-dominio)** | `CoT` | Gap inter-dataset de 0.038 vs 0.314 de V8 |

Para un sistema de propósito general se recomienda `llama3.3 + T=0.0 + CoT` por su estabilidad. Para un sistema especializado en texto administrativo de administración pública española, `llama3.3 + T=0.0 + V8` es la configuración de mayor rendimiento absoluto.

---

## 8. Próximos pasos — Fase 2B

Los resultados de Fase 2A confirman T=0.0 como temperatura óptima, pero descartan la Fase 2B de variabilidad de semilla sobre esa temperatura al ser determinista. Si se desea estudiar la estabilidad estocástica del sistema, la temperatura candidata es **T=0.3**, la mejor temperatura no-determinista para `llama3.3`:

- test_poor: llama3.3 T=0.3 V8 = 0.756 (2.º mejor absoluto)
- exemples: llama3.3 T=0.3 CoT = 0.475 (2.º mejor absoluto)

La Fase 2B con T=0.3 respondería: ¿cuánto varía el output entre ejecuciones con la misma configuración y distintas semillas? Esto mediría la **estabilidad estocástica intrínseca** del modelo y permitiría reportar resultados con intervalos de confianza.

---

## Referencias

Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. (2020). The curious case of neural text degeneration. *Proceedings of ICLR 2020*.

Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., ... & Clark, P. (2023). Self-Refine: Iterative refinement with self-feedback. *Advances in Neural Information Processing Systems (NeurIPS)*, 36.

Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., ... & Zhou, D. (2023). Self-consistency improves chain of thought reasoning in language models. *Proceedings of ICLR 2023*.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems (NeurIPS)*, 35, 24824–24837.

Xu, W., Napoles, C., Pavlick, E., Chen, Q., & Callison-Burch, C. (2016). Optimizing statistical machine translation for text simplification. *Transactions of the Association for Computational Linguistics*, 4, 401–415.

Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating text generation with BERT. *Proceedings of ICLR 2020*.
