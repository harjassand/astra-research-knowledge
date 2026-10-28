"""Independent stdlib-only consumer of rational moment/SOS value brackets.

Does not import the acquirer, a solver, NumPy, or SymPy. Rebuilds the literal
quartic, moment indexing, all polynomial coefficients, and exact LDL tests.
Also compares all norm4 cases and the old-F zero-mean slice to independent
closed formulas and rational root intervals.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cwr
from pathlib import Path
import json
import math
import time

OUT = Path(__file__).resolve().parent
ZERO = (0,0,0,0)


def mono(ii):
    return tuple(ii.count(j) for j in range(4))


MOMS = [mono(ii) for degree in range(5) for ii in cwr(range(4), degree)]
FEAT = MOMS[:15]
INDEX = {e:i for i,e in enumerate(MOMS)}


def plus(e,f):
    return tuple(x+y for x,y in zip(e,f))


def poly_sum(*polys):
    ans = {}
    for p in polys:
        for e,v in p.items():
            ans[e] = ans.get(e,Q(0))+v
    return {e:v for e,v in ans.items() if v}


def poly_scale(k,p):
    return {e:k*v for e,v in p.items() if k*v}


def mul(p,r):
    ans = {}
    for e,v in p.items():
        for f,w in r.items():
            g=plus(e,f)
            ans[g]=ans.get(g,Q(0))+v*w
    return {e:v for e,v in ans.items() if v}


P = [{mono((j,)):Q(1)} for j in range(4)]
u = poly_sum(mul(P[0],P[0]),mul(P[2],P[2]))
v = poly_sum(mul(P[1],P[1]),mul(P[3],P[3]))
w = poly_sum(mul(P[0],P[1]),mul(P[2],P[3]))
det = poly_sum(mul(P[0],P[3]),poly_scale(-1,mul(P[1],P[2])))
norm = poly_sum(u,v)
p0=Q(55220381,10**10)
p2=Q(114430029,625000000)
p3=-Q(801761987,5000000000)
ell=Q(118849817,4000000000)
FC=poly_sum(poly_scale(p0,poly_sum(mul(u,u),mul(v,v))),poly_scale(p2,mul(u,v)),
            poly_scale(p3,mul(w,w)),poly_scale(ell,mul(det,poly_sum(u,poly_scale(-1,v)))))
NC=mul(norm,norm)


def evalpoly(p,b):
    return sum((val*math.prod(x**n for x,n in zip(b,e)) for e,val in p.items()),Q(0))


def strict_psd(mat):
    n=len(mat)
    low=[[Q(0) for j in range(n)] for i in range(n)]
    diag=[]
    for i in range(n):
        for j in range(i):
            assert mat[i][j]==mat[j][i]
        d=mat[i][i]-sum((low[i][k]**2*diag[k] for k in range(i)),Q(0))
        assert d>0
        diag.append(d)
        for j in range(i+1,n):
            low[j][i]=(mat[j][i]-sum((low[j][k]*low[i][k]*diag[k]
                                      for k in range(i)),Q(0)))/d
    return min(diag)


SQRT_DEN = 1 << 120


def sqrt_bounds(z):
    k=math.isqrt(z.numerator*SQRT_DEN**2//z.denominator)
    lo,hi=Q(k,SQRT_DEN),Q(k+1,SQRT_DEN)
    assert lo*lo<=z<hi*hi
    return lo,hi


def independent_slice(s,eps):
    s=abs(s)
    if not s:
        return Q(0),Q(0)
    c0=2*p0+p2
    assert p0>0 and p0*c0-ell*ell/4>0
    left,right=-ell*s/(2*p0),Q(0)
    for _ in range(88):
        mid=(left+right)/2
        rlo,rhi=sqrt_bounds(mid*mid+4*s*s)
        dlow=2*p0*mid+ell*s+eps*mid/rlo
        dhigh=2*p0*mid+ell*s+eps*mid/rhi
        if dhigh<0:
            left=mid
        elif dlow>0:
            right=mid
        else:
            break
    qleft=p0*left*left+ell*s*left+c0*s*s
    qright=p0*right*right+ell*s*right+c0*s*s
    nlo,_=sqrt_bounds(right*right+4*s*s)
    _,nhi=sqrt_bounds(left*left+4*s*s)
    return qleft+eps*nlo,qright+eps*nhi


def main():
    start=time.monotonic()
    raw=json.loads((OUT/'MOMENT_EVALUATIONS.json').read_text())
    rows=[]
    for row in raw['rows']:
        cert=json.loads((OUT/row['certificate_path']).read_text())
        y=list(map(Q,cert['primal_moments']))
        lam=list(map(Q,cert['dual_lambda']))
        gram=[list(map(Q,r)) for r in cert['dual_gram']]
        b=list(map(Q,cert['mean_scaled']))
        s,eps,scale=map(Q,[cert['det_scaled'],cert['eps_scaled'],cert['scale']])
        assert len(y)==70 and len(lam)==6 and len(gram)==15
        assert y[0]==1
        assert [y[INDEX[mono((i,))]] for i in range(4)]==b
        assert sum((val*y[INDEX[e]] for e,val in det.items()),Q(0))==s
        m=[[y[INDEX[plus(e,f)]] for f in FEAT] for e in FEAT]
        primal_pivot=strict_psd(m)
        dual_pivot=strict_psd(gram)
        base=FC if row['model']=='old_F' else NC
        objective=poly_sum(base,poly_scale(eps,norm))
        target=poly_sum(objective,{ZERO:-lam[0]},
                        *[poly_scale(-lam[1+i],P[i]) for i in range(4)],
                        poly_scale(-lam[5],det))
        rebuilt={}
        for i,e in enumerate(FEAT):
            for j,f in enumerate(FEAT):
                g=plus(e,f)
                rebuilt[g]=rebuilt.get(g,Q(0))+gram[i][j]
        rebuilt={e:v for e,v in rebuilt.items() if v}
        assert rebuilt==target
        lower=(lam[0]+sum((lam[i+1]*b[i] for i in range(4)),Q(0))+lam[5]*s)*scale**4
        upper=sum((val*y[INDEX[e]] for e,val in objective.items()),Q(0))*scale**4
        assert lower==Q(row['lower']) and upper==Q(row['upper']) and lower<=upper
        original_b=list(map(Q,row['B']))
        original_s,original_eps=Q(row['s']),Q(row['epsilon'])
        assert original_b==[z*scale for z in b]
        assert original_s==s*scale**2 and original_eps==eps*scale**2
        control=None
        if row['model']=='norm4_control':
            tau=evalpoly(norm,original_b)+2*abs(original_s-evalpoly(det,original_b))
            exact=tau*tau+original_eps*tau
            assert lower<=exact<=upper
            control={'type':'closed_norm4_all_five_variables','exact':str(exact)}
        elif original_s==evalpoly(det,original_b):
            exact=evalpoly(FC,original_b)+original_eps*evalpoly(norm,original_b)
            assert lower<=exact<=upper
            control={'type':'graph_equality','exact':str(exact)}
        elif original_b==[Q(0)]*4:
            slo,shi=independent_slice(original_s,original_eps)
            assert lower<=slo<=shi<=upper
            control={'type':'independent_rational_slice','lower':str(slo),'upper':str(shi),
                     'display_width':float(shi-slo)}
        rows.append({'model':row['model'],'label':row['label'],'status':'EXACT_PRIMAL_AND_DUAL_PASSED',
                     'display_lower':float(lower),'display_upper':float(upper),
                     'primal_min_pivot':str(primal_pivot),'dual_min_pivot':str(dual_pivot),
                     'control':control})
    out={'status':'INDEPENDENT_STDLIB_CONSUMER_PASSED','rows':rows,
         'seconds':time.monotonic()-start,
         'scope':'Exact PSD, all70 coefficient identities, six affine constraints and rational objective brackets. '
         'Independent formulas check every norm4 case and old-F graph/zero-mean slice cases. '
         'Generic nonzero-mean off-graph old-F values have rational feasible bounds, not a separate closed formula.'}
    (OUT/'INDEPENDENT_MOMENT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'cases':len(rows),
                      'formula_controls':sum(r['control'] is not None for r in rows),
                      'seconds':out['seconds']},indent=2))


if __name__=='__main__':
    main()
