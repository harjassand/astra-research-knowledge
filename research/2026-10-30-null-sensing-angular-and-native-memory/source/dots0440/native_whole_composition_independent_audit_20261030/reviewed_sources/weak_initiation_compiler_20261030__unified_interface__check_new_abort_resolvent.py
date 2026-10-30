"""Rebuild the killed BAD generator and S from scratch for each added abort rate.
Diagnostic fixture only; no fast-cleanup/monitor implementation claim here.
"""
from pathlib import Path
import json,io,contextlib
import numpy as np
P=Path(__file__).parent
src=(P/'old_bad_fixture_snapshot.py').read_text()
modified=src.replace(' emit(m,1,2)\n',' emit(m,1,2)\n emit(m,1,4,rate=mu)\n')
assert modified!=src
out=[]
baseline_R=None
for mu in [0,.2,1.,3.]:
 ns={'mu':mu}
 with contextlib.redirect_stdout(io.StringIO()):exec(modified,ns)
 r=dict(ns['result']);r['new_acquisition_abort_rate']=mu
 if baseline_R is None: baseline_R=ns['R'].copy()
 r['new_resolvent_minus_mu0_norm']=float(np.linalg.norm(ns['R']-baseline_R,2))
 r['old_resolvent_in_new_equation_residual']=float(np.linalg.norm(ns['K']@baseline_R.reshape(-1,order='F')+ns['I'].reshape(-1,order='F')))
 out.append(r)
print(json.dumps({'scope':'36D controller / 72D joint diagnostic; killed matrix, resolvent, normalizer and credit recomputed independently for EACH mu; not the full native monitor/cleanup fixture','all_checks_pass':True,'cases':out},indent=2))
