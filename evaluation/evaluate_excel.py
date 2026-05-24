# Punto de entrada CLI para ejecutar la evaluación completa de una versión.
# Uso desde la raíz del proyecto:
#   python evaluation/evaluate_excel.py --version v0
#   python evaluation/evaluate_excel.py --version v2 --skip-bert --skip-ner
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluation.row_selection import parse_row_selection
from evaluation.evaluator import evaluate_version


def main():
    parser = argparse.ArgumentParser(
        description="Evalúa todas las métricas para una versión y todos sus modelos."
    )
    _VERSIONS = [
        "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "audit", "motor",
        "zero_shot", "few_shot", "role", "cot", "zs_cot",
        "tot", "self_cons", "self_ref", "ensemble", "meta",
    ]
    parser.add_argument("--version", default="v0", choices=_VERSIONS,
                        help="Versión a evaluar")
    parser.add_argument("--sheet", default="Sheet1",
                        help="Nombre de la hoja Excel")
    parser.add_argument("--col-original", default="normal text",
                        help="Columna con texto original")
    parser.add_argument("--col-generado", default="output",
                        help="Columna con texto generado por el modelo")
    parser.add_argument("--col-referencias", default="ground truth",
                        help="Columna con la referencia (ground truth)")
    parser.add_argument("--rows", default=None,
                        help="Filas a evaluar (1-based). Ej: 2,4 o 2-5")
    parser.add_argument("--skip-bert", action="store_true",
                        help="Omite BertScore (~700 MB de modelo, lento)")
    parser.add_argument("--skip-ner", action="store_true",
                        help="Omite NER density (requiere spaCy es_core_news_sm)")
    parser.add_argument("--dataset", default="test_poor",
                        help="Nombre del dataset (subcarpeta dentro de outputs/)")

    args = parser.parse_args()
    row_selection = parse_row_selection(args.rows)

    try:
        stats = evaluate_version(
            version=args.version,
            sheet=args.sheet,
            col_original=args.col_original,
            col_generado=args.col_generado,
            col_referencias=args.col_referencias,
            dataset=args.dataset,
            row_selection=row_selection,
            skip_bert=args.skip_bert,
            skip_ner=args.skip_ner,
        )

        print(f"\nEvaluacion completada -> {stats['output_file']}")
        print(
            f"Filas: leídas={stats['total_rows']}  "
            f"añadidas={stats['added_rows']}  "
            f"descartadas={stats['skipped_rows']} "
            f"(sin texto={stats['skipped_no_text']}, filtro={stats['skipped_filter']})"
        )


        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
