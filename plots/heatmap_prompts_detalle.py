"""
Heatmap detallado — prompts × 7 métricas finales.
Cada celda muestra el valor real. Color: verde = mejor rendimiento en esa métrica.
Filas ordenadas por puntuación combinada descendente.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).parent))
from plot_config import get_config

DATA_DIR, OUTPUT_DIR = get_config()

METRICS = {
    "sari_score":            "SARI",
    "bert_score_f1":         "BERTScore",
    "flesch_ratio":          "Flesch\nratio",
    "compression_ratio_rel": "CR\nratio",
    "ttr_ratio":             "TTR\nratio",
    "cwr_ratio":             "CWR\nratio",
    "levenshtein_similarity":"Levenshtein",
}

HIGHER_IS_BETTER = {"sari_score", "bert_score_f1", "levenshtein_similarity"}
CLOSER_TO_ONE    = {"flesch_ratio", "compression_ratio_rel", "ttr_ratio", "cwr_ratio"}


def load_raw(exclude_v0=True):
    frames = []
    for f in sorted(DATA_DIR.glob("*.xlsx")):
        version = f.stem.replace("_general_results", "")
        if exclude_v0 and version.upper() == "V0":
            continue
        try:
            df = pd.read_excel(f, sheet_name="Detalles")
            df["version"] = version
            frames.append(df)
        except Exception:
            continue
    if not frames:
        raise FileNotFoundError(f"No se encontraron archivos en {DATA_DIR}")
    return pd.concat(frames, ignore_index=True)


def score_column(series: pd.Series, col: str) -> pd.Series:
    """Normaliza a [0,1] donde 1 = mejor rendimiento."""
    if col in HIGHER_IS_BETTER:
        mn, mx = series.min(), series.max()
        if mx == mn:
            return pd.Series(0.5, index=series.index)
        return (series - mn) / (mx - mn)
    else:  # CLOSER_TO_ONE
        dist = series.sub(1).abs()
        mn, mx = dist.min(), dist.max()
        if mx == mn:
            return pd.Series(0.5, index=series.index)
        return 1 - (dist - mn) / (mx - mn)


df = load_raw()
version_means = df.groupby("version")[list(METRICS.keys())].mean()
version_means["sari_score"] = version_means["sari_score"] / 100

# Puntuación combinada para ordenar filas
score_parts = pd.DataFrame(index=version_means.index)
for col in METRICS:
    score_parts[col] = score_column(version_means[col], col)
version_means["_combined"] = score_parts.mean(axis=1)
version_means = version_means.sort_values("_combined", ascending=False)
version_means = version_means.drop(columns=["_combined"])

# Matriz de color normalizada por columna
color_matrix = np.zeros((len(version_means), len(METRICS)))
for j, col in enumerate(METRICS):
    color_matrix[:, j] = score_column(version_means[col], col).values

cmap = mcolors.LinearSegmentedColormap.from_list("rg", ["#e74c3c", "#f9f9a0", "#2ecc71"])

n_versions = len(version_means)
n_metrics  = len(METRICS)

fig, ax = plt.subplots(figsize=(11, 0.52 * n_versions + 3))

im = ax.imshow(color_matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

ax.set_xticks(range(n_metrics))
ax.set_xticklabels(list(METRICS.values()), fontsize=10, rotation=0, ha="center")
ax.set_yticks(range(n_versions))
ax.set_yticklabels(version_means.index, fontsize=9)

for i in range(n_versions):
    for j, col in enumerate(METRICS):
        val = version_means.iloc[i][col]
        brightness = color_matrix[i, j]
        txt_color = "black" if 0.2 < brightness < 0.85 else ("white" if brightness <= 0.2 else "black")
        ax.text(j, i, f"{val:.3f}",
                ha="center", va="center", fontsize=8.5,
                color=txt_color, fontweight="bold")

cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label("Rendimiento relativo", fontsize=9)
cbar.set_ticks([0, 0.5, 1])
cbar.set_ticklabels(["Peor", "Medio", "Mejor"])

ax.set_title(
    "Puntuaciones detalladas por prompt y métrica\n"
    "(ordenado por puntuación combinada · verde = mejor · rojo = peor)",
    fontsize=12, pad=12
)

plt.tight_layout()
out = OUTPUT_DIR / "heatmap_prompts_detalle.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
