#!/usr/bin/env python3
"""Materialize two source-geometry PETS2 branches, without running a solver.

Usage: python3 prepare_hpm_replay.py /absolute/new/staging/directory
Requires only the standard library. The staging directory must not exist.
"""
from pathlib import Path
import hashlib
import shutil
import sys
import zipfile

BASE = Path(__file__).resolve().parent
PIN = 'c9b927414929aa8e6a4e08579793d222c741c70086c1ed6944a471ec8b84251d'


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    target = Path(sys.argv[1]).expanduser().resolve()
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing staging directory')
    archive = BASE / 'data/HPM-1_RT.zip'
    if hashlib.sha256(archive.read_bytes()).hexdigest() != PIN:
        raise SystemExit('Raw archive does not match the frozen pin')
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            path = Path(member.filename)
            if path.is_absolute() or '..' in path.parts:
                raise SystemExit('Unsafe archive member')
        z.extractall(target)
    root = target / 'HPM-1_RT'
    source = (root / 'crs3.pts2').read_text()
    for stem, exclude in [('source_with_fills', False), ('detector_files_only', True)]:
        output = []
        inside = False
        for line in source.splitlines():
            if line.strip() == 'imagelist':
                inside = True
            elif line.strip() == 'endimagelist':
                inside = False
            elif inside and line.strip():
                fields = line.split()
                if exclude and fields[0].endswith('i.tiff'):
                    fields[8] = '0'
                    line = ' '.join(fields)
            output.append(line)
        (root / (stem + '.pts2')).write_text('\n'.join(output) + '\n')
        for suffix in ['.cenloc', '.celllist']:
            shutil.copy2(root / ('crs3' + suffix), root / (stem + suffix))
    (root / 'REPLAY_STATUS.txt').write_text(
        'Staged source files and two inclusion branches only. No solver was run.\n'
        'Both branches retain the source-supplied fitted geometry.\n'
        '22 i TIFFs are deterministic fills, not independent detector observations.\n'
        'Read REPLAY_CONTRACT.txt before interpreting any atomic-hand output.\n')
    print(root)


if __name__ == '__main__':
    main()
