import itertools,json,math,numpy as np
from pathlib import Path
here=Path(__file__).parent
fs=[]
for a in range(3):
 for s in [-1,1]:
  f=np.zeros(4);f[0]=1;f[a+1]=3*s;fs.append(f)
A=np.zeros((16,16));B=np.zeros((9,9));norms=[]
for fi,fj,z in itertools.product(fs,fs,range(9)):
 v=np.kron(fi,fj);X=np.zeros((16,9));X[:,z]=9*v
 A+=X@X.T/324;B+=X.T@X/324;norms.append(np.linalg.norm(X,2))
D=np.diag([1,3,3,3]);assert np.linalg.norm(A-81*np.kron(D,D))<1e-10;assert np.linalg.norm(B-900*np.eye(9))<1e-10
ell=math.log(25*3/.05);m=1000000;e=(31*ell+math.sqrt((31*ell)**2+1800*m*ell))/m
out={'matrix_norm_max':max(norms),'row_moment_residual':float(np.linalg.norm(A-81*np.kron(D,D))),'column_moment_residual':float(np.linalg.norm(B-900*np.eye(9))),'fixed_endpoint_m':m,'delta':.05,'operator_radius':e,'old_entrywise_radius':12*math.sqrt(220*math.log(288*3/.05)/m),'tail_at_radius':25*3*math.exp(-m*e*e/(2*(900+31*e)))}
def polar(A):
 U,s,V=np.linalg.svd(A);return U@np.diag([1,1,np.linalg.det(U@V)])@V
if (here/'actual_bank_counters.npz').exists():
 f=np.load(here/'actual_bank_counters.npz');out['empirical_edges']=[]
 for i,S in enumerate(f['sums']):
  M=S/m-f['Jembed'];u,s,vt=np.linalg.svd(M);s1,s2=s[-1],s[-2];v=vt[-1];alpha=math.sqrt(max(0,(e*e-s1*s1)/(s2*s2-s1*s1)));h=math.sqrt(2-2*math.sqrt(1-alpha*alpha));AA=math.sqrt(3)*v.reshape(3,3);Rp,Rm=polar(AA),polar(-AA);rp=np.linalg.norm(Rp-AA);rm=np.linalg.norm(Rm+AA);chosen=Rp if rp<=rm else Rm;rw=max(rp,rm);assert s1<=e<s2 and min(rp,rm)<=math.sqrt(3)*h;bound=min(rp,rm)+math.sqrt(3)*h
  out['empirical_edges'].append({'edge':[i+1,0],'s1':float(s1),'s2':float(s2),'gap_lower':float(s2-e),'cone_alpha':alpha,'wrong_polar_distance':float(rw),'cone_radius_unscaled':math.sqrt(3)*h,'sign_certified':bool(rw>math.sqrt(3)*h),'frame_F_bound':float(bound),'diagnostic_true_frame_F_error':float(np.linalg.norm(chosen-f['O'][i+1]@f['O'][0].T))})
print(json.dumps(out,indent=2))
