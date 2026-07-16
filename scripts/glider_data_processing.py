"""
Glider Dive Data Processor
Reads all per-leg CSV files (e.g. leg1_glider_data.csv, leg2_glider_data.csv, ...)
from a directory, collapses multiple surface GPS rows to a single row per
surface period within each leg, tags each row with a Leg_Index (taken from
the filename), and merges everything into one output CSV.

Usage:
    python glider_data_processing.py static/data/glider/raw/ static/data/glider/processed/glider_data_processed.csv
"""

import pandas as pd
import re
import sys
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

NZ_TZ = ZoneInfo("Pacific/Auckland")

INPUT_DIR  = Path("static/data/glider/raw/")
OUTPUT_FILE = Path("static/data/glider/processed/glider_data_processed.csv")

if len(sys.argv) >= 3:
    INPUT_DIR, OUTPUT_FILE = Path(sys.argv[1]), Path(sys.argv[2])
elif len(sys.argv) == 2:
    INPUT_DIR = Path(sys.argv[1])

SENSOR_COLS = [
    "Pressure [dBar]",
    "Temperature [degC]",
    "Salinity [psu]",
    "PAR [microE/m2/s]",
    "CDOM [ppb]",
    "Backscatter (700nm)",
    "Chlorophyll-a [micro-gm/l]",
]

LEG_FILENAME_RE = re.compile(r"leg(\d+)", re.IGNORECASE)


def extract_leg_index(path: Path) -> int:
    """Pull the leg number out of a filename like 'leg3_glider_data.csv'."""
    match = LEG_FILENAME_RE.search(path.stem)
    if not match:
        raise ValueError(
            f"Could not find a 'legN' pattern in filename '{path.name}'. "
            "Expected something like 'leg1_glider_data.csv'."
        )
    return int(match.group(1))


def process_leg_file(path: Path) -> pd.DataFrame:
    """Load a single leg's CSV and collapse consecutive surface-only rows."""
    df = pd.read_csv(path)
    leg_index = extract_leg_index(path)
    print(f"Loaded {len(df):,} rows from '{path}' (Leg {leg_index})")

    # Add NZ local timestamp (converted from UTC epoch seconds)
    df["Timestamp (NZ)"] = (
        pd.to_datetime(df["Timestamp (UTC)"], unit="s", utc=True)
        .dt.tz_convert(NZ_TZ)
    )

    # Classify rows as dive (has sensor data) vs surface (no sensor data)
    df["_has_sensor"] = df[SENSOR_COLS].notna().any(axis=1)
    df["_segment"] = (df["_has_sensor"] != df["_has_sensor"].shift()).cumsum()

    output_rows = []
    for _, group in df.groupby("_segment", sort=True):
        if group["_has_sensor"].iloc[0]:
            output_rows.append(group.copy())
        else:
            output_rows.append(group.iloc[[-1]].copy())

    result = pd.concat(output_rows, ignore_index=True)
    result = result.drop(columns=["_has_sensor", "_segment"])
    result.insert(0, "Leg_Index", leg_index)
    # Move Timestamp (NZ) right after Leg_Index for readability
    nz_col = result.pop("Timestamp (NZ)")
    result.insert(1, "Timestamp (NZ)", nz_col)

    is_dive_row = result[SENSOR_COLS].notna().any(axis=1)
    print(f"  Rows after collapsing surface periods: {len(result):,} "
          f"(surface: {(~is_dive_row).sum()}, dive: {is_dive_row.sum()})")

    return result


# Find and sort all leg CSV files
csv_files = sorted(INPUT_DIR.glob("*.csv"), key=lambda p: extract_leg_index(p))
if not csv_files:
    sys.exit(f"No .csv files found in '{INPUT_DIR}'")

print(f"Found {len(csv_files)} leg file(s) in '{INPUT_DIR}':")
for f in csv_files:
    print(f"  {f.name}")
print()

# Process each leg file independently, then merge
all_legs = [process_leg_file(f) for f in csv_files]
result = pd.concat(all_legs, ignore_index=True)

# Summary
print(f"\nCombined results:")
print(f"  Total output rows : {len(result):,}")
print(f"\nRows per Leg_Index:")
print(result.groupby("Leg_Index").size().rename("rows").to_string())

# Save
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved to '{OUTPUT_FILE}'")
