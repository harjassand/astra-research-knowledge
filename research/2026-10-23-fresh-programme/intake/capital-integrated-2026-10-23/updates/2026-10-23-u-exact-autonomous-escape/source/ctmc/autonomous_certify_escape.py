"""Construct/check an exact rational balanced-CTMC two-alias certificate.

Only the Python standard library is needed. Verification reads the explicit
rational matrices and does not invoke an optimizer, eigensolver, or expm.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, localcontext, ROUND_HALF_EVEN
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import time

DIRECTORY=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)


def eye(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a,b):
    bt=tr(b)
    return [[sum((x*y for x,y in zip(row,col)),ZERO) for col in bt] for row in a]


def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def sub(a,b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def inverse(a):
    n=len(a)
    aug=[list(row)+unit for row,unit in zip(a,eye(n))]
    determinant=ONE
    for j in range(n):
        pivot=next((i for i in range(j,n) if aug[i][j]),None)
        if pivot is None:
            raise ValueError('Singular rational matrix.')
        if pivot!=j:
            aug[j],aug[pivot]=aug[pivot],aug[j]
            determinant=-determinant
        scale=aug[j][j]
        determinant*=scale
        aug[j]=[value/scale for value in aug[j]]
        for i in range(n):
            if i!=j and aug[i][j]:
                coefficient=aug[i][j]
                aug[i]=[x-coefficient*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug],determinant


def quantize(value,denominator=10**18):
    with localcontext() as context:
        context.prec=80
        integer=int((Decimal(str(value))*Decimal(denominator)).to_integral_value(rounding=ROUND_HALF_EVEN))
    return F(integer,denominator)


def strings(a):
    return [[str(value) for value in row] for row in a]


def rationals(a):
    return [[F(value) for value in row] for row in a]


def make_certificate(source):
    data=json.loads(source.read_text())
    n=data['n']
    rho=F(1,50_000_000)
    a0=quantize(data['a'])
    a=a0+rho
    if not 0<a<1:
        raise ValueError('Filling consumed the escape margin.')
    u=rationals(strings([[quantize(value) for value in row] for row in data['U']]))
    for column in range(1,4):
        mean=sum((row[column] for row in u),ZERO)/n
        for row in u:row[column]-=mean
    epsilon=F(3,5000)
    j=rationals([[0,-1,0,0],[1,0,0,0],[0,0,0,-3],[0,0,3,0]])
    s=eye(4);s[2][0]=epsilon
    sinv=eye(4);sinv[2][0]=-epsilon
    k=mm(mm(s,j),sinv)
    raw=[[quantize(value)+rho*(F(1,n)-F(i==col)) for col,value in enumerate(row)]
         for i,row in enumerate(data['Q'])]
    rowmeans=[sum(row,ZERO)/n for row in raw]
    colmeans=[sum(col,ZERO)/n for col in tr(raw)]
    grandmean=sum(rowmeans,ZERO)/n
    r=[[raw[i][col]-rowmeans[i]-colmeans[col]+grandmean for col in range(n)] for i in range(n)]
    m=[[ONE]+row for row in u]
    gram=mm(tr(m),m)
    gram_inv,gram_determinant=inverse(gram)
    w=mm(gram_inv,tr(m))
    h=[[ZERO]*5 for _ in range(5)]
    for i in range(4):
        for col in range(4):h[i+1][col+1]=k[i][col]-(a if i==col else ZERO)
    b=sub(mm(m,h),mm(r,m))
    q=add(r,mm(b,w))
    return {'schema':'rational-balanced-ctmc-returned-bit-v1','n':n,
            'a':str(a),'a_before_fill':str(a0),'rho':str(rho),'T':'pi',
            'epsilon':str(epsilon),'Q':strings(q),'U':strings(u),'K':strings(k),
            'construction':{'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                            'quantization_denominator':10**18,
                            'formula':'R+(MH-RM)(M^T M)^(-1)M^T',
                            'gram_determinant':str(gram_determinant)}}


def verify(data):
    q,u,k=rationals(data['Q']),rationals(data['U']),rationals(data['K'])
    n=data['n'];a=F(data['a'])
    assert len(q)==n and all(len(row)==n for row in q)
    assert len(u)==n and all(len(row)==4 for row in u)
    assert len(k)==4 and all(len(row)==4 for row in k)
    assert n%2==0 and 0<a<1
    assert [row[0] for row in u]==[ONE]*(n//2)+[-ONE]*(n//2)
    assert all(sum(col,ZERO)==0 for col in tr(u))
    assert all(sum(row,ZERO)==0 for row in q)
    assert all(sum(col,ZERO)==0 for col in tr(q))
    off=[q[i][j] for i in range(n) for j in range(n) if i!=j]
    assert min(off)>0
    _,gram_det=inverse(mm(tr(u),u))
    assert gram_det>0
    h=[[k[i][j]-(a if i==j else ZERO) for j in range(4)] for i in range(4)]
    assert mm(q,u)==mm(u,h)
    epsilon=F(data['epsilon'])
    j=rationals([[0,-1,0,0],[1,0,0,0],[0,0,0,-3],[0,0,3,0]])
    s=eye(4);s[2][0]=epsilon
    sinv=eye(4);sinv[2][0]=-epsilon
    assert mm(s,sinv)==eye(4)
    assert k==mm(mm(s,j),sinv)
    # A cyclic first coordinate ensures both distinct aliases contribute to z.
    powers=[[ONE,ZERO,ZERO,ZERO]]
    for _ in range(3):
        powers.append([sum((k[i][j]*powers[-1][j] for j in range(4)),ZERO) for i in range(4)])
    _,krylov_det=inverse(tr(powers))
    assert krylov_det!=0
    # One nonzero diagonal of QQ^T-Q^TQ certifies nonnormality.
    diagonal_commutators=[sum((q[i][j]**2-q[j][i]**2 for j in range(n)),ZERO) for i in range(n)]
    assert any(diagonal_commutators)
    alpha=math.exp(-math.pi*float(a))
    ceiling=math.exp(-math.pi)
    max_exit=max(-q[i][i] for i in range(n))
    mean_exit=sum((-q[i][i] for i in range(n)),ZERO)/n
    sigma=sum((float(q[i][j]-q[j][i])/n*math.log(float(q[i][j]/q[j][i]))
               for i in range(n) for j in range(i)),0.)
    return {'status':'EXACT_RATIONAL_CERTIFICATE_PASSED','n':n,'memory_states':n//2,
            'a_exact':str(a),'a_decimal':float(a),'gap_1_minus_a_exact':str(1-a),
            'min_offdiagonal_exact':str(min(off)),'min_offdiagonal_decimal':float(min(off)),
            'gram_det_positive':True,'krylov_det_exact':str(krylov_det),
            'row_balance_exact':True,'column_balance_exact':True,'intertwiner_exact':True,
            'flat_sign_exact':True,'rank_U':4,'nonnormal_exact':True,
            'contrast_decimal':alpha,'four_cycle_contrast_decimal':ceiling,
            'contrast_gain_decimal':alpha-ceiling,'success_decimal':(1+alpha)/2,
            'success_gain_decimal':(alpha-ceiling)/2,
            'max_exit_times_pi_decimal':math.pi*float(max_exit),
            'stationary_expected_jumps_to_pi_decimal':math.pi*float(mean_exit),
            'stationary_entropy_production_to_pi_decimal':math.pi*sigma,
            'thermodynamic_convention':'dimensionless natural-log CTMC edge entropy; uniform stationary law',
            'scope':'finite fueled balanced CTMC; external readout at T=pi; no physical implementation or advantage claim'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify',type=Path)
    args=parser.parse_args()
    start=time.monotonic()
    if args.verify:
        path=args.verify
        data=json.loads(path.read_text())
    else:
        path=DIRECTORY/'AUTONOMOUS_ESCAPE_RATIONAL_CERTIFICATE.json'
        data=make_certificate(DIRECTORY/'AUTONOMOUS_ESCAPE_FLOAT_PINNED.json')
        path.write_text(json.dumps(data,indent=2))
    result=verify(data)
    result['certificate_file']=str(path)
    result['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    result['verification_elapsed_seconds']=time.monotonic()-start
    if not args.verify:
        (DIRECTORY/'AUTONOMOUS_ESCAPE_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
