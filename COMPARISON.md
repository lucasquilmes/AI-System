# Comparison: sustain_poi vs general_processor

## Side-by-Side Overview

```
SUSTAIN_POI (Original)          GENERAL_PROCESSOR (New)
═══════════════════════════════════════════════════════════

Purpose: Environmental Eval    Purpose: General Processing
Domain: POI Assessment          Domain: Any Text Task

Registry: PILLAR_REGISTRY       Registry: GENERAL_REGISTRY
├── env                         ├── classification
├── test                        ├── extraction
├── cul, soc, eco               ├── sentiment
    (if implemented)            └── custom

Input: Complex POI Data         Input: Simple 3 Fields
├── poi_id                      ├── number
├── title                       ├── title
├── category                    └── text
├── description
├── rating
├── reviews_count
├── address
├── location
└── ...many more

Output: Structured Schema       Output: Raw LLM Output
├── Pydantic models             ├── Try parse JSON
├── Validated fields            ├── Fallback to text
├── Type-checked                ├── Flexible structure
└── Strict validation           └── No validation

Processing: 3-Step Chain        Processing: 2-Step Chain
├── Prompt                      ├── Prompt
├── LLM                         └── LLM
└── PydanticOutputParser        (no parser)
```

## File Structure Comparison

```
sustain_poi/                    general_processor/
├── run_pillar.py              ├── run_general.py
├── config/                    ├── config/
│   ├── pillars.py             │   ├── general_registry.py
│   ├── models.py              │   ├── models.py
│   └── credentials.py          │   └── credentials.py
├── schemas/                   ├── prompts/
│   ├── env.py                 │   ├── classification_*.txt
│   ├── test.py                │   ├── extraction_*.txt
│   └── ...                    │   ├── sentiment_*.txt
├── prompts/                   │   └── custom_*.txt
│   ├── env_system.txt         ├── data/
│   ├── env_user.txt           │   └── sample_input.xlsx
│   ├── test_system.txt        ├── outputs/
│   └── test_user.txt          ├── requirements.txt
├── data/                      ├── README.md
├── outputs/                   ├── QUICKSTART.md
└── requirements.txt           ├── ARCHITECTURE.md
                               └── PROJECT_SUMMARY.md
```

**Key Difference:** No `schemas/` folder in new project!

## Configuration Comparison

### sustain_poi - pillars.py
```python
PILLAR_REGISTRY = {
    "env": {
        "name": "environmental",
        "system_prompt": Path("prompts/env_system.txt"),
        "user_prompt": Path("prompts/env_user.txt"),
        "schema_module": "schemas.env",           # ← Extra!
        "schema_class": "EnvAssessment",          # ← Extra!
        "output_prefix": "env",
    },
}
```

### general_processor - general_registry.py
```python
GENERAL_REGISTRY = {
    "classification": {
        "name": "classification",
        "system_prompt": Path("prompts/classification_system.txt"),
        "user_prompt": Path("prompts/classification_user.txt"),
        # No schema needed!
        "output_prefix": "classification",
    },
}
```

## Input Data Comparison

### sustain_poi Excel Format
```
poi_id | title       | category | sub_category | description  | rating | reviews_count | address | latitude | longitude | city | country | url
1      | Hotel ABC   | Hotel    | 3-star       | Beautiful... | 4.5    | 123          | Street1 | 1.23    | 2.34     | NYC  | USA     | ...
```

### general_processor Excel Format
```
id | number | title       | text
1  | 101    | Hotel ABC   | This is a beautiful hotel with...
2  | 102    | Museum XYZ  | The museum features...
3  | 103    | Restaurant  | Great food and service...
```

**Much simpler!**

## Output Parsing Comparison

### sustain_poi - With Pydantic Validation
```python
from pydantic import BaseModel, confloat

class EnvWaterCriterion(BaseModel):
    criterion_id: Literal["ENV1"]
    criterion_name: str
    confidence: confloat(ge=0.0, le=1.0)  # type: ignore
    value: confloat(ge=0.0, le=1.0)       # type: ignore
    actual_water_consumption_daily: DailyWaterConsumption
    # ... many more fields

# Processing
chain = prompt | llm | PydanticOutputParser(pydantic_object=EnvAssessment)
result = chain.invoke(context)
# Result is validated EnvAssessment object
```

### general_processor - No Parser
```python
# Processing
chain = prompt | llm
# No parser!

response = chain.invoke(context)
# Try to parse as JSON
try:
    result_json = json.loads(response.content)
except json.JSONDecodeError:
    result_json = {"raw_output": response.content}
```

**Much simpler and more flexible!**

## Command Line Comparison

### sustain_poi
```bash
python run_pillar.py \
  --excel data/poi_master.xlsx \
  --sheet Sheet1 \
  --pillar env              # ← "pillar", not "task"
  --model llama3:8b \
  --id-col poi_id \
  --from-row 0 \
  --to-row 10
```

### general_processor
```bash
python run_general.py \
  --excel data/input.xlsx \
  --sheet Sheet1 \
  --task sentiment          # ← "task", more general
  --model gpt-4o-mini \
  --number-col number \
  --title-col title \
  --text-col text \
  --from-row 0 \
  --to-row 10
```

## Processing Chain Comparison

### sustain_poi - 3-Stage Pipeline
```python
def build_chain(pillar_cfg, model_key, creds):
    # 1. Load schema
    mod = importlib.import_module(pillar_cfg["schema_module"])
    AssessmentModel = getattr(mod, pillar_cfg["schema_class"])
    
    # 2. Create parser
    parser = PydanticOutputParser(pydantic_object=AssessmentModel)
    
    # 3. Build chain: Prompt → LLM → Parser
    chain = prompt | llm | parser
    return chain, AssessmentModel, provider, model_cfg
```

### general_processor - 2-Stage Pipeline
```python
def build_chain(task_cfg, model_key, creds):
    # 1. Build chain: Prompt → LLM
    chain = prompt | llm
    # No parser!
    return chain, provider, model_cfg
```

**Simpler!**

## Error Handling Comparison

### sustain_poi
```python
try:
    response = chain.invoke(context)
    # Response is validated Pydantic object
    output_record = {
        "criteria": response.criteria,
        "score": response.overall_score,
    }
except ValidationError as e:
    # Pydantic validation failed
    error_record = {"validation_error": str(e)}
```

### general_processor
```python
try:
    response = chain.invoke(context)
    
    # Try to parse JSON
    try:
        result_json = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback to raw text
        result_json = {"raw_output": response.content}
    
    output_record = {
        "result": result_json
    }
except Exception as e:
    error_record = {"error": str(e)}
```

**More graceful degradation!**

## Documentation Comparison

### sustain_poi
- `README.md` (if exists)
- Code comments

### general_processor
- `README.md` - Full feature documentation
- `QUICKSTART.md` - Getting started guide
- `ARCHITECTURE.md` - Design patterns & comparison
- `PROJECT_SUMMARY.md` - This summary
- `.env.example` - Template
- Inline code comments

**Much better documented!**

## Use Case Scenarios

### Use sustain_poi When:
✓ You need strict output validation
✓ Output structure is complex & domain-specific
✓ You're building a permanent evaluation system
✓ Data quality is critical
✓ You want guaranteed field structure
✓ You're doing environmental/sustainability assessment

### Use general_processor When:
✓ You're prototyping / experimenting
✓ You want quick iteration
✓ You need simple output (text, labels, categories)
✓ You're handling diverse tasks
✓ You want flexibility in prompt engineering
✓ You need general-purpose text processing
✓ You don't want schema overhead

## Performance Comparison

### sustain_poi
- Slower due to schema validation
- Requires full schema definition
- Better for production (strict contracts)

### general_processor
- Faster (no validation)
- Minimal setup
- Better for R&D and experimentation

## Extensibility Comparison

### Adding a new domain in sustain_poi
```
1. Create schemas/newdomain.py (Pydantic models)
2. Create prompts/newdomain_system.txt
3. Create prompts/newdomain_user.txt
4. Add to config/pillars.py
5. Test thoroughly
```

### Adding a new task in general_processor
```
1. Create prompts/newtask_system.txt
2. Create prompts/newtask_user.txt
3. Add to config/general_registry.py
4. Run immediately
```

**Much easier!**

## Code Size Comparison

### sustain_poi
- `run_pillar.py`: ~544 lines
- `schemas/env.py`: ~74 lines
- Total processing code: 600+ lines

### general_processor
- `run_general.py`: ~544 lines (same length but simpler)
- No schema files
- Easier to understand

## Testing Workflow

### sustain_poi
```
Modify prompt → Update schema if needed → Test → Iterate
```

### general_processor
```
Modify prompt → Test immediately → Iterate
```

**Faster iteration!**

## Feature Matrix

| Feature | sustain_poi | general_processor |
|---------|------------|-------------------|
| Multiple providers | ✓ | ✓ |
| Output validation | ✓ | ✗ |
| Schema required | ✓ | ✗ |
| JSONL output | ✓ | ✓ |
| Excel export | ✓ | ✓ |
| Error handling | Good | Better |
| Task flexibility | Low | High |
| Setup complexity | Medium | Low |
| Documentation | Basic | Comprehensive |
| Multi-provider | ✓ | ✓ |

## Summary: Which One to Use?

**Choose sustain_poi if:**
- You're doing environmental/sustainability assessment
- You need guaranteed output structure
- You have a well-defined domain with complex validation
- You're building a production system
- Data quality must be verified at parse time

**Choose general_processor if:**
- You're doing general text processing
- You want quick prototyping
- You need flexibility and adaptability
- You're experimenting with different tasks
- You want simple, understandable code
- You need to add tasks quickly

**Can use both:**
- sustain_poi for production evaluation
- general_processor for research & experimentation
- They're compatible in the same project!

---

## Migration Path

If you already have a `sustain_poi` workflow and want to simplify:

1. Create `general_processor` directory
2. Copy `config/models.py` and `config/credentials.py`
3. Create simplified `config/general_registry.py`
4. Migrate prompts from `sustain_poi/prompts/`
5. Use `general_processor/run_general.py`
6. Remove schema requirements
7. Adjust Excel input format (3 fields instead of many)

---

Both projects are available and complementary. Use the right tool for the right job!
