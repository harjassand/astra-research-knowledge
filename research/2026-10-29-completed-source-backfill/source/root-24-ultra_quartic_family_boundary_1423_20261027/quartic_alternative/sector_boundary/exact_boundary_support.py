"""Acquire an exact Q(sqrt42) face certificate from the numeric suggestion."""
from pathlib import Path
from fractions import Fraction as F
import json,pickle,time
import sympy as s
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parent
rad=s.sqrt(42);K=s.QQ.algebraic_field(rad)


def pair(v):
    e=s.expand(K.to_sympy(v));b=e.coeff(rad);a=s.expand(e-b*rad)
    assert a.is_Rational and b.is_Rational
    return [str(a),str(b)]


def positive(v):
    a,b=map(F,pair(v))
    if b==0:return a>0
    if a==0:return b>0
    if a>0 and b>0:return True
    if a<0 and b<0:return False
    return (a*a>42*b*b) if a>0 else (42*b*b>a*a)


def ldl(Q):
    n=len(Q);zero=K.zero;one=K.one
    L=[[one if i==j else zero for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=Q[j][j]-sum((L[j][k]**2*D[k] for k in range(j)),zero)
        assert positive(d),(j,pair(d));D.append(d)
        for i in range(j+1,n):
            L[i][j]=(Q[i][j]-sum((L[i][k]*D[k]*L[j][k] for k in range(j)),zero))/d
    assert all(Q[i][j]==sum((L[i][k]*D[k]*L[j][k] for k in range(n)),zero)
               for i in range(n) for j in range(n))
    return D


def main():
    start=time.monotonic();M,b,terms,bases,ranks,monoms=pickle.loads((ROOT/'FACE_MAP.pkl').read_bytes())
    md=DomainMatrix.from_Matrix(M).convert_to(K);bd=DomainMatrix.from_Matrix(b).convert_to(K)
    rref,pivcols=md.rref();pivcols=list(pivcols);rank=len(pivcols)
    mp=md.extract(list(range(md.shape[0])),pivcols)
    _,pivrows=mp.transpose().rref();pivrows=list(pivrows)
    square=mp.extract(pivrows,list(range(rank)))
    numeric=json.loads((ROOT/'FACIAL_SUPPORT.json').read_text())
    suggestion=[]
    for block,i,j,p in terms:suggestion.append(s.Rational(round(numeric['blocks'][block][i][j]*1_000_000),1_000_000))
    suggestion.append(s.Rational(round(numeric['alpha']*1_000_000),1_000_000))
    vd=DomainMatrix.from_Matrix(s.Matrix(suggestion)).convert_to(K)
    residual=bd-md.matmul(vd)
    delta=square.lu_solve(residual.extract(pivrows,[0]))
    values=[K.from_sympy(x) for x in suggestion]
    for j,c in zip(pivcols,delta.to_list()):values[j]+=c[0]
    final=DomainMatrix.from_Matrix(s.Matrix([K.to_sympy(x) for x in values])).convert_to(K)
    assert md.matmul(final)==bd
    blocks=[];pivots=[];rho=K.from_sympy(s.Rational(1,200))
    for k,V in enumerate(bases):
        n=V.cols;Q=[[K.zero for j in range(n)] for i in range(n)]
        for col,(kk,i,j,p) in enumerate(terms):
            if kk==k:Q[i][j]=Q[j][i]=values[col]
        D=ldl([[Q[i][j]-(rho if i==j else K.zero) for j in range(n)] for i in range(n)])
        blocks.append([[pair(x) for x in row] for row in Q]);pivots.append([pair(x) for x in D])
    alpha=values[-1];delta=K.from_sympy(162-21*rad)-alpha*K.from_sympy(-s.Rational(3,2)+rad/3)
    out={'status':'EXACT_ALGEBRAIC_BOUNDARY_PC_SUPPORT_ACQUIRED',
         'field':'Q(sqrt42), positive sqrt42','tau':['89','-12'],
         'selector_alpha':pair(alpha),'selector_delta':pair(delta),
         'multiplier':'|X|^2','feature_definition':'spin1 then spin3, rephased by i^(second-column count); see PRIMARY_PROOF.md',
         'basis_matrices':[[[pair(K.from_sympy(x)) for x in row] for row in V.tolist()] for V in bases],
         'positive_blocks':blocks,'shifted_LDL_pivots':pivots,'positive_shift':'1/200',
         'block_dimensions':[V.cols for V in bases],'affine_rows':M.rows,'exact_affine_rank':rank,
         'coefficient_identity':'ALL_ROWS_EXACT_OVER_Q_SQRT42','wall_seconds':time.monotonic()-start,
         'scope':'Global PC boundary support; classification requires exact acoustic iff proof. No independent replay yet.'}
    (ROOT/'EXACT_BOUNDARY_SUPPORT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['basis_matrices','positive_blocks','shifted_LDL_pivots']},indent=2))


if __name__=='__main__':main()
