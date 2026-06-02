"""Helper para que todos los scripts de plots resuelvan DATA_DIR y OUTPUT_DIR por dataset."""
import argparse
from pathlib import Path


def get_config():
    """Devuelve (data_dir, output_dir) según --dataset.

    data_dir   → outputs/<dataset>/general/
    output_dir → plots/<dataset>/          (se crea si no existe)
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--dataset", default=None)
    args, _ = parser.parse_known_args()

    root = Path(__file__).parent.parent
    outputs   = root / "outputs"
    plots_dir = Path(__file__).parent

    if args.dataset:
        dataset_name = args.dataset
    else:
        datasets = sorted([
            d for d in outputs.iterdir()
            if d.is_dir() and d.name != "general" and (d / "general").exists()
        ])
        if not datasets:
            raise FileNotFoundError(f"No se encontraron datasets en {outputs}")
        if len(datasets) > 1:
            print(f"Datasets disponibles: {[d.name for d in datasets]}")
            print(f"Usando: {datasets[0].name}  (usa --dataset <nombre> para cambiar)")
        dataset_name = datasets[0].name

    data_dir   = outputs / dataset_name / "general"
    output_dir = plots_dir / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return data_dir, output_dir


def get_data_dir() -> Path:
    data_dir, _ = get_config()
    return data_dir
