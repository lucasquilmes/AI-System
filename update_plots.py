#!/usr/bin/env python
"""
Regenera los gráficos del proyecto organizados por dataset.

Uso:
  python update_plots.py                          # todo: per-dataset + combined
  python update_plots.py --scope per_dataset      # solo plots por dataset
  python update_plots.py --scope combined         # solo plots combinados
  python update_plots.py --scope per_dataset --dataset test_poor   # un dataset concreto
  python update_plots.py --only heatmap_ranking_modelos heatmap_ranking_prompts
"""

import subprocess
import sys
import argparse
from pathlib import Path

PLOTS_DIR = Path("plots")
OUTPUTS   = Path("outputs")

PER_DATASET_PLOTS = [
    "barras_metricas_finales.py",
    "barras_metricas_vx.py",
    "heatmap_ranking_modelos.py",
    "heatmap_ranking_prompts.py",
    "heatmap_prompts_detalle.py",
    "heatmap_sari.py",
    "heatmap_flesch.py",
    "heatmap_rouge_l.py",
    "heatmap_bleu.py",
    "heatmap_lmo.py",
    "heatmap_complex_words.py",
    "barras_score_modelo.py",
    "barras_score_tecnica.py",
]

COMBINED_PLOTS = [
    "combined_ranking_modelos.py",
    "combined_ranking_prompts.py",
]

FASE2A_SCRIPT = PLOTS_DIR / "fase2" / "compare_temperatures.py"


def run_script(script_path: Path, extra_args: list[str]) -> bool:
    cmd = [sys.executable, str(script_path)] + extra_args
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error (código {e.returncode})")
        return False


def get_datasets(dataset_filter: str | None) -> list[str]:
    if dataset_filter:
        return [dataset_filter]
    return sorted([
        d.name for d in OUTPUTS.iterdir()
        if d.is_dir() and d.name != "general" and (d / "general").exists()
    ])


def get_fase2a_bases() -> list[str]:
    """Detecta los nombres base únicos en outputs/fase2/ (sin _t* ni _s*)."""
    import re
    fase2 = OUTPUTS / "fase2"
    if not fase2.exists():
        return []
    pattern = re.compile(r"^(.+)_t[\d.]+_s\d+$")
    bases = set()
    for d in fase2.iterdir():
        if not d.is_dir():
            continue
        m = pattern.match(d.name)
        if m and (d / "general").exists():
            bases.add(m.group(1))
    return sorted(bases)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenera los gráficos del proyecto")
    parser.add_argument(
        "--scope",
        choices=["per_dataset", "combined", "fase2a", "all"],
        default="all",
        help="Qué conjunto de gráficos regenerar (default: all)"
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="Para --scope per_dataset: limita a este dataset concreto"
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="SCRIPT",
        help="Regenera solo estos scripts (sin extensión .py)"
    )
    args = parser.parse_args()

    all_scripts = PER_DATASET_PLOTS + COMBINED_PLOTS
    if args.only:
        requested = [f"{s}.py" if not s.endswith(".py") else s for s in args.only]
        unknown = [s for s in requested if s not in all_scripts]
        if unknown:
            print(f"Scripts no reconocidos: {', '.join(unknown)}")
            print(f"Disponibles: {', '.join(s.replace('.py','') for s in all_scripts)}")
            sys.exit(1)
        per_dataset_run = [s for s in requested if s in PER_DATASET_PLOTS]
        combined_run    = [s for s in requested if s in COMBINED_PLOTS]
        fase2a_run      = False
    else:
        per_dataset_run = PER_DATASET_PLOTS if args.scope in ("per_dataset", "all") else []
        combined_run    = COMBINED_PLOTS    if args.scope in ("combined",    "all") else []
        fase2a_run      = args.scope in ("fase2a", "all")

    datasets = get_datasets(args.dataset)
    if not datasets and per_dataset_run:
        print(f"No se encontraron datasets en {OUTPUTS}")
        sys.exit(1)

    failed = []
    total  = 0

    # --- Per-dataset plots ---
    if per_dataset_run:
        for ds in datasets:
            print(f"\n{'='*55}")
            print(f"Dataset: {ds}")
            print(f"{'='*55}")
            for script in per_dataset_run:
                path = PLOTS_DIR / script
                print(f"  {script}")
                total += 1
                ok = run_script(path, ["--dataset", ds])
                if not ok:
                    failed.append(f"{ds}/{script}")

    # --- Combined plots ---
    if combined_run:
        print(f"\n{'='*55}")
        print("Combined (todos los datasets)")
        print(f"{'='*55}")
        for script in combined_run:
            path = PLOTS_DIR / script
            print(f"  {script}")
            total += 1
            ok = run_script(path, [])
            if not ok:
                failed.append(f"combined/{script}")

    # --- Fase 2A comparison plots ---
    if fase2a_run:
        bases = get_fase2a_bases()
        if not bases:
            print("\nNo se encontraron datasets de Fase 2A evaluados en outputs/fase2/")
        else:
            print(f"\n{'='*55}")
            print("Fase 2A — comparativa de temperaturas")
            print(f"{'='*55}")
            for base in bases:
                print(f"\n  Base: {base}")
                total += 1
                ok = run_script(FASE2A_SCRIPT, ["--base", base])
                if not ok:
                    failed.append(f"fase2a/{base}")

    print(f"\n{'='*55}")
    if failed:
        print(f"Completado con errores: {total - len(failed)}/{total} OK")
        for s in failed:
            print(f"  ✗ {s}")
        sys.exit(1)
    else:
        print(f"Todos los gráficos actualizados ({total}/{total})")
