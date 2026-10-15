#!/usr/bin/env python3
"""Reconstruct the finite Theta/T map in Pedregal 1905.06571v5.

Produces valid periodic P1 maps on exactly the stated three-normal mesh.
This is a proof-step audit, not a search for a ROC/non-QC integrand.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools, json, random
import sympy as S
from sympy.solvers.simplex import linprog, InfeasibleLPError

HERE=Path(__file__).resolve().parent

def mesh(n):
    triangles=[]
    for i in range(n):
        for j in range(n):
            triangles += [[(i,j),(i+1,j),(i,j+1)],
                          [(i+1,j+1),(i,j+1),(i+1,j)]]
    edges={}
    for s,vertices in enumerate(triangles):
        for p,q in itertools.combinations(vertices,2):
            dx,dy=q[0]-p[0],q[1]-p[1]
            normal=0 if dx==0 else 1 if dy==0 else 2
            key=(normal,(p[0]+q[0])%(2*n),(p[1]+q[1])%(2*n))
            edges.setdefault(key,[]).append(s)
    assert all(len(v)==2 for v in edges.values())
    assert len(edges)==3*len(triangles)//2
    return triangles,edges

def gradients(n,values):
    node=lambda i,j:values[(i%n)*n+(j%n)]
    result=[]
    for i in range(n):
        for j in range(n):
            result += [(n*(node(i+1,j)-node(i,j)),n*(node(i,j+1)-node(i,j))),
                       (n*(node(i+1,j+1)-node(i,j+1)),n*(node(i+1,j+1)-node(i+1,j)))]
    assert tuple(map(sum,zip(*result)))==(0,0)
    return result

def make_mold(edges,rng):
    groups=[]
    for normals in [(0,1),(0,2),(1,2)]:
        group=[key for key in edges if key[0] in normals]
        rng.shuffle(group)
        groups.append(group)
    leaves=[]
    for group in groups:
        for key in group:leaves.extend(edges[key])
    return groups,leaves

def theta_equations(leaves,nt):
    size=len(leaves);rows=[];rhs=[]
    for i in range(size//2):
        row=[0]*size;row[2*i]=row[2*i+1]=1;rows.append(row);rhs.append(F(1,3*nt))
    for s in range(nt):
        row=[int(v==s) for v in leaves];assert sum(row)==6;rows.append(row);rhs.append(F(1,nt))
    return rows,rhs

def node_maps(groups,leaves,grad):
    """Each node's barycenter is linear in the leaf weights.

    Pair sums are fixed by Theta; all higher relative weights are fixed.
    The lowest direction (difference of adjacent fixed gradients) is
    automatic and is not part of the variable parallelism equations.
    """
    size=len(leaves);nt=len(grad);nodes=[];roots=[];offset=0
    for group in groups:
        level=[]
        for _ in group:
            mx=[F(0)]*size;my=[F(0)]*size
            for col in [offset,offset+1]:
                mx[col]=3*nt*grad[leaves[col]][0]
                my[col]=3*nt*grad[leaves[col]][1]
            level.append((mx,my));offset+=2
        while len(level)>1:
            next_level=[]
            for odd,even in zip(level[::2],level[1::2]):
                nodes.append(([b-a for a,b in zip(odd[0],even[0])],
                              [b-a for a,b in zip(odd[1],even[1])]))
                next_level.append(([F(a+b,2) for a,b in zip(odd[0],even[0])],
                                   [F(a+b,2) for a,b in zip(odd[1],even[1])]))
            level=next_level
        roots.append(level[0])
    mean12=([F(a+b,2) for a,b in zip(roots[0][0],roots[1][0])],
            [F(a+b,2) for a,b in zip(roots[0][1],roots[1][1])])
    nodes.append(([b-a for a,b in zip(roots[0][0],roots[1][0])],
                  [b-a for a,b in zip(roots[0][1],roots[1][1])]))
    nodes.append(([b-a for a,b in zip(mean12[0],roots[2][0])],
                  [b-a for a,b in zip(mean12[1],roots[2][1])]))
    return nodes,roots

def evaluate(node,weights):
    return tuple(sum(a*b for a,b in zip(row,weights)) for row in node)

def feasible_weights(groups,leaves,edges,nt,rng):
    base=F(1,6*nt);t=[base]*len(leaves)
    occurrences={key:[] for key in edges}
    offset=0
    for group in groups:
        for key in group:
            occurrences[key].append(offset);offset+=2
    for key,cols in occurrences.items():
        assert len(cols)==2
        delta=base*F(rng.choice([-2,-1,0,1,2]),3)
        a,b=cols
        t[a]+=delta;t[a+1]-=delta;t[b]-=delta;t[b+1]+=delta
    assert min(t)>0
    return t

def svalue(q):return str(q.numerator) if q.denominator==1 else f'{q.numerator}/{q.denominator}'

def trial(n,seed):
    rng=random.Random(seed)
    triangles,edges=mesh(n);nt=len(triangles)
    groups,leaves=make_mold(edges,rng)
    uv=[rng.randrange(-7,8) for _ in range(n*n)]
    vv=[rng.randrange(-7,8) for _ in range(n*n)]
    gu,gv=gradients(n,uv),gradients(n,vv)
    t=feasible_weights(groups,leaves,edges,nt,rng)
    theta,rhs=theta_equations(leaves,nt)
    assert all(sum(F(a)*b for a,b in zip(row,t))==v for row,v in zip(theta,rhs))
    unodes,uroots=node_maps(groups,leaves,gu)
    vnodes,vroots=node_maps(groups,leaves,gv)
    rows=list(theta)
    for unode,vnode in zip(unodes,vnodes):
        ux,uy=evaluate(unode,t)
        rows.append([ux*y-uy*x for x,y in zip(vnode[0],vnode[1])]);rhs.append(F(0))
    A=S.Matrix(rows);b=S.Matrix(rhs)
    contradiction=None
    for y in A.T.nullspace():
        value=(y.T*b)[0]
        if value!=0:
            y=-y/value
            assert y.T*A==S.zeros(1,A.cols) and (y.T*b)[0]==-1
            contradiction=[str(q) for q in y]
            break
    if contradiction is not None:
        lp_status,lp_message=2,'Exact inconsistent linear equations; left-null certificate saved.'
    else:
        try:
            optimum,solution=linprog([0]*len(leaves),A_eq=A,b_eq=b)
            lp_status,lp_message=0,'Exact nonnegative solution found.'
        except InfeasibleLPError:
            lp_status,lp_message=2,'Exact simplex infeasible; a separate certificate is still required.'
    record={'n':n,'l':n.bit_length()-1,'seed':seed,'u_nodal_values':uv,'v_nodal_values':vv,
            'groups':[[list(k) for k in group] for group in groups],
            'triangles':triangles,'leaves':leaves,'weights_t':[svalue(q) for q in t],
            'u_group_barycenters':[[svalue(q) for q in evaluate(node,t)] for node in uroots],
            'rows':[[svalue(F(q)) for q in row] for row in rows],
            'rhs':[svalue(q) for q in rhs],
            'lp_status':lp_status,'lp_message':lp_message,
            'left_null_certificate':contradiction,
            'rows_count':len(rows),'variables':len(leaves)}
    return record

if __name__=='__main__':
    diagnostics=[]
    for n in [2,4]:
        for seed in range(1,21):
            record=trial(n,seed)
            diagnostics.append({k:record[k] for k in ['n','seed','lp_status','rows_count','variables']})
            if record['lp_status']==2:
                (HERE/'PEDREGAL_MAP_CANDIDATE.json').write_text(json.dumps(record,indent=2)+'\n')
                (HERE/'PEDREGAL_MAP_DISCOVERY_LOG.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
                print(json.dumps({k:record[k] for k in ['n','seed','lp_status','u_group_barycenters','rows_count','variables']},indent=2))
                raise SystemExit(0)
    (HERE/'PEDREGAL_MAP_DISCOVERY_LOG.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    print('No floating infeasible map instance in recorded trials; this is not a proof.')
