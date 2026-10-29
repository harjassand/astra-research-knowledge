import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import numpy as np,importlib.util,json,hashlib
D=Path(__file__).parent.parent;Q=D.parent
sp=importlib.util.spec_from_file_location('clock',D/'clocked_channel_v1.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);H=(X+Z)/np.sqrt(2);PS=[I,X,Y,Z];CX=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
G=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];clock={'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}
def emb(g,qs,n):
 out=np.zeros((2**n,2**n),complex)
 for col in range(2**n):
  a=sum(((col>>(n-1-q))&1)<<(len(qs)-1-j) for j,q in enumerate(qs))
  for b in range(2**len(qs)):
   row=col
   for j,q in enumerate(qs):
    mask=1<<(n-1-q);row=(row&~mask)|(((b>>(len(qs)-1-j))&1)*mask)
   out[row,col]=g[b,a]
 return out
def rot(p,a):return np.cos(a/2)*np.eye(len(p))-1j*np.sin(a/2)*p
def schedule(k,flag):
 r=[('prepZ',[5])]+([('prepX',[6])] if flag else [])
 for j,(q,p) in enumerate((q,p) for q,p in enumerate(G[k]) if p!='I'):
  if flag and j in [1,3]:r.append(('CX',[6,5]))
  if p=='X':r.append(('H',[q]))
  r.append(('CX',[q,5]))
  if p=='X':r.append(('H',[q]))
 return r+[('measureZ',[5]),('readoutZ',[5])]+([('measureX',[6]),('readoutX',[6])] if flag else [])
def dur(kind):return clock['prep' if kind.startswith('prep') else 'measure' if kind.startswith('measure') else 'feedback' if kind.startswith('readout') else 'two' if kind=='CX' else 'one']
def direct(rho,k,flag,eta,rate):
 n=7 if flag else 6;av=np.kron([1,0],np.array([1,1])/np.sqrt(2)) if flag else np.array([1,0]);B={():np.kron(rho,np.outer(av,av))};live=list(range(5));ix=np.arange(2**n)
 for kind,qs in schedule(k,flag):
  if kind.startswith('prep'):live+=qs;U=emb(rot(Y,eta),qs,n)
  elif kind=='H':U=emb(rot(X,eta)@H,qs,n)
  elif kind=='CX':U=emb(rot(np.kron(Z,Z),eta)@CX,qs,n)
  else:U=None
  if U is not None:B={sy:U@v@U.conj().T for sy,v in B.items()}
  hd=sum((((ix[:,None]>>(n-1-q))^(ix[None,:]>>(n-1-q)))&1) for q in live)
  factor=np.exp(-rate*dur(kind)*hd);B={sy:v*factor for sy,v in B.items()}
  if kind.startswith('measure'):
   U=emb(rot(Y if kind=='measureZ' else Z,eta),qs,n);axis=Z if kind=='measureZ' else X
   B2={}
   for sy,v in B.items():
    v=U@v@U.conj().T
    for bit in [0,1]:
     proj=emb((I+(-1)**bit*axis)/2,qs,n);B2[sy+(bit,)]=proj@v@proj
   B=B2;live=[q for q in live if q not in qs]
 anc=2**(n-5);out={}
 for sy,v in B.items():out[sy if flag else sy[0]]=np.einsum('iaja->ij',v.reshape(32,anc,32,anc))
 return out
basis=[np.ones((1,1),complex)]
for _ in range(5):basis=[np.kron(p,q) for p in basis for q in PS]
basis=np.array(basis);basisflat=basis.reshape(1024,1024)
rng=np.random.default_rng(20261028);r=rng.normal(size=(32,32))+1j*rng.normal(size=(32,32));rho=r@r.conj().T;rho/=np.trace(rho)
z=rng.normal(size=(32,32))+1j*rng.normal(size=(32,32));z/=np.linalg.norm(z)
inputs=[rho,z];coeff=[np.einsum('aij,ji->a',basis,v) for v in inputs]
def local(B,T,q):
 ten=B.reshape([4]*5+[B.shape[1]]);return np.moveaxis(np.tensordot(T,ten,axes=(1,q)),0,q).reshape(B.shape)
counts=np.array([sum(p in (1,2) for p in digs) for digs in np.ndindex(*(4,)*5)])
def wait(B,rate,dt):return np.exp(-rate*dt*counts)[:,None]*B
def correct(B,e,eta,rate):
 w=m.fc.string(e)
 for q,p in enumerate(w):
  if p!='I':
   u=rot(X,eta)@{'X':X,'Y':Y,'Z':Z}[p];T=np.array([[np.trace(a@u@b@u.conj().T).real/2 for b in PS] for a in PS]);B=local(B,T,q)
  B=wait(B,rate,1.)
 return B
rows=[]
for strength in [0.,.01,.1]:
 eta=.001;rate=strength/201;flag=[];plain=[];errs=[]
 for flagged in [True,False]:
  target=flag if flagged else plain
  for k in range(4):
   T=m.check(k,flagged,eta,rate,clock);target.append(T)
   for inp,co in zip(inputs,coeff):
    dc=direct(inp,k,flagged,eta,rate)
    for key,out in dc.items():
     pred=(T[key]@co)@basisflat/32;err=float(np.max(abs(pred.reshape(32,32)-out)));assert err<3e-13;errs.append(err)
 # Independently compose actual branches and physical padding in Pauli coordinates.
 fresh={():np.eye(1024)}
 for U in plain:fresh={sy+(b,):op@pre for sy,pre in fresh.items() for b,op in U.items()}
 rec={}
 for mode in [-1,0,1,2,3]:
  rec[mode]=sum((correct(op.copy(),m.fc.W1COR[sy] if mode<0 else m.fc.FLAGCOR[mode].get(sy,m.fc.W1COR[sy]),eta,rate) for sy,op in fresh.items()),np.zeros((1024,1024)))
 F=np.zeros((1024,1024));pre=np.eye(1024)
 for k,U in enumerate(flag):
  for (s,f),op in U.items():
   if (s,f)!=(0,0):F+=rec[k if f else -1]@wait(op@pre,rate,(3-k)*30)
  pre=U[0,0]@pre
 F+=correct(wait(pre,rate,4*19),0,eta,rate)
 tp=float(np.max(abs(F[0]-np.eye(1024)[0])));assert tp<3e-11
 if strength==0:
  K=m.old.ec_kraus(eta)[0];densityF=m.old.superop(K);expected=(basisflat.conj()@densityF@basisflat.T/32).real
  zeroerr=float(np.max(abs(F-expected)));assert zeroerr<2e-12
 saved=json.loads((D/('zero_clock_v1.json' if strength==0 else 'rate_'+str(strength)+'_v1.json')).read_text())
 init,dec=m.code_coordinates();A=init.copy();native=m.native();rep=[]
 for t in range(1,33):
  for q,N in enumerate(native):A=local(A,N,q)
  A=F@A
  if t in [1,2,4,8,16,32]:
   M=dec@A;savedrow=next(x for x in saved['encoded'] if x['T']==t);err=float(np.max(abs(M-savedrow['logical_PTM'])));assert err<3e-11
   rep.append({'T':t,'PTM_error':err,'infidelity':float((4-np.trace(M))/4)})
 for q,N in enumerate(native):
  E=np.diag([1,np.exp(-strength),np.exp(-strength),1])@N
  for x in saved['same_elapsed_unencoded'][q]['results']:assert np.max(abs(np.linalg.matrix_power(E,x['T'])-x['logical_PTM']))<1e-12
 row={'integrated':strength,'direct_density_instrument_max_error':max(errs),'TP_max_error':tp,'replays':rep};rows.append(row);print(row,flush=True)
files=[D/'clocked_channel_v1.py',D/'GOVERNING_CLOCK_MODEL_v1.md',D/'MANDATORY_CHANNEL_SCOPE_ADDENDUM_v1.md',D/'AUTHOR_MANIFEST_CLOCK_v2.json',D/'zero_clock_v1.json',D/'rate_0.01_v1.json',D/'rate_0.1_v1.json',Q/'flagged_five_qubit_storage_check_20261028.py',Path(__file__)]
out={'status':'PASS_DIRECT_DENSITY_CLOCK_INSTRUMENTS_AND_PHYSICAL_REUSE','rows':rows,'zero_background_fulloperator_max_error':zeroerr,'source_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
