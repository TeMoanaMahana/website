import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import gsw
import re
import sys

# Paths
INPUT_FILE  = Path("static/data/glider_data_processed.csv")
OUTPUT_DIR  = Path("static/images/glider")          # Hugo serves everything in static/

if len(sys.argv) >= 2:
    INPUT_FILE = Path(sys.argv[1])
if len(sys.argv) >= 3:
    OUTPUT_DIR = Path(sys.argv[2])

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Style
label_size  = 12
tick_size   = 10
font_weight = "bold"

# Load data
df = pd.read_csv(INPUT_FILE)
df = df.rename(columns={
    "Temperature [degC]":        "Temperature (°C)",
    "Salinity [psu]":            "Salinity (PSU)",
    "PAR [microE/m2/s]":         "PAR (µmol photons/m²/s)",
    "CDOM [ppb]":                "Coloured Dissolved Organic Matter (ppb)",
    "Backscatter (700nm)":       "Optical Backscatter (700nm)",
    "Chlorophyll-a [micro-gm/l]":"Chlorophyll-a (µg/L)",
})

cmap_map = {
    "Temperature (°C)":                          "inferno",
    "Salinity (PSU)":                            "viridis",
    "PAR (µmol photons/m²/s)":                  "cividis",
    "Coloured Dissolved Organic Matter (ppb)":   "cividis",
    "Optical Backscatter (700nm)":               "cividis",
    "Chlorophyll-a (µg/L)":                      "BuGn",
}

# Derived columns
time     = pd.to_datetime(df.iloc[:, 1], unit="s", utc=True).dt.tz_convert("Pacific/Auckland")
pressure = df.iloc[:, 4]
lat_val  = df.iloc[:, 3].median()
data_cols = df.columns[5:]

mask    = pressure.notna()
depth   = -gsw.z_from_p(pressure[mask], lat_val)
mask2   = depth.notna()

time_p  = time[mask][mask2]
depth_p = depth[mask2]

# Plot each variable
saved_files = []

for col in data_cols:
    values = df[col][mask][mask2]
    valid  = values.notna()

    fig, ax = plt.subplots(figsize=(10, 5))
    sc = ax.scatter(
        time_p[valid],
        depth_p[valid],
        c=values[valid],
        cmap=cmap_map.get(col, "viridis"),
        s=8,
        alpha=0.8,
    )

    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(col, fontsize=label_size, fontweight=font_weight)
    cbar.ax.tick_params(labelsize=tick_size)
    plt.setp(cbar.ax.yaxis.get_majorticklabels(), fontweight=font_weight)

    ax.set_ylabel("Depth (m)", fontsize=label_size, fontweight=font_weight)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=tick_size)
    ax.tick_params(axis="x", rotation=30, labelsize=tick_size)
    plt.setp(ax.yaxis.get_majorticklabels(), fontweight=font_weight)
    plt.setp(ax.xaxis.get_majorticklabels(), ha="right", fontweight=font_weight)
    ax.grid(linestyle="--", linewidth=0.5, alpha=0.7)
    ax.xaxis.set_major_formatter(
        plt.matplotlib.dates.DateFormatter("%d %b %Y", tz="Pacific/Auckland")
    )

    filename = re.split(r"[\[(]", col)[0].strip().replace(" ", "_") + ".png"
    out_path = OUTPUT_DIR / filename
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(filename)
    print(f"Saved: {out_path}")

print(f"\nDone — {len(saved_files)} plots written to '{OUTPUT_DIR}'")
