import numpy as np,json,math
from scipy.linalg import expm
rng=np.random.default_rng(202610294)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);pa=[X,Y,Z]
def kron(xs):
 r=np.ones((1,1),complex)
 for x in xs:r=np.kron(r,x)
 return r
def rot():
 q=rng.normal(size=4);q/=np.linalg.norm(q);v=q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3));return np.array([[np.trace(pa[a]@v@pa[b]@v.conj().T).real/2 for b in range(3)] for a in range(3)])
def swap(c):return (np.eye(4)+sum(c[a,b]*np.kron(pa[a],pa[b]) for a in range(3) for b in range(3)))/2
def effect(ks,S,D=4):
 SS=np.kron(S,I);G=sum((k@SS-SS@k).conj().T@(k@SS-SS@k) for k in ks)/(2*D)
 return np.trace(G.reshape(D,2,D,2),axis1=0,axis2=2)
max_res=-1e9;tri_res=-1e9;sum_cur=sum_star=sum_A=0.
for trial in range(64):
 z=rng.normal(size=(40,8))+1j*rng.normal(size=(40,8));q,_=np.linalg.qr(z);ks=q.reshape(5,8,8)
 c=rot();ct=rot();S=swap(c);St=swap(ct)
 z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));sigma=z@z.conj().T;sigma/=np.trace(sigma)
 dc=np.trace(sigma@effect(ks,S)).real;dt=np.trace(sigma@effect(ks,St)).real;aa=4.5*np.linalg.norm(c-ct)**2
 diff=np.trace(sigma@effect(ks,S-St)).real
 assert diff<=aa+1e-11
 tri_res=max(tri_res,np.sqrt(dc)-np.sqrt(dt)-np.sqrt(aa))
 for gamma in [.01,.1,1.,10.]:max_res=max(max_res,dc-(1+gamma)*dt-(1+1/gamma)*aa)
 sum_cur+=dc;sum_star+=dt;sum_A+=aa
assert max_res<1e-10 and tri_res<1e-10
aggregate_bound=(np.sqrt(sum_star)+np.sqrt(sum_A))**2
assert sum_cur<=aggregate_bound+1e-10
# A channel perfect on the full four-spin singlet code but bad for the star-loss objective.
n=4;D=16;ops=[[kron([p if k==i else I for k in range(n)]) for i in range(n)] for p in pa]
J=[sum(xx)/2 for xx in ops];ev,vec=np.linalg.eigh(sum(j@j for j in J));E=vec[:,ev<1e-9];P=E@E.conj().T;Q=np.eye(D)-P
H=Q@ops[0][0]@Q;U=expm(-1j*.8*H)
losses=[]
for i in range(1,n):
 S=(np.eye(D)+sum(ops[a][0]@ops[a][i] for a in range(3)))/2
 losses.append(np.linalg.norm(U@S-S@U)**2/(2*D))
raw=1-abs(np.trace(E.conj().T@U@E)/E.shape[1])**2
assert abs(raw)<1e-12 and sum(losses)>.01
near_res=-1e9;coherent_effect_res=-1e9
for trial in range(32):
 nu=.001+.1*rng.random();angle=.001+.1*rng.random()
 U0=expm(-1j*(.7*np.kron((np.kron(Z,I)+np.kron(I,Z))/2,Z)+.2*np.kron(np.eye(4),X)))
 U=expm(-1j*nu*np.kron(np.kron(X,I),Z))@U0
 vv=expm(-.5j*angle*Y);c=np.array([[np.trace(pa[a]@vv@pa[b]@vv.conj().T).real/2 for b in range(3)] for a in range(3)])
 z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));sigma=z@z.conj().T;sigma/=np.trace(sigma)
 ee=effect([U],swap(np.eye(3)));dt=np.trace(sigma@ee).real;dc=np.trace(sigma@effect([U],swap(c))).real
 aa=4.5*np.linalg.norm(c-np.eye(3))**2
 near_res=max(near_res,np.sqrt(dc)-np.sqrt(dt)-np.sqrt(aa))
 coherent_effect_res=max(coherent_effect_res,np.linalg.eigvalsh(ee-2*nu**2*I).max())
assert near_res<1e-10 and coherent_effect_res<1e-10
result=dict(near_collective_fixtures=32,max_near_triangle_residual=near_res,max_coherent_budget_operator_residual=coherent_effect_res,random_joint_CPTP_fixtures=64,max_weighted_gamma_residual=max_res,max_triangle_residual=tri_res,aggregate_loss=sum_cur,aggregate_bound=aggregate_bound,perfect_code_counterexample=dict(raw_Bell_loss=raw,star_loss_sum=sum(losses),star_losses=losses),scope='Numerical diagnostics of analytic inequalities, not an operational noisy-code simulation or proof of novelty.')
print(json.dumps(result,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')
