"""Exact one-branch logical fault-amplitude resummation on native pair slots.

This finite conditional clock schedule checks the receiver algebra; it is
not a probability estimate for the whole autonomous clock ensemble.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/"outputs/logical_phase_20261101"
I=s.eye(2)
X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
N=4
ALL=(1<<N)-1
LOCS=[0,1,3]
TS=[s.Rational(1,70),s.Rational(1,80),s.Rational(1,90)]
BATH=[X,Z,Y]


def active(state, i):
    y,x=divmod(i,2)
    left=y*2+(x-1)%2
    down=((y-1)%2)*2+x
    return ((state>>i)&1)!=((state>>left)&1) and ((state>>i)&1)!=((state>>down)&1)


def classical_bad(bits):
    state=0
    for slot,i in enumerate(LOCS):
        if bits&(1<<slot):state^=1<<i
        if active(state,2):state^=1<<2
    other=state^ALL
    return int((state.bit_count(),state)>(other.bit_count(),other))


def combine(dic,key,A):
    dic[key]=dic.get(key,s.zeros(2))+A


def bad_isometry(modes):
    # Maps the persistent bath to the decoded wrong logical value and to
    # the ACTUAL correction/decoder environment. Kraus outcomes are never
    # replaced by a classical bath average.
    states={(0,()):I}
    for slot,(i,t,B,mode) in enumerate(zip(LOCS,TS,BATH,modes)):
        c=(1-t*t)/(1+t*t)
        u=2*t/(1+t*t)
        noisy={}
        for (state,record),A in states.items():
            if mode=="identity":combine(noisy,(state,record),A)
            else:
                combine(noisy,(state,record),(c-int(mode=="fault"))*A)
                combine(noisy,(state^(1<<i),record),-s.I*u*B*A)
        states={}
        for (state,record),A in noisy.items():
            jump=int(active(state,2))
            target=state^(jump<<2)
            combine(states,(target,record+(jump,)),A)
    bad={}
    for (state,record),A in states.items():
        comp=state^ALL
        if (state.bit_count(),state)>(comp.bit_count(),comp):
            combine(bad,(record,comp),A)
    return {key:s.simplify(A) for key,A in bad.items() if A!=s.zeros(2)}


def difference(A,B):
    return {key:s.simplify(A.get(key,s.zeros(2))-B.get(key,s.zeros(2)))
            for key in A.keys()|B.keys()}


def main():
    n=len(LOCS)
    subsets=range(1<<n)
    # A support must cover every Pauli choice, including identity pieces
    # in U-Id. Hence use the upward closure of the bad classical histories.
    b={S:max(classical_bad(V) for V in subsets if V&~S==0) for S in subsets}
    assert b[0]==0 and b[(1<<n)-1]==1
    coeff={U:sum((-1)**((U^V).bit_count())*b[V]
                 for V in subsets if V&~U==0) for U in subsets}
    W=bad_isometry(["actual"]*n)
    expansion={}
    for S in subsets:
        term=bad_isometry(["fault" if S&(1<<i) else "identity" for i in range(n)])
        if b[S]==0:assert all(A==s.zeros(2) for A in term.values())
        for key,A in term.items():combine(expansion,key,A)
    assert all(A==s.zeros(2) for A in difference(W,expansion).values())
    resummed={}
    for U in subsets:
        if coeff[U]:
            term=bad_isometry(["fault" if U&(1<<i) else "actual" for i in range(n)])
            for key,A in term.items():combine(resummed,key,coeff[U]*A)
    assert all(A==s.zeros(2) for A in difference(W,resummed).values())
    # ||U_i-I|| <= 2t_i; the exact rotation angle is 2 arctan(t_i).
    w=sum(abs(coeff[U])*s.prod(2*TS[i] for i in range(n) if U&(1<<i)) for U in subsets)
    E=s.simplify(sum((A.conjugate().T*A for A in W.values()),s.zeros(2)))
    gap=s.simplify(w*w*I-E)
    assert gap==gap.conjugate().T
    assert gap[0,0]>=0 and gap[1,1]>=0 and gap.det()>=0
    # Noncommuting bath products must be retained even in this finite test.
    assert X*Z!=Z*X
    out=dict(native_virtual_plane="2x2", noise_faces=LOCS,
             actual_pair_proposals=[2,2,2], bath_operators=["X","Z","Y"],
             support_badness={str(k):v for k,v in b.items()},
             boolean_mobius_coefficients={str(k):v for k,v in coeff.items()},
             exact_bad_isometry_identity=True, exact_error_effect=str(E),
             amplitude_upper=str(w), squared_effect_upper=str(w*w),
             receiver_joint_upper=str(2*w+2*w*w),
             exact_psd_effect_certificate=True,
             scope="Finite exact receiver on a conditional native completed-clock schedule; no continuum, clock-average tail or scalable threshold")
    out["program_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"fault_amplitude_controls.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(output=str(OUT/"fault_amplitude_controls.json"),amplitude_upper=str(w))))


if __name__=="__main__":main()
