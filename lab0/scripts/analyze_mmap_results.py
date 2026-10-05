#!/usr/bin/env python3

import csv
import math
import statistics
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = LAB_DIR / "logs/mmap/final/graph-traverse-mmap-write-nocache.csv"
IMAGE_DIR = LAB_DIR / "docs/img"
T_CRITICAL_95_DF9 = 2.2621571627409915
COLORS = {"seq": "#2563eb", "rand": "#dc2626"}


def load_data():
    values = {"seq": [], "rand": []}
    pairs = {}
    rows = {"seq": [], "rand": []}
    with CSV_PATH.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            name = row["configuration"]
            if row["exit_status"] != "0":
                raise ValueError(f"Неуспешный запуск: {row}")
            value = float(row["wall_time_s"])
            values[name].append(value)
            rows[name].append(row)
            pairs.setdefault(int(row["run_id"]), {})[name] = value
    return values, pairs, rows


def quantile(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def summarize(values):
    if len(values) != 10:
        raise ValueError(f"Ожидалось 10 измерений, получено {len(values)}")
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    half = T_CRITICAL_95_DF9 * sd / math.sqrt(len(values))
    return {
        "n": len(values), "mean": mean, "sd": sd,
        "median": statistics.median(values),
        "iqr": quantile(values, 0.75) - quantile(values, 0.25),
        "ci_low": mean - half, "ci_high": mean + half,
        "half": half, "relative_half": half / mean * 100,
    }


def svg_start(width, height):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#172033}.grid{stroke:#dbe3ec}.axis{stroke:#475569;stroke-width:1.5}.title{font-size:22px;font-weight:700}.label{font-size:15px}.tick{font-size:13px}</style>',
    ]


def write_ci_chart(summaries):
    width, height = 860, 500
    left, right, top, bottom = 100, 45, 70, 75
    low = min(s["ci_low"] for s in summaries.values())
    high = max(s["ci_high"] for s in summaries.values())
    margin = max((high - low) * 0.35, 0.15)
    y_min, y_max = low - margin, high + margin

    def y(value):
        return top + (y_max - value) / (y_max - y_min) * (height - top - bottom)

    lines = svg_start(width, height)
    lines.append('<text x="430" y="36" text-anchor="middle" class="title">mmap: среднее время и 95%-й CI</text>')
    for index in range(6):
        value = y_min + (y_max - y_min) * index / 5
        yy = y(value)
        lines.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/>')
        lines.append(f'<text x="{left-10}" y="{yy+5:.1f}" text-anchor="end" class="tick">{value:.2f}</text>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    positions = {"seq": 300, "rand": 620}
    for name in ("seq", "rand"):
        s, x, color = summaries[name], positions[name], COLORS[name]
        lines.append(f'<line x1="{x}" y1="{y(s["ci_low"]):.1f}" x2="{x}" y2="{y(s["ci_high"]):.1f}" stroke="{color}" stroke-width="4"/>')
        for bound in (s["ci_low"], s["ci_high"]):
            lines.append(f'<line x1="{x-18}" y1="{y(bound):.1f}" x2="{x+18}" y2="{y(bound):.1f}" stroke="{color}" stroke-width="4"/>')
        lines.append(f'<circle cx="{x}" cy="{y(s["mean"]):.1f}" r="9" fill="{color}"/>')
        lines.append(f'<text x="{x}" y="{height-35}" text-anchor="middle" class="label">{name}</text>')
        lines.append(f'<text x="{x}" y="{y(s["mean"])-15:.1f}" text-anchor="middle" class="label">{s["mean"]:.3f} с</text>')
    lines.append('</svg>')
    (IMAGE_DIR / "mmap-ci.svg").write_text("\n".join(lines), encoding="utf-8")


def write_pairs_chart(pairs):
    width, height = 920, 500
    left, right, top, bottom = 85, 35, 65, 75
    all_values = [value for pair in pairs.values() for value in pair.values()]
    y_min, y_max = min(all_values) - 0.2, max(all_values) + 0.2

    def x(run):
        return left + (run - 1) / 9 * (width - left - right)

    def y(value):
        return top + (y_max - value) / (y_max - y_min) * (height - top - bottom)

    lines = svg_start(width, height)
    lines.append('<text x="460" y="34" text-anchor="middle" class="title">mmap: парные измерения</text>')
    for run in range(1, 11):
        lines.append(f'<text x="{x(run):.1f}" y="{height-38}" text-anchor="middle" class="tick">{run}</text>')
    for run, pair in sorted(pairs.items()):
        lines.append(f'<line x1="{x(run):.1f}" y1="{y(pair["seq"]):.1f}" x2="{x(run):.1f}" y2="{y(pair["rand"]):.1f}" stroke="#94a3b8"/>')
        for name in ("seq", "rand"):
            lines.append(f'<circle cx="{x(run):.1f}" cy="{y(pair[name]):.1f}" r="6" fill="{COLORS[name]}"/>')
    lines.append(f'<text x="{left+(width-left-right)/2:.1f}" y="{height-12}" text-anchor="middle" class="label">Номер блока</text>')
    lines.append('<rect x="690" y="58" width="16" height="16" fill="#2563eb"/><text x="714" y="72" class="label">seq</text>')
    lines.append('<rect x="770" y="58" width="16" height="16" fill="#dc2626"/><text x="794" y="72" class="label">rand</text>')
    lines.append('</svg>')
    (IMAGE_DIR / "mmap-pairs.svg").write_text("\n".join(lines), encoding="utf-8")


def write_distribution_chart(values):
    width, height = 920, 500
    left, right, top, bottom = 85, 35, 65, 75
    all_values = values["seq"] + values["rand"]
    lower = math.floor(min(all_values) * 5) / 5
    upper = math.ceil(max(all_values) * 5) / 5
    bin_count = max(6, round((upper - lower) / 0.2))
    bin_width = (upper - lower) / bin_count
    histograms = {}
    for name in ("seq", "rand"):
        counts = [0] * bin_count
        for value in values[name]:
            index = min(int((value - lower) / bin_width), bin_count - 1)
            counts[index] += 1
        histograms[name] = counts
    max_count = max(max(counts) for counts in histograms.values())

    def x(value):
        return left + (value - lower) / (upper - lower) * (width - left - right)

    def y(value):
        return top + (max_count - value) / max_count * (height - top - bottom)

    lines = svg_start(width, height)
    lines.append('<text x="460" y="34" text-anchor="middle" class="title">mmap: распределение полного времени</text>')
    for tick in range(max_count + 1):
        yy = y(tick)
        lines.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/>')
        lines.append(f'<text x="{left-10}" y="{yy+5:.1f}" text-anchor="end" class="tick">{tick}</text>')
    bar_width = (width - left - right) / bin_count
    for name in ("seq", "rand"):
        for index, count in enumerate(histograms[name]):
            if count:
                xx = left + index * bar_width + 2
                yy = y(count)
                lines.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{bar_width-4:.1f}" height="{height-bottom-yy:.1f}" fill="{COLORS[name]}" fill-opacity="0.45" stroke="{COLORS[name]}"/>')
    for index in range(6):
        value = lower + (upper - lower) * index / 5
        lines.append(f'<text x="{x(value):.1f}" y="{height-38}" text-anchor="middle" class="tick">{value:.2f}</text>')
    lines.append(f'<text x="{left+(width-left-right)/2:.1f}" y="{height-12}" text-anchor="middle" class="label">Время, с</text>')
    lines.append('<rect x="690" y="58" width="16" height="16" fill="#2563eb" fill-opacity="0.55"/><text x="714" y="72" class="label">seq</text>')
    lines.append('<rect x="770" y="58" width="16" height="16" fill="#dc2626" fill-opacity="0.55"/><text x="794" y="72" class="label">rand</text>')
    lines.append('</svg>')
    (IMAGE_DIR / "mmap-distribution.svg").write_text("\n".join(lines), encoding="utf-8")


def metric_mean(rows, field):
    return statistics.mean(float(row[field]) for row in rows)


def main():
    values, pairs, rows = load_data()
    summaries = {name: summarize(series) for name, series in values.items()}
    differences = [pairs[run]["rand"] - pairs[run]["seq"] for run in sorted(pairs)]
    difference = summarize(differences)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    write_ci_chart(summaries)
    write_pairs_chart(pairs)
    write_distribution_chart(values)
    for name in ("seq", "rand"):
        s = summaries[name]
        required = math.ceil((1.96 * s["sd"] / (0.05 * s["mean"])) ** 2)
        print(f"{name}: mean={s['mean']:.3f}; sd={s['sd']:.3f}; median={s['median']:.3f}; IQR={s['iqr']:.3f}; CI95=[{s['ci_low']:.3f}; {s['ci_high']:.3f}]; rel_half={s['relative_half']:.2f}%; N5={required}")
        print(f"  user={metric_mean(rows[name], 'user_time_s'):.3f}; sys={metric_mean(rows[name], 'sys_time_s'):.3f}; vol_ctx={metric_mean(rows[name], 'vol_ctx'):.1f}; invol_ctx={metric_mean(rows[name], 'invol_ctx'):.1f}; minflt={metric_mean(rows[name], 'minflt'):.1f}")
    print(f"paired rand-seq: mean={difference['mean']:.3f}; CI95=[{difference['ci_low']:.3f}; {difference['ci_high']:.3f}]")
    print("pairs:", ", ".join(f"{run}:{pairs[run]['rand']-pairs[run]['seq']:.2f}" for run in sorted(pairs)))


if __name__ == "__main__":
    main()
