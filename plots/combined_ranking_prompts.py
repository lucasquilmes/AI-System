"""
Combined — ranking de prompts en ambos datasets (side-by-side).
Columnas izquierda: test_poor  |  Columnas derecha: exemples_lectura_facil_formatted
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).parent))

PLOTS_DIR  = Path(__file__).parent
OUTPUT_DIR = PLOTS_DIR / "combined"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUTS = Path(__file__).parent.parent / "outputs"

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


def load_dataset(dataset_name: str, exclude_v0: bool = True) -> pd.DataFrame:
    data_dir = OUTPUTS / dataset_name / "general"
    frames = []
    for f in sorted(data_dir.glob("*.xlsx")):
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
        raise FileNotFoundError(f"No se encontraron archivos en {data_dir}")
    return pd.concat(frames, ignore_index=True)


def version_means(dataset_name: str) -> pd.DataFrame:
    df = load_dataset(dataset_name)
    means = df.groupby("version")[list(METRICS.keys())].mean()
    means["sari_score"] = means["sari_score"] / 100
    return means


def rank_matrix(means: pd.DataFrame) -> pd.DataFrame:
    rank_df = pd.DataFrame(index=means.index)
    for col in METRICS:
        if col in HIGHER_IS_BETTER:
            rank_df[col] = means[col].rank(ascending=False, method="min")
        else:
            rank_df[col] = means[col].sub(1).abs().rank(ascending=True, method="min")
    return rank_df


def combined_score(means: pd.DataFrame) -> pd.Series:
    scores = pd.DataFrame(index=means.index)
    for col in METRICS:
        if col in HIGHER_IS_BETTER:
            mn, mx = means[col].min(), means[col].max()
            scores[col] = (means[col] - mn) / (mx - mn) if mx != mn else 0.5
        else:
            dist = means[col].sub(1).abs()
            mn, mx = dist.min(), dist.max()
            scores[col] = 1 - (dist - mn) / (mx - mn) if mx != mn else 0.5
    return scores.mean(axis=1)


datasets = sorted([
    d.name for d in OUTPUTS.iterdir()
    if d.is_dir() and d.name != "general" and (d / "general").exists()
])

if len(datasets) < 2:
    print(f"Solo hay {len(datasets)} dataset(s) disponible(s): {datasets}")
    print("Este gráfico requiere al menos 2 datasets.")
    import sys; sys.exit(0)

ds_a, ds_b = datasets[0], datasets[1]
means_a = version_means(ds_a)
means_b = version_means(ds_b)

# Unión de prompts presentes en ambos, ordenados por score combinado del primer dataset
all_versions = sorted(set(means_a.index) | set(means_b.index))
means_a = means_a.reindex(all_versions)
means_b = means_b.reindex(all_versions)

# Ordenar filas por score combinado promedio entre los dos datasets
score_a = combined_score(means_a.dropna())
score_b = combined_score(means_b.dropna())
combined = (score_a.reindex(all_versions).fillna(0) + score_b.reindex(all_versions).fillna(0)) / 2
sorted_versions = combined.sort_values(ascending=False).index.tolist()

means_a = means_a.loc[sorted_versions]
means_b = means_b.loc[sorted_versions]

rank_a = rank_matrix(means_a.dropna(how="all"))
rank_b = rank_matrix(means_b.dropna(how="all"))
rank_a = rank_a.reindex(sorted_versions)
rank_b = rank_b.reindex(sorted_versions)

n_versions = len(sorted_versions)
n_metrics  = len(METRICS)
cmap = mcolors.LinearSegmentedColormap.from_list("rg", ["#2ecc71", "#f9f9a0", "#e74c3c"])

fig, axes = plt.subplots(1, 2, figsize=(20, 0.52 * n_versions + 3),
                          gridspec_kw={"wspace": 0.05})

for ax, rank_df, means, ds_name in [
    (axes[0], rank_a, means_a, ds_a),
    (axes[1], rank_b, means_b, ds_b),
]:
    im = ax.imshow(rank_df.values, cmap=cmap, vmin=1, vmax=n_versions, aspect="auto")
    ax.set_xticks(range(n_metrics))
    ax.set_xticklabels(list(METRICS.values()), fontsize=9, rotation=20, ha="right")
    ax.set_yticks(range(n_versions))
    ax.set_yticklabels(rank_df.index, fontsize=8)
    ax.set_title(ds_name.replace("_", " "), fontsize=11, pad=8)

    for i, ver in enumerate(sorted_versions):
        for j, col in enumerate(METRICS):
            if pd.isna(rank_df.loc[ver, col]) if ver in rank_df.index else True:
                ax.text(j, i, "N/A", ha="center", va="center", fontsize=6.5, color="gray")
            else:
                rank_val = int(rank_df.loc[ver, col])
                mean_val = means.loc[ver, col]
                ax.text(j, i, f"#{rank_val}\n{mean_val:.3f}",
                        ha="center", va="center", fontsize=6.5, color="black")

cbar = plt.colorbar(im, ax=axes, fraction=0.015, pad=0.01)
cbar.set_label("Ranking (1 = mejor)", fontsize=9)
cbar.set_ticks([1, n_versions])
cbar.set_ticklabels(["1 (mejor)", f"{n_versions} (peor)"])

fig.suptitle(
    "Ranking de prompts por dataset y métrica\n(verde = mejor · rojo = peor · ordenado por score combinado)",
    fontsize=13, y=1.01
)

out = OUTPUT_DIR / "combined_ranking_prompts.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Guardado: {out}")
