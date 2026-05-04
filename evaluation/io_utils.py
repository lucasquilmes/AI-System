import pandas as pd


def load_excel_dataframe(excel_file, sheet_name):
    """Carga una hoja de un archivo Excel, intentando la primera hoja si la solicitada no existe."""
    try:
        return pd.read_excel(excel_file, sheet_name=sheet_name)
    except ValueError as e:
        if 'Worksheet named' in str(e) or 'Sheet' in str(e):
            xl = pd.ExcelFile(excel_file)
            first_sheet = xl.sheet_names[0]
            print(f"Hoja '{sheet_name}' no encontrada en {excel_file}. Usando hoja '{first_sheet}' en su lugar.")
            return pd.read_excel(excel_file, sheet_name=first_sheet)
        raise


def write_evaluation_results(output_file, results_df, summary_stats):
    """Escribe los resultados y el resumen en un archivo XLSX con dos hojas."""
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        results_df.to_excel(writer, sheet_name='Detalles', index=False)
        summary_stats.to_excel(writer, sheet_name='Resumen_Metricas', index=False)
