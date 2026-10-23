"""Independent bounded checks. No input/output in candidate directories."""
from fractions import Fraction
from pathlib import Path
import json, math, time
import numpy as np

start = time.perf_counter()
def norm2(x):
    return float(np.vdot(x, x).real / x.shape[0])

def expectation(x, D, N, r, task, prefix):
    sites = N*r
    marked = list(range(task*N, task*N+prefix))
    rest = [j for j in range(sites) if j not in marked]
    order = marked+rest
    axes = order+[sites+j for j in order]
    k, h = D**prefix, D**(sites-prefix)
    tensor = x.reshape([D]*(2*sites)).transpose(axes).reshape(k,h,k,h)
    partial = np.trace(tensor, axis1=0, axis2=2)
    output = np.kron(np.eye(k)/k, partial)
    restored = output.reshape([D]*(2*sites)).transpose(np.argsort(axes))
    return restored.reshape(x.shape), partial

matrix_rows=[]
for D,N,r in [(2,2,2),(2,3,2),(3,2,2)]:
    d=D**(N*r)
    u,v=np.indices((d,d))
    # Distinct deterministic complex input and unequal nonnegative weights.
    x=np.sin((u+2)*(v+1)*.271)+1j*np.cos((u+1)*(v+3)*.163)
    x/=math.sqrt(norm2(x))
    left,s,right_star=np.linalg.svd(x, full_matrices=False)
    R=(right_star.conj().T*s)@right_star
    L=(left*s)@left.conj().T
    assert abs(norm2(R)-1)<1e-12 and abs(norm2(L)-1)<1e-12
    score=np.zeros(3)
    min_margin=float('inf')
    max_density_residual=0.
    for a in range(r):
        for i in range(1,N+1):
            weight=0. if (a==0 and i==1) else (a+1)*(i+.375)
            px=norm2(expectation(x,D,N,r,a,i)[0])
            pr=norm2(expectation(R,D,N,r,a,i)[0])
            pl=norm2(expectation(L,D,N,r,a,i)[0])
            min_margin=min(min_margin,math.sqrt(pr*pl)-px)
            score+=weight*np.array([px,pr,pl])
            # sqrt(rho)=R/sqrt(d), without another eigenvalue decomposition.
            partial_sqrt=expectation(R/math.sqrt(d),D,N,r,a,i)[1]
            density_formula=float(np.trace(partial_sqrt@partial_sqrt).real/D**i)
            max_density_residual=max(max_density_residual,abs(density_formula-pr))
    assert min_margin>=-1e-12
    assert score[0]<=math.sqrt(score[1]*score[2])+1e-12
    assert max_density_residual<1e-12
    matrix_rows.append(dict(D=D,N=N,r=r,d=d,weighted_scores=score.tolist(),
       min_geometric_margin=min_margin,max_density_formula_residual=max_density_residual))

scalar_rows=[]
for D,k in [(2,1),(2,2),(2,3),(2,4),(2,5),(3,1),(3,2),(3,3),(5,1),(5,2)]:
    T=D**k-1; L=T-k
    assert 0<=L<=2*T
    # Enumerate the actual abstract probability law and all rectangles,
    # independently of relying only on the sum-index reduction.
    joint={(j,T-j):Fraction(1,T+1) for j in range(T+1)}
    assert sum(joint.values())==1
    count=0
    for i in range(T+1):
        for j in range(T+1):
            tail=sum(p for (a,b),p in joint.items() if a>=i and b>=j)
            s=i+j
            B=Fraction(1) if s<=L else Fraction(1,D**(s-L))
            formula=Fraction(max(T-s+1,0),T+1)
            assert tail==formula and tail<=B
            count+=1
    expected_sum=sum((a+b)*p for (a,b),p in joint.items())
    assert expected_sum-L==k
    # Extreme saturation is what the analytic nonrealizability check uses.
    assert sum(p for (a,b),p in joint.items() if a>=T)==Fraction(1,D**k)
    assert sum(p for (a,b),p in joint.items() if b>=T)==Fraction(1,D**k)
    assert sum(p for (a,b),p in joint.items() if a>=T and b>=T)==0
    scalar_rows.append(dict(D=D,k=k,N=T,L=L,rectangles=count,gap_over_logD=k))

result=dict(status='PASS',scope='Bounded checks of proved reductions and abstract relaxation only; no uniform tensor conclusion',
            matrix_cases=matrix_rows,scalar_cases=scalar_rows,
            total_rectangles=sum(row['rectangles'] for row in scalar_rows),
            elapsed_seconds=time.perf_counter()-start)
target=Path(__file__).with_name('INDEPENDENT_CHECKS.json')
target.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
