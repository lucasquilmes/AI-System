# v2 Prompt: Estrategia para Aumentar SARI y Flesch

## Problema con v0 y v1

### v0: SARI Alto ✓ | Flesch Bajo ✗
- **Ventaja**: Preserva toda la información → SARI alto
- **Problema**: Demasiadas reglas, párrafos aún complejos → Flesch bajo (~40-50)
- **Resultado**: Texto correcto semánticamente pero difícil de leer

### v1: Flesch Alto ✓ | SARI Bajo ✗
- **Ventaja**: Síntesis extrema, frases muy cortas → Flesch alto (~70-80)
- **Problema**: Elimina datos clave, contexto, números específicos → SARI muy bajo (~20-30)
- **Resultado**: Texto legible pero pierde el significado original

### SARI Explicado
La métrica SARI compara 3 elementos:
1. **Texto original**: Versión densa original
2. **Predicción**: Tu simplificación
3. **Referencia**: La simplificación "correcta"

SARI = 0-100, donde mide QUÉ TAN BIEN preservas el significado MIENTRAS simplificas.

**Por qué v1 falla en SARI**: Elimina "Departamentos Ministeriales" → "el Estado" pierde información específica. Las referencias de SARI esperan que digas "el acuerdo entre 3 departamentos" y tú dices "hay un acuerdo". El algoritmo penaliza esa pérdida de contenido.

## Solución v2: Balance Óptimo

### Filosofía de v2
**"Preserva TODOS los hechos clave. Simplifica SOLO el lenguaje"**

### Cambios clave respecto a v1

| Aspecto | v1 | v2 |
|--------|----|----|
| **Síntesis de contenido** | Extrema (elimina detalles) | Conservadora (mantiene datos) |
| **Números** | "muchos" de 1000 | "mil" o "más de 1000" |
| **Organismos** | Agrupa sin especificar | Mantiene nombres clave |
| **Contexto causal** | Puede omitir "porque" | Preserva "porque", "entonces" |
| **Objetivo SARI** | Solo 20-30 | Target 45-60 |

### Cambios clave respecto a v0

| Aspecto | v0 | v2 |
|--------|----|----|
| **Complejidad sintáctica** | Media (aún hay comas) | Muy baja (casi nada de comas) |
| **Puntuación** | Realizada pero compleja | Extremadamente simple |
| **Párrafos** | Siguen estructura tradicional | Saltos de línea agresivos |
| **Flexibilidad de reglas** | Muy ceñido a normas | Pragmático (si hay ambigüedad, repite) |
| **Objetivo Flesch** | 50-60 | Target 65-75 |

## Por Qué Funciona: Análisis Métrico

### SARI aumentará (45-60 esperado)
```
Razón 1: Preservación de contenido
- Si el original dice "3 departamentos" → v2 mantiene "3" (v1 lo cambia a "varios")
- SARI ve menos pérdida de información → Puntuación más alta

Razón 2: Lenguaje simplificado sin perder semántica
- v0: "Los procedimientos administrativos contienen elementos complejos"
- v2: "Los trámites tienen cosas complicadas"
- Ambas conservan el sentido, v2 es más simple → SARI mejora respecto a v1

Razón 3: Mantenimiento de relaciones causales
- Original: "Porque la regla es X, entonces sucede Y"
- v1: podría omitir el "porque" (pierde causalidad)
- v2: mantiene "porque" con palabras simples
- SARI penaliza menos cambios sintácticos cuando semántica se preserva
```

### Flesch aumentará (65-75 esperado)
```
Razón 1: Frases ultra-cortas (como v1, pero manteniendo contenido)
- v0 típico: 12-15 palabras/frase → Flesch ~50
- v2 típico: 7-10 palabras/frase → Flesch ~70+

Razón 2: Vocabulario común (no jerga, incluso si es específico)
- En vez de: "Los organismos autónomos rigen los procesos"
- Escribir: "Los organismos independientes controlan los procesos"
- Flesch ve palabras más simples → Puntuación más alta

Razón 3: Evitar complejidad que v0 puede mantener
- v0 puede usar: "Si bien existen excepciones, generalmente..."
- v2 evita: "Aunque existen excepciones, normalmente..."
- v2 usa: "Hay excepciones. Normalmente sucede esto."
- Cada pausa = Flesch más alto
```

## Cálculos Esperados de Flesch (Español)

Para español, la fórmula Flesch-Kincaid ajustada es aproximadamente:
```
FKG = 0.60 * (palabras/frases) - 0.30 * (sílabas/palabras) - 3.8
```

### v0 estimado
- Palabras/frase: 11
- Sílabas/palabra: 2.5
- FKG ≈ 0.60 * 11 - 0.30 * 2.5 - 3.8 = 6.6 - 0.75 - 3.8 = **2.05 (Muy difícil)**

### v1 estimado
- Palabras/frase: 6
- Sílabas/palabra: 1.8
- FKG ≈ 0.60 * 6 - 0.30 * 1.8 - 3.8 = 3.6 - 0.54 - 3.8 = **-0.74 (Muy fácil pero pierde contenido)**

### v2 objetivo
- Palabras/frase: 8
- Sílabas/palabra: 1.9
- FKG ≈ 0.60 * 8 - 0.30 * 1.9 - 3.8 = 4.8 - 0.57 - 3.8 = **0.43 (Fácil + contenido preservado)**

## Reglas Clave de v2 Alineadas con Métricas

### 1. "Preserva TODOS los hechos principales"
- **Impacto SARI**: Reduce penalización por pérdida de contenido
- **Ejemplo**:
  - ✗ v1: "Hay una ley sobre datos" (pierde números, organismos)
  - ✓ v2: "Hay 1 ley sobre datos. 3 organismos la controlan" (preserva hechos)

### 2. "Simplifica CÓMO se expresa, no QUÉ se expresa"
- **Impacto Flesch**: Frases cortas = Flesch más alto
- **Impacto SARI**: Semántica preservada = SARI no penaliza
- **Ejemplo**:
  - ✗ v0: "Los procedimientos administrativos a los que están sujetos los ciudadanos incluyen"
  - ✓ v2: "El ciudadano sigue estos procedimientos:" (mismo significado, Flesch +20)

### 3. "Usa saltos de línea agresivamente"
- **Impacto Flesch**: Más párrafos cortos = Flesch +10-15
- **Impacto SARI**: No cambia semántica, solo formato = SARI neutral
- **Ejemplo**:
  - v0: "Los desarrolladores pueden usar APIs pero deben respetar límites y no pueden usar datos personales."
  - v2: "Los desarrolladores pueden usar APIs.
            Pero deben respetar límites.
            No pueden usar datos personales."
  - Flesch: +5-10 puntos, SARI sin cambio

### 4. "Si hay ambigüedad, repite en lugar de usar pronombres"
- **Impacto Flesch**: Pequeño (+2-3, porque repetir es más corto que pronombre aclarador)
- **Impacto SARI**: **Crítico** – Repetición preserva referentes claros = SARI ve menos ambigüedad
- **Ejemplo**:
  - ✗ v1: "La ley lo requiere. Esto se publica."
  - ✓ v2: "La ley lo requiere. El resultado se publica."

## Benchmark Esperado

### Comparativa de Métricas
| Métrica | v0 | v1 | v2 |
|---------|-----|-----|-----|
| **SARI** | 50-60 | 20-30 | 45-55 |
| **Flesch** | 40-50 | 70-80 | 65-75 |
| **Balance** | Alto contenido, difícil | Fácil, poco contenido | **Óptimo: fácil + contenido** |

### Interpretación
- **v0**: Semánticamente correcto pero lento de leer
- **v1**: Rápido de leer pero pierde el propósito (simplificar, no transformar)
- **v2**: **Equilibrio: Legible + Significado preservado** ← OBJETIVO

## Instrucciones para Agentes (LLMs)

Cuando proceses un texto con v2:

1. **ANTES de escribir**, identifica:
   - ¿Cuáles son los 5 hechos clave?
   - ¿Qué números/organismos/fechas son críticos?
   
2. **DURANTE la reescritura**:
   - Cada oración = 1 idea máximo
   - Si es más de 8 palabras, divide
   - Cada párrafo = máximo 3 oraciones
   - Luego SALTO DE LÍNEA
   
3. **DESPUÉS de escribir**, verifica:
   - ¿Está toda la información del original? → Sí = SARI potencial 45+
   - ¿Cada frase es < 10 palabras? → Sí = Flesch potencial 65+
   - ¿Hay ambigüedad de pronombres? → Repite nombres

## Conclusión

v2 es la versión que busca el **punto dulce**:
- **No es síntesis** (preserva v0)
- **No es transcripción** (simplifica v0)
- **Es simplificación** (combina lo mejor de v0 y v1)

Resultado esperado: **SARI 45-55 + Flesch 65-75 = Máxima accesibilidad y máxima fidelidad al original**
