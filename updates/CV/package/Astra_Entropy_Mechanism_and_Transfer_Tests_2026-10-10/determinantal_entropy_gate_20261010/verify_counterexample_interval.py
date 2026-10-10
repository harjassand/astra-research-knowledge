#!/usr/bin/env python3
"""Outward-rounded interval check of the finite-cutoff determinant gap.

Uses mpmath.iv for the algebraic Fock amplitudes, interval Gram matrix, and
interval Cholesky logdet. The infinite-output remainder is controlled by an
exact rational geometric-tail bound below.
"""
import json, math
from fractions import Fraction
from pathlib import Path
from mpmath import iv

iv.dps=60
M=150; t=1000
zero=iv.mpf(0); one=iv.mpf(1)
sqrt2501=iv.sqrt(iv.mpf(2501))
coeff={0:iv.mpf(50)/sqrt2501,3:one/sqrt2501}
fac=[math.factorial(i) for i in range(M+4)]

def sqrt_upper_fraction(x:Fraction, places=60):
    """Rational upper enclosure of sqrt(x), on a 10^-places grid."""
    Q=10**places
    n=x.numerator*Q*Q; d=x.denominator
    q=math.isqrt(n//d)
    if q*q*d<n: q+=1
    return Fraction(q,Q)

def exact_tail_B(M):
    """Exact rational upper bound for ||(I-P_{N<=M}) S(f⊗g)||."""
    B=Fraction(0,1); weights={0:50,3:1}
    for m,wm in weights.items():
      for n,wn in weights.items():
       for j in range(min(m,n)+1):
        a,b=m-j,n-j
        k0=max(0,(M-a-b)//2+1)
        # At G=2, |c_k|^2 is rational and q=m+n-j+k+1.
        q=m+n-j+k0+1
        c2=Fraction(fac[m]*fac[n]*fac[a+k0]*fac[b+k0],
                     2**q*fac[j]**2*fac[k0]**2*fac[a]**2*fac[b]**2)
        ratio=Fraction((k0+a+1)*(k0+b+1),2*(k0+1)**2)
        if ratio>=1: raise ArithmeticError('tail ratio is not contractive')
        tail2=c2/(1-ratio)
        B+=Fraction(wm*wn,2501)*sqrt_upper_fraction(tail2)
    return B

def amp(m,n,j,k):
    a,b=m-j,n-j
    q=m+n-j+k+1
    facratio=iv.sqrt(iv.mpf(fac[m]*fac[n]*fac[a+k]*fac[b+k]))/iv.mpf(fac[j]*fac[k]*fac[a]*fac[b])
    pow2=one/iv.sqrt(iv.mpf(2)**q)
    return (-one if j%2 else one)*pow2*facratio

psi=[[zero for _ in range(M+1)] for _ in range(M+1)]
for m,fm in coeff.items():
 for n,gn in coeff.items():
  for j in range(min(m,n)+1):
   a,b=m-j,n-j
   for k in range((M-a-b)//2+1):
    p,q=a+k,b+k
    psi[p][q]+=fm*gn*amp(m,n,j,k)

# ρ is exactly block diagonal by photon-number residue modulo 3.
ld_out=zero
pivot_lower=[]
for residue in range(3):
    inds=list(range(residue,M+1,3)); d=len(inds)
    R=[[zero for _ in range(d)] for _ in range(d)]
    for i,p in enumerate(inds):
      for j,p2 in enumerate(inds):
        R[i][j]=sum((psi[p][q]*psi[p2][q] for q in range(M+1)),zero)
    A=[[iv.mpf(1000)*R[i][j] + (one if i==j else zero) for j in range(d)] for i in range(d)]
    L=[[zero for _ in range(d)] for _ in range(d)]
    for i in range(d):
      piv=A[i][i]-sum((L[i][k]*L[i][k] for k in range(i)),zero)
      if float(piv.a) <= 0:
          raise ArithmeticError(f"nonpositive interval Cholesky pivot at block {residue}, row {i}: {piv}")
      L[i][i]=iv.sqrt(piv)
      pivot_lower.append(float(L[i][i].a))
      for j in range(i+1,d):
        num=A[j][i]-sum((L[j][k]*L[i][k] for k in range(i)),zero)
        L[j][i]=num/L[i][i]
    ld_out+=2*sum((iv.ln(L[i][i]) for i in range(d)),zero)

ld_tau=sum((iv.ln(one+iv.mpf(1000)/iv.mpf(2**(n+1))) for n in range(M+1)),zero)
# Thermal determinant beyond n=M is <= t sum_{n>=M+1} 2^(-n-1)=t*2^(-M-1).
gap=ld_out-ld_tau
B=exact_tail_B(M)
tailprob_upper=B*B
logdet_output_tail=Fraction(2*t,1)*B
logdet_thermal_tail=Fraction(t,2**(M+1))
cut_error_exact=logdet_output_tail+logdet_thermal_tail
cut_error_iv=iv.mpf(cut_error_exact.numerator)/iv.mpf(cut_error_exact.denominator)
# Parse interval endpoints to floats solely for a readable combined bound.
lo=float(gap.a);hi=float(gap.b)
full_lo=gap-cut_error_iv
full_hi=gap+cut_error_iv
assert float(full_hi.b)<0
result={"dps":iv.dps,"M":M,"t":t,"finite_gap_interval":str(gap),"finite_gap_interval_lower_float":lo,
        "finite_gap_interval_upper_float":hi,"output_omitted_vector_norm_upper_rational":str(B),
        "output_omitted_vector_norm_upper_decimal":str(float(B)),"output_tail_probability_upper_rational":str(tailprob_upper),
        "trace_norm_rho_truncation_upper_decimal":str(float(2*B)),
        "thermal_logdet_tail_upper_rational":str(logdet_thermal_tail),"combined_logdet_tail_bound_rational":str(cut_error_exact),
        "combined_logdet_tail_bound_decimal":str(float(cut_error_exact)),"full_gap_lower_interval":str(full_lo.a),
        "full_gap_upper_interval":str(full_hi.b),"full_gap_upper_float_for_readability":float(full_hi.b),
        "min_cholesky_diagonal_interval_lower":min(pivot_lower)}
path=Path(__file__).with_name('counterexample_interval_results.json')
path.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
