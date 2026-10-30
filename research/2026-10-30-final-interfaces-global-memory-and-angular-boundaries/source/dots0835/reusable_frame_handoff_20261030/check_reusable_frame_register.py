"""Exact finite-register/gauge regressions. Not a full native lifetime simulation."""
import json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix, eye, kron
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import expm
rng=np.random.default_rng(30777)
# Exact permutation representation of GL(2,F2), bits ordered (A,B).
group=[]
for bits in range(16):
 M=np.array([(bits>>j)&1 for j in range(4)],int).reshape(2,2)
 if (M[0,0]*M[1,1]-M[0,1]*M[1,0])%2:
  U=np.zeros((4,4),complex)
  for j in range(4):
   y=M@np.array([j>>1,j&1])%2;U[2*y[0]+y[1],j]=1
  group.append((M,U))
m=len(group);assert m==6
identity=next(i for i,(_,u) in enumerate(group) if np.allclose(u,np.eye(4)))
labels=[('r',g) for g in range(m)]+[('e',a,b) for a in range(m) for b in range(m) if a!=b]
idx={z:j for j,z in enumerate(labels)};d=len(labels);assert d==m*m
w=[z[1] if z[0]=='r' else z[2] for z in labels]
Omega=kappa=1.
Js=[]
for z in labels:
 if z[0]=='e':
  j=np.zeros((d,d),complex);j[idx[('r',z[2])],idx[z]]=np.sqrt(kappa);Js.append(j)
def H(v):
 h=np.zeros((d,d),complex)
 for g in range(m):
  if g!=v:
   a,b=idx[('r',g)],idx[('e',g,v)];h[a,b]=h[b,a]=Omega
 return h
def adjoint(h,obs):
 out=1j*(h@obs-obs@h)
 for j in Js:
  jj=j.conj().T@j;out+=j.conj().T@obs@j-(jj@obs+obs@jj)/2
 return out
R2=np.array([[2/kappa+kappa/(4*Omega**2),-1j/(2*Omega)],[1j/(2*Omega),2/kappa]])
c=3/kappa+kappa/(4*Omega**2)
Rs=[];gramian=[]
for v in range(m):
 R=np.zeros((d,d),complex)
 for g in range(m):
  if g!=v:
   ab=[idx[('r',g)],idx[('e',g,v)]];R[np.ix_(ab,ab)]=R2
 for z in labels:
  if z[0]=='e' and z[2]!=v:R[idx[z],idx[z]]=c
 B=np.eye(d);B[idx[('r',v)],idx[('r',v)]]=0
 ev=np.linalg.eigvalsh(R)[1:];error=np.linalg.norm(adjoint(H(v),R)+B)
 gramian.append({'v':v,'residual':float(error),'min_active':float(min(ev)),'max':float(max(ev))})
 assert error<1e-12 and min(ev)>0;Rs.append(R)
# Full physical gauge, arbitrary coherent native busy prefix, exact target seam.
I2=np.eye(2);I4=np.eye(4);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1])
V=expm(-.37j*(np.kron(X,X)+.41*np.kron(Z,I2)))
F=np.zeros((8,8),complex);F[:4,:4]=I4;F[4:,4:]=V
G=np.zeros((8*d,8*d),complex)
for j,q in enumerate(labels):G[8*j:8*j+8,8*j:8*j+8]=np.kron(I2,group[w[j]][1])
Fbig=np.kron(np.eye(d),F)
frame_errors=[];clock_reset_errors=[];physical_hop_errors=[]
for j in Js:
 jbig=np.kron(j,np.eye(8));clock_reset_errors.append(float(np.linalg.norm(G@jbig@G.conj().T-jbig)))
for v in range(m):
 U=np.kron(I2,group[v][1]);Fv=U@F@U.conj().T
 lhs=np.kron(np.eye(d),Fv.conj().T)@G@Fbig
 E=Fbig.conj().T@np.kron(np.eye(d),U.conj().T)@G@Fbig
 rhs=np.kron(np.eye(d),U)@E
 frame_errors.append(float(np.linalg.norm(lhs-rhs)))
 physical=G@np.kron(H(v),np.eye(8))@G.conj().T
 expected=np.zeros_like(physical)
 for g in range(m):
  if g!=v:
   a,b=idx[('r',g)],idx[('e',g,v)];edge=Omega*np.kron(I2,group[v][1]@group[g][1].conj().T)
   expected[8*b:8*b+8,8*a:8*a+8]=edge;expected[8*a:8*a+8,8*b:8*b+8]=edge.conj().T
 physical_hop_errors.append(float(np.linalg.norm(physical-expected)))
assert max(frame_errors+clock_reset_errors+physical_hop_errors)<1e-12
# Actual sequential program evolution: deliberately interrupt before prior target settled.
# Include coherent initial stale-label superpositions; norm bound makes no diagonal assumption.
def liouv(h):
 h=csr_matrix(h);eye_d=eye(d,format='csr')
 L=-1j*(kron(eye_d,h)-kron(h.T,eye_d))
 for jd in Js:
  j=csr_matrix(jd);jj=j.getH()@j
  L+=kron(j.conjugate(),j)-.5*(kron(eye_d,jj)+kron(jj.T,eye_d))
 return L.tocsr()
psi=rng.normal(size=d)+1j*rng.normal(size=d);psi/=np.linalg.norm(psi)
rho=np.outer(psi,psi.conj());trajectory=[]
commands=[(0,.17),(4,.23),(1,.11),(5,.41),(2,18.)]
a=float(np.linalg.eigvalsh(R2)[0]/c);r=1/c
for v,duration in commands:
 rho=expm_multiply(liouv(H(v))*duration,rho.reshape(-1,order='F')).reshape((d,d),order='F')
 B=np.eye(d);B[idx[('r',v)],idx[('r',v)]]=0
 unfinished=float(np.trace(B@rho).real);moment=float(np.trace((Rs[v]/c)@rho).real)
 # Every new target comparison starts only from the <=1 operator bound.
 bound=float(np.exp(-r*duration)/a)
 assert unfinished<=bound+1e-11
 trajectory.append({'absolute_target':v,'duration':duration,'unfinished_probability':unfinished,'uniform_gramian_bound':bound,'weighted_moment':moment,'trace':float(np.trace(rho).real)})
# A scheduled coherent ramp between targets is still DATA-free before the fixed gauge.
ramp=.37*H(1)+.63*H(3)
rho=expm_multiply(liouv(ramp)*.7,rho.reshape(-1,order='F')).reshape((d,d),order='F')
rho=expm_multiply(liouv(H(3))*18,rho.reshape(-1,order='F')).reshape((d,d),order='F')
B=np.eye(d);B[idx[('r',3)],idx[('r',3)]]=0
ramp_tail=float(np.trace(B@rho).real);assert ramp_tail<=np.exp(-18*r)/a+1e-11
# Ready-controller endpoint cannot manufacture a gate by choosing final target frame.
z=rng.normal(size=(4,2))+1j*rng.normal(size=(4,2));z/=np.linalg.norm(z)
ready=np.vstack((z,np.zeros_like(z)))
timezero=[];settled=[]
# Coherent BUSY native state, not an assumed empty workspace.
busy=np.vstack((z,.73j*z));busy/=np.linalg.norm(busy)
for v in range(m):
 U=np.kron(I2,group[v][1]);Fv=U@F@U.conj().T
 timezero.append(float(np.linalg.norm(Fv.conj().T@ready-ready)))
 settled.append(float(np.linalg.norm(Fv.conj().T@U@F@busy-U@busy)))
assert max(timezero+settled)<1e-12
out={'group':'GL(2,F2), exact permutation representatives','group_size':m,'program_dimension':d,'clock_gramian':gramian,'gramian_a':a,'gramian_r':r,'max_frame_identity_error':max(frame_errors),'max_physical_clock_only_reset_error':max(clock_reset_errors),'max_physical_command_hop_error':max(physical_hop_errors),'interrupted_command_trajectory':trajectory,'finite_ramp_then_settle_unfinished_probability':ramp_tail,'max_time_zero_identity_error':max(timezero),'max_settled_busy_controller_frame_error':max(settled),'scope':'Exact finite-register/physical-gauge regression and single-clock evolution. Not a full native threshold, bath model, or noisy retrieval simulation.'}
Path(__file__).with_name('reusable_frame_register_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
