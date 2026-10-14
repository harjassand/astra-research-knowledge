"""Acquire an AKLT gap certificate from a small patch, then bound response.

Exact rational arithmetic. No supplied full-chain excitation gap or spectrum.
This is an established finite-size-criterion plus residual-bound comparator.
"""
from pathlib import Path
import itertools
import json
import sys
import time
import sympy as sp

def projector():
    pairs=list(itertools.product([1,0,-1],repeat=2))
    index={x:i for i,x in enumerate(pairs)}
    dot=sp.zeros(9)
    for col,(a,b) in enumerate(pairs):
        dot[col,col]=a*b
        for da,db in [(1,-1),(-1,1)]:
            if -1<=a+da<=1 and -1<=b+db<=1:
                dot[index[a+da,b+db],col]=1
    return pairs,(dot*dot+3*dot+2*sp.eye(9))/6

def psd_pivots(matrix):
    """Exact Schur/LDL certificate; zero pivot requires zero remaining row."""
    a=matrix.copy(); pivots=[]
    for k in range(a.rows):
        pivot=a[k,k]
        assert pivot>=0,('negative pivot',k,pivot)
        pivots.append(pivot)
        if pivot==0:
            assert all(a[k,j]==0 for j in range(k+1,a.cols)),('zero nonzero row',k)
        else:
            for i in range(k+1,a.rows):
                for j in range(i,a.cols):
                    a[i,j]-=a[i,k]*a[k,j]/pivot
                    a[j,i]=a[i,j]
    return pivots

def patch_certificate():
    pairs,p=projector()
    output=[]
    for total in range(-4,5):
        words=[w for w in itertools.product([1,0,-1],repeat=4) if sum(w)==total]
        lookup={w:i for i,w in enumerate(words)}
        h=sp.zeros(len(words))
        for col,w in enumerate(words):
            for j in range(3):
                pair=pairs.index((w[j],w[j+1]))
                for out,changed in enumerate(pairs):
                    if p[out,pair]:
                        v=list(w);v[j:j+2]=changed
                        h[lookup[tuple(v)],col]+=p[out,pair]
        certificate=h*h-sp.Rational(2,5)*h
        pivots=psd_pivots(certificate)
        output.append({'total_Sz':total,'dimension':len(words),
            'nonnegative_ldl_pivots':[str(x) for x in pivots]})
    return output

def main():
    t0=time.monotonic()
    patch=patch_certificate()
    # For m=3 consecutive bonds B_i, sum_i B_i^2 >=3*(2/5) H.
    # Projector and disjoint-commutation identities give sum_i B_i^2<=2H^2+H
    # on periodic chains N>=6. Thus H^2>=(1/10)H, acquiring gamma=1/10.
    gamma=sp.Rational(1,10)
    worker=Path(__file__).resolve().parents[1]/'workers/f_sol_quantum_dual'
    sys.path.insert(0,str(worker))
    import aklt_n6_interval as inst
    ak=inst.ak
    assert ak.N==6
    bonds=[inst.bond_projector(j) for j in range(6)]
    h=sum(bonds,sp.zeros(len(ak.ZERO)))
    psi=inst.psi; b=inst.b; norm=inst.norm
    vectors=[]; v=b
    for _ in range(6): vectors.append(v);v=h*v
    gram=sp.Matrix([[vi.dot(h*vj) for vj in vectors] for vi in vectors])
    rhs=sp.Matrix([b.dot(v) for v in vectors])
    coeff=gram.inv()*rhs
    x=sum((coeff[i]*vectors[i] for i in range(6)),sp.zeros(len(ak.ZERO),1))
    lower=(2*b.dot(x)-x.dot(h*x))/norm
    residual=b-h*x
    residual2=residual.dot(residual)/norm
    upper=lower+residual2/gamma
    proposed_upper=sp.Rational(159740147,109636215)
    result={'scope':'exact finite-patch gap certificate and established response residual bound',
        'patch_local_gap_lower_exact':'2/5','periodic_gap_lower_exact':str(gamma),
        'periodic_scope':'spin-1 AKLT rings N>=6 with P2 normalization',
        'patch_psd_statement':'H_open4^2-(2/5)H_open4 is PSD by exact sectorwise LDL',
        'patch_sector_certificates':patch,
        'same_primal_krylov_steps':6,'lower_exact':str(lower),
        'residual_norm2_normalized_exact':str(residual2),
        'residual_upper_exact':str(upper),'residual_upper_decimal':float(upper),
        'proposed_dual_upper_decimal':float(proposed_upper),
        'baseline_interval_width':float(upper-lower),
        'proposed_interval_width':float(proposed_upper-lower),
        'baseline_is_tighter':bool(upper<proposed_upper),
        'wall_seconds':time.monotonic()-t0,
        'comparison_limits':'same primal; exact gap acquisition charged; not a full MPS runtime or memory comparison'}
    Path(__file__).with_name('knabe_response_baseline.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['lower_exact','residual_upper_decimal',
        'proposed_dual_upper_decimal','baseline_interval_width','proposed_interval_width','baseline_is_tighter','wall_seconds']},indent=2))

if __name__=='__main__':main()
