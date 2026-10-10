"""Exploratory double-precision multiscale normal form. NOT CERTIFIED.

This implements the same jet recurrence as prototype_multiscale.py with NumPy.
It uses approximate roots, heuristic Taylor/residual indicators and floating
projectors. It is a mechanism experiment, not the theorem's interval algorithm.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

I=np.eye(3,dtype=complex)
def z():return np.zeros((3,3),dtype=complex)
def dag(A):return A.conj().T
def herm(A):return (A+dag(A))/2
def norm(A):return np.linalg.norm(A)
def ev(A,x):
 V=A[-1].copy()
 for a in A[-2::-1]:V=V*x+a
 return V
def conv(A,B,L):
 out=[]
 for r in range(L+1):
  out.append(sum((A[k]@B[r-k] for k in range(max(0,r-len(B)+1),min(r,len(A)-1)+1)),np.zeros((A[0].shape[0],B[0].shape[1]),complex)))
 return out
def ode(G,L):
 C=[np.eye(G[0].shape[0],dtype=complex)]
 for r in range(L):C.append(sum((G[k]@C[r-k] for k in range(min(r,len(G)-1)+1)),np.zeros_like(C[0]))/(r+1))
 return C
def invjet(A,L):
 C=[np.linalg.inv(A[0])]
 for r in range(1,L+1):C.append(-C[0]@sum((A[k]@C[r-k] for k in range(1,min(r,len(A)-1)+1)),z()))
 return C
D2=np.diag([1.,0.,-1.]);D1=np.diag([0.,1/3,-1/3]);D0=np.array([[-1.,1.,1/3],[1.,0.,2.],[1/3,2.,1.]])
def base(c,h,k,L):return [h*k*(c*c*D2+c*D1+D0),h*h*k*(2*c*D2+D1),h**3*k*D2]+[z() for _ in range(max(0,L-2))]
def groupsfor(A,gap,count):
 vals=np.linalg.eigvalsh(A);count['eigensystems']+=1;g=[[0]]
 for j in (1,2):
  if vals[j]-vals[j-1]<gap:g[-1].append(j)
  else:g.append([j])
 return g

def projectors(A,groups,L,count):
 vals,Q=np.linalg.eigh(herm(A[0]));count['eigensystems']+=1;Qh=dag(Q)
 AJ=[Qh@a@Q for a in A[:L+1]]+[z() for _ in range(max(0,L+1-len(A)))];out=[]
 for group in groups:
  inside=set(group);P=[np.diag([int(i in inside) for i in range(3)]).astype(complex)]
  for r in range(1,L+1):
   S=sum((P[k]@P[r-k] for k in range(1,r)),z())
   R=-sum((AJ[k]@P[r-k]-P[r-k]@AJ[k] for k in range(1,r+1)),z());X=z()
   for i in range(3):
    for j in range(3):
     if (i in inside)==(j in inside):X[i,j]=(-1 if i in inside else 1)*S[i,j]
     else:X[i,j]=R[i,j]/(vals[i]-vals[j])
   P.append(herm(X));count['projector_jet_orders']+=1
  out.append([Q@X@Qh for X in P])
 return out

def connection(P,L):return [herm(1j*sum(((k+1)*pj[k+1]@pj[r-k] for pj in P for k in range(r+1)),z())) for r in range(L+1)]
def panel(c,h,k,L,N,groups,count):
 full=L+N+2;A=base(c,h,k,full)
 if len(groups)==1:
  C=ode([-1j*a for a in A[:3]],L)
  meta={'groups':[3],'N':0}
  if count.get('_capture_polynomials'):meta['_polys']=[C];meta['_phases']=[[0.]]
  return ev(C,1)@dag(ev(C,-1)),sum(norm(a) for a in C[-5:]),0.,meta
 H=A;prev=None;originalP=None
 for j in range(N+1):
  order=full-j;P=projectors(H,groups,order,count)
  if j==0:originalP=P
  K=connection(P,order-1)
  if j==N:break
  prev=K;H=[A[r]-K[r] for r in range(len(K))]
 count['normal_form_stages']+=N+1
 delta=K if prev is None else [K[r]-prev[r] for r in range(len(K))]
 res=sum(norm(x) for x in delta[:L+1])
 W=ode([-1j*x for x in K[:L]],L);Wi=invjet(W,L);B=conv(conv(Wi,H,L),W,L)
 vals,S=np.linalg.eigh(herm(H[0]));count['eigensystems']+=1;Sh=dag(S);B=[Sh@x@S for x in B]
 phases=[];solutions=[]
 for a,group in enumerate(groups):
  size=len(group);chi=[]
  for r in range(L):chi.append(np.trace(sum((A[j]@originalP[a][r-j] for j in range(r+1)),z()))/size)
  G=[-1j*(B[r][np.ix_(group,group)]-chi[r]*np.eye(size)) for r in range(L)]
  phases.append(chi);solutions.append(ode(G,L))
 def endpoint(sign):
  D=z()
  for group,V,chi in zip(groups,solutions,phases):
   phase=sum(x*float(sign)**(r+1)/(r+1) for r,x in enumerate(chi))
   D[np.ix_(group,group)]=np.exp(-1j*phase)*ev(V,sign)
  return ev(W,sign)@S@D@Sh
 V=endpoint(1)@dag(endpoint(-1))
 tail=sum(norm(x) for x in W[-5:])+sum(sum(norm(x) for x in v[-5:]) for v in solutions)+sum(sum(abs(x)/(L-4+j) for j,x in enumerate(C[-5:])) for C in phases)
 meta={'groups':[len(g) for g in groups],'N':N}
 if count.get('_capture_polynomials'):
  polynomials=[]
  for group,solution in zip(groups,solutions):
   embed=[]
   for coeff in solution:
    e=z();e[np.ix_(group,group)]=coeff;embed.append(S@e@Sh)
   polynomials.append(conv(W,embed,2*L))
  meta['_polys']=polynomials;meta['_phases']=[[0.]+[float(np.real(x))/(r+1) for r,x in enumerate(chi)] for chi in phases]
 return V,tail,res,meta

def run(B,f,s,seconds,L=26,N=3,gap=8.,fraction=.12,acquired_roots=None):
 begin=time.perf_counter();deadline=begin+seconds;end=2.**(B-1);k=2.**f;tol=2.**(-s)
 if acquired_roots is None:
  rootdata=json.loads(Path(__file__).with_name('three_channel_scaling_results.json').read_text())
  roots=[complex(str(x).replace('*I','j').replace(' ','')) for x in rootdata['complex_discriminant_roots_approximate']]
 else:roots=acquired_roots
 count={'eigensystems':0,'projector_jet_orders':0,'normal_form_stages':0,'panels':0,'rejected_panels':0,'geometry_bisections':0}
 records=[];stack=[(-end,end)];U=I.copy();status='complete_uncertified';reason=None
 while stack:
  if time.perf_counter()>deadline:status='censored';reason='native solver row budget exceeded';break
  a,b=stack.pop();c=(a+b)/2;h=(b-a)/2
  if h>fraction*min(abs(c-r) for r in roots):stack.extend([(c,b),(a,c)]);count['geometry_bisections']+=1;continue
  A=base(c,h,k,2);groups=groupsfor(A[0],gap,count)
  V,tail,res,meta=panel(c,h,k,L,N,groups,count);indicator=tail+2*res
  if indicator>tol/2048 or not np.isfinite(indicator):
   count['rejected_panels']+=1
   if len(groups)>1 and norm(A[0])<12:V,tail,res,meta=panel(c,h,k,L,0,[[0,1,2]],count);indicator=tail
   if indicator>tol/2048 or not np.isfinite(indicator):stack.extend([(c,b),(a,c)]);continue
  U=V@U;count['panels']+=1;records.append({'a':a,'b':b,'indicator_uncertified':float(indicator),**meta})
  if count['panels']>1800:status='censored';reason='prototype panel-count budget exceeded';break
 result={'B':B,'f':f,'s':s,'L':L,'N':N,'gap_threshold':gap,'geometry_fraction':fraction,'certified':False,'scope':'exploratory double-precision mechanism test','status':status,'reason':reason,'seconds':time.perf_counter()-begin,'counters':count,'panels':records,'claimed_operation_error_bound':None}
 if status=='complete_uncertified':result.update(endpoint=[[[float(x.real),float(x.imag)] for x in row] for row in U],unitarity_defect_frobenius=float(norm(dag(U)@U-I)))
 return result,U

def reference(B,f,rtol=2e-12):
 end=2.**(B-1);k=2.**f;count=0
 def rhs(u,y):return (-1j*k*(u*u*D2+u*D1+D0)@y.reshape(3,3)).ravel()
 start=time.perf_counter();sol=solve_ivp(rhs,(-end,end),I.ravel(),method='DOP853',rtol=rtol,atol=rtol/100)
 return sol.y[:,-1].reshape(3,3),{'method':'SciPy DOP853 (uncertified diagnostic reference)','rhs_calls':sol.nfev,'seconds':time.perf_counter()-start,'rtol':rtol,'success':sol.success}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--B',type=int,default=4);ap.add_argument('--f',type=int,default=0);ap.add_argument('--s',type=int,default=20);ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--L',type=int,default=26);ap.add_argument('--N',type=int,default=3);ap.add_argument('--gap',type=float,default=8.);ap.add_argument('--reference',action='store_true');ap.add_argument('--tag',default='')
 a=ap.parse_args();r,U=run(a.B,a.f,a.s,a.seconds,a.L,a.N,a.gap)
 if a.reference and r['status']=='complete_uncertified':
  V,ref=reference(a.B,a.f);r.update(reference=ref,observed_operator_disagreement=float(np.linalg.norm(U-V,2)))
 path=Path(__file__).with_name(f'numpy_B{a.B}_f{a.f}_s{a.s}{a.tag}.json');path.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k not in ('panels','endpoint')},indent=2))
