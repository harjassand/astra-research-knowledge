import numpy as np,json
from pathlib import Path
I=np.eye(2); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1])
v=np.array([1,0,0,1])/np.sqrt(2); bell=np.outer(v,v); product=np.eye(4)/4
# Original memory marginal becomes final accessible output after the fixed SWAP.
def marginal_after(A,rho):
 t=sum(np.kron(a,I)@rho@np.kron(a.conj().T,I) for a in A)
 return np.einsum('ijil->jl',t.reshape(2,2,2,2))
rng=np.random.default_rng(28);err=0
for _ in range(100):
 g=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));u,_=np.linalg.qr(g)
 err=max(err,float(np.max(np.abs(marginal_after([u],bell)-marginal_after([u],product)))))
P=(I+Z)/2;Q=(I-Z)/2
p_bell=sum(float(np.trace(a@marginal_after([a],bell)).real) for a in [P,Q])
p_product=sum(float(np.trace(a@marginal_after([a],product)).real) for a in [P,Q])
assert err<1e-12 and abs(p_bell-1)<1e-12 and abs(p_product-.5)<1e-12
out={'status':'PASS','random_unitary_cases':100,'max_unconditioned_output_difference':err,'instrument_record_final_match_bell':p_bell,'instrument_record_final_match_product':p_product,'source_calls':0,'scope':'algebraic model check, not acquired data or hardware'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
