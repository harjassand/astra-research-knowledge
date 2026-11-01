#!/usr/bin/env python3
"""A stronger ordinary comparator for the illustrative stiffness family.

The fast-mode limit is a damped slow mode; this finite comparison prevents the
normalization sweep from being represented as a practical speedup benchmark.
It does not certify the infinite-Fock or continuum reduction for all inputs.
"""
import json,math
from pathlib import Path
import numpy as np
from loss_clock import CoupledBath,annihilators,expm
from retained_process_check import reduced_choi,tn
P=Path(__file__).resolve().parent

def channel(G,Ls,t):
    d=len(G);Lio=np.kron(np.eye(d),G)+np.kron(G.conj(),np.eye(d))
    for L in Ls:Lio+=np.kron(L.conj(),L)
    return expm(Lio*t)

if __name__=='__main__':
    t=.35;K=2;ref=CoupledBath(40,K);states,bs=annihilators(1,K);db=len(states)
    sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex)
    us=expm(-.47j*sy)
    L=np.kron(np.eye(2),math.sqrt(2)*bs[0]);N=bs[0].conj().T@bs[0]
    D=np.kron(ref.Hs,np.eye(db))+np.kron(sx,.12*(bs[0]+bs[0].conj().T))
    G=-np.kron(np.eye(2),N)-1j*D
    e=channel(G,[L],t);u=np.kron(us,np.eye(db));ctrl=np.kron(u.conj(),u)
    class Size: d=db
    Jlim=reduced_choi(e@ctrl@e,Size())
    data={'scope':'Finite two-window, retained-memory qubit Choi comparison at K=2. No universal elimination theorem or hardware benchmark.',
          'ordinary_comparator':'one slow retained mode with A=-1, E=sqrt(2), c=.12, same Hs and system control',
          'total_time':2*t,'K':K,'stiffness_sweep':[]}
    for R in [4,40,4000,400000]:
        b=CoupledBath(R,K);e=channel(b.G,[b.L],t);u=np.kron(us,np.eye(b.d));ctrl=np.kron(u.conj(),u)
        J=reduced_choi(e@ctrl@e,b)
        data['stiffness_sweep'].append({'R':R,'diamond_upper_from_numerical_Choi_vs_slow_limit':2*tn(J-Jlim)})
    x=[r['diamond_upper_from_numerical_Choi_vs_slow_limit'] for r in data['stiffness_sweep']]
    assert all(b<a for a,b in zip(x,x[1:]))
    data['interpretation']='A legitimate ordinary reduction can bypass the large rate at modest error once R is sufficiently large. The new proposed theorem is uniform at finite R and arbitrary requested precision, but the normalization sweep alone does not establish a practical advantage.'
    (P/'results'/'reduction_comparator.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
