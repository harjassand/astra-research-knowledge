"""Small exact-matrix checks and a large Majorana matrix diagnostic.
This is not a synthesized Gaussian circuit or a complete simulator backend.
"""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(610312)
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);Y=np.array([[0.,-1j],[1j,0.]]);Z=np.diag([1.,-1.])
def pauli(N,terms):
 a=np.array([[1.]])
 for j in reversed(range(N)):a=np.kron(a,terms.get(j,I))
 return a

def coefficients(q):
 n=len(q)+1;N=n+1;fields=np.zeros(N);xx=np.zeros(N-1);yy=np.zeros(N-1)
 if n==1:xx[0]=-.5
 else:
  for site,edge in [(1,0),(n-1,n-2)]:fields[site]-=.5*(q[edge]-1)/(q[edge]+1)
  xx[0]-=np.sqrt(q[0])/(q[0]+1);xx[n-1]-=np.sqrt(q[-1])/(q[-1]+1)
  for j in range(1,n-1):
   l,r=q[j-1],q[j];tp=(l*r-1)/(l*r+1);tm=(l-r)/(l+r)
   fields[j]-=(tp+tm)/4;fields[j+1]-=(tp-tm)/4
   sp=2*np.sqrt(l*r)/(1+l*r);sm=2*np.sqrt(l*r)/(l+r)
   xx[j]-=(sp+sm)/4;yy[j]+=(sp-sm)/4
 A=np.zeros((2*N,2*N))
 def add(i,j,v):A[i,j]+=v;A[j,i]-=v
 for j,f in enumerate(fields):add(2*j,2*j+1,-2*f)
 for j,c in enumerate(xx):add(2*j+1,2*j+2,-2*c)
 for j,c in enumerate(yy):add(2*j,2*j+3,2*c)
 return n/2,fields,xx,yy,A
rows=[]
for n in [1,2,3,4,5,6]:
 q=np.array([21/20 if rng.integers(2) else 20/21 for _ in range(n-1)])
 const,fields,xx,yy,A=coefficients(q);N=n+1;d=1<<n
 Ha=const*np.eye(1<<N,dtype=complex)
 for j,f in enumerate(fields):Ha+=f*pauli(N,{j:Z})
 for j,c in enumerate(xx):Ha+=c*pauli(N,{j:X,j+1:X})
 for j,c in enumerate(yy):Ha+=c*pauli(N,{j:Y,j+1:Y})
 w=np.ones(d)
 for x in range(d):
  for j in range(n-1):
   if ((x>>j)&1)==((x>>(j+1))&1):w[x]*=q[j]
 pi=w/w.sum();Hs=np.zeros((d,d))
 for i in range(n):
  for x in range(d):
   if (x>>i)&1:continue
   y=x^(1<<i);v=np.zeros(d);v[x]=np.sqrt(pi[y]/(pi[x]+pi[y]));v[y]=-np.sqrt(pi[x]/(pi[x]+pi[y]));Hs+=np.outer(v,v)
 C=np.zeros((d,d))
 for z in range(d):
  bit=0;x=0
  for j in range(n):bit^=(z>>j)&1;x|=bit<<j
  C[x,z]=1
 plus=np.array([1.,1.])/np.sqrt(2);Emb=np.kron(plus[:,None],np.eye(d))
 residual=float(np.linalg.norm(Emb.conj().T@Ha@Emb-C.T@Hs@C))
 omega=np.linalg.eigvalsh(1j*A)[N:];omega[np.abs(omega)<1e-12]=0
 predicted=const-omega.sum()/2+np.array([sum(omega[j] for j in range(N) if (z>>j)&1) for z in range(1<<N)])
 specres=float(np.max(np.abs(np.sort(predicted)-np.linalg.eigvalsh(Ha))))
 assert residual<1e-11 and specres<1e-11
 assert sum(abs(omega)<1e-10)==1
 rows.append({'n':n,'restricted_parent_residual':residual,'quadratic_spectrum_residual':specres,'minimum_positive_frequency':float(min(omega[omega>1e-10]))})
 print(json.dumps(rows[-1]),flush=True)
q=np.array([21/20 if rng.integers(2) else 20/21 for _ in range(127)])
const,f,x,y,A=coefficients(q);omega=np.linalg.eigvalsh(1j*A)[129:]
large={'n':128,'Majorana_matrix_dimension':258,'near_zero_frequencies':int(sum(abs(omega)<1e-10)),'minimum_positive_frequency':float(min(omega[omega>1e-10])),'ground_offset_residual':float(abs(const-omega.sum()/2)),'scope':'No 2^128 table; numerical frequencies are not a certified spectral gap'}
result={'scope':'Quadratic-source-kernel diagnostics only; no new mechanism/whole implementation claim','small':rows,'large':large}
Path(__file__).with_name('glauber_quadratic_kernel_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(large))
