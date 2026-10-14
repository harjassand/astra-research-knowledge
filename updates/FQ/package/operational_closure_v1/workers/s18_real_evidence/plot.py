#!/usr/bin/env python3
"""Render one measured interior hysteresis cycle (requires matplotlib)."""

import csv
import io
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt


here = Path(__file__).resolve().parent
source = here / "source" / "Data_v1.0.0.zip"
member = "Data.v1.0.0/02_SMAWD/02_8wires_sin20mm_0p5Hz.csv"
with zipfile.ZipFile(source) as archive, archive.open(member) as raw:
    rows = [r for r in csv.DictReader(io.TextIOWrapper(raw)) if 10 <= float(r["Time"]) < 12]
x = [float(r["Actuator1_Disp"]) for r in rows]
f = [float(r["Actuator1_Force"]) for r in rows]

fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.plot(x, f, color="#24466b", linewidth=1.7)
ax.axvline(10, color="#bd561e", linewidth=1.1, linestyle="--", label="+10 mm crossing")
ax.set(xlabel="Measured actuator displacement (mm)", ylabel="Measured actuator force (kN)",
       title="8-wire SMA damper, 0.5 Hz, one measured cycle (10–12 s)")
ax.grid(alpha=0.2)
ax.legend(loc="upper left")
fig.tight_layout()
output = here / "hysteresis_cycle.png"
fig.savefig(output, dpi=180)
print(output)
