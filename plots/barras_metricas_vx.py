"""
Barras agrupadas — 7 métricas finales por modelo, filtrado a prompts v2-v6.
X: métrica  |  Y: valor medio (sin normalizar)  |  Color: modelo
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).parent))
from plot_config import get_config

DATA_DIR, OUTPUT_DIR = get_config()

VERSIONS = {"V4", "V5", "V6", "V7", "V8"}

METRICS = {
    "sari_score":            "SARI",
    "bert_score_f1":         "BERTScore",
    "flesch_ratio":          "Flesch\nratio",
    "compression_ratio_rel": "CR\nratio",
    "ttr_ratio":             "TTR\nratio",
    "cwr_ratio":             "CWR\nratio",
    "levenshtein_similarity":"Levenshtein\nsimilarity",
}

def load_raw():
    frames = []
    for f in sorted(DATA_DIR.glob("*.xlsx")):
        version = f.stem.replace("_general_results", "")
        if version.upper() not in VERSIONS:
            continue
        try:
            df = pd.read_excel(f, sheet_name="Detalles")
        except Exception:
            continue
        df["version"] = version
        frames.append(df)
    if not frames:
        raise FileNotFoundError(f"No se encontraron archivos para {VERSIONS} en {DATA_DIR}")
    return pd.concat(frames, ignore_index=True)

df = load_raw()

missing = [c for c in METRICS if c not in df.columns]
if missing:
    raise KeyError(f"Columnas no encontradas: {missing}")

model_means = df.groupby("modelo")[list(METRICS.keys())].mean()
model_means["sari_score"] = model_means["sari_score"] / 100

models = model_means.index.tolist()
n_models  = len(models)
n_metrics = len(METRICS)

colors = plt.cm.tab10(np.linspace(0, 0.9, n_models))

x = np.arange(n_metrics)
bar_width = 0.8 / n_models

fig, ax = plt.subplots(figsize=(13, 5.5))

for i, (model, color) in enumerate(zip(models, colors)):
    vals = [model_means.loc[model, col] for col in METRICS]
    offset = (i - n_models / 2 + 0.5) * bar_width
    ax.bar(x + offset, vals, width=bar_width * 0.92,
           color=color, label=model, edgecolor="white", linewidth=0.5)

ax.set_xticks(x)
ax.set_xticklabels(list(METRICS.values()), fontsize=10)
ax.set_ylabel("Valor medio", fontsize=10)
ax.set_title(
    "Métricas finales por modelo (prompts v4, v5, v6, v7, v8)",
    fontsize=12, pad=12
)
ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
ax.grid(axis="y", alpha=0.3)
ax.tick_params(axis="y", labelsize=9)

legend_patches = [mpatches.Patch(color=colors[i], label=m) for i, m in enumerate(models)]
ax.legend(handles=legend_patches, fontsize=8.5, loc="upper right",
          framealpha=0.85, ncol=2)

plt.tight_layout()
out = OUTPUT_DIR / "barras_metricas_vx.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
