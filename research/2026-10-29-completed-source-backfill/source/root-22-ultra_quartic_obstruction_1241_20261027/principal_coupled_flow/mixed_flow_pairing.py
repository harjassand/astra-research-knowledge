"""Test a new output-coupled parabolic operation against the exact obstruction.

Flow v_t=Delta v+2*b*J*partial12(v), J=90degree output rotation.
The Fourier symbol has real part-|k|² for every real b. Dissipation after
integration by parts adds b*(H[B1,J B2]+H[B2,J B1]).
"""
from pathlib import Path
from itertools import combinations_with_replacement
from fractions import Fraction
import sympy as s
import json,hashlib,time
ROOT=Path(__file__).resolve().parent
SOURCE=Path('producer-workspace/EXACT_HEAT_SEPARATOR.json')
raw=SOURCE.read_bytes();cert=json.loads(raw)
x=s.symbols('a b c d');a,b,c,d=x;z=s.symbols('z0:6')
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=u*u+v*v+3*w*w+16*q*q+4*q*(u-v)
B1=s.Matrix([z[0],z[1],z[3],z[4]])
B2=s.Matrix([z[1],z[2],z[4],z[5]])
J=s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
xp=list(combinations_with_replacement(range(4),2))
zp=list(combinations_with_replacement(range(6),2))
lam=list(map(Fraction,cert['lambda_xpair_zpair']))

def coefficient_vector(expr):
    out=[Fraction(0)]*210
    for powers,coefficient in s.Poly(s.expand(expr),*x,*z).terms():
        xi=tuple(i for i,p in enumerate(powers[:4]) for _ in range(p))
        zi=tuple(i for i,p in enumerate(powers[4:]) for _ in range(p))
        assert len(xi)==len(zi)==2
        out[xp.index(xi)*21+zp.index(zi)]+=Fraction(coefficient)
    return out

start=time.monotonic();rows=[]
for name,poly in [('F',F),('det2',q*q)]:
    H=s.hessian(poly,x)
    standard=(B1.T*H*B1)[0]+(B2.T*H*B2)[0]
    mixed=(B1.T*H*J*B2)[0]+(B2.T*H*J*B1)[0]
    vs=coefficient_vector(standard);vm=coefficient_vector(mixed)
    ps=sum((a*b for a,b in zip(lam,vs)),Fraction(0))
    pm=sum((a*b for a,b in zip(lam,vm)),Fraction(0))
    rows.append({'energy':name,'standard_pairing':str(ps),'mixed_pairing':str(pm),
      'mixed_coefficient_vector':[str(c) for c in vm]})
assert rows[0]['standard_pairing']=='-4049717/6250000'
assert rows[1]['standard_pairing']=='80001/25000000'
out={'status':'EXACT_NEW_COUPLED_FLOW_PAIRINGS','flow':'v_t=Delta v+2*b*J*partial12v',
 'source_separator_sha256':hashlib.sha256(raw).hexdigest(),'rows':rows,
 'seconds':time.monotonic()-start,
 'scope':'Exact algebraic pairing for a new constant output-coupled flow. No QC/flow monotonicity or novelty conclusion from pairings alone.'}
(ROOT/'PAIRINGS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({**out,'rows':[{k:v for k,v in r.items() if k!='mixed_coefficient_vector'} for r in rows]},indent=2))
