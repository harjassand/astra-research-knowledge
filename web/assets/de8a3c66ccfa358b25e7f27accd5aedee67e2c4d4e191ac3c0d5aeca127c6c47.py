"""Finite exact-matrix diagnostics for the gap-compression archive.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/archive_checks.py
NumPy only. This verifies sampled algebra, not infinite theorems or novelty.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

J, TAU, B, GMIN = 1., 0.11, 0.7, 0.03
TOL = 5e-9
c = min(GMIN/96, J/72)
chalf = 1+2*sum(math.exp(-2*J*TAU*k*k) for k in range(1,100))
bhalf = 1+math.log(chalf)+TAU*B+TAU*c/2
ebar = bhalf*bhalf/(TAU*c)+2*math.log(1+math.sqrt(2*math.pi/(TAU*c)))


def sector(S, m):
    cfg = list(itertools.combinations(range(1,S+1),m))
    ix = {x:i for i,x in enumerate(cfg)}
    h = np.zeros((len(cfg),len(cfg)))
    w = np.zeros(len(cfg))
    for i,x in enumerate(cfg):
        xs = set(x)
        w[i] = sum(v+1 in xs for v in x)
        h[i,i] = 2*J*((1 in xs)+(S in xs))
        for v in x:
            for dest in (v-1,v+1):
                if 1<=dest<=S and dest not in xs:
                    y=tuple(sorted((xs-{v})|{dest}))
                    h[i,i]+=2*J
                    h[i,ix[y]]-=2*J
    return cfg, h, np.diag(w)


def apply_axis(a, matrix, axis):
    # matrix acts on a selected labeled coordinate, leaving columns intact.
    t = np.tensordot(matrix, a, axes=(1,axis))
    return np.moveaxis(t, 0, axis)


def exact_K(S,m,cfg):
    n=S-m+1
    labels=list(itertools.product(range(1,n+1),repeat=m))
    ix={x:i for i,x in enumerate(cfg)}
    K=np.zeros((n**m,len(cfg)))
    w=[]
    for j,z in enumerate(labels):
        y=sorted(z)
        x=tuple(y[i]+i for i in range(m))
        K[j,ix[x]]=1/math.sqrt(math.factorial(m))
    for x in cfg:
        y=[x[i]-i for i in range(m)]
        counts=[y.count(v) for v in set(y)]
        w.append(1/math.prod(math.factorial(r) for r in counts))
    return n,labels,K,np.array(w)


gram_errors, form_margins, defect_margins=[],[],[]
channel_margins, mode_margins, dimensions=[],[],[]
energy_values=[]
for S in range(1,9):
    L=S+1
    ztotal={g:0. for g in (GMIN,0.4,2.,12.)}
    etotal={g:0. for g in ztotal}
    # Vacuum contribution.
    for g in ztotal:
        ztotal[g]=1.
    for m in range(1,S+1):
        cfg,h,w=sector(S,m)
        n,labels,K,diag=exact_K(S,m,cfg)
        gram=K.T@K
        gram_errors.append(float(np.max(np.abs(gram-np.diag(diag)))))
        defect_margins.append(float(np.linalg.eigvalsh(w-np.eye(len(cfg))+gram)[0]))
        hn=np.diag(np.full(n,4*J))-2*J*(np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1))
        kt=K.reshape((n,)*m+(len(cfg),))
        hkt=sum((apply_axis(kt,hn,i) for i in range(m)),np.zeros_like(kt))
        form_margins.append(float(np.linalg.eigvalsh(h-K.T@hkt.reshape(K.shape))[0]))
        grid=np.arange(1,n+1)
        sine=np.sqrt(2/(n+1))*np.sin(np.pi*np.outer(grid,grid)/(n+1))
        mode=kt
        for i in range(m):
            mode=apply_axis(mode,sine.T,i)
        mode=mode.reshape(K.shape)
        for g in ztotal:
            hp=h+g/L*w
            ev,vec=np.linalg.eigh(hp)
            weights=np.exp(-TAU*L*L*ev+TAU*B*m)
            ztotal[g]+=float(weights.sum())
            etotal[g]+=float((TAU*L*L*ev*weights).sum())
        # Use a conditional Gibbs state to test the channel algebra, rather
        # than a state chosen to mirror the success filter.
        hp=h+0.4/L*w
        ev,vec=np.linalg.eigh(hp)
        p=np.exp(-TAU*L*L*(ev-ev.min()))
        rho=(vec*(p/p.sum()))@vec.T
        for M in (1,2):
            kept=np.array([all(v<=min(M,n) for v in z) for z in labels])
            Kkeep=mode[kept,:]
            R=Kkeep.T@Kkeep
            bad_mode=float(np.trace((gram-R)@rho))
            e_crit=float(np.trace(h@rho))
            mode_margins.append(L*L*e_crit/(8*J*(M+1)**2)-bad_mode)
            p_fail=float(np.trace((np.eye(len(cfg))-R@R)@rho))
            decoded=R@rho@R
            # Decoder overflow is orthogonal vacuum for m>=1.
            error=float(np.linalg.svd(decoded-rho,compute_uv=False).sum()+p_fail)
            channel_margins.append(3*math.sqrt(max(0,p_fail))-error)
            dimensions.append(int(np.linalg.matrix_rank(Kkeep,tol=1e-9)))
            assert dimensions[-1] <= math.comb(min(M,n)+m-1,m)
    for g in ztotal:
        energy_values.append(etotal[g]/ztotal[g])

assert max(gram_errors)<=TOL
assert min(form_margins)>=-TOL
assert min(defect_margins)>=-TOL
assert min(mode_margins)>=-TOL
assert min(channel_margins)>=-TOL
assert max(energy_values)<=ebar+TOL

# A precise decoder energy limitation: two particles in the first bosonic
# sine mode. K^* creates a half-amplitude contact jump. Its physical
# Hcrit energy is exactly 2 eps_1(1-s)+2Js, s=sum_v f(v)^4.
uv=[]
for L in (17,33,65,129):
    S=L-1
    n=L-2
    cfg=list(itertools.combinations(range(1,S+1),2))
    # Avoid dense high-L sector matrices; construct the form directly.
    f=np.sqrt(2/(n+1))*np.sin(np.pi*np.arange(1,n+1)/(n+1))
    psi={x: (math.sqrt(2) if x[1]>x[0]+1 else 1/math.sqrt(2))
              *f[x[0]-1]*f[x[1]-2] for x in cfg}
    energy=0.
    for x,amp in psi.items():
        xs=set(x)
        energy+=2*J*((1 in xs)+(S in xs))*abs(amp)**2
        for v in x:
            dest=v+1
            if dest<=S and dest not in xs:
                y=tuple(sorted((xs-{v})|{dest}))
                energy+=2*J*abs(amp-psi[y])**2
    eps=4*J*(1-math.cos(math.pi/(n+1)))
    s=float((f**4).sum())
    exact=2*eps*(1-s)+2*J*s
    assert abs(energy-exact)<=TOL
    uv.append({"L":L,"physical_energy":energy,
               "critical_scaled_energy_per_L":TAU*L*energy,
               "predicted_limit":3*TAU*J,"formula_error":abs(energy-exact)})

out={"status":"FINITE-EVIDENCE","all_checks_passed":True,"S_range":[1,8],
     "sector_cases":len(gram_errors),"max_K_gram_error":max(gram_errors),
     "min_free_form_comparison_margin":min(form_margins),
     "min_contact_defect_margin":min(defect_margins),
     "mode_cases":len(mode_margins),"min_mode_bound_margin":min(mode_margins),
     "channel_cases":len(channel_margins),"min_channel_error_margin":min(channel_margins),
     "uniform_energy_certificate":ebar,"max_finite_Gibbs_energy":max(energy_values),
     "decoder_energy_growth":uv}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
