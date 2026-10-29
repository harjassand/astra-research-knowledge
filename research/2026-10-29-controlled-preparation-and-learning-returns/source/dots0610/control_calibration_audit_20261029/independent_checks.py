#!/usr/bin/env python3
import numpy as np, itertools, math, json, pathlib, hashlib
from scipy.linalg import expm, eigh, null_space
ROOT=pathlib.Path(__file__).resolve().parent
rng=np.random.default_rng(202610290441)
out={'seed':202610290441,'spin_spectra':[],'endpoint_fixtures':[]}
for j in range(1,31):
 m=np.arange(-j,j+1);z=np.diag(m.astype(float));plus=np.zeros((2*j+1,2*j+1),complex)
 for k,a in enumerate(m[:-1]):plus[k+1,k]=np.sqrt(j*(j+1)-a*(a+1))
 x=(plus+plus.conj().T)/2;y=(plus-plus.conj().T)/(2j)
 v=np.eye(2*j+1)[:,j];vx=expm(-1j*np.pi*y/2)@v;vy=expm(1j*np.pi*x/2)@v
 T=(np.outer(v,v)+np.outer(vx,vx.conj())+np.outer(vy,vy.conj()))/3
 beta=float(eigh(T,eigvals_only=True)[-1]);c=0 if j%2 else (-1)**(j//2)*math.comb(j,j//2)/2**j
 expected=max(1+2*c,1-c)/3
 assert abs(beta-expected)<1e-12 and beta<=7/12+1e-12
 out['spin_spectra'].append({'j':j,'matrix_beta':beta,'formula_beta':expected})
def matchings(v):
 if not v:yield ();return
 for j in range(1,len(v)):
  for t in matchings(v[1:j]+v[j+1:]):yield ((v[0],v[j]),)+t
def state(n,M):
 v=np.zeros(2**n)
 for x in range(2**n):
  b=[(x>>(n-1-j))&1 for j in range(n)]
  if all(b[a]!=b[c] for a,c in M):v[x]=np.prod([1 if b[a]==0 else -1 for a,c in M])/np.sqrt(2**len(M))
 return v
n=4;D=16;states=np.column_stack([state(n,M) for M in matchings(tuple(range(n)))])
_,V=eigh(states@states.T);V=V[:,-2:];P=V@V.T;W=null_space(V.T)[:,:2]
perms=[]
for p in itertools.permutations(range(n)):
 ids=[]
 for x in range(D):
  b=[(x>>(n-1-j))&1 for j in range(n)];ids.append(sum(b[p[j]]<<(n-1-j) for j in range(n)))
 perms.append(np.eye(D)[ids])
for trial in range(16):
 eta=(0,1e-5,.001,.01)[trial%4];de=.0001*(trial%3);noise=(.0001,.002,.01,.1)[trial//4]
 Eiso=np.sqrt(1-eta)*V+np.sqrt(eta)*W
 Es=[np.sqrt(1-de)*Eiso,np.sqrt(de)*Eiso@np.diag([1.,-1.])]
 Ds=[Eiso.conj().T]+[np.outer([1.,0.],v.conj()) for v in null_space(Eiso.conj().T).T]
 A=rng.normal(size=(3*D,D))+1j*rng.normal(size=(3*D,D));A,_=np.linalg.qr(A)
 Ns=[np.sqrt(1-noise)*np.eye(D)]+[np.sqrt(noise)*B for B in A.reshape(3,D,D)]
 delta=1-sum(abs(np.trace(d@e)/2)**2 for d in Ds for e in Es)
 measuredeta=sum(np.trace(e.conj().T@(np.eye(D)-P)@e).real/2 for e in Es)
 pbad=1-sum(abs(np.trace(V.T@a@V)/2)**2 for a in Ns)
 servicefe=sum(abs(np.trace(d@R.T@a@R@e)/2)**2 for R in perms for d in Ds for a in Ns for e in Es)/len(perms)
 error=1-servicefe
 bound=(np.sqrt(max(delta,0))+np.sqrt(max(pbad,0))+2*np.sqrt(max(measuredeta,0)))**2
 assert error<=bound+1e-11
 if eta==0:assert error<=delta+pbad-delta*pbad+1e-11
 out['endpoint_fixtures'].append({'trial':trial,'eta':measuredeta,'delta':delta,'p_orbit':pbad,'service_loss':error,'triangle_bound':bound})
# GHZ counterexample: collective phase is logical iZ, identity on P.
z=np.diag([1.,-1.]);Ztot=sum(np.kron(np.kron(np.eye(2**i),z),np.eye(2**(n-i-1))) for i in range(n))
U=expm(1j*np.pi*Ztot/8);G=np.eye(D)[:,[0,D-1]]
assert np.linalg.norm(V.T@U@V-np.eye(2))<1e-12
assert np.linalg.norm(G.T@U@G-1j*z)<1e-12
out['wrong_encoder_counterexample']={'singlet_identity_residual':float(np.linalg.norm(V.T@U@V-np.eye(2))),'GHZ_logical_iZ_residual':float(np.linalg.norm(G.T@U@G-1j*z))}
# Identity instead of requested permutations: exact n6 numerical fixture.
n=6;vs=[state(n,M) for M in matchings(tuple(range(n)))];E=[]
for v in vs:
 v=v.copy()
 for e in E:v-=np.vdot(e,v)*e
 if np.linalg.norm(v)>1e-10:E.append(v/np.linalg.norm(v))
E=np.column_stack(E[:4]);U=np.eye(64)-2*np.outer(vs[0],vs[0])
loss=1-abs(np.trace(E.T@U@E)/4)**2;q=1-np.mean([abs(v@U@v)**2 for v in vs])
assert abs(loss-.75)<1e-12 and abs(q-17/40)<1e-12
out['wrong_permutation_counterexample']={'fixed_loss':loss,'matching_q':q,'claimed_orbit_upper_if_controls_wrong':8*q/5}
out['all_checks_passed']=True
out['script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
(ROOT/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'spin_sectors':30,'endpoint_fixtures':16}))
