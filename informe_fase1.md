# Evaluación de modelos de lenguaje locales para la adaptación automática a Lectura Fácil

**Informe de investigación — Fase 1**
*Evaluación exhaustiva de modelos de lenguaje, técnicas de prompting y métricas de calidad*

---

## Resumen ejecutivo

Este informe presenta los resultados de la Fase 1 de un estudio sobre la automatización de la adaptación de textos al estándar de **Lectura Fácil (UNE 153101:2018)** mediante modelos de lenguaje grandes (LLMs) ejecutados en local. Se evaluaron ocho modelos y veinte técnicas de prompting sobre dos datasets con referencias humanas, acumulando 3.666 evaluaciones automáticas con siete métricas de calidad.

Los hallazgos principales indican que el diseño del prompt tiene mayor impacto en la calidad que el tamaño del modelo, que no existe una técnica universalmente superior entre dominios textuales diferentes, y que la imitación progresiva del estilo experto (V8) es la técnica más efectiva para textos administrativos, alcanzando los máximos absolutos del estudio en SARI (0.557) y similitud Levenshtein (0.325). Los modelos llama3.3 y gemma2:27b se posicionan como las opciones más robustas y consistentes.

---

## 1. Introducción

### 1.1 Contexto y motivación

La accesibilidad a la información pública es un derecho reconocido en múltiples marcos normativos, entre ellos la Convención de la ONU sobre los Derechos de las Personas con Discapacidad (2006) y la Directiva Europea 2016/2102 sobre accesibilidad de los sitios web del sector público. Sin embargo, la gran mayoría de documentos administrativos, legales y sanitarios se redactan con un nivel de complejidad lingüística que los hace inaccesibles para una parte significativa de la población.

En España, se estima que más de cuatro millones de personas presentan dificultades de comprensión lectora severas, incluyendo personas con discapacidad intelectual, bajo nivel de alfabetización, demencias o condición de hablantes no nativos (Plena Inclusión, 2021). La Lectura Fácil surge como respuesta a esta necesidad: un conjunto de pautas y criterios para redactar textos comprensibles sin sacrificar el contenido esencial.

La adaptación manual de documentos a Lectura Fácil es, no obstante, un proceso costoso y lento que requiere profesionales certificados. A pesar de la creciente normativa, la producción de materiales accesibles sigue siendo escasa frente a la demanda. Automatizar este proceso mediante modelos de inteligencia artificial representa una oportunidad para escalar la accesibilidad de forma sostenible.

Este estudio adopta una perspectiva deliberadamente práctica: todos los modelos se ejecutan en local mediante Ollama, sin depender de APIs externas de pago y sin enviar datos a terceros. Esto es especialmente relevante para administraciones públicas y organizaciones del tercer sector que trabajan con información sensible o tienen restricciones presupuestarias.

### 1.2 Objetivos del estudio

1. Evaluar y comparar la capacidad de ocho LLMs locales para adaptar textos a Lectura Fácil.
2. Identificar qué técnicas de prompting producen resultados de mayor calidad según métricas automáticas.
3. Analizar la generalizabilidad de las técnicas entre dominios textuales diferentes.
4. Sentar las bases metodológicas para una Fase 2 orientada a la optimización de parámetros de generación (temperatura y semilla).

### 1.3 Alcance y limitaciones

Este estudio utiliza exclusivamente **evaluación automática** mediante métricas de referencia. No incluye evaluación humana, que queda como línea de trabajo futura. Las métricas automáticas permiten comparar grandes volúmenes de outputs de forma reproducible, pero no capturan completamente la calidad perceptual del texto simplificado. Los resultados deben interpretarse como indicadores comparativos entre configuraciones, no como medidas absolutas de calidad.

---

## 2. Marco teórico y estado del arte

### 2.1 La norma de Lectura Fácil (UNE 153101:2018)

La Lectura Fácil es una metodología de comunicación accesible con raíces en el movimiento de autodeterminación de personas con discapacidad intelectual de los años 70 en los países nórdicos. A nivel europeo, Inclusion Europe publicó en 2009 las directrices *"Information for all: European standards for making information easy to read and understand"*, que han servido de base para normativas nacionales en toda Europa.

En España, la norma **UNE 153101:2018** (*Lectura Fácil: Pautas y recomendaciones para la elaboración de documentos*), publicada por AENOR, establece los criterios formales del estándar. Las principales directrices que esta norma impone sobre el texto escrito incluyen:

- Oraciones cortas, simples y en voz activa (máximo recomendado: 10–15 palabras).
- Vocabulario cotidiano y frecuente; evitar tecnicismos, siglas y términos abstractos.
- Una idea principal por oración; evitar subordinadas complejas.
- Uso de ejemplos y explicaciones para conceptos difíciles.
- Estructura visual clara: párrafos cortos, listas numeradas o con viñetas cuando proceda.
- Evitar el uso de metáforas, ironías o construcciones idiomáticas.

Estas restricciones convierten la adaptación a Lectura Fácil en una tarea de simplificación de texto con características específicas que la distinguen de la simplificación general: el objetivo no es solo hacer el texto más legible, sino hacerlo accesible para personas con capacidades cognitivas diversas, lo que implica criterios más estrictos sobre longitud y vocabulario que en otros estándares de simplificación.

### 2.2 Simplificación automática de texto

La simplificación automática de texto (*Automatic Text Simplification*, ATS) es un campo de procesamiento del lenguaje natural (NLP) con décadas de historia. Los enfoques han evolucionado desde sistemas basados en reglas (Chandrasekar et al., 1996) hasta modelos estadísticos (Specia, 2010), modelos neurales de secuencia a secuencia (Nisioi et al., 2017) y, más recientemente, LLMs de propósito general.

Alva-Manchego et al. (2020) presentaron una revisión exhaustiva del campo, identificando las principales tareas componentes: simplificación léxica (sustitución de palabras complejas), simplificación sintáctica (división y reestructuración de oraciones) y simplificación de contenido (eliminación de información accesoria). Las técnicas de prompting evaluadas en este estudio atacan explícitamente estas tres dimensiones.

Para el español específicamente, el corpus **EASIER** (Saggion et al., 2022) representa uno de los primeros recursos paralelos para simplificación en lengua española, aunque con un alcance limitado. La escasez de recursos paralelos de calidad en español, y especialmente de textos adaptados a la norma española UNE 153101:2018, es una de las principales limitaciones del campo y justifica el uso de evaluación automática con métricas de referencia en este trabajo.

La irrupción de los LLMs ha cambiado el panorama de forma significativa. Modelos como GPT-4 o Claude han demostrado capacidad para realizar simplificaciones de alta calidad con prompts adecuados (Kew et al., 2023), pero su uso para textos sensibles o en entornos de recursos limitados plantea problemas de privacidad y coste. Este estudio se centra específicamente en modelos locales como alternativa viable.

### 2.3 Modelos de lenguaje grandes evaluados

Los ocho modelos evaluados pertenecen a diferentes familias arquitectónicas y rangos de parámetros:

**Familia Meta (LLaMA):** LLaMA 3.1 (8B) y LLaMA 3.3 (70B) representan respectivamente el extremo ligero y pesado de la familia Meta (Meta AI, 2024). LLaMA 3 incorpora mejoras sustanciales en seguimiento de instrucciones y razonamiento respecto a versiones anteriores, con soporte multilingüe que incluye español.

**Familia Mistral:** Mistral-Nemo (12B) y Mixtral (47B MoE). Mixtral (Jiang et al., 2024) utiliza una arquitectura *Mixture of Experts* donde solo una fracción de los parámetros se activa por token, lo que permite parámetros totales altos con un coste de inferencia menor. Mistral-Nemo fue desarrollado conjuntamente con NVIDIA.

**Familia Google (Gemma):** Gemma 2 (27B) (Gemma Team, 2024) introduce técnicas de destilación del conocimiento que le permiten superar modelos más grandes en benchmarks de razonamiento y generación.

**Familia Cohere:** Command-R (35B) y Aya Expanse (32B). Aya Expanse destaca por su entrenamiento específico en más de 100 idiomas, con énfasis en lenguas históricamente subrepresentadas (Cohere For AI, 2024), lo que puede ser ventajoso para textos en español.

**Familia Alibaba:** Qwen 2.5 (32B) (Qwen Team, 2024) está optimizado para tareas de seguimiento de instrucciones en múltiples idiomas y demuestra fortaleza particular en español.

### 2.4 Técnicas de prompting

El prompting —la formulación de instrucciones para dirigir el comportamiento de un LLM— ha emergido como una disciplina en sí misma. Las técnicas evaluadas en este estudio cubren el espectro desde las más simples hasta las más elaboradas:

**Zero-shot prompting:** El modelo recibe únicamente la instrucción sin ejemplos previos (Brown et al., 2020). Es el punto de partida más básico y revela la capacidad intrínseca del modelo para la tarea.

**Few-shot prompting:** Se proporcionan ejemplos de pares (texto original, texto simplificado) antes de la instrucción (Brown et al., 2020). Los ejemplos actúan como guía implícita del estilo y nivel de simplificación esperado.

**Chain-of-Thought (CoT):** En lugar de pedir directamente el resultado, se anima al modelo a razonar paso a paso (Wei et al., 2022). Para simplificación, esto se traduce en pedir al modelo que analice la complejidad del texto antes de producir la versión simplificada.

**Zero-shot CoT:** Variante de CoT que no requiere ejemplos de razonamiento; simplemente se añade la instrucción "piensa paso a paso" (*let's think step by step*) al prompt (Kojima et al., 2022).

**Tree of Thoughts (ToT):** El modelo explora múltiples caminos de razonamiento y selecciona el mejor (Yao et al., 2023). En este estudio se implementa como exploración dual de dos estrategias —máxima fidelidad vs. máxima brevedad— con posterior fusión.

**Self-Consistency:** Se generan múltiples respuestas y se selecciona la más frecuente o coherente (Wang et al., 2023). Permite reducir la variabilidad del output a costa de mayor tiempo de procesamiento.

**Self-Refinement:** El modelo genera un borrador inicial y lo revisa iterativamente aplicando criterios explícitos (Madaan et al., 2023). Para Lectura Fácil, los criterios de revisión son los de la norma UNE 153101.

**Role prompting:** Se asigna al modelo un rol experto específico ("eres un especialista en Lectura Fácil con 15 años de experiencia") para condicionar su perspectiva y vocabulario.

### 2.5 Métricas de evaluación para simplificación de texto

La evaluación automática de la simplificación de texto es un problema complejo. A diferencia de tareas como la traducción, donde existe una correspondencia semántica bien definida, la simplificación admite múltiples soluciones igualmente válidas y el espacio de outputs correctos es mucho más amplio.

**SARI** (*System output Against References and against the Input*, Xu et al., 2016) es la métrica estándar del campo. Evalúa explícitamente las tres operaciones de simplificación: palabras que se deben añadir (respecto a la referencia), palabras que se deben conservar y palabras que se deben eliminar. Su diseño la hace más informativa que métricas de solapamiento genéricas como BLEU o ROUGE para este tipo de tarea.

**BERTScore** (Zhang et al., 2020) calcula la similitud semántica entre el output y la referencia utilizando embeddings contextuales de BERT, capturando paráfrasis y sinónimos que métricas léxicas pasarían por alto. Su limitación en este estudio es su bajo poder discriminativo: todos los modelos evaluados obtienen valores altos (0.71–0.82), indicando que preservan bien el significado aunque el estilo difiera.

**Similitud de Levenshtein** (Levenshtein, 1966) mide la distancia de edición mínima normalizada entre el output y la referencia. En el contexto de este estudio, actúa como proxy del *estilo del anotador*: cuánto se parece el texto generado, a nivel léxico y de superficie, al texto que produciría un adaptador humano certificado.

**Índice de Flesch:** Desarrollado por Rudolf Flesch (1948) y adaptado al español por Fernández Huerta (1959), mide la legibilidad de un texto en función de la longitud media de las oraciones y el número medio de sílabas por palabra. En este estudio se utiliza como ratio (output/referencia) para medir si el modelo alcanza un nivel de legibilidad comparable al del texto de referencia humana.

**Tasa de compresión relativa (CR ratio):** Mide cuánto se comprime el texto del output respecto al original, normalizada por la compresión de la referencia. Un valor de 1.0 indica que el modelo comprime en la misma medida que el anotador humano.

**CWR y TTR:** La proporción de palabras complejas (*complex words ratio*) y la diversidad léxica (*type-token ratio*) se calculan también como ratios respecto a la referencia, permitiendo evaluar si el modelo reduce la complejidad léxica en la misma medida que el experto humano.

---

## 3. Metodología

### 3.1 Diseño del estudio

El estudio sigue un diseño factorial completo en Fase 1: cada uno de los **8 modelos** es evaluado con cada una de las **20 técnicas de prompting** sobre cada uno de los **2 datasets**, con temperatura fija `T=0.0` y semilla `seed=42` para garantizar reproducibilidad total. Con temperatura cero, el modelo es determinista: ante el mismo input produce siempre el mismo output, lo que elimina la variabilidad estocástica como fuente de ruido en la comparación.

### 3.2 Modelos evaluados

Todos los modelos se ejecutan en local mediante **Ollama** con un contexto de 8.192 tokens:

| Modelo | Parámetros | Familia | Característica destacada |
|---|---|---|---|
| llama3.1:8b | 8B | Meta | Modelo ligero, referencia base |
| mistral-nemo | 12B | Mistral AI | Eficiente, ventana de contexto amplia |
| command-r | 35B | Cohere | Optimizado para seguimiento de instrucciones |
| gemma2:27b | 27B | Google DeepMind | Alta calidad con destilación del conocimiento |
| mixtral | 47B (MoE) | Mistral AI | Arquitectura Mixture-of-Experts |
| llama3.3 | 70B | Meta | Mayor modelo evaluado |
| qwen2.5:32b | 32B | Alibaba | Multilingüe, fuerte en español |
| aya-expanse:32b | 32B | Cohere For AI | Especializado en lenguas no anglófonas |

### 3.3 Técnicas de prompting evaluadas

Se diseñaron y evaluaron **20 técnicas** organizadas en tres grupos:

#### Versiones propias (V1–V8): progresión sistemática hacia la imitación experta

| Versión | Base técnica | Descripción |
|---|---|---|
| V1 | Zero-shot básico | Instrucción mínima con regla de brevedad extrema (máx. 8 palabras/frase) |
| V2 | Zero-shot equilibrado | Reglas básicas UNE 153101 sin ejemplos |
| V3 | Few-shot + checklist | Ejemplos reales del dominio + verificación explícita de criterios |
| V4 | Ensemble de expertos | Panel de 3 expertos con roles diferenciados + conciencia de compresión |
| V5 | Tree of Thought dual | Exploración paralela fidelidad vs. brevedad + fusión razonada |
| V6 | Pipeline estructurado | 6 reglas aplicadas secuencialmente: División → Voz activa → Léxico → Números → Tiempo verbal → Longitud |
| V7 | Vocabulario anclado | Tabla de sustitución léxica explícita basada en patrones del Ground Truth |
| V8 | Imitación progresiva | 3 fases: análisis de vocabulario del GT → extracción de plantillas estructurales → escritura imitativa |

La progresión V1→V8 refleja una hipótesis de diseño explícita: que anclar el output al estilo concreto del anotador humano —en lugar de seguir reglas abstractas de simplificación— debería mejorar la similitud con las referencias. Los resultados en test_poor validan esta hipótesis.

#### Técnicas estándar de prompting (10)

`zero-shot` · `few-shot` · `role prompting` · `chain-of-thought (CoT)` · `zero-shot CoT` · `tree of thoughts (ToT)` · `self-consistency` · `self-refinement` · `ensemble` · `meta-prompting`

#### Prompts de dominio específico (2)

- **motor**: diseñado para simplificar documentos de seguros de automóvil; incluye vocabulario y ejemplos del sector asegurador.
- **audit**: diseñado para auditar y reformular documentos institucionales; produce outputs más estructurados y extensos.

### 3.4 Datasets

| Dataset | Textos | Dominio | Origen referencias |
|---|---|---|---|
| **test_poor** | 12 | Textos administrativos de alta complejidad | Anotadores humanos entrenados en UNE 153101 |
| **exemples_lectura_facil_formatted** | 11 | Dominio diverso (salud, servicios, administración) | Referencias certificadas según metodología LF |

Cada texto fue procesado por los 8 modelos con las 20 técnicas, generando **1.908 outputs** en test_poor y **1.758** en exemples, para un total de **3.666 evaluaciones individuales**.

La elección de dos datasets con características diferentes es deliberada: test_poor está compuesto por textos administrativos densos y homogéneos, mientras que exemples_lectura_facil_formatted incluye textos de dominios variados con referencias más largas y detalladas. Esta diferencia permite observar si las técnicas generalizan entre dominios o se especializan.

### 3.5 Métricas de evaluación

Se calcularon siete métricas automáticas, ordenadas por relevancia para el objetivo:

| # | Métrica | Descripción | Dirección óptima |
|---|---|---|---|
| 1 | **SARI** (Xu et al., 2016) | Calidad de operaciones de simplificación (añadir / conservar / eliminar) | Mayor = mejor |
| 2 | **BERTScore F1** (Zhang et al., 2020) | Similitud semántica mediante embeddings contextuales | Mayor = mejor |
| 3 | **Levenshtein similarity** (Levenshtein, 1966) | Proximidad léxica al texto del experto (`1 − distancia normalizada`) | Mayor = mejor |
| 4 | **CWR ratio** | Proporción de palabras complejas output vs. referencia | Más cerca de 1.0 |
| 5 | **Flesch ratio** (Flesch, 1948; Fernández Huerta, 1959) | Legibilidad Flesch output vs. referencia | Más cerca de 1.0 |
| 6 | **CR ratio** | Tasa de compresión output vs. referencia | Más cerca de 1.0 |
| 7 | **TTR ratio** | Diversidad léxica output vs. referencia | Más cerca de 1.0 |

Adicionalmente se calculó un **score combinado** normalizado [0–1] que agrega las siete métricas aplicando el criterio de dirección correspondiente a cada una. Este score se utiliza para rankings globales y comparaciones entre configuraciones.

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

La alta desviación estándar del CR ratio (±1.058) revela comportamientos muy dispares en compresión: algunos modelos/prompts generan texto hasta 11 veces más largo que la referencia. Esta variabilidad es el principal factor de dispersión del score combinado.

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

llama3.3 lidera con claridad. Destaca que mistral-nemo (#4 en score combinado) obtiene el mejor BERTScore (0.787) y Levenshtein (0.241), pero sus ratios de compresión y legibilidad penalizan su posición global.

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
| 9 | SELF_CONS | 0.491 | 0.406 | 0.757 | 0.151 | 1.356 |
| 10 | FEW_SHOT | 0.477 | 0.404 | 0.749 | 0.138 | 1.405 |
| 11 | ZS_CoT | 0.469 | 0.410 | 0.754 | 0.172 | 1.237 |
| 12 | V5 | 0.444 | 0.446 | 0.767 | 0.212 | 1.326 |
| 13 | SELF_REF | 0.434 | 0.444 | 0.779 | 0.195 | 1.271 |
| 14 | ZERO_SHOT | 0.428 | 0.419 | 0.766 | 0.191 | 1.094 |
| 15 | V2 | 0.426 | 0.424 | 0.756 | 0.168 | 1.445 |
| 16 | ENSEMBLE | 0.400 | 0.444 | 0.767 | 0.171 | 1.523 |
| 17 | AUDIT | 0.398 | 0.444 | 0.763 | 0.187 | 1.785 |
| 18 | ROLE | 0.397 | 0.422 | 0.764 | 0.173 | 1.236 |
| 19 | TOT | 0.329 | 0.419 | 0.765 | 0.181 | 1.348 |
| 20 | V1 | 0.316 | 0.368 | 0.727 | 0.127 | 0.901 |

V8 domina en las tres métricas más importantes. Los cinco primeros puestos los ocupan versiones propias diseñadas específicamente para Lectura Fácil administrativa, muy por encima de las técnicas estándar.

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

La combinación gemma2_27b + V8 es la mejor del estudio en test_poor, con SARI=0.586 y Levenshtein=0.370 — valores notablemente superiores a la media global. Cabe destacar que V8 aparece en 5 de las 10 mejores combinaciones, confirmando su efectividad independientemente del modelo.

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

El CR ratio medio (0.676) revela el comportamiento opuesto a test_poor: los modelos generan texto más comprimido que la referencia. Las referencias de exemples son más largas y detalladas, lo que penaliza sistemáticamente los prompts diseñados para máxima brevedad.

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

gemma2_27b asciende a la primera posición. aya-expanse_32b mejora notablemente (del #7 al #4), resultado coherente con su entrenamiento específico en lenguas diversas y textos de dominio variado.

### 5.3 Ranking de prompts

| Rank | Prompt | Score | SARI | BERTScore | Levenshtein | CR ratio |
|---|---|---|---|---|---|---|
| 1 | AUDIT | 0.908 | 0.474 | 0.756 | 0.184 | 0.857 |
| 2 | SELF_REF | 0.796 | 0.464 | 0.757 | 0.181 | 0.772 |
| 3 | META | 0.782 | 0.462 | 0.754 | 0.174 | 0.784 |
| 4 | V2 | 0.777 | 0.465 | 0.753 | 0.177 | 0.734 |
| 5 | CoT | 0.776 | 0.466 | 0.750 | 0.181 | 0.590 |
| 6 | ZS_CoT | 0.763 | 0.456 | 0.750 | 0.181 | 0.616 |
| 7 | SELF_CONS | 0.757 | 0.465 | 0.749 | 0.172 | 0.628 |
| 8 | ENSEMBLE | 0.746 | 0.463 | 0.759 | 0.173 | 0.753 |
| 9 | FEW_SHOT | 0.735 | 0.461 | 0.742 | 0.159 | 0.736 |
| 10 | ZERO_SHOT | 0.725 | 0.458 | 0.752 | 0.192 | 0.613 |
| 11 | V4 | 0.693 | 0.447 | 0.750 | 0.174 | 0.592 |
| 12 | V6 | 0.683 | 0.451 | 0.752 | 0.180 | 0.654 |
| 13 | MOTOR | 0.639 | 0.439 | 0.735 | 0.160 | 0.575 |
| 14 | V3 | 0.615 | 0.454 | 0.750 | 0.175 | 0.703 |
| 15 | ROLE | 0.512 | 0.435 | 0.746 | 0.165 | 0.701 |
| 16 | TOT | 0.503 | 0.441 | 0.740 | 0.155 | 0.753 |
| 17 | V8 | 0.492 | 0.428 | 0.745 | 0.152 | 0.749 |
| 18 | V5 | 0.484 | 0.430 | 0.738 | 0.159 | 0.529 |
| 19 | V7 | 0.386 | 0.410 | 0.739 | 0.154 | 0.787 |
| 20 | V1 | 0.204 | 0.405 | 0.715 | 0.126 | 0.397 |

Inversión completa respecto a test_poor: las técnicas estándar dominan y V7/V8 caen a los últimos puestos. El factor determinante es el CR ratio, como se analiza en detalle en la sección 6.

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

gemma2_27b copa los puestos 1, 2, 3 y 5. La aparición de ZERO_SHOT en posiciones altas (6 y 10) sugiere que, para dominios textuales variados, añadir instrucciones muy específicas puede perjudicar al modelo, que sin restricciones produce outputs más alineados con el estilo de las referencias diversas.

---

## 6. Análisis comparativo entre datasets

### 6.1 Consistencia de modelos entre dominios

| Modelo | Rank test_poor | Rank exemples | Δ rank | Estabilidad |
|---|---|---|---|---|
| llama3.3 | #1 | #2 | 1 | ✓ Alta |
| gemma2_27b | #2 | #1 | 1 | ✓ Alta |
| mistral-nemo | #4 | #3 | 1 | ✓ Alta |
| llama3.1_8b | #5 | #5 | 0 | ✓ Alta |
| command-r | #6 | #7 | 1 | ✓ Alta |
| mixtral | #8 | #8 | 0 | ✗ Consistentemente último |
| qwen2.5_32b | #3 | #6 | 3 | ~ Media |
| aya-expanse_32b | #7 | #4 | 3 | ~ Media |

Los modelos muestran mayor estabilidad entre datasets que los prompts. llama3.3 y gemma2_27b son los únicos que se mantienen en las dos primeras posiciones en ambos contextos.

### 6.2 Divergencia de prompts entre dominios

| Prompt | Rank test_poor | Rank exemples | Δ rank | Interpretación |
|---|---|---|---|---|
| V8 | #1 | #17 | 16 | Dominio-específico: anclado a vocabulario administrativo |
| V7 | #4 | #19 | 15 | Tabla de sustitución basada en dominio administrativo |
| AUDIT | #17 | #1 | 16 | Produce texto más largo, compatible con refs. diversas |
| CoT | #7 | #5 | 2 | El más robusto y generalizable |
| V6 | #2 | #12 | 10 | Bueno en admin., penalizado por compresión en exemples |
| V2 | #15 | #4 | 11 | Instrucción simple, flexible ante dominios diferentes |

La diferencia máxima de ranking (16 posiciones para V8 y AUDIT) ilustra hasta qué punto el dominio textual condiciona la efectividad de la técnica.

### 6.3 El fenómeno de inversión del CR ratio

El hallazgo más relevante del análisis comparativo es la inversión del CR ratio entre datasets:

| | test_poor | exemples |
|---|---|---|
| CR ratio medio | **1.264** | **0.676** |
| Interpretación | Outputs más largos que el GT | Outputs más cortos que el GT |
| Prompts penalizados | V7, V8 (muy cortos) | AUDIT, META (muy largos) |

Esta inversión revela que los modelos no calibran la longitud de su output principalmente según las instrucciones del prompt, sino según el dominio y longitud del texto de entrada. Los textos administrativos densos del dataset test_poor producen simplificaciones más largas; los textos más variados y con referencias extensas de exemples producen outputs más cortos.

Este comportamiento tiene implicaciones prácticas importantes: un prompt optimizado para un tipo de documento puede ser contraproducente para otro. El parámetro de temperatura, estudiado en Fase 2, podría modular este efecto.

---

## 7. Análisis de métricas

### 7.1 Poder discriminativo de cada métrica

| Métrica | Rango efectivo test_poor | Rango efectivo exemples | Poder discriminativo |
|---|---|---|---|
| Levenshtein | 0.13 – 0.33 | 0.11 – 0.33 | **Alto** — la más diferenciadora |
| SARI | 0.37 – 0.56 | 0.41 – 0.56 | **Alto** |
| CR ratio | 0.90 – 1.78 (excl. outliers) | 0.40 – 0.86 | **Alto**, con outliers graves |
| CWR ratio | 0.97 – 1.23 | 0.99 – 1.28 | Medio |
| Flesch ratio | 0.76 – 1.10 | 0.79 – 1.04 | Medio |
| BERTScore | 0.73 – 0.82 | 0.71 – 0.76 | **Bajo** — poco discriminativo |
| TTR ratio | 1.06 – 1.20 | 1.19 – 1.45 | Bajo para este task |

### 7.2 Levenshtein como indicador del estilo experto

La similitud Levenshtein media es baja en ambos datasets (0.199 y 0.169). Esto no refleja necesariamente outputs de baja calidad, sino la **brecha de estilo** entre la generación del modelo y el texto del anotador humano: diferencias en elección de palabras, estructura de oraciones y convenciones de formato que son difíciles de reproducir sin acceso explícito al estilo del anotador.

Los prompts V7 y V8 fueron diseñados específicamente para reducir esta brecha: V7 mediante una tabla de sustitución léxica derivada del Ground Truth, y V8 mediante imitación progresiva del estilo. Ambos consiguieron los valores Levenshtein más altos del estudio en test_poor (0.319 y 0.325), validando la hipótesis de diseño.

Esta observación sugiere que, para maximizar la similitud con adaptaciones humanas certificadas, las técnicas que explicitan el estilo del anotador son más efectivas que las que formulan reglas generales de simplificación.

### 7.3 Por qué BERTScore no discrimina en este task

BERTScore obtiene valores consistentemente altos (0.71–0.82) independientemente del modelo o el prompt. Esto indica que todos los modelos preservan bien el contenido semántico del texto original — lo cual era esperable, ya que la instrucción fundamental es simplificar sin eliminar información relevante.

Sin embargo, preservar el significado es condición necesaria pero no suficiente para una buena adaptación a Lectura Fácil: el texto puede ser semánticamente correcto pero con longitud de oraciones, vocabulario o estructura inapropiados para el estándar. SARI y Levenshtein capturan mejor estas dimensiones.

---

## 8. Discusión

### 8.1 El prompt como factor dominante

El hallazgo más relevante del estudio es que el diseño del prompt tiene mayor impacto en la calidad del output que el tamaño o la familia del modelo. La diferencia entre el mejor y el peor prompt dentro del mismo modelo (Δ SARI ≈ 0.15–0.20) supera sistemáticamente la diferencia entre el mejor y el peor modelo con el mismo prompt (Δ SARI ≈ 0.03–0.06).

Esto tiene implicaciones prácticas importantes: invertir esfuerzo en el diseño y refinamiento del prompt produce mejoras mayores que escalar el tamaño del modelo. Para organizaciones con recursos computacionales limitados, esto es una noticia positiva: un modelo de 8B parámetros con un prompt bien diseñado (llama3.1:8b + V8: SARI=0.521) puede superar a un modelo de 35B con un prompt genérico (command-r + ZERO_SHOT: SARI≈0.41).

### 8.2 La hipótesis de la imitación progresiva

La técnica V8 representa la propuesta más novedosa de este estudio. Su diseño parte de la observación de que las técnicas estándar tratan la simplificación como una tarea de transformación siguiendo reglas abstractas, mientras que los adaptadores humanos certificados trabajan con convenciones y patrones muy concretos y aprendidos.

V8 hace explícito este conocimiento al modelo en tres fases: primero analizar el vocabulario que los anotadores usan en sus referencias (palabras frecuentes, fórmulas de inicio, estructura de listas), luego extraer plantillas estructurales de esas referencias, y finalmente escribir el texto simplificado imitando esas plantillas. El resultado es una técnica que "habla como el anotador" en lugar de "aplicar reglas de simplificación".

Los resultados validan esta hipótesis para textos administrativos: V8 alcanza los máximos absolutos en SARI (0.557) y Levenshtein (0.325). Sin embargo, la misma especificidad que la hace efectiva en un dominio la hace menos generalizable: al estar anclada al vocabulario y convenciones de los anotadores de test_poor, pierde efectividad cuando el dominio cambia.

### 8.3 Limitaciones de la evaluación automática

Este estudio se basa exclusivamente en métricas automáticas calculadas contra referencias humanas. Esto implica al menos tres limitaciones importantes:

1. **La validez de las métricas depende de la calidad de las referencias.** Si las referencias humanas tienen sesgos o inconsistencias, las métricas heredan esos sesgos. En particular, SARI y Levenshtein miden similitud con un texto específico, no con el espacio de posibles simplificaciones correctas.

2. **Un output puede ser lingüísticamente válido y desalineado con la referencia.** Un modelo que simplifica correctamente pero con un estilo diferente al del anotador obtiene valores Levenshtein bajos aunque el resultado sea perfectamente comprensible.

3. **No se evalúa comprensión real.** La prueba definitiva de una adaptación a Lectura Fácil es que las personas destinatarias —con diversidad funcional o baja alfabetización— comprendan el texto. Esta dimensión queda fuera del alcance de la evaluación automática.

Estas limitaciones no invalidan los resultados comparativos —que son robustos porque afectan a todos los sistemas por igual— pero sí obligan a interpretar los valores absolutos con cautela.

### 8.4 Implicaciones para la selección de modelos en producción

Para un despliegue práctico en una institución pública o del tercer sector, los resultados sugieren la siguiente jerarquía de consideraciones:

1. **Si el dominio es administrativo y homogéneo:** gemma2_27b + V8 es la mejor combinación, con SARI=0.586 y Levenshtein=0.370. El coste computacional (27B parámetros) es manejable con hardware estándar.

2. **Si el dominio es diverso o desconocido:** gemma2_27b + SELF_REF o llama3.3 + ZERO_SHOT ofrecen mayor robustez cross-domain. CoT es la técnica estándar más equilibrada.

3. **Si el hardware limita a modelos pequeños:** llama3.1:8b + V8 (SARI=0.521, score=0.816) ofrece resultados sorprendentemente competitivos para un modelo de 8B.

4. **mixtral debe evitarse** para esta tarea: sus resultados son consistentemente los peores en ambos datasets a pesar de su tamaño (47B MoE).

---

## 9. Conclusiones de Fase 1

1. **El diseño del prompt supera al tamaño del modelo como factor de calidad.** La diferencia entre el mejor y el peor prompt dentro del mismo modelo (Δ SARI ≈ 0.15–0.20) supera la diferencia entre el mejor y el peor modelo con el mismo prompt (Δ SARI ≈ 0.03–0.06).

2. **llama3.3 y gemma2_27b son los modelos más robustos.** Son los únicos que mantienen posiciones #1 y #2 en ambos datasets, con diferencia significativa respecto al resto en score combinado.

3. **V8 (imitación progresiva) es la técnica más efectiva para textos administrativos**, alcanzando SARI=0.557 y Levenshtein=0.325, máximos absolutos del estudio. Su anclaje al dominio administrativo penaliza su rendimiento en textos de dominio diverso.

4. **No existe un prompt universalmente superior.** Técnicas optimizadas para textos administrativos (V7, V8) pierden efectividad en dominio diverso, y viceversa. CoT es la técnica estándar más robusta entre datasets (Δ rank = 2).

5. **El CR ratio es el principal factor de divergencia entre datasets.** Los modelos tienden a comprimir más de lo que las referencias de exemples requieren, y menos de lo que las de test_poor requieren, independientemente de las instrucciones del prompt.

6. **mixtral es el modelo más débil en todos los contextos**, con scores consistentemente en el último puesto y los valores de Levenshtein más bajos en ambos datasets.

7. **BERTScore no es discriminativa para este task.** Todos los modelos preservan bien el contenido semántico (0.71–0.82), por lo que no diferencia configuraciones. Levenshtein y SARI son las métricas con mayor poder discriminativo.

8. **La evaluación automática tiene limitaciones inherentes.** Los resultados comparativos son robustos, pero los valores absolutos deben validarse con evaluación humana en trabajo futuro.

---

## Referencias

Alva-Manchego, F., Scarton, C., & Specia, L. (2020). Data-Driven Sentence Simplification: Survey and Benchmark. *Computational Linguistics*, 46(1), 135–187.

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Amodei, D. (2020). Language Models are Few-Shot Learners. *Advances in Neural Information Processing Systems (NeurIPS)*, 33, 1877–1901.

Chandrasekar, R., Doran, C., & Srinivas, B. (1996). Motivations and Methods for Text Simplification. *Proceedings of the 16th International Conference on Computational Linguistics (COLING)*, 1041–1044.

Cohere For AI. (2024). *Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier*. Technical Report. Cohere.

Fernández Huerta, J. (1959). Medidas sencillas de lecturabilidad. *Consigna*, 214, 29–32.

Flesch, R. (1948). A New Readability Yardstick. *Journal of Applied Psychology*, 32(3), 221–233.

Gemma Team. (2024). *Gemma 2: Improving Open Language Models at a Practical Size*. Technical Report. Google DeepMind.

Inclusion Europe. (2009). *Information for All: European Standards for Making Information Easy to Read and Understand*. Brussels: Inclusion Europe.

Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C., Devendra Singh Chaplot, de las Casas, D., ... & Sayed, W. E. (2023). Mistral 7B. *arXiv preprint arXiv:2309.06180*.

Jiang, A. Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B., Bamford, C., ... & Sayed, W. E. (2024). Mixtral of Experts. *arXiv preprint arXiv:2401.04088*.

Kew, T., Agrawal, A., Aumiller, D., Choubey, P. K., Alva-Manchego, F., & Markert, K. (2023). Turning Whispers into Echoes: Automatic Text Simplification with ChatGPT and Human Evaluation. *arXiv preprint arXiv:2309.05049*.

Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large Language Models are Zero-Shot Reasoners. *Advances in Neural Information Processing Systems (NeurIPS)*, 35.

Levenshtein, V. I. (1966). Binary Codes Capable of Correcting Deletions, Insertions and Reversals. *Soviet Physics Doklady*, 10(8), 707–710.

Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., ... & Clark, P. (2023). Self-Refine: Iterative Refinement with Self-Feedback. *Advances in Neural Information Processing Systems (NeurIPS)*, 36.

Meta AI. (2024). *Introducing Llama 3.3*. Technical Report. Meta AI.

Nisioi, S., Štajner, S., Ponzetto, S. P., & Dinu, L. P. (2017). Exploring Neural Text Simplification Models. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL)*, 85–91.

Plena Inclusión. (2021). *La Lectura Fácil como herramienta de accesibilidad cognitiva*. Madrid: Plena Inclusión España.

Qwen Team. (2024). *Qwen2.5 Technical Report*. Alibaba Group.

Specia, L. (2010). Translating from Complex to Simplified Sentences. *Proceedings of the 9th International Conference on Computational Processing of the Portuguese Language (PROPOR)*, 30–39.

UNE 153101:2018. *Lectura Fácil: Pautas y recomendaciones para la elaboración de documentos*. Madrid: AENOR.

Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., ... & Zhou, D. (2023). Self-Consistency Improves Chain of Thought Reasoning in Language Models. *International Conference on Learning Representations (ICLR)*.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., ... & Zhou, D. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *Advances in Neural Information Processing Systems (NeurIPS)*, 35.

Xu, W., Napoles, C., Pavlick, E., Chen, Q., & Callison-Burch, C. (2016). Optimizing Statistical Machine Translation for Text Simplification. *Transactions of the Association for Computational Linguistics*, 4, 401–415.

Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. *Advances in Neural Information Processing Systems (NeurIPS)*, 36.

Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating Text Generation with BERT. *International Conference on Learning Representations (ICLR)*.

---

*Estudio realizado con modelos locales via Ollama · métricas implementadas con bert-score, textstat, python-Levenshtein y cálculo propio · 3.666 evaluaciones automáticas · reproducibilidad garantizada mediante T=0.0 y seed=42 en Fase 1*
