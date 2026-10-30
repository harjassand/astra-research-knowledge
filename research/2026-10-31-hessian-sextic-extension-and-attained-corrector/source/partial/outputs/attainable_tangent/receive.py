"""Attainable fourth-order variational reduction and exact Fourier compiler.

Every corrector is constructed as a genuine gradient by a Poisson right
inverse. The universal theorem is analytic in PROOF.txt; this receiver
checks the universal scalar Taylor identity and exact compatible controls.
No optimizer, angular sample, free law, or work/ module is imported.
"""
from pathlib import Path
from fractions import Fraction as R
from functools import lru_cache
import importlib.util,json,time,sys
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tangent_square_source',HERE.parent/'square_completion/receive.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
b=s.b;add,mul,scale,diff=b.add,b.mul,b.scale,b.diff
cert=json.loads((HERE.parent/'square_completion/certificate.json').read_text());pco=list(map(R,cert['zeta_minimal_polynomial_monic']));s.zh=-pco[1];s.zk=-pco[2];Q=s.Q;Z=Q(0,1);alpha=R(cert['eta_equals_alpha_zeta']);ell=[Q(1),alpha*Z,Q(0),Z];LM=[[ell[0],ell[1]],[ell[2],ell[3]]];dell=ell[0]*ell[3]-ell[1]*ell[2];assert dell
Linvt=[[ell[3]/dell,-ell[2]/dell],[-ell[1]/dell,ell[0]/dell]];J=[[R(0),R(-1)],[R(1),R(0)]];T=[[sum(Linvt[i][k]*J[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def val(P,x):return b.evaluate(P,x)
def literal(q):return Q(q).literal()
def constant(n,v):return {(0,)*n:Q(v)} if v else {}
def linear(v):
 out={}
 for i,q in enumerate(v):
  if q:pw=[0]*len(v);pw[i]=1;out[tuple(pw)]=q
 return out
A=[b.var(4,i) for i in range(4)];L=linear(ell);detA=add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1));base=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text());kk=list(map(R,base['ray']['K_coefficients']));X=add(mul(A[0],A[0]),mul(A[2],A[2]),scale(mul(A[1],A[1]),-1),scale(mul(A[3],A[3]),-1));Y=scale(add(mul(A[0],A[1]),mul(A[2],A[3])),2);D=scale(detA,2);forms=[mul(X,X),scale(mul(X,Y),2),scale(mul(X,D),2),mul(Y,Y),scale(mul(Y,D),2),mul(D,D)];F=add(*(scale(p,q) for p,q in zip(forms,kk)));HF=[[diff(diff(F,i),j) for j in range(4)] for i in range(4)]
def root_interval(steps):
 lo,hi=R(-2,3),R(-33,50)
 for _ in range(steps):
  mid=(lo+hi)/2;pp=mid*mid-s.zh*mid-s.zk
  if pp>0:lo=mid
  else:hi=mid
 return lo,hi
def bounds(q,steps=0):
 q=Q(q);lo,hi=root_interval(steps);a=q.a+q.c*lo;c=q.a+q.c*hi;return min(a,c),max(a,c)
def sign(q):
 q=Q(q)
 if not q:return 0
 for steps in range(0,513,8):
  lo,hi=bounds(q,steps)
  if lo>0:return 1
  if hi<0:return -1
 raise AssertionError('A nonzero quadratic-field sign was not isolated.')
def solve(A,B):
 rows=[[Q(v) for v in row]+[Q(v) for v in bb] for row,bb in zip(A,B)];n=len(A);m=len(B[0])
 for j in range(n):
  k=next(i for i in range(j,n) if rows[i][j]);rows[j],rows[k]=rows[k],rows[j];v=rows[j][j];rows[j]=[q/v for q in rows[j]]
  for i in range(n):
   if i!=j and rows[i][j]:v=rows[i][j];rows[i]=[a-v*c for a,c in zip(rows[i],rows[j])]
 out=[row[n:] for row in rows];assert all(sum(Q(a)*out[k][j] for k,a in enumerate(row))==B[i][j] for i,row in enumerate(A) for j in range(m));return out
def mean(P):return Q(P.get((0,0),Q(0)))
def expectation(poly,field):
 @lru_cache(maxsize=None)
 def mon(pw):
  if not any(pw):return constant(2,1)
  j=next(i for i,p in enumerate(pw) if p);prev=list(pw);prev[j]-=1;return mul(mon(tuple(prev)),field[j])
 return sum((co*mean(mon(tuple(pw))) for pw,co in poly.items()),Q(0))
def field_dot(v,G):return add(*(scale(P,q) for P,q in zip(G,v)))
def field_det(G):return add(mul(G[0],G[3]),scale(mul(G[1],G[2]),-1))
def cofactor_dot(M,G):return field_dot([M[3],-M[2],-M[1],M[0]],G)
def cosine_field(rays):
 G=[{} for _ in range(4)]
 for k,Rv in rays:
  for i,q in enumerate(Rv):
   if q:G[i]=add(G[i],{tuple(k):q/2,tuple(-v for v in k):q/2})
 return G
def check_compatible(G):
 assert all(not mean(P) for P in G)
 for k in {key for P in G for key in P}:
  assert k!=(0,0)
  for i in (0,2):assert G[i].get(k,Q(0))*k[1]-G[i+1].get(k,Q(0))*k[0]==0
def build(Cfactor,nu,M,G0):
 nu=R(nu);assert nu>0;M=list(map(Q,M));mc=list(map(Q,Cfactor[:4]));lam=Q(Cfactor[4]);C=add(mul(mul(L,L),linear(mc)),scale(mul(detA,L),lam));p=add(F,C,scale(mul(L,L),nu));check_compatible(G0);assert not field_dot(ell,G0);assert not mean(field_det(G0))
 psi=add(scale(field_dot(mc,G0),2*sum(a*c for a,c in zip(ell,M))),scale(add(cofactor_dot(M,G0),field_det(G0)),lam));assert not mean(psi);zz=scale(psi,-R(1,2)/nu);H=[{} for _ in range(4)]
 for k,q in zz.items():
  assert k!=(0,0);knorm=k[0]**2+k[1]**2;out=[sum(Linvt[i][j]*k[j] for j in range(2)) for i in range(2)]
  for i in range(2):
   for j in range(2):H[2*i+j][k]=q*out[i]*k[j]/knorm
 check_compatible(H);assert field_dot(ell,H)==zz
 FF=[add(P,constant(2,q)) for P,q in zip(G0,M)];deltaF=expectation(F,FF)-val(F,M);target=deltaF-mean(mul(psi,psi))/(4*nu)
 # Full exact polynomial in epsilon for the actual potential epsilon*phi0
 # plus epsilon^2*phiH and affine mean epsilon*M.
 field=[]
 for i in range(4):
  P={(k[0],k[1],1):v for k,v in G0[i].items()};P=add(P,{(0,0,1):M[i]} if M[i] else {},{(k[0],k[1],2):v for k,v in H[i].items()});field.append(P)
 @lru_cache(maxsize=None)
 def mon(pw):
  if not any(pw):return {(0,0,0):Q(1)}
  j=next(i for i,q in enumerate(pw) if q);prev=list(pw);prev[j]-=1;return mul(mon(tuple(prev)),field[j])
 ee={}
 for pw,co in p.items():
  for (kx,ky,ep),q in mon(tuple(pw)).items():
   if kx==ky==0:ee[ep]=ee.get(ep,Q(0))+co*q
  ep=sum(pw);ee[ep]=ee.get(ep,Q(0))-co*__import__('math').prod(q**j for q,j in zip(M,pw))
 ee={j:q for j,q in ee.items() if q};assert all(j>=4 for j in ee) and ee.get(4,Q(0))==target
 return {'G0':G0,'corrector':H,'mean':M,'p':p,'energy_coefficients':ee,'attained_fourth_order_energy':target,'corrector_square_completed_exactly':True,'corrector_modes':len({k for P in H for k in P})//2}
def universal_scalar_identity():
 # Formal scalar variables: epsilon,L(M),L(H),m(M),m(G),m(H),
 # det(M),cof(M):G,det(G),cof(M):H,cof(G):H,det(H),lambda.
 v=[b.var(13,i) for i in range(13)];ep,ll,z,mm,mg,mh,dm,dmg,dg,dmh,dgh,dh,lam=v
 le=add(mul(ep,ll),mul(mul(ep,ep),z));me=add(mul(ep,add(mm,mg)),mul(mul(ep,ep),mh));de=add(mul(mul(ep,ep),add(dm,dmg,dg)),mul(mul(mul(ep,ep),ep),add(dmh,dgh)),mul(mul(mul(ep,ep),mul(ep,ep)),dh));ce=add(mul(mul(le,le),me),mul(lam,mul(de,le)))
 def coefficient(P,j):return {pw[1:]:co for pw,co in P.items() if pw[0]==j}
 target4=add(mul(z,add(scale(mul(ll,mg),2),mul(lam,add(dmg,dg)))),mul(lam,mul(ll,dgh)),mul(add(scale(mul(ll,mm),2),mul(lam,dm)),z),mul(mul(ll,ll),mh),mul(lam,mul(ll,dmh)))
 assert coefficient(ce,4)=={pw[1:]:co for pw,co in target4.items()}
 return True
def main():
 start=time.perf_counter();assert universal_scalar_identity();factors=[[Q(*q) for q in row] for row in cert['factored_cubic_basis']]
 # Positive actual control, with the previously proved QC coefficient.
 rays=[]
 for k,amp in (((1,0),R(1)),((0,1),R(2,3)),((1,1),R(1,4))):
  out=[sum(T[i][j]*k[j] for j in range(2)) for i in range(2)];rays.append((k,[amp*out[i]*k[j] for i in range(2) for j in range(2)]))
 positive=build([a+c for a,c in zip(*factors)],2**94,[R(1),R(-1,2),R(2,3),R(1,4)],cosine_field(rays));assert sign(positive['attained_fourth_order_energy'])>0
 # Decisive negative control: its input polynomial is explicitly NOT ROC.
 tt=R(-385371,10**6);xi=[R(1),tt];u=[-Z*tt,Q(1)+alpha*Z*tt];Rv=[u[i]*xi[j] for i in range(2) for j in range(2)];HH=[[val(P,Rv) for P in row] for row in HF];M=[row[0] for row in solve(HH,[[q] for q in ell])];negative=build(factors[0],1,M,cosine_field([((10**6,-385371),Rv)]));c4=negative['attained_fourth_order_energy'];assert sign(c4)<0
 for steps in range(0,513,8):
  _,ub=bounds(c4,steps)
  if ub<0:delta=-ub;break
 else:raise AssertionError
 higher=sum((q.upper() for k,q in negative['energy_coefficients'].items() if k>4),R(0));eps=min(R(1),delta/(2*higher)) if higher else R(1);energy=sum((q*eps**j for j,q in negative['energy_coefficients'].items()),Q(0));assert sign(energy)<0
 H=negative['corrector'];k=(10**6,-385371);ampH=[2*P.get(k,Q(0)) for P in H];direction=[a+eps*c for a,c in zip(Rv,ampH)];meanpt=[eps*q for q in M];hp=[[val(diff(diff(negative['p'],i),j),meanpt) for j in range(4)] for i in range(4)];score=sum((direction[i]*hp[i][j]*direction[j] for i in range(4) for j in range(4)),Q(0));assert direction[0]*direction[3]-direction[1]*direction[2]==0 and sign(score)<0
 output={'universal_scalar_Taylor_identity':True,'actual_corrector_is_constructed_by_Poisson_right_inverse':True,'exact_square_completion_coefficient_verified':True,'positive_control':{'known_QC_input':True,'constraint_modes':3,'corrector_modes':positive['corrector_modes'],'fourth_order_energy':literal(positive['attained_fourth_order_energy']),'energy_coefficients':{str(j):literal(q) for j,q in sorted(positive['energy_coefficients'].items())}},'negative_control':{'global_ROC_input':False,'strict_actual_energy_negative':True,'explicit_rank_one_Hessian_score_negative':True,'epsilon':str(eps),'energy':literal(energy),'fourth_order_energy':literal(c4),'rank_one_Hessian_score':literal(score),'energy_coefficients':{str(j):literal(q) for j,q in sorted(negative['energy_coefficients'].items())}},'genuine_ROC_QC_separation':'NOT_ACHIEVED','seconds':time.perf_counter()-start,'scope':'Universal attained smooth-corrector variational principle in PROOF.txt. Exact compatible Fourier controls validate the executable compiler. The negative control deliberately fails ROC and is not a counterexample.'}
 (HERE/'replay.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('positive_control','negative_control')},indent=2))
if __name__=='__main__':main()
