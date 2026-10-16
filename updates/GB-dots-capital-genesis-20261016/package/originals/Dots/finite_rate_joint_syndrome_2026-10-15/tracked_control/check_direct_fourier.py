import numpy as np
from scipy.sparse import csr_matrix,eye,kron,block_diag
from scipy.sparse.linalg import expm_multiply
from functools import reduce
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex)
k=np.kron;ctrl=[k(Z,I),k(I,Z)];d=4;dc=4;D=16;D2=D*D
Hbase=.7*k(Z,I)+.31*k(Z,X)+.13*k(I,Z)
As=[.12*k(X,Z),.11*k(Y,X)];Js=[.12,.11];gammas=[.8,1.1]
assert np.linalg.norm(Hbase@As[0]-As[0]@Hbase)>.01
plus=np.ones(4)/2;cp=np.outer(plus,plus);minus=np.array([1,-1])/np.sqrt(2)
obs=[k(np.outer(minus,minus),I),k(I,np.outer(minus,minus)),np.outer(k(minus,minus),k(minus,minus))]
subs=[[0],[1],[0,1]]
def liou(H):
 h=csr_matrix(H);ident=eye(D,format='csr');return -1j*(kron(ident,h)-kron(h.T,ident))
def generator(active):
 blocks=[]
 for bits in range(4):
  H=k(np.eye(dc),Hbase)
  for i in active:H+=(-1 if bits>>i&1 else 1)*k(ctrl[i],As[i])
  blocks.append(liou(H))
 M=block_diag(blocks,format='csr');C=np.zeros((4,4))
 for bits in range(4):
  for i in active:C[bits,bits]-=gammas[i];C[bits^(1<<i),bits]+=gammas[i]
 return M+kron(csr_matrix(C),eye(D2,format='csr'))
def bound(j,g,t):
 dd=np.sqrt(g*g+4*j*j);return .5*(np.exp(-g*t)*(np.cosh(dd*t)+g/dd*np.sinh(dd*t))-1)
# One column for every input matrix unit, testing the complete joint input effect.
vin=np.zeros((4*D2,d*d),complex)
for b in range(d):
 for c in range(d):
  e=np.zeros((d,d),complex);e[b,c]=1;vin[:D2,b*d+c]=k(cp,e).reshape(-1,order='F')
for name,segments,taus in [('reused_sequential',[(.4,[0]),(.6,[1])],[.4,.6]),('formal_overlap',[(.3,[0]),(.4,[0,1]),(.3,[1])],[.7,.7])]:
 v=vin.copy(); vvirtual=vin[:D2].copy()
 for duration,active in segments:
  v=expm_multiply(duration*generator(active),v)
  H=k(np.eye(dc),Hbase)+sum((k(ctrl[i],As[i]) for i in active),np.zeros((D,D),complex))
  Lv=liou(H)
  for i in active:
   xc=k(k(X,I) if i==0 else k(I,X),np.eye(d)); xs=csr_matrix(xc)
   Lv+=gammas[i]*(kron(xs.conj(),xs)-eye(D2,format='csr'))
  vvirtual=expm_multiply(duration*Lv,vvirtual)
 out=sum(v[j*D2:(j+1)*D2] for j in range(4))
 for subset,O in zip(subs,obs):
  E=np.zeros((d,d),complex);observable=k(O,np.eye(d))
  for b in range(d):
   for c in range(d):E[c,b]=np.trace(observable@out[:,b*d+c].reshape((D,D),order='F'))
  Ev=np.zeros((d,d),complex)
  for b in range(d):
   for c in range(d):Ev[c,b]=np.trace(observable@vvirtual[:,b*d+c].reshape((D,D),order='F'))
  assert np.linalg.norm(E-Ev)<2e-12,(name,subset,'virtual seed mismatch',np.linalg.norm(E-Ev))
  E=(E+E.conj().T)/2;ev=np.linalg.eigvalsh(E);bb=np.prod([min(1,bound(Js[i],gammas[i],taus[i])) for i in subset])
  assert ev.min()>-2e-12 and ev.max()<=bb+2e-12,(name,subset,ev,bb)
  print(f'PASS {name}, subset={subset}: maximal exact effect={ev.max():.10g}, bound={bb:.10g}')
print('PASS exact virtual-seed Lindblad equivalence for all tested joint-input effect matrix units.')
print('Full-joint operator effects tested with noncommuting baseline and shared/reused physical support.')
print('Formal overlap is an algebra test, not a claim of a clean physical pulse implementation.')
