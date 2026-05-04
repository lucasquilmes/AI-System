# Orquestador principal de evaluación: itera sobre todos los modelos de una versión,
# calcula todas las métricas configuradas por fila y construye el DataFrame de resultados.
import pandas as pd
from pathlib import Path

from evaluation.filters import should_add_result
from evaluation.io_utils import load_excel_dataframe, write_evaluation_results
from evaluation.summary_metrics import build_summary_stats
from evaluation.metrics import (
    get_sari_metric,
    calcular_sari,
    calcular_flesch,
    calcular_bert_score,
    calcular_rouge_l,
    calcular_bleu,
    calcular_compression_ratio,
    calcular_lmo,
    calcular_ttr,
    calcular_complex_words_ratio,
    calcular_ner_density,
    calcular_levenshtein_normalizada,
)


def evaluate_version(
    version,
    sheet,
    col_original,
    col_generado,
    col_referencias,
    row_selection=None,
    skip_bert=False,
    skip_ner=False,
):
    base_dir = Path("outputs") / version
    general_dir = Path("outputs") / "general"
    general_dir.mkdir(parents=True, exist_ok=True)
    output_file = general_dir / f"{version.upper()}_general_results.xlsx"

    all_results = []
    total_rows = added_rows = skipped_rows = skipped_no_text = skipped_filter = 0

    try:
        get_sari_metric()
    except RuntimeError as e:
        raise

    if not base_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta {base_dir}")

    for model_dir in sorted(base_dir.iterdir()):
        if not model_dir.is_dir() or model_dir.name == "general":
            continue

        model_name = model_dir.name
        excel_file = model_dir / "results.xlsx"

        if not excel_file.exists():
            print(f"  [!] No se encontró results.xlsx en {model_dir}")
            continue

        print(f"Evaluando modelo: {model_name}")

        try:
            df = load_excel_dataframe(excel_file, sheet)
        except Exception as e:
            print(f"  [!] Error al leer {excel_file}: {e}")
            continue

        required_cols = [col_original, col_generado, col_referencias]
        if not all(col in df.columns for col in required_cols):
            print(f"  [!] Columnas faltantes en {excel_file}. Saltando.")
            continue

        for row_number, (_, row) in enumerate(df.iterrows(), start=1):
            if row_selection and row_number not in row_selection:
                continue

            total_rows += 1
            texto_original = str(row[col_original])
            texto_generado = str(row[col_generado])
            referencias = str(row[col_referencias])

            if not texto_original.strip() or not texto_generado.strip() or not referencias.strip():
                skipped_rows += 1
                skipped_no_text += 1
                continue

            # --- Métricas basadas en referencia ---
            try:
                sari_score = calcular_sari(texto_original, texto_generado, referencias)
            except Exception as e:
                print(f"  [!] Error SARI {model_name} fila {row_number}: {e}")
                sari_score = None

            flesch_original = calcular_flesch(texto_original)
            flesch_generado = calcular_flesch(texto_generado)
            flesch_referencias = calcular_flesch(referencias)

            if not should_add_result(sari_score, flesch_generado):
                skipped_rows += 1
                skipped_filter += 1
                continue

            rouge_l = calcular_rouge_l(texto_generado, referencias)
            bleu = calcular_bleu(texto_generado, referencias)
            levenshtein = calcular_levenshtein_normalizada(texto_original, texto_generado)

            # --- Métricas de síntesis y superficie ---
            compression_ratio = calcular_compression_ratio(texto_original, texto_generado)
            lmo_original = calcular_lmo(texto_original)
            lmo_generado = calcular_lmo(texto_generado)
            ttr = calcular_ttr(texto_generado)
            complex_words_ratio = calcular_complex_words_ratio(texto_generado)

            # --- Métricas pesadas (opcionales via --skip-bert / --skip-ner) ---
            bert_score_f1 = None
            if not skip_bert:
                try:
                    bert_score_f1 = calcular_bert_score(texto_generado, referencias)
                except Exception as e:
                    print(f"  [!] Error BertScore {model_name} fila {row_number}: {e}")

            ner_density_original = ner_density_generado = None
            if not skip_ner:
                try:
                    ner_density_original = calcular_ner_density(texto_original)
                    ner_density_generado = calcular_ner_density(texto_generado)
                except Exception as e:
                    print(f"  [!] Error NER {model_name} fila {row_number}: {e}")

            all_results.append({
                "modelo": model_name,
                "row_index": row_number,
                # Basadas en referencia
                "sari_score": sari_score,
                "rouge_l": rouge_l,
                "bleu": bleu,
                "bert_score_f1": bert_score_f1,
                "levenshtein_normalizada": levenshtein,
                # Legibilidad
                "flesch_original": flesch_original,
                "flesch_generado": flesch_generado,
                "flesch_referencias": flesch_referencias,
                # Síntesis y superficie
                "compression_ratio": compression_ratio,
                "lmo_original": lmo_original,
                "lmo_generado": lmo_generado,
                "ttr": ttr,
                "complex_words_ratio": complex_words_ratio,
                # NER (opcionales)
                "ner_density_original": ner_density_original,
                "ner_density_generado": ner_density_generado,
                # Textos
                "texto_original": texto_original,
                "texto_generado": texto_generado,
                "referencias": referencias,
            })
            added_rows += 1

    results_df = pd.DataFrame(all_results)
    summary_stats = build_summary_stats(results_df)
    write_evaluation_results(output_file, results_df, summary_stats)

    return {
        "output_file": output_file,
        "results_df": results_df,
        "summary_stats": summary_stats,
        "total_rows": total_rows,
        "added_rows": added_rows,
        "skipped_rows": skipped_rows,
        "skipped_no_text": skipped_no_text,
        "skipped_filter": skipped_filter,
    }
