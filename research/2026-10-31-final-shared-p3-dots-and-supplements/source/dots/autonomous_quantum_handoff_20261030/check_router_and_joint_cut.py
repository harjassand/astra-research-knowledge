"""Finite algebra diagnostics only: actual router local matrices and joint-cut identity."""
from pathlib import Path
from functools import reduce
import json,numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(10153)
kron=lambda *x:reduce(np.kron,x)
I2=np.eye(2);I3=np.eye(3);X=np.array([[0,1],[1,0]],complex)
S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
ps=[np.diag([float(j==k) for j in range(3)]) for k in range(3)]
u=[np.eye(4),S,S];G=sum(kron(u[k],ps[k]) for k in range(3))
e=np.zeros((3,3),complex);e[1,0]=1;hclock=e+e.conj().T
Omega=.8;kappa=.9;mu=.37
Hphys=Omega*kron(S,hclock);Hcan=Omega*kron(np.eye(4),hclock)
j=np.zeros((3,3),complex);j[2,1]=np.sqrt(kappa);J=kron(np.eye(4),j)
resets=[];pulled=[]
for c in range(3):
 for b in range(2):
  r=np.zeros((2,2),complex);r[0,b]=np.sqrt(mu)
  K=kron(I2,r,ps[c]);pulled.append(K);resets.append(G@K@G.conj().T)
protectedX=kron(X,I2,I3)
checks={'frame_unitarity':float(np.linalg.norm(G.conj().T@G-np.eye(12))),
'hop_exact_covariance':float(np.linalg.norm(G.conj().T@Hphys@G-Hcan)),
'done_same_frame':float(np.linalg.norm(G.conj().T@J@G-J)),
'each_vacant_reset_protected_commutator':max(float(np.linalg.norm((G.conj().T@K@G)@protectedX-protectedX@(G.conj().T@K@G))) for K in resets),
'complete_reset_loss':float(np.linalg.norm(sum(K.conj().T@K for K in resets)-mu*np.eye(12)))}
R=np.zeros((3,3),complex);R[:2,:2]=[[2/kappa+(kappa+2*mu)/(4*Omega**2),-1j/(2*Omega)],[1j/(2*Omega),2/kappa]]
def adj(H,js,O):
 gam=sum(v.conj().T@v for v in js)
 return 1j*(H@O-O@H)+sum(v.conj().T@O@v for v in js)-(gam@O+O@gam)/2
clockjs=[j]+[np.sqrt(mu)*p for p in ps]
checks['actual_dephased_clock_gramian_error']=float(np.linalg.norm(adj(Omega*hclock,clockjs,R)+ps[0]+ps[1]))
checks['gramian_min_eigenvalue']=float(np.linalg.eigvalsh(R[:2,:2]).min())
# Coherent route phases, unknown Q maximally entangled with its reference,
# and uninitialized spare maximally entangled with a different retained bath.
cl=np.array([.6,.48j,.4]);cl/=np.linalg.norm(cl)
phi=np.eye(2)/np.sqrt(2)
v=np.einsum('qr,bs,c->qbcrs',phi,phi,cl).reshape(-1)
rho=np.outer(v,v.conj());GG=kron(G,np.eye(4));physical=GG@rho@GG.conj().T
out=sum(kron(K/np.sqrt(mu),np.eye(4))@physical@kron(K/np.sqrt(mu),np.eye(4)).conj().T for K in resets)
canout=GG.conj().T@out@GG
# trace out B,clock,R_b; keep Q,R_q
reduced=lambda a:np.einsum('qbcrsQbcRs->qrQR',a.reshape(2,2,3,2,2,2,2,3,2,2)).reshape(4,4)
checks['coherent_reset_protected_reference_error']=float(np.linalg.norm(reduced(canout)-reduced(rho)))
checks['coherent_reset_trace_error']=float(abs(np.trace(out)-1))
# Cross-witness-free joint projection identity, with a strong bath-only H.
p0=np.diag([1.,0.]);PC=kron(p0,I2,I2);PB=kron(I2,p0,I2);P=PC@PB;d=8
FC=kron(p0,2*I2+.3*X,I2)+kron(I2-p0,3*I2+.2*X,I2)
GB=kron(2*I2+.4*X,p0,I2)+kron(3*I2+.1*X,I2-p0,I2)
checks['FC_own_cut_commutator']=float(np.linalg.norm(FC@PC-PC@FC))
checks['FC_other_cut_commutator']=float(np.linalg.norm(FC@PB-PB@FC))
checks['GB_other_cut_commutator']=float(np.linalg.norm(GB@PC-PC@GB))
h=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=(h+h.conj().T)/35
js=[(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))/45 for _ in range(2)]
gam=sum(k.conj().T@k for k in js)
L=lambda a:-1j*(h@a-a@h)+sum(k@a@k.conj().T for k in js)-(gam@a+a@gam)/2
Hbath=kron(I2,I2,1000*X)
Lb=lambda a:-1j*(Hbath@a-a@Hbath)
w=rng.normal(size=d)+1j*rng.normal(size=d);w/=np.linalg.norm(w);a=np.outer(w,w.conj())
sigma=P@a@P;rem=P@L(a-sigma)@P
checks['joint_projected_derivative_identity']=float(np.linalg.norm(P@L(a)@P-P@L(sigma)@P-rem))
checks['unbounded_bath_surrogate_remainder']=float(np.linalg.norm(P@Lb(a-sigma)@P))
C=2*np.linalg.norm(h,2)+2*sum(np.linalg.norm(k,2)**2 for k in js)
delta=float(np.trace((np.eye(d)-P)@a).real)
checks['remainder_norm']=float(np.linalg.norm(rem,'nuc'))
checks['remainder_bound']=float(2*C*np.sqrt(delta))
checks['pulse_mode_loss']={str(t):float(1-np.exp(-.01*t)) for t in [1,10,100,1000]}
checks['scope']='finite router and projection algebra; not a controller-validity, Tanner-family, or lifetime simulation'
for k in ['frame_unitarity','hop_exact_covariance','done_same_frame','each_vacant_reset_protected_commutator','complete_reset_loss','actual_dephased_clock_gramian_error','coherent_reset_protected_reference_error','coherent_reset_trace_error','FC_own_cut_commutator','joint_projected_derivative_identity','unbounded_bath_surrogate_remainder']:assert checks[k]<1e-11,(k,checks[k])
assert checks['FC_other_cut_commutator']>.1 and checks['GB_other_cut_commutator']>.1
assert checks['gramian_min_eigenvalue']>0 and checks['remainder_norm']<=checks['remainder_bound']
Path(__file__).with_suffix('.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
