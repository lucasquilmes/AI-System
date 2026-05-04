# Prompt para Claude Desktop — Búsqueda de textos para nuevos datasets

Copia y pega el siguiente bloque directamente en Claude Desktop:

---

Estoy construyendo un dataset para un proyecto de investigación universitaria sobre simplificación automática de texto al estándar de **Lectura Fácil** (UNE 153101:2018). Necesito tu ayuda para identificar y recopilar textos originales en español que sirvan como material fuente.

## Qué necesito exactamente

Textos en español redactados en lenguaje administrativo, técnico o formal que sean **reales o realistas**, que provengan de fuentes públicas institucionales (webs gubernamentales, organismos oficiales, portales de atención ciudadana) y que todavía NO estén simplificados. Estos textos serán enviados a un grupo de expertos en accesibilidad cognitiva para que realicen la adaptación humana a Lectura Fácil, creando así pares (texto original, texto simplificado) para entrenar y evaluar modelos de lenguaje.

## Criterios que debe cumplir cada texto

- **Longitud:** entre 60 y 200 palabras por texto (ni demasiado corto ni demasiado largo)
- **Lenguaje:** burocrático, técnico o formal — con subordinadas largas, siglas, términos jurídicos o administrativos
- **Tema:** informativo o procedimental — explica un servicio, un trámite, una norma o una prestación
- **Fuente:** pública y verificable (no opinión, no periodismo, no ficción)
- **Idioma:** español peninsular

## Las 5 temáticas que necesito cubrir

Para cada temática necesito **entre 8 y 12 textos distintos**, variando la dificultad y la fuente dentro de cada bloque.

### 1. Trámites y burocracia
Textos sobre procedimientos administrativos: solicitud de documentos, certificados, registros civiles, empadronamiento, DNI, NIE, herencias, notaría, impuestos (IRPF, IVA), subvenciones, becas, ayudas al alquiler, etc.
Fuentes sugeridas: sede.gob.es, agenciatributaria.gob.es, administracion.gob.es, portales municipales.

### 2. Salud y bienestar
Textos sobre el sistema sanitario público: cómo pedir cita médica, qué es la tarjeta sanitaria, derechos del paciente, prestaciones de la Seguridad Social, incapacidad laboral, pensiones por discapacidad, salud mental, medicamentos genéricos, vacunación, etc.
Fuentes sugeridas: sanidad.gob.es, seg-social.es, imserso.es.

### 3. Consumo y servicios
Textos sobre derechos del consumidor: garantías de productos, reclamaciones, devoluciones, contratos de suministro (luz, agua, gas, internet), cláusulas abusivas, resolución de contratos, servicios financieros básicos, seguros obligatorios, etc.
Fuentes sugeridas: consumo.gob.es, ocu.org (secciones informativas), cnmc.es.

### 4. Entorno urbano y transporte
Textos sobre movilidad y espacio público: cómo usar el transporte público, tarjetas de transporte, bonificaciones, normas de circulación, solicitud de aparcamiento para personas con movilidad reducida, obras en vía pública, licencias de obras menores, gestión de residuos, etc.
Fuentes sugeridas: portales de ayuntamientos (Madrid, Barcelona, Valencia), renfe.com, dgt.es.

### 5. Cultura y ocio
Textos sobre acceso a la cultura y el tiempo libre: cómo inscribirse en actividades municipales, bibliotecas públicas, museos nacionales y sus condiciones de acceso, becas culturales, centros cívicos, programas de ocio para mayores o personas con discapacidad, etc.
Fuentes sugeridas: cultura.gob.es, portales municipales de cultura, museodelprado.es, museoreinasofia.es.

## Formato de entrega que necesito

Para cada texto, entrégamelo en este formato exacto:

```
TEMÁTICA: [nombre del bloque]
FUENTE: [URL o nombre del organismo]
TÍTULO: [título o sección del documento original]
DIFICULTAD ESTIMADA: [baja / media / alta]
TEXTO:
[texto completo sin modificar]
```

## Qué hacer si no encuentras textos reales

Si no tienes acceso a una URL en tiempo real, genera textos **realistas y representativos** del estilo administrativo español para esa temática, indicando claramente `FUENTE: Texto sintético de estilo administrativo`. Los textos sintéticos deben imitar fielmente el registro burocrático real: frases subordinadas largas, nominalizaciones, voz pasiva, siglas sin explicar, remisiones a artículos de ley.

## Ejemplo del nivel de complejidad que busco

Este es un ejemplo del tipo de texto que necesito (nivel medio):

> "La solicitud de reconocimiento de la situación de dependencia deberá presentarse en los servicios sociales del municipio de residencia del solicitante, acompañada de la documentación acreditativa de identidad, informe de salud actualizado y, en su caso, documentación que justifique la representación legal. La resolución, que determinará el grado de dependencia reconocido conforme al baremo establecido en el Real Decreto 174/2011, será notificada en el plazo máximo de seis meses desde la fecha de entrada de la solicitud en el registro."

## Entrega final

Entrega los textos organizados por temática, numerados dentro de cada bloque (T1.1, T1.2... T2.1, T2.2...) y con variedad de dificultad dentro de cada bloque (al menos 3 de nivel alto, 3 de nivel medio y 2 de nivel bajo).
