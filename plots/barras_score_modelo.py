"""Barras horizontales — Score compuesto por modelo (promedio entre técnicas)."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# Score compuesto
for col in ["sari_score_promedio", "rouge_l_promedio", "bleu_promedio", "flesch_generado_promedio"]:
    mn, mx = df[col].min(), df[col].max()
    df[col + "_n"] = (df[col] - mn) / (mx - mn)

for col in ["lmo_generado_promedio", "complex_words_ratio_promedio", "levenshtein_similarity_promedio"]:
    mn, mx = df[col].min(), df[col].max()
    df[col + "_n"] = 1 - (df[col] - mn) / (mx - mn)

norm_cols = [c + "_n" for c in [
    "sari_score_promedio", "rouge_l_promedio", "bleu_promedio",
    "flesch_generado_promedio", "lmo_generado_promedio",
    "complex_words_ratio_promedio", "levenshtein_similarity_promedio"
]]
df["composite"] = df[norm_cols].mean(axis=1)

# Score medio por modelo + desglose de métricas clave
model_composite = df.groupby("modelo")["composite"].mean().sort_values()
model_sari       = df.groupby("modelo")["sari_score_promedio"].mean()
model_flesch     = df.groupby("modelo")["flesch_generado_promedio"].mean()

palette = plt.cm.RdYlGn(np.linspace(0.2, 0.85, len(model_composite)))

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# Panel 1: score compuesto
bars = axes[0].barh(model_composite.index, model_composite.values,
                     color=palette, edgecolor="white", height=0.6)
for bar, val in zip(bars, model_composite.values):
    axes[0].text(val + 0.003, bar.get_y() + bar.get_height() / 2,
                 f"{val:.3f}", va="center", fontsize=8.5)
axes[0].set_title("Score compuesto", fontsize=11)
axes[0].set_xlabel("Score normalizado (0–1)", fontsize=9)
axes[0].axvline(model_composite.mean(), color="gray", linestyle="--", linewidth=1, alpha=0.7)
axes[0].grid(axis="x", alpha=0.3)
axes[0].tick_params(labelsize=9)

# Panel 2: SARI medio
sari_ord = model_sari.loc[model_composite.index]
bars2 = axes[1].barh(sari_ord.index, sari_ord.values,
                      color=palette, edgecolor="white", height=0.6)
for bar, val in zip(bars2, sari_ord.values):
    axes[1].text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}", va="center", fontsize=8.5)
axes[1].set_title("SARI medio", fontsize=11)
axes[1].set_xlabel("SARI (0–100)", fontsize=9)
axes[1].axvline(sari_ord.mean(), color="gray", linestyle="--", linewidth=1, alpha=0.7)
axes[1].grid(axis="x", alpha=0.3)
axes[1].tick_params(axis="y", labelleft=False)
axes[1].tick_params(axis="x", labelsize=9)

# Panel 3: Flesch medio
flesch_ord = model_flesch.loc[model_composite.index]
bars3 = axes[2].barh(flesch_ord.index, flesch_ord.values,
                      color=palette, edgecolor="white", height=0.6)
for bar, val in zip(bars3, flesch_ord.values):
    axes[2].text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}", va="center", fontsize=8.5)
axes[2].set_title("Flesch medio", fontsize=11)
axes[2].set_xlabel("Flesch Reading Ease", fontsize=9)
axes[2].axvline(flesch_ord.mean(), color="gray", linestyle="--", linewidth=1, alpha=0.7)
axes[2].axvline(65, color="#e74c3c", linestyle=":", linewidth=1.2, alpha=0.8)
axes[2].text(65.5, -0.5, "objetivo\n(65)", color="#e74c3c", fontsize=7.5)
axes[2].grid(axis="x", alpha=0.3)
axes[2].tick_params(axis="y", labelleft=False)
axes[2].tick_params(axis="x", labelsize=9)

fig.suptitle("Ranking de modelos — Score compuesto, SARI y Flesch\n(ordenados por score compuesto)", fontsize=13, y=1.02)
plt.tight_layout()
out = OUTPUT_DIR / "barras_score_modelo.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
