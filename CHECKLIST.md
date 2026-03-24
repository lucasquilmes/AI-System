# Getting Started Checklist

## Pre-Setup

- [ ] Python 3.8+ installed
- [ ] pip package manager available
- [ ] Text editor or IDE (VS Code recommended)
- [ ] Terminal/Command Prompt access

## Initial Setup

### 1. Dependencies
- [ ] Run `pip install -r requirements.txt`
- [ ] Wait for all packages to install
- [ ] Verify no errors during installation

### 2. API Credentials (If Using Cloud Providers)
- [ ] Copy `.env.example` to `.env`
- [ ] Open `.env` and add your API keys:
  - [ ] OPENAI_API_KEY (for GPT models)
  - [ ] ANTHROPIC_API_KEY (for Claude models)
  - [ ] GOOGLE_API_KEY (for Gemini models)
- [ ] Save `.env` file
- [ ] Note: Ollama doesn't need API keys

### 3. Ollama Setup (Optional, for Local Models)
- [ ] Download Ollama from https://ollama.ai
- [ ] Install Ollama
- [ ] Run `ollama serve` in a terminal
- [ ] In another terminal, verify: `ollama list`
- [ ] Pull models: `ollama pull llama2`, `ollama pull mistral`, etc.

## First Run - Local Testing

### Test 1: Verify Installation
```bash
# Check Python
python --version

# Check dependencies
python -c "import langchain; print('LangChain OK')"
python -c "import pandas; print('Pandas OK')"
```
- [ ] All imports work without errors

### Test 2: Verify File Structure
```bash
# Check key files exist
ls run_general.py
ls config/general_registry.py
ls prompts/sentiment_system.txt
ls data/sample_input.xlsx
```
- [ ] All key files present

### Test 3: First Processing Run
```bash
# With Ollama (if running)
python run_general.py \
  --excel data/sample_input.xlsx \
  --sheet Sheet1 \
  --task sentiment \
  --model llama3:8b \
  --from-row 0 \
  --to-row 2
```
- [ ] Script runs without crashing
- [ ] See progress messages
- [ ] Output directory created

### Test 4: Check Results
```bash
# Check JSONL output
cat outputs/sentiment/llama3_8b/results.jsonl

# Open Excel results
outputs/sentiment/llama3_8b/results.xlsx
```
- [ ] JSONL file has records
- [ ] Excel file opens without errors
- [ ] Data looks reasonable

## Second Run - With Cloud Provider

### Test 5: OpenAI Processing (If API Key Available)
```bash
python run_general.py \
  --excel data/sample_input.xlsx \
  --sheet Sheet1 \
  --task sentiment \
  --model gpt-4o-mini \
  --from-row 0 \
  --to-row 2
```
- [ ] API key accepted (no auth error)
- [ ] Results generated
- [ ] Quality looks good

### Test 6: Compare Models
```bash
# Run same data through different models
python run_general.py --excel data/sample_input.xlsx --task sentiment --model llama3:8b --from-row 0 --to-row 5
python run_general.py --excel data/sample_input.xlsx --task sentiment --model gpt-4o-mini --from-row 0 --to-row 5
```
- [ ] Results saved to different directories
- [ ] Can compare outputs

## Customization - Add Your Data

### Test 7: Prepare Your Excel File
- [ ] Create Excel file with your data
- [ ] Add column: `id` (unique identifier)
- [ ] Add column: `number` (numeric/string ID)
- [ ] Add column: `title` (name/context)
- [ ] Add column: `text` (main content)
- [ ] Save to `data/` folder

### Test 8: Run With Your Data
```bash
python run_general.py \
  --excel data/your_file.xlsx \
  --sheet Sheet1 \
  --task classification \
  --model gpt-4o-mini
```
- [ ] Script processes your data
- [ ] Results look correct
- [ ] No unexpected errors

## Customization - Add New Task

### Test 9: Create Custom Prompts
- [ ] Create `prompts/mytask_system.txt`
  - [ ] Add system instructions
  - [ ] Save file
- [ ] Create `prompts/mytask_user.txt`
  - [ ] Add user template with `{title}` and `{text}`
  - [ ] Save file

### Test 10: Register New Task
- [ ] Open `config/general_registry.py`
- [ ] Add new task entry:
  ```python
  "mytask": {
      "name": "mytask",
      "system_prompt": Path("prompts/mytask_system.txt"),
      "user_prompt": Path("prompts/mytask_user.txt"),
      "output_prefix": "mytask",
  }
  ```
- [ ] Save file

### Test 11: Run New Task
```bash
python run_general.py \
  --excel data/sample_input.xlsx \
  --task mytask \
  --model gpt-4o-mini
```
- [ ] New task runs successfully
- [ ] Results in expected output directory
- [ ] Output format is correct

## Customization - Add New Model

### Test 12: Register New Model
- [ ] Open `config/models.py`
- [ ] Add new model entry:
  ```python
  "my-new-model": {
      "provider": "openai",
      "temperature": 0.0,
      "seed": 42,
  }
  ```
- [ ] Save file

### Test 13: Run With New Model
```bash
python run_general.py \
  --excel data/sample_input.xlsx \
  --task sentiment \
  --model my-new-model
```
- [ ] New model runs successfully
- [ ] Results generated
- [ ] Compare with other models

## Production Setup

### Test 14: Batch Processing
- [ ] Process 100+ rows
- [ ] Monitor for errors
- [ ] Check output quality
- [ ] Verify completion time

### Test 15: Error Handling
- [ ] Intentionally break a prompt
- [ ] Run processing
- [ ] Verify errors are logged
- [ ] Verify processing continues

### Test 16: Results Analysis
- [ ] Open results.xlsx
- [ ] Sort/filter results
- [ ] Identify patterns
- [ ] Generate insights

## Documentation Review

- [ ] Read README.md - Understand features
- [ ] Read QUICKSTART.md - Review examples
- [ ] Read ARCHITECTURE.md - Understand design
- [ ] Read COMPARISON.md - Compare with original
- [ ] Bookmark all .md files

## Performance Optimization

- [ ] Test with batch sizes (10, 50, 100, 500)
- [ ] Measure time per item
- [ ] Monitor API costs (if using cloud)
- [ ] Adjust temperature/seed if needed
- [ ] Consider parallel processing for future

## Troubleshooting Guide

If issues occur, check:

### Installation Issues
- [ ] Python version correct?
- [ ] All packages installed? (`pip list`)
- [ ] Virtual environment active?

### API Key Issues
- [ ] .env file exists?
- [ ] Keys correctly formatted?
- [ ] Keys are valid and active?
- [ ] Right key for right provider?

### Data Issues
- [ ] Excel file format correct?
- [ ] Column names match CLI args?
- [ ] No empty cells in required columns?
- [ ] Proper encoding (UTF-8)?

### Runtime Issues
- [ ] Error message informative?
- [ ] Check JSONL for error records?
- [ ] Try with smaller batch?
- [ ] Check output directory created?

### Ollama Issues
- [ ] Ollama service running? (`ollama serve`)
- [ ] Model available? (`ollama list`)
- [ ] Model name matches config?
- [ ] Sufficient disk space?

## Success Indicators

✓ You're ready when:
- [ ] Dependencies install without errors
- [ ] Sample data processes successfully
- [ ] Results generate in JSONL and Excel
- [ ] Can run with multiple models
- [ ] Can create custom tasks
- [ ] Understanding the workflow
- [ ] Can troubleshoot basic issues
- [ ] Generated meaningful results

---

## Next Steps After Setup

1. **Explore Documentation**
   - Read all `.md` files
   - Understand architecture
   - Know available options

2. **Process Your Data**
   - Prepare Excel file
   - Run with best model for your task
   - Analyze results

3. **Experiment**
   - Try different tasks
   - Compare model outputs
   - Adjust prompts
   - Build custom workflows

4. **Optimize**
   - Batch process large files
   - Compare provider costs
   - Measure quality metrics
   - Build automation

5. **Scale**
   - Process thousands of items
   - Schedule regular jobs
   - Monitor results
   - Generate reports

---

## Quick Reference Commands

```bash
# Installation
pip install -r requirements.txt

# Basic run
python run_general.py --excel data/input.xlsx --task sentiment --model gpt-4o-mini

# With custom columns
python run_general.py --excel data/input.xlsx --task classification \
  --model llama3:8b \
  --number-col id \
  --title-col name \
  --text-col content

# Batch processing
python run_general.py --excel data/input.xlsx --task sentiment \
  --model gpt-4o-mini \
  --from-row 0 \
  --to-row 100

# Available options
python run_general.py --help

# Check models
grep "provider" config/models.py

# Check tasks
grep "\".*\":" config/general_registry.py
```

---

## Support Resources

In project:
- README.md - Main documentation
- QUICKSTART.md - Quick start
- ARCHITECTURE.md - Design details
- COMPARISON.md - vs original project
- PROJECT_SUMMARY.md - Overview

Online:
- LangChain docs: https://python.langchain.com/
- OpenAI docs: https://platform.openai.com/docs
- Anthropic docs: https://docs.anthropic.com
- Google GenAI: https://ai.google.dev

---

Last Updated: March 24, 2026
Status: Ready for Use ✓
