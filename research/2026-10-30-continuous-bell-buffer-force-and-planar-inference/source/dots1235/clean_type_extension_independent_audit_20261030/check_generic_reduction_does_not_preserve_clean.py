"""A generic reducing extension need not preserve a second clean range.
The actual native proof needs its stronger complete tag-source structure.
"""
import numpy as np,json
from pathlib import Path
I=np.eye(4);F=np.diag([1.,1.,0.,0.]);G=np.diag([1.,0.,1.,0.]);B=I-G
J=np.zeros((4,4));J[0,2]=J[2,2]=J[0,3]=1/np.sqrt(2);J[2,3]=-1/np.sqrt(2)
Jd=F@J@F+(I-F)@J@(I-F)
def Lstar(j,O):
 gam=j.T@j;return j.T@O@j-(gam@O+O@gam)/2
norm=lambda x:float(np.linalg.norm(x,2))
out={'original_clean_range_creation':norm(B@J@G),'original_FREE_range_creation':norm((I-F)@J@F),'original_loss_clean_commutator':norm(J.T@J@G-G@J.T@J),'reduced_jump_clean_creation':norm(B@Jd@G),'reduced_loss_clean_commutator':norm(Jd.T@Jd@G-G@Jd.T@Jd),'reduced_bad_effect_clean_cross':norm(G@Lstar(Jd,B)@B),'scope':'generic negative example only; native source-resolved complete tag losses have extra structure'}
assert out['original_clean_range_creation']<1e-12 and out['original_FREE_range_creation']<1e-12 and out['original_loss_clean_commutator']<1e-12
assert out['reduced_loss_clean_commutator']>.4 and out['reduced_bad_effect_clean_cross']>.2
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
