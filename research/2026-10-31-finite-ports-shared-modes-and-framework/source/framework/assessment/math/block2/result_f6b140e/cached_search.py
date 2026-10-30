"""Reuse the already constructed exact-coefficient affine SOS system numerically."""
import numpy as np
import sys,json,pathlib
base=pathlib.Path(__file__).parent
data=np.load(base/'sos_search_system.npz')
A=data['A'];nu=float(sys.argv[1]);b=data['b0']+nu*data['b1']
sizes=[5,4,3,2,1]
entries=[(k,i,j) for k,n in enumerate(sizes) for i in range(n) for j in range(i,n)]
weights=np.array([1 if i==j else 2**.5 for k,i,j in entries]+[1]*5)
At=A/weights;pi=np.linalg.pinv(At,rcond=1e-10)
pa=lambda v:v+pi@(b-At@v)
def pp(v):
    ans=v.copy();off=0
    for n in sizes:
        ma=np.zeros((n,n));ids=[]
        for i in range(n):
            for j in range(i,n):
                idx=off;off+=1;ma[i,j]=ma[j,i]=v[idx]/weights[idx];ids.append((idx,i,j))
        lam,U=np.linalg.eigh(ma);pos=(U*np.maximum(lam,0))@U.T
        for idx,i,j in ids:ans[idx]=pos[i,j]*weights[idx]
    return ans
v=np.zeros(A.shape[1])
for it in range(40000):
    av=pa(v);v+=pp(2*av-v)-av
    if it%1000==0 and np.linalg.norm(av-pp(av))<1e-10:break
av=pa(v);error=np.linalg.norm(av-pp(av));out=av/weights
print('nu',nu,'iteration',it,'error',error,'parameters',out[-5:])
names=list(json.loads((base/'sos_search_0.2_result.json').read_text())['unknowns'])
(base/f'cached_{nu}_result.json').write_text(json.dumps(dict(nu=nu,error=float(error),unknowns=dict(zip(names,map(float,out)))),indent=2))
