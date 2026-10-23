"""Exact small checks of the path flow/stability lemma, no spectral benchmark."""
import time
START=time.perf_counter()
CPU=time.process_time()
from fractions import Fraction as F
from pathlib import Path
import json
import resource


def dot(x,y):return sum((a*b for a,b in zip(x,y)),F(0))
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def J(x):return[-x[1],x[0]]
def fro2(a):return sum((v*v for row in a for v in row),F(0))
def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def make_d(x):
    n=len(x);c=[F(min(i,n-i)) for i in range(n+1)]
    assert all(dot(v,v)==1 for v in x)
    delta=[det(x[i],x[i+1]) for i in range(n-1)]
    assert all(delta)
    b=[c[i+1]/delta[i] for i in range(n-1)]
    a=[]
    for i in range(n):
        a.append(-(b[i-1]*dot(x[i],x[i-1]) if i else F(0))
                 -(b[i]*dot(x[i],x[i+1]) if i<n-1 else F(0)))
    d=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        d[i][i]=a[i]
        if i<n-1:d[i][i+1]=d[i+1][i]=b[i]
    return d,c,b,delta


def fixture(n,kind):
    cycle=[(F(1),F(0)),(F(3,5),F(4,5)),(F(-5,13),F(12,13)),
           (F(-1),F(0)),(F(-3,5),F(-4,5)),(F(5,13),F(-12,13))]
    if kind=='alternating':x=[(F(i%2==0),F(i%2==1)) for i in range(n)]
    else:x=[cycle[i%len(cycle)] for i in range(n)]
    d,c,b,delta=make_d(x)
    dx=mm(d,x)
    expected=[[(c[i+1]-c[i])*z for z in J(x[i])] for i in range(n)]
    assert dx==expected
    m=n//2
    assert fro2(dx)==2*m
    assert max(abs(z) for z in b)>=m
    assert fro2(d)>=2*sum((v*v for v in c),F(0))
    cf2=F((2*m*m+1),3) if n%2==0 else F((m+1)*(2*m+1),3)
    assert 2*sum((v*v for v in c),F(0))/fro2(dx)==cf2
    x3=[[F(j==i%3) for j in range(3)] for i in range(n)]
    assert fro2(mm(d,x3))==fro2(d)
    # A second arbitrary D tests the three-color identity away from flow witnesses.
    e=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        e[i][i]=F(3*i-2,5)
        if i<n-1:e[i][i+1]=e[i+1][i]=F(i*i-1,7)
    assert fro2(mm(e,x3))==fro2(e)
    # T^T T is exactly the stated integer tridiagonal, supporting the analytic spectrum.
    t=[[F(i==j or i==j+1) for j in range(n-1)] for i in range(n)]
    gram=mm([list(row) for row in zip(*t)],t)
    assert gram==[[F(2 if i==j else 1 if abs(i-j)==1 else 0)
                   for j in range(n-1)] for i in range(n-1)]
    return {'n':n,'query_kind':kind,'determinant_signs':sorted(set(1 if z>0 else -1 for z in delta)),
            'exact_residual_energy':str(fro2(dx)),
            'tent_frobenius_inverse_constant_squared_lower':str(cf2),
            'flow_identity_checked':True,'three_color_isometry_checked':True}


def main():
    results=[fixture(n,kind) for n in [2,3,4,5,9,12] for kind in ['alternating','rational_cycle']]
    parallel=[]
    for sign in [F(1),F(-1)]:
        x=[[F(1),F(0)],[sign,F(0)],[F(0),F(1)]]
        w=[F(1),-sign,F(0)]
        d=[[a*b for b in w] for a in w]
        assert any(v for row in d for v in row)
        assert mm(d,x)==[[F(0),F(0)] for _ in range(3)]
        parallel.append({'adjacent_direction_sign':str(sign),'nonzero_supported_rank_one_annihilator':True})
    receipt={'PASS':True,'arithmetic':'fractions.Fraction',
             'fixtures':results,'parallel_row_cases':parallel,
             'wall_seconds_including_imports':time.perf_counter()-START,
             'cpu_seconds_including_imports':time.process_time()-CPU,
             'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
             'scope':'Exact finite checks complement the universal proof; no new spectral benchmark or floating optimization.'}
    out=Path(__file__).resolve().parents[1]/'results/path_stability_challenge.json'
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
