"""Actual reset-first own-generator fixture, all 96 basis states and coherences.
Includes complete/incomplete ownership, dirty workspace, aborts, commit,
nonmonomial payload completion, and the actual driven label-resolved monitor.
It does not test Tanner density or acquisition service.
"""
import numpy as np,json,itertools
from scipy.linalg import sqrtm
phases=['A','C0','C1','Q','R0','R1'];shape=(2,6,2,2,2);dim=np.prod(shape)
states=list(itertools.product(*[range(s) for s in shape]));ix={v:i for i,v in enumerate(states)}
I=np.eye(dim,dtype=complex)
def dis(J,O):
 E=J.conj().T@J;return J.conj().T@O@J-(E@O+O@E)/2
g=.5;Omega=.4;km=.7;kt=1.;kc=.6;ka=.8
H=np.zeros_like(I)
for x in states:
 e,c,w,o,m=x
 # Monitor Hamiltonian, active in every clock/ownership/workspace sector.
 y=(e,c,w,o,1-m);H[ix[y],ix[x]]+=Omega
 if o==1 and c in (1,2):
  y=(e,3-c,w,o,m);H[ix[y],ix[x]]+=g
 if o==0 and c in (1,2,4,5):
  partner={1:4,4:1,2:5,5:2}[c]
  y=(e,partner,w,o,m);H[ix[y],ix[x]]+=g
jumps=[];kind=[]
for c in range(6):
 J=np.zeros_like(I)
 for e,w,o in itertools.product(range(2),repeat=3):J[ix[(e,c,w,o,0)],ix[(e,c,w,o,1)]]=np.sqrt(km)
 jumps.append(J);kind.append('monitor')
for s in range(2):
 J=np.zeros_like(I)
 for e,o,m in itertools.product(range(2),repeat=3):J[ix[(e,1,0,o,m)],ix[(e,0,s,o,m)]]=np.sqrt(kc)
 jumps.append(J);kind.append('commit')
# Payload U=SWAP times a dirty-workspace controlled Hadamard on DATA.
U=np.zeros((4,4),complex);Had=np.array([[1,1],[1,-1]])/np.sqrt(2)
for e,w in itertools.product(range(2),repeat=2):
 for q in range(2):
  amp=(int(q==e) if w==0 else Had[q,e])
  U[2*w+q,2*e+w]=amp
assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-14
endpoint=[]
for c,rate in [(2,kt),(4,ka),(5,ka)]:
 for s in range(2):
  J=np.zeros_like(I)
  for e,w,o,m in itertools.product(range(2),repeat=4):
   payload=U if o==1 and c in (2,5) else np.eye(4)
   for ep in range(2):J[ix[(ep,3,0,o,m)],ix[(e,c,w,o,m)]]=np.sqrt(rate)*payload[2*ep+s,2*e+w]
  jumps.append(J);kind.append('endpoint');endpoint.append((c,rate))
def L(O):return 1j*(H@O-O@H)+sum(dis(J,O) for J in jumps)
# Actual committed clock+monitor killed generator (4 dimensional).
x=np.array([[0,1],[1,0]],complex);pl=np.diag([0.,1.]);ac=kt*np.kron(pl,np.eye(2))
hc=g*np.kron(x,np.eye(2))+Omega*np.kron(np.eye(2),x)
mon=[np.sqrt(km)*np.kron(np.diag([int(j==c) for j in range(2)]),np.array([[0,1],[0,0]])) for c in range(2)]
def kill(O):return 1j*(hc@O-O@hc)+sum(dis(J,O) for J in mon)-(ac@O+O@ac)/2
cols=[]
for j in range(16):
 E=np.zeros(16,complex);E[j]=1;cols.append(kill(E.reshape(4,4)).reshape(-1))
Kmat=np.stack(cols,axis=1);R=np.linalg.solve(Kmat,-np.eye(4).reshape(-1)).reshape(4,4);R=(R+R.conj().T)/2
Rmax=2*np.linalg.eigvalsh(R).max();beta=.2/Rmax;s0=1-beta*Rmax;S=s0*np.eye(4)+beta*R
root=np.asarray(sqrtm(S),complex);rcomp=np.asarray(sqrtm(np.eye(4)-S),complex)
D=np.zeros_like(I);Se=np.zeros_like(I);Re=np.zeros_like(I);Be=np.zeros_like(I)
for e,c,m,cp,mp in itertools.product(range(2),range(2),range(2),range(2),range(2)):
 row=ix[(e,c+1,0,1,m)];col=ix[(e,cp+1,0,1,mp)]
 Se[row,col]=S[2*c+m,2*cp+mp];Re[row,col]=root[2*c+m,2*cp+mp];Be[row,col]=rcomp[2*c+m,2*cp+mp]
for e,c,m in itertools.product(range(2),range(2),range(2)):D[ix[(e,c+1,0,1,m)],ix[(e,c+1,0,1,m)]]=1
KD=[]
for s in range(2):
 J=np.zeros_like(I)
 for c,w,o,m in itertools.product(range(6),range(2),range(2),range(2)):J[ix[(0,c,w,o,m)],ix[(s,c,w,o,m)]]=1
 KD.append(J)
credits=[I-D+Re]+[Be@J for J in KD]
def T(O):return sum(J.conj().T@O@J for J in credits)
flag=[]
for e,c,w,o,m in states:flag.append(int(not(w==0 and (c==3 or (c in (0,1,2) and o==1)))))
flag=np.array(flag);B=np.diag(flag);theta=.01;u=.02
weights=[theta**(u-np.array([x[0] for x in states]))]+[theta**(u-flag)]*2
vv=np.prod(1+np.array(weights),axis=0)-1
ww=sum(weights[j]*np.prod([1+weights[k] for k in range(3) if k!=j],axis=0) for j in range(3))
outputs={}
for label,values in [('V',vv),('W',ww)]:
 O=np.diag(values);d=O-sum(J.conj().T@O@J for J in KD);F=T(O)
 term=beta*D@d
 # Retained ordinary terminal occupation service.
 terminal_source=np.diag([kt*int(c==2) for e,c,w,o,m in states])
 term+=s0*terminal_source@D@d
 full_animal=theta**(3*u-(np.array([x[0] for x in states])+2*flag))
 qbad=np.diag([(kt if c==2 else ka if c in (4,5) else 0)*flag[i]*(1-theta)/2*theta*full_animal[i]*(3 if label=='W' else 1) for i,(e,c,w,o,m) in enumerate(states)])
 residual=L(F)+term+qbad
 outputs[label]={'whole_space_service_residual_maxeig_relative':float(np.linalg.eigvalsh((residual+residual.conj().T)/2).max()/max(values)),
  'credit_formula_error_relative':float(np.linalg.norm(F-(O-(D-Se)@d))/max(values)),
  'flag_commutator_relative':float(np.linalg.norm(F@B-B@F)/max(values))}
 assert outputs[label]['whole_space_service_residual_maxeig_relative']<1e-11
out={'dimension':int(dim),'beta':float(beta),'S_min':float(np.linalg.eigvalsh(S).min()),
 'resolvent_identity_error':float(np.linalg.norm(kill(R)+np.eye(4))),
 'credit_unitality_error':float(np.linalg.norm(T(I)-I)),
 'nonmonomial_payload_completion':bool(np.max(np.count_nonzero(abs(U)>1e-12,axis=0))>1),
 'results':outputs,'scope':'Full own-generator/commit/abort/monitor fixture, including retained strict raw bad charge; not acquisition or exterior-many-hub proof.'}
print(json.dumps(out,indent=2))
