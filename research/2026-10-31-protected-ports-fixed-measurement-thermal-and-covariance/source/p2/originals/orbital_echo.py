"""Exact Hubbard charge permutations on the complete dimer Fock space.

This supplies the physical pulse behind a charge sign echo. It does not
assume zero capacitive interaction during the pulse; the exact identity
is the nominal single-dimer identity, with finite-pulse interaction errors
and mid-cycle charge faults treated separately in the derivation.
"""
import math
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, expm_frechet


def fermion_ops(modes=4):
    d=2**modes; out=[]
    for j in range(modes):
        a=np.zeros((d,d),complex)
        for x in range(d):
            if x>>j&1:
                a[x^(1<<j),x]=(-1)**((x&((1<<j)-1)).bit_count())
        out.append(a)
    return out


def orbital_permutation(perm):
    d=2**len(perm); p=np.zeros((d,d),complex)
    for x in range(d):
        mapped=[perm[j] for j in range(len(perm)) if x>>j&1]
        inversions=sum(mapped[i]>mapped[j] for i in range(len(mapped))
                       for j in range(i+1,len(mapped)))
        y=sum(1<<j for j in mapped)
        p[y,x]=(-1)**inversions
    return p


def model(U=1.,g=3/16,detuning=0.,V=0.):
    a=fermion_ops(); ns=[x.conj().T@x for x in a]
    nl=ns[0]+ns[1]; nr=ns[2]+ns[3]
    N=nl+nr; D=(nl-nr)/2
    double=ns[0]@ns[1]+ns[2]@ns[3]
    hop=-sum(a[s].conj().T@a[2+s]+a[2+s].conj().T@a[s]
             for s in [0,1])
    # U is the effective dimer charging energy, U_on - V.
    H=(U+V)*double+V*nl@nr+g*hop+detuning*D
    return dict(H=H,N=N,D=D,nl=nl,nr=nr,double=double,hop=hop,
                permutation=orbital_permutation([2,3,0,1]))


def pulse(q=3,U=1.,V=0.,detuning=0.):
    assert q>=3 and q%2==1
    g=q*U/(2*(q*q-1))
    tau=math.pi*(q*q-1)/U
    m=model(U,g,detuning,V)
    u=expm(-1j*tau*m['H'])
    return u,m,g,tau


def checks():
    out=[]
    for q in [3,5,7,25]:
        u,m,g,t=pulse(q)
        N=m['N']; p=m['permutation']
        target=expm(1j*q*math.pi*N/2)@p
        du=expm_frechet(-1j*t*m['H'],-1j*t*m['D'],
                       compute_expm=False)
        out.append(dict(q=q,g_over_U=g,U_time=t,
            full_unitary_error=float(np.linalg.norm(u-target,2)),
            full_charge_swap_error=float(np.linalg.norm(
                u.conj().T@m['nl']@u-m['nr'],2)),
            static_detuning_derivative_norm=float(np.linalg.norm(du,2))))
    # Intra-dimer Coulomb gives an N-dependent phase but keeps the exact
    # occupation permutation on all N=0..4 sectors.
    u,m,g,t=pulse(3,V=.17)
    number_phase=expm(-1j*.17*t*(m['N']@(m['N']-np.eye(16)))/2)
    target=number_phase@expm(1j*3*math.pi*m['N']/2)@m['permutation']
    extra=dict(intradimer_V=.17,
               full_unitary_error=float(np.linalg.norm(u-target,2)),
               full_charge_swap_error=float(np.linalg.norm(
                   u.conj().T@m['nl']@u-m['nr'],2)))
    # Two gate pairs use balanced, orthogonal Walsh words.
    y=np.array([[1,1,-1,-1],[1,-1,1,-1]],int)
    assert np.all(y.sum(axis=1)==0)
    assert np.array_equal(y@y.T,4*np.eye(2,dtype=int))
    assert max(x['full_unitary_error'] for x in out)<1e-10
    assert extra['full_charge_swap_error']<1e-12
    return dict(pulses=out,intradimer_coulomb=extra,
                ideal_Walsh_gram=(y@y.T).tolist(),
                single_jump_minimum_max_partial_area='T/[2(m+1)]')


if __name__=='__main__':
    r=checks()
    Path(__file__).with_name('orbital_echo_results.json').write_text(
        json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
