import numpy as np, itertools, json
from pathlib import Path
# Exhaustive all records for small finite groups, not Monte Carlo acquisition.
rows=[]
for K in [4,8]:
 roots=np.exp(2j*np.pi*np.arange(K)/K)
 for N in [1,2,3]:
  for p in [.1,.25,.4]:
   a=1-2*p
   for j in [0,1]:
    theta=np.pi*j/K;mean=0j;second=0.;mass=0.
    for rec in itertools.product(range(2*K),repeat=N):
     prob=1.;S=0j
     for z in rec:
      l=z//2;y=1 if z%2 else -1
      prob*= (1+y*a*np.cos(2*theta-2*np.pi*l/K))/(2*K)
      S+=y*roots[l]
     # Exact algebraic cancellation recognized with floating tolerance in fixture only.
     r=0j if abs(S)<1e-12 else S/abs(S)
     mean+=prob*r*np.exp(-2j*theta);mass+=prob
     m=2*S/(a*N);second+=prob*abs(m-np.exp(2j*theta))**2
    v=(4/a**2-1)/N
    assert abs(mass-1)<1e-11 and abs(mean.imag)<1e-11 and abs(second-v)<1e-10
    b=(1-mean.real)/2;assert b<=min(1,v)+1e-11
    rows.append({'K':K,'N':N,'p':p,'grid_index':j,'averaged_complete_loss':b,'variance':second,'bound':min(1,v),'imaginary_residual':float(mean.imag)})
out={'status':'PASS_AUTHOR_EXHAUSTIVE_FINITE_RECORD_FIXTURES','fixtures':len(rows),'scope':'No production gate compiler or hardware; enumeration checks exact finite-group identities numerically. Analytical source governs arbitrary N and continuous-angle bound.','rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(rows))
