"""Exact counterexample to treating the coherence Schur complement as Markov."""
import json
from pathlib import Path
import sympy as s
from checks import sector

states,h,_,_=sector(4,2); D=len(states)
H=s.Matrix([[s.Rational(str(float(z.real))) for z in row] for row in h])
A=-s.I*(s.kronecker_product(s.eye(D),H)-s.kronecker_product(H.T,s.eye(D)))
pop=list(range(0,D*D,D+1)); off=[x for x in range(D*D) if x%(D+1)!=0]
rates=[s.Rational(1,4)*(x^y).bit_count() for y in states for x in states]
C=s.diag(*[rates[x] for x in off])+A.extract(off,off)
y=C.inv(method='DM')*A.extract(off,[pop[0]])
entry=s.simplify(-(A.extract([pop[5]],off)*y)[0])
assert entry==s.Rational(115904,10076409)>0
out={'n':4,'sector_particles':2,'t':'1','U':'4','V':'1','d':'1/2',
     'row_configuration':states[5],'column_configuration':states[0],
     'effective_B_offdiagonal':str(entry),'float':float(entry),
     'meaning':'Positive offdiagonal of negative-generator Schur complement requires a negative Markov rate.',
     'arithmetic':'exact rational/symbolic'}
Path(__file__).with_name('schur_exact.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
