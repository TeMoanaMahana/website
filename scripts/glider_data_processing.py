"""
Glider Dive Data Processor

Collapses multiple surface GPS rows to a single row per surface period.
Adds Day_Index based on NZ local date (Pacific/Auckland).

Usage:
    python glider_data_processing.py data/glider_data.csv data/glider_data_processed.csv

Requirements:
    pip install pandas
"""

import pandas as pd
import sys
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

# Config
INPUT_FILE  = Path("static/data/glider_data.csv")
OUTPUT_FILE = Path("static/data/glider_data_processed.csv")

if len(sys.argv) >= 3:
    INPUT_FILE, OUTPUT_FILE = Path(sys.argv[1]), Path(sys.argv[2])
elif len(sys.argv) == 2:
    INPUT_FILE = Path(sys.argv[1])

NZ_TZ = ZoneInfo("Pacific/Auckland")

SENSOR_COLS = [
    "Pressure [dBar]",
    "Temperature [degC]",
    "Salinity [psu]",
    "PAR [microE/m2/s]",
    "CDOM [ppb]",
    "Backscatter (700nm)",
    "Chlorophyll-a [micro-gm/l]",
]

# Load data
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df):,} rows from '{INPUT_FILE}'")

# Convert timestamp to NZ local date
df["_nz_date"] = (
    pd.to_datetime(df["Timestamp (UTC)"], unit="s", utc=True)
    .dt.tz_convert(NZ_TZ)
    .dt.date
)

# Build Day_Index
unique_days  = sorted(df["_nz_date"].dropna().unique())
day_to_index = {day: i + 1 for i, day in enumerate(unique_days)}
df["Day_Index"] = df["_nz_date"].map(day_to_index)

print("\nNZ date -> Day_Index mapping:")
for day, idx in day_to_index.items():
    print(f"  {day}  ->  Day {idx}")

# Classify rows
df["_has_sensor"] = df[SENSOR_COLS].notna().any(axis=1)
df["_segment"]    = (df["_has_sensor"] != df["_has_sensor"].shift()).cumsum()

# Process segments
output_rows = []
for seg_id, group in df.groupby("_segment", sort=True):
    if group["_has_sensor"].iloc[0]:
        output_rows.append(group.copy())
    else:
        output_rows.append(group.iloc[[-1]].copy())

# Assemble and clean up
result = pd.concat(output_rows, ignore_index=True)
result = result.drop(columns=["_has_sensor", "_segment", "_nz_date"])

cols   = ["Day_Index"] + [c for c in result.columns if c != "Day_Index"]
result = result[cols]

# Summary
is_dive_row = result[SENSOR_COLS].notna().any(axis=1)
print(f"\nResults:")
print(f"  Total output rows : {len(result):,}")
print(f"  Surface rows kept : {(~is_dive_row).sum()}  (one per surface period)")
print(f"  Dive rows kept    : {is_dive_row.sum()}")
print(f"\nRows per Day_Index:")
print(result.groupby("Day_Index").size().rename("rows").to_string())

# Save
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved to '{OUTPUT_FILE}'")
