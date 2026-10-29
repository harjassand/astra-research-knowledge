import sympy as s,itertools,json
from pathlib import Path
root=Path(__file__).parent;src=Path('producer-workspace/certificate.json');z=json.loads(src.read_text());B=s.Matrix([[s.Rational(v) for v in row] for row in z['B']]);ex=[tuple(e) for e in z['exponents']];T=s.Matrix.vstack(*[B[ex.index(tuple(t.count(i) for i in range(4))),:] for t in itertools.product(range(4),repeat=4)])
I3=s.eye(3);I4=s.eye(4);I9=s.eye(9)
def kron_all(xs):
 out=s.Matrix([[1]])
 for x in xs:out=s.kronecker_product(out,x)
 return out
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import QQ
def dm(a):return DomainMatrix.from_Matrix(a).convert_to(QQ)
def mm(a,b):return dm(a).matmul(dm(b)).to_Matrix()
checks=0
# Hamilton left/right multiplication by each pure unit quaternion.
for a in range(3):
 e=s.eye(3)[:,a]
 skew=s.Matrix([[0,-e[2],e[1]],[e[2],0,-e[0]],[-e[1],e[0],0]])
 for side in ['left','right']:
  Q=s.zeros(4);Q[0,1:]=-e.T;Q[1:,0]=e;Q[1:,1:]=skew if side=='left' else -skew
  D=s.kronecker_product(2*skew,I3) if side=='left' else s.kronecker_product(I3,(2*skew).T)
  Din=s.kronecker_product(D,I9)+s.kronecker_product(I9,D)
  Dout=sum((kron_all([Q if j==i else I4 for j in range(4)]) for i in range(4)),s.zeros(256))
  assert mm(T,Din)==mm(Dout,T)
  checks+=1
# Independently evaluate full pair matrices at three rational points, interpolate the quadratic output.
u=s.Matrix([1,0,0,0,1,0,0,0,1]);P=u*u.T/3
blocks=[T[64*i:64*(i+1),:] for i in range(4)]
def reduced(v):
 tau=(1-v)*P+v*(I9-P)/8;pair=s.kronecker_product(tau,tau);out=s.zeros(4)
 for i in range(4):
  for j in range(4):out[i,j]=s.Rational(16,3)*sum(a*b for a,b in zip(mm(blocks[i],pair),blocks[j]))
 return out
samples={v:reduced(v) for v in [s.Rational(0),s.Rational(1,2),s.Rational(1)]};v=s.symbols('v');O=s.Matrix(4,4,lambda i,j:s.factor(s.interpolate([(a,m[i,j]) for a,m in samples.items()],v)))
expected=s.diag((216*v*v-453*v+256)/432,*[v*(62-9*v)/864]*3);assert s.simplify(O-expected)==s.zeros(4)
p=s.factor(s.trace(O));w=s.factor(3*O[1,1]/p);assert s.limit(w/v,v,0)==s.Rational(93,256)
# Bell-basis transform preserves maximally mixed term and maps target |0> to Bell |I>.
pa=[s.eye(2),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
C=s.Matrix.hstack(*[s.Matrix(list(a if j==0 else -s.I*a))/s.sqrt(2) for j,a in enumerate(pa)])
assert C.H*C==s.eye(4)
Ch=C*(O/p)*C.H
marg=s.Matrix(2,2,lambda a,b:sum(Ch[2*i+a,2*i+b] for i in range(2)))
assert s.simplify(marg-I3[:2,:2]/2)==s.zeros(2)
out={'exact_left_right_generator_intertwiners':checks,'quadratic_output_reconstructed_from_full_pair_matrices':True,'success':str(p),'program_infidelity':str(w),'small_v_slope':'93/256','Choi_input_marginal_exact':'I2/2','convex_depolarizing_range':'0<=v<=8/9','depolarizing_mixture_parameter':'4w/3','source_assumption':'two independent identical isotropic rotation programs'}
(root/'independent_covariance_fast.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
