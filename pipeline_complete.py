#!/usr/bin/env python
"""
Script maestro para ejecutar generación + evaluación de una versión completa.
Uso: python pipeline_complete.py --version v0
"""

import subprocess
import sys
import argparse
def run_command(cmd, description):
    """Ejecuta un comando y retorna True si es exitoso"""
    print(f"\n{'='*60}")
    print(f"[{description}]")
    print('='*60)

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ {description} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} falló con código {e.returncode}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline completo: generar + evaluar para una versión"
    )
    _ALL_VERSIONS = [
        "v0", "v1", "v2", "v3",
        "zero_shot", "few_shot", "role", "cot", "zs_cot",
        "tot", "self_cons", "self_ref", "ensemble", "meta",
    ]
    parser.add_argument(
        "--version",
        required=True,
        choices=_ALL_VERSIONS,
        help="Version a procesar"
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
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Omitir fase de generación, solo evaluar"
    )
    parser.add_argument(
        "--skip-evaluation",
        action="store_true",
        help="Omitir fase de evaluación, solo generar"
    )
    
    args = parser.parse_args()
    
    python_exe = sys.executable
    version = args.version
    from_row = args.from_row
    to_row = args.to_row
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║          PIPELINE COMPLETO - Versión {version.upper()}                    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    results = {"generación": False, "evaluación": False}
    
    # FASE 1: GENERACIÓN
    if not args.skip_generation:
        cmd = [
            python_exe,
            "run_all_models.py",
            "--task", version,
            "--from-row", str(from_row),
            "--to-row", str(to_row)
        ]
        results["generación"] = run_command(cmd, f"GENERACIÓN: Ejecutando todos los modelos para {version}")
    
    # FASE 2: EVALUACIÓN
    if not args.skip_evaluation:
        cmd = [
            python_exe,
            "evaluation/evaluate_excel.py",
            "--version", version
        ]
        results["evaluación"] = run_command(cmd, f"EVALUACIÓN: Calculando SARI para {version}")
    
    # RESUMEN FINAL
    print(f"\n{'='*60}")
    print("RESUMEN DEL PIPELINE")
    print('='*60)
    print(f"Versión:       {version.upper()}")
    print(f"Generación:    {'✓ EXITOSA' if results['generación'] else '⊘ OMITIDA' if args.skip_generation else '✗ FALLÓ'}")
    print(f"Evaluación:    {'✓ EXITOSA' if results['evaluación'] else '⊘ OMITIDA' if args.skip_evaluation else '✗ FALLÓ'}")
    
    if results["generación"] or args.skip_generation:
        print(f"\nResultados guardados en:")
        print(f"  - Generación: outputs/{version}/{{modelo}}/results.xlsx")
    
    if results["evaluación"] or args.skip_evaluation:
        print(f"  - Evaluación: outputs/general/{version.upper()}_general_results.xlsx")
    
    all_success = all(results.values())
    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()
