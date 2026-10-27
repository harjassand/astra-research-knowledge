from pathlib import Path
import numpy as np,sympy as S,json,itertools,time
OUT=Path(__file__).parent
# Symmetric quartic tensor, reconstructed independently from F.
a,b,c,d=S.symbols('a b c d');xs=(a,b,c,d);u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=u*u+v*v+3*w*w+16*q*q+4*q*(u-v)
T=np.zeros((4,4,4,4))
for exp,coef in S.Poly(F,*xs).terms():
 ids=sum(([i]*n for i,n in enumerate(exp)),[]);perms=set(itertools.permutations(ids))
 for perm in perms:T[perm]=float(coef)/len(perms)
K=np.array([(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2)])
N=9;grid=np.stack(np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij'),axis=-1).reshape(-1,2)
G=[];J=[]
for k in K:
 phase=grid@k;scale=np.sqrt(2)/np.linalg.norm(k)
 for out in range(2):
  for trig in range(2):
   # phi = scale*sin or scale*cos; derivatives are exact Fourier functions.
   val=np.cos(phase) if trig==0 else -np.sin(phase)
   der=-np.sin(phase) if trig==0 else -np.cos(phase)
   gg=np.zeros((len(grid),4));jj=np.zeros((2,len(grid),4))
   for col in range(2):
    ix=out*2+col;gg[:,ix]=scale*k[col]*val
    for i in range(2):jj[i,:,ix]=scale*k[col]*k[i]*der
   G.append(gg);J.append(jj)
G=np.array(G).transpose(1,2,0);J=np.array(J).transpose(1,2,3,0)
assert np.linalg.norm(np.einsum('nia,nib->ab',G,G)/len(grid)-np.eye(G.shape[-1]))<1e-12

def calc(coef,kind):
 gg=G@coef;jj=J@coef
 if kind=='jensen':
  Q=6*np.einsum('ijkl,nk,nl->ij',T,gg,gg,optimize=True)/len(grid)
  ell=4*np.einsum('ijkl,nj,nk,nl->i',T,gg,gg,gg,optimize=True)/len(grid)
 else:
  Q=12*np.einsum('abkl,ina,inb->kl',T,jj,jj,optimize=True)/len(grid)
  ell=24*np.einsum('abkl,nl,ina,inb->k',T,gg,jj,jj,optimize=True)/len(grid)
 eig=np.linalg.eigvalsh(Q)
 if eig[0]<1e-10:raise ArithmeticError('unresolved singular background')
 B=-.5*np.linalg.solve(Q,ell);A=gg+B
 if kind=='jensen':
  val=np.einsum('ijkl,ni,nj,nk,nl->',T,A,A,A,A,optimize=True)/len(grid)-np.einsum('ijkl,i,j,k,l->',T,B,B,B,B,optimize=True)
  ga=4*np.einsum('ijkl,nj,nk,nl->ni',T,A,A,A,optimize=True)
  grad=np.einsum('ni,nic->c',ga,G,optimize=True)/len(grid)
 else:
  val=12*np.einsum('abkl,nk,nl,ina,inb->',T,A,A,jj,jj,optimize=True)/len(grid)
  ga=24*np.einsum('abkl,nl,ina,inb->nk',T,A,jj,jj,optimize=True)
  gj=24*np.einsum('abkl,nk,nl,inb->ina',T,A,A,jj,optimize=True)
  grad=(np.einsum('ni,nic->c',ga,G,optimize=True)+np.einsum('ina,inac->c',gj,J,optimize=True))/len(grid)
 return float(val),grad,B,float(eig[0])

if __name__=='__main__':
 rng=np.random.default_rng(20261027);records=[];tick=time.monotonic()
 for kind in ['heat','jensen']:
  best=None
  for restart in range(12):
   coef=rng.normal(size=32);coef/=np.linalg.norm(coef);m=coef*0;vv=coef*0
   for step in range(1200):
    val,g,B,ev=calc(coef,kind);g-=coef*(coef@g)
    if best is None or val<best['value']:
     best={'kind':kind,'value':val,'coef':coef.tolist(),'B':B.tolist(),'background_min_eigenvalue':ev,'restart':restart,'step':step,'status':'NUMERICAL_ONLY','modes':K.tolist(),'grid':N}
    m=.9*m+.1*g;vv=.999*vv+.001*g*g
    lr=.012*(.2+.8*(1-step/1200))
    coef-=lr*m/(np.sqrt(vv)+1e-8);coef/=np.linalg.norm(coef)
   print(json.dumps({'kind':kind,'restart':restart,'local':val,'best':best['value'],'seconds':time.monotonic()-tick}),flush=True)
   (OUT/f'{kind}_fourier_candidate.json').write_text(json.dumps(best,indent=2)+'\n')
  records.append(best)
 (OUT/'fourier_results.json').write_text(json.dumps(records,indent=2)+'\n')
