#!/usr/bin/env python
"""
Lanza las evaluaciones de todos los datasets generados en Fase 2.

Detecta automáticamente las carpetas outputs/<dataset>_t*_s*/ y llama
a evaluation/evaluate_excel.py para cada versión encontrada.

Uso:
  python evaluation/fase2/evaluate_fase2.py
  python evaluation/fase2/evaluate_fase2.py --phase 2a          # solo T variable
  python evaluation/fase2/evaluate_fase2.py --phase 2b          # solo seed variable
  python evaluation/fase2/evaluate_fase2.py --skip-bert         # omite BertScore
  python evaluation/fase2/evaluate_fase2.py --dry-run           # muestra sin ejecutar
"""

import subprocess
import sys
import argparse
import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent
OUTPUTS  = ROOT / "outputs"
EVAL_CLI = ROOT / "evaluation" / "evaluate_excel.py"

PROMPTS  = ["v8", "cot"]


def detect_fase2_datasets(phase_filter: str | None) -> list[dict]:
    """Encuentra carpetas outputs/<name>_t<T>_s<seed>/ y extrae metadata."""
    pattern = re.compile(r"^(.+)_t([\d.]+)_s(\d+)$")
    datasets = []
    for d in sorted(OUTPUTS.iterdir()):
        if not d.is_dir():
            continue
        m = pattern.match(d.name)
        if not m:
            continue
        base, temp_str, seed_str = m.group(1), m.group(2), m.group(3)
        temperature = float(temp_str)
        seed        = int(seed_str)

        # Filtrar por fase
        if phase_filter == "2a" and seed != 42:
            continue
        if phase_filter == "2b" and seed == 42:
            # Seed 42 con T=0.0 es Fase 1; seed 42 con otras T es Fase 2A
            if temperature == 0.0:
                continue

        datasets.append({
            "folder":      d.name,
            "base":        base,
            "temperature": temperature,
            "seed":        seed,
        })
    return datasets


def run_evaluation(dataset_name: str, version: str, skip_bert: bool, dry_run: bool) -> bool:
    cmd = [
        sys.executable, str(EVAL_CLI),
        "--version", version,
        "--dataset", dataset_name,
    ]
    if skip_bert:
        cmd.append("--skip-bert")

    label = f"{dataset_name} | {version}"
    if dry_run:
        print(f"  [DRY-RUN] {label}")
        return True
    print(f"  ▶ {label}")
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT))
        print(f"  ✓ OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error (código {e.returncode})")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evalúa todos los outputs de Fase 2")
    parser.add_argument("--phase", choices=["2a", "2b"], default=None,
                        help="Limitar a Fase 2A (temperaturas) o 2B (seeds)")
    parser.add_argument("--skip-bert", action="store_true",
                        help="Omite BERTScore (~700 MB, lento)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Muestra las evaluaciones sin ejecutarlas")
    args = parser.parse_args()

    datasets = detect_fase2_datasets(args.phase)
    if not datasets:
        print("No se encontraron carpetas de Fase 2 en outputs/.")
        print("Ejecuta primero: python evaluation/fase2/run_fase2.py --phase 2a")
        sys.exit(1)

    total  = len(datasets) * len(PROMPTS)
    failed = []
    done   = 0

    print(f"\n{'='*60}")
    print(f"Evaluando {len(datasets)} datasets × {len(PROMPTS)} prompts = {total} evaluaciones")
    print(f"{'='*60}")

    for ds in datasets:
        print(f"\n[T={ds['temperature']}  seed={ds['seed']}  base={ds['base']}]")
        for version in PROMPTS:
            done += 1
            print(f"  ({done}/{total})", end="")
            ok = run_evaluation(ds["folder"], version, args.skip_bert, args.dry_run)
            if not ok:
                failed.append(f"{ds['folder']} | {version}")

    print(f"\n{'='*60}")
    if args.dry_run:
        print(f"DRY-RUN: {total} evaluaciones listadas")
    elif failed:
        print(f"Completado con errores: {total - len(failed)}/{total} OK")
        for f in failed:
            print(f"  ✗ {f}")
        sys.exit(1)
    else:
        print(f"Todas las evaluaciones completadas ({total}/{total})")
