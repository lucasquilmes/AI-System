# seleccion de filas a evaluar, formato: "1,3,5-7"
def parse_row_selection(row_selection):
    """Parsea un string de filas seleccionadas en un conjunto de índices 1-based."""
    if not row_selection:
        return None

    selected_rows = set()
    for part in str(row_selection).split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start.strip())
            end = int(end.strip())
            selected_rows.update(range(start, end + 1))
        else:
            selected_rows.add(int(part))

    return selected_rows
