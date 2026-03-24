PROJECT COMPLETION SUMMARY
==========================

## ✅ Project Created Successfully

Location: f:\evaluation system\general_processor\

---

## 📁 Complete File Structure

general_processor/
├── .env.example                    # Template for API credentials
├── ARCHITECTURE.md                 # Detailed architecture & comparison
├── QUICKSTART.md                   # Quick start guide with examples
├── README.md                       # Full documentation
├── requirements.txt                # Python dependencies
├── run_general.py                  # Main processing script (544 lines)
│
├── config/                         # Configuration modules
│   ├── __init__.py
│   ├── credentials.py              # Load API keys from .env
│   ├── models.py                   # MODEL_REGISTRY (all LLM configs)
│   └── general_registry.py         # GENERAL_REGISTRY (task configs)
│
├── prompts/                        # Task-specific prompts
│   ├── classification_system.txt   # Classification system prompt
│   ├── classification_user.txt     # Classification user prompt template
│   ├── extraction_system.txt       # Extraction system prompt
│   ├── extraction_user.txt         # Extraction user prompt template
│   ├── sentiment_system.txt        # Sentiment system prompt
│   ├── sentiment_user.txt          # Sentiment user prompt template
│   ├── custom_system.txt           # Generic system prompt
│   └── custom_user.txt             # Generic user prompt template
│
├── data/                           # Input Excel files
│   └── sample_input.xlsx           # Sample data (5 products)
│
└── outputs/                        # Results (auto-created)
    └── {task}/{model}/
        ├── results.jsonl           # Line-by-line results
        └── results.xlsx            # Excel snapshot

---

## 🔑 Key Features

✓ **No Schema Required**
  - Works with raw LLM output
  - No Pydantic models needed
  - Flexible output structure

✓ **Multi-Provider Support**
  - Ollama (local, free)
  - OpenAI
  - Anthropic
  - Google

✓ **Task-Based Registry**
  - Easy to add new tasks
  - Organize by prompt files
  - Name-based task selection

✓ **3-Field Input Format**
  - Number (identifier)
  - Title (name/context)
  - Text (main content for LLM)

✓ **Dual Output**
  - JSONL for processing
  - Excel for analysis/sharing

✓ **Error Handling**
  - Graceful degradation
  - Continues on errors
  - Logs failures to output

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd f:\evaluation system\general_processor
pip install -r requirements.txt
```

### 2. Setup API Keys (if using cloud providers)
```bash
# Copy template
copy .env.example .env

# Edit .env with your API keys
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...
```

### 3. Run Processing
```bash
# With Ollama (local, free)
python run_general.py \
  --excel data/sample_input.xlsx \
  --task sentiment \
  --model llama3:8b

# Or with OpenAI
python run_general.py \
  --excel data/sample_input.xlsx \
  --task sentiment \
  --model gpt-4o-mini
```

### 4. Check Results
```
outputs/sentiment/llama3_8b/
├── results.jsonl      # Raw JSON lines
└── results.xlsx       # Excel snapshot
```

---

## 📊 Excel Input Format

Your Excel file must have these columns (customizable via CLI):

| id | number | title          | text                              |
|----|--------|----------------|-----------------------------------|
| 1  | 101    | Product A      | This product is amazing...        |
| 2  | 102    | Product B      | Good quality but overpriced...    |
| 3  | 103    | Product C      | Terrible experience...            |

Use `--id-col`, `--number-col`, `--title-col`, `--text-col` to customize.

---

## 📚 Available Tasks

Pre-built tasks in GENERAL_REGISTRY:

1. **classification** - Categorize text
2. **extraction** - Extract key information
3. **sentiment** - Analyze sentiment
4. **custom** - Generic analysis

Add more by:
1. Creating prompt files: `prompts/mytask_system.txt` + `mytask_user.txt`
2. Registering in `config/general_registry.py`
3. Running: `python run_general.py --task mytask --model ...`

---

## 🤖 Available Models

See `config/models.py` for all registered models:

**Local (Ollama - free):**
- llama3:8b
- qwen3:8b
- mistral
- deepseek-r1

**OpenAI:**
- gpt-4o-mini (cheapest, good)
- gpt-4o (best quality)

**Anthropic:**
- claude-3-5-sonnet-20241022
- claude-3-opus-20250219

**Google:**
- gemini-1.5-pro
- gemini-2.0-flash

Add new models by editing `config/models.py`.

---

## 📖 Documentation Files

1. **README.md** - Full documentation & examples
2. **QUICKSTART.md** - Quick start guide
3. **ARCHITECTURE.md** - Detailed architecture & comparison with original project
4. **QUICKSTART.md** - Examples and workflows

---

## 🔄 Processing Flow

```
Excel File
    ↓
Parse CLI arguments
    ↓
Load credentials (API keys)
    ↓
Load task config → Load prompts
    ↓
For each row:
  - Extract {id, number, title, text}
  - Build LLM chain
  - Call LLM with formatted prompt
  - Get response
  - Try to parse JSON
  - Write record to JSONL
  - Handle errors gracefully
    ↓
Export JSONL → Excel snapshot
```

---

## ✨ Key Differences from Original Project

| Aspect | sustain_poi | general_processor |
|--------|------------|-------------------|
| **Purpose** | Environmental POI evaluation | General text processing |
| **Registry** | PILLAR_REGISTRY | GENERAL_REGISTRY |
| **Schema** | Required (Pydantic models) | None (raw output) |
| **Input** | POI data (many fields) | 3 fields only |
| **Task Definition** | Pillar-based | Task-based |
| **Complexity** | Higher | Lower |
| **Flexibility** | Domain-specific | Multi-purpose |
| **Setup** | More steps | Fewer steps |

---

## 🛠️ Example Use Cases

### 1. Sentiment Analysis on Product Reviews
```bash
python run_general.py \
  --excel data/reviews.xlsx \
  --task sentiment \
  --model gpt-4o-mini \
  --number-col review_id \
  --title-col product_name \
  --text-col review_text
```

### 2. Content Classification
```bash
python run_general.py \
  --excel data/content.xlsx \
  --task classification \
  --model llama3:8b \
  --number-col content_id \
  --title-col content_title \
  --text-col content_body
```

### 3. Information Extraction
```bash
python run_general.py \
  --excel data/documents.xlsx \
  --task extraction \
  --model claude-3-5-sonnet-20241022 \
  --number-col doc_id \
  --title-col doc_name \
  --text-col doc_content \
  --from-row 0 \
  --to-row 100
```

### 4. Batch Processing with Multiple Models
```bash
# Compare models
for model in llama3:8b gpt-4o-mini claude-3-5-sonnet; do
  python run_general.py \
    --excel data/input.xlsx \
    --task sentiment \
    --model $model
done
```

---

## 🔌 Extending the Project

### Add a New Task

1. **Create prompts:**
   ```bash
   prompts/mytask_system.txt    # System role
   prompts/mytask_user.txt      # User template
   ```

2. **Register in config/general_registry.py:**
   ```python
   "mytask": {
       "name": "mytask",
       "system_prompt": Path("prompts/mytask_system.txt"),
       "user_prompt": Path("prompts/mytask_user.txt"),
       "output_prefix": "mytask",
   }
   ```

3. **Run it:**
   ```bash
   python run_general.py --excel data/input.xlsx --task mytask --model gpt-4o-mini
   ```

### Add a New Model

1. **Register in config/models.py:**
   ```python
   "my-new-model": {
       "provider": "openai",  # or ollama, anthropic, google
       "temperature": 0.0,
       "seed": 42,
   }
   ```

2. **Run it:**
   ```bash
   python run_general.py --excel data/input.xlsx --task sentiment --model my-new-model
   ```

---

## 💡 Tips & Best Practices

1. **Test with Ollama first** - Free, fast iteration, no API costs
2. **Start small** - Process 5-10 rows to test before large batches
3. **Check JSONL first** - Look at raw results before Excel
4. **Version your prompts** - Keep old prompts if you iterate
5. **Compare models** - Run same data through multiple models
6. **Monitor costs** - Track token usage for cloud providers
7. **Batch similar tasks** - Group processing by task/model

---

## 🐛 Troubleshooting

### "Column not found"
- Check Excel column names
- Use `--number-col`, `--title-col`, `--text-col` to specify names

### "Model not found"
- Check `config/models.py`
- Add model if missing

### "Task not found"
- Check `config/general_registry.py`
- Create task if missing

### "API key error"
- Check `.env` file
- Verify API key validity
- Ensure proper formatting

### Ollama models not working
- Start Ollama: `ollama serve`
- Check model is available: `ollama list`

---

## 📝 Output Record Structure

Each line in JSONL:
```json
{
  "timestamp": "2025-03-24T10:30:00+00:00",
  "item_id": "1",
  "number": 101,
  "title": "Product Title",
  "task": "sentiment",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "result": {
    "sentiment": "positive",
    "intensity": 0.95,
    ...
  }
}
```

On error:
```json
{
  "timestamp": "...",
  "item_id": "...",
  "task": "...",
  "model": "...",
  "provider": "...",
  "error": "Error message here"
}
```

---

## 🎓 Learning Resources

- **README.md** - Full feature documentation
- **ARCHITECTURE.md** - Design patterns & comparison
- **QUICKSTART.md** - Hands-on examples
- **Sample data** - data/sample_input.xlsx
- **Prompt files** - prompts/*.txt (easy to understand)

---

## ✅ What's Included

✓ Complete project structure
✓ 4 pre-built tasks (classification, extraction, sentiment, custom)
✓ Support for 4 providers (Ollama, OpenAI, Anthropic, Google)
✓ 10+ pre-registered models
✓ Comprehensive documentation (3 MD files)
✓ Sample Excel file with test data
✓ Error handling & graceful degradation
✓ JSONL + Excel export

---

## 🚀 Next Steps

1. **Install dependencies:** `pip install -r requirements.txt`
2. **Set up API keys:** Copy `.env.example` → `.env` (if using cloud)
3. **Try sample:** `python run_general.py --excel data/sample_input.xlsx --task sentiment --model llama3:8b`
4. **Check results:** Open `outputs/sentiment/llama3_8b/results.xlsx`
5. **Read docs:** README.md for full features
6. **Customize:** Edit prompts and add new tasks

---

## 📞 Support

All documentation is self-contained in the project:
- README.md - Feature guide
- QUICKSTART.md - Getting started
- ARCHITECTURE.md - Design details
- Code comments - Implementation details

---

Generated: March 24, 2026
Project: General Processor
Based on: sustain_poi (simplified & generalized)
