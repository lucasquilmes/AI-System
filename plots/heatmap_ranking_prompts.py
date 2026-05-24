"""
Heatmap de ranking — técnicas/prompts × 7 métricas finales.
Cada celda = posición de la técnica en esa métrica (1 = mejor).
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
    "flesch_ratio":          "Flesch ratio",
    "compression_ratio_rel": "CR ratio",
    "ttr_ratio":             "TTR ratio",
    "cwr_ratio":             "CWR ratio",
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


df = load_raw()
version_means = df.groupby("version")[list(METRICS.keys())].mean()
version_means["sari_score"] = version_means["sari_score"] / 100

# Ordenar versiones alfabéticamente para consistencia visual
version_means = version_means.sort_index()

n_versions = len(version_means)
rank_df = pd.DataFrame(index=version_means.index)
for col in METRICS:
    if col in HIGHER_IS_BETTER:
        rank_df[col] = version_means[col].rank(ascending=False, method="min")
    else:
        rank_df[col] = version_means[col].sub(1).abs().rank(ascending=True, method="min")

cmap = mcolors.LinearSegmentedColormap.from_list("rg", ["#2ecc71", "#f9f9a0", "#e74c3c"])

fig, ax = plt.subplots(figsize=(10, 0.6 * n_versions + 2.5))

im = ax.imshow(rank_df.values, cmap=cmap, vmin=1, vmax=n_versions, aspect="auto")

ax.set_xticks(range(len(METRICS)))
ax.set_xticklabels(list(METRICS.values()), fontsize=10, rotation=20, ha="right")
ax.set_yticks(range(n_versions))
ax.set_yticklabels(rank_df.index, fontsize=9)

for i in range(n_versions):
    for j in range(len(METRICS)):
        rank_val = int(rank_df.iloc[i, j])
        mean_val = version_means.iloc[i, j]
        ax.text(j, i, f"#{rank_val}\n{mean_val:.3f}",
                ha="center", va="center", fontsize=7,
                color="black")

cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cbar.set_label("Ranking (1 = mejor)", fontsize=9)
cbar.set_ticks([1, n_versions])
cbar.set_ticklabels(["1 (mejor)", f"{n_versions} (peor)"])

ax.set_title("Ranking de técnicas/prompts por métrica\n(verde = mejor, rojo = peor)", fontsize=12, pad=12)
plt.tight_layout()

out = OUTPUT_DIR / "heatmap_ranking_prompts.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
