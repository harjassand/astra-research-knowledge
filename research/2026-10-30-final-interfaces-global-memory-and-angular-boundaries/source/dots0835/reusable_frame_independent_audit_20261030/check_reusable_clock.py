"""Independent exact reusable-clock/gauge checks, not a native-code simulation."""
from pathlib import Path
import itertools,json,numpy as np
from scipy.linalg import norm,eigvalsh
from scipy.sparse import csc_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply

def kb(i,j,d):
 z=np.zeros((d,d),complex);z[i,j]=1;return z

def model(m,v,Om=1.,kap=1.):
 labels=[('r',g) for g in range(m)]+[('e',a,b) for a in range(m) for b in range(m) if a!=b]
 ix={q:i for i,q in enumerate(labels)};D=len(labels)
 H=np.zeros((D,D),complex)
 for g in range(m):
  if g!=v:H+=Om*(kb(ix[('r',g)],ix[('e',g,v)],D)+kb(ix[('e',g,v)],ix[('r',g)],D))
 js=[np.sqrt(kap)*kb(ix[('r',b)],ix[('e',a,b)],D) for a in range(m) for b in range(m) if a!=b]
 Q=np.eye(D)-kb(ix[('r',v)],ix[('r',v)],D)
 A0=2/kap+kap/(4*Om**2);d=1/kap+A0
 R2=np.array([[A0,-1j/(2*Om)],[1j/(2*Om),2/kap]])
 R=np.zeros((D,D),complex)
 for g in range(m):
  if g!=v:R[np.ix_([ix[('r',g)],ix[('e',g,v)]],[ix[('r',g)],ix[('e',g,v)]])]=R2
 for a in range(m):
  for b in range(m):
   if a!=b and b!=v:R[ix[('e',a,b)],ix[('e',a,b)]]=d
 return labels,ix,H,js,Q,R,R2,d

def adj(H,js,O):return 1j*(H@O-O@H)+sum((j.conj().T@O@j-.5*(j.conj().T@j@O+O@j.conj().T@j) for j in js),np.zeros_like(O))
def liouv(H,js):
 D=len(H);I=eye(D,dtype=complex,format='csc');H=csc_matrix(H)
 L=-1j*(kron(I,H)-kron(H.T,I))
 for j in js:
  j=csc_matrix(j);jj=j.conj().T@j
  L+=kron(j.conjugate(),j)-.5*(kron(I,jj)+kron(jj.T,I))
 return L.tocsc()
rows=[]
for m in [2,3,6]:
 worst=0.
 for v in range(m):
  labs,ix,H,js,Q,R,R2,d=model(m,v)
  residual=norm(adj(H,js,R)+Q);worst=max(worst,residual)
  assert residual<1e-11 and eigvalsh(R+np.eye(m*m)-Q)[0]>0
 rows.append({'group_size':m,'register_dimension':m*m,'reset_channels':m*(m-1),'worst_Gramian_residual':float(worst),'Rmax':float(d),'R2max':float(eigvalsh(R2)[-1]),'a':float(eigvalsh(R2)[0]/d),'r':1/d})
# Counterexample to coherently merging resets by their target.
labs,ix,H,js,Q,R,_,_=model(3,0);D=9
merged=[]
for b in range(3):merged.append(sum((kb(ix[('r',b)],ix[('e',a,b)],D) for a in range(3) if a!=b),np.zeros((D,D),complex)))
psi=(np.eye(D)[:,ix[('e',0,1)]]-np.eye(D)[:,ix[('e',2,1)]])/np.sqrt(2)
rhod=np.outer(psi,psi.conj());Ld=liouv(H,merged)
dark=float(norm(Ld@rhod.ravel(order='F')));proper=float(norm(liouv(H,js)@rhod.ravel(order='F')))
assert dark<1e-12 and proper>.5
# Exact GL(2,F2) permutation lifts.
matrices=[]
for bits in itertools.product([0,1],repeat=4):
 A=np.array(bits,dtype=int).reshape(2,2)
 if (A[0,0]*A[1,1]-A[0,1]*A[1,0])%2:matrices.append(A)
identity=next(i for i,A in enumerate(matrices) if np.array_equal(A,np.eye(2,dtype=int)))
us=[]
for A in matrices:
 u=np.zeros((4,4),complex)
 for x in range(4):
  y=A@np.array([x>>1,x&1])%2;u[2*y[0]+y[1],x]=1
 us.append(u)
def multiply(a,b):return next(i for i,A in enumerate(matrices) if np.array_equal(A,matrices[a]@matrices[b]%2))
closure=max(norm(us[a]@us[b]-us[multiply(a,b)]) for a in range(6) for b in range(6))
forward=next(i for i,A in enumerate(matrices) if np.array_equal(A,[[1,0],[1,1]]))
reverse=next(i for i,A in enumerate(matrices) if np.array_equal(A,[[1,1],[0,1]]))
v1=forward;v2=multiply(reverse,v1);v3=multiply(forward,v2)
labs,ix,H,js,Q,R,R2,d=model(6,v3);D=36
w=[q[1] if q[0]=='r' else q[2] for q in labs]
G=sum((np.kron(us[w[q]],kb(q,q,D)) for q in range(D)),np.zeros((4*D,4*D),complex))
reset_res=max(norm(G@np.kron(np.eye(4),j)@G.conj().T-np.kron(np.eye(4),j)) for j in js)
edge_res=0.
for g in range(6):
 if g==v3:continue
 E=kb(ix[('e',g,v3)],ix[('r',g)],D)
 edge_res=max(edge_res,norm(G@np.kron(np.eye(4),E)@G.conj().T-np.kron(us[v3]@us[g].conj().T,E)))
rho=kb(ix[('r',identity)],ix[('r',identity)],D)
schedule=[(v1,.31),(v2,.47),(v3,80.)]
for v,time in schedule:
 _,_,hh,jj,*_=model(6,v)
 rho=expm_multiply(time*liouv(hh,jj),rho.ravel(order='F')).reshape(D,D,order='F')
unfinished=float(np.trace(Q@rho).real);bound=np.exp(-80/d)/(eigvalsh(R2)[0]/d)
rng=np.random.default_rng(991);x=rng.normal(size=8)+1j*rng.normal(size=8);x/=norm(x);data=np.outer(x,x.conj())
out=np.zeros_like(data)
for q in range(D):
 u=np.kron(us[w[q]],np.eye(2));out+=rho[q,q].real*u@data@u.conj().T
u=np.kron(us[v3],np.eye(2));target=u@data@u.conj().T
err=float(np.linalg.svd(out-target,compute_uv=False).sum())
assert closure<1e-12 and reset_res<1e-12 and edge_res<1e-12
assert unfinished<=bound+1e-12 and err<=2*unfinished+1e-10
# Reissuing an order-3 absolute target leaves it, rather than multiplying again.
_,ix2,h2,j2,_,_,_,_=model(6,v2);settled=kb(ix2[('r',v2)],ix2[('r',v2)],D)
absolute=float(norm(liouv(h2,j2)@settled.ravel(order='F')))
assert absolute<1e-12 and multiply(v2,v2)!=v2
outdict={'scope':'Exact finite-clock/group/gauge and ideal DATA-reference sanity checks only. No native memory, bath threshold or encoded retrieval is simulated.','Gramians':rows,'coherent_merged_reset_counterexample':{'dark_state_generator_norm':dark,'separate_reset_generator_norm':proper},'GL2_exact_closure_residual':float(closure),'physical_clock_only_reset_residual':float(reset_res),'physical_command_edge_residual':float(edge_res),'schedule':schedule,'total_elapsed_time':sum(t for _,t in schedule),'final_unfinished_probability':unfinished,'uniform_Gramian_tail_bound':float(bound),'final_DATA_reference_trace_norm_error':err,'reissued_absolute_target_stationarity_residual':absolute}
Path(__file__).with_name('reusable_clock_checks.json').write_text(json.dumps(outdict,indent=2)+'\n');print(json.dumps(outdict,indent=2))
