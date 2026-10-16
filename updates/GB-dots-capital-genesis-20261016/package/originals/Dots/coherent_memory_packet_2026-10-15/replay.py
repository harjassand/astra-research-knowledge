from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
if not __debug__: raise RuntimeError('Run with assertions enabled, without -O or PYTHONOPTIMIZE')
for name in ['check_exact.py','check_bath_exact.py','check_numeric.py','check_microscopic_envelope.py']:
    print('=== '+name+' ===',flush=True)
    subprocess.run([sys.executable,str(root/'checks'/name)],check=True,cwd=root)
print('PASS: all four scripts completed; numerical outputs are illustrations, not a lifetime proof.')
