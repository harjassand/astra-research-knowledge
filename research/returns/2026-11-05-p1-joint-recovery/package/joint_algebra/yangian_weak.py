from pathlib import Path
ROOT = str(Path(__file__).resolve().parent) + "/"
import numpy as np, itertools, math,json,sys
from singlet_singular import basis
from scipy.linalg import eigh
p=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def local(n,i,a):
 r=np.ones((1,1))
 for j in range(n):r=np.kron(r,p[a if i==j else 0])
 return r

def weak(n):
 B=basis(n); d=2**n;sites=[[local(n,i,a) for a in range(1,4)] for i in range(n)]
 pairs=list(itertools.combinations(range(n),2));Q=[np.zeros((d,d),complex) for _ in range(3)]
 for i,j in pairs:
  for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]:Q[a]+=sites[i][b]@sites[j][c]-sites[i][c]@sites[j][b]
 H=np.zeros((len(B),len(B)),complex)
 for q in Q:
  C=q@B-B@q
  H+=np.einsum('ijk,ljk->il',C.conj(),C,optimize=True)/16
 vals,vs=eigh(H)
 low=np.einsum('i,ijk->jk',vs[:,1],B)
 pairbasis=np.array([sum(sites[i][a]@sites[j][a] for a in range(3))/math.sqrt(3*d) for i,j in pairs])
 coeffs=np.einsum('ijk,jk->i',pairbasis.conj(),low)
 rec=dict(n=n,leading_gap=float(vals[1]),pair_fraction=float(np.sum(abs(coeffs)**2)),pair_coefficients=[[i+1,j+1,float(co.real),float(co.imag)] for (i,j),co in zip(pairs,coeffs)])
 Hp=np.zeros((len(pairs),len(pairs)),complex)
 for q in Q:
  C=q@pairbasis-pairbasis@q
  Hp+=np.einsum('ijk,ljk->il',C.conj(),C,optimize=True)/16
 rec['pair_gap']=float(eigh(Hp,eigvals_only=True)[0]);rec['leading_eigenvalues']=[float(v) for v in vals[:min(len(vals),15)]]
 np.savez(ROOT+'weak_n'+str(n)+'.npz',H=H,Hp=Hp,eigs=vals,vs=vs)
 print(json.dumps(rec),flush=True)
if __name__=='__main__':
 for n in range(2,int(sys.argv[1])+1):weak(n)
