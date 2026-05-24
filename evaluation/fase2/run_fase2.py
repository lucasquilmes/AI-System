#!/usr/bin/env python
"""
Fase 2 — Ejecución de modelos con variación de temperatura y semilla.

Fase 2A: temperatura variable (T=0.0, 0.3, 0.7, 1.0) con seed fijo (42).
Fase 2B: seed variable (42, 123, 7, 999) con la temperatura óptima de 2A.

Los outputs se guardan en:
  outputs/<dataset>_t<T>_s<seed>/<task>/<model>/

Uso:
  python evaluation/fase2/run_fase2.py --phase 2a
  python evaluation/fase2/run_fase2.py --phase 2b --optimal-temp 0.7
  python evaluation/fase2/run_fase2.py --phase 2a --dataset test_poor   # un solo dataset
  python evaluation/fase2/run_fase2.py --phase 2a --dry-run             # ver combinaciones sin ejecutar
"""

import subprocess
import sys
import argparse
from pathlib import Path

# ── Configuración fija de Fase 2 ────────────────────────────────────────────

MODELS  = ["llama3.3", "gemma2:27b"]
PROMPTS = ["v8", "cot"]

DATASETS = [
    {"excel": "data/Test_poor.xlsx",                         "sheet": "Hoja1"},
    {"excel": "data/exemples_lectura_facil_formatted.xlsx",  "sheet": "Hoja1"},
]

TEMPERATURES_2A = [0.0, 0.3, 0.7, 1.0]
SEEDS_2B        = [42, 123, 7, 999]
SEED_2A         = 42   # semilla fija para Fase 2A

ROOT = Path(__file__).parent.parent.parent  # raíz del proyecto


# ── Helpers ──────────────────────────────────────────────────────────────────

def dataset_label(excel_path: str) -> str:
    return Path(excel_path).stem.lower().replace(" ", "_")


def run_one(excel: str, sheet: str, task: str, model: str,
            temperature: float, seed: int, dry_run: bool) -> bool:
    """Llama a run_fase2_general.py para una combinación concreta."""
    script = Path(__file__).parent / "run_fase2_general.py"
    cmd = [
        sys.executable, str(script),
        "--excel",       excel,
        "--sheet",       sheet,
        "--task",        task,
        "--model",       model,
        "--temperature", str(temperature),
        "--seed",        str(seed),
    ]
    label = f"{dataset_label(excel)} | {task} | {model} | T={temperature} | seed={seed}"
    if dry_run:
        print(f"  [DRY-RUN] {label}")
        return True
    print(f"\n  ▶ {label}")
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT))
        print(f"  ✓ Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error (código {e.returncode})")
        return False


# ── Fase 2A ───────────────────────────────────────────────────────────────────

def run_phase_2a(dataset_filter: str | None, dry_run: bool):
    datasets = [d for d in DATASETS
                if dataset_filter is None or dataset_label(d["excel"]) == dataset_filter]
    if not datasets:
        print(f"Dataset no encontrado: {dataset_filter}")
        sys.exit(1)

    combos = [(d, t, SEED_2A) for d in datasets for t in TEMPERATURES_2A]
    total  = len(combos) * len(MODELS) * len(PROMPTS)

    print(f"\n{'='*60}")
    print(f"FASE 2A — Variación de temperatura")
    print(f"Modelos: {MODELS}")
    print(f"Prompts: {PROMPTS}")
    print(f"Temperaturas: {TEMPERATURES_2A}  |  Seed fijo: {SEED_2A}")
    print(f"Datasets: {[dataset_label(d['excel']) for d in datasets]}")
    print(f"Total ejecuciones: {total}")
    print(f"{'='*60}")

    failed = []
    done   = 0
    for ds in datasets:
        for temp in TEMPERATURES_2A:
            print(f"\n[Dataset: {dataset_label(ds['excel'])}  T={temp}  seed={SEED_2A}]")
            for model in MODELS:
                for prompt in PROMPTS:
                    done += 1
                    print(f"  ({done}/{total})", end="")
                    ok = run_one(ds["excel"], ds["sheet"], prompt, model,
                                 temp, SEED_2A, dry_run)
                    if not ok:
                        failed.append(f"T={temp} | {model} | {prompt} | {dataset_label(ds['excel'])}")

    _print_summary(total, failed, dry_run)


# ── Fase 2B ───────────────────────────────────────────────────────────────────

def run_phase_2b(optimal_temp: float, dataset_filter: str | None, dry_run: bool):
    datasets = [d for d in DATASETS
                if dataset_filter is None or dataset_label(d["excel"]) == dataset_filter]

    combos = [(d, optimal_temp, s) for d in datasets for s in SEEDS_2B]
    total  = len(combos) * len(MODELS) * len(PROMPTS)

    print(f"\n{'='*60}")
    print(f"FASE 2B — Variación de semilla (seed)")
    print(f"Modelos: {MODELS}")
    print(f"Prompts: {PROMPTS}")
    print(f"Temperatura óptima: {optimal_temp}  |  Seeds: {SEEDS_2B}")
    print(f"Datasets: {[dataset_label(d['excel']) for d in datasets]}")
    print(f"Total ejecuciones: {total}")
    print(f"{'='*60}")

    failed = []
    done   = 0
    for ds in datasets:
        for seed in SEEDS_2B:
            print(f"\n[Dataset: {dataset_label(ds['excel'])}  T={optimal_temp}  seed={seed}]")
            for model in MODELS:
                for prompt in PROMPTS:
                    done += 1
                    print(f"  ({done}/{total})", end="")
                    ok = run_one(ds["excel"], ds["sheet"], prompt, model,
                                 optimal_temp, seed, dry_run)
                    if not ok:
                        failed.append(f"seed={seed} | {model} | {prompt} | {dataset_label(ds['excel'])}")

    _print_summary(total, failed, dry_run)


# ── Utils ─────────────────────────────────────────────────────────────────────

def _print_summary(total: int, failed: list, dry_run: bool):
    print(f"\n{'='*60}")
    if dry_run:
        print(f"DRY-RUN completado — {total} combinaciones listadas")
        return
    if failed:
        print(f"Completado con errores: {total - len(failed)}/{total} OK")
        for f in failed:
            print(f"  ✗ {f}")
        sys.exit(1)
    else:
        print(f"Todos los modelos completados ({total}/{total})")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecuta Fase 2 del estudio (temperatura y seed)")
    parser.add_argument("--phase", required=True, choices=["2a", "2b"],
                        help="Fase a ejecutar: 2a (temperaturas) o 2b (seeds)")
    parser.add_argument("--optimal-temp", type=float, default=None,
                        help="Temperatura óptima identificada en Fase 2A (requerido para --phase 2b)")
    parser.add_argument("--dataset", default=None,
                        help="Limitar a un dataset concreto (nombre sin extensión)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Muestra las combinaciones sin ejecutarlas")
    args = parser.parse_args()

    if args.phase == "2a":
        run_phase_2a(args.dataset, args.dry_run)
    else:
        if args.optimal_temp is None:
            parser.error("--optimal-temp es obligatorio para --phase 2b")
        run_phase_2b(args.optimal_temp, args.dataset, args.dry_run)
