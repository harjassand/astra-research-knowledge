"""Own exact F2 cellular-chain checker; no trajectories or external dependencies."""
import itertools, json, time

def xoradd(out, cell):
    if cell in out: out.remove(cell)
    else: out.add(cell)

def boundary(chain,L):
    out=set()
    for x,axes in chain:
        for a in axes:
            rem=tuple(i for i in axes if i!=a)
            y=list(x);y[a]=(y[a]+1)%L
            xoradd(out,(x,rem));xoradd(out,(tuple(y),rem))
    return out

def project_cell(cell,L):
    x,axes=cell
    if any(x[a]!=L-1 for a in axes): return set()
    choices=[range(L) if a in axes else [0] for a in range(4)]
    return {(tuple(y),axes) for y in itertools.product(*choices)}

def project(chain,L):
    out=set()
    for c in chain:
        for d in project_cell(c,L): xoradd(out,d)
    return out

def homotopy(chain,L):
    out=set()
    for x,axes in chain:
        for j in range(4):
            if j in axes or any(x[a]!=L-1 for a in axes if a<j): continue
            choices=[]
            for a in range(4):
                if a<j: choices.append(range(L) if a in axes else [0])
                elif a==j: choices.append(range(x[j]))
                else: choices.append([x[a]])
            newaxes=tuple(sorted(axes+(j,)))
            for y in itertools.product(*choices): xoradd(out,(tuple(y),newaxes))
    return out

def parity_cuts(chain,L):
    # p tensor factors: each edge factor uses the seam edge L-1.
    out=set()
    for x,axes in chain:
        if all(x[a]==L-1 for a in axes): xoradd(out,axes)
    return out

def cells(L,k):
    for x in itertools.product(range(L),repeat=4):
        for axes in itertools.combinations(range(4),k): yield (x,axes)

def check(L):
    count={};start=time.monotonic()
    for k in (0,1,2):
        n=0
        for c in cells(L,k):
            C={c}
            left=boundary(homotopy(C,L),L)^homotopy(boundary(C,L),L)
            assert left==C^project(C,L),(L,k,c,'contraction')
            assert not boundary(boundary(C,L),L)
            if k==2:
                z=boundary(C,L)
                assert boundary(homotopy(z,L),L)==z
                assert parity_cuts(C^homotopy(z,L),L)==parity_cuts(C,L)
            n+=1
        count[str(k)]=n
    for c in cells(L,3):
        assert not parity_cuts(boundary({c},L),L)
    for axes in itertools.combinations(range(4),2):
        sheet={(x,axes) for x in itertools.product(range(L),repeat=4)
               if all(x[a]==0 for a in range(4) if a not in axes)}
        assert not boundary(sheet,L)
        assert parity_cuts(sheet,L)=={axes}
        for ai,aj in itertools.product(range(L),repeat=2):
            assert sum(x[axes[0]]==ai and x[axes[1]]==aj for x,a in sheet)%2==1
    # Two individually nonbounding winding loops, jointly a boundary.
    strip={((i,0,0,0),(0,1)) for i in range(L)}
    z=boundary(strip,L)
    assert z and not parity_cuts(z,L)
    assert boundary(homotopy(z,L),L)==z
    return {'L':L,'basis_identity_checks':count,'cube_boundary_checks':4*L**4,
            'logical_sheet_checks':6,'global_H_only_single_face_logical_failures':6*L**2,'seconds':time.monotonic()-start,'status':'PASS'}

if __name__=='__main__':
    print(json.dumps({'checks':[check(L) for L in (2,3,4)]},indent=2))
