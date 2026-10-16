"""Own code only. Needs Python, NumPy, SciPy, SymPy and PyMuPDF already available."""
from pathlib import Path
import subprocess,sys,hashlib,time
p=Path(__file__).parent
for line in (p/'SHA256SUMS').read_text().splitlines():
 h,f=line.split('  ',1); assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h,f
scripts=[
 'measurement/check_shared_bath.py',
 'measurement/check_independent_phase_bridge.py',
 'measurement/check_deterministic_cells_independent.py',
 'measurement/check_measurement_cost_criterion.py',
 'measurement/check_partial_dephasing.py',
 'detector_footprints/check_complete_detectors.py',
 'detector_footprints/independent_audit_detector_footprints.py',
 'experiments/extract_slichter_figure4.py']
t=time.monotonic()
for s in scripts:
 q=p/s
 r=subprocess.run([sys.executable,str(q)],cwd=q.parent,capture_output=True,text=True)
 if r.returncode: print(r.stdout,r.stderr);raise SystemExit(r.returncode)
 print('PASS',s)
print('PASS all',len(scripts),'checks; elapsed seconds',round(time.monotonic()-t,3))
