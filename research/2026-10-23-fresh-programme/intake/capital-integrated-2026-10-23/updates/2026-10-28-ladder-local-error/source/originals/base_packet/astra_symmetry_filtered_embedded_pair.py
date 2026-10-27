#!/usr/bin/env python3
"""Exactly symmetry-filtered two-band hard-core pair embedded in a GLOBAL two-photon continuum.
Calculates full parity one-body spectral measures and hard-core rank-2 resolvent,
checks connected g^4 interaction, isolated even-sector pole and finite-volume Fock spectra.
Every reported result is for the declared finite model unless analytically noted.
"""
import json, math
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

SQ3=math.sqrt(3)
A=4-2*SQ3
B=4/SQ3-2
CHICOEF=3*A*B

def oneparity(g, label, n=256):
    """h+ : emitter 3 coupled sqrt(2)g to endpoint of band [4,6].
        h- : emitter 3 coupled g to endpoint of band [0,2]."""
    plus=(label==1)
    diag=np.r_[3., np.full(n,5. if plus else 1.)]
    off=np.r_[(math.sqrt(2.) if plus else 1.)*g, np.full(n-1,-.5)]
    eig, vec=eigh_tridiagonal(diag,off)
    weight=vec[0,:]**2
    mask=(eig>2.0)&(eig<4.0)
    assert mask.sum()==1,(g,label,eig[mask])
    loc=np.where(mask)[0][0]
    return eig,weight,float(eig[loc]),float(weight[loc])

def L(z,spec):
    E,w,_,_=spec
    return np.sum((w[:,None]*w[None,:])/(E[:,None]+E[None,:]-z))

def Lp(z,spec):
    E,w,_,_=spec
    den=E[:,None]+E[None,:]-z
    return np.sum((w[:,None]*w[None,:])/(den*den))

def evaluate(g,n=256):
    sp=oneparity(g,1,n); sm=oneparity(g,-1,n)
    ep,pm=sp[2],sm[2]
    assert ep<3<pm, (ep,pm)
    lo,hi=2*ep+1e-12,2*pm-1e-12
    root=brentq(lambda z:L(z,sp)+L(z,sm),lo,hi,xtol=8.9e-15)
    Lplus=L(root,sp)
    Lminus=L(root,sm)
    residue=-2*Lplus*Lminus/(Lp(root,sp)+Lp(root,sm))
    chi=root-ep-pm
    gap=min(root-(pm+2), (ep+4)-root)
    # root lies inside continuum of mixed bath lower [0,2] + upper [4,6]: [4,8]
    assert 4<root<8 and gap>0
    return dict(g=g,n=n,onebody_plus=ep,onebody_minus=pm,pole=root,
                connected_shift=chi,coef=chi/g**4,analytic_coef=-CHICOEF,
                bare_pair_overlap_squared=residue,
                lower_even_threshold=pm+2,upper_even_threshold=ep+4,
                isolated_pair_gap=gap,
                parity_plus_weight=sp[3],parity_minus_weight=sm[3],
                symmetry_odd_mixed_continuum=[4,8])

def run():
    cases=[evaluate(g) for g in [.20,.15,.10,.08,.05,.03]]
    out=dict(analytic=dict(surface_value=A,surface_derivative=-B,
                chi_coefficient_exact='-(28*sqrt(3)-48)',chi_coefficient=-CHICOEF,
                c_octice_decay=0.,energy_of_global_odd_continuum=[4.,8.]),cases=cases)
    out['fit_error_at_smallest_g']=cases[-1]['coef']+CHICOEF
    with open('/mnt/data/astra_symmetry_filtered_embedded_pair_results.json','w') as f: json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))
if __name__=='__main__':run()

def physical_fock_audit(g=0.16,n=8):
    """Full 2-hardcore-memory + two truncated boson-chain Fock Hamiltonian.
    Audit parity symmetry, protected bound eigenvalue, and odd mixed-band continuum.
    """
    from scipy.linalg import eigh
    d=2+2*n
    h=np.zeros((d,d),float)
    np.fill_diagonal(h,np.r_[3.,3.,np.full(n,5.),np.full(n,1.)])
    iu,il=2,2+n
    h[0,iu]=h[iu,0]=g;h[1,iu]=h[iu,1]=g
    h[0,il]=h[il,0]=g/math.sqrt(2)
    h[1,il]=h[il,1]=-g/math.sqrt(2)
    for j in range(n-1):
        for start in (iu,il):
            h[start+j,start+j+1]=h[start+j+1,start+j]=-.5
    # physical two-boson basis without forbidden double memory occupancy
    basis=[(i,j) for i in range(d) for j in range(i,d) if not (i==j and i in (0,1))]
    lookup={a:i for i,a in enumerate(basis)}
    H2=np.zeros((len(basis),len(basis)))
    for a,(i,j) in enumerate(basis):
        H2[a,a]=h[i,i]+h[j,j]
        if i==j:
            for k in range(d):
                if k==i or h[k,i]==0:continue
                to=tuple(sorted((i,k)))
                H2[lookup[to],a]+=math.sqrt(2)*h[k,i]
        else:
            for idx,other in ((i,j),(j,i)):
                for k in range(d):
                    if k==idx or h[k,idx]==0:continue
                    to=tuple(sorted((k,other)))
                    if to not in lookup:continue
                    mult=math.sqrt(2) if k==other else 1.0
                    H2[lookup[to],a]+=mult*h[k,idx]
    assert np.linalg.norm(H2-H2.T)<1e-12
    singleperm=np.arange(d)
    singleperm[0]=1;singleperm[1]=0
    signs=np.ones(d);signs[il:]=-1
    S=np.zeros_like(H2)
    for a,(i,j) in enumerate(basis):
        z=tuple(sorted((singleperm[i],singleperm[j])))
        S[lookup[z],a]=signs[i]*signs[j]
    comm=np.linalg.norm(H2@S-S@H2)
    assert comm<1e-12,comm
    E,U=eigh(H2)
    p=np.zeros(len(basis));p[lookup[(0,1)]]=1
    weights=(U.T@p)**2
    idx=np.argmax(weights)
    pair_energy=float(E[idx]);overlap=float(weights[idx])
    svec=np.einsum('ij,ij->j',U,S@U)
    assert svec[idx]>.999
    idx_odd=np.where(svec < -.5)[0]
    oddnear=np.min(abs(E[idx_odd]-pair_energy))
    spec=evaluate(g,n)
    out=dict(g=g,n=n,n_fock=len(basis),symmetry_commutator=comm,
       protected_energy=pair_energy,resolvent_pole=spec['pole'],
       protected_overlap=overlap,resolvent_residue=spec['bare_pair_overlap_squared'],
       odd_spectrum_min_distance_to_embedded_pair=float(oddnear),
       projected_symmetry_expectation=float(svec[idx]),
       lowest_odd_eigs_near_pair=np.sort(E[idx_odd][np.argsort(abs(E[idx_odd]-pair_energy))[:7]]).tolist())
    return out
