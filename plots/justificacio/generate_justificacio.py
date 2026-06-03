"""
Genera els grafics de justificacio de decisions per Fase 1 i Fase 2A.
Sortida: plots/justificacio/
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path

ROOT    = Path(__file__).parent.parent.parent
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

METRICS = {
    "sari_score_promedio":             "higher",
    "bert_score_f1_promedio":          "higher",
    "levenshtein_similarity_promedio": "higher",
    "flesch_ratio_promedio":           "closer1",
    "compression_ratio_rel_promedio":  "closer1",
    "ttr_ratio_promedio":              "closer1",
    "cwr_ratio_promedio":              "closer1",
}

MODEL_LABELS = {
    "llama3.3":        "llama3.3\n(70B)",
    "gemma2_27b":      "gemma2\n(27B)",
    "aya-expanse_32b": "aya-expanse\n(32B)",
    "qwen2.5_32b":     "qwen2.5\n(32B)",
    "mistral-nemo":    "mistral-nemo\n(12B)",
    "llama3.1_8b":     "llama3.1\n(8B)",
    "command-r":       "command-r\n(35B)",
    "mixtral":         "mixtral\n(47B)",
}
MODEL_ORDER = ["llama3.3","gemma2_27b","aya-expanse_32b","qwen2.5_32b",
               "mistral-nemo","llama3.1_8b","command-r","mixtral"]

DS_SHORT = {
    "test_poor":                        "PAGE_DS",
    "exemples_lectura_facil_formatted": "exemples",
}


def load_fase1():
    frames = []
    for ds in ["test_poor", "exemples_lectura_facil_formatted"]:
        for xlsx in sorted((ROOT / "outputs" / ds / "general").glob("*.xlsx")):
            prompt = xlsx.stem.replace("_general_results", "").upper()
            try:
                df = pd.read_excel(xlsx, sheet_name="Resumen_Metricas")
                df["prompt"]  = prompt
                df["dataset"] = DS_SHORT[ds]
                frames.append(df)
            except Exception:
                pass
    all_df = pd.concat(frames, ignore_index=True)
    all_df["sari_score_promedio"] /= 100
    parts = []
    for col, direction in METRICS.items():
        if direction == "higher":
            mn, mx = all_df[col].min(), all_df[col].max()
            parts.append((all_df[col]-mn)/(mx-mn) if mx > mn else pd.Series(0.5, index=all_df.index))
        else:
            dist = (all_df[col]-1).abs()
            mn, mx = dist.min(), dist.max()
            parts.append(1-(dist-mn)/(mx-mn) if mx > mn else pd.Series(0.5, index=all_df.index))
    all_df["score"] = pd.concat(parts, axis=1).mean(axis=1)
    all_df["sari_score_promedio"] *= 100
    return all_df


def load_fase2():
    import re
    frames = []
    pattern = re.compile(r"^(.+)_t([\d.]+)_s(\d+)$")
    for folder in sorted((ROOT / "outputs" / "fase2").iterdir()):
        m = pattern.match(folder.name)
        if not m: continue
        base, temp, seed = m.group(1), float(m.group(2)), int(m.group(3))
        if seed != 42: continue
        general = folder / "general"
        if not general.exists(): continue
        for xlsx in sorted(general.glob("*.xlsx")):
            version = xlsx.stem.replace("_general_results", "").upper()
            try:
                df = pd.read_excel(xlsx, sheet_name="Resumen_Metricas")
                df["temperature"] = temp
                df["version"]     = version
                df["dataset"]     = DS_SHORT.get(base, base)
                frames.append(df)
            except Exception:
                pass
    if not frames:
        return pd.DataFrame()
    all_df = pd.concat(frames, ignore_index=True)
    all_df["sari_score_promedio"] /= 100
    parts = []
    for col, direction in METRICS.items():
        if direction == "higher":
            mn, mx = all_df[col].min(), all_df[col].max()
            parts.append((all_df[col]-mn)/(mx-mn) if mx > mn else pd.Series(0.5, index=all_df.index))
        else:
            dist = (all_df[col]-1).abs()
            mn, mx = dist.min(), dist.max()
            parts.append(1-(dist-mn)/(mx-mn) if mx > mn else pd.Series(0.5, index=all_df.index))
    all_df["score"] = pd.concat(parts, axis=1).mean(axis=1)
    all_df["sari_score_promedio"] *= 100
    return all_df


def plot_j1(df):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    colors_ds = {"PAGE_DS": "#2196F3", "exemples": "#FF9800"}
    for ax, (label, sub) in zip(axes[:2], [
        ("PAGE_DS", df[df.dataset == "PAGE_DS"]),
        ("exemples", df[df.dataset == "exemples"]),
    ]):
        means = sub.groupby("modelo")["score"].mean().reindex(MODEL_ORDER)
        bars  = ax.barh([MODEL_LABELS.get(m, m) for m in MODEL_ORDER],
                        means.values, color=colors_ds[label], edgecolor="white", height=0.6)
        for bar, v in zip(bars, means.values):
            ax.text(bar.get_width()+0.003, bar.get_y()+bar.get_height()/2,
                    f"{v:.3f}", va="center", fontsize=9)
        ax.set_title(f"Dataset: {label}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Score compost [0-1]", fontsize=9)
        ax.set_xlim(0, 1.0)
        ax.axvline(0.70, color="grey", linestyle="--", alpha=0.4, linewidth=1)
        ax.grid(axis="x", alpha=0.3)
    ax = axes[2]
    means_g = df.groupby("modelo")["score"].mean().reindex(MODEL_ORDER)
    palette = ["#00467F" if m in ["llama3.3","gemma2_27b"] else "#90CAF9" for m in MODEL_ORDER]
    bars = ax.barh([MODEL_LABELS.get(m, m) for m in MODEL_ORDER],
                   means_g.values, color=palette, edgecolor="white", height=0.6)
    for bar, v in zip(bars, means_g.values):
        ax.text(bar.get_width()+0.003, bar.get_y()+bar.get_height()/2,
                f"{v:.3f}", va="center", fontsize=9, fontweight="bold")
    ax.set_title("Global (tots 2 datasets)", fontsize=11, fontweight="bold")
    ax.set_xlabel("Score compost [0-1]", fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.axvline(0.70, color="grey", linestyle="--", alpha=0.4, linewidth=1)
    ax.grid(axis="x", alpha=0.3)
    fig.suptitle("Score compost per model - Comparativa entre datasets",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    out = OUT_DIR / "j1_score_per_model.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j2(df):
    GROUPS = {
        "V0":"Versio propia","V1":"Versio propia","V2":"Versio propia",
        "V3":"Versio propia","V4":"Versio propia","V5":"Versio propia",
        "V6":"Versio propia","V7":"Versio propia","V8":"Versio propia",
        "ZERO_SHOT":"Estandard","ZS_COT":"Estandard","FEW_SHOT":"Estandard",
        "ROLE":"Estandard","COT":"Estandard","TOT":"Estandard",
        "SELF_CONS":"Estandard","SELF_REF":"Estandard","ENSEMBLE":"Estandard",
        "META":"Estandard","MOTOR":"Domini","AUDIT":"Domini",
    }
    GROUP_COLORS = {"Versio propia":"#00467F","Estandard":"#4CAF50","Domini":"#FF9800"}
    means  = df.groupby("prompt")["score"].mean().sort_values(ascending=True)
    colors = [GROUP_COLORS.get(GROUPS.get(p,"Estandard"),"grey") for p in means.index]
    fig, ax = plt.subplots(figsize=(9, 8))
    bars = ax.barh(means.index, means.values, color=colors, edgecolor="white", height=0.7)
    for bar, v in zip(bars, means.values):
        ax.text(bar.get_width()+0.003, bar.get_y()+bar.get_height()/2,
                f"{v:.3f}", va="center", fontsize=8.5)
    ax.set_xlabel("Score compost mitja [0-1]", fontsize=10)
    ax.set_title("Score compost per tecnica de prompting", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 1.0)
    ax.axvline(0.70, color="grey", linestyle="--", alpha=0.4, linewidth=1)
    ax.grid(axis="x", alpha=0.3)
    from matplotlib.patches import Patch
    legend = [Patch(color=c, label=l) for l, c in GROUP_COLORS.items()]
    ax.legend(handles=legend, loc="lower right", fontsize=9)
    plt.tight_layout()
    out = OUT_DIR / "j2_score_per_prompt.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j3(df):
    pivot = df.groupby(["modelo","prompt"])["score"].mean().unstack()
    pivot = pivot.reindex(MODEL_ORDER)
    prompt_order = df.groupby("prompt")["score"].mean().sort_values(ascending=False).index.tolist()
    pivot = pivot[prompt_order]
    cmap = mcolors.LinearSegmentedColormap.from_list("rg", ["#e74c3c","#f9f9a0","#2ecc71"])
    fig, ax = plt.subplots(figsize=(18, 5))
    im = ax.imshow(pivot.values, cmap=cmap, vmin=0.3, vmax=0.95, aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([MODEL_LABELS.get(m, m).replace("\n"," ") for m in pivot.index], fontsize=9)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.iloc[i, j]
            if pd.isna(val): continue
            col = "black" if 0.4 < val < 0.85 else "white"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", fontsize=7.5, color=col)
    plt.colorbar(im, ax=ax, fraction=0.02, label="Score compost [0-1]")
    ax.set_title("Heatmap score compost - Model x Prompt (2 datasets)",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    out = OUT_DIR / "j3_heatmap_model_prompt.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j4(df):
    means = df.groupby(["modelo","dataset"])["score"].mean().unstack()
    means = means.reindex(MODEL_ORDER)
    x, w = np.arange(len(MODEL_ORDER)), 0.35
    fig, ax = plt.subplots(figsize=(12, 5))
    b1 = ax.bar(x - w/2, means["PAGE_DS"].values, w, label="PAGE_DS",
                color="#2196F3", edgecolor="white")
    b2 = ax.bar(x + w/2, means["exemples"].values, w, label="exemples",
                color="#FF9800", edgecolor="white")
    for bar in list(b1) + list(b2):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005,
                f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_LABELS.get(m,m).replace("\n"," ") for m in MODEL_ORDER], fontsize=9)
    ax.set_ylabel("Score compost [0-1]", fontsize=10)
    ax.set_ylim(0, 0.88)
    ax.set_title("Score compost per model i dataset", fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.axhline(0.68, color="grey", linestyle="--", alpha=0.4, linewidth=1)
    for xi in [0, 1]:
        ax.axvspan(xi - 0.5, xi + 0.5, alpha=0.06, color="#00467F")
    plt.tight_layout()
    out = OUT_DIR / "j4_model_per_dataset.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j5(df):
    highlight = {"llama3.3","gemma2_27b"}
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, ds in zip(axes, ["PAGE_DS","exemples"]):
        sub = df[df["dataset"]==ds]
        c   = sub["modelo"].apply(lambda m: "#00467F" if m in highlight else "#BBBBBB")
        s   = sub["modelo"].apply(lambda m: 60 if m in highlight else 25)
        ax.scatter(sub["sari_score_promedio"], sub["levenshtein_similarity_promedio"],
                   c=c, s=s, alpha=0.7, edgecolors="white", linewidth=0.5)
        top = sub.nlargest(5, "score")
        for _, row in top.iterrows():
            ax.annotate(f"{row.modelo.split('_')[0][:6]}+{row.prompt}",
                        (row["sari_score_promedio"], row["levenshtein_similarity_promedio"]),
                        textcoords="offset points", xytext=(5, 3), fontsize=7, color="#00467F")
        ax.set_xlabel("SARI", fontsize=10)
        ax.set_ylabel("Levenshtein similarity", fontsize=10)
        ax.set_title(f"Dataset: {ds}", fontsize=11, fontweight="bold")
        ax.grid(alpha=0.3)
    from matplotlib.lines import Line2D
    legend = [
        Line2D([0],[0],marker="o",color="w",markerfacecolor="#00467F",markersize=8,label="llama3.3 / gemma2"),
        Line2D([0],[0],marker="o",color="w",markerfacecolor="#BBBBBB",markersize=6,label="Altres models"),
    ]
    fig.legend(handles=legend, loc="lower center", ncol=2, fontsize=9, bbox_to_anchor=(0.5,-0.02))
    fig.suptitle("Relacio entre SARI i similitud de Levenshtein per model i dataset",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    out = OUT_DIR / "j5_scatter_sari_lev.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j6(df):
    tp = df[df.dataset=="PAGE_DS"].groupby(["modelo","prompt"])["score"].mean()
    ex = df[df.dataset=="exemples"].groupby(["modelo","prompt"])["score"].mean()
    gap_df = pd.DataFrame({"PAGE_DS": tp, "exemples": ex}).dropna()
    gap_df["mean"] = gap_df.mean(axis=1)
    gap_df["gap"]  = (gap_df["PAGE_DS"] - gap_df["exemples"]).abs()
    gap_df = gap_df.sort_values("mean", ascending=False).head(15)
    labels = [f"{m.split('_')[0][:7]}+{p}" for (m,p) in gap_df.index]
    x, w = np.arange(len(labels)), 0.32
    fig, ax = plt.subplots(figsize=(14, 5))
    b1 = ax.bar(x - w, gap_df["PAGE_DS"].values, w, label="PAGE_DS",  color="#2196F3", edgecolor="white")
    b2 = ax.bar(x,     gap_df["exemples"].values, w, label="exemples", color="#FF9800", edgecolor="white")
    b3 = ax.bar(x + w, gap_df["gap"].values,      w, label="Gap (|d|)",color="#E91E63", alpha=0.8, edgecolor="white")
    for b in list(b1)+list(b2)+list(b3):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005,
                f"{b.get_height():.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("Score compost [0-1]", fontsize=10)
    ax.set_ylim(0, 1.05)
    ax.set_title("Score i gap inter-dataset - Top-15 configuracions per score mitja",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    for i, (m,p) in enumerate(gap_df.index):
        if m == "llama3.3" and p == "V8":
            ax.axvspan(i-0.5, i+0.5, alpha=0.1, color="#00467F")
            ax.text(i, 1.01, "* Recomanat", ha="center", fontsize=8,
                    color="#00467F", fontweight="bold")
    plt.tight_layout()
    out = OUT_DIR / "j6_gap_cross_dataset.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j7(df2):
    if df2.empty:
        print("  ! j7: dades Fase 2A no disponibles"); return
    temps  = sorted(df2["temperature"].unique())
    styles = {"llama3.3":{"color":"#00467F","marker":"o"},
              "gemma2_27b":{"color":"#FF9800","marker":"s"}}
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    for ax, ds in zip(axes, ["PAGE_DS","exemples"]):
        sub = df2[df2["dataset"]==ds]
        for model, style in styles.items():
            msub   = sub[sub["modelo"]==model]
            mean_t = msub.groupby("temperature")["score"].mean().reindex(temps)
            ax.plot(temps, mean_t.values, marker=style["marker"], linewidth=2.5,
                    color=style["color"], label=model, markersize=7)
            for t, s in zip(temps, mean_t.values):
                if not np.isnan(s):
                    ax.annotate(f"{s:.3f}", (t, s), textcoords="offset points",
                                xytext=(0, 8), ha="center", fontsize=8, color=style["color"])
        ax.set_title(f"Dataset: {ds}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Temperatura", fontsize=10)
        ax.set_xticks(temps)
        ax.set_ylim(0, 0.85)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Score compost [0-1]", fontsize=10)
    fig.suptitle("Evolucio del score compost per temperatura - Fase 2A",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    out = OUT_DIR / "j7_score_vs_temp.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j8(df2):
    if df2.empty:
        print("  ! j8: dades Fase 2A no disponibles"); return
    sub   = df2[(df2["modelo"]=="llama3.3") & (df2["version"]=="V8")]
    tp    = sub[sub["dataset"]=="PAGE_DS"].set_index("temperature")["score"]
    ex    = sub[sub["dataset"]=="exemples"].set_index("temperature")["score"]
    temps = sorted(sub["temperature"].unique())
    tp_v  = [tp.get(t, np.nan) for t in temps]
    ex_v  = [ex.get(t, np.nan) for t in temps]
    gap_v = [abs(a-b) if not (np.isnan(a) or np.isnan(b)) else np.nan for a,b in zip(tp_v,ex_v)]
    x, w  = np.arange(len(temps)), 0.28
    fig, ax = plt.subplots(figsize=(8, 5))
    b1 = ax.bar(x-w, tp_v,  w, label="PAGE_DS", color="#2196F3", edgecolor="white")
    b2 = ax.bar(x,   ex_v,  w, label="exemples",color="#FF9800", edgecolor="white")
    b3 = ax.bar(x+w, gap_v, w, label="Gap",     color="#E91E63", alpha=0.8, edgecolor="white")
    for bars in [b1, b2, b3]:
        for b in bars:
            if b.get_height() > 0:
                ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005,
                        f"{b.get_height():.3f}", ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(x)
    ax.set_xticklabels([f"T={t}" for t in temps], fontsize=10)
    ax.set_ylabel("Score compost [0-1]", fontsize=10)
    ax.set_ylim(0, 0.88)
    ax.set_title("Score i gap inter-dataset per temperatura - llama3.3 + V8",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    out = OUT_DIR / "j8_gap_per_temperatura.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


def plot_j9(df2):
    if df2.empty:
        print("  ! j9: dades Fase 2A no disponibles"); return
    sub  = df2[(df2["modelo"]=="llama3.3") & (df2["temperature"]==0.0)]
    data = {}
    for ds in ["PAGE_DS","exemples"]:
        for v in ["V8","COT"]:
            r = sub[(sub["dataset"]==ds) & (sub["version"]==v)]
            data[(ds,v)] = r["score"].mean() if len(r) else np.nan
    datasets = ["PAGE_DS","exemples"]
    x, w = np.arange(len(datasets)), 0.35
    colors_p = {"V8":"#00467F","COT":"#4CAF50"}
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, prompt in enumerate(["V8","COT"]):
        vals = [data[(ds,prompt)] for ds in datasets]
        bars = ax.bar(x + (i-0.5)*w, vals, w, label=prompt,
                      color=colors_p[prompt], edgecolor="white")
        for b, v in zip(bars, vals):
            if not np.isnan(v):
                ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=11)
    ax.set_ylabel("Score compost [0-1]", fontsize=10)
    ax.set_ylim(0, 0.78)
    ax.set_title("Comparativa V8 vs. CoT per dataset - llama3.3, T=0.0",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.annotate("V8 guanya\n+22pp", xy=(0+0.5*w-w*0.5, data[("PAGE_DS","V8")]),
                xytext=(0.35, data[("PAGE_DS","V8")]+0.06),
                arrowprops=dict(arrowstyle="->", color="#00467F"),
                fontsize=9, color="#00467F", fontweight="bold")
    ax.annotate("CoT guanya\n+5pp", xy=(1-0.5*w+w*0.5, data[("exemples","COT")]),
                xytext=(1.25, data[("exemples","COT")]+0.06),
                arrowprops=dict(arrowstyle="->", color="#4CAF50"),
                fontsize=9, color="#4CAF50", fontweight="bold")
    plt.tight_layout()
    out = OUT_DIR / "j9_v8_cot_inversion.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  OK {out.name}")
    plt.close()


# == MAIN ======================================================================
print("Carregant dades Fase 1...")
df1 = load_fase1()
print(f"  {len(df1)} files carregades")

print("Carregant dades Fase 2A...")
df2 = load_fase2()
print(f"  {len(df2)} files carregades")

print("\nGenerant grafics de justificacio...")
print("  -- Fase 1 --")
plot_j1(df1)
plot_j2(df1)
plot_j3(df1)
plot_j4(df1)
plot_j5(df1)
plot_j6(df1)

print("  -- Fase 2A --")
plot_j7(df2)
plot_j8(df2)
plot_j9(df2)

print(f"\nFet. Grafics a: {OUT_DIR}")

# cleanup
import os, pathlib
fix = pathlib.Path("_fix_titles.py")
if fix.exists():
    os.remove(fix)
