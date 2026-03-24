import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate

from config.credentials import load_credentials
from config.models import MODEL_REGISTRY
from config.general_registry import GENERAL_REGISTRY


# ====================== UTILITIES ======================

def utc_now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def load_text(path: Path) -> str:
    """Load text from file."""
    return path.read_text(encoding="utf-8")


def write_line(path: Path, text: str) -> None:
    """Append line to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text + "\n")


def safe_name(s: str) -> str:
    """Convert name to folder-safe format."""
    return str(s).replace(":", "_").replace("/", "_").replace("\\", "_").replace(" ", "_")


# ====================== LLM FACTORY ======================

def build_llm(provider: str, model_name: str, model_cfg: dict, creds: dict):
    """
    Build LLM instance for different providers.
    
    Providers: ollama / openai / anthropic / google
    """
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        return ChatOllama(model=model_name, **extra)

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        if not creds.get("openai_api_key"):
            raise ValueError("OPENAI_API_KEY missing. Put it in .env or environment variables.")
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        return ChatOpenAI(
            model=model_name,
            api_key=creds["openai_api_key"],
            base_url=creds.get("openai_base_url"),
            **extra,
        )

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        if not creds.get("anthropic_api_key"):
            raise ValueError("ANTHROPIC_API_KEY missing. Put it in .env or environment variables.")
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        return ChatAnthropic(
            model=model_name,
            api_key=creds["anthropic_api_key"],
            **extra,
        )

    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        if not creds.get("google_api_key"):
            raise ValueError("GOOGLE_API_KEY missing. Put it in .env or environment variables.")
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        return ChatGoogleGenerativeAI(
            model=model_name,
            api_key=creds["google_api_key"],
            **extra,
        )

    raise ValueError(f"Unsupported provider: {provider}")


# ====================== CHAIN BUILDER ======================

def build_chain(task_cfg: dict, model_key: str, creds: dict):
    """
    Build chain: prompt -> llm
    No Pydantic output parser needed (raw LLM output).
    """
    system_prompt = load_text(task_cfg["system_prompt"])
    user_prompt = load_text(task_cfg["user_prompt"])

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt),
    ])

    model_cfg = MODEL_REGISTRY.get(model_key)
    if model_cfg is None:
        raise ValueError(f"Model '{model_key}' not found in MODEL_REGISTRY (config/models.py).")

    provider = model_cfg.get("provider")
    if not provider:
        raise ValueError(f"Model '{model_key}' has no provider in MODEL_REGISTRY.")

    llm = build_llm(provider=provider, model_name=model_key, model_cfg=model_cfg, creds=creds)

    chain = prompt | llm
    return chain, provider, model_cfg


# ====================== ROW CONTEXT ======================

def row_to_context(row: dict, item_id: str, number_col: str, title_col: str, text_col: str) -> dict:
    """
    Extract context from row for LLM input.
    
    Args:
        row: Dictionary representation of Excel row
        item_id: Unique identifier for this item
        number_col: Name of the number column
        title_col: Name of the title column
        text_col: Name of the text column
    
    Returns:
        Dictionary with number, title, and text
    """
    return {
        "item_id": item_id,
        "number": int(row.get(number_col)) if row.get(number_col) is not None else None,
        "title": row.get(title_col),
        "text": row.get(text_col),
    }


# ====================== PROCESSING ======================

def process_excel(
    excel_path: Path,
    sheet_name: str,
    task_name: str,
    model_key: str,
    output_prefix: str,
    number_col: str,
    title_col: str,
    text_col: str,
    id_col: str,
    from_row: int = 0,
    to_row: int = None,
):
    """
    Main processing function.
    """
    # Load credentials and build chain
    creds = load_credentials()
    task_cfg = GENERAL_REGISTRY.get(task_name)
    if not task_cfg:
        raise ValueError(f"Task '{task_name}' not found in GENERAL_REGISTRY (config/general_registry.py).")

    chain, provider, model_cfg = build_chain(task_cfg, model_key, creds)

    # Read Excel
    print(f"Reading Excel: {excel_path}")
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        raise ValueError(f"Failed to read Excel: {e}")

    # Validate columns exist
    for col in [id_col, number_col, title_col, text_col]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in Excel. Available: {list(df.columns)}")

    # Slice rows
    total_rows = len(df)
    to_row = to_row if to_row is not None else total_rows
    to_row = min(to_row, total_rows)

    print(f"Processing rows {from_row} to {to_row-1} (total: {total_rows})")

    # Output paths
    output_dir = Path(f"outputs/{safe_name(task_name)}/{safe_name(model_key)}")
    output_jsonl = output_dir / "results.jsonl"

    # Process each row
    for idx in range(from_row, to_row):
        row = df.iloc[idx]
        item_id = str(row.get(id_col, idx))

        # Build context
        context = row_to_context(row, item_id, number_col, title_col, text_col)

        print(f"[{idx+1}/{to_row}] Processing item {item_id}...")

        try:
            # Invoke chain
            response = chain.invoke(context)
            
            # Extract content from response
            if hasattr(response, 'content'):
                result_text = response.content
            else:
                result_text = str(response)

            # Try to parse as JSON, otherwise store as raw text
            try:
                result_json = json.loads(result_text)
            except json.JSONDecodeError:
                result_json = {"raw_output": result_text}

            # Create output record
            output_record = {
                "timestamp": utc_now_iso(),
                "item_id": item_id,
                "number": context.get("number"),
                "title": context.get("title"),
                "task": task_name,
                "model": model_key,
                "provider": provider,
                "result": result_json,
            }

            # Write to JSONL
            write_line(output_jsonl, json.dumps(output_record))
            print(f"  ✓ Completed")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            error_record = {
                "timestamp": utc_now_iso(),
                "item_id": item_id,
                "number": context.get("number"),
                "title": context.get("title"),
                "task": task_name,
                "model": model_key,
                "provider": provider,
                "error": str(e),
            }
            write_line(output_jsonl, json.dumps(error_record))

    print(f"\nResults saved to: {output_jsonl}")
    export_jsonl_to_excel(output_jsonl, output_dir / "results.xlsx")
    print(f"Excel export saved to: {output_dir / 'results.xlsx'}")


# ====================== EXCEL EXPORT ======================

def export_jsonl_to_excel(jsonl_path: Path, xlsx_path: Path, dedup_key: str = "item_id"):
    """
    Read JSONL and write Excel snapshot.
    Dedup: keep the latest occurrence per item_id.
    """
    if not jsonl_path.exists():
        return

    records = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if not records:
        return

    # Last write wins dedup
    deduped = {}
    for r in records:
        deduped[str(r.get(dedup_key))] = r

    df = pd.json_normalize(list(deduped.values()))
    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(xlsx_path, index=False)


# ====================== CLI ======================

def main():
    parser = argparse.ArgumentParser(
        description="Process Excel data with LLM and configurable tasks"
    )
    parser.add_argument(
        "--excel",
        type=Path,
        required=True,
        help="Path to Excel file with data"
    )
    parser.add_argument(
        "--sheet",
        type=str,
        default="Sheet1",
        help="Sheet name in Excel (default: Sheet1)"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help=f"Task name (from GENERAL_REGISTRY): {', '.join(GENERAL_REGISTRY.keys())}"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help=f"Model name (from MODEL_REGISTRY): see config/models.py"
    )
    parser.add_argument(
        "--id-col",
        type=str,
        default="id",
        help="Column name for unique identifier (default: id)"
    )
    parser.add_argument(
        "--number-col",
        type=str,
        default="number",
        help="Column name for number field (default: number)"
    )
    parser.add_argument(
        "--title-col",
        type=str,
        default="title",
        help="Column name for title field (default: title)"
    )
    parser.add_argument(
        "--text-col",
        type=str,
        default="text",
        help="Column name for text/input field (default: text)"
    )
    parser.add_argument(
        "--from-row",
        type=int,
        default=0,
        help="Start row index (0-based, default: 0)"
    )
    parser.add_argument(
        "--to-row",
        type=int,
        default=None,
        help="End row index (exclusive, default: end of file)"
    )
    parser.add_argument(
        "--output-prefix",
        type=str,
        default=None,
        help="Output prefix (default: task name)"
    )

    args = parser.parse_args()

    # Validate Excel path
    if not args.excel.exists():
        print(f"Error: Excel file not found: {args.excel}")
        return

    # Use task name as output prefix if not specified
    output_prefix = args.output_prefix or args.task

    # Run processing
    process_excel(
        excel_path=args.excel,
        sheet_name=args.sheet,
        task_name=args.task,
        model_key=args.model,
        output_prefix=output_prefix,
        number_col=args.number_col,
        title_col=args.title_col,
        text_col=args.text_col,
        id_col=args.id_col,
        from_row=args.from_row,
        to_row=args.to_row,
    )


if __name__ == "__main__":
    main()
