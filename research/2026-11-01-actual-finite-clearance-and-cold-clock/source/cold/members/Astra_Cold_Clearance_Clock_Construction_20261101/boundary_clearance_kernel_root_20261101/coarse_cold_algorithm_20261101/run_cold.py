#!/usr/bin/env python3
"""Mandatory fresh pipeline; no fine certificate or dynamic source execution."""
from pathlib import Path
import subprocess
import sys
from coarse_windows import check_sources

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    check_sources()
    for name in ('coarse_clock.py','independent_coarse_verify.py','coarse_windows.py'):
        subprocess.run([sys.executable,str(here/name)],check=True,cwd=str(here))
