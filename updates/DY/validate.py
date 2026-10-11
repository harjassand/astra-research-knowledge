#!/usr/bin/env python3
"""Validate DY using the shared compact DX/DY intake validator; no research execution."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1] / 'DX' / 'validate.py'))['main']('DY', 2, 51426)
