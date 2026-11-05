"""Regression for the independently discovered near-rotation chart defect."""
from pathlib import Path
import json,math
import numpy as np
from scipy.linalg import expm
from gradient_rotation import shape_distance,rotation,E,J

rows=[]
angles=[-math.pi,-.7,-1e-3,-1e-6,-1e-9,0.,1e-9,1e-6,1e-3,.7,math.pi]
for exponent in range(2,15):
    q=10.**(-exponent)
    for theta in angles:
        u=math.hypot(1.,q)*complex(math.cos(theta),math.sin(theta))
        v=q*complex(math.cos(.6),math.sin(.6))
        N=np.array([[u.real+v.real,v.imag-u.imag],
                    [v.imag+u.imag,u.real-v.real]])
        p=shape_distance(N)
        d,w,alpha=p['distance'],p['w'],p['alpha']
        found=rotation(alpha+w)@expm(-(d*E+w*J))@rotation(-alpha)
        error=float(np.linalg.norm(found-N))
        rows.append({'q_requested':q,'theta_requested':theta,'q_recovered':p['q'],
                     'branch':p['branch'],'distance':d,'endpoint_error_Frobenius':error})
        assert error<2e-11,rows[-1]
out={'status':'Executed floating regression, not rigorous interval arithmetic',
     'preserved_defect':'Direct delta root and sin(delta) division gave ~0.01 endpoint error at q=1e-12,theta=.7 in the independent audit.',
     'repair':'Rescaled epsilon=pi-delta=qz chart; old tiny-q substitution removed.',
     'cases':rows,'maximum_endpoint_error_Frobenius':max(r['endpoint_error_Frobenius'] for r in rows)}
Path(__file__).with_name('near_rotation_regression_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'cases':len(rows),'maximum_endpoint_error_Frobenius':out['maximum_endpoint_error_Frobenius']},indent=2))
