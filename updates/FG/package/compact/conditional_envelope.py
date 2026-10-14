"""Two-source conditional-envelope closure.
Compiles bounds for every hidden bath from local weight/conductance envelopes.
No hidden-bath states, transition alphabet, normalizer or rate queries enter it.
The small resolved gate block is deliberately explicit for an exact audit of
this more general closure; large tensor experiments use the constant-envelope case.
"""
from fractions import Fraction as F
from time import perf_counter
from pathlib import Path
import sympy as s,json
BASE=Path(__file__).resolve().parent

def compile_envelope(n=4,R=100,feature='all_open'):
 t=perf_counter();N=2**n;q=s.Rational(1,26);eps=s.Rational(1,10000)
 m=s.Matrix([q**g.bit_count()*(1-q)**(n-g.bit_count()) for g in range(N)])
 indicator={'all_open':lambda g:int(g==N-1),'first_open':lambda g:g&1,'all_closed':lambda g:int(g==0)}[feature]
 l=[s.Rational(1)]*N;u=[1+(s.Rational(R)-1)*indicator(g) for g in range(N)]
 def form(weights):
  A=s.zeros(N)
  for g in range(N):
   A[g,g]+=m[g]*weights[g]*q*(1 if (g>>(n-1))&1 else eps)
   for i in range(n):
    if (g>>i)&1:continue
    h=g|(1<<i);c=m[g]*q*(1 if i==0 or (g>>(i-1))&1 else eps)*min(weights[g],weights[h])
    A[g,g]+=c;A[h,h]+=c;A[g,h]-=c;A[h,g]-=c
  return A
 Aminus=form(l);Aplus=form(u);bminus=s.Matrix([m[i]*l[i] for i in range(N)]);bplus=s.Matrix([m[i]*u[i] for i in range(N)])
 lower=(bminus.T*Aplus.inv()*bminus)[0]/sum(bplus)
 upper=(bplus.T*Aminus.inv()*bplus)[0]/sum(bminus)
 tau0=(m.T*Aminus.inv()*m)[0]
 return {'gate_coordinates':n,'gate_states':N,'feature':feature,'R':R,'lower_exact':str(lower),'upper_exact':str(upper),'baseline_exact':str(tau0),'lower':float(lower),'upper':float(upper),'ratio':float(upper/lower),'scalar_envelope_ratio':float(s.Rational(R)**4),'hidden_states_constructed':0,'unknown_bath_equilibrium_samples':0,'seconds':perf_counter()-t}

if __name__=='__main__':
 out=[compile_envelope(feature=f,R=r) for f in ['all_open','first_open','all_closed'] for r in [3,100]]
 (BASE/'conditional_envelope_results.json').write_text(json.dumps(out,indent=2));print(json.dumps([{k:r[k] for k in ['feature','R','lower','upper','ratio','scalar_envelope_ratio','seconds']} for r in out],indent=2))
