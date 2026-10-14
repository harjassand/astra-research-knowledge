"""Exact OR-pair tensor scaling and rationally certified optimizer.
No search over coefficient laws, group orders, or support patterns is needed.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, math

HERE = Path(__file__).resolve().parent
TERMS = 64

def floor_log2(x):
    e = x.numerator.bit_length() - x.denominator.bit_length()
    p = Q(2)**e
    if x < p: e -= 1
    elif x >= 2*p: e += 1
    assert Q(2)**e <= x < Q(2)**(e+1)
    return e

def atanh_log_bounds(x, terms=TERMS):
    """Rational bounds for ln(x), 1 <= x <= 2, from positive series."""
    assert 1 <= x <= 2
    z = (x-1)/(x+1)
    z2 = z*z
    power = z
    total = Q(0)
    for j in range(terms):
        total += power/(2*j+1)
        power *= z2
    lo = 2*total
    err = 2*power/((2*terms+1)*(1-z2))
    return lo, lo+err

LN2 = atanh_log_bounds(Q(2))

def log_bounds(x):
    x = Q(x)
    assert x >= 1
    e = floor_log2(x)
    lo,hi = atanh_log_bounds(x/(Q(2)**e))
    return lo+e*LN2[0],hi+e*LN2[1]

def ratio_bounds(numer, denom):
    assert 0 < denom[0] <= denom[1]
    assert numer[0] <= numer[1]
    candidates=[x/y for x in numer for y in denom]
    return min(candidates),max(candidates)

def decimal_endpoint(value, upward=False, places=24):
    """Directed rational-to-decimal conversion; no floating logarithms."""
    scale=10**places
    scaled=value*scale
    integer=scaled.numerator//scaled.denominator
    if upward and scaled.denominator!=1:integer+=1
    sign='-' if integer<0 else ''
    integer=abs(integer)
    return f'{sign}{integer//scale}.{integer%scale:0{places}d}'

def pair(a,b):
    n=a+b
    m=2**a+2**b-2
    W=n*2**(n-1)
    P=Q(W,m)
    alpha=ratio_bounds(log_bounds(P),log_bounds(m))
    lm=log_bounds(m);lw=log_bounds(W)
    gap=(lw[0]-2*lm[1],lw[1]-2*lm[0])
    gamma=ratio_bounds(gap,(n*LN2[0],n*LN2[1]))
    return dict(n=n,a=a,b=b,m=m,k=m,W=W,
        proposals_fraction=str(P),ratio_mk_over_W_fraction=str(Q(m*m,W)),
        alpha_interval=[decimal_endpoint(alpha[0]),decimal_endpoint(alpha[1],True)],
        alpha_decimal=[float(alpha[0]),float(alpha[1])],
        gamma_interval=[decimal_endpoint(gamma[0]),decimal_endpoint(gamma[1],True)],
        gamma_decimal=[float(gamma[0]),float(gamma[1])]),alpha,gamma

def small_integer_audit():
    cases=[]
    for a in range(1,5):
        for b in range(1,5):
            n=a+b; maskA=(1<<a)-1;maskB=((1<<b)-1)<<a
            coeff=[0]*(1<<n)
            for x in range(1,1<<a): coeff[x]=1 if x.bit_count()%2 else -1
            for y in range(1,1<<b): coeff[y<<a]=-1 if y.bit_count()%2 else 1
            vals=coeff[:]
            for i in range(n):
                for x in range(1<<n):
                    if x>>i&1: vals[x]+=vals[x^(1<<i)]
            expected=[int(bool(x&maskA))-int(bool(x&maskB)) for x in range(1<<n)]
            assert vals==expected
            m=sum(c!=0 for c in coeff);k=sum(v!=0 for v in vals)
            W=n*2**(n-1)
            assert m==k==2**a+2**b-2
            assert all(coeff[1<<i] for i in range(n))
            for modulus in (2,3,4,6,9):
                for g in range(1,modulus):
                    assert all((c*g)%modulus!=0 for c in coeff if c)
                    assert sum((v*g)%modulus!=0 for v in vals)==k
            cases.append(dict(a=a,b=b,n=n,m=m,k=k,W=W,violates=m*k<W))
    return cases

def main():
    cases=small_integer_audit()
    rows=[];intervals=[]
    for n in range(2,128):
        row,alpha,gamma=pair(n//2,n-n//2)
        rows.append(row);intervals.append((alpha,gamma))
    ai=max(range(len(rows)),key=lambda j:intervals[j][0][0])
    gi=max(range(len(rows)),key=lambda j:intervals[j][1][0])
    assert rows[ai]['n']==24 and rows[gi]['n']==22
    assert all(intervals[ai][0][0]>x[0][1] for j,x in enumerate(intervals) if j!=ai)
    assert all(intervals[gi][1][0]>x[1][1] for j,x in enumerate(intervals) if j!=gi)
    # For n>=128, M>=2^(n/2), and (log2(n)-1)/n decreases.
    alpha_tail=Q(35,32) # 1+2*(7-1)/128
    gamma_tail=Q(3,64) # (7-1)/128
    assert intervals[ai][0][0]>alpha_tail
    assert intervals[gi][1][0]>gamma_tail
    result=dict(status='EXACT_SYMBOLIC_FORMULAS_AND_RATIONAL_LOG_CERTIFICATE',
        coefficient_scope='Every nontrivial finite abelian group, any fixed nonzero g, coefficients +/-g',
        family='Disjoint OR_a-OR_b pairs and their independent tensor products',
        small_integer_checks=cases,
        uniform_cube_points_checked=sum(2**x['n'] for x in cases),
        logarithm_certificate=dict(terms=TERMS,
          formula='ln(x)=2 sum_j z^(2j+1)/(2j+1), z=(x-1)/(x+1)',
          tail='0 <= remainder <= 2 z^(2K+1)/((2K+1)(1-z^2))',
          normalization='x=2^e*y, 1<=y<2; exact rational operations'),
        globally_optimal_sparsity_exponent=rows[ai],
        globally_optimal_dimension_gap=rows[gi],
        tail_n_ge_128=dict(alpha_upper=str(alpha_tail),gamma_upper=str(gamma_tail)),
        finite_optimizer_rows=rows,
        scope_limit='Optimizers are global only within OR-pair tensor family; universal optimal exponent is UNKNOWN')
    (HERE/'tensor_scaling_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('finite_optimizer_rows','small_integer_checks')},indent=2))

if __name__=='__main__':main()
