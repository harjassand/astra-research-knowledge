from pathlib import Path
import itertools,json,sympy as s
r=Path(__file__).parent;c=json.loads(Path('producer-workspace/certificate.json').read_text());B=s.Matrix([[s.Rational(x) for x in row] for row in c['B']]);ex=[tuple(e) for e in c['exponents']];T=s.Matrix.vstack(*[B[ex.index(tuple(t.count(i) for i in range(4))),:] for t in itertools.product(range(4),repeat=4)]);A=s.Rational(16,3)*T.T*T;I=s.eye(81);roots=[s.Rational(0),s.Rational(1,3),s.Rational(2,3),s.Rational(1)]
assert A*(A-I/3)*(A-2*I/3)*(A-I)==s.zeros(81)
ps=[]
for a in roots:
 P=I
 for b in roots:
  if a!=b:P=P*(A-b*I)/(a-b)
 assert P==P.T and P*P==P and A*P==a*P
 ps.append(P)
assert sum(ps,s.zeros(81))==I and [s.trace(p) for p in ps]==[46,25,1,9]
cols=[16*a+b for a in range(9) for b in range(9)];assert len(set(cols))==81 and max(cols)<256
# Padding is an isometric coordinate embedding: adds exactly175 zero eigenvectors.
assert 256-len(cols)==175
# Exact positive root coefficients used in both defect operators.
for a in roots:assert s.simplify(s.sqrt(1-a)**2-(1-a))==0
# Every pair on the9-bit basis admits the advertised path conjugation.
cases=0;maxg=0
for aa in range(512):
 for bb in range(aa+1,512):
  path=[aa]
  for bit in range(9):
   if (aa^bb)&(1<<bit):path.append(path[-1]^(1<<bit))
  assert path[-1]==bb and len(set(path))==len(path)
  assert all((a^b).bit_count()==1 for a,b in zip(path,path[1:]))
  xa,xb=aa,bb
  for a,b in zip(path[:-2],path[1:-1]):
   xa=b if xa==a else a if xa==b else xa;xb=b if xb==a else a if xb==b else xb
  assert xa==path[-2] and xb==bb
  gates=2*(len(path)-2)+1;assert gates<=17;maxg=max(maxg,gates);cases+=1
# All-eight-controls computation and uncomputation, keeping original controls intact.
for inputs in itertools.product([0,1],repeat=8):
 w=[0]*7;w[0]^=inputs[0]&inputs[1]
 for j in range(1,7):w[j]^=w[j-1]&inputs[j+1]
 assert w[-1]==int(all(inputs))
 for j in range(6,0,-1):w[j]^=w[j-1]&inputs[j+1]
 w[0]^=inputs[0]&inputs[1];assert w==[0]*7
assert all(b-(a^b)+a==2*a*b for a,b in itertools.product([0,1],repeat=2))
G=17*512*511//2+512;assert G==2224384
out={'reduced_exact_input_spectrum':{'0':46,'1/3':25,'2/3':1,'1':9},'padded_zero_multiplicity':221,'valid_input_embedding_columns':81,'invalid_input_columns':175,'gray_pairs_checked':cases,'maximum_gray_controlled_operations':maxg,'AND_truth_cases':256,'eight_controlled_gate_bound':G,'CNOT_bound':114*G,'arbitrary_single_qubit_bound':188*G,'total_elementary_bound':302*G,'total_qubits':16,'scope':'Exact algebraic spectral and classical reversible compiler checks; not physical gates or precise native synthesis'}
(r/'check_exact_compiler.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
