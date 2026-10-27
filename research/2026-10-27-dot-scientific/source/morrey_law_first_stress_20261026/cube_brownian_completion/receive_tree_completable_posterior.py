"""Exact rational uniform neighborhood for a nondegenerate, tree-completable posterior diffusion."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,itertools,sympy as s
P=Path(__file__).resolve().parent;O=P/'same_law_AC';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();src=O/'local_posterior_feasibility_receipt.json';j=json.loads(src.read_text());Y=s.Matrix([list(map(s.Rational,r['point']))for r in j['rows']]).T;p0=s.Matrix([s.Rational(r['original_probability'])for r in j['rows']]);J=s.ones(3)-s.eye(3);G=Y.T*J*Y;qq=s.Matrix([[G[i,i]for i in range(8)]]);H0=-G;H1=s.zeros(8);H1[4,7]=H1[7,4]=1;H1[5,6]=H1[6,5]=-s.Rational(3,2);H1[5,7]=H1[7,5]=-s.Rational(1,2);linear=s.Matrix([[1,-1,0,0,0,0,0,0]]);C0=s.ones(1,8).col_join(linear).col_join(qq-2*p0.T*G).col_join(2*p0.T*H1);piv=C0.rref()[1];free=[i for i in range(8)if i not in piv];assert len(piv)==4;T0=s.zeros(8,4);top=-C0[:,piv].inv()*C0[:,free]
for i,row in enumerate(piv):T0[row,:]=top[i,:]
for i,row in enumerate(free):T0[row,i]=1
HH=[T0.T*H*T0 for H in[H0,H1]];gram=s.Matrix([[s.trace(a*b)for b in HH]for a in HH]);coef=gram.inv()*s.Matrix([s.trace(h)for h in HH]);K0=s.eye(4)-sum((coef[i]*HH[i]for i in range(2)),s.zeros(4));assert all(s.trace(h*K0)==0 for h in HH);R0=Y*T0;A0=R0*R0.T
assert all((K0-s.eye(4)/8)[:i,:i].det()>0 for i in range(1,5));assert all((A0-s.eye(3)/4)[:i,:i].det()>0 for i in range(1,4))
class V:
 def __init__(self,a,b=None):self.lo=Q(str(a));self.hi=self.lo if b is None else Q(str(b))
 def __add__(self,o):o=vv(o);return V(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return V(-self.hi,-self.lo)
 def __sub__(self,o):return self+-vv(o)
 def __rsub__(self,o):return vv(o)+-self
 def __mul__(self,o):o=vv(o);v=[a*b for a in[self.lo,self.hi]for b in[o.lo,o.hi]];return V(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,o):o=vv(o);assert not(o.lo<=0<=o.hi);return self*V(1/o.hi,1/o.lo)
 def absmax(self):return max(abs(self.lo),abs(self.hi))
def vv(x):return x if isinstance(x,V)else V(x)
def mat(M):return[[V(M[i,k])for k in range(M.cols)]for i in range(M.rows)]
def tr(A):return list(map(list,zip(*A)))
def mul(A,B):return[[sum((a*b for a,b in zip(row,col)),V(0))for col in tr(B)]for row in A]
def determinant(A):
 n=len(A);out=V(0)
 for perm in itertools.permutations(range(n)):
  sg=(-1)**sum(perm[i]>perm[k]for i in range(n)for k in range(i+1,n));v=V(sg)
  for i,k in enumerate(perm):v=v*A[i][k]
  out=out+v
 return out
def inv(A):
 n=len(A);d=determinant(A);assert not(d.lo<=0<=d.hi);return[[((-1)**(i+k))*determinant([[A[a][b]for b in range(n)if b!=i]for a in range(n)if a!=k])/d for k in range(n)]for i in range(n)]
def trace(A):return sum((A[i][i]for i in range(len(A))),V(0))
def maxerr(A,B):return max(sum((A[i][k]-V(B[i,k])).absmax()for k in range(len(A[0])))for i in range(len(A)))
YI=mat(Y);GI=mat(G);HIs=[mat(H0),mat(H1)];delta=Q(1,4096);attempts=0
while True:
 attempts+=1
 try:
  pp=[[V(Q(str(v))-delta,Q(str(v))+delta)]for v in p0];rootgrad=mul(tr(pp),GI)[0];rightgrad=mul(tr(pp),HIs[1])[0];C=[[V(1)for _ in range(8)],mat(linear)[0],[V(qq[i])-2*rootgrad[i]for i in range(8)],[2*v for v in rightgrad]];CP=[[row[i]for i in piv]for row in C];CF=[[row[i]for i in free]for row in C];top=mul(inv(CP),CF);T=[[V(0)for _ in range(4)]for _ in range(8)]
  for ii,row in enumerate(piv):T[row]=[-v for v in top[ii]]
  for ii,row in enumerate(free):T[row][ii]=V(1)
  hs=[mul(mul(tr(T),H),T)for H in HIs];gr=[[trace(mul(a,b))for b in hs]for a in hs];co=mul(inv(gr),[[trace(h)]for h in hs]);K=[[V(int(i==k))-sum((co[n][0]*hs[n][i][k]for n in range(2)),V(0))for k in range(4)]for i in range(4)];R=mul(YI,T);RR=mul(R,tr(R));ke=maxerr(K,K0);re=maxerr(RR,A0)
  assert ke<=Q(1,16)and re<=Q(1,8)and delta<=min(Q(str(v))for v in p0)/2
  break
 except AssertionError:delta/=2
assert attempts<40
out={'status':'UNIFORM_TREE_COMPLETABLE_POSTERIOR_DIFFUSION_PENDING_AUDIT','source_interface_sha256':sha(src),'probability_center':list(map(str,p0)),'constraints':['sum p=1','p0-p1=0','sum_i p_i q(Y_i)-q(sum_i p_iY_i)=0','2p4p7-3p5p6-p5p7=0'],'pivot_probability_columns':list(piv),'free_probability_columns':free,'tangent_at_center':[[str(T0[i,k])for k in range(4)]for i in range(8)],'rational_tangent_covariance_at_center':[[str(K0[i,k])for k in range(4)]for i in range(4)],'uniform_probability_neighborhood_infinity_radius':str(delta),'stopping_neighborhood_radius':str(delta/2),'deterministic_interval_backtracking_attempts':attempts,'K_difference_operator_upper':str(ke),'RRt_difference_operator_upper':str(re),'uniform_tangent_covariance_Loewner_lower':'1/16','uniform_mean_RRt_Loewner_lower':'1/8','uniform_mean_covariance_Loewner_lower':'1/128','posterior_lower_bound':'each p_i>=p_i(original)/2','script_sha256':sha(Path(__file__)),'proof_note':'TREE_COMPLETABLE_POSTERIOR.md','scope':'Uniform rational neighborhood where a stopped continuous posterior martingale has nondegenerate null mean covariance and every stopped posterior has an explicit original-tree null completion to the SAME eight helper outcomes. Completion/source-law preservation and positive AC occupation follow from the analytic note. No quantitative occupation-overlap/N gain is yet received.'};(O/'tree_completable_posterior_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('delta',delta,'attempts',attempts,'Kerr',float(ke),'RRerr',float(re))
