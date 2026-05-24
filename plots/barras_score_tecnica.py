"""Barras horizontales — Score compuesto por técnica (promedio entre modelos)."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).parent))
from plot_config import get_config

DATA_DIR, OUTPUT_DIR = get_config()

def load_summary(exclude_v0=True):
    frames = []
    for f in sorted(DATA_DIR.glob("*.xlsx")):
        version = f.stem.replace("_general_results", "")
        if exclude_v0 and version == "V0":
            continue
        df = pd.read_excel(f, sheet_name="Resumen_Metricas")
        df["version"] = version
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

df = load_summary()

# Métricas higher-better
for col in ["sari_score_promedio", "rouge_l_promedio", "bleu_promedio", "flesch_generado_promedio"]:
    mn, mx = df[col].min(), df[col].max()
    df[col + "_n"] = (df[col] - mn) / (mx - mn)

# Métricas lower-better
for col in ["lmo_generado_promedio", "complex_words_ratio_promedio", "levenshtein_similarity_promedio"]:
    mn, mx = df[col].min(), df[col].max()
    df[col + "_n"] = 1 - (df[col] - mn) / (mx - mn)

norm_cols = [c + "_n" for c in [
    "sari_score_promedio", "rouge_l_promedio", "bleu_promedio",
    "flesch_generado_promedio", "lmo_generado_promedio",
    "complex_words_ratio_promedio", "levenshtein_similarity_promedio"
]]
df["composite"] = df[norm_cols].mean(axis=1)

ranking = df.groupby("version")["composite"].mean().sort_values()

# Colores: verde para técnicas nuevas, azul para versiones base
VERSION_COLORS = {
    "V1": "#d9534f", "V2": "#5bc0de", "V3": "#5cb85c",
}
colors = [VERSION_COLORS.get(v, "#7b68ee") for v in ranking.index]

fig, ax = plt.subplots(figsize=(9, 7))
bars = ax.barh(ranking.index, ranking.values, color=colors, edgecolor="white", height=0.65)

# Etiquetas de valor
for bar, val in zip(bars, ranking.values):
    ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}", va="center", ha="left", fontsize=8.5)

ax.set_xlim(0, ranking.max() + 0.08)
ax.set_xlabel("Score compuesto normalizado (0–1)", fontsize=10)
ax.set_title("Ranking de técnicas de prompting\npor score compuesto (promedio entre modelos)", fontsize=13, pad=12)
ax.axvline(ranking.mean(), color="gray", linestyle="--", linewidth=1, alpha=0.7)
ax.text(ranking.mean() + 0.003, -0.6, "media", color="gray", fontsize=8)

legend_patches = [
    mpatches.Patch(color="#d9534f", label="V1 (brevedad extrema)"),
    mpatches.Patch(color="#5bc0de", label="V2 (equilibrio)"),
    mpatches.Patch(color="#5cb85c", label="V3 (nuevo)"),
    mpatches.Patch(color="#7b68ee", label="Técnicas de prompting"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=8)
ax.tick_params(axis="y", labelsize=9)
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
out = OUTPUT_DIR / "barras_score_tecnica.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
