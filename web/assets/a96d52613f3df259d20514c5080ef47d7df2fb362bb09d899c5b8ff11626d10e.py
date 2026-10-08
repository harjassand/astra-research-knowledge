"""Independent dense-Choi replay using Clebsch-Gordan states, not 6j blocks.

Checks normalization conventions, output equality, unitality, HS symmetry,
and harmonic spectra for the two exact projectors used in PROOF_REPORT.
Finite floating-point output is diagnostic; algebraic legality is proved
in the report from the normalized invariant projector construction.
"""
from functools import lru_cache
import json
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.physics.wigner import clebsch_gordan


@lru_cache(None)
def cg(a,b,c,x,y,z):
    return float(clebsch_gordan(a,b,c,x,y,z))


def tensor_operators(n):
    j=sp.Rational(n,2)
    mags=[j-i for i in range(n+1)]
    operators={}
    for rank in range(n+1):
        basis=[]
        for q in range(-rank,rank+1):
            matrix=np.array([[np.sqrt(2*rank+1)*cg(j,sp.Integer(rank),j,col,sp.Integer(q),row)
                              for col in mags] for row in mags])
            basis.append(matrix)
        operators[rank]=basis
    return operators


def density(n,total,labels,amplitudes):
    j=sp.Rational(n,2)
    d=n+1
    mags=[j-i for i in range(d)]
    result=np.zeros((d**3,d**3))
    for step in range(int(2*total)+1):
        mag=total-step
        vector=np.zeros((d,d,d))
        for ell,amplitude in zip(labels,amplitudes):
            for a,ma in enumerate(mags):
                for b,mb in enumerate(mags):
                    for c,mc in enumerate(mags):
                        vector[a,b,c]+=amplitude*cg(j,j,sp.Integer(ell),mb,mc,mb+mc)*cg(j,sp.Integer(ell),total,ma,mb+mc,mag)
        flat=vector.reshape(-1)
        result+=np.outer(flat,flat)/(int(2*total)+1)
    return result


def replay(n,total,labels,amplitudes,expected):
    d=n+1
    physical=density(n,total,labels,amplitudes)
    six=physical.reshape(d,d,d,d,d,d)
    phys_ab=np.einsum('abkdek->abde',six)
    phys_ac=np.einsum('akcdkf->acdf',six)
    y=np.zeros((d,d))
    for col in range(d):
        y[d-1-col,col]=(-1)**col
    rotate=np.kron(y.T,np.eye(d))
    choi_ab=rotate@phys_ab.reshape(d*d,d*d)@rotate.T
    choi_ac=rotate@phys_ac.reshape(d*d,d*d)@rotate.T
    four=choi_ab.reshape(d,d,d,d)
    def phi(x):
        return d*np.einsum('abcd,ac->bd',four,x)
    matrix_units=[np.eye(d)[[a]].T@np.eye(d)[[b]] for a in range(d) for b in range(d)]
    superop=np.column_stack([phi(x).reshape(-1) for x in matrix_units])
    obs=tensor_operators(n)
    spectra={}
    sector_residual=0.
    for rank in range(n+1):
        values=[np.trace(t.T@phi(t)).real/d for t in obs[rank]]
        scalar=sum(values)/len(values)
        spectra[str(rank)]=scalar
        for tensor in obs[rank]:
            sector_residual=max(sector_residual,float(np.linalg.norm(phi(tensor)-scalar*tensor)))
    result={
        'n':n,'trace_error':float(abs(np.trace(physical)-1)),
        'joint_psd_min':float(np.linalg.eigvalsh(physical)[0]),
        'equal_marginal_error':float(np.linalg.norm(choi_ab-choi_ac)),
        'unital_error':float(np.linalg.norm(phi(np.eye(d))-np.eye(d))),
        'TP_error':float(np.linalg.norm(np.einsum('abcb->ac',four)-np.eye(d)/d)),
        'HS_selfadjoint_error':float(np.linalg.norm(superop-superop.T)),
        'sector_scalar_error':sector_residual,'spectrum':spectra,
        'expected_spectrum_error':max(abs(spectra[str(rank)]-value) for rank,value in expected.items())}
    assert result['trace_error']<1e-12
    assert result['joint_psd_min']>-1e-12
    assert result['equal_marginal_error']<1e-12
    assert result['unital_error']<1e-12
    assert result['TP_error']<1e-12
    assert result['HS_selfadjoint_error']<1e-12
    assert result['sector_scalar_error']<1e-12
    assert result['expected_spectrum_error']<1e-12
    return result


def main():
    sqrt345=np.sqrt(345)
    mu=(6+2*sqrt345)/5
    vector=np.array([8*np.sqrt(21)/5,mu])
    vector/=np.linalg.norm(vector)
    one=replay(3,sp.Rational(3,2),[1,3],vector,
               {1:7/15+1/sqrt345,2:2/5+6*sqrt345/575,3:(3+sqrt345)/35})
    z=np.sqrt(77)
    two=replay(5,sp.Rational(5,2),[3,5],[1/np.sqrt(2)]*2,
               {1:3/5,2:31/100+5*z/588,3:31/105+25*z/882,
                4:1/7+13*z/294,5:109/924+13*z/396})
    output={'scope':'independent dense-Choi finite numerical replay; exact proofs are in PROOF_REPORT.txt',
            'cases':[one,two]}
    path=Path(__file__).with_name('direct_choi_replay.json')
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
