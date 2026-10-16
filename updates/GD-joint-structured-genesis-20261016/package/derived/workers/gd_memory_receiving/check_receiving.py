#!/usr/bin/env python3
"""Finite algebra/geometry checks, not an asymptotic memory proof."""
from datetime import datetime, timezone
from itertools import combinations, product
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = dict(I=I2, X=X, Y=Y, Z=Z)

def kron_all(ms):
    out = np.array([[1]], complex)
    for m in ms:
        out = np.kron(out, m)
    return out

def norm(a):
    return float(np.linalg.norm(a, ord='fro'))

def dissipator(a):
    d = a.shape[0]
    i = np.eye(d)
    s = a.conj().T @ a
    return np.kron(a.conj(), a) - (np.kron(i, s)+np.kron(s.T, i))/2

def cptp_super(ks):
    return sum(np.kron(k.conj(), k) for k in ks)

def choi_from_super(s):
    d = int(round(math.sqrt(s.shape[0])))
    out = np.zeros((d*d,d*d), complex)
    for i in range(d):
        for j in range(d):
            e = np.zeros((d,d), complex)
            e[i,j] = 1
            se = (s @ e.reshape(-1, order='F')).reshape((d,d), order='F')
            out += np.kron(se, e)/d
    return (out+out.conj().T)/2

def false_trigger_checks():
    # Faithful representation of the check/write algebra; physical patch geometry below.
    s1, s2, q = np.kron(Z,I2), np.kron(I2,Z), np.kron(X,X)
    eye = np.eye(4, dtype=complex)
    pi = (eye-s1) @ (eye-s2)/4
    a0, inactive = q@pi, eye-pi
    ps = [q, 1j*q@s1, 1j*q@s2, q@s1@s2]
    rs = [s1,s2,s1@s2]
    c0 = np.array([1,1j,1j,1],complex)/4
    assert norm(sum(c*p for c,p in zip(c0,ps))-a0)<1e-12
    assert norm(sum(np.trace(p.conj().T @ r)/4 * np.outer(np.eye(4)[i],np.eye(4)[j])
                    for i,p in enumerate(ps) for j,r in enumerate(ps))-eye)<1e-12
    ideal_channel = cptp_super([a0,inactive])
    completion_error = norm(dissipator(a0)+dissipator(inactive)-(ideal_channel-np.eye(16)))
    max_reconstruction = max_tp = max_kraus = 0.0
    min_eigenvalue = float('inf')
    cases = 0
    physical_rates = []
    for a in [0.001,0.07,0.3]:
        kappa=0.73
        m0=kappa*(a/2+a*a)
        me=kappa*a/4
        floor=kappa*(5*a/4+a*a)*dissipator(q)
        floor+=sum(me*dissipator(p) for p in ps[1:]+rs)
        total_rate=kappa*(4*a+2*a*a)
        physical_rates.append(dict(a=a, kappa=kappa, floor_coefficient=kappa*(11*a/4+a*a),
                                   fault_proposal_rate=total_rate))
        for eps in np.linspace(-a,a,17):
            ap=q@(pi+eps*eye)
            error=kappa*(dissipator(ap)-dissipator(a0))
            c=c0.copy(); c[0]+=eps
            coeff=kappa*(np.outer(c,c.conj())-np.outer(c0,c0.conj()))
            coeff_generator=np.zeros((16,16),complex)
            for i,p in enumerate(ps):
                for j,r in enumerate(ps):
                    rp=r@p
                    coeff_generator+=coeff[i,j]*(np.kron(r.conj(),p)
                        -(np.kron(eye,rp)+np.kron(rp.T,eye))/2)
            max_reconstruction=max(max_reconstruction,norm(error-coeff_generator))
            # Exactly the four fixed-rate proposal channels in the written proof.
            diag_c=kappa*(eps/2+eps*eps)
            diag_ks=[math.sqrt(max(0,(m0-diag_c)/(2*m0)))*eye,
                     math.sqrt(max(0,(m0+diag_c)/(2*m0)))*q]
            proposal_generator=2*m0*(cptp_super(diag_ks)-np.eye(16))
            for j,r in enumerate(rs,1):
                z=coeff[0,j]
                omega=np.trace(r.conj().T @ (ps[j]@q))/4
                edge_a=float(np.real(z*omega))
                t=float(abs(z)); theta=float(np.angle(z)) if t>0 else 0.0
                ks=[math.sqrt(max(0,(me+t)/2))*(q+np.exp(-1j*theta)*ps[j]),
                    math.sqrt(max(0,(me-t)/2))*(q-np.exp(-1j*theta)*ps[j]),
                    math.sqrt(me)*r-edge_a/math.sqrt(me)*eye,
                    math.sqrt(max(0,me-edge_a*edge_a/me))*eye]
                max_tp=max(max_tp,norm(sum(k.conj().T@k for k in ks)-4*me*eye))
                ks=[k/math.sqrt(4*me) for k in ks]
                proposal_generator+=4*me*(cptp_super(ks)-np.eye(16))
            max_kraus=max(max_kraus,norm(proposal_generator-(floor+error)))
            phi=np.eye(16)+(floor+error)/total_rate
            min_eigenvalue=min(min_eigenvalue,float(np.linalg.eigvalsh(choi_from_super(phi))[0]))
            cases+=1
    return dict(cases=cases, max_signed_coefficient_error=max_reconstruction,
                max_edge_kraus_tp_error=max_tp, max_compiled_generator_error=max_kraus,
                min_aggregate_choi_eigenvalue=min_eigenvalue,
                completed_channel_generator_error=completion_error,
                example_rates=physical_rates)

def vec_add(v, directions, signs=None):
    w=list(v)
    for d,s in zip(directions, signs or [1]*len(directions)):
        w[d]+=s
    return tuple(w)

def primal_edge_faces(v,i):
    out=set()
    for j in range(4):
        if i==j: continue
        pair=tuple(sorted((i,j)))
        out.add((v,pair))
        out.add((vec_add(v,[j],[-1]),pair))
    return out

def dual_to_physical(face):
    v,ij=face
    return vec_add(v,ij), tuple(k for k in range(4) if k not in ij)

def boundary_vertices(face):
    v,ij=face
    kl=tuple(k for k in range(4) if k not in ij)
    primal=set(); dual=set()
    for bits in product([0,1],repeat=2):
        primal.add(vec_add(v,ij,bits))
        dual.add(vec_add(v,kl,[-b for b in bits]))
    return primal,dual

def geometry_checks():
    origin=(0,0,0,0)
    patches=[]
    for sector in ['primal','dual']:
        for i,j in combinations(range(4),2):
            star1=primal_edge_faces(origin,i)
            star2=primal_edge_faces(origin,j)
            if sector=='dual':
                star1={dual_to_physical(f) for f in star1}
                star2={dual_to_physical(f) for f in star2}
            patch=star1|star2
            assert len(star1)==len(star2)==6 and len(patch)==11
            assert len(star1&star2)==1
            pverts=set(); dverts=set()
            for f in patch:
                pv,dv=boundary_vertices(f)
                pverts|=pv; dverts|=dv
            reset_radius=max(abs(c) for v in pverts|dverts for c in v)
            assert reset_radius==1
            patches.append(dict(sector=sector,pair=[i,j],qubits=len(patch),
                                tested_check_weights=[6,6],product_check_weight=len(star1^star2),
                                reset_radius=reset_radius,
                                primal_vertex_count=len(pverts),dual_vertex_count=len(dverts)))
    return dict(patch_count=len(patches),patches=patches,
                seven_floor_weights=[1,6,6,11,6,6,10])

def guard_checks():
    cases=[]
    for b in [1,2,5,11]:
        for q in range(b+1):
            r=3
            low=-(r+2)*b-q
            high=(r+3)*b-1+q
            side=high-low+1
            assert side==(2*r+5)*b+2*q
            coarse_low=low//b; coarse_high=high//b
            assert coarse_low>=-(r+3) and coarse_high<=r+3
            cases.append(dict(b=b,q=q,integer_side=side,owner_count=side**4,
                              coarse_owner_low=coarse_low,coarse_owner_high=coarse_high))
    # Two body labels can be arbitrarily far apart: body count is not geometric locality.
    diameter_counterexample=dict(label_weights=[1,1],union_weight=2,
        separation=1000,required_union_diameter=1000,
        scope='Rejects body-count-only admission; does not contradict the bounded-diameter theorem.')
    return dict(cases=cases,body_count_only_counterexample=diameter_counterexample)

def fixed_dictionary_checks():
    rng=np.random.default_rng(1051610)
    records=[]
    for d in [2,4,8]:
        q1,_=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
        q2,_=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
        sigma=np.linspace(1,0,d)
        a=q1@np.diag(sigma)@q2.conj().T
        positive=q2@np.diag(sigma)@q2.conj().T
        polar=q1@q2.conj().T
        v=positive+1j*q2@np.diag(np.sqrt(1-sigma*sigma))@q2.conj().T
        u1=polar@v; u2=polar@v.conj().T
        records.append(dict(dimension=d,rank=int(np.count_nonzero(sigma>1e-14)),
                            expansion_one_norm=1.0,
                            reconstruction_error=norm(a-(u1+u2)/2),
                            unitarity_error=max(norm(u1.conj().T@u1-np.eye(d)),
                                                norm(u2.conj().T@u2-np.eye(d)))))
    return records

def kraus_span_receiving_check():
    # Construct a finite code and one decoder explicitly; no memory lifetime is inferred.
    strings=['XZZXI','IXZZX','XIXZZ','ZXIXZ']
    stabilizers=[kron_all(PAULIS[c] for c in s) for s in strings]
    eye=np.eye(32,dtype=complex)
    project=eye.copy()
    for s in stabilizers: project=project@(eye+s)/2
    logical_z=kron_all([Z]*5)
    p0=project@(eye+logical_z)/2
    eigenvalues,eigenvectors=np.linalg.eigh((p0+p0.conj().T)/2)
    v0=eigenvectors[:,-1]
    v1=kron_all([X]*5)@v0
    enc=np.column_stack((v0,v1))
    recoveries={0:eye}
    for qubit in range(5):
        for p in [X,Y,Z]:
            factors=[I2]*5; factors[qubit]=p
            e=kron_all(factors)
            syndrome=0
            for j,s in enumerate(stabilizers):
                if norm(s@e+e@s)<1e-10: syndrome|=1<<j
            assert syndrome not in recoveries
            recoveries[syndrome]=e
    assert len(recoveries)==16
    projections={}
    for syndrome in range(16):
        p=eye.copy()
        for j,s in enumerate(stabilizers):
            p=p@(eye+((-1)**((syndrome>>j)&1))*s)/2
        projections[syndrome]=p
    n=(X+2*Y+3*Z)/math.sqrt(14)
    rotation=math.cos(0.37)*I2-1j*math.sin(0.37)*n
    max_scalar_residual=max_normalization_error=max_logical_choi_error=0.0
    cases=0
    for qubit in range(5):
        for damping in [0.0,0.17,0.71,1.0]:
            local_ks=[rotation@np.diag([1,math.sqrt(1-damping)]),
                      rotation@np.array([[0,math.sqrt(damping)],[0,0]],complex)]
            rs=[]
            for local_k in local_ks:
                factors=[I2]*5; factors[qubit]=local_k
                k=kron_all(factors)
                for syndrome in range(16):
                    r=enc.conj().T@recoveries[syndrome].conj().T@projections[syndrome]@k@enc
                    scalar=np.trace(r)/2
                    max_scalar_residual=max(max_scalar_residual,norm(r-scalar*I2))
                    rs.append(r)
            max_normalization_error=max(max_normalization_error,
                abs(sum(abs(np.trace(r)/2)**2 for r in rs)-1))
            max_logical_choi_error=max(max_logical_choi_error,
                norm(choi_from_super(cptp_super(rs))-choi_from_super(np.eye(4))))
            cases+=1
    return dict(cases=cases,max_recovered_kraus_nonscalar_residual=max_scalar_residual,
                max_scalar_normalization_error=max_normalization_error,
                max_logical_choi_identity_error=max_logical_choi_error,
                interpretation='Finite operator-span test for dense non-Pauli CPTP faults; not a 4D or asymptotic test.')

if __name__=='__main__':
    results=dict(generated_at_utc=datetime.now(timezone.utc).isoformat(),
                 scope='Finite algebra and geometry only; general claims rest on written proofs.',
                 false_trigger=false_trigger_checks(),geometry=geometry_checks(),
                 guards=guard_checks(),fixed_dictionary=fixed_dictionary_checks(),
                 kraus_span=kraus_span_receiving_check())
    f=results['false_trigger']
    assert f['max_signed_coefficient_error']<1e-12
    assert f['max_edge_kraus_tp_error']<1e-12
    assert f['max_compiled_generator_error']<1e-12
    assert f['min_aggregate_choi_eigenvalue']>-1e-12
    assert f['completed_channel_generator_error']<1e-12
    assert max(x['reconstruction_error'] for x in results['fixed_dictionary'])<1e-12
    assert max(x['unitarity_error'] for x in results['fixed_dictionary'])<1e-12
    assert results['kraus_span']['max_recovered_kraus_nonscalar_residual']<1e-12
    assert results['kraus_span']['max_scalar_normalization_error']<1e-12
    assert results['kraus_span']['max_logical_choi_identity_error']<1e-12
    results['all_checks_passed']=True
    (HERE/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({key:results[key] for key in ['all_checks_passed','false_trigger','fixed_dictionary','kraus_span']},indent=2))
