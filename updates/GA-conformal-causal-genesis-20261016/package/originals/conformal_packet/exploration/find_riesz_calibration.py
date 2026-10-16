import sympy as s, itertools, random, sys, json
from pathlib import Path
root=Path(__file__).parent
order=int(sys.argv[1]) if len(sys.argv)>1 else 2
A=s.symbols('a b c d');a,b,c,d=A
C=a**3+5*a*a*d-4*a*b*c+a*c*c+2*a*d*d-2*b*c*d+c*c*d
terms=[(i,j,k,s.diff(C,A[i],A[j],A[k])/6) for i in range(4) for j in range(4) for k in range(4) if s.diff(C,A[i],A[j],A[k])]
def grad(k,i):return (k[0],k[1],0,0) if i==0 else (0,0,k[0],k[1])
def zp(X,Y):
 a,b,c,d=X;e,f,g,h=Y
 return (a*e+c*g,b*f+d*h,(a*f+b*e+c*h+d*g)/s.Integer(2),(a*h+d*e-b*g-c*f)/s.Integer(2))
def tv(X):return(2*X[0]+X[3],X[2])
def angle(k):return [s.Rational(k[0]**(order-j)*k[1]**j,(k[0]**2+k[1]**2)**(order//2)) for j in range(order+1)]
random.seed(42);rows=[];rhs=[];triples=[]
for z in range(24):
 p=(random.randint(-4,4),random.randint(-4,4));l=(random.randint(-4,4),random.randint(-4,4));k=(-p[0]-l[0],-p[1]-l[1])
 if not all(any(x) for x in [p,l,k]):continue
 for typ in itertools.product(range(2),repeat=3):
  freq=[k,p,l];vs=[grad(freq[i],typ[i]) for i in range(3)]
  val=sum(c*vs[0][i]*vs[1][j]*vs[2][kk] for i,j,kk,c in terms)
  row=[s.Rational(0) for _ in range(8*(order+1))]
  for i in range(3):
   T=tv(vs[i]);Z=zp(vs[(i+1)%3],vs[(i+2)%3]);ang=angle(freq[i])
   for ii in range(2):
    for jj in range(4):
     for h in range(order+1):row[(ii*4+jj)*(order+1)+h]+=T[ii]*Z[jj]*ang[h]/3
  rows.append(row);rhs.append(val);triples.append([freq,typ])
M=s.Matrix(rows);b=s.Matrix(rhs)
print('shape',M.shape,flush=True)
rr,piv=M.row_join(b).rref();rank=sum(p<M.cols for p in piv);aug=len(piv)
print('ranks',rank,aug,'free',M.cols-rank,flush=True)
result={'degree':order,'n_variables':M.cols,'rank':rank,'augmented_rank':aug,'status':'IDENTITY_INFEASIBLE' if aug>rank else 'IDENTITY_FEASIBLE','sample_scope':'exact selected Fourier triads; inconsistency suffices for declared multiplier class only'}
if aug==rank:
 sol=s.linsolve((M,b));print(sol)
 result['solution']=str(sol)
(root/f'linear_riesz_identity_degree{order}.json').write_text(json.dumps(result,indent=2))
