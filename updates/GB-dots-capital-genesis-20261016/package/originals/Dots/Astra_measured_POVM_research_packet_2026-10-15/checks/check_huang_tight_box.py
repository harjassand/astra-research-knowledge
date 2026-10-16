from pathlib import Path
exec(open(Path(__file__).resolve().parent/'check_huang_frozen.py').read())
ph=json.loads((p/'physical_half_box_candidate.json').read_text());print('candidate keys',ph.keys())
Fh=[(S.Matrix(e['real_numerators'])+S.I*S.Matrix(e['imag_numerators']))/ph['denominator'] for e in ph['effects']]
assert sum(Fh,S.zeros(4))==S.eye(4)
for e,er in zip(Fh,E):
 assert e==e.conjugate().T and all(e[:k,:k].det()>0 for k in range(1,5))
 assert all(abs(S.re(v))<=S.Rational(1,2000) and abs(S.im(v))<=S.Rational(1,2000) for v in e-er)
# Solve each relaxed four-variable LP by enumerating vertices, independently of greedy algorithm.
from itertools import product
for tau in [S.Rational(1,2000),S.Rational(1,1000)]:
 upper=0
 for i in range(4):
  for j in range(i,4):
   for imag in ([False] if i==j else [False,True]):
    lower=[];higher=[];cs=[]
    for er,loss in zip(E,losses):
     centers=[S.im(er[i,j]),-S.im(er[j,i])] if imag else [S.re(er[i,j]),S.re(er[j,i])]
     lower.append(max(centers)-tau);higher.append(min(centers)+tau)
     cs.append(S.simplify((1 if i==j else 2)*(S.im(loss[i,j]) if imag else S.re(loss[i,j]))))
    total=1 if i==j else 0;candidates=[]
    for free in range(4):
     others=[k for k in range(4) if k!=free]
     for bits in product([0,1],repeat=3):
      val=[None]*4
      for k,bit in zip(others,bits):val[k]=(lower if bit==0 else higher)[k]
      val[free]=total-sum(val[k] for k in others)
      if lower[free]<=val[free]<=higher[free]:candidates.append(S.simplify(sum(x*c for x,c in zip(val,cs))))
    best=max(candidates,key=lambda x:float(x))
    assert all(S.simplify(best-x)>=0 for x in candidates)
    upper+=best
 upper=S.simplify(upper)
 print('Independent LP vertex upper',tau,S.N(upper,20),'q45 gap',S.N(S.Rational(524,605)-upper,20),'q43 gap',S.N(source-upper,20))
 assert upper==S.sympify(json.loads((p/'tight_box_certificate.json').read_text())[0 if tau==S.Rational(1,2000) else 1]['risk_upper_exact'])
print('Physical half-box and independent vertex-enumerated risk bound PASS')
