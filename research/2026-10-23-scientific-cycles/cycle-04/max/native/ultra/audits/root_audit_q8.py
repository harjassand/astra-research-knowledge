#!/usr/bin/env python3
"""Independent exact-inverse audit of the physical 8-dimensional cone witness.

Unlike the discovery certificate, this computes the actual Cayley unitary and
its Gram by Fraction complex arithmetic. No perturbation estimate or NumPy.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse, json, time, resource

ZERO=(F(0),F(0)); ONE=(F(1),F(0))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def conj(a): return (a[0],-a[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
    d=b[0]*b[0]+b[1]*b[1]
    r=mul(a,conj(b));return(r[0]/d,r[1]/d)
def total(xs):
    out=ZERO
    for x in xs: out=add(out,x)
    return out

def main(inputs,output):
    cpu,wall=time.process_time(),time.perf_counter()
    data=json.loads(Path(inputs).read_text()); q=8; P=data['P']
    A=[[(F(data['Ar'][i][j],P),F(data['Ai'][i][j],P)) for j in range(q)] for i in range(q)]
    assert all(A[i][j]==neg(conj(A[j][i])) for i in range(q) for j in range(q))
    I=[[ONE if i==j else ZERO for j in range(q)] for i in range(q)]
    # Solve (I-A)U=(I+A) directly, with exact nonzero pivoting.
    aug=[[sub(I[i][j],A[i][j]) for j in range(q)]+[add(I[i][j],A[i][j]) for j in range(q)] for i in range(q)]
    for k in range(q):
        p=next(i for i in range(k,q) if aug[i][k]!=ZERO)
        aug[k],aug[p]=aug[p],aug[k]
        pivot=aug[k][k];aug[k]=[div(x,pivot) for x in aug[k]]
        for i in range(q):
            if i==k: continue
            scale=aug[i][k]
            aug[i]=[sub(aug[i][j],mul(scale,aug[k][j])) for j in range(2*q)]
    U=[row[q:] for row in aug]
    assert all(total(mul(conj(U[k][i]),U[k][j]) for k in range(q))==I[i][j] for i in range(q) for j in range(q))
    G=[[F(0) for _ in range(q)] for _ in range(q)]
    for bit in range(3):
        inds=[[v for v in range(q) if ((v>>bit)&1)==s] for s in range(2)]
        rho=[[[total(mul(U[inds[s][a]][j],conj(U[inds[s][b]][j])) for s in range(2)) for b in range(4)] for a in range(4)] for j in range(q)]
        for j in range(q):
            for k in range(q):
                v=total(mul(rho[j][a][b],rho[k][b][a]) for a in range(4) for b in range(4))
                assert v[1]==0
                G[j][k]+=v[0]/2
    assert all(sum(row)==3 for row in G)
    Y=data['Y']; W=[[sum(Y[i][a]*Y[j][a] for a in range(4)) for j in range(q)] for i in range(q)]
    tr=sum(W[i][i] for i in range(q)); assert tr>0
    actual=sum(W[i][j]*G[i][j] for i in range(q) for j in range(q))/tr
    edges=[(i,i^(1<<b)) for i in range(q) for b in range(3) if i<(i^(1<<b))]
    graphs=set(); maximum=None
    for perm in permutations(range(q)):
        graph=tuple(sorted(tuple(sorted((perm[i],perm[j]))) for i,j in edges))
        if graph in graphs: continue
        graphs.add(graph); value=sum(W[i][j] for i,j in graph)
        maximum=value if maximum is None else max(maximum,value)
    assert len(graphs)==840
    support=F(3,2)+F(maximum,tr)
    gap=actual-support
    assert gap>F(1,500)
    result={'status':'PASS_INDEPENDENT_EXACT_INVERSE',
      'unitarity':'U*U=I checked exactly entrywise',
      'common_Gram':'actual exact Cayley column-projector reductions; row sums 3 checked',
      'reference_orbit_size':840,'permutations':40320,
      'gap_over_ln2':str(gap),'gap_diagnostic':float(gap),
      'claim':'every common DS mixture requires kappa > ln(2)/500',
      'float_input_used':False,'perturbation_bound_used':False,
      'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
      'maxrss_platform_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--inputs',default=str(Path(__file__).with_name('cone_challenge')/'EXACT_INPUTS.json'))
    p.add_argument('--output',default=str(Path(__file__).with_name('ROOT_EXACT_AUDIT.json')))
    a=p.parse_args();main(a.inputs,a.output)
