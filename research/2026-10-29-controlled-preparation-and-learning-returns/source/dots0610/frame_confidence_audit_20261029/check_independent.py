import numpy as np,math,json
from pathlib import Path
p=Path('producer-workspace/sharpened_frame_confidence_20261029');r=Path(__file__).parent
F=np.array([[1]+[3*s if b==a else 0 for b in range(3)] for a in range(3) for s in [-1,1]])
VV=np.array([np.kron(x,y) for x in F for y in F]);A=81*VV.T@VV/36;B=np.eye(9)*81*np.mean(np.sum(VV*VV,axis=1))/9
assert np.max(np.linalg.eigvalsh(A))==729 and np.max(np.linalg.eigvalsh(B))==900
m=10**6;delta=.05;E=3;L=math.log(25*E/delta)
def radius(R):return ((R/3)*L+math.sqrt(((R/3)*L)**2+1800*m*L))/m
e=radius(93);bank=np.load(p/'actual_bank_counters.npz');rows=[]
for S in bank['sums']:
 M=S/m-bank['Jembed'];_,sv,Vt=np.linalg.svd(M);s1,s2=sv[-1],sv[-2]
 assert s1<=e<s2
 alpha2=(e*e-s1*s1)/(s2*s2-s1*s1);h=math.sqrt(2-2*math.sqrt(1-alpha2));A=math.sqrt(3)*Vt[-1].reshape(3,3)
 rs=[]
 for sign in [1,-1]:
  U,s,V=np.linalg.svd(sign*A);R=U@np.diag([1,1,np.linalg.det(U@V)])@V;rs.append(float(np.linalg.norm(R-sign*A)))
 feasible=[i for i,a in enumerate(rs) if a<=math.sqrt(3)*h]
 assert len(feasible)==1
 rows.append({'s1':s1,'s2':s2,'gap_lower':s2-e,'branch_distances':rs,'feasible_signs':[1 if i==0 else -1 for i in feasible],'confidence_F_bound':min(rs)+math.sqrt(3)*h})
out={'ideal_radius':e,'safe_R180_radius':radius(180),'input16_output9_moment_bounds':[729,900],'edge_results':rows,'uses_true_frame':False,'scope':'fixed endpoint and ideal trusted interface; structural kernel promise conditional'}
(r/'independent_confidence.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
