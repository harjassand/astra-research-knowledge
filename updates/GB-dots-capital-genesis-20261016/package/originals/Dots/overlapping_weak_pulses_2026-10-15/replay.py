from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parent
if not __debug__: raise RuntimeError('Enable assertions; do not use -O or PYTHONOPTIMIZE')
mode=sys.argv[1:] or ['--all']
if mode not in [['--all'],['--exact'],['--numeric']]: raise SystemExit('Usage: replay.py [--exact|--numeric]')
for kind in ['exact','numeric']:
 if mode==['--exact'] and kind!='exact':continue
 if mode==['--numeric'] and kind!='numeric':continue
 for p in sorted((r/'checks'/kind).glob('*.py')):
  print('=== '+kind+': '+p.name+' ===',flush=True)
  subprocess.run([sys.executable,str(p)],cwd=r,check=True)
print('PASS: selected finite certificates completed; no complete-memory or hardware verification implied.')
