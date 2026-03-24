# Architecture Overview

## Original Project (sustain_poi) Analysis

### Flow
1. **Input**: Excel file with POI data (name, category, description, rating, etc.)
2. **Registry**: Looks up pillar configuration (env, test, etc.)
3. **Prompts**: Loads system and user prompts from files
4. **Schema**: Imports Pydantic model for structured output validation
5. **LLM**: Calls LLM with formatted prompt
6. **Parser**: Validates output against Pydantic schema
7. **Output**: Saves to JSONL + Excel

### Key Components

**config/pillars.py** - PILLAR_REGISTRY
```
Maps pillar → {name, system_prompt, user_prompt, schema_module, schema_class}
```

**config/models.py** - MODEL_REGISTRY
```
Maps model_name → {provider, temperature, num_ctx, seed}
```

**schemas/env.py** - Pydantic models
```
Defines strict structure with validation (confidence 0-1, unit types, etc.)
```

**run_pillar.py** - Main processing
```
1. Parse CLI args
2. Load credentials
3. Build chain: prompt → LLM → Pydantic parser
4. Process each row from Excel
5. Write to JSONL
6. Export to Excel
```

---

## New Project (general_processor) - Simplified Version

### Design Principles
- **No Schema**: Works with any LLM output format
- **Task-Based**: Generic registry instead of pillar-specific
- **Flexible**: Support any Excel format with configurable columns
- **Minimal**: Only 3 required fields (number, title, text)

### Flow
1. **Input**: Excel with 3 fields (number, title, text)
2. **Registry**: Looks up task configuration
3. **Prompts**: Loads system and user prompts
4. **No Schema**: Skips validation, accepts raw LLM output
5. **LLM**: Calls LLM with formatted prompt
6. **Output**: Saves to JSONL + Excel (no parsing required)

### Key Components

**config/general_registry.py** - GENERAL_REGISTRY
```
Maps task → {name, system_prompt, user_prompt, output_prefix}
Note: No schema needed!
```

**config/models.py** - MODEL_REGISTRY (same as original)
```
Maps model_name → {provider, temperature, num_ctx, seed}
```

**config/credentials.py** (same as original)
```
Loads API keys from environment
```

**run_general.py** - Main processing
```
1. Parse CLI args
2. Load credentials  
3. Build chain: prompt → LLM (no parser)
4. Process each row from Excel
5. Try to parse JSON, fallback to raw text
6. Write to JSONL
7. Export to Excel
```

---

## Comparison: Original vs New

### Class Diagram

**Original (sustain_poi)**
```
Excel Row
    ↓
[row_to_poi_context] → POI Context Dict
    ↓
Chain:
  - ChatPromptTemplate (system + user)
  - ChatLLM
  - PydanticOutputParser
    ↓
[AssessmentModel] → Validated Pydantic Object
    ↓
JSONL + Excel
```

**New (general_processor)**
```
Excel Row
    ↓
[row_to_context] → Simple Context Dict {number, title, text}
    ↓
Chain:
  - ChatPromptTemplate (system + user)
  - ChatLLM
  (no parser)
    ↓
Raw LLM Output
    ↓
[Try parse JSON / Keep raw]
    ↓
JSONL + Excel
```

---

## Configuration

### How It Works

1. **Task Definition** (`config/general_registry.py`)
   - Maps task name to prompt files
   - No schema class needed

2. **Model Definition** (`config/models.py`)
   - Maps model name to provider + parameters
   - Works for both original and new projects

3. **Credentials** (`config/credentials.py`)
   - Loads API keys from .env
   - Works for both original and new projects

4. **Prompts** (`prompts/`)
   - System prompt: Role + instructions
   - User prompt: Template with `{number}`, `{title}`, `{text}` placeholders

### Adding a New Task

**Step 1: Create prompts**
```
prompts/mytask_system.txt
prompts/mytask_user.txt
```

**Step 2: Register in config/general_registry.py**
```python
"mytask": {
    "name": "mytask",
    "system_prompt": Path("prompts/mytask_system.txt"),
    "user_prompt": Path("prompts/mytask_user.txt"),
    "output_prefix": "mytask",
}
```

**Step 3: Run**
```bash
python run_general.py --excel data/input.xlsx --task mytask --model gpt-4o-mini
```

---

## Provider Support

Both projects support the same providers:

### Ollama (Local/Open-Source)
- Free, runs locally
- Models: llama3, qwen, mistral, deepseek, etc.
- No API key needed

### OpenAI
- Requires OPENAI_API_KEY
- Models: gpt-4o, gpt-4o-mini, etc.
- Best quality for most tasks

### Anthropic
- Requires ANTHROPIC_API_KEY
- Models: claude-3-5-sonnet, claude-3-opus, etc.
- Good for reasoning and safety

### Google
- Requires GOOGLE_API_KEY
- Models: gemini-1.5-pro, gemini-2.0-flash, etc.
- Good balance of price and performance

---

## LLM Building Process

### build_llm() Function

```python
def build_llm(provider, model_name, model_cfg, creds):
    # Provider-specific initialization
    if provider == "ollama":
        return ChatOllama(model=model_name, **extra)
    elif provider == "openai":
        return ChatOpenAI(model=model_name, api_key=..., **extra)
    elif provider == "anthropic":
        return ChatAnthropic(model=model_name, api_key=..., **extra)
    elif provider == "google":
        return ChatGoogleGenerativeAI(model=model_name, api_key=..., **extra)
```

Each provider uses a different LangChain integration but follows the same pattern.

---

## Output Structure

### JSONL Format (Raw Output)
```json
{
  "timestamp": "2025-03-24T10:30:00+00:00",
  "item_id": "1",
  "number": 101,
  "title": "Product A Review",
  "task": "sentiment",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "result": {
    "sentiment": "positive",
    "intensity": 0.95,
    "drivers": ["amazing", "best purchase", "highly recommend"]
  }
}
```

### Excel Export
- One row per item_id (deduped)
- All JSON fields flattened
- Easy to view and share

---

## Why No Schema?

### Original Project Benefits
✓ Type safety and validation
✓ Clear contract between LLM and code
✓ Early error detection

### Original Project Drawbacks
✗ Rigid structure - hard to adapt
✗ Requires schema per task/domain
✗ More boilerplate code
✗ Parse failures stop processing

### New Project Benefits
✓ Flexibility - same LLM for many tasks
✓ Easier to experiment with different prompts
✓ Less code - no schema validation
✓ Graceful degradation - accepts any output

### New Project Drawbacks
✗ Less type safety
✗ Requires more careful prompt engineering
✗ Output structure depends on LLM behavior
✗ Need manual post-processing for some tasks

---

## Use Case Recommendations

### Use Original Project (sustain_poi) When:
- You need strict output validation
- Output structure is complex and well-defined
- Domain-specific evaluation with many criteria
- Data quality is critical

### Use New Project (general_processor) When:
- Quick prototyping and experimentation
- Multiple different tasks on same data
- Simple output structure (text, labels, categories)
- You control the prompt engineering
- You're iterating on task definitions

---

## File-by-File Explanation

### run_general.py

**Key Functions:**
- `utc_now_iso()` - Timestamp for records
- `load_text()` - Read prompt files
- `write_line()` - Append to JSONL
- `safe_name()` - Make folder-safe names
- `build_llm()` - Create LLM instance
- `build_chain()` - Create prompt + LLM chain
- `row_to_context()` - Extract {number, title, text} from Excel
- `process_excel()` - Main processing loop
- `export_jsonl_to_excel()` - Convert results to Excel
- `main()` - CLI argument parsing

**Processing Loop:**
```
For each row in Excel:
  1. Extract context (id, number, title, text)
  2. Invoke chain with context
  3. Get LLM response
  4. Try to parse as JSON
  5. Create output record
  6. Write to JSONL
  7. Handle errors gracefully
```

### config/general_registry.py

Maps task names to prompt configuration:
```python
GENERAL_REGISTRY = {
    "task_name": {
        "name": "task_name",
        "system_prompt": Path("prompts/..."),
        "user_prompt": Path("prompts/..."),
        "output_prefix": "...",
    }
}
```

### config/models.py

Maps model names to LLM configuration:
```python
MODEL_REGISTRY = {
    "model_name": {
        "provider": "openai|ollama|anthropic|google",
        "temperature": 0.0,
        ...provider-specific params...
    }
}
```

### prompts/*.txt

**System Prompt** (`{task}_system.txt`)
- Defines the role
- Provides instructions
- Sets expectations

**User Prompt** (`{task}_user.txt`)
- Template with `{title}` and `{text}` placeholders
- Specific task instructions
- Output format requirements

---

## Scalability

### Batch Processing
```bash
# Process first 100 rows
python run_general.py --excel data/input.xlsx --from-row 0 --to-row 100

# Process next 100
python run_general.py --excel data/input.xlsx --from-row 100 --to-row 200
```

### Multiple Models
```bash
# Test with different models
for model in llama3:8b gpt-4o-mini claude-3-5-sonnet; do
    python run_general.py --excel data/input.xlsx --task sentiment --model $model
done
```

### Results Organization
```
outputs/
  ├── sentiment/
  │   ├── llama3_8b/
  │   ├── gpt-4o-mini/
  │   └── claude-3-5-sonnet/
  ├── classification/
  │   └── ...
  └── extraction/
      └── ...
```

---

## Error Handling

### Graceful Degradation
```python
try:
    response = chain.invoke(context)
    result_json = json.loads(response.content)
except json.JSONDecodeError:
    result_json = {"raw_output": response.content}
except Exception as e:
    write error record to JSONL
    continue to next item
```

Result: Robust processing that completes even with some failures.

---

## Next: Integration Ideas

### Enhanced Monitoring
- Track success/error rates
- Monitor token usage
- Compare model performance

### Post-Processing
- Aggregate results across models
- Validate outputs against rules
- Generate reports

### Workflow Integration
- Chain multiple tasks
- Use task output as input for next task
- Create ETL pipelines

---

## Summary

**General Processor** is a **simplified, flexible version** of the original project:

| Aspect | sustain_poi | general_processor |
|--------|------------|-------------------|
| **Purpose** | Environmental evaluation | General text processing |
| **Schema** | Required (Pydantic) | Optional/none |
| **Registry** | PILLAR_REGISTRY | GENERAL_REGISTRY |
| **Flexibility** | Domain-specific | Multi-purpose |
| **Setup** | More complex | Simpler |
| **Code Reuse** | High | Moderate |

Choose based on your needs for **structure vs. flexibility**.
