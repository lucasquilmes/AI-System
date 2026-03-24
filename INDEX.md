📦 GENERAL PROCESSOR - PROJECT COMPLETE

Location: f:\evaluation system\general_processor\

═══════════════════════════════════════════════════════════════════════════════

📚 PROJECT DOCUMENTATION (Start Here)

   ✓ PROJECT_SUMMARY.md         ← START HERE: Complete overview
   ✓ README.md                  ← Full feature documentation
   ✓ QUICKSTART.md              ← Quick start with examples
   ✓ ARCHITECTURE.md            ← Design & comparison with original
   ✓ COMPARISON.md              ← sustain_poi vs general_processor
   ✓ CHECKLIST.md               ← Setup & testing checklist

═══════════════════════════════════════════════════════════════════════════════

🚀 CORE FILES

   run_general.py               ← Main processing script (544 lines)
   requirements.txt             ← Python dependencies
   .env.example                 ← API key template

═══════════════════════════════════════════════════════════════════════════════

⚙️ CONFIGURATION (Customize Here)

   config/
   ├── __init__.py
   ├── credentials.py           ← Load API keys from .env
   ├── models.py                ← MODEL_REGISTRY (10+ models)
   └── general_registry.py      ← GENERAL_REGISTRY (4 tasks)

═══════════════════════════════════════════════════════════════════════════════

💬 PROMPTS (Customize Tasks)

   prompts/
   ├── classification_system.txt    ← Classification system prompt
   ├── classification_user.txt      ← Classification user template
   ├── extraction_system.txt        ← Information extraction
   ├── extraction_user.txt
   ├── sentiment_system.txt         ← Sentiment analysis
   ├── sentiment_user.txt
   ├── custom_system.txt            ← Generic task
   └── custom_user.txt

═══════════════════════════════════════════════════════════════════════════════

📊 DATA & OUTPUT

   data/
   └── sample_input.xlsx        ← Sample 5-row test data

   outputs/                     ← Auto-created results
   └── {task}/{model}/
       ├── results.jsonl        ← Line-by-line results
       └── results.xlsx         ← Excel snapshot

═══════════════════════════════════════════════════════════════════════════════

🎯 QUICK START (3 Steps)

   1. pip install -r requirements.txt
   
   2. python run_general.py \
        --excel data/sample_input.xlsx \
        --task sentiment \
        --model llama3:8b
   
   3. Open: outputs/sentiment/llama3_8b/results.xlsx

═══════════════════════════════════════════════════════════════════════════════

✨ KEY FEATURES

   ✓ No schema required         - Simple & flexible
   ✓ Multi-provider support    - Ollama, OpenAI, Anthropic, Google
   ✓ Task-based registry       - Easy to add new tasks
   ✓ 3-field input format      - number, title, text
   ✓ Dual output format        - JSONL + Excel
   ✓ Error handling            - Graceful degradation
   ✓ Comprehensive docs        - 6 markdown files

═══════════════════════════════════════════════════════════════════════════════

📖 DOCUMENTATION GUIDE

   PROJECT_SUMMARY.md    = Overview + examples (read first!)
   README.md             = Full features + options
   QUICKSTART.md         = Getting started guide
   ARCHITECTURE.md       = Design details + comparison
   COMPARISON.md         = vs sustain_poi (original project)
   CHECKLIST.md          = Setup & testing checklist

═══════════════════════════════════════════════════════════════════════════════

🤖 AVAILABLE MODELS (10+)

   Local (Ollama - FREE):
   ├── llama3:8b
   ├── qwen3:8b
   ├── mistral
   └── deepseek-r1

   OpenAI:
   ├── gpt-4o-mini         (cheapest)
   └── gpt-4o              (best)

   Anthropic:
   ├── claude-3-5-sonnet-20241022
   └── claude-3-opus-20250219

   Google:
   ├── gemini-1.5-pro
   └── gemini-2.0-flash

═══════════════════════════════════════════════════════════════════════════════

📋 AVAILABLE TASKS (4 Pre-Built)

   classification    → Categorize text
   extraction        → Extract key information
   sentiment         → Analyze sentiment
   custom            → Generic analysis

   Easy to add more in config/general_registry.py

═══════════════════════════════════════════════════════════════════════════════

🔑 SETUP STEPS

   Step 1: Install Dependencies
   ├── pip install -r requirements.txt
   └── (takes 1-2 minutes)

   Step 2: Setup API Keys (Optional)
   ├── Copy .env.example → .env
   ├── Add API keys if using cloud providers
   └── (Ollama works without keys)

   Step 3: Verify Installation
   ├── Run sample: python run_general.py --excel data/sample_input.xlsx --task sentiment --model llama3:8b
   └── Check outputs directory

═══════════════════════════════════════════════════════════════════════════════

💡 EXAMPLE USE CASES

   Use Case 1: Sentiment Analysis
   ├── Data: Product reviews (title + review text)
   ├── Task: sentiment
   └── Output: sentiment, intensity, drivers

   Use Case 2: Content Classification
   ├── Data: Articles (title + content)
   ├── Task: classification
   └── Output: category, confidence

   Use Case 3: Information Extraction
   ├── Data: Documents (title + text)
   ├── Task: extraction
   └── Output: entities, topics, summary

   Use Case 4: Custom Analysis
   ├── Data: Any text (title + content)
   ├── Task: custom (or create your own)
   └── Output: Your defined structure

═══════════════════════════════════════════════════════════════════════════════

🔧 CUSTOMIZATION

   Add New Task:
   1. Create: prompts/mytask_system.txt
   2. Create: prompts/mytask_user.txt
   3. Add to: config/general_registry.py
   4. Run: python run_general.py --task mytask --model ...

   Add New Model:
   1. Add to: config/models.py
   2. Run: python run_general.py --model mymodel --task ...

═══════════════════════════════════════════════════════════════════════════════

📊 EXCEL INPUT FORMAT

   Your Excel must have these columns:

   id      number      title              text
   ───     ──────      ─────              ────
   1       101         Product A          This product is amazing...
   2       102         Product B          Good quality but...
   3       103         Product C          Terrible experience...

   Customize column names with:
   --id-col NAME --number-col NAME --title-col NAME --text-col NAME

═══════════════════════════════════════════════════════════════════════════════

🔄 PROCESSING FLOW

   Excel File
       ↓
   Parse Arguments
       ↓
   Load Task Config + Prompts
       ↓
   Load LLM Model
       ↓
   For Each Row:
   ├─ Extract {id, number, title, text}
   ├─ Send to LLM with prompt
   ├─ Get response
   ├─ Parse JSON (or keep raw)
   └─ Write to JSONL
       ↓
   Export to Excel

═══════════════════════════════════════════════════════════════════════════════

📈 OUTPUT FORMAT

   JSONL (Line by Line):
   {
     "timestamp": "2025-03-24T10:30:00+00:00",
     "item_id": "1",
     "number": 101,
     "title": "Product A",
     "task": "sentiment",
     "model": "gpt-4o-mini",
     "provider": "openai",
     "result": {
       "sentiment": "positive",
       "intensity": 0.95,
       ...
     }
   }

   Excel: Flattened, deduplicated snapshot

═══════════════════════════════════════════════════════════════════════════════

🆚 ORIGINAL vs NEW

   ORIGINAL (sustain_poi)    |    NEW (general_processor)
   ────────────────────────────────────────────────────────
   Domain-specific           |    General purpose
   Requires schema           |    No schema needed
   Complex input             |    3 fields only
   PILLAR_REGISTRY           |    GENERAL_REGISTRY
   Environmental focus       |    Any text task

═══════════════════════════════════════════════════════════════════════════════

❓ TROUBLESHOOTING

   "Column not found"        → Check Excel column names
   "Model not found"         → Check config/models.py
   "Task not found"          → Check config/general_registry.py
   "API key error"           → Check .env file
   "Ollama not working"      → Start ollama serve

═══════════════════════════════════════════════════════════════════════════════

✅ WHAT'S INCLUDED

   ✓ Complete project structure
   ✓ 4 pre-built tasks
   ✓ 10+ pre-registered models
   ✓ Multi-provider support
   ✓ 6 comprehensive documentation files
   ✓ Sample Excel with test data
   ✓ Error handling & logging
   ✓ JSONL + Excel export
   ✓ Easy customization
   ✓ Production-ready code

═══════════════════════════════════════════════════════════════════════════════

🚀 READY TO START?

   1. Read: PROJECT_SUMMARY.md (5 minutes)
   2. Setup: Follow QUICKSTART.md (5 minutes)
   3. Test: Run sample data (2 minutes)
   4. Customize: Add your data & tasks
   5. Deploy: Process your dataset

   Total time to first results: ~15 minutes

═══════════════════════════════════════════════════════════════════════════════

📞 HELP & SUPPORT

   All documentation is self-contained:
   ├── README.md for features
   ├── QUICKSTART.md for getting started
   ├── ARCHITECTURE.md for design
   ├── COMPARISON.md for context
   ├── CHECKLIST.md for verification
   └── Code comments for details

═══════════════════════════════════════════════════════════════════════════════

Project Status: ✅ READY TO USE

Created: March 24, 2026
Based on: sustain_poi (simplified & generalized)
License: [Add your license]

═══════════════════════════════════════════════════════════════════════════════
