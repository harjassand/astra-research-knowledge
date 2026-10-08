"""Finite diagnostics for the public Gram-normalized decoder.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/energy_checks.py
NumPy only; finite evidence, not infinite validity/priority.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

J, TAU, GPLUS, TOL = 1., .11, 2., 8e-9


def sector(S,m):
    cfg=list(itertools.combinations(range(1,S+1),m))
    ix={x:i for i,x in enumerate(cfg)}
    h=np.zeros((len(cfg),len(cfg)))
    w=np.zeros(len(cfg))
    for i,x in enumerate(cfg):
        xs=set(x)
        h[i,i]=2*J*((1 in xs)+(S in xs))
        w[i]=sum(v+1 in xs for v in x)
        for v in x:
            for dest in (v-1,v+1):
                if 1<=dest<=S and dest not in xs:
                    y=tuple(sorted((xs-{v})|{dest}))
                    h[i,i]+=2*J
                    h[i,ix[y]]-=2*J
    return cfg,h,np.diag(w)


def axis_apply(a,matrix,axis):
    return np.moveaxis(np.tensordot(matrix,a,axes=(1,axis)),0,axis)


errs, gram_margins, kinetic_margins, contact_margins, recovery_margins=[],[],[],[],[]
energy_margins=[]
cases=0
for S in range(2,9):
    L=S+1
    for m in range(1,min(3,S)+1):
        cfg,h,w=sector(S,m)
        n=S-m+1
        labeled=list(itertools.product(range(1,n+1),repeat=m))
        lidx={z:i for i,z in enumerate(labeled)}
        cidx={x:i for i,x in enumerate(cfg)}
        K=np.zeros((n**m,len(cfg)))
        for i,z in enumerate(labeled):
            y=sorted(z)
            x=tuple(y[j]+j for j in range(m))
            K[i,cidx[x]]=1/math.sqrt(math.factorial(m))
        grid=np.arange(1,n+1)
        phi=np.sqrt(2/(n+1))*np.sin(np.pi*np.outer(grid,grid)/(n+1))
        for M in sorted(set((1,min(2,n)))):
            modecfg=list(itertools.combinations_with_replacement(range(1,M+1),m))
            Ji=np.zeros((n**m,len(modecfg)))
            for j,k in enumerate(modecfg):
                perms=set(itertools.permutations(k))
                for z in perms:
                    Ji[lidx[z],j]=1/math.sqrt(len(perms))
            jt=Ji.reshape((n,)*m+(len(modecfg),))
            for i in range(m):
                jt=axis_apply(jt,phi,i)
            Jm=jt.reshape(Ji.shape)
            A=np.zeros((len(cfg),len(modecfg)))
            for i,x in enumerate(cfg):
                y=tuple(x[j]-j for j in range(m))
                A[i,:]=math.sqrt(math.factorial(m))*Jm[lidx[y],:]
            G=A.T@A
            B=K.T@Jm
            gv,ge=np.linalg.eigh(G)
            V=A@(ge*(gv**-.5))@ge.T
            ident=np.eye(len(modecfg))
            errs.extend((float(np.max(abs(K@A-Jm))),float(np.max(abs(A.T@B-ident))),
                         float(np.max(abs(V.T@V-ident))),float(np.max(abs(Jm.T@Jm-ident)))))
            eta=(math.factorial(m)-1)*m*(m-1)*M/(n+1)
            gram_margins.append(eta-float(np.linalg.eigvalsh(G-ident)[-1]))
            olddiff=np.linalg.norm(V-B,2)
            recovery_margins.append(math.sqrt(eta)+eta/2-float(olddiff))
            mode_energy=np.diag([sum(4*J*(1-math.cos(math.pi*k/(n+1))) for k in ks)
                                for ks in modecfg])
            kinetic_margins.append(float(np.linalg.eigvalsh(math.factorial(m)*mode_energy-A.T@h@A)[0]))
            c_bound=math.factorial(m)*m*(m-1)*M/(n+1)
            contact_margins.append(float(np.linalg.eigvalsh(c_bound*ident-A.T@w@A)[0]))
            e_bound=math.factorial(m)*(2*J*math.pi**2*m*M*M*L*L/(n+1)**2
                          +GPLUS*L*m*(m-1)*M/(n+1))
            energy_margins.append(e_bound-float(np.linalg.eigvalsh(L*L*V.T@(h+GPLUS/L*w)@V)[-1]))
            cases+=1
assert max(errs)<=TOL
assert min(gram_margins)>=-TOL
assert min(kinetic_margins)>=-TOL
assert min(contact_margins)>=-TOL
assert min(recovery_margins)>=-TOL
assert min(energy_margins)>=-TOL

# Explicit repeated two-plane amplification, including the attenuation
# that makes an integer number of ordinary reflections deterministic.
amp=[]
for m in range(1,11):
    theta=math.asin(1/math.sqrt(math.factorial(m)))
    q=math.ceil(math.pi/(4*theta)-.5)
    tp=math.pi/(4*q+2)
    assert tp<=theta+TOL
    vec=np.array([math.sin(tp),math.cos(tp)])
    reflection=2*np.outer(vec,vec)-np.eye(2)
    grover=reflection@np.diag([-1.,1.])
    got=np.linalg.matrix_power(grover,q)@vec
    error=float(np.linalg.norm(got-np.array([1.,0.])))
    assert error<=TOL
    amp.append({"m":m,"q":q,"success_amplitude_error":error})

# Check the stabilizer identity used by the linear-N Gram setup formula.
stabilizer=0
for m in range(1,6):
    perms=list(itertools.permutations(range(m)))
    for z in itertools.product(range(1,4),repeat=m):
        left=math.prod(math.factorial(z.count(v)) for v in set(z))
        right=sum(all(z[i]==z[p[i]] for i in range(m)) for p in perms)
        assert left==right
        stabilizer+=1

# Exactly normalized smooth recovery for m=2,M=1: unlike K^* it has no
# fixed contact jump and its critical output energy has a finite limit.
smooth=[]
g=.4
for L in (17,33,65,129,257):
    n=L-2
    f=np.sqrt(2/(n+1))*np.sin(np.pi*np.arange(1,n+1)/(n+1))
    s=float((f**4).sum())
    eps=4*J*(1-math.cos(math.pi/(n+1)))
    e=TAU*L*L*(2*eps+g/L*2*s)/(1+s)
    smooth.append({"L":L,"decoded_positive_critical_energy":e,
                   "limit":TAU*(4*J*math.pi**2+3*g)})

out={"status":"FINITE-EVIDENCE","all_checks_passed":True,"S_range":[2,8],
     "mode_sector_cases":cases,"max_isometry_inverse_error":max(errs),
     "min_Gram_bound_margin":min(gram_margins),"min_kinetic_margin":min(kinetic_margins),
     "min_contact_margin":min(contact_margins),"min_recovery_norm_margin":min(recovery_margins),
     "min_energy_margin":min(energy_margins),"amplification":amp,
     "stabilizer_configurations":stabilizer,"smooth_energy_recovery":smooth}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
