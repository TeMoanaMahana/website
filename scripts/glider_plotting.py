import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import gsw
import re
import sys

# Paths
INPUT_FILE  = Path("static/data/glider/processed/glider_data_processed.csv")
OUTPUT_DIR  = Path("static/images/glider")
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

# Columns: Leg_Index, Timestamp (NZ), Timestamp (UTC), Longitude, Latitude,
# Pressure [dBar], then the sensor data columns.
# NOTE: this assumes that fixed column layout. If the input CSV's column
# order ever changes, update the positional indices below (or better,
# switch to df["Actual Column Name"] once you confirm the exact names).
TIME_COL_POS     = 2  # "Timestamp (UTC)"
LAT_COL_POS      = 4  # "Latitude"
PRESSURE_COL_POS = 5  # "Pressure [dBar]"
DATA_COLS_START  = 6

data_cols = df.columns[DATA_COLS_START:]

if "Leg_Index" not in df.columns:
    sys.exit("Expected a 'Leg_Index' column in the input CSV but didn't find one.")

legs = sorted(df["Leg_Index"].dropna().unique())
print(f"Found {len(legs)} leg(s): {legs}\n")

saved_files = []

for leg in legs:
    leg_df = df[df["Leg_Index"] == leg].reset_index(drop=True)

    leg_out_dir = OUTPUT_DIR / f"leg{int(leg)}"
    leg_out_dir.mkdir(parents=True, exist_ok=True)

    # Derived columns (per leg)
    time     = pd.to_datetime(leg_df.iloc[:, TIME_COL_POS], unit="s", utc=True).dt.tz_convert("Pacific/Auckland")
    pressure = leg_df.iloc[:, PRESSURE_COL_POS]
    lat_val  = leg_df.iloc[:, LAT_COL_POS].median()

    mask    = pressure.notna()
    depth   = -gsw.z_from_p(pressure[mask], lat_val)
    mask2   = depth.notna()
    time_p  = time[mask][mask2]
    depth_p = depth[mask2]

    print(f"Leg {int(leg)}: {len(leg_df):,} rows -> {mask2.sum():,} valid depth points")

    for col in data_cols:
        values = leg_df[col][mask][mask2]
        valid  = values.notna()

        if valid.sum() == 0:
            print(f"  Skipping '{col}' for Leg {int(leg)} (no valid data)")
            continue

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
        out_path = leg_out_dir / filename
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        saved_files.append(out_path)
        print(f"  Saved: {out_path}")

print(f"\nDone — {len(saved_files)} plots written across {len(legs)} leg(s) to '{OUTPUT_DIR}'")
