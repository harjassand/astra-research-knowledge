from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parent
if not __debug__: raise RuntimeError('Assertions must remain enabled; do not use -O or PYTHONOPTIMIZE')
for name in ['check_syndrome_sandwich_exact.py','check_composition_algebra.py']:
 print('=== '+name+' ===',flush=True)
 subprocess.run([sys.executable,str(r/'checks'/name)],cwd=r,check=True)
print('PASS: both exact certificates completed. This is not a complete memory-proof or hardware verification.')
