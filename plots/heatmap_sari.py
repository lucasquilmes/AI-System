"""Heatmap SARI — modelo x técnica (media por combinación)."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

pivot = df.pivot_table(
    values="sari_score_promedio",
    index="modelo",
    columns="version",
    aggfunc="mean"
).round(2)

# Ordenar columnas por media descendente
col_order = pivot.mean().sort_values(ascending=False).index
row_order  = pivot.mean(axis=1).sort_values(ascending=False).index
pivot = pivot.loc[row_order, col_order]

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(
    pivot,
    annot=True,
    fmt=".1f",
    cmap="YlGn",
    linewidths=0.5,
    linecolor="white",
    vmin=28,
    vmax=55,
    ax=ax,
    cbar_kws={"label": "SARI (0–100)"},
)
ax.set_title("SARI — Media por modelo y técnica\n(mayor = mejor preservación semántica)", fontsize=13, pad=12)
ax.set_xlabel("Técnica de prompting", fontsize=10)
ax.set_ylabel("Modelo", fontsize=10)
ax.tick_params(axis="x", rotation=30, labelsize=8)
ax.tick_params(axis="y", rotation=0, labelsize=9)

plt.tight_layout()
out = OUTPUT_DIR / "heatmap_sari.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
