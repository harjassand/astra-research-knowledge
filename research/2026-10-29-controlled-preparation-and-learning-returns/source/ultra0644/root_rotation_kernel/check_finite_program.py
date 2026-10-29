"""Independent all-time program identity; no producer-module imports."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,time

def mm(a,b):return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
def tr(a):return tuple(a[3*j+i] for i in range(3) for j in range(3))
def action(g,e):return mm(mm(g,e),tr(g))

def run():
    start=time.perf_counter();base=Path(__file__).resolve().parents[1]
    program=json.loads((base/'t_collision_operation/outputs/FINITE_SINGLETON_PROGRAM.json').read_text())
    group=[tuple(x) for x in program['group']];idx={g:i for i,g in enumerate(group)}
    identity=(1,0,0,0,1,0,0,0,1);assert group[0]==identity and len(idx)==24
    rx=(1,0,0,0,0,-1,0,1,0);ry=(0,0,1,0,1,0,-1,0,0)
    rotations=[rx,tr(rx),ry,tr(ry)]
    for g in group:assert mm(g,tr(g))==identity
    q=[[F(0) for _ in group] for _ in group]
    for j,g in enumerate(group):
        q[j][j]-=F(1,2)
        for r in rotations:q[idx[mm(r,g)]][j]+=F(1,8)
    b=[[F(col['weights'][g],col['denominator']) for col in program['columns']] for g in range(24)]
    assert all(x>=0 for row in b for x in row)
    assert all(sum(row[k] for row in b)==1 for k in range(5))
    # Expand positive Bernstein form directly; no spectral decomposition.
    coefficients=[[F(0) for _ in range(5)] for _ in group]
    for g in range(24):
        for k in range(5):
            for j in range(5-k):
                coefficients[g][k+j]+=b[g][k]*comb(4,k)*comb(4-k,j)*(-1)**j
    for g in range(24):
        assert sum(coefficients[g])==(1 if g==0 else 0)
        for k in range(5):
            lhs=sum(q[g][j]*coefficients[j][k] for j in range(24))
            assert lhs==-F(k,4)*coefficients[g][k]
    # All matrix units: group-chain generator intertwinement is an identity.
    for a in range(3):
        for bindex in range(3):
            e=tuple(int(i==3*a+bindex) for i in range(9))
            images=[action(g,e) for g in group]
            for j,g in enumerate(group):
                lhs=[sum(q[k][j]*images[k][h] for k in range(24)) for h in range(9)]
                rhs=[sum(F(1,8)*action(r,images[j])[h] for r in rotations)-F(1,2)*images[j][h] for h in range(9)]
                assert lhs==rhs
    return dict(scope='independent exact ALL-time finite-program identities, no MC or producer imports',
                bernstein_nonnegative_entries=120,normalized_columns=5,
                polynomial_generator_coefficients=120,initial_state_identities=24,
                all_matrix_units=9,group_states=24,status='PASS',
                continuous_exp_coins='still an independent random-bit primitive interface',
                seconds=time.perf_counter()-start)

if __name__=='__main__':
    r=run();Path(__file__).with_name('EXACT_PROGRAM_REVIEW.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
