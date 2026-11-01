"""Exact identities and finite-cutoff diagnostics for ordinary coherent eraser.
Cavity numerical cutoff results are DIAGNOSTICS, not certified infinite-mode bounds.
"""
import numpy as np,sympy as s,json
from scipy.sparse import csr_matrix,kron,eye
from scipy.sparse.linalg import expm_multiply
from pathlib import Path

def coh_f(b,kappa,T,zeta=1):
 p=kappa*(1+1j)/2
 return np.exp(-8*b*b*(1-zeta)*T+4*zeta*b*b/p*(-3+4*np.exp(-p*T)-np.exp(-2*p*T)))

def finite_source_f(lam,b,kext,kint,T,nc=10,eta=1,chi=None):
 kappa=kext+kint
 if chi is None:chi=kappa/2
 c=np.sqrt(lam)*b
 sm=csr_matrix(np.array([[0,1],[0,0]],complex));X=sm+sm.T
 a=csr_matrix(np.diag(np.sqrt(np.arange(1,nc)),1));sop=kron(sm,eye(nc,format='csr'));cav=kron(eye(2,format='csr'),a);n=cav.conj().T@cav
 sourceH=kron(c*X,eye(nc,format='csr'))
 Ls=np.sqrt(lam)*sop;Lc=np.sqrt(kext)*cav
 Hcas=(Lc.conj().T@(np.sqrt(eta)*Ls)-(np.sqrt(eta)*Ls).conj().T@Lc)/(2j)
 Hp=sourceH+chi*n+Hcas;Hm=-sourceH-chi*n+Hcas
 Llist=[np.sqrt(eta)*Ls+Lc]
 if eta<1:Llist.append(np.sqrt(1-eta)*Ls)
 if kint:Llist.append(np.sqrt(kint)*cav)
 d=2*nc;Id=eye(d,format='csr')
 G=-1j*(kron(Id,Hp)-kron(Hm.T,Id))
 for L in Llist:
  LL=L.conj().T@L;G+=kron(L.conj(),L)-.5*kron(Id,LL)-.5*kron(LL.T,Id)
 v=np.zeros(d*d,complex);v[0]=1
 x=expm_multiply(T*G,v).reshape((d,d),order='F')
 return np.trace(x)

def bound(lam,b,T):
 E=(4*b*b+32*b**4*T)/lam
 return 2*(np.sqrt(2*E)+2*abs(b)/np.sqrt(lam)+16*abs(b)**3*np.sqrt(T)/lam)

def main():
 # Exact source determinant and covariance algebra.
 p,y,c,l=s.symbols('p y c l',real=True)
 D=p-p*p-y*y/4
 pd=-l*p-c*y;yd=4*c*p-2*c-l*y/2
 assert s.expand(s.diff(D,p)*pd+s.diff(D,y)*yd-l*(p*p-D))==0
 # Exact coherent amplitude ODE -> logarithmic coherence derivative.
 t,k,b=s.symbols('t k b',positive=True,real=True)
 pc=k*(1+s.I)/2
 ap=2*b*(1+s.I)/s.sqrt(k)*(1-s.exp(-pc*t))
 logf=4*b*b/pc*(-3+4*s.exp(-pc*t)-s.exp(-2*pc*t))
 assert s.simplify(s.diff(logf,t)-(-8*b*b-s.I*k*ap*ap))==0
 assert s.simplify(logf.subs(t,0))==0
 # Finite-cutoff diagnostics across rate, loss, and time; source always remains on.
 rows=[]
 for lam,b,kext,kint,T,eta in [(64,.2,2,0,1,1),(256,.2,2,0,1,1),(1024,.2,2,0,1,1),(256,.2,8,0,2,1),(256,.2,8,.2,2,.98),(1024,.2,8,0,4,1)]:
  f8=finite_source_f(lam,b,kext,kint,T,8,eta)
  f12=finite_source_f(lam,b,kext,kint,T,12,eta)
  fc=coh_f(b,kext+kint,T,eta*kext/(kext+kint));e=bound(lam,b,T)
  assert abs(f8-f12)<1e-7
  assert abs(f12-fc)<=e
  rows.append(dict(lam=lam,b=b,kext=kext,kint=kint,T=T,eta=eta,coherent_comparator=[fc.real,fc.imag],finite_source_cutoff12=[f12.real,f12.imag],cutoff_difference=abs(f8-f12),actual_vs_coherent_difference=abs(f12-fc),analytic_full_channel_comparison_upper=e,scope='Floating diagnostic; cutoff convergence is not an infinite-mode certificate'))
 out={'exact_symbolic_checks':3,'rows':rows,'scope':'Analytic finite-lambda theorem must justify infinite-mode complete channel; these finite-cutoff diagnostics do not.'}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
