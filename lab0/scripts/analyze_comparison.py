#!/usr/bin/env python3

import csv
import math
import statistics
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1]
SOURCES = {
    "read/lseek": LAB_DIR / "logs/final/graph-traverse-write-nocache-pilot.csv",
    "mmap": LAB_DIR / "logs/mmap/final/graph-traverse-mmap-write-nocache.csv",
}
OUTPUT = LAB_DIR / "docs/img/methods-comparison-ci.svg"
T_CRITICAL_95_DF9 = 2.2621571627409915
COLORS = {"read/lseek": "#7c3aed", "mmap": "#0891b2"}


def load():
    series = {}
    for method, path in SOURCES.items():
        with path.open(newline="", encoding="utf-8") as source:
            for row in csv.DictReader(source):
                if row["exit_status"] != "0":
                    raise ValueError(f"Неуспешный запуск в {path}: {row}")
                key = (method, row["configuration"])
                iterations = int(row["iterations"])
                series.setdefault(key, []).append(float(row["wall_time_s"]) / iterations)
    return series


def summarize(values):
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    half = T_CRITICAL_95_DF9 * sd / math.sqrt(len(values))
    return mean, mean - half, mean + half


def write_chart(summaries):
    width, height = 1040, 570
    left, right, top, bottom = 115, 45, 70, 105
    plot_height = height - top - bottom
    y_min, y_max = 0.02, 20.0

    def y(value):
        fraction = (math.log10(value) - math.log10(y_min)) / (math.log10(y_max) - math.log10(y_min))
        return top + (1 - fraction) * plot_height

    positions = {
        ("read/lseek", "seq"): 245,
        ("read/lseek", "rand"): 430,
        ("mmap", "seq"): 680,
        ("mmap", "rand"): 865,
    }
    ticks = [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#172033}.grid{stroke:#dbe3ec}.axis{stroke:#475569;stroke-width:1.5}.title{font-size:22px;font-weight:700}.label{font-size:15px}.tick{font-size:13px}.group{font-size:16px;font-weight:700}</style>',
        '<text x="520" y="35" text-anchor="middle" class="title">Время одного обхода и 95%-й CI</text>',
    ]
    for tick in ticks:
        yy = y(tick)
        label = f"{tick:g}"
        lines.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/>')
        lines.append(f'<text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" class="tick">{label}</text>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    lines.append(f'<text x="28" y="{top+plot_height/2:.1f}" transform="rotate(-90 28 {top+plot_height/2:.1f})" text-anchor="middle" class="label">Время, с (логарифмическая шкала)</text>')
    for key, (mean, low, high) in summaries.items():
        method, topology = key
        x, color = positions[key], COLORS[method]
        lines.append(f'<line x1="{x}" y1="{y(low):.1f}" x2="{x}" y2="{y(high):.1f}" stroke="{color}" stroke-width="4"/>')
        for bound in (low, high):
            lines.append(f'<line x1="{x-15}" y1="{y(bound):.1f}" x2="{x+15}" y2="{y(bound):.1f}" stroke="{color}" stroke-width="4"/>')
        lines.append(f'<circle cx="{x}" cy="{y(mean):.1f}" r="8" fill="{color}"/>')
        lines.append(f'<text x="{x}" y="{y(mean)-13:.1f}" text-anchor="middle" class="tick">{mean:.4f} с</text>')
        lines.append(f'<text x="{x}" y="{height-bottom+28}" text-anchor="middle" class="label">{topology}</text>')
    lines.append('<text x="338" y="535" text-anchor="middle" class="group">read/lseek</text>')
    lines.append('<text x="772" y="535" text-anchor="middle" class="group">mmap</text>')
    lines.append('</svg>')
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    series = load()
    summaries = {key: summarize(values) for key, values in series.items()}
    write_chart(summaries)
    for key in (("read/lseek", "seq"), ("read/lseek", "rand"), ("mmap", "seq"), ("mmap", "rand")):
        mean, low, high = summaries[key]
        print(f"{key[0]} {key[1]}: mean={mean:.6f}; CI95=[{low:.6f}; {high:.6f}]")


if __name__ == "__main__":
    main()
