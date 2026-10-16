"""Own separable dense F2 readout checker; standard library only."""
import itertools, json, random, time
from check_tensor_readout import boundary, homotopy, cells

def dense_H(z,L):
    N=L**4; strides=[L**(3-a) for a in range(4)]
    edge=[[0]*N for _ in range(4)]
    def index(x): return sum(x[a]*strides[a] for a in range(4))
    for x,axes in z: edge[axes[0]][index(x)]^=1
    result={ij:[0]*N for ij in itertools.combinations(range(4),2)}
    def axis_map(arr,a,kind):
        step=strides[a];out=[0]*N
        for base in range(N):
            if (base//step)%L: continue
            if kind=='vertex':
                v=0
                for t in range(L): v^=arr[base+t*step]
                out[base]=v
            elif kind=='edge':
                v=arr[base+(L-1)*step]
                for t in range(L): out[base+t*step]=v
            else:
                v=0
                for t in range(L-1,-1,-1):
                    out[base+t*step]=v
                    v^=arr[base+t*step]
        return out
    for k in range(4):
        for j in range(4):
            if j==k: continue
            a=edge[k]
            for ell in range(j): a=axis_map(a,ell,'edge' if ell==k else 'vertex')
            a=axis_map(a,j,'h')
            out=result[tuple(sorted((j,k)))]
            for n in range(N): out[n]^=a[n]
    out=set()
    for ij,a in result.items():
        for n,b in enumerate(a):
            if b: out.add((tuple((n//strides[k])%L for k in range(4)),ij))
    return out

if __name__=='__main__':
    results=[]
    for L in (2,3,4):
        start=time.monotonic();count=0
        for c in cells(L,1):
            assert dense_H({c},L)==homotopy({c},L)
            count+=1
        results.append({'L':L,'all_basis_edges_compared':count,'seconds':time.monotonic()-start,'status':'PASS'})
    rng=random.Random(20261015);L=16;start=time.monotonic()
    faces=list(itertools.combinations(range(4),2));E=set()
    for _ in range(2000):
        c=(tuple(rng.randrange(L) for _ in range(4)),rng.choice(faces))
        if c in E:E.remove(c)
        else:E.add(c)
    z=boundary(E,L);D=dense_H(z,L)
    assert boundary(D,L)==z
    results.append({'L':L,'seed':20261015,'face_proposals':2000,'syndrome_edges':len(z),'output_faces':len(D),'seconds':time.monotonic()-start,'status':'PASS'})
    print(json.dumps(results,indent=2))
