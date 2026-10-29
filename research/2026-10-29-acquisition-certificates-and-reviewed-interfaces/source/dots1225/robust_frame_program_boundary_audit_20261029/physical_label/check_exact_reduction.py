"""Independent exact collective-source and actual commutator-output checks."""
import sympy as S,json
from pathlib import Path
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);Z=S.diag(1,-1);P=[S.kronecker_product(a,b) for a in [X,Y,Z] for b in [X,Y,Z]]
sing=S.Matrix([0,1,-1,0])/S.sqrt(2);trip=[S.Matrix([1,0,0,0]),S.Matrix([0,1,1,0])/S.sqrt(2),S.Matrix([0,0,0,1])];Ps=sing*sing.H;Pt=S.eye(4)-Ps;swap=S.eye(4)-2*Ps
K=[Ps]+[a*b.H/S.sqrt(3) for a in trip for b in trip]
def clean(A):return A.applyfunc(S.simplify)
def summ(items,shape):return sum(items,S.zeros(*shape))
def gram(ks):
 cs=[]
 for k in ks:
  cols=[(k*p-p*k).reshape(16,1) for p in P];cs.append(S.Matrix.hstack(*cols))
 C=S.Matrix.vstack(*cs);return clean(C.H*C/8)
def choi(ks):return clean(summ([k.reshape(16,1)*k.reshape(16,1).H for k in ks],(16,16)))
assert clean(summ([k.H*k for k in K],(4,4)))==S.eye(4)
assert clean(summ([k*k.H for k in K],(4,4)))==S.eye(4)
for a in range(4):
 for b in range(4):
  e=S.zeros(4);e[a,b]=1
  assert clean(summ([k*e*k.H for k in K],(4,4)))==clean(Ps*e*Ps+S.trace(Pt*e)*Pt/3)
J=choi(K);assert J.eigenvals()=={S.Rational(1):1,S.Rational(1,3):9,S.Rational(0):6}
D=[]
for a in range(4):
 for b in range(4):
  k=S.zeros(4);k[a,b]=S.Rational(1,2);D.append(k)
assert choi(D)==S.eye(16)/4 and gram(D)==S.eye(9)
checks=0
for V in [S.eye(2),S.Rational(3,5)*I-S.I*S.Rational(4,5)*X]:
 W=S.kronecker_product(V,I);ks=[W*k*W.H for k in K];Srot=clean(W*swap*W.H)
 c=S.Matrix([S.trace(p*Srot)/(2*S.sqrt(3)) for p in P]);assert clean(c.H*c)==S.ones(1)
 H=gram(ks);Pc=clean(c*c.H);assert H==S.eye(9)-Pc
 for eta in [S.Rational(0),S.Rational(1,100),S.Rational(1,2),S.Rational(1)]:
  mix=[S.sqrt(1-eta)*k for k in ks]+[S.sqrt(eta)*k for k in D]
  # Explicit branch amplitudes, with control-minus 1/2, uniform9 label, and I4/4 input.
  amplitudes=[[clean((k*p-p*k)/6) for p in P] for k in mix]
  output=S.zeros(9)
  for branch in amplitudes:
   for a in range(9):
    for b in range(9):output[a,b]+=S.trace(branch[a]*branch[b].H)/4
  output=clean(output);expected=(S.eye(9)-(1-eta)*Pc)/18
  assert output==expected
  prob=S.trace(output);assert prob==(8+eta)/18
  state=clean(output/prob);assert S.simplify((c.H*state*c)[0])==eta/(8+eta)
  assert state==clean((S.eye(9)-Pc+eta*Pc)/(8+eta));checks+=1
out={'exact_channel_matrix_units':16,'exact_source_twists':2,'exact_actual_minus_instruments':checks,'untwisted_Choi_spectrum':{'1':1,'1/3':9,'0':6},'scope':'Exact finite dimensional ideal memoryless source identities, not measured hardware, source acquisition or a general correlated-noise reduction.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
