from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Run with assertions enabled; do not use -O or PYTHONOPTIMIZE')
for kind in ['core','refinement','detector']:
 for p in sorted((r/'checks'/kind).glob('*.py')):
  print('=== '+kind+': '+p.name+' ===',flush=True)
  subprocess.run([sys.executable,str(p)],cwd=r,check=True)
print('PASS: five exact certificates completed; no full-theorem, benchmark or hardware verification implied.')
