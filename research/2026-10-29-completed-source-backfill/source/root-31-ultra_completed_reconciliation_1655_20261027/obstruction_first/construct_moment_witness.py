"""Construct an actual finite counting spectrum, not a weighted-measure fit.

The J sector is forced to have two equal largest eigenvalues v>1. All remaining
eigenvalues have modulus <v. N has three identical copies. Their moments are
matched to the acquired I/P thermal trace boxes at n=4,...,8, at one beta.
This is an obstruction to inference from these finite inputs, NOT an alternative
local Heisenberg Hamiltonian or a temperature-consistent counterexample.
"""
from __future__ import annotations
import pathlib,sys,json,math
from fractions import Fraction as F
import moment_attack as ma
import numpy as np
from scipy.optimize import linprog,least_squares
import mpmath as mp
mp.mp.dps=90
ROOT=pathlib.Path(__file__).resolve().parent


def fit(target,forced,cap,seed):
    rng=np.random.default_rng(seed)
    ns=np.arange(4,9);ys=np.array([float(target[int(n)])for n in ns])
    fixed=np.array([sum(mult*x**int(n)for mult,x in forced)for n in ns])
    remaining=ys-fixed
    grid=np.linspace(-cap,cap,501);grid=grid[np.abs(grid)>.015]
    mat=grid[None,:]**ns[:,None]
    scale=np.maximum(np.abs(remaining),1.)
    # A small deterministic cost perturbation selects a nondegenerate basic
    # feasible solution. Counts are continuous only during this search.
    lp=linprog(1+1e-4*rng.random(len(grid)),A_eq=mat/scale[:,None],b_eq=remaining/scale,bounds=(0,None),method='highs')
    assert lp.success,lp.message
    take=np.flatnonzero(lp.x>1e-6);counts=np.ceil(lp.x[take]).astype(np.int64)
    x0=grid[take]*(lp.x[take]/counts)**.25
    def residual(x):return (np.sum(counts[None,:]*x[None,:]**ns[:,None],axis=1)-remaining)/scale
    def jac(x):return counts[None,:]*ns[:,None]*x[None,:]**(ns[:,None]-1)/scale[:,None]
    ls=least_squares(residual,x0,jac=jac,bounds=(-cap,cap),xtol=2e-15,ftol=2e-15,gtol=2e-15,max_nfev=5000,x_scale='jac')
    assert np.max(np.abs(residual(ls.x)))<1e-8,(ls.message,residual(ls.x))
    assert len(counts)==5,(len(counts),counts)
    goals=[mp.mpf(target[n].numerator)/target[n].denominator-sum(mp.mpf(mult)*mp.mpf(str(x))**n for mult,x in forced)for n in range(4,9)]
    def equations(*xs):return tuple(sum(int(c)*x**n for c,x in zip(counts,xs))-goal for n,goal in zip(range(4,9),goals))
    roots=mp.findroot(equations,tuple(mp.mpf(float(x))for x in ls.x),tol=mp.mpf('1e-80'),maxsteps=150)
    # Exact rational eigenvalues, with integer multiplicities. No fractional
    # spectral weights or numerical root claims enter the final verification.
    den=10**36
    spectrum=[(int(mult),F(str(x)))for mult,x in forced]
    for c,x in zip(counts,roots):spectrum.append((int(c),F(int(mp.nint(x*den)),den)))
    assert all(abs(x)<F(str(cap))for c,x in spectrum[len(forced):])
    moments={n:sum(c*x**n for c,x in spectrum)for n in range(4,9)}
    return spectrum,moments


def run(diagnostic=False):
    boxes={};centers={}
    for n in range(4,9):
        for p in range(2):
            path=ROOT/f'data/trace_n{n}_p{p}_b12.json'
            if diagnostic:
                j=json.loads((ROOT/f'data/spin2_n{n}_p{p}.json').read_text());z=ma.partition(j,mp.mpf(12),mp.mpf('4.76124816'));centers[n,p]=F(str(z))
            else:
                j=json.loads(path.read_text());assert j['status']=='DIRECTED_SCALAR_ENCLOSURE_UNDER_DECLARED_IEEE_MATRIX_MODEL'
                lo,hi=F(j['trace_lower']),F(j['trace_upper']);boxes[n,p]=(lo,hi);centers[n,p]=(lo+hi)/2
    J={n:(centers[n,0]+3*centers[n,1])/4 for n in range(4,9)}
    N={n:(centers[n,0]-centers[n,1])/4 for n in range(4,9)}
    sj,mj=fit(J,[(2,1.1)],1.09,271027)
    sn,mn=fit(N,[],1.09,271028)
    checks=[]
    for n in range(4,9):
        for p,moment in [(0,mj[n]+3*mn[n]),(1,mj[n]-mn[n])]:
            lo,hi=boxes[n,p] if not diagnostic else (centers[n,p]-F(1,10**12),centers[n,p]+F(1,10**12))
            assert lo<moment<hi,(n,p,float(moment-lo),float(hi-moment))
            checks.append({'n':n,'twist':p,'moment':str(moment),'lower':str(lo),'upper':str(hi),'lower_margin':str(moment-lo),'upper_margin':str(hi-moment)})
    answer={'status':'EXACT_RATIONAL_WITNESS_INSIDE_VALIDATED_TRACE_BOXES' if not diagnostic else 'DIAGNOSTIC_ONLY','beta':'12','shift':'4.76124816','J_spectrum':[{'multiplicity':c,'eigenvalue':str(x)}for c,x in sj],'N_spectrum_one_copy':[{'multiplicity':c,'eigenvalue':str(x)}for c,x in sn],'dimension_J':sum(c for c,x in sj),'dimension_N_one_copy':sum(c for c,x in sn),'largest_eigenvalue':'11/10','largest_multiplicity':2,'checks':checks,'scope':__doc__}
    file=ROOT/('data/moment_counting_witness_diagnostic.json' if diagnostic else 'data/moment_counting_witness.json');file.write_text(json.dumps(answer,indent=2))
    print(answer['status'],'dimensionJ',answer['dimension_J'],'dimensionN',answer['dimension_N_one_copy']);print('J',[(c,float(x))for c,x in sj]);print('N',[(c,float(x))for c,x in sn]);print('min enclosure margin',min(float(min(F(x['lower_margin']),F(x['upper_margin'])))for x in checks))
    return answer


if __name__=='__main__':run('--diagnostic' in sys.argv)
