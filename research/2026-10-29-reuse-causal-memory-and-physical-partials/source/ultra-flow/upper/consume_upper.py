#!/usr/bin/env python3
"""Exact complementary-energy consumer. Imports neither numerical producer.
The lower matrix is consumed from the root-reviewed frozen lower certificate.
"""
from pathlib import Path
import hashlib,itertools,json,time
import numpy as np
import sympy as sy
BASE=Path(__file__).parent
R=sy.Rational

def encode(x):
    x=R(x);return dict(numerator=str(x.p),denominator=str(x.q),approximate_display=float(x))

def parse_matrix(a):return sy.Matrix([[R(x['numerator'])/R(x['denominator']) for x in row] for row in a])

def principal(a):
    return [a.extract(idx,idx).det() for n in [1,2,3] for idx in itertools.combinations(range(3),n)]

def psd(a):return all(x>=0 for x in principal(a))

def symbolic_cell_control():
    # Independent exact integration of all affine row/column components.
    x=sy.symbols('x0:3');a=sy.symbols('a0:9');b=sy.symbols('b0:9')
    A=sy.Matrix(3,3,a);B=sy.Matrix(3,3,b)
    stress=sy.Matrix(3,3,lambda i,j:A[i,j]+(B[i,j]-A[i,j])*x[j])
    integrand=sum(y*y for y in stress)-sy.trace(stress)**2/3
    poly=sy.Poly(sy.expand(integrand),*x)
    literal=sum(coef/sy.prod(e+1 for e in powers) for powers,coef in poly.terms())
    mean=(A+B)/2;delta=B-A
    formula=sum(y*y for y in mean)-sy.trace(mean)**2/3
    formula+=(sum(y*y for y in delta)-sum(delta[i,i]**2 for i in range(3))/3)/12
    assert sy.expand(literal-formula)==0
    return True

def exact_energy(z,inc,out):
    # Shape: face,row,force. Local gather is cell,column,row,force.
    zo=z.astype(object);minus=zo[inc];plus=zo[out]
    S=minus+plus;D=plus-minus
    GS=np.zeros((3,3),dtype=object);GD=GS.copy();Gdiag=GS.copy()
    for col,row in itertools.product(range(3),repeat=2):
        v=S[:,col,row,:];w=D[:,col,row,:]
        GS+=v.T@v;GD+=w.T@w
        if col==row:Gdiag+=w.T@w
    trace=sum(S[:,j,j,:] for j in range(3))
    G=9*GS-3*(trace.T@trace)+3*GD-Gdiag
    return sy.Matrix([[int(x) for x in row] for row in G.tolist()])

def scalar_energy(z,inc,out):
    z=z.astype(object);a=z[inc];b=z[out];S=a+b;D=b-a
    raw=sum(3*int(x)*int(x) for x in S.flat)+sum(int(x)*int(x) for x in D.flat)
    cov=sy.zeros(3)
    for i,j in itertools.product(range(3),repeat=2):
        cov[i,j]=sum(int(v)*int(w) for v,w in zip(S[:,i],S[:,j]))/R(4)
        if i==j:cov[i,j]+=sum(int(x)*int(x) for x in D[:,i])/R(12)
    mass=R(raw,12)
    return mass,mass*sy.eye(3)-cov/3

def relative_factor(L,U):
    lo=R(0);hi=R(sy.ceiling(sy.trace(L.inv()*U)))
    assert psd(hi*L-U)
    for _ in range(40):
        mid=(lo+hi)/2
        if psd(mid*L-U):hi=mid
        else:lo=mid
    coarse=sy.ceiling(100*hi)/R(100)
    assert psd(coarse*L-U)
    return lo,hi,coarse

def main():
    t0=time.perf_counter();a=np.load(BASE/'STRESSES.npz')
    mask=a['pore_mask'];assert mask.shape==(48,48,48)
    original=np.load(BASE.parent/'CURRENTS.npz')['pore_mask'];assert np.array_equal(mask,original)
    source=BASE.parent/'source_cache/berea_100_to_300.npz'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='0c55fa043b95724000f2c56d9d947409932ba72230413ed5d738410c86838d66'
    full=np.load(source)['im'];assert np.array_equal(mask,full[76:124,76:124,76:124])
    coords=a['coords'];assert np.array_equal(coords,np.argwhere(mask))
    M=48;nv=len(coords);node=np.full(mask.shape,-1,dtype=np.int64);node[tuple(coords.T)]=np.arange(nv)
    tail=a['tail'];head=a['head'];axis=a['axis'];site=a['site'];z=a['stress_numerators'];scalar=a['scalar_numerators']
    nf=len(tail);bits=int(a['dyadic_bits']);scale=1<<bits
    assert z.shape==(nf,3,3) and z.dtype==np.int64 and scalar.shape==(nf,)
    maps=[np.full(mask.shape,-1,dtype=np.int64) for _ in range(3)]
    div=[[[0 for _ in range(3)] for _ in range(3)] for _ in range(nv)];sd=[0]*nv
    seen=set();wall_total=[[0]*3 for _ in range(3)]
    for e in range(nf):
        ax=int(axis[e]);r=site[e];s=r.copy();s[ax]=(s[ax]+1)%M
        p=int(node[tuple(r)]);q=int(node[tuple(s)])
        assert p>=0 or q>=0
        assert tail[e]==p and head[e]==q
        key=(ax,*(int(x) for x in r));assert key not in seen;seen.add(key);maps[ax][tuple(r)]=e
        for cell,sgn in [(p,1),(q,-1)]:
            if cell<0:continue
            sd[cell]+=sgn*int(scalar[e])
            for row,f in itertools.product(range(3),repeat=2):div[cell][row][f]+=sgn*int(z[e,row,f])
        if (p<0)!=(q<0):
            sign=1 if p>=0 else -1
            for row,f in itertools.product(range(3),repeat=2):wall_total[row][f]+=sign*int(z[e,row,f])
    assert all(v==scale for v in sd)
    assert all(div[c][row][f]==(scale if row==f else 0) for c in range(nv) for row,f in itertools.product(range(3),repeat=2))
    assert wall_total==[[nv*scale if i==j else 0 for j in range(3)] for i in range(3)]
    assert nf==sum(int((mask|np.roll(mask,-1,axis=ax)).sum()) for ax in range(3))
    inc=np.empty((nv,3),dtype=np.int64);out=np.empty_like(inc)
    for ax in range(3):
        out[:,ax]=maps[ax][tuple(coords.T)]
        r=coords.copy();r[:,ax]=(r[:,ax]-1)%M;inc[:,ax]=maps[ax][tuple(r.T)]
    assert np.array_equal(inc,a['incoming']) and np.array_equal(out,a['outgoing'])
    checks_seconds=time.perf_counter()-t0
    ts=time.perf_counter();symbolic_cell_control();symbolic_seconds=time.perf_counter()-ts
    te=time.perf_counter();G=exact_energy(z,inc,out)
    U=G/(36*M**3*scale**2);mass,initial=scalar_energy(scalar,inc,out)
    initial/=M**3*scale**2;scalar_iso=mass/(M**3*scale**2)
    assert U==U.T and psd(U)
    lower=json.loads((BASE.parent/'TRANSPORT_CERTIFICATE.json').read_text())
    L=parse_matrix(lower['tensor_in_voxel_squared']);assert all(x>0 for x in principal(L))
    assert psd(U-L)
    lo,hi,gamma=relative_factor(L,U)
    il,ih,ig=relative_factor(L,initial)
    h=R(1069,200000000)
    result=dict(status='EXACT_SAME_ORIGINAL_CONTINUUM_LOWER_UPPER_TENSOR_CERTIFICATE',
        original_shape=list(mask.shape),fluid_cells=nv,faces=nf,stress_fields=9,dyadic_bits=bits,
        exact_checks=dict(same_original_image=True,all_faces_valid_and_complete=True,
            all_original_fluid_forces_exact=True,solid_counterforce_compatibility=True,
            independent_symbolic_cell_integration=True,upper_PSD=True,gap_PSD=True,
            producer_code_imports=False,numerical_optimality_required=False),
        tensor_lower_voxel_squared=lower['tensor_in_voxel_squared'],
        tensor_upper_voxel_squared=[[encode(x) for x in row] for row in U.tolist()],
        tensor_upper_metres_squared=[[encode(x*h*h) for x in row] for row in U.tolist()],
        gap_voxel_squared=[[encode(x) for x in row] for row in (U-L).tolist()],
        scalar_Poisson_initializer=dict(isotropic_upper=encode(scalar_iso),
            deviatoric_tensor=[[encode(x) for x in row] for row in initial.tolist()],
            all_force_factor_upper=encode(ig),final_upper_Loewner_improves_initializer=bool(psd(initial-U))),
        all_force_interval=dict(statement='L <= K_original <= U <= gamma L',gamma=encode(gamma),
            sharp_generalized_factor_interval=[encode(lo),encode(hi)]),
        hypercircle=dict(statement='||grad(u_true-v_primal_span)||^2_average <= f^T(U-L)f',
            convention='Gradient-form unit-viscosity energy; retained span is optimally combined for f; no pressure measurement'),
        costs=dict(interface_integer_force_checks_seconds=checks_seconds,
            symbolic_cell_identity_seconds=symbolic_seconds,
            exact_energy_and_tensor_seconds=time.perf_counter()-te,
            total_consumer_seconds=time.perf_counter()-t0,new_physical_shots=0,paid_compute=0),
        physical_scope='No outer or inner physical geometry/RVE/model admission acquired; this is the SAME original periodic image continuum.',
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [BASE/'PROOF.md',BASE/'build_upper.py',Path(__file__),BASE/'STRESSES.npz',BASE.parent/'TRANSPORT_CERTIFICATE.json']})
    (BASE/'UPPER_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(upper=np.array(U.tolist(),dtype=float).tolist(),
        scalar_isotropic_upper=float(scalar_iso),initial_all_force_gamma=float(ig),
        certified_all_force_gamma=float(gamma),factor_interval=[float(lo),float(hi)],
        optimized_Loewner_improvement=bool(psd(initial-U)),costs=result['costs']),indent=2))

if __name__=='__main__':main()
