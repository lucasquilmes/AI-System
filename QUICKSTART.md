# Quick Start Guide

## Installation

```bash
# 1. Navigate to project directory
cd general_processor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with API keys (if using cloud providers)
# Example:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

## Try It Out (Local Ollama)

```bash
# 1. Make sure Ollama is running
ollama serve

# 2. In another terminal, run with sample data
python run_general.py \
  --excel data/sample_input.xlsx \
  --sheet Sheet1 \
  --task sentiment \
  --model llama3:8b \
  --from-row 0 \
  --to-row 5
```

Results will be in: `outputs/sentiment/llama3_8b/`

## Try It with OpenAI

```bash
python run_general.py \
  --excel data/sample_input.xlsx \
  --sheet Sheet1 \
  --task sentiment \
  --model gpt-4o-mini \
  --from-row 0 \
  --to-row 5
```

## Try It with Anthropic

```bash
python run_general.py \
  --excel data/sample_input.xlsx \
  --sheet Sheet1 \
  --task sentiment \
  --model claude-3-5-sonnet-20241022 \
  --from-row 0 \
  --to-row 5
```

## File Structure Explained

```
general_processor/
├── config/
│   ├── credentials.py           ← Add your API keys (or use .env)
│   ├── models.py                ← Register LLM models
│   └── general_registry.py      ← Register tasks (prompts)
├── prompts/
│   ├── classification_*         ← Pre-built classification task
│   ├── extraction_*             ← Pre-built extraction task
│   ├── sentiment_*              ← Pre-built sentiment task
│   └── custom_*                 ← Generic task for custom rules
├── data/
│   └── sample_input.xlsx        ← Your Excel input files
├── outputs/                     ← Results (organized by task/model)
└── run_general.py               ← Main script
```

## Key Differences from Original Project

| Feature | Original (sustain_poi) | New (general_processor) |
|---------|------------------------|------------------------|
| Schema Required | Yes (Pydantic) | No (raw output) |
| Purpose | Environmental evaluation | General text processing |
| Input | POI data | Any 3-field data |
| Registry Name | PILLAR_REGISTRY | GENERAL_REGISTRY |
| Configuration | Pillar-based | Task-based |
| Output Parsing | Structured validation | Flexible (JSON or raw) |

## Next Steps

1. **Customize Prompts**: Edit files in `prompts/` for your specific needs
2. **Add More Models**: Edit `config/models.py` to add new LLM providers
3. **Create New Tasks**: Add to `config/general_registry.py` with corresponding prompt files
4. **Prepare Your Data**: Format your Excel with `number`, `title`, and `text` columns
5. **Run Processing**: Use the command-line interface to process your data

## Example Workflows

### Sentiment Analysis Workflow
```bash
# 1. Prepare Excel with review data
# 2. Run sentiment task
python run_general.py --excel data/reviews.xlsx --task sentiment --model gpt-4o-mini

# 3. Check results in outputs/sentiment/gpt-4o-mini/results.xlsx
```

### Custom Analysis Workflow
```bash
# 1. Edit prompts/custom_system.txt and prompts/custom_user.txt
# 2. Run custom task
python run_general.py --excel data/input.xlsx --task custom --model llama3:8b

# 3. Check results
```

## Support

For issues or questions, check:
- README.md for full documentation
- config/general_registry.py for available tasks
- config/models.py for available models
