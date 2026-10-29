import runpy,contextlib,io,numpy as np,json
from pathlib import Path
p=Path('producer-workspace/check_retained_memory_bank_v4.py')
with contextlib.redirect_stdout(io.StringIO()): z=runpy.run_path(str(p))
np.savez(Path(__file__).with_name('actual_bank_counters.npz'),sums=z['sums'],Jembed=z['Jembed'],O=z['O'],moments=z['moments'],coeff=z['coeff'],bath=z['bath'])
print(json.dumps({'empirical_singular_values':[np.linalg.svd(x/1e6-z['Jembed'],compute_uv=False).tolist() for x in z['sums']],'last_rows':z['rows'][-1]},indent=2))
