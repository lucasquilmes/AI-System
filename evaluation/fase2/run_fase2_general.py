#!/usr/bin/env python
"""
Versión de run_general.py para Fase 2 — añade soporte a --temperature y --seed.
Los outputs se guardan en outputs/<dataset>_t<T>_s<seed>/<task>/<model>/

Uso (llamado normalmente desde run_fase2.py):
  python evaluation/fase2/run_fase2_general.py \
      --excel data/Test_poor.xlsx --sheet Hoja1 \
      --task v8 --model llama3.3 \
      --temperature 0.7 --seed 123
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate

# Añadir raíz del proyecto al path
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from config.credentials import load_credentials
from config.models import MODEL_REGISTRY
from config.general_registry import GENERAL_REGISTRY


# ── Utilidades ────────────────────────────────────────────────────────────────

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_line(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text + "\n")


def safe_name(s: str) -> str:
    return str(s).replace(":", "_").replace("/", "_").replace("\\", "_").replace(" ", "_")


# ── LLM con overrides de temperatura y seed ───────────────────────────────────

def build_llm(provider: str, model_name: str, model_cfg: dict, creds: dict,
              temperature: float, seed: int):
    """Construye el LLM aplicando los overrides de temperatura y seed."""
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        extra["temperature"] = temperature
        extra["seed"] = seed
        return ChatOllama(model=model_name, **extra)

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        if not creds.get("openai_api_key"):
            raise ValueError("OPENAI_API_KEY missing.")
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        extra["temperature"] = temperature
        extra["seed"] = seed
        return ChatOpenAI(model=model_name, api_key=creds["openai_api_key"],
                          base_url=creds.get("openai_base_url"), **extra)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        if not creds.get("anthropic_api_key"):
            raise ValueError("ANTHROPIC_API_KEY missing.")
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        extra["temperature"] = temperature
        return ChatAnthropic(model=model_name, api_key=creds["anthropic_api_key"], **extra)

    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        if not creds.get("google_api_key"):
            raise ValueError("GOOGLE_API_KEY missing.")
        extra = {k: v for k, v in model_cfg.items() if k not in ["provider"]}
        extra["temperature"] = temperature
        return ChatGoogleGenerativeAI(model=model_name, api_key=creds["google_api_key"], **extra)

    raise ValueError(f"Unsupported provider: {provider}")


def build_chain(task_cfg: dict, model_key: str, creds: dict,
                temperature: float, seed: int):
    system_prompt = load_text(ROOT / task_cfg["system_prompt"])
    user_prompt   = load_text(ROOT / task_cfg["user_prompt"])

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user",   user_prompt),
    ])

    model_cfg = MODEL_REGISTRY.get(model_key)
    if model_cfg is None:
        raise ValueError(f"Model '{model_key}' not found in MODEL_REGISTRY.")

    provider = model_cfg.get("provider")
    if not provider:
        raise ValueError(f"Model '{model_key}' has no provider in MODEL_REGISTRY.")

    llm   = build_llm(provider, model_key, model_cfg, creds, temperature, seed)
    chain = prompt | llm
    return chain, provider


# ── Procesado ─────────────────────────────────────────────────────────────────

def process_excel(excel_path: Path, sheet_name: str, task_name: str,
                  model_key: str, temperature: float, seed: int,
                  from_row: int = 0, to_row: int = None):

    creds    = load_credentials()
    task_cfg = GENERAL_REGISTRY.get(task_name)
    if not task_cfg:
        raise ValueError(f"Task '{task_name}' not found in GENERAL_REGISTRY.")

    chain, provider = build_chain(task_cfg, model_key, creds, temperature, seed)

    print(f"Reading Excel: {excel_path}")
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    required = ["title", "normal text", "ground truth", "output"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Columna requerida '{col}' no encontrada. Disponibles: {list(df.columns)}")

    total_rows = len(df)
    to_row     = min(to_row if to_row is not None else total_rows, total_rows)

    # Output path: outputs/<dataset>_t<T>_s<seed>/<task>/<model>/
    dataset_name = safe_name(excel_path.stem.lower())
    variant_name = f"{dataset_name}_t{temperature}_s{seed}"
    output_dir   = ROOT / "outputs" / variant_name / safe_name(task_name) / safe_name(model_key)
    output_jsonl = output_dir / "results.jsonl"

    print(f"Output → {output_dir}")
    print(f"Procesando filas {from_row}–{to_row - 1} (total: {total_rows})")

    results = []
    for idx in range(from_row, to_row):
        row     = df.iloc[idx]
        item_id = str(idx)
        context = {
            "item_id": item_id,
            "number":  None,
            "title":   row.get("title"),
            "text":    row.get("normal text"),
        }
        print(f"[{idx + 1}/{to_row}] Procesando ítem {item_id}...")
        try:
            response    = chain.invoke(context)
            result_text = response.content if hasattr(response, "content") else str(response)
            try:
                result_json = json.loads(result_text)
            except json.JSONDecodeError:
                result_json = {"raw_output": result_text}

            write_line(output_jsonl, json.dumps({
                "timestamp":   utc_now_iso(),
                "item_id":     item_id,
                "title":       context["title"],
                "task":        task_name,
                "model":       model_key,
                "provider":    provider,
                "temperature": temperature,
                "seed":        seed,
                "result":      result_json,
            }))
            results.append(result_text)
            print("  ✓ Completado")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            write_line(output_jsonl, json.dumps({
                "timestamp": utc_now_iso(), "item_id": item_id,
                "task": task_name, "model": model_key,
                "temperature": temperature, "seed": seed, "error": str(e),
            }))
            results.append(f"ERROR: {e}")

    # Guardar Excel con outputs
    df["output"] = df["output"].astype(str)
    for i, result in enumerate(results):
        df.at[from_row + i, "output"] = str(result)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_dir / "results.xlsx", index=False)
    print(f"\nGuardado: {output_dir / 'results.xlsx'}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="run_general para Fase 2 — con temperatura y seed explícitos"
    )
    parser.add_argument("--excel",       type=Path, required=True)
    parser.add_argument("--sheet",       default="Hoja1")
    parser.add_argument("--task",        required=True)
    parser.add_argument("--model",       required=True)
    parser.add_argument("--temperature", type=float, required=True,
                        help="Temperatura del modelo (0.0 – 1.0)")
    parser.add_argument("--seed",        type=int,   required=True,
                        help="Semilla aleatoria")
    parser.add_argument("--from-row",   type=int, default=0)
    parser.add_argument("--to-row",     type=int, default=None)
    args = parser.parse_args()

    excel = args.excel if args.excel.is_absolute() else ROOT / args.excel
    if not excel.exists():
        print(f"Error: fichero no encontrado: {excel}")
        sys.exit(1)

    try:
        process_excel(
            excel_path=excel,
            sheet_name=args.sheet,
            task_name=args.task,
            model_key=args.model,
            temperature=args.temperature,
            seed=args.seed,
            from_row=args.from_row,
            to_row=args.to_row,
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
