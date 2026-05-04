# v2 Implementation Guide - Comandos de Ejecución

## Resumen de Versiones

| Versión | Objetivo | SARI Esperado | Flesch Esperado | Caso de Uso |
|---------|----------|--------------|-----------------|------------|
| **v0** | Completo + Legible | 50-60 | 40-50 | Estándar: máxima fidelidad + legibilidad basada |
| **v1** | Síntesis Extrema | 20-30 | 70-80 | Experimental: máxima brevedad (pierde contenido) |
| **v2** | Balance Óptimo | 45-55 | 65-75 | **NUEVO: Máxima legibilidad + máxima preservación** |

## Cambios Realizados

### 1. Nuevos Prompts (v2)
- ✅ `prompts/v2_system.txt` – Sistema mejorado con énfasis en preservación
- ✅ `prompts/v2_user.txt` – Instructions alineadas con SARI+Flesch
- ✅ `V2_STRATEGY.md` – Documento técnico completo con explicaciones métricas

### 2. Configuración Actualizada
- ✅ `config/general_registry.py` – Registrada tarea v2
- ✅ `config/models.py` – Actualizado con solo 7 modelos verificados
- ✅ `evaluation/evaluate_excel.py` – Ahora acepta `--version` como parámetro

### 3. Scripts Nuevos
- ✅ `run_all_models.py` – Ejecuta todos los modelos de una versión (requiere `--task`)
- ✅ `pipeline_complete.py` – Pipeline integrado: generación + evaluación

## Comandos de Ejecución

### Opción 1: Generación + Evaluación Integrada (Recomendado)

**Para v0:**
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe pipeline_complete.py --version v0 --from-row 0 --to-row 12
```

**Para v1:**
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe pipeline_complete.py --version v1 --from-row 0 --to-row 12
```

**Para v2:**
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe pipeline_complete.py --version v2 --from-row 0 --to-row 12
```

### Opción 2: Solo Generación (sin Evaluación)

**Para v2:**
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe run_all_models.py --task v2 --from-row 0 --to-row 12
```

### Opción 3: Solo Evaluación (de datos ya generados)

**Para v2:**
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe evaluation/evaluate_excel.py --version v2
```

## Flujo de Ejecución Recomendado

### Paso 1: Generar con v2
```powershell
# Ejecuta todos los 7 modelos con v2
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe run_all_models.py --task v2 --from-row 0 --to-row 12
```

**Genera:**
- `outputs/v2/llama3.1_8b/results.xlsx`
- `outputs/v2/mistral-nemo/results.xlsx`
- `outputs/v2/command-r/results.xlsx`
- `outputs/v2/gemma2_27b/results.xlsx`
- `outputs/v2/mixtral/results.xlsx`
- `outputs/v2/llama3.3/results.xlsx`
- `outputs/v2/qwen2.5_32b/results.xlsx`

### Paso 2: Evaluar con SARI
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe evaluation/evaluate_excel.py --version v2
```

**Genera:**
- `outputs/general/V2_general_results.xlsx` (con dos hojas: "Detalles" y "Resumen_SARI")

### Paso 3: Comparar Resultados

Una vez completadas v0, v1 y v2:
```powershell
# Revisa estas rutas:
outputs/general/V0_general_results.xlsx  # Comparación SARI v0
outputs/general/V1_general_results.xlsx  # Comparación SARI v1
outputs/general/V2_general_results.xlsx  # Comparación SARI v2
```

## Modelos Procesados (7 Total)

1. `llama3.1:8b` → `llama3.1_8b`
2. `mistral-nemo` → `mistral-nemo`
3. `command-r` → `command-r`
4. `gemma2:27b` → `gemma2_27b`
5. `mixtral` → `mixtral`
6. `llama3.3` → `llama3.3`
7. `qwen2.5:32b` → `qwen2.5_32b`

## Parámetros Disponibles

### `run_all_models.py`
```
--task {v0,v1,v2}              Tarea (REQUERIDO)
--from-row INT                 Fila inicial (default: 0)
--to-row INT                   Fila final (default: 12)
--excel FILE                   Archivo Excel (default: data\Test_poor.xlsx)
--sheet NAME                   Hoja Excel (default: Hoja1)
```

### `evaluation/evaluate_excel.py`
```
--version {v0,v1,v2}           Versión a evaluar (default: v0)
--sheet NAME                   Hoja Excel (default: Hoja1)
--col-original NAME            Columna original (default: "normal text")
--col-generado NAME            Columna generada (default: "output")
--col-referencias NAME         Columna referencias (default: "ground truth")
```

### `pipeline_complete.py`
```
--version {v0,v1,v2}           Versión (REQUERIDO)
--from-row INT                 Fila inicial (default: 0)
--to-row INT                   Fila final (default: 12)
--skip-generation              Omitir generación
--skip-evaluation              Omitir evaluación
```

## Métricas de Éxito

### SARI (System for Automatic Rate of Intelligibility)
- **Escala**: 0-100 (100 = perfecto)
- **Qué mide**: Qué tan bien preservas el significado mientras simplificas
- **Interpretación**:
  - 0-20: Muy malo (demasiada pérdida de contenido)
  - 20-40: Malo (mucha síntesis sin sentido)
  - 40-60: Bueno (balance decente)
  - 60-80: Muy bueno (alta preservación + simplificación correcta)
  - 80-100: Excelente (prácticamente perfecto)

### Flesch-Kincaid
- **Escala**: Típicamente 0-100
- **Qué mide**: Legibilidad del texto
- **Interpretación**:
  - 0-30: Muy difícil (universidad)
  - 30-60: Moderado (secundaria)
  - 60-100: Fácil (primaria/popular)

### Objetivos de v2
- **SARI**: 45-55 (balance: preserva semántica, simplifica forma)
- **Flesch**: 65-75 (legible para público general)

## Archivos Clave Modificados

```
d:\AI-System\
├── prompts/
│   ├── v2_system.txt          # NUEVO: Sistema v2
│   ├── v2_user.txt            # NUEVO: Usuario v2
│   ├── v0_system.txt          # (sin cambios)
│   ├── v0_user.txt            # (sin cambios)
│   ├── v1_system.txt          # (sin cambios)
│   └── v1_user.txt            # (sin cambios)
├── config/
│   ├── general_registry.py    # ACTUALIZADO: +v2
│   └── models.py              # ACTUALIZADO: 7 modelos verificados
├── evaluation/
│   └── evaluate_excel.py      # ACTUALIZADO: --version como parámetro
├── run_all_models.py          # (sin cambios desde última vez)
├── pipeline_complete.py       # NUEVO: Integración completa
└── V2_STRATEGY.md             # NUEVO: Documento técnico
```

## Próximos Pasos

1. ✅ Confirmar v2 configurado correctamente
2. ⏳ Ejecutar generación v2 completa
3. ⏳ Ejecutar evaluación SARI v2
4. ⏳ Comparar SARI entre v0, v1, v2
5. ⏳ Analizar resultados y ajustar v2 si es necesario

## Troubleshooting

### Error: "Módulo evaluate no encontrado"
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install evaluate sacrebleu sacremoses
```

### Error: "El archivo Test_poor.xlsx no existe"
Verifica que existe en `data/Test_poor.xlsx` o especifica una ruta diferente:
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe run_all_models.py --task v2 --excel "data\ruta_correcta.xlsx"
```

### Error: "No se encontró results.xlsx en modelo"
Ejecuta primero la generación:
```powershell
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe run_all_models.py --task v2 --from-row 0 --to-row 12
```

## Más Información

Ver [V2_STRATEGY.md](V2_STRATEGY.md) para análisis detallado de por qué v2 aumenta SARI y Flesch.
