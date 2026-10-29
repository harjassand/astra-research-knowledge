import json,sys,math,time
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path('producer-workspace/grevlex_coordinate_recovery_20261029');src=Path('producer-workspace/grevlex_value_oracle_20261029');o=Path(__file__).parent
j=json.loads((src/'quotient.json').read_text());f=json.loads((r/'left_eigenvector_finder.json').read_text());n=40;S=2**int(f['dyadic_bits']);st=time.time()
I=[[S*int(i==k) for k in range(n)] for i in range(n)];zero=[[0]*n for i in range(n)]
def norm(A):return F(max(sum(abs(t) for t in row) for row in A),S)
def plus(a,b,sgn=1):return [[x+sgn*y for x,y in zip(u,v)] for u,v in zip(a[0],b[0])],a[1]+b[1]
def times(a,b):
 BT=list(zip(*b[0]));C=[[sum(x*y for x,y in zip(row,col))//S for col in BT] for row in a[0]]
 return C,norm(a[0])*b[1]+norm(b[0])*a[1]+a[1]*b[1]+F(n,S)
def scalar(a,c):
 c=F(c);return [[v*c.numerator//c.denominator for v in row] for row in a[0]],abs(c)*a[1]+F(n,S)
def upper(a):return norm(a[0])+a[1]
def read(k):return [[int(v) for v in row] for row in f[k]],F(0)
Ms=[([[int(F(cols[k][i])*S) for k in range(n)] for i in range(n)],F(n,S)) for cols in j['multiplication_columns']];Q=(I,F(0));powers=[]
for M in Ms:
 M2=times(M,M);Q=plus(Q,M2);powers.append([(I,F(0)),M,M2,times(M2,M)])
N=(zero,F(0))
for ex,c in j['f0_terms']:
 v=(I,F(0))
 for i,k in enumerate(ex):
  if k:v=times(v,powers[i][k])
 N=plus(N,scalar(v,c))
Cq=read('approximate_Q_inverse_integer');rq=upper(plus((I,F(0)),times(Cq,Q),-1));assert rq<1
Z=read('approximate_L_integer');eL=norm(Cq[0])/(1-rq)*upper(plus(times(Q,Z),scalar(N,F(1,4)),-1))
l,u=map(F,f['root_interval']);mid=F(f['midpoint']);assert l<mid<u
A=[list(t) for t in zip(*Z[0])]
for i in range(n):A[i][i]-=int(mid*S)
A[0]=[S]+[0]*(n-1);Aball=A,n*eL+max(mid-l,u-mid)+F(1,S)
Ca=read('approximate_A_inverse_integer');ra=upper(plus((I,F(0)),times(Ca,Aball),-1));assert ra<1
w=[F(row[0],S) for row in Ca[0]];ew=ra/(1-ra)*max(map(abs,w));author=json.loads((r/'left_interval_certificate.json').read_text())
assert rq==F(author['Q_inverse_residual_bound']);assert eL==F(author['L_infinity_error_bound']);assert ra==F(author['A_inverse_residual_bound']);assert ew==F(author['evaluation_vector_infinity_error_bound'])
fq=json.loads((r/'left_feasible_certificate.json').read_text());q=list(map(F,fq['rational_unit_quaternion']));assert sum(v*v for v in q)==1
inp=json.loads((src/'received/input.json').read_text());val=sum(F(c)*math.prod(v**e for v,e in zip(q,ex)) for ex,c in zip(inp['exponents'],inp['original']));bias=sum(abs(F(a)-F(b)) for a,b in zip(inp['original'],inp['perturbed']));assert val==F(fq['exact_original_upper']);assert l-bias==F(fq['exact_original_lower']);assert val-l+bias==F(fq['exact_gap'])<F(inp['target_gap'])
res={'independent_list_integer_ball_arithmetic':True,'all_four_bounds_match_exactly':True,'evaluation_error':str(ew),'evaluation_error_float':float(ew),'candidate_unit_norm_exact':True,'candidate_objective_exact':True,'gap_float':float(val-l+bias),'seconds':time.time()-st};(o/'independent_checks.json').write_text(json.dumps(res,indent=2)+'\n');print({k:v for k,v in res.items() if k!='evaluation_error'})
