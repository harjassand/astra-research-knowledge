"""Exact rational open5 lower energy; cold one-mode moment boundary.

Numerical Cholesky and solve only produce dyadic L,X. Every subsequent
product/inequality is integer/rational. sqrt(6) has rational endpoints.
"""
import pathlib,json,math,time
from fractions import Fraction as F
import numpy as np
import scipy.linalg as la
import mpmath as mp
from relative_order_bridge import pair,SLO,SHI
ROOT=pathlib.Path(__file__).resolve().parent
mp.iv.dps=90;iv=mp.iv
def hi(x):return math.nextafter(float(x.b),math.inf)
def lo(x):return math.nextafter(float(x.a),-math.inf)

def run():
    start=time.monotonic();n=5
    terms=[pair(n,i,i+1)for i in range(n-1)]
    h0=sum(x[0]for x in terms);h1=sum(x[1]for x in terms)
    words=np.array(list(np.ndindex(*(5,)*n)));inds=np.flatnonzero(np.sum(words-2,axis=1)==0)
    h0=h0[inds,:][:,inds].toarray();h1=h1[inds,:][:,inds].toarray();d=len(inds)
    a=F(4901,250)
    numeric=h0+np.sqrt(6)*h1+float(a)*np.eye(d)
    # Explicitly discard the unused returned triangle before exact replay.
    ell=np.tril(la.cholesky(numeric,lower=True,check_finite=False))
    inverse=la.solve_triangular(ell,np.eye(d),lower=True,check_finite=False)
    scale=2**40
    lint=np.rint(ell*scale).astype(np.int64);xint=np.rint(inverse*scale).astype(np.int64)
    L=lint.astype(object);X=xint.astype(object)
    LL=L@L.T;LX=L@X
    row=[0]*d;col=[0]*d
    for i in range(d):
        for j in range(d):
            z=abs((scale*scale if i==j else 0)-int(LX[i,j]))
            row[i]+=z;col[j]+=z
    rho=F(max(max(row),max(col)),scale*scale)
    print('dyadic inverse residual',float(rho),'numeric residual',float(np.linalg.norm(ell@inverse-np.eye(d))),flush=True)
    assert rho<1
    assert max(abs(int(z))for z in xint.flat)*d<2**62
    xnorm=F(max(int(np.sum(np.abs(xint),axis=0).max()),int(np.sum(np.abs(xint),axis=1).max())),scale)
    B=xnorm/(1-rho);errors=[]
    for i in range(d):
        r=F(0)
        for j in range(d):
            base=F(int(h0[i,j]))+(a if i==j else 0)-F(int(LL[i,j]),scale*scale)
            c=int(h1[i,j]);r+=max(abs(base+c*SLO),abs(base+c*SHI))
        errors.append(r)
    error=max(errors);margin=1/(B*B)-error;assert margin>0
    np.savez(ROOT/'data/open5_rational_cholesky.npz',L_numerator=lint,X_numerator=xint,denominator=np.array(scale,dtype=np.int64))
    # Anderson averaging: H_N=(1/4)sum translated H_open5 >=-4.901N.
    # Hence ||K_beta||<=5exp(4.901beta). Complete moments obey
    # TrK²>=exp(12beta), TrK⁴>=exp(20beta).
    rows=[];aa=iv.mpf(4901)/1000
    for beta in [1,12,64,96,128]:
        ratio=iv.exp((20-4*aa)*beta)/625
        rows.append({'beta':beta,'p2_effective_mass_ratio_lower':lo(iv.exp((12-2*aa)*beta)/25),
            'p4_effective_mass_ratio_lower':lo(ratio),
            'A4_invariant_p4_mass_ratio_lower':lo(ratio/12),
            'A4_rank_needed_for_residual_mass_below_one_mode_lower':lo(ratio/12-1)})
    result={'status':'EXACT_RATIONAL_LOCAL_ENERGY_AND_COLD_COUNT_OBSTRUCTION',
        'open_chain_sites':5,'magnetization_zero_dimension':d,
        'global_completeness':'SU2 invariance and integer total spins put an M=0 vector in every multiplet.',
        'physical_open5_lower_energy':str(-a),'dyadic_denominator':scale,
        'inverse_residual_operator_upper_rational':str(rho),'inverse_norm_upper_rational':str(B),
        'matrix_residual_operator_upper_rational':str(error),'positive_eigenvalue_margin_lower_rational':str(margin),
        'physical_global_ring_energy_per_bond_lower':'-4.901',
        'p4_no_single_mode_count_for_beta_greater_than':hi(iv.log(1250)/(20-4*aa)),
        'A4_p4_no_single_mode_count_for_beta_greater_than':hi(iv.log(15000)/(20-4*aa)),
        'rows':rows,'seconds':time.monotonic()-start,
        'scope':'Obstruction to this single-mode p2/p4 count even with an exact leading vector; not a no-go for larger moments, multiple modes, sector-aware compression or other MPO algorithms.'}
    (ROOT/'data/cold_moment_boundary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result

if __name__=='__main__':run()
