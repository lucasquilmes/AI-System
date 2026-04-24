# Resumen del Trabajo Realizado - General Processor

**Fecha:** 24 de Abril de 2026  
**Usuario:** ITAKA (acceso remoto a Windows 10/11)  
**Proyecto:** General Processor - Framework flexible de procesamiento con LLM

---

## 1. Contexto del Proyecto

**General Processor** es un framework en Python que procesa datos de archivos Excel usando modelos de lenguaje grandes (LLMs) de múltiples proveedores (Ollama local, OpenAI, Anthropic, Google).

### Objetivo Principal
Procesar un archivo Excel con formato específico y generar respuestas en **Lectura Fácil** (estándar de accesibilidad español) usando modelos LLM locales (Ollama).

### Archivo de Entrada
- **Ruta:** `data/Libro1 (version 1).xlsb.xlsx`
- **Hoja:** `Hoja1`
- **Columnas requeridas:**
  - `title`: Título del item
  - `normal text`: Texto principal a procesar
  - `ground truth`: Datos de referencia (se mantienen sin cambios)
  - `output`: Columna de salida (donde se guardan resultados del LLM)
- **Total de filas:** 12 items para procesar

---

## 2. Problemas Iniciales Identificados

### 2.1 Configuración del Sistema
- **Python no estaba en PATH:** Instalador de Windows lo detectó como alias de Microsoft Store
- **Solución:** Instalación manual de Python 3.14.4 desde python.org con agregación a PATH

### 2.2 Mapeo de Columnas
- El script original esperaba columnas genéricas (`title`, `number`, `text`)
- El archivo tenía columnas específicas: `title(normal text)` en el archivo original, luego corregido a `title`
- **Problema:** La columna se llamaba exactamente `title`, no `title(normal text)`
- **Solución:** Investigamos el archivo real y lo alineamos correctamente

### 2.3 Archivo run_general.py Dañado
- Durante las modificaciones, el archivo se corrompió o se perdió
- Python lanzaba error: "can't open file 'D:\\AI-System\\run_general.py': [Errno 2] No such file or directory"
- **Solución:** Recreación completa del archivo con todas las modificaciones integradas

### 2.4 Nombre de Hoja Excel Incorrecto
- Script usaba por defecto "Sheet1", pero la hoja se llamaba "Hoja1"
- **Solución:** Especificar `--sheet Hoja1` en cada comando

---

## 3. Cambios Realizados en el Código

### 3.1 Modificaciones en `run_general.py`

#### a) Validación de Columnas (línea ~175)
```python
required_cols = ["title", "normal text", "ground truth", "output"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(...)
```
- Valida que el Excel tenga las 4 columnas requeridas

#### b) Mapeo de Columnas (línea ~185)
```python
title_col = "title"
text_col = "normal text"
id_col = None
number_col = None
```
- **title** se mapea a `{title}` en el prompt
- **normal text** se mapea a `{text}` en el prompt
- No hay columna de número ni ID personalizado

#### c) Procesamiento de Fila (línea ~215)
```python
df["output"] = df["output"].astype(str)
for i, result in enumerate(results):
    df.at[from_row + i, "output"] = str(result)
```
- Asigna los resultados solo a las filas procesadas
- Mantiene las otras filas sin cambios
- Convierte a string para evitar errores de tipo

#### d) Función `row_to_context` (línea ~120)
```python
def row_to_context(row, item_id, number_col, title_col, text_col):
    number = None
    if number_col and number_col in row:
        try:
            number = int(row.get(number_col)) if row.get(number_col) is not None else None
        except (ValueError, TypeError):
            number = None
    
    return {
        "item_id": item_id,
        "number": number,
        "title": row.get(title_col),
        "text": row.get(text_col),
    }
```
- Maneja el caso donde `number_col` es None
- Nunca causa error si la columna no existe

### 3.2 Modificaciones en `config/models.py`

Se agregaron 7 modelos Ollama disponibles en el PC del usuario:
```python
"llama3.3": {...}
"qwen2.5:32b": {...}
"mixtral": {...}
"gemma2:27b": {...}
"command-r": {...}
"mistral-nemo": {...}
"llama3.1:8b": {...}
```

Cada uno con configuración:
```python
{
    "provider": "ollama",
    "temperature": 0.0,
    "num_ctx": 8192,
    "seed": 42,
}
```

### 3.3 Corrección en `config/general_registry.py`

Se corrigió error de sintaxis en entrada "v0":
```python
"v0": {
    "name": "v0",  # ← Agregada coma
    "system_prompt": Path("prompts/v0_system.txt"),
    "user_prompt": Path("prompts/v0_user.txt"),
    "output_prefix": "v0",
}
```

---

## 4. Instalación de Dependencias

### Comando Ejecutado
```bash
python -m pip install -r requirements.txt
```

### Paquetes Instalados
- **LangChain:** `langchain`, `langchain-core`, `langchain-ollama`, `langchain-openai`, `langchain-anthropic`, `langchain-google-genai`
- **Datos:** `pandas`, `openpyxl`
- **Utilidades:** `python-dotenv`, `pydantic`
- **Librerias de proveedores:** `openai`, `anthropic`, `google-generativeai`

---

## 5. Configuración Final

### Presencia de Modelos
Usuario confirmó con `ollama list` que tiene instalados:
- llama3.3
- qwen2.5:32b
- mixtral
- gemma2:27b
- command-r
- mistral-nemo
- llama3.1:8b

### Directorio de Trabajo
- **Ubicación:** `D:\AI-System`
- **Python:** `C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe`

---

## 6. Flujo de Procesamiento Implementado

### Proceso Paso a Paso

1. **Entrada:** Excel con 12 filas de datos
2. **Lectura:** Pandas lee el Excel y valida columnas
3. **Procesamiento por fila:**
   - Extrae `title` y `normal text`
   - Inyecta en prompt (`{title}` y `{text}`)
   - Llama al LLM (Ollama) con el modelo especificado
   - Recibe respuesta en Lectura Fácil
   - Intenta parsear como JSON, sino guarda como texto
4. **Guardado:**
   - Registra en `results.jsonl` (logs detallados)
   - Actualiza columna `output` en DataFrame original
   - Exporta a `results.xlsx`
5. **Salida:** `outputs/v0/[modelo]/`
   - `results.jsonl` - Registro línea por línea con timestamps
   - `results.xlsx` - Excel completo con columna `output` actualizada

### Datos Preservados
- La columna `ground truth` se mantiene intacta
- Las filas no procesadas conservan su valor original en `output`
- Todas las columnas originales se exportan al Excel final

---

## 7. Comandos para Ejecutar por Modelo

**Ubicación:** Cualquier terminal (Windows PowerShell)  
**Formato:** Rutas absolutas para evitar problemas de PATH

### Template
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model [MODELO] --from-row 0 --to-row 2
```

### Comandos por Modelo

**Llama3.3:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model llama3.3 --from-row 0 --to-row 2
```

**Qwen2.5:32b:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model qwen2.5:32b --from-row 0 --to-row 2
```

**Mixtral:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model mixtral --from-row 0 --to-row 2
```

**Gemma2:27b:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model gemma2:27b --from-row 0 --to-row 2
```

**Command-r:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model command-r --from-row 0 --to-row 2
```

**Mistral-nemo:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model mistral-nemo --from-row 0 --to-row 2
```

**Llama3.1:8b:**
```
C:\Users\ITAKA\AppData\Local\Python\pythoncore-3.14-64\python.exe "D:\AI-System\run_general.py" --excel "data\Libro1 (version 1).xlsb.xlsx" --sheet Hoja1 --task v0 --model llama3.1:8b --from-row 0 --to-row 2
```

### Opciones de Configuración
- `--from-row 0 --to-row 2`: Procesa solo primeras 2 filas (para testing)
- Sin `--to-row`: Procesa todas las filas (12)
- `--sheet Hoja1`: Especifica la hoja del Excel (obligatorio)
- `--task v0`: Tarea a ejecutar (usa prompts de Lectura Fácil)

---

## 8. Estado Actual

✅ **Sistema Operativo:**
- Python 3.14.4 instalado y funcionando
- Todas las dependencias instaladas correctamente
- Variables de entorno configuradas

✅ **Proyecto:**
- `run_general.py` completamente funcional
- `config/models.py` con 7 modelos Ollama registrados
- `config/general_registry.py` correctamente configurado
- Validación de columnas implementada
- Mapeo de datos correcto

✅ **Procesamiento:**
- Primer test exitoso con `llama3.1:8b` (2 filas procesadas)
- Test en progreso con `llama3.3` (normal que tarde 2-5 minutos por fila)
- Resultados se guardan correctamente en `outputs/v0/[modelo]/`

✅ **Salidas:**
- `results.jsonl` - Generado correctamente
- `results.xlsx` - Generado correctamente con columna `output` actualizada

---

## 9. Próximos Pasos Recomendados

1. **Completar pruebas con todos los modelos**
2. **Comparar calidad de respuestas** entre modelos
3. **Analizar velocidad de procesamiento** (algunos modelos serán más rápidos que otros)
4. **Procesar todas las 12 filas** para evaluación final
5. **Documentar hallazgos** sobre qué modelo es mejor para Lectura Fácil

---

## 10. Recursos Generados

### Archivos Modificados
- `run_general.py` - Recreado con todas las funcionalidades
- `config/models.py` - 7 modelos Ollama agregados
- `config/general_registry.py` - Sintaxis corregida

### Archivos de Salida Esperados
- `outputs/v0/llama3.1_8b/results.jsonl` - ✅ Generado
- `outputs/v0/llama3.1_8b/results.xlsx` - ✅ Generado
- `outputs/v0/llama3.3/results.jsonl` - En progreso
- `outputs/v0/llama3.3/results.xlsx` - En progreso
- Similar para cada modelo probado

---

## 11. Documentación del Proyecto

### Archivos de Referencia
- `README.md` - Documentación completa del framework
- `QUICKSTART.md` - Guía de inicio rápido
- `ARCHITECTURE.md` - Detalles técnicos del diseño
- `COMPARISON.md` - Comparación con proyecto original (sustain_poi)

---

## Conclusión

El **General Processor** está completamente funcional y listo para procesar datos con múltiples modelos LLM locales. Se adaptó exitosamente para trabajar con el formato específico del Excel (columnas `title`, `normal text`, `ground truth`, `output`) y se validó el flujo de procesamiento generando respuestas en Lectura Fácil.

**Estado:** ✅ **OPERATIVO Y PROBADO**
