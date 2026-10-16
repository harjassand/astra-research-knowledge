"""Rigorously computable unweighted TT l1 upper bounds (possibly loose).

These helpers do not construct a full residual or certify missing construction
errors. They avoid normalized product denominators and require no positivity of
the represented tensor. No actual candidate contraction was run with them.
"""
from decimal import Decimal, Context, ROUND_CEILING
from fractions import Fraction
import numpy as np

def absolute_core_l1_upper(cores, precision=80):
    """Return exact rational upper endpoint of sum over absolute TT paths.

    For T(n)=G1[n1]...Gd[nd], ||T||1 <= (sum_n |G1[n]|)...
    (sum_n |Gd[n]|). Entrywise absolute value is before matrix contraction.
    All binary64 input entries are treated as exact dyadics.
    """
    up=Context(prec=precision,rounding=ROUND_CEILING,Emin=-999999999,Emax=999999999)
    row=[Decimal(1)]
    for core in cores:
        if core.dtype!=np.float64 or not np.isfinite(core).all(): raise ValueError('Need finite binary64 cores')
        if core.shape[0]!=len(row): raise ValueError('Invalid TT ranks')
        new=[]
        for j in range(core.shape[2]):
            value=Decimal(0)
            for i,weight in enumerate(row):
                if not weight: continue
                total=Decimal(0)
                for x in core[i,:,j]: total=up.add(total,Decimal.from_float(abs(float(x))))
                value=up.add(value,up.multiply(weight,total))
            new.append(value)
        row=new
    if len(row)!=1: raise ValueError('Need terminal rank 1')
    return Fraction(row[0])

def bernstein_integral_upper(bernstein_coefficient_tts,h,construction_error_integral,precision=80):
    """Upper bound for R(u)=sum_k B_{k,K}(u) V_k plus an accounted error.

    The caller must provide a proved nonnegative integral-l1 upper bound for
    every error incurred constructing the supplied V_k. Zero is legitimate
    only when those exact saved tensors really are the full residual
    coefficients. This function does not check that representation assertion.
    """
    h=Fraction(h); error=Fraction(construction_error_integral)
    if h<0 or error<0 or not bernstein_coefficient_tts: raise ValueError('Invalid inputs')
    return h*sum((absolute_core_l1_upper(g,precision) for g in bernstein_coefficient_tts),Fraction(0))/len(bernstein_coefficient_tts)+error
