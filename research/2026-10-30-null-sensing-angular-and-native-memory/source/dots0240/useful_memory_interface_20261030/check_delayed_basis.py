import json
import numpy as np
out=[]
for k in range(1,7):
    d=2**k
    H=np.array([[(-1)**((i&j).bit_count())/np.sqrt(d) for j in range(d)] for i in range(d)])
    povm_sum=np.zeros((d,d))
    score=0.0
    for z in range(d):
        ez=np.eye(d)[:,z]
        for x in range(d):
            hx=H[:,x]
            psi=(ez+np.sign(H[z,x])*hx)/np.sqrt(2*(1+1/np.sqrt(d)))
            M=np.outer(psi,psi)/d
            povm_sum+=M
            score+=(ez@M@ez+hx@M@hx)/(2*d)
    target=(1+1/np.sqrt(d))/2
    out.append(dict(k=k,d=d,povm_error=float(np.linalg.norm(povm_sum-np.eye(d))),score=score,target=target,passed=bool(np.allclose(povm_sum,np.eye(d)) and abs(score-target)<1e-10)))
assert all(r['passed'] for r in out)
print(json.dumps(out,indent=2))
