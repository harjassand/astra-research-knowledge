"""Exact rational kernel enclosures; no sampled trajectories or native data.

For gamma=tau=1 and integer frequency n, lambda=n*n. Integration by
parts of the incomplete-gamma expression yields the positive series
I_n=sum_{j>=0} lambda**j * lambda!/(lambda+j+1)!.
The omitted tail is bounded by a geometric series with decreasing ratios.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import hashlib
import json

def kernel(n, tol=F(1,10**24)):
    if n==0:return F(1),F(1),0
    lam=n*n; term=F(1,lam+1); total=term; j=0
    while True:
        nxt=term*F(lam,lam+j+2)
        tail=nxt/(1-F(lam,lam+j+3))
        if tail<=tol:return total,total+tail,j+1
        total+=nxt;term=nxt;j+=1
        if j>20000:raise RuntimeError('unexpected series cost')

def dec(x,up=False):
    with localcontext() as c:
        c.prec=28;c.rounding=ROUND_CEILING if up else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def interval(lo,hi):return [dec(lo),dec(hi,True)]

def main():
    rows=[]; kernels={}
    for n in [0,1,2,3,4,8,16,32,64]:
        lo,hi,terms=kernel(n);kernels[n]=(lo,hi)
        # Weaker rational c=1/5 is below exp(-3/2).
        assert lo>=F(1,5*(1+n))
        assert hi<=F(5,1+n)
        if n==0:continue
        slo,shi=lo/2,hi/2
        rows.append({'n':n,'kernel':interval(lo,hi),
          'sigma_fixed_amplitude':interval(slo,shi),
          'n_sigma':interval(n*slo,n*shi),
          'native_equilibrium_kl_rate':'1/8',
          'same_initial_full_path_kl_h1':'1/8',
          'stationary_initial_kl_upper':dec(shi/2,True),
          'common_thermal_work_upper_h1':dec(shi,True),
          'native_tv_lower_force_cap1_h1':'1/96',
          'bandlimit_optimal_rate_constant':interval(1/(4*hi),1/(4*lo)),
          'necessary_gaussian_precision_budget_for_tv_0p1':interval(F(1,25)/shi,F(1,25)/slo),
          'sigma_for_lipschitz1_sine':interval(slo/(n*n),shi/(n*n)),
          'native_kl_for_lipschitz1_sine':str(F(1,8*n*n)),
          'terms':terms,'enclosure_width':dec(hi-lo,True),
          'denominator_bits':max(lo.denominator.bit_length(),hi.denominator.bit_length())})
    # Mixed spectrum, normalized Fourier energies (a sine has energy a^2/2).
    energies={0:F(1,25),1:F(1,8),3:F(1,18),8:F(1,128)}
    l2=sum(energies.values(),F(0))
    neg=sum((e/F(1+n) for n,e in energies.items()),F(0))
    reg=sum((e*(1+n)**2 for n,e in energies.items()),F(0))
    sig_lo=sum((e*kernels[n][0] for n,e in energies.items()),F(0))
    sig_hi=sum((e*kernels[n][1] for n,e in energies.items()),F(0))
    assert l2**3<=neg**2*reg
    assert neg<=5*sig_lo
    assert l2<=sig_lo/kernels[8][1]
    # Monotonicity at separated frequencies is verified by disjoint enclosures.
    ns=sorted(kernels)
    assert all(kernels[a][0]>kernels[b][1] for a,b in zip(ns,ns[1:]))
    report={'status':'PASS','date':'2026-10-29',
      'scope':'Exact rational series enclosures and finite controls; general theorems proved in accompanying notes. No physical observations or trajectory draws.',
      'units':{'amplitude':1,'gamma':1,'temperature':1,'horizon':1},
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'kernel_series':'sum_{j>=0} lambda^j lambda!/(lambda+j+1)!, lambda=n^2',
      'tail_bound':'next_term/(1-lambda/(lambda+j+3)) after including index j',
      'rows':rows,
      'mixed_spectrum':{'energies':{str(k):str(v) for k,v in energies.items()},
        'l2_squared':str(l2),'negative_norm_squared':str(neg),'weighted_h1_squared':str(reg),
        'sigma':interval(sig_lo,sig_hi),'holder_cubic_residual':str(neg**2*reg-l2**3)},
      'limitations':['No rate or information budget is acquired from a native system.',
       'Noise-budget lower bound is not claimed optimal.',
       'Printed rational constants concern the specified normalized source only.',
       'Approximate n*sigma values corroborate, and do not prove, the asymptotic limit.']}
    path=Path(__file__).with_name('THERMAL_INFORMATION_SPECTRUM_CHECKS.json')
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'script_sha256':report['script_sha256'],
      'rows':len(rows),'n64':rows[-1],'mixed_spectrum':report['mixed_spectrum']},indent=2))

if __name__=='__main__':main()
