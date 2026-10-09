#!/usr/bin/env python3
"""Short deterministic check of the explicit rational construction; no searches."""
from pathlib import Path
import sys,json,itertools,importlib.util
sys.dont_write_bytecode=True
import sympy as sp
import numpy as np
root=Path(__file__).resolve().parent
q=sp.Rational
a=sp.diag(q(25,64),q(7,64));b=sp.diag(q(7,64),q(25,64));o=sp.eye(2)/5
W=a.row_join(o).col_join(o.row_join(b))
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
require(sp.trace(W)==1,'trace')
minors=[]
for k in range(1,5):
    for idx in itertools.combinations(range(4),k):
        value=W.extract(idx,idx).det();require(value>0,'positive principal minor');minors.append(str(value))
require(2*sp.trace(o)==q(4,5),'coherence')
r=sp.sqrt(175)/32;cp=sp.simplify(r+q(4,25)/r)
require(bool(cp>q(4,5)),'strict coherence improvement')
spec=importlib.util.spec_from_file_location('binary_fixture',root/'broadcast_inequality/iterate_binary_squash.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
w=np.array(W.tolist(),dtype=float);out=module.sym(w,.8)
value=float(module.cmi(out));initial=float(module.cmi(w))
ef=module.h(np.array([.8,.2]));ed=1-module.h(np.array([.9,.1]));target=float(ef+ed)
require(abs(value-1.4275011456)<1e-8,'reported finite CMI value')
require(value<initial and value>target,'improvement without violation')
require(abs(float(np.trace(out))-1)<1e-12,'numeric output trace')
require(np.linalg.eigvalsh(out).min()>-1e-12,'numeric output positivity')
expected=float(q(4,5)/cp)*initial
require(abs(value-expected)<1e-10,'CMI scaling formula')
report={'status':'PASS','exact_checks':['Rational input trace 1','15 strictly positive exact principal minors','Exact input coherence 4/5','Exact cprime > 4/5'], 'floating_checks':{'initial_cmi_bits':initial,'symmetrized_cmi_bits':value,'formation_plus_distillation_bits':target,'formula_residual':abs(value-expected)},'scope':'One explicit construction only. Entropy values use floating eigensolvers. No optimizer run, conjecture certificate or global exclusion.'}
print(json.dumps(report,indent=2))
