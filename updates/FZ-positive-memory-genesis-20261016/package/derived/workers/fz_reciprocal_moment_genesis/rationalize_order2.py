"""Build and verify an EXACT rational truncated-moment witness.

The solver supplies a candidate only. All final tests use Fraction arithmetic.
The quotient x*u=y*v=1 is encoded by Laurent exponent labels (k,l).
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import itertools, json
ROOT=Path(__file__).resolve().parent
src=json.loads((ROOT/'search_b4p0.json').read_text())
groups=defaultdict(list)
for a,t in zip(src['monomials'],src['moments']):
    k,l=a[0]-a[2],a[1]-a[3]
    groups[tuple(sorted((k,l)))].append(t)
N=10**7
raw={key:F(round(sum(vals)/len(vals)*N),N) for key,vals in groups.items()}
raw[(0,0)]=F(1)
for k,l in list(raw):
    if (k+l)%2: raw[(k,l)]=F(0)

# A symmetric true probability measure in the strict voltage-bound interior.
# X,Y independent, each uniform on {+/-5/4,+/-3/2,+/-7/4}.
supp=[F(5,4),F(3,2),F(7,4)]
def marginal(k):
    return F(0) if k%2 else sum(x**k for x in supp)/3
epsilon=F(1,100)
mom={key:(1-epsilon)*t+epsilon*marginal(key[0])*marginal(key[1]) for key,t in raw.items()}
FINAL_DENOMINATOR=100000
mom={key:F(round(t*FINAL_DENOMINATOR),FINAL_DENOMINATOR) for key,t in mom.items()}
def L(k,l): return mom[tuple(sorted((k,l)))]
def mat(bs,terms={(0,0):F(1)}):
    return [[sum(c*L(a[0]+b[0]+t[0],a[1]+b[1]+t[1]) for t,c in terms.items()) for b in bs] for a in bs]
def ldlt(A):
    n=len(A); D=[]; T=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        T[i][i]=F(1)
        D.append(A[i][i]-sum(T[i][k]**2*D[k] for k in range(i)))
        if D[-1]<=0: raise AssertionError((i,str(D[-1])))
        for j in range(i+1,n):
            T[j][i]=(A[j][i]-sum(T[j][k]*T[i][k]*D[k] for k in range(i)))/D[i]
    assert all(A[i][j]==sum(T[i][k]*D[k]*T[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D

lin=[(0,0),(1,0),(0,1),(-1,0),(0,-1)]
quad=lin+[(2,0),(1,1),(1,-1),(0,2),(-1,1),(-2,0),(-1,-1),(0,-2)]
checks={}
checks['quotient_moment_order2']=ldlt(mat(quad))
for label,t in [('x',(2,0)),('y',(0,2)),('u',(-2,0)),('v',(0,-2))]:
    lo,hi=(F(1),F(4)) if label in ('x','y') else (F(1,64),F(64))
    checks[label+'_lower_localizer']=ldlt(mat(lin,{t:F(1),(0,0):-lo}))
    checks[label+'_upper_localizer']=ldlt(mat(lin,{t:F(-1),(0,0):hi}))
lower=2*(L(2,0)-L(1,1)-L(-2,0)+L(-1,-1))
assert lower<0
# Every degree <=2 multiplier of x*u-1 or y*v-1 reduces identically to zero.
for a in src['monomials']:
    if sum(a)<=2:
        k,l=a[0]-a[2],a[1]-a[3]
        assert L(k+1-1,l)==L(k,l) and L(k,l+1-1)==L(k,l)
result={
 'schema':'astra.exact-order2-reciprocal-counterexample.v1',
 'status':'EXACT_COUNTEREXAMPLE_VERIFIED',
 'definition':'L(x^a y^b u^c v^d)=m[a-c,b-d] for a+b+c+d<=4',
 'zero_odd_total_degree':True,'swap_symmetry':True,
 'voltage_vector':['x','y','u','v'],'B_i':[0,0,1,0],'B_j':[0,0,0,1],
 'complex_embedding':'All four voltage coordinates have imaginary part identically zero; every moment involving a positive imaginary exponent is zero.',
 'bounds':{'x':[1,4],'y':[1,4],'u':['1/64',64],'v':['1/64',64]},
 'fixed_power_equalities':['x*u=1','y*v=1'],
 'direction':{'alpha':1,'beta':-1},
 'violating_polynomial':'(y-x)^2-(u-v)^2',
 'lower_cut_value':str(lower),'lower_cut_decimal_for_display':float(lower),
 'moments':[{'k':k,'l':l,'value':str(t)} for (k,l),t in sorted(mom.items())],
 'exact_ldlt_pivots':{key:list(map(str,val)) for key,val in checks.items()},
 'minimum_pivots_for_display':{key:float(min(val)) for key,val in checks.items()},
 'rounding_denominator':N,'true_measure_mix_before_final_rounding':str(epsilon),
 'final_rounding_denominator':FINAL_DENOMINATOR,
 'true_measure_support_magnitudes':list(map(str,supp)),
 'proof_boundary':'This is a positive truncated functional, not a representing probability measure. It disproves universal containment under the listed algebraic assumptions, not a particular physical PGLib instance.'
}
(ROOT/'EXACT_COUNTEREXAMPLE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ('status','lower_cut_value','lower_cut_decimal_for_display','minimum_pivots_for_display')},indent=2))
