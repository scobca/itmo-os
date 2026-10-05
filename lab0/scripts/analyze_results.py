#!/usr/bin/env python3

import csv
import math
import statistics
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = LAB_DIR / "logs/final/graph-traverse-write-nocache-pilot.csv"
IMAGE_DIR = LAB_DIR / "docs/img"
T_CRITICAL_95_DF9 = 2.2621571627409915

COLORS = {"seq": "#2563eb", "rand": "#dc2626"}


def load_values():
    values = {"seq": [], "rand": []}
    pairs = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            configuration = row["configuration"]
            wall_time = float(row["wall_time_s"])
            values[configuration].append(wall_time)
            pairs.setdefault(int(row["run_id"]), {})[configuration] = wall_time
    return values, pairs


def quantile_linear(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def summarize(values):
    count = len(values)
    if count != 10:
        raise ValueError(f"Ожидалось 10 измерений, получено {count}")
    mean = statistics.mean(values)
    deviation = statistics.stdev(values)
    half_width = T_CRITICAL_95_DF9 * deviation / math.sqrt(count)
    q1 = quantile_linear(values, 0.25)
    q3 = quantile_linear(values, 0.75)
    return {
        "n": count,
        "mean": mean,
        "sd": deviation,
        "median": statistics.median(values),
        "iqr": q3 - q1,
        "ci_low": mean - half_width,
        "ci_high": mean + half_width,
        "half_width": half_width,
    }


def svg_header(width, height):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text { font-family: Arial, sans-serif; fill: #172033; } .axis { stroke: #475569; stroke-width: 1.5; } .grid { stroke: #dbe3ec; stroke-width: 1; } .tick { font-size: 13px; } .label { font-size: 15px; } .title { font-size: 22px; font-weight: 700; }</style>',
    ]


def write_ci_chart(summaries):
    width, height = 900, 520
    left, right, top, bottom = 105, 45, 70, 80
    plot_width = width - left - right
    plot_height = height - top - bottom
    y_min = 7.0
    y_max = 12.0

    def y(value):
        return top + (y_max - value) / (y_max - y_min) * plot_height

    lines = svg_header(width, height)
    lines.append('<text x="450" y="36" text-anchor="middle" class="title">Среднее время и 95%-й доверительный интервал</text>')

    for tick in range(7, 13):
        tick_y = y(tick)
        lines.append(f'<line x1="{left}" y1="{tick_y:.1f}" x2="{width-right}" y2="{tick_y:.1f}" class="grid"/>')
        lines.append(f'<text x="{left-12}" y="{tick_y+5:.1f}" text-anchor="end" class="tick">{tick}</text>')

    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    lines.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis"/>')
    lines.append(f'<text x="28" y="{top + plot_height/2:.1f}" transform="rotate(-90 28 {top + plot_height/2:.1f})" text-anchor="middle" class="label">Время, с</text>')

    positions = {"seq": left + plot_width * 0.32, "rand": left + plot_width * 0.72}
    for configuration in ("seq", "rand"):
        summary = summaries[configuration]
        x = positions[configuration]
        low_y = y(summary["ci_low"])
        high_y = y(summary["ci_high"])
        mean_y = y(summary["mean"])
        color = COLORS[configuration]
        lines.append(f'<line x1="{x:.1f}" y1="{low_y:.1f}" x2="{x:.1f}" y2="{high_y:.1f}" stroke="{color}" stroke-width="4"/>')
        lines.append(f'<line x1="{x-18:.1f}" y1="{low_y:.1f}" x2="{x+18:.1f}" y2="{low_y:.1f}" stroke="{color}" stroke-width="4"/>')
        lines.append(f'<line x1="{x-18:.1f}" y1="{high_y:.1f}" x2="{x+18:.1f}" y2="{high_y:.1f}" stroke="{color}" stroke-width="4"/>')
        lines.append(f'<circle cx="{x:.1f}" cy="{mean_y:.1f}" r="9" fill="{color}"/>')
        lines.append(f'<text x="{x:.1f}" y="{height-bottom+32}" text-anchor="middle" class="label">{configuration}</text>')
        lines.append(f'<text x="{x:.1f}" y="{mean_y-15:.1f}" text-anchor="middle" class="label">{summary["mean"]:.3f} с</text>')

    lines.append('</svg>')
    (IMAGE_DIR / "graph-traverse-ci.svg").write_text("\n".join(lines), encoding="utf-8")


def write_distribution_chart(values):
    width, height = 950, 520
    left, right, top, bottom = 100, 45, 70, 85
    plot_width = width - left - right
    plot_height = height - top - bottom
    bin_start, bin_end, bin_width = 7.0, 17.0, 1.0
    bin_count = int((bin_end - bin_start) / bin_width)

    histograms = {}
    for configuration in ("seq", "rand"):
        counts = [0] * bin_count
        for value in values[configuration]:
            index = min(int((value - bin_start) // bin_width), bin_count - 1)
            if index >= 0:
                counts[index] += 1
        histograms[configuration] = counts

    max_count = max(max(counts) for counts in histograms.values())

    def x(value):
        return left + (value - bin_start) / (bin_end - bin_start) * plot_width

    def y(value):
        return top + (max_count - value) / max_count * plot_height

    lines = svg_header(width, height)
    lines.append('<text x="475" y="36" text-anchor="middle" class="title">Распределение полного времени</text>')

    for tick in range(max_count + 1):
        tick_y = y(tick)
        lines.append(f'<line x1="{left}" y1="{tick_y:.1f}" x2="{width-right}" y2="{tick_y:.1f}" class="grid"/>')
        lines.append(f'<text x="{left-12}" y="{tick_y+5:.1f}" text-anchor="end" class="tick">{tick}</text>')

    for tick in range(7, 18):
        tick_x = x(tick)
        lines.append(f'<text x="{tick_x:.1f}" y="{height-bottom+28}" text-anchor="middle" class="tick">{tick}</text>')

    bar_width = plot_width / bin_count
    for configuration in ("seq", "rand"):
        color = COLORS[configuration]
        for index, count in enumerate(histograms[configuration]):
            if count == 0:
                continue
            bar_x = left + index * bar_width + 2
            bar_y = y(count)
            bar_height = height - bottom - bar_y
            lines.append(f'<rect x="{bar_x:.1f}" y="{bar_y:.1f}" width="{bar_width-4:.1f}" height="{bar_height:.1f}" fill="{color}" fill-opacity="0.48" stroke="{color}"/>')

    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    lines.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis"/>')
    lines.append(f'<text x="{left + plot_width/2:.1f}" y="{height-22}" text-anchor="middle" class="label">Время, с</text>')
    lines.append(f'<text x="28" y="{top + plot_height/2:.1f}" transform="rotate(-90 28 {top + plot_height/2:.1f})" text-anchor="middle" class="label">Число запусков</text>')

    legend_x = width - right - 190
    for index, configuration in enumerate(("seq", "rand")):
        legend_y = 70 + index * 28
        lines.append(f'<rect x="{legend_x}" y="{legend_y-14}" width="22" height="16" fill="{COLORS[configuration]}" fill-opacity="0.55"/>')
        lines.append(f'<text x="{legend_x+32}" y="{legend_y}" class="label">{configuration}</text>')

    lines.append('</svg>')
    (IMAGE_DIR / "graph-traverse-distribution.svg").write_text("\n".join(lines), encoding="utf-8")


def main():
    values, pairs = load_values()
    summaries = {name: summarize(series) for name, series in values.items()}
    differences = [pairs[run]["rand"] - pairs[run]["seq"] for run in sorted(pairs)]
    difference_summary = summarize(differences)

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    write_ci_chart(summaries)
    write_distribution_chart(values)

    for configuration in ("seq", "rand"):
        summary = summaries[configuration]
        print(
            f"{configuration}: mean={summary['mean']:.3f}, "
            f"sd={summary['sd']:.3f}, "
            f"CI95=[{summary['ci_low']:.3f}; {summary['ci_high']:.3f}]"
        )
    print(
        f"paired rand-seq: mean={difference_summary['mean']:.3f}, "
        f"CI95=[{difference_summary['ci_low']:.3f}; {difference_summary['ci_high']:.3f}]"
    )


if __name__ == "__main__":
    main()
