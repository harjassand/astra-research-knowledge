import numpy as np
import json

def make(k,s0=2):
    verts=[(i,x,y) for i in range(k+1) for x in range(s0*2**i) for y in range(s0*2**i)]
    index={v:j for j,v in enumerate(verts)}
    A=np.zeros((len(verts),len(verts)),dtype=np.int64)
    for v,j in index.items():
        i,x,y=v;s=s0*2**i
        nb=[((x+2*y)%s,y),((x-2*y)%s,y),((x+2*y+1)%s,y),((x-2*y-1)%s,y),
            (x,(y+2*x)%s),(x,(y-2*x)%s),(x,(y+2*x+1)%s),(x,(y-2*x-1)%s)]
        for a,b in nb:A[j,index[(i,a,b)]]+=1
        if i<k:
            for a in range(2):
                for b in range(2):
                    l=index[(i+1,x+a*s,y+b*s)]
                    A[j,l]+=1;A[l,j]+=1
    assert np.array_equal(A,A.T)
    for j in range(len(verts)):A[j,j]+=13-A[j].sum()
    assert np.all(A.sum(axis=1)==13)
    return verts,index,A
out=[]
for k in range(4):
    v,ix,A=make(k)
    P=(A+13*np.eye(len(v)))/26
    vals=np.linalg.eigvalsh(P)
    item={'k':k,'n':len(v),'lazy_lambda2':float(vals[-2]),'lazy_min_eigenvalue':float(vals[0])}
    if k:
        ov,oi,OA=make(k-1);s=2*2**(k-1)
        pi=[oi[(i,x,y)] if i<k else oi[(k-1,x%s,y%s)] for i,x,y in v]
        for a,b in zip(*np.nonzero(A)):
            assert OA[pi[a],pi[b]]>0
        item['base_retraction_checked']=True
        # Fixed small powers test the support argument; production L stays symbolic.
        oldpow=np.linalg.matrix_power(OA+13*np.eye(len(ov),dtype=np.int64),3)
        newpow=np.linalg.matrix_power(A+13*np.eye(len(v),dtype=np.int64),3)
        for a,b in zip(*np.nonzero(newpow)):
            assert oldpow[pi[a],pi[b]]>0
        item['power3_retraction_checked']=True
    out.append(item)
print(json.dumps(out,indent=2))
