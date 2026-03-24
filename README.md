# General Processor - Project Documentation

A flexible LLM processing framework that reads Excel files and processes data through configurable LLM tasks with support for multiple providers.

## Project Structure

```
general_processor/
├── config/
│   ├── __init__.py
│   ├── credentials.py          # Load API keys from .env
│   ├── models.py               # MODEL_REGISTRY with all LLM configurations
│   └── general_registry.py     # GENERAL_REGISTRY with task configurations
├── prompts/
│   ├── classification_system.txt
│   ├── classification_user.txt
│   ├── extraction_system.txt
│   ├── extraction_user.txt
│   ├── sentiment_system.txt
│   ├── sentiment_user.txt
│   ├── custom_system.txt
│   └── custom_user.txt
├── data/                       # Input Excel files
├── outputs/                    # Results (JSONL + Excel)
├── run_general.py             # Main script
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Key Features

- **Multiple LLM Providers**: Ollama, OpenAI, Anthropic, Google
- **Flexible Input Format**: Excel with configurable column names
- **No Schema Required**: Works with raw LLM output (JSON or text)
- **Task-Based Registry**: Organize prompts and configuration by task
- **Dual Output Format**: JSONL for line-by-line processing + Excel snapshot
- **Error Handling**: Captures and logs errors while continuing processing

## Excel Input Format

Your Excel file should have exactly 3 data fields:

| Column | Description |
|--------|-------------|
| `number` | A numeric or string identifier for the item |
| `title` | A title or name for the item |
| `text` | The main text content to be processed by the LLM |

Plus an ID column (customizable, default: `id`) for unique identification.

**Example:**
```
id | number | title         | text
1  | 101    | Item One      | This is the text content to analyze...
2  | 102    | Item Two      | Another piece of text content...
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

For Ollama models, no API key is needed (runs locally).

### 3. Add or Modify Prompts

Edit prompt files in the `prompts/` folder:
- `{task}_system.txt`: System prompt (instructions/role)
- `{task}_user.txt`: User prompt template (can use `{title}` and `{text}` placeholders)

### 4. Register Your Model

Edit `config/models.py` to add new LLM configurations:

```python
"my-model": {
    "provider": "openai",  # or ollama, anthropic, google
    "temperature": 0.0,
    "seed": 42,
}
```

### 5. Register Your Task

Edit `config/general_registry.py` to add new tasks:

```python
"my-task": {
    "name": "my-task",
    "system_prompt": Path("prompts/my-task_system.txt"),
    "user_prompt": Path("prompts/my-task_user.txt"),
    "output_prefix": "my-task",
}
```

## Usage

### Basic Command

```bash
python run_general.py \
  --excel data/input.xlsx \
  --sheet Sheet1 \
  --task classification \
  --model gpt-4o-mini
```

### Full Options

```bash
python run_general.py \
  --excel data/input.xlsx \
  --sheet Sheet1 \
  --task classification \
  --model gpt-4o-mini \
  --id-col id \
  --number-col number \
  --title-col title \
  --text-col text \
  --from-row 0 \
  --to-row 100
```

### Available Tasks

Currently available tasks:
- `classification` - Classify text into categories
- `extraction` - Extract key information
- `sentiment` - Analyze sentiment
- `custom` - Generic analysis

### Available Models

See `config/models.py` for all registered models. Examples:

**Local (Ollama):**
- `llama3:8b`
- `qwen3:8b`
- `mistral`
- `deepseek-r1`

**OpenAI:**
- `gpt-4o-mini`
- `gpt-4o`

**Anthropic:**
- `claude-3-5-sonnet-20241022`
- `claude-3-opus-20250219`

**Google:**
- `gemini-1.5-pro`
- `gemini-2.0-flash`

## Output Format

Results are saved in `outputs/{task}/{model}/`:

### results.jsonl
Each line is a JSON object with:
```json
{
  "timestamp": "2025-03-24T10:30:00+00:00",
  "item_id": "1",
  "number": 101,
  "title": "Item Title",
  "task": "classification",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "result": { ... },  // LLM output (parsed JSON or raw)
}
```

### results.xlsx
Excel snapshot with all results deduplicated by `item_id`.

## Examples

### Example 1: Classify customer feedback

```bash
python run_general.py \
  --excel data/customer_feedback.xlsx \
  --sheet Feedback \
  --task classification \
  --model gpt-4o-mini \
  --number-col feedback_id \
  --title-col customer_name \
  --text-col feedback_text
```

### Example 2: Extract information with Ollama

```bash
python run_general.py \
  --excel data/documents.xlsx \
  --sheet Documents \
  --task extraction \
  --model llama3:8b \
  --number-col doc_number \
  --title-col doc_title \
  --text-col doc_content \
  --from-row 0 \
  --to-row 50
```

### Example 3: Analyze sentiment with Anthropic

```bash
python run_general.py \
  --excel data/reviews.xlsx \
  --sheet Reviews \
  --task sentiment \
  --model claude-3-5-sonnet-20241022 \
  --number-col review_id \
  --title-col product_name \
  --text-col review_text
```

## Creating Custom Tasks

### Step 1: Create prompt files

Create `prompts/mynewtask_system.txt`:
```
You are an expert at [your task].

Your job is to [describe what to do].

Return ONLY valid JSON output with the following fields:
- field1: description
- field2: description
```

Create `prompts/mynewtask_user.txt`:
```
Analyze the following:

Title: {title}
Text: {text}

Provide your analysis in JSON format with:
- field1: ...
- field2: ...

Return ONLY the JSON object, no additional text.
```

### Step 2: Register in config/general_registry.py

```python
"mynewtask": {
    "name": "mynewtask",
    "system_prompt": Path("prompts/mynewtask_system.txt"),
    "user_prompt": Path("prompts/mynewtask_user.txt"),
    "output_prefix": "mynewtask",
}
```

### Step 3: Run

```bash
python run_general.py \
  --excel data/input.xlsx \
  --task mynewtask \
  --model gpt-4o-mini
```

## Error Handling

If an error occurs during processing:
- The error is logged to the output JSONL file
- Processing continues with the next item
- Check JSONL for error records with `"error"` field

## Troubleshooting

### "Column not found" error
Make sure your Excel column names match the `--*-col` arguments.

### "Model not found" error
Check that your model is registered in `config/models.py`.

### "Task not found" error
Check that your task is registered in `config/general_registry.py`.

### API key errors
Ensure your `.env` file has the correct API keys and they're loaded properly.

### Ollama models not working
Make sure Ollama is running: `ollama serve`

## Advantages Over Original Project

1. **No Schema Required**: Simpler, more flexible for different tasks
2. **General Purpose**: Not limited to specific evaluation domains
3. **Registry-Based**: Easy to add new tasks and models
4. **Raw Output Support**: Works with any JSON structure the LLM produces
5. **Cleaner API**: Simpler command-line interface for common use cases

## License

[Your license here]
