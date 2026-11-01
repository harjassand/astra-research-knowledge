"""Independent physical-model and certificate receipt. No frozen inputs are modified."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools,sys
import numpy as np
from scipy.linalg import expm
import monitored_phase as candidate
import certify_receiver as cert
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,ok,**evidence):
 if not bool(ok): raise AssertionError((name,evidence))
 checks.append(dict(name=name,**evidence))
def close(name,a,b,tol=4e-11):
 err=float(np.linalg.norm(a-b));check(name,err<tol,error=err,tolerance=tol)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);sm=np.array([[0,1],[0,0]],complex)
def kron(*xs):
 a=np.array([[1.]])
 for x in xs:a=np.kron(a,x)
 return a

def physical_bin(c,loss,up,eta_m,eta_p,dt,dark):
 """Source+data detector directly in laboratory frame, never a parity gauge."""
 h=c*kron(X,Z);l=kron(sm,I);j=kron(l.conj(),l);jp=kron(l.T.conj(),l.T)
 n=l.conj().T@l;p=l@l.conj().T;ident=np.eye(4)
 g=-1j*(kron(ident,h)-kron(h.T,ident))
 g-=loss/2*(kron(ident,n)+kron(n.T,ident))+up/2*(kron(ident,p)+kron(p.T,ident))
 m=np.zeros((32,32),complex)
 m[:16,:16]=g+(1-eta_m)*loss*j+(1-eta_p)*up*jp-dark*np.eye(16)
 m[16:,16:]=g+loss*j+up*jp
 m[16:,:16]=eta_m*loss*j+eta_p*up*jp+dark*np.eye(16)
 e=expm(dt*m)
 return e[:16,:16],e[16:,:16]

def local_chans(params,q0,bins=2,endpoint='none',readout=.07):
 """Find optimal physical record decisions by direct channel overlap with identity.
 Returns complete-record data superoperators, risks, outcome laws and signs.
 No candidate signed map or decision is consulted here.
 """
 c,l,a,em,ep,T,d=params
 maps=physical_bin(c,l,a,em,ep,T/bins,d)
 branches={():np.eye(16,dtype=complex)}
 for _ in range(bins):branches={r+(b,):maps[b]@m for r,m in branches.items() for b in [0,1]}
 source=np.diag([1,0]) if q0==0 else np.diag([0,1])
 outs=[];decisions={};risk=0
 for record,m in branches.items():
  for report in ([None] if endpoint=='none' else [0,1]):
   K=np.zeros((4,4),complex)
   for col in range(4):
    u=np.zeros(4);u[col]=1;u=u.reshape(2,2,order='F')
    rho=(m@kron(source,u).reshape(16,order='F')).reshape(4,4,order='F')
    out=np.zeros((2,2),complex)
    for actual in [0,1]:
     pr=1 if report is None else (1-readout if actual==report else readout)
     out+=pr*rho[actual*2:actual*2+2,actual*2:actual*2+2]
    K[:,col]=out.reshape(4,order='F')
   # Diagonal Z-mixture: physical map is a I(.)I+b Z(.)Z.
   w=float(K[0,0].real);signed=float(K[1,1].real)
   a0=(w+signed)/2;b0=(w-signed)/2
   check('physical_branch_nonnegative',a0>-1e-12 and b0>-1e-12,minimum=min(a0,b0))
   close('physical_branch_is_pauli',K,a0*np.eye(4)+b0*kron(Z,Z))
   correction=int(b0>a0);U=Z if correction else I
   outs.append(kron(U.conj(),U)@K);risk+=min(a0,b0);decisions[(record,report)]=correction
 return sum(outs),risk,branches,decisions

# Independent direct physical complete-channel checks, including q0=1, thermal/dark,
# zero loss, no capture, and actively misleading report probabilities >1/2.
case_params=[(1,4,.3,.8,.35,.7,.05),(.7,0,2,.2,.9,1,.03),(0,3,0,1,0,1,0),(.5,6,.2,0,0,.8,.2)]
for j,par in enumerate(case_params):
 for q in [0,1]:
  for endpoint,e in [('none',0),('noisy_bit',.07),('noisy_bit',.8)]:
   K,p,branches,dec=local_chans(par,q,endpoint=endpoint,readout=e)
   c,l,a,em,ep,T,d=par
   target=(candidate.photon_only_error(c,l,a,em,ep,T,2,q,d) if endpoint=='none' else candidate.bayes_error(c,l,a,em,ep,T,2,q,e,d))
   close('physical_optimal_vs_candidate',np.array(p),np.array(target))
   close('whole_local_superoperator',K,(1-p)*np.eye(4)+p*kron(Z,Z))
   check('risk_beats_best_fixed_pauli',p<=min(candidate.raw_error(c,l,a,T),1-candidate.raw_error(c,l,a,T))+1e-11)

# Product graph channel on a data/reference Choi state, not only |+>.
# Every local physical superoperator was independently generated above.
def apply_to_subsystem(rho,superop,axes,n):
 rest=[a for a in range(n) if a not in axes];perm=list(axes)+rest+[a+n for a in axes]+[a+n for a in rest]
 t=rho.reshape([2]*(2*n)).transpose(perm)
 dl=2**len(axes);dr=2**len(rest);t=t.reshape(dl,dr,dl,dr)
 # vectorization index: output row + dl*output column.
 m=superop.reshape(dl,dl,dl,dl,order='F')
 out=np.einsum('abij,irjs->arbs',m,t)
 inv=np.argsort(perm);return out.reshape([2]*(2*n)).transpose(inv).reshape(2**n,2**n)

p1=case_params[0];p2=case_params[1]
K1,r1,_,_=local_chans(p1,0);K2,r2,_,_=local_chans(p2,1)
U=expm(-1j*(.31*kron(Z,I)-.23*kron(I,Z)+.49*kron(Z,Z)))
phi=np.eye(4).reshape(16)/2;rho=np.outer(phi,phi.conj())
Ur=kron(U,np.eye(4));ideal=Ur@rho@Ur.conj().T
physical=apply_to_subsystem(apply_to_subsystem(ideal,K1,[0],4),K2,[1],4)
expected=np.zeros((16,16),complex);prob=[]
for b1,b2 in itertools.product([0,1],repeat=2):
 w=(r1 if b1 else 1-r1)*(r2 if b2 else 1-r2);prob.append(w)
 zz=kron(Z if b1 else I,Z if b2 else I,np.eye(4));expected+=w*zz@ideal@zz
close('two_source_weighted_graph_complete_Choi_channel',physical,expected)
check('joint_selected_vertex_probability',abs(prob[-1]-r1*r2)<1e-15)
# Reference entanglement and arbitrary Z phases make this a full two-data channel test.
check('physical_channel_trace',abs(np.trace(physical)-1)<1e-11)

# Exact parity Fourier generator signs, independently reconstruct signed 8x8 block.
args=(F(2,3),F(7,2),F(1,3),F(4,5),F(1,4),F(2,7),F(1,100))
A,C=cert.build(*args);c,l,a,em,ep,dt,d=args
Id=np.eye(2,dtype=object);Xo=np.array([[0,1],[1,0]],dtype=object);smo=np.array([[0,1],[0,0]],dtype=object);Q=smo.T@smo;P=Id-Q
Jm=l*kron(smo,smo);Jp=a*kron(smo.T,smo.T)
# Use integer/Fraction construction (not kron helper's floating start).
k=np.kron;Jm=l*k(smo,smo);Jp=a*k(smo.T,smo.T)
Ar=-l/2*(k(Id,Q)+k(Q,Id))-a/2*(k(Id,P)+k(P,Id));Ai=-c*(k(Id,Xo)-k(Xo,Id))
for z in [1,-1]:
 R=np.zeros((8,16),dtype=object)
 for f in [0,1]:R[4*f:4*f+4,8*f:8*f+4]=np.eye(4,dtype=object);R[4*f:4*f+4,8*f+4:8*f+8]=z*np.eye(4,dtype=object)
 B0=np.block([[Ar+z*((1-em)*Jm+(1-ep)*Jp)-d*np.eye(4,dtype=object),np.zeros((4,4),dtype=object)],[em*Jm+ep*Jp+z*d*np.eye(4,dtype=object),Ar+z*(Jm+Jp)]])*dt
 B1=np.block([[Ai,np.zeros((4,4),dtype=object)],[np.zeros((4,4),dtype=object),Ai]])*dt
 check('exact_CQ_Fourier_lift',all(v==0 for M,B in zip(A,[B0,B1]) for v in (R@M-B@R).flat),z=z)

# Exact certificate replay of all five endpoint omission claims; verify decision margins,
# so equality is proved by shared optimal policy, not merely matching decimal displays.
rows=json.loads((ROOT/'receiver_certificates.json').read_text())['rows']
sign_witness=[]
for row in rows:
 l=F(row['parameters']['loss']);A,C=cert.build(F(1),l,F(0),F(99,100),F(0),F(1,4),F(0));E,err,meta=cert.exponential(A,C,8)
 Ms=cert.signed_instruments(E);v=np.array([1,0,0,0],dtype=object);bs=[(v,np.zeros(4,dtype=object))]
 for _ in range(4):bs=[cert.vecmul(M,v) for v in bs for M in Ms]
 total=(1+err)**4-1;e=F(1,1000);minimum=None;extra_dependent=0;photon_blind_opt=True
 for v,im in bs:
  x=F(int(v[0]),cert.S**4);y=F(int(v[3]),cert.S**4);s0=(1-e)*x-e*y;s1=(1-e)*y-e*x;t=x-y
  margin=min(abs(s0),abs(s1),abs(t));minimum=margin if minimum is None else min(minimum,margin)
  if s0*s1>=0:extra_dependent+=1
  if t<0:photon_blind_opt=False
 check('exact_policy_signs_not_rounding',minimum>total,loss=str(l),minimum_margin=str(minimum),process_error=str(total))
 if l>=64:check('exact_omitted_endpoint_policy_equality',extra_dependent==0 and photon_blind_opt,loss=str(l))
 else:check('lambda16_endpoint_genuinely_helps',extra_dependent>0 and F(row['bayes_risk_interval'][1])<F(row['photon_only_receiver']['bayes_risk_interval'][0]))
 sign_witness.append(dict(loss=str(l),same_sign_endpoint_branches=extra_dependent,photon_blind_opt=photon_blind_opt,minimum_margin=str(minimum)))

out={'scope':'Independent declared-model audit; physical detector services not supplied','checks':len(checks),'check_details':checks,'policy_sign_witness':sign_witness}
(ROOT/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'joint_channel_error':[x for x in checks if x['name']=='two_source_weighted_graph_complete_Choi_channel'],'policy_sign_witness':sign_witness},indent=2))
