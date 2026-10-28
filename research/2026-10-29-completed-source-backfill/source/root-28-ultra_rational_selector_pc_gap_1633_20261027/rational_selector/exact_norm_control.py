"""Analytic exact 180-feature control; no numerical optimization is needed."""
from pathlib import Path
from itertools import combinations_with_replacement as cw, combinations
from fractions import Fraction as Q
import json
import time
import sympy as s

ROOT=Path(__file__).resolve().parent


def exp(ai,xi):
    e=[0]*8
    for i in ai:e[i]+=1
    for i in xi:e[i+4]+=1
    return tuple(e)


def main():
    start=time.monotonic()
    delta=Q(1,4)
    xpair=list(cw(range(4),2))
    base=[exp((i,),(j,)) for i in range(4) for j in range(4)]
    base += [exp((),ij) for ij in xpair]
    r=[[Q(0) for _ in range(26)] for _ in range(26)]
    reserve=[Q(1)]*16+[Q(1 if i==j else 2) for i,j in xpair]
    for i,v in enumerate(reserve):r[i][i]+=delta*v
    for i,j in combinations(range(4),2):
        idx,rev=4*i+j,4*j+i
        r[idx][idx]+=Q(7,4);r[rev][rev]+=Q(7,4)
        r[idx][rev]-=Q(7,4);r[rev][idx]-=Q(7,4)
    sv=[4*i+i for i in range(4)]
    tv=[16+xpair.index((i,i)) for i in range(4)]
    for i in sv:
        for j in sv:r[i][j]+=Q(23,4)
    for i in tv:
        for j in tv:r[i][j]+=Q(3,4)
    for i in sv:
        for j in tv:r[i][j]+=2;r[j][i]+=2
    assert Q(23,4)*Q(3,4)-4==Q(5,16)>0
    features=[exp(ai,(k,)) for ai in cw(range(4),3) for k in range(4)]
    features += [exp(ai,xi) for ai in cw(range(4),2) for xi in cw(range(4),2)]
    lookup={e:i for i,e in enumerate(features)}
    gram=[[Q(0) for _ in range(180)] for _ in range(180)]
    cover=[Q(0)]*180
    for ai in cw(range(4),2):
        factor=Q(1 if ai[0]==ai[1] else 2)
        power=exp(ai,())
        indices=[lookup[tuple(v+w for v,w in zip(power,e))] for e in base]
        for i,target in enumerate(indices):cover[target]+=factor*reserve[i]
        for i,ii in enumerate(indices):
            for j,jj in enumerate(indices):gram[ii][jj]+=factor*r[i][j]
    assert min(cover)>=1
    # Fresh coefficient aggregation and literal symbolic target.
    rebuilt={}
    for i in range(180):
        for j in range(i,180):
            coef=gram[i][j]*(1 if i==j else 2)
            if coef:
                power=tuple(v+w for v,w in zip(features[i],features[j]))
                rebuilt[power]=rebuilt.get(power,Q(0))+coef
    rebuilt={e:c for e,c in rebuilt.items() if c}
    a=s.symbols('a0:4');x=s.symbols('x0:4')
    fa=sum(v*v for v in a)**2
    breg=fa.xreplace(dict(zip(a,(ai+xi for ai,xi in zip(a,x)))))-fa-sum(
        s.diff(fa,ai)*xi for ai,xi in zip(a,x))
    target=s.Poly(sum(v*v for v in a)**2*breg,*a,*x,domain=s.QQ)
    assert rebuilt=={e:Q(int(c.p),int(c.q)) for e,c in target.terms()}
    out={'status':'EXACT_ANALYTIC_180_FEATURE_NORM_CONTROL_PASS',
         'identity':'Z180^T R Z180 = |A|^4 B_(norm4)(A,X)',
         'positive_Gram_lower_bound':'R >= I/4',
         'PSD_proof':'Diagonal reserve plus wedge squares and the positive2x2 matrix [[23/4,2],[2,3/4]], multiplied by the exact normA4 multinomial.',
         'minimum_diagonal_feature_coverage':str(min(cover)),
         'literal_nonzero_coefficient_equations':len(target.terms()),
         'all_possible_coefficient_slots':3185,
         'seconds':time.monotonic()-start}
    (ROOT/'EXACT_NORM_CONTROL_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
