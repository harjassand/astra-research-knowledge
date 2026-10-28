#!/usr/bin/env python3
"""Exact continuum lower-certificate consumer; imports no producer code.

Rebuilds polynomial mass/derivative integrals and verifies the full integer
flow/support interface. The producer's numerical solve is NOT trusted.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json,time
import numpy as np
import sympy as s

BASE=Path(__file__).parent
X=s.Symbol('x')
R=s.Rational

def branch(p,mid,z):
    if p==1:
        if -1<mid<0:return 1+z
        if 0<=mid<1:return 1-z
        return s.S.Zero
    if -R(3,2)<mid<-R(1,2):return (R(3,2)+z)**2/2
    if -R(1,2)<=mid<R(1,2):return R(3,4)-z*z
    if R(1,2)<=mid<R(3,2):return (R(3,2)-z)**2/2
    return s.S.Zero

def integrate_pair(p,k,derivative):
    knots=[-1,0,1] if p==1 else [-R(3,2),-R(1,2),R(1,2),R(3,2)]
    breaks=sorted(set(knots+[t+k for t in knots]))
    total=0
    for a,b in zip(breaks[:-1],breaks[1:]):
        mid=(a+b)/2
        u=branch(p,mid,X);v=branch(p,mid-k,X-k)
        if derivative:u=s.diff(u,X);v=s.diff(v,X)
        primitive=s.integrate(s.expand(u*v),X)
        total+=primitive.subs(X,b)-primitive.subs(X,a)
    return s.factor(total)

def independent_kernels():
    mass={p:{k:integrate_pair(p,k,False) for k in range(-2,3)} for p in [1,2]}
    stiff={p:{k:integrate_pair(p,k,True) for k in range(-2,3)} for p in [1,2]}
    assert mass[1]=={-2:0,-1:R(1,6),0:R(2,3),1:R(1,6),2:0}
    assert mass[2]=={-2:R(1,120),-1:R(13,60),0:R(11,20),1:R(13,60),2:R(1,120)}
    assert stiff[1]=={-2:0,-1:-1,0:2,1:-1,2:0}
    assert stiff[2]=={-2:-R(1,6),-1:-R(1,3),0:1,1:-R(1,3),2:-R(1,6)}
    all_k=[]
    for ax in range(3):
        other=[j for j in range(3) if j!=ax]
        kernel=[]
        for dn in range(-2,3):
            for d1,d2 in itertools.product(range(-1,2),repeat=2):
                d=[0,0,0];d[ax]=dn;d[other[0]]=d1;d[other[1]]=d2
                c=stiff[2][dn]*mass[1][d1]*mass[1][d2]
                c+=mass[2][dn]*stiff[1][d1]*mass[1][d2]
                c+=mass[2][dn]*mass[1][d1]*stiff[1][d2]
                z=c*2160
                assert z.q==1
                if z:kernel.append((d,int(z)))
        all_k.append(kernel)
    return mass,stiff,all_k

def encode(x):
    x=s.Rational(x)
    return dict(numerator=str(x.p),denominator=str(x.q),approximate_display=float(x))

def main():
    t0=time.perf_counter()
    source=BASE/'source_cache/berea_100_to_300.npz'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='0c55fa043b95724000f2c56d9d947409932ba72230413ed5d738410c86838d66'
    a=np.load(BASE/'CURRENTS.npz');Fmask=a['pore_mask'];active=a['active']
    M=Fmask.shape[0];assert Fmask.shape==(M,M,M) and M>=6
    whole=np.load(source)['im'];c=(whole.shape[0]-M)//2
    assert np.array_equal(Fmask,whole[c:c+M,c:c+M,c:c+M])
    sure=Fmask.copy()
    for d in itertools.product(range(-1,2),repeat=3):sure &=np.roll(Fmask,d,axis=(0,1,2))
    assert np.array_equal(active,sure)
    coords=a['coords'];tail=a['tail'];head=a['head'];axis=a['axis'];site=a['site']
    z=a['current_numerators'];assert z.dtype==np.int64 and z.shape==(len(tail),3)
    assert np.array_equal(coords,np.argwhere(active))
    n=len(tail);node=np.full(Fmask.shape,-1,dtype=np.int64);node[tuple(coords.T)]=np.arange(len(coords))
    fmap=[np.full(Fmask.shape,-1,dtype=np.int64) for _ in range(3)]
    # Verify every edge and the integer divergence with an independent literal loop.
    div=[[0,0,0] for _ in coords]
    seen=set()
    for e in range(n):
        ax=int(axis[e]);r=site[e];r2=r.copy();r2[ax]=(r2[ax]+1)%M
        assert active[tuple(r)] and active[tuple(r2)]
        assert tail[e]==node[tuple(r)] and head[e]==node[tuple(r2)]
        key=(ax,*(int(x) for x in r));assert key not in seen;seen.add(key)
        fmap[ax][tuple(r)]=e
        for j in range(3):
            q=int(z[e,j]);div[int(tail[e])][j]+=q;div[int(head[e])][j]-=q
    assert all(not any(v) for v in div)
    # Completeness of edge list is unnecessary for a valid trial, but is checked.
    assert sum(int((active & np.roll(active,-1,axis=ax)).sum()) for ax in range(3))==n
    t1=time.perf_counter();mass,stiff,kernels=independent_kernels();t2=time.perf_counter()
    G=s.zeros(3);zo=z.astype(object);links=0
    for ax in range(3):
        rows=np.flatnonzero(axis==ax);p=site[rows]
        for d,coefficient in kernels[ax]:
            nei=(p+np.array(d))%M;cols=fmap[ax][tuple(nei.T)];ok=cols>=0
            left=zo[rows[ok]];right=zo[cols[ok]]
            block=left.T@right;links+=int(ok.sum())
            for i,j in itertools.product(range(3),repeat=2):G[i,j]+=int(block[i,j])*coefficient
    assert G==G.T
    J=s.Matrix([[sum(int(x) for x in z[axis==ax,col]) for col in range(3)] for ax in range(3)])
    principal={str(k):G[:k,:k].det() for k in [1,2,3]}
    if not all(x>0 for x in principal.values()):
        raise ValueError('Dependent trials: reduce to independent columns before certification')
    K=2160*J*G.inv()*J.T/(M**3)
    minors=[K.extract(idx,idx).det() for k in [1,2,3] for idx in itertools.combinations(range(3),k)]
    assert all(m>=0 for m in minors)
    h=R(1069,200000000);physical=K*h*h
    # A useful derived task consequence, not a preregistered empirical threshold.
    floor=R(1,100)
    margin=K-floor*s.eye(3)
    floor_minors=[margin[:k,:k].det() for k in [1,2,3]]
    floor_pass=all(x>0 for x in floor_minors)
    build=json.loads((BASE/'BUILD_RECEIPT.json').read_text())
    point=np.array(build['ordinary_matched_spline_solver']['permeability_point_in_voxel_squared'])
    Kdisplay=np.array(K.tolist(),dtype=float)
    result=dict(status='EXACT_CONTINUUM_STOKES_TENSOR_LOWER_CERTIFICATE',
        theorem='K_continuum >= K_lower in Loewner order; PROOF.md equations (1)-(6)',
        input_geometry='periodically tiled centered public-image crop; not physical/RVE inclusion',
        checks=dict(image_and_crop=True,one_cell_support_buffer=True,
            literal_integer_divergence_zero=True,face_edges_valid_and_complete=True,
            independent_exact_polynomial_mass_stiffness=True,Gram_positive_definite=True,
            tensor_positive_semidefinite=True,producer_code_imports=False,
            large_floating_solve_validated=False),
        counts=dict(cells=M**3,pore_cells=int(Fmask.sum()),active_cells=len(coords),edges=n,
                    nonzero_stencil_pair_terms=links,current_mean_rank=int(J.rank())),
        exact_Gram_integer=[[str(x) for x in row] for row in G.tolist()],
        exact_mean_integer=[[str(x) for x in row] for row in J.tolist()],
        Gram_leading_minors={k:str(v) for k,v in principal.items()},
        tensor_in_voxel_squared=[[encode(x) for x in row] for row in K.tolist()],
        tensor_in_metres_squared=[[encode(x) for x in row] for row in physical.tolist()],
        tensor_principal_minors=[encode(x) for x in minors],
        derived_all_direction_floor=dict(voxel_squared=encode(floor),
            metres_squared=encode(floor*h*h),strictly_certified=bool(floor_pass),
            leading_margin_minors=[encode(x) for x in floor_minors],
            robust_geometry_tolerance_metres=encode(h/2),
            robust_geometry_promise='Omega_physical contains nominal closed pore union eroded by cube[-h/2,h/2]^3, on the same periodic cell',
            physical_tolerance_acquired=False,
            scope='A posterior algebraic consequence for the model and admitted perturbations; not physical material qualification'),
        matched_ordinary_comparison=dict(same_geometry_basis_and_rhs=True,
            point_prediction=point.tolist(),certificate_approximate=Kdisplay.tolist(),
            maximum_absolute_difference=float(np.max(np.abs(point-Kdisplay))),
            relative_Frobenius_difference=float(np.linalg.norm(point-Kdisplay)/np.linalg.norm(point)),
            scope='Postprocessing adds a continuous lower certificate, not claimed speedup/new spline principle'),
        costs=dict(input_interface_and_exact_flow_checks_seconds=t1-t0,
            independent_polynomial_integration_seconds=t2-t1,
            exact_energy_tensor_seconds=time.perf_counter()-t2,
            total_consumer_seconds=time.perf_counter()-t0,physical_shots=0,paid_compute=0),
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [BASE/'PROOF.md',BASE/'build_transport.py',Path(__file__),BASE/'CURRENTS.npz',source]},
        not_claimed=['historical novelty','upper/relative continuum error bound',
            'actual rock permeability','RVE status','physical subvoxel geometry',
            'general speedup over rigorous FEM/FFT','discovery multiplier acquired'])
    (BASE/'TRANSPORT_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'counts':result['counts'],'tensor_lower_voxel_squared':Kdisplay.tolist(),
        'ordinary_comparison':result['matched_ordinary_comparison'],'costs':result['costs']},indent=2))

if __name__=='__main__':main()
