#!/usr/bin/env python3
"""Independent exact-rational audit. Writes only this worker's result file.

The reference solve and projection matrix are Fraction Gaussian elimination,
independent of SciPy and Decimal residual arithmetic. The audited module is a
saved snapshot, never imported from the live author directory.
"""
from __future__ import annotations
import decimal
from decimal import Decimal as D
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import random
import sys
sys.dont_write_bytecode = True

BASE = Path(__file__).resolve().parent
SNAPSHOT = BASE / "snapshots/initial_terminal_mass_certificate.py"
spec = importlib.util.spec_from_file_location("audited_certificate", SNAPSHOT)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
np = mod.np

def solve(A, b):
    A = [list(row) for row in A]
    b = list(b)
    n = len(b)
    for k in range(n):
        if not A[k][k]:
            p = next(i for i in range(k+1, n) if A[i][k])
            A[k], A[p] = A[p], A[k]
            b[k], b[p] = b[p], b[k]
        for i in range(k+1, n):
            q = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= q * A[k][j]
            b[i] -= q * b[k]
    x = [F(0)] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def dot(a, b):
    return sum((x*y for x, y in zip(a,b)), F(0))

def reference(n, edges, target):
    vertices = [i for i in range(n) if i != target]
    index = {v:i for i,v in enumerate(vertices)}
    B = [[F(0)] * len(edges) for _ in vertices]
    for e,(u,v,c) in enumerate(edges):
        if u != target: B[index[u]][e] += 1
        if v != target: B[index[v]][e] -= 1
    A = [[sum((B[i][e]*c*B[j][e] for e,(_,_,c) in enumerate(edges)), F(0))
          for j in range(n-1)] for i in range(n-1)]
    # H = B^T A^-1 B = C^-1/2 P C^-1/2, using exact columns.
    sols = [solve(A,[B[i][e] for i in range(n-1)]) for e in range(len(edges))]
    H = [[sum((B[i][e]*sols[d][i] for i in range(n-1)), F(0))
          for d in range(len(edges))] for e in range(len(edges))]
    return vertices, B, A, H

def matvec(A,x):
    return [dot(row,x) for row in A]

def independent_tree_route(n, edges, target, forcing):
    # Build a BFS tree without using the author's selector or router.
    adj = [[] for _ in range(n)]
    for e,(u,v,_) in enumerate(edges):
        adj[u].append((v,e)); adj[v].append((u,e))
    parent = {target:(target,-1)}
    order = [target]
    for u in order:
        for v,e in adj[u]:
            if v not in parent:
                parent[v]=(u,e); order.append(v)
    assert len(order)==n
    accum=list(forcing)
    flow=[F(0)]*len(edges)
    tree=[]
    for v in reversed(order[1:]):
        u,e=parent[v]
        eu,ev,_=edges[e]
        flow[e]=accum[v] if (eu,ev)==(v,u) else -accum[v]
        accum[u]+=accum[v]
        tree.append(e)
    return flow, np.array(tree,dtype=np.int64)

def check_projection_and_forcing(n, edges, target, source, rng):
    verts,B,A,H=reference(n,edges,target)
    g=mod.graph(n,[(u,v,float(c)) for u,v,c in edges],[1]*n,source,target)
    block,sizes=mod.cycle_blocks(g)
    m=len(edges)
    for e in range(m):
        if sizes[block[e]]==1:
            assert H[e][e]==1/edges[e][2]
        for d in range(m):
            if block[e]!=block[d]: assert H[e][d]==0
    # Exact P^2=P without square roots: H C H=H.
    for e in range(m):
        for d in range(m):
            assert sum((H[e][k]*edges[k][2]*H[k][d] for k in range(m)), F(0))==H[e][d]
    a=[F(rng.randint(-5,5),8) for _ in verts]
    b=[F(rng.randint(-5,5),8) for _ in verts]
    x=[F(rng.randint(-7,7),16) for _ in verts]
    y=[F(rng.randint(-7,7),16) for _ in verts]
    ax,ay=matvec(A,x),matvec(A,y)
    ra=[v-w for v,w in zip(a,ax)]
    rb=[v-w for v,w in zip(b,ay)]
    T=dot(a,solve(A,b))
    T0=dot(a,y)+dot(x,rb)
    R=dot(ra,solve(A,rb))
    assert T==T0+R
    fa=[F(0)]*n; fb=[F(0)]*n
    for i,v in enumerate(verts): fa[v]=ra[i]; fb[v]=rb[i]
    f,tree=independent_tree_route(n,edges,target,fa)
    h,_=independent_tree_route(n,edges,target,fb)
    assert matvec(B,f)==ra and matvec(B,h)==rb
    E1=sum((f[e]*f[e]/edges[e][2] for e in range(m)),F(0))
    E2=sum((h[e]*h[e]/edges[e][2] for e in range(m)),F(0))
    J=sum((f[e]*h[e]/edges[e][2] for e in range(m)),F(0))
    assert (2*R-J)**2 <= E1*E2
    total=F(0)
    for bid,size in enumerate(sizes):
        ee=[e for e in range(m) if block[e]==bid]
        rr=sum((f[e]*H[e][d]*h[d] for e in ee for d in ee),F(0))
        jj=sum((f[e]*h[e]/edges[e][2] for e in ee),F(0))
        es=sum((f[e]*f[e]/edges[e][2] for e in ee),F(0))
        ew=sum((h[e]*h[e]/edges[e][2] for e in ee),F(0))
        assert (2*rr-jj)**2 <= es*ew
        if size==1: assert rr==jj
        total+=rr
    assert total==R
    return dict(states=n,edges=m,target=target,blocks=len(sizes),bridges=int(sum(sizes==1)))

def certificate_check(g,x,y,tree,precision=40):
    cert=mod.interval_certificate(g,x,y,tree,precision)
    edges=[(int(u),int(v),F(float(c))) for u,v,c in zip(g.u,g.v,g.c)]
    verts,_,A,_=reference(g.n,edges,g.t)
    exact=solve(A,[F(float(g.w[i])) for i in verts])[verts.index(g.s)]
    contained=F(D(cert['lower']))<=exact<=F(D(cert['upper']))
    assert contained,(exact,cert)
    return dict(exact=str(exact),lower=cert['lower'],upper=cert['upper'],precision=precision,
                radius=cert.get('blockwise_radius_upper'),contained=contained)

def main():
    rng=random.Random(615074)
    results={"snapshot_sha256":hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(),
             "python":sys.version,"libmpdec":decimal.__libmpdec_version__,
             "projection_checks":[],"arithmetic_checks":[],"countermodels":{}}
    # Figure-eight (one articulation, no bridge) and a two-parallel-edge cycle.
    fixtures=[(5,[(0,1,F(2)),(1,2,F(3)),(2,0,F(5)),(2,3,F(7)),(3,4,F(11)),(4,2,F(13))]),
              (3,[(0,1,F(2)),(0,1,F(3)),(1,2,F(5))])]
    for n,edges in fixtures:
        for target in range(n):
            results['projection_checks'].append(check_projection_and_forcing(n,edges,target,(target+1)%n,rng))
    for run in range(120):
        n=rng.randint(2,8)
        edges=[(i,rng.randrange(i),F(rng.randint(1,20),8)) for i in range(1,n)]
        for _ in range(rng.randint(0,8)):
            u,v=rng.sample(range(n),2)
            edges.append((u,v,F(rng.randint(1,20),8)))
        target=rng.randrange(n); source=(target+1)%n
        results['projection_checks'].append(check_projection_and_forcing(n,edges,target,source,rng))
        masses=[float(F(rng.randint(1,100),16)) for _ in range(n)]
        g=mod.graph(n,[(u,v,float(c)) for u,v,c in edges],masses,source,target)
        # Arbitrary grounded potentials, including signed and intentionally bad solves.
        x=np.array([rng.randint(-100,100)/32 for _ in range(n)])
        y=np.array([rng.randint(-100,100)/32 for _ in range(n)])
        x[target]=y[target]=0
        _,tree=independent_tree_route(n,edges,target,[F(0)]*n)
        results['arithmetic_checks'].append(certificate_check(g,x,y,tree,20 if run%2 else 40))
    # Exact bridge correction isolates a huge leaf's mass from core residual energy.
    mass=2.0**80; eps=2.0**-40
    g=mod.graph(4,[(0,1,1),(0,2,1),(1,2,1.5),(0,3,2.0**-80)], [1,1,1,mass],0,2)
    x=np.array([.625+eps,.25,0,.625+eps]); y=np.array([.625*mass,.25*mass,0,.625*mass])
    tree=np.array([0,2,3],dtype=np.int64)
    results['heavy_leaf']=certificate_check(g,x,y,tree,100)
    results['heavy_leaf_diagnostic']=mod.diagnostic_certificate(g,x,y,tree)
    stress=[]
    for name,conductance,mass in [('smallest_subnormal_c',2.0**-1074,1.0),
                                 ('full_binary64_dynamic_range',2.0**-1074,2.0**1023),
                                 ('large_conductance_cancellation',2.0**900,2.0**-900)]:
        g=mod.graph(2,[(0,1,conductance)],[mass,1],0,1)
        x=np.array([2.0**100,0]); y=np.array([-2.0**100,0])
        stress.append(dict(name=name,**certificate_check(g,x,y,np.array([0]),40)))
    results['dynamic_range_stress']=stress
    g=mod.graph(3,[(0,1,1),(0,2,1),(1,2,1.5)],[1,1,1],0,2)
    results['zero_residual_source_and_mass']=certificate_check(g,np.array([.625,.25,0]),
            np.array([.875,.75,0]),np.array([0,2]),80)
    # Grouping arbitrary contraction clusters is not the cycle-block theorem.
    _,_,_,H=reference(4,[(0,1,F(1)),(1,2,F(1)),(2,3,F(1)),(3,0,F(1))],3)
    assert H[0][2]==F(-1,4)
    results['countermodels']['arbitrary_cluster_localization']={
        'graph':'unit four-cycle 0->1->2->3->0; ground3',
        'clusters':[[0,1],[2,3]],'f':[1,0,0,0],'g':[0,0,1,0],
        'false_clusterwise_interval':['0','0'],'actual_remainder':'-1/4'}
    # With several grounds, a boundary-to-boundary path joins ker(B_grounded).
    # Original bridges are no longer necessarily identity blocks of P.
    Bmulti=[[F(-1),F(1)]]
    Amulti=[[F(2)]]
    fmulti=[F(-1),F(0)]
    rmulti=matvec(Bmulti,fmulti)
    actual=dot(rmulti,solve(Amulti,rmulti))
    assert actual==F(1,2)
    results['countermodels']['multiple_grounds_without_identification']={
        'graph':'unit path 0-1-2; source1; targets0,2',
        'grounded_incidence':[['-1','1']], 'residual_flow':['-1','0'],
        'false_original_bridge_correction':'1','actual_remainder':'1/2',
        'repair':'identify all targets into one ground, then recompute multigraph blocks'}
    # Uniform coefficient bands: evaluate every corner with an exact reference.
    g=mod.graph(3,[(0,1,1),(1,2,1),(2,0,1)],[1,1,1],0,2)
    g.c_bounds=[(D('.9'),D('1.1'))]*3
    g.w_bounds=[(D('.8'),D('1.2'))]*3
    x=np.array([.25,.125,0]); y=np.array([.7,.8,0]); tree=np.array([0,1])
    cert=mod.interval_certificate(g,x,y,tree,50)
    lo,hi=F(D(cert['lower'])),F(D(cert['upper']))
    corner_count=0
    for picks in itertools.product((0,1),repeat=5):
        edges=[(int(g.u[e]),int(g.v[e]),F(g.c_bounds[e][picks[e]])) for e in range(3)]
        verts,B,A,H=reference(3,edges,2)
        b=[F(g.w_bounds[i][picks[3+i]]) for i in range(2)]
        exact=solve(A,b)[0]
        assert lo<=exact<=hi
        corner_count+=1
    results['coefficient_bands']={"corners":corner_count,"certificate":cert}
    # Ambient decimal precision must not alter the verifier's enclosure.
    ctx=decimal.getcontext().copy()
    ambient=[]
    for prec in (2,7,28,100):
        decimal.getcontext().prec=prec
        ambient.append(mod.interval_certificate(g,x,y,tree,50))
    decimal.setcontext(ctx)
    assert len({(z['lower'],z['upper']) for z in ambient})==1
    results['ambient_context_invariance']={"precisions":[2,7,28,100],"same_endpoints":True}
    # Invalid grounding is currently accepted and gives a false enclosure.
    g=mod.graph(2,[(0,1,1)],[1,1],0,1)
    cert=mod.interval_certificate(g,np.zeros(2),np.ones(2),np.array([0]),50)
    results['countermodels']['unchecked_ground']={"x":[0,0],"y":[1,1],"true_mfpt":"1","returned":cert,
       "excludes_truth": not F(D(cert['lower']))<=1<=F(D(cert['upper']))}
    assert results['countermodels']['unchecked_ground']['excludes_truth']
    # Supplying a false cached block partition turns a triangle into fake bridges.
    g=mod.graph(3,[(0,1,1),(1,2,1),(2,0,1)],[1,1,1],0,2)
    cert=mod.interval_certificate(g,np.zeros(3),np.zeros(3),np.array([0,1]),50,
                                  blocks=(np.arange(3),np.ones(3,dtype=int)))
    results['countermodels']['unchecked_cached_blocks']={"true_mfpt":"1","returned":cert,
       "excludes_truth":not F(D(cert['lower']))<=1<=F(D(cert['upper']))}
    assert results['countermodels']['unchecked_cached_blocks']['excludes_truth']
    # The binary64 scope is material: it cannot enclose exact decimal data by fiat.
    g=mod.graph(2,[(0,1,.1)],[1,1],0,1)
    cert=mod.interval_certificate(g,np.zeros(2),np.zeros(2),np.array([0]),50)
    exact_binary=mod.exact_solve(g)
    results['countermodels']['decimal_float_ingress']={"intended_decimal_mfpt":"10",
        "binary64_mfpt":str(exact_binary),"returned":cert,
        "excludes_decimal_truth":not F(D(cert['lower']))<=10<=F(D(cert['upper']))}
    assert results['countermodels']['decimal_float_ingress']['excludes_decimal_truth']
    # Signed forcing needs the unclipped theorem, not the positive-MFPT API.
    g=mod.graph(2,[(0,1,1)],[-1,1],0,1)
    cert=mod.interval_certificate(g,np.zeros(2),np.zeros(2),np.array([0]),50)
    results['countermodels']['signed_mass_clipping']={"true_signed_functional":"-1","returned":cert}
    # A self-loop is rejected by the current Tarjan implementation, not miscertified.
    g=mod.graph(2,[(0,1,1),(0,0,1)],[1,1],0,1)
    try: mod.cycle_blocks(g)
    except Exception as e: results['countermodels']['self_loop']={"raised":repr(e)}
    else: raise AssertionError('Expected loop rejection changed')
    results['counts']={"exact_projection_general_forcing":len(results['projection_checks']),
                       "independent_interval_enclosures":len(results['arithmetic_checks']),
                       "coefficient_band_corners":corner_count}
    results['status']='PASS_VALID_DOMAIN_WITH_EXPLICIT_INTERFACE_COUNTERMODELS'
    (BASE/'audit_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({"status":results['status'],"counts":results['counts'],
                      "countermodels":list(results['countermodels'])},indent=2))

if __name__=='__main__': main()
