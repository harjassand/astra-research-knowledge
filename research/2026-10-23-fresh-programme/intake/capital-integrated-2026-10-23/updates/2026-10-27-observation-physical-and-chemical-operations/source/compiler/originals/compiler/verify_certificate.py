"""Independent exact primal/dual verifier; standard library only."""
from fractions import Fraction as F
import json,sys
from pathlib import Path


def verify(d):
    K=[[F(v) for v in row] for row in d['K']]
    L=[[F(v) for v in row] for row in d['L']]
    U=[[F(v) for v in row] for row in d['U']]
    ny,nx,nz=len(K),len(K[0]),len(L);q=F(d['q'])
    assert ny and nx and nz and 0<=q<=1
    assert all(len(row)==nx for row in K+L)
    assert len(U)==ny and all(len(row)==nz for row in U)
    assert all(v>=0 for row in K+L+U for v in row)
    assert all(sum(K[y][x] for y in range(ny))==1 for x in range(nx))
    assert all(sum(L[z][x] for z in range(nz))==1 for x in range(nx))
    sums=[sum(U[y][z] for y in range(ny)) for z in range(nz)]
    assert all(v<=1 for v in sums)
    D=[[K[y][x]-sum(U[y][z]*L[z][x] for z in range(nz)) for x in range(nx)] for y in range(ny)]
    assert all(v>=0 for row in D for v in row)
    qx=[1-sum(sums[z]*L[z][x] for z in range(nz)) for x in range(nx)]
    assert all(0<=v<=q for v in qx)
    assert all(sum(D[y][x] for y in range(ny))==qx[x] for x in range(nx))
    weights={e['constraint']:F(e['weight']) for e in d['dual']}
    assert len(weights)==len(d['dual']) and all(v>=0 for v in weights.values())
    allowed={f'column_{z}' for z in range(nz)}|{f'output_{y}_{x}' for y in range(ny) for x in range(nx)}|{f'query_{x}' for x in range(nx)}
    assert weights.keys()<=allowed
    beta=[weights.get(f'column_{z}',F(0)) for z in range(nz)]
    alpha=[[weights.get(f'output_{y}_{x}',F(0)) for x in range(nx)] for y in range(ny)]
    pi=[weights.get(f'query_{x}',F(0)) for x in range(nx)]
    assert sum(pi)<=1
    for y in range(ny):
        for z in range(nz):
            assert beta[z]+sum((alpha[y][x]-pi[x])*L[z][x] for x in range(nx))>=0
    lower=sum(pi)-sum(beta)-sum(alpha[y][x]*K[y][x] for y in range(ny) for x in range(nx))
    assert lower==q
    if q:assert sum(pi)==1
    # Exact identity: nonquery UL plus the raw-read residual is K, entrywise.
    assert all(sum(U[y][z]*L[z][x] for z in range(nz))+D[y][x]==K[y][x] for y in range(ny) for x in range(nx))
    return {'primal_feasible':True,'dual_feasible':True,'equal_objectives':True,
            'q_by_input':[str(v) for v in qx],'residual':[[str(v) for v in row] for row in D],
            'least_favorable_input':[str(v) for v in pi] if q else None}


if __name__=='__main__':
    print(json.dumps(verify(json.loads(Path(sys.argv[1]).read_text())),indent=2))
