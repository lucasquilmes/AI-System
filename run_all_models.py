#!/usr/bin/env python
"""
Script para ejecutar todos los modelos disponibles en una tarea específica.
Uso: python run_all_models.py --task v0 --from-row 0 --to-row 12
"""

import subprocess
import sys
import argparse
from config.models import MODEL_REGISTRY

def run_all_models(excel_file, sheet, task, from_row, to_row):
    """Ejecuta run_general.py para todos los modelos Ollama"""
    
    # Filtrar solo modelos Ollama
    ollama_models = [
        model for model, config in MODEL_REGISTRY.items() 
        if config.get("provider") == "ollama"
    ]
    
    print(f"Ejecutando {len(ollama_models)} modelos Ollama para la tarea '{task}'...")
    print(f"Modelos: {', '.join(ollama_models)}\n")
    
    failed_models = []
    successful_models = []
    
    for i, model in enumerate(ollama_models, 1):
        print(f"[{i}/{len(ollama_models)}] Ejecutando modelo: {model}")
        print("-" * 60)
        
        cmd = [
            sys.executable,
            "run_general.py",
            "--excel", excel_file,
            "--sheet", sheet,
            "--task", task,
            "--model", model,
            "--from-row", str(from_row),
            "--to-row", str(to_row)
        ]
        
        try:
            result = subprocess.run(cmd, check=True)
            successful_models.append(model)
            print(f"✓ {model} completado\n")
        except subprocess.CalledProcessError as e:
            failed_models.append(model)
            print(f"✗ {model} falló con código {e.returncode}\n")
    
    print("\n" + "=" * 60)
    print("RESUMEN DE EJECUCIÓN")
    print("=" * 60)
    print(f"Exitosos: {len(successful_models)}/{len(ollama_models)}")
    if successful_models:
        for model in successful_models:
            print(f"  ✓ {model}")
    
    if failed_models:
        print(f"\nFallidos: {len(failed_models)}/{len(ollama_models)}")
        for model in failed_models:
            print(f"  ✗ {model}")
    
    return len(failed_models) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ejecuta todos los modelos Ollama disponibles"
    )
    parser.add_argument(
        "--excel",
        default="data\\Test_poor.xlsx",
        help="Ruta del archivo Excel"
    )
    parser.add_argument(
        "--sheet",
        default="Hoja1",
        help="Nombre de la hoja Excel"
    )
    _ALL_TASKS = [
        "v0", "v1", "v2", "v3",
        "zero_shot", "few_shot", "role", "cot", "zs_cot",
        "tot", "self_cons", "self_ref", "ensemble", "meta",
    ]
    parser.add_argument(
        "--task",
        required=True,
        choices=_ALL_TASKS,
        help="Tarea a ejecutar"
    )
    parser.add_argument(
        "--from-row",
        type=int,
        default=0,
        help="Fila inicial"
    )
    parser.add_argument(
        "--to-row",
        type=int,
        default=12,
        help="Fila final"
    )
    
    args = parser.parse_args()
    
    success = run_all_models(
        args.excel,
        args.sheet,
        args.task,
        args.from_row,
        args.to_row
    )
    
    sys.exit(0 if success else 1)
