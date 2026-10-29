import sys; sys.set_int_max_str_digits(0)
import itertools,math,json,numpy as np
from fractions import Fraction as F
from pathlib import Path
PTH=Path(__file__).parent

def wedge_basis(d,k):
 sets=list(itertools.combinations(range(d),k));V=np.zeros((d**k,len(sets)),complex)
 for col,I in enumerate(sets):
  for p in itertools.permutations(range(k)):
   ix=sum(I[p[j]]*d**(k-1-j) for j in range(k));sg=(-1)**sum(p[i]>p[j] for i in range(k) for j in range(i+1,k));V[ix,col]=sg/math.sqrt(math.factorial(k))
 return sets,V
# Full dense CP success/failure reduction versus compressed subset formula.
cp_rows=[];r=4;p=np.array([1,2,3,4])/10
for k in [1,2,3]:
 old,V=wedge_basis(r,k);new,T=wedge_basis(r,k+1);Proj=T@T.conj().T;Q=np.eye(r**(k+1))-Proj;oi={a:i for i,a in enumerate(old)};ni={a:i for i,a in enumerate(new)};S=np.zeros((len(new),len(old)));Fail=np.zeros((len(old),len(old)))
 for J,jj in ni.items():
  for a in J:S[jj,oi[tuple(x for x in J if x!=a)]]+=p[a]/(k+1)
 for I,ii in oi.items():
  Fail[ii,ii]=1-2*(1-sum(p[a] for a in I))/(k+1)
  for j in range(r):
   if j not in I:Fail[ii]+=S[ni[tuple(sorted(I+(j,)))]]/(k+1)
 maxerr=0
 for i in range(len(old)):
  rho=np.kron(np.outer(V[:,i],V[:,i].conj()),np.diag(p));succ=T.conj().T@rho@T;failed=Q@rho@Q;red=np.trace(failed.reshape(r**k,r,r**k,r),axis1=1,axis2=3);compressed=V.conj().T@red@V
  maxerr=max(maxerr,np.linalg.norm(succ-np.diag(S[:,i])),np.linalg.norm(compressed-np.diag(Fail[:,i])))
 assert maxerr<1e-12;cp_rows.append({'r':r,'k':k,'max_dense_compressed_residual':float(maxerr)})
# Explicit actual LCU. Demonstrate that its naive failure instrument is NOT enough.
d=4;k=2;n=3;dim=d**n;perms=list(itertools.permutations(range(n)));m=len(perms)
selector=np.ones(m)/math.sqrt(m);e=np.eye(m)[:,0];v=e-selector;Prep=np.eye(m)-2*np.outer(v,v)/(v@v)
Select=np.zeros((m*dim,m*dim))
for j,pmt in enumerate(perms):
 for bits in itertools.product(range(d),repeat=n):
  ix=sum(bits[a]*d**(n-1-a) for a in range(n));dest=sum(bits[pmt[a]]*d**(n-1-a) for a in range(n));sg=(-1)**sum(pmt[a]>pmt[b] for a in range(n) for b in range(a+1,n));Select[j*dim+dest,j*dim+ix]=sg
U=np.kron(Prep,np.eye(dim))@Select@np.kron(Prep,np.eye(dim));E=np.kron(e[:,None],np.eye(dim));Q0=E@E.T
_,V=wedge_basis(d,k);_,T=wedge_basis(d,n);Pg=T@T.conj().T;oldP=np.kron(V@V.conj().T,np.eye(d));psi=np.kron(V[:,0],np.eye(d)[:,2]);naive=0
for j in range(1,m):naive+=np.linalg.norm((np.eye(dim)-oldP)@U[j*dim:(j+1)*dim,:dim]@psi)**2
Lfail=U.conj().T@(np.eye(m*dim)-Q0)@U@E;lferr=np.linalg.norm(Lfail-E@(np.eye(dim)-Pg));assert naive>.01 and lferr<1e-12
rng=np.random.default_rng(111318);z=rng.normal(size=(dim,5))+1j*rng.normal(size=(dim,5));z=oldP@z;z/=np.linalg.norm(z);failed=(np.eye(dim)-Pg)@z;failure_leak=np.linalg.norm((np.eye(dim)-oldP)@failed);assert failure_leak<1e-12
# Full-rank marginals alone are insufficient for growth.
d2=8;swap=np.zeros((d2*d2,d2*d2))
for i in range(d2):
 for j in range(d2):swap[i*d2+j,j*d2+i]=1
Panti=(np.eye(d2*d2)-swap)/2;rho=np.zeros_like(Panti)
for i in range(d2):rho[i*d2+i,i*d2+i]=1/d2
assert np.trace(Panti@rho)==0
# Independent geometric-stage distribution calculation for every finite bound.
j=json.loads((PTH/'replay/exact_birth_chain.json').read_text());rates=list(map(F,j['rates']));D=math.lcm(*(x.denominator for x in rates));weights=[int(x*D) for x in rates];verified=0
for programs in [1,2]:
 N=4096;mass=[1]+[0]*N
 for a in weights*programs:
  next=[0]*(N+1)
  for t in range(1,N+1):next[t]=(D-a)*next[t-1]+a*mass[t-1]
  mass=next
 for row in j['rows']:
  if row['programs']!=programs:continue
  t=row['source_call_cap'];num=0
  for a in mass[:t+1]:num=num*D+a
  assert F(num,D**t)==F(row['lower_probability']);verified+=1
assert sum(1/a for a in rates)==F(j['expected_calls_one_program_upper'])
out={'dense_compressed_checks':cp_rows,'naive_LCU_failure_old_block_leakage':float(naive),'correct_Luders_failure_operator_residual':float(lferr),'correlated_new_old_bath_failure_support_residual':float(failure_leak),'full_rank_correlated_marginals_growth_probability':0,'independent_exact_tail_rows':verified};(PTH/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
