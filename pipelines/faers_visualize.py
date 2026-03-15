"""
RS-001b: FAERS Signal Visualization
Reads the findings markdown, extracts signal tables, produces:
  1. PRR bar chart (top novel signals per drug)
  2. Signal heatmap (drugs × events)
  3. Known vs novel signal breakdown
  4. Summary stats card (text)
"""

import re, os, sys
from datetime import date
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("matplotlib not available — skipping charts")

FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "..", "findings", "charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DRUG_COLORS = {
    "fluoxetine":   "#4C72B0",
    "sertraline":   "#DD8452",
    "escitalopram": "#55A868",
    "paroxetine":   "#C44E52",
    "citalopram":   "#8172B2",
    "fluvoxamine":  "#937860",
}

SSRI_SHORT = {
    "fluoxetine":   "Fluoxetine",
    "sertraline":   "Sertraline",
    "escitalopram": "Escitalopram",
    "paroxetine":   "Paroxetine",
    "citalopram":   "Citalopram",
    "fluvoxamine":  "Fluvoxamine",
}


def find_latest_report():
    files = sorted([
        f for f in os.listdir(FINDINGS_DIR)
        if f.endswith("_faers_ssri_signals.md")
    ])
    if not files:
        print("No findings file found. Run faers_prr.py first.")
        sys.exit(1)
    return os.path.join(FINDINGS_DIR, files[-1])


def parse_signal_table(md_text):
    """Parse the per-drug signal tables from markdown."""
    drug_signals = defaultdict(list)
    current_drug = None
    in_table = False

    for line in md_text.splitlines():
        # Detect drug section header
        m = re.match(r"### (.+) \(", line)
        if m:
            current_drug = m.group(1).lower()
            in_table = False
            continue

        # Detect table rows (event | count | prr | chi2 | known)
        if current_drug and "|" in line and "Event" not in line and "---" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 5:
                try:
                    event  = parts[0]
                    count  = int(parts[1].replace(",", ""))
                    prr    = float(parts[2])
                    chi2   = float(parts[3])
                    known  = "✓" in parts[4]
                    drug_signals[current_drug].append({
                        "event": event, "count": count,
                        "prr": prr, "chi2": chi2, "known": known
                    })
                except (ValueError, IndexError):
                    pass

    return drug_signals


def plot_top_novel_signals(drug_signals, out_dir):
    """Bar chart: top 10 novel signals by PRR across all drugs."""
    if not HAS_MPL:
        return None

    all_novel = []
    for drug, sigs in drug_signals.items():
        for s in sigs:
            if not s["known"] and s["prr"] >= 2.0:
                all_novel.append({**s, "drug": drug})

    if not all_novel:
        print("No novel signals to plot.")
        return None

    all_novel.sort(key=lambda x: -x["prr"])
    top = all_novel[:20]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    labels  = [f"{s['event'][:40]}\n({SSRI_SHORT.get(s['drug'], s['drug'])})" for s in top]
    values  = [s["prr"] for s in top]
    colors  = [DRUG_COLORS.get(s["drug"], "#aaaaaa") for s in top]

    bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1],
                   edgecolor="white", linewidth=0.3, height=0.7)

    ax.axvline(x=2.0, color="yellow", linestyle="--", alpha=0.7, linewidth=1.5,
               label="Signal threshold (PRR=2)")

    # Count annotations
    for bar, s in zip(bars, reversed(top)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"n={s['count']:,}", va="center", ha="left",
                color="white", fontsize=7)

    ax.set_xlabel("Proportional Reporting Ratio (PRR)", color="white", fontsize=11)
    ax.set_title("FAERS — Top Novel SSRI Adverse Event Signals\n"
                 "(Events not in published trial AE profiles, PRR ≥ 2.0)",
                 color="white", fontsize=13, pad=15)
    ax.tick_params(colors="white", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    ax.xaxis.label.set_color("white")

    # Legend for drugs
    patches = [mpatches.Patch(color=c, label=SSRI_SHORT[d])
               for d, c in DRUG_COLORS.items() if d in drug_signals]
    ax.legend(handles=patches, loc="lower right",
              facecolor="#1a1a2e", edgecolor="#444444",
              labelcolor="white", fontsize=8)
    ax.legend(handles=patches + [plt.Line2D([0],[0], color="yellow",
              linestyle="--", label="Signal threshold")],
              loc="lower right", facecolor="#1a1a2e",
              edgecolor="#444444", labelcolor="white", fontsize=8)

    ax.set_xlim(0, max(values) * 1.15)
    plt.tight_layout()
    outpath = os.path.join(out_dir, "novel_signals_prr.png")
    plt.savefig(outpath, dpi=150, bbox_inches="tight",
                facecolor="#1a1a2e")
    plt.close()
    print(f"  Chart: {outpath}")
    return outpath


def plot_signal_heatmap(drug_signals, out_dir):
    """Heatmap: drugs × top shared events, colored by PRR."""
    if not HAS_MPL:
        return None

    # Find events that appear across multiple drugs
    event_drugs = defaultdict(dict)
    for drug, sigs in drug_signals.items():
        for s in sigs:
            if s["prr"] >= 2.0:
                event_drugs[s["event"]][drug] = s["prr"]

    # Keep events in >=2 drugs OR top PRR events
    shared_events = {e: d for e, d in event_drugs.items() if len(d) >= 2}
    # Add top PRR overall
    all_events_by_prr = sorted(event_drugs.items(),
                               key=lambda x: max(x[1].values()), reverse=True)
    for e, d in all_events_by_prr[:30]:
        shared_events[e] = d

    if not shared_events:
        return None

    drugs = [d for d in DRUG_COLORS if d in drug_signals]
    events = sorted(shared_events.keys(),
                    key=lambda e: -max(shared_events[e].values()))[:25]

    matrix = np.zeros((len(events), len(drugs)))
    for i, event in enumerate(events):
        for j, drug in enumerate(drugs):
            matrix[i, j] = shared_events.get(event, {}).get(drug, 0)

    fig, ax = plt.subplots(figsize=(10, 9))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    # Replace 0 with nan for grey coloring
    masked = np.where(matrix > 0, matrix, np.nan)
    im = ax.imshow(masked, cmap="YlOrRd", aspect="auto",
                   vmin=1.0, vmax=min(20, np.nanmax(matrix)))

    ax.set_xticks(range(len(drugs)))
    ax.set_xticklabels([SSRI_SHORT.get(d, d) for d in drugs],
                       color="white", fontsize=10, rotation=30, ha="right")
    ax.set_yticks(range(len(events)))
    ax.set_yticklabels([e[:45] for e in events], color="white", fontsize=8)

    # PRR value annotations in cells
    for i in range(len(events)):
        for j in range(len(drugs)):
            val = matrix[i, j]
            if val > 0:
                ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                       fontsize=7, color="black" if val > 5 else "white",
                       fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label("PRR (Proportional Reporting Ratio)",
                   color="white", fontsize=9)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

    ax.set_title("FAERS Signal Heatmap — SSRIs × Adverse Events\n"
                 "(PRR value shown; grey = no signal)",
                 color="white", fontsize=12, pad=12)

    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

    plt.tight_layout()
    outpath = os.path.join(out_dir, "signal_heatmap.png")
    plt.savefig(outpath, dpi=150, bbox_inches="tight",
                facecolor="#1a1a2e")
    plt.close()
    print(f"  Chart: {outpath}")
    return outpath


def plot_known_vs_novel(drug_signals, out_dir):
    """Stacked bar: known vs novel signals per drug."""
    if not HAS_MPL:
        return None

    drugs_list = [d for d in DRUG_COLORS if d in drug_signals]
    known_counts  = []
    novel_counts  = []

    for d in drugs_list:
        sigs = [s for s in drug_signals[d] if s["prr"] >= 2.0]
        known_counts.append(sum(1 for s in sigs if s["known"]))
        novel_counts.append(sum(1 for s in sigs if not s["known"]))

    x = np.arange(len(drugs_list))
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    b1 = ax.bar(x, known_counts,  color="#4CAF50", label="Known AE (in trial profiles)", width=0.5)
    b2 = ax.bar(x, novel_counts,  bottom=known_counts,
                color="#FF5252", label="Novel signal (not in trial profiles)", width=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([SSRI_SHORT.get(d, d) for d in drugs_list],
                       color="white", fontsize=10)
    ax.set_ylabel("Number of signals (PRR ≥ 2, n ≥ 3, chi² ≥ 4)",
                  color="white", fontsize=10)
    ax.set_title("FAERS Signals by Drug — Known vs Novel\n"
                 "(Novel = not in published SSRI trial adverse event profiles)",
                 color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.legend(facecolor="#1a1a2e", edgecolor="#444444",
              labelcolor="white", fontsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    # Count labels
    for i, (k, n) in enumerate(zip(known_counts, novel_counts)):
        if k > 0:
            ax.text(i, k/2, str(k), ha="center", va="center",
                    color="white", fontweight="bold", fontsize=9)
        if n > 0:
            ax.text(i, k + n/2, str(n), ha="center", va="center",
                    color="white", fontweight="bold", fontsize=9)

    plt.tight_layout()
    outpath = os.path.join(out_dir, "known_vs_novel.png")
    plt.savefig(outpath, dpi=150, bbox_inches="tight",
                facecolor="#1a1a2e")
    plt.close()
    print(f"  Chart: {outpath}")
    return outpath


def print_summary_card(drug_signals):
    """Text summary card."""
    total_signals = sum(
        sum(1 for s in sigs if s["prr"] >= 2.0)
        for sigs in drug_signals.values()
    )
    total_novel = sum(
        sum(1 for s in sigs if s["prr"] >= 2.0 and not s["known"])
        for sigs in drug_signals.values()
    )
    top_signal = max(
        (s for sigs in drug_signals.values() for s in sigs if s["prr"] >= 2.0),
        key=lambda x: x["prr"], default=None
    )
    print("\n" + "="*55)
    print("  FAERS SSRI SIGNAL DETECTION — RESULTS SUMMARY")
    print("="*55)
    print(f"  Total signals detected (Evans criteria):  {total_signals}")
    print(f"  Novel signals (not in trial AE profiles): {total_novel}")
    if top_signal:
        print(f"  Highest PRR signal:  {top_signal['event']}")
        print(f"    PRR={top_signal['prr']:.1f}, n={top_signal['count']:,}")
    print()
    for drug, sigs in drug_signals.items():
        n_sig = sum(1 for s in sigs if s["prr"] >= 2.0)
        n_nov = sum(1 for s in sigs if s["prr"] >= 2.0 and not s["known"])
        print(f"  {SSRI_SHORT.get(drug,drug):15s}  {n_sig:3d} signals  "
              f"({n_nov} novel)")
    print("="*55)


if __name__ == "__main__":
    report_path = find_latest_report()
    print(f"Reading: {report_path}")
    with open(report_path, encoding="utf-8") as f:
        md = f.read()

    drug_signals = parse_signal_table(md)
    print(f"Parsed signals for {len(drug_signals)} drugs")

    print_summary_card(drug_signals)

    print("\nGenerating charts...")
    plot_top_novel_signals(drug_signals, OUTPUT_DIR)
    plot_signal_heatmap(drug_signals,    OUTPUT_DIR)
    plot_known_vs_novel(drug_signals,    OUTPUT_DIR)

    print(f"\nCharts saved to: {OUTPUT_DIR}")
