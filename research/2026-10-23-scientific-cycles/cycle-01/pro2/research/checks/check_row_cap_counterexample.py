"""Exact n=4 counterexample to the proposed sharp capped-row extension."""
import time
START=time.perf_counter()
CPU=time.process_time()
from fractions import Fraction as F
from pathlib import Path
import json
import resource


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def flat(a):return[v for row in a for v in row]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def qa(a,b):return(a[0]+b[0],a[1]+b[1])
def qm(a,b):return(a[0]*b[0]+3281*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def qs(a,c):return(a[0]*c,a[1]*c)
def qsum(vals):
    out=(F(0),F(0))
    for x in vals:out=qa(out,x)
    return out


def main():
    n=4
    x=[[F(4,5),F(0)],[F(0),F(1)],[F(1),F(0)],[F(0),F(4,5)]]
    norms=[dot(row,row) for row in x]
    assert norms==[F(16,25),F(1),F(1),F(16,25)]
    diag_outputs=[];edge_outputs=[]
    for i in range(n):
        d=[[F(0) for _ in range(n)] for _ in range(n)];d[i][i]=1
        diag_outputs.append(flat(mm(d,x)))
    for i in range(n-1):
        d=[[F(0) for _ in range(n)] for _ in range(n)]
        d[i][i+1]=d[i+1][i]=1
        edge_outputs.append(flat(mm(d,x)))
    assert [[dot(u,v) for v in diag_outputs] for u in diag_outputs]==[
        [norms[i] if i==j else F(0) for j in range(n)] for i in range(n)]
    assert all(dot(u,v)==0 for u in diag_outputs for v in edge_outputs)
    g=[[dot(u,v) for v in edge_outputs] for u in edge_outputs]
    expected=[[F(41,25),F(4,5),F(0)],[F(4,5),F(2),F(4,5)],
              [F(0),F(4,5),F(41,25)]]
    assert g==expected
    # Exact arithmetic in Q(sqrt3281), encoded as (rational part, radical part).
    lminus=(F(91,50),F(-1,50));lplus=(F(91,50),F(1,50))
    assert qm(lminus,lplus)==(F(2),F(0))
    b=[(F(1),F(0)),(F(9,40),F(-1,40)),(F(1),F(0))]
    gb=[qsum(qs(b[j],g[i][j]) for j in range(3)) for i in range(3)]
    assert gb==[qm(lminus,bi) for bi in b]
    numerator=qs(qsum(qm(bi,bi) for bi in b),F(2))
    denominator=qsum(qm(bi,gi) for bi,gi in zip(b,gb))
    assert numerator==qm(lplus,denominator)
    # Rational isolation establishes positivity, ordering, and strict improvement.
    assert 57**2<3281<58**2
    assert F(0)<F(33,50)<F(34,50)<F(41,25)
    assert F(25,16)<F(74,25)<F(149,50)<F(3)
    assert 1**2<2<2**2  # sqrt2>1, so2+sqrt2>3.
    receipt={'PASS':True,'n':4,'arithmetic':'Fraction and exact Q(sqrt3281) pairs',
             'query_rows':[[str(v) for v in row] for row in x],
             'row_norms_squared':[str(v) for v in norms],
             'total_query_energy':str(sum(norms)),
             'offdiagonal_action_gram':[[str(v) for v in row] for row in g],
             'exact_counterexample_inverse_constant_squared':'(91+sqrt(3281))/50',
             'strict_enclosure_squared':{'lower':'74/25','upper':'149/50'},
             'unit_row_optimum_squared_at_n4':'2+sqrt(2)',
             'strict_counterexample_verified':True,
             'quadratic_field_extremizer_verified':True,
             'wall_seconds_including_imports':time.perf_counter()-START,
             'cpu_seconds_including_imports':time.process_time()-CPU,
             'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
             'scope':'Refutes sharp capped-row extension; no numerical optimization or forest test duplication.'}
    out=Path(__file__).resolve().parents[1]/'results/row_cap_counterexample_challenge.json'
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
