"""Exact tests and labelled floating diagnostics for spectral extrapolation.

Run: python verify.py
The assertions check finite instances; they do not validate general proofs or novelty.
No Hamiltonian learning samples are simulated or claimed to have been acquired.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import comb, factorial, ceil, log2
from pathlib import Path
import json
import numpy as np
import mpmath as mp

OUT = Path(__file__).resolve().parent
exact_count = 0

def check(statement: bool, message: str) -> None:
    global exact_count
    if not statement:
        raise AssertionError(message)
    exact_count += 1


def spectral_pair(m: int):
    if m < 1 or m % 2 != 1:
        raise ValueError('m must be a positive odd integer')
    n = m + 1
    x = [F(3, 8) + F(k, 4*m) for k in range(n)]
    # 1/4 uniform spectrum + 1/4 uniform even spectrum + 1/2 binomial parity.
    wplus, wminus = [], []
    for k in range(n):
        base = F(1, 4*n) + (F(1, 2*n) if k % 2 == 0 else F(0))
        extra = F(comb(m,k), 2**m)
        wplus.append(base + (extra if k % 2 == 0 else 0))
        wminus.append(base + (extra if k % 2 == 1 else 0))
    return x, wplus, wminus


def jacobi(x, w):
    """Exact diagonals and squared positive couplings via monic polynomials."""
    n = len(x)
    prev = [F(0)]*n
    cur = [F(1)]*n
    prev_norm = None
    a, b2 = [], []
    for j in range(n):
        norm = sum((wi*pi*pi for wi,pi in zip(w,cur)), F(0))
        check(norm > 0, 'positive polynomial norm')
        aj = sum((wi*xi*pi*pi for wi,xi,pi in zip(w,x,cur)), F(0))/norm
        bj2 = F(0) if j == 0 else norm/prev_norm
        a.append(aj)
        if j:
            b2.append(bj2)
        nxt = [(xi-aj)*pi-bj2*pp for xi,pi,pp in zip(x,cur,prev)]
        prev, cur, prev_norm = cur, nxt, norm
    check(all(v == 0 for v in cur), 'degree n polynomial vanishes at all eigenvalues')
    return a, b2


def matvec(a, b2, v):
    # Diagonal similarity of the symmetric Jacobi matrix: upper 1, lower b^2.
    n=len(a)
    out=[]
    for j in range(n):
        z=a[j]*v[j]
        if j: z+=b2[j-1]*v[j-1]
        if j+1<n: z+=v[j+1]
        out.append(z)
    return out


def exact_moments(a, b2, x, w, max_order):
    v=[F(1)]+[F(0)]*(len(a)-1)
    powers=[F(1)]*len(x)
    for degree in range(max_order+1):
        target=sum((wi*zi for wi,zi in zip(w,powers)), F(0))
        check(v[0] == target, f'Jacobi moment {degree}')
        v=matvec(a,b2,v)
        powers=[zi*xi for zi,xi in zip(powers,x)]


def ff(q):
    return mp.mpf(q.numerator)/q.denominator


def as_symmetric(a, b2):
    return np.diag([float(v) for v in a])-np.diag(np.sqrt([float(v) for v in b2]),1)-np.diag(np.sqrt([float(v) for v in b2]),-1)


def amplitude(H, t):
    ev, U=np.linalg.eigh(H)
    return np.sum(U[0,:]**2*np.exp(-1j*t*ev))


def main():
    global exact_count
    mp.mp.dps=180
    rows=[]
    models={}
    for m in [1,3,5,7,9,13,17,21]:
        x,wp,wm=spectral_pair(m)
        n=m+1
        check(sum(wp)==1 and sum(wm)==1, 'normalization')
        check(F(1,4)+F(3,4)*sum(wp)==1, 'ground-reference normalization')
        check(F(1,4)**2+(F(3,4)*F(3,4))**2==F(97,256), 'reference positive return')
        check(F(1,4)**2+(F(3,4)*F(1,4))**2==F(25,256), 'reference negative return')
        for k in range(n):
            check(wp[k]>=F(1,4*n) and wm[k]>=F(1,4*n), 'spectral weight floor')
            check(F(3,4)*min(wp[k],wm[k])>=F(3,16*n), 'reference spectral weight floor')
            check(wp[k]-wm[k]==F((-1)**k*comb(m,k),2**m), 'finite-difference coefficient')
        for degree in range(m):
            check(sum((wp[k]-wm[k])*x[k]**degree for k in range(n))==0, 'matching low-order moment')
        first=sum((wp[k]-wm[k])*x[k]**m for k in range(n))
        check(first==F(-factorial(m),(8*m)**m), 'first different moment')
        check(sum(wp[k]*(-1)**k for k in range(n))==F(3,4), 'positive real-time amplitude')
        check(sum(wm[k]*(-1)**k for k in range(n))==F(-1,4), 'negative real-time amplitude')
        ap,bp=jacobi(x,wp); am,bm=jacobi(x,wm)
        exact_moments(ap,bp,x,wp,2*n+1)
        exact_moments(am,bm,x,wm,2*n+1)
        r=(m+1)//2
        check(ap[:r-1]==am[:r-1], 'common near-end diagonal')
        check(bp[:r-1]==bm[:r-1], 'common near-end couplings')
        for a in ap+am:
            check(F(3,8)<=a<=F(5,8), 'diagonal spectral interval')
        lower=F(1,4*m)**2/F(36*n)
        for b in bp+bm:
            check(lower<=b<=1, 'polynomial lower coupling bound')
        Hplus=as_symmetric(ap,bp); Hminus=as_symmetric(am,bm)
        t=4*np.pi*m
        vp=amplitude(Hplus,t); vm=amplitude(Hminus,t)
        assert abs(abs(vp)**2-9/16)<2e-11
        assert abs(abs(vm)**2-1/16)<2e-11
        totalp=0.25+0.75*vp; totalm=0.25+0.75*vm
        assert abs(abs(totalp)**2-97/256)<2e-11
        assert abs(abs(totalm)**2-25/256)<2e-11
        lap=[]
        for beta in [mp.mpf('0.25'),mp.mpf('1'),mp.mpf(m),mp.mpf(10*m)]:
            actual=sum((ff(wp[k])-ff(wm[k]))*mp.exp(-beta*ff(x[k])) for k in range(n))
            formula=mp.exp(-3*beta/8)*((1-mp.exp(-beta/(4*m)))/2)**m
            assert abs(actual-formula)<mp.mpf('1e-150')
            lap.append({'beta':str(beta),'difference':mp.nstr(formula,12)})
        maxbits=max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in ap+am+bp+bm)
        rows.append({'m':m,'sites':n,'time_over_pi':4*m,'max_exact_coefficient_bits':maxbits,
                     'minimum_hopping_squared':str(min(bp+bm)) if bp else None,
                     'bulk_return_probabilities':[float(abs(vp)**2),float(abs(vm)**2)],
                     'reference_return_probabilities':[float(abs(totalp)**2),float(abs(totalm)**2)],
                     'high_precision_laplace_checks':lap})
        if m in [3,7]:
            models[str(m)]={'nodes':list(map(str,x)), 'wplus':list(map(str,wp)), 'wminus':list(map(str,wm)),
                           'plus_diagonal':list(map(str,ap)), 'plus_hopping_squared':list(map(str,bp)),
                           'minus_diagonal':list(map(str,am)), 'minus_hopping_squared':list(map(str,bm))}
    # Exact preservation of moment matching by shared tridiagonal perturbations,
    # using a diagonal perturbation to keep squared-coupling encoding rational.
    perturb=[]
    for m in [3,5,7,9,13]:
        x,wp,wm=spectral_pair(m)
        ap,bp=jacobi(x,wp); am,bm=jacobi(x,wm)
        eps=F(1,1024*m)  # < 1/(64 * (4*pi*m))
        ed=[eps*F((-1)**j*(j+1),m+1) for j in range(m+1)]
        ap2=[a+e for a,e in zip(ap,ed)]; am2=[a+e for a,e in zip(am,ed)]
        vp=[F(1)]+[F(0)]*m; vm=vp.copy()
        for j in range(m):
            check(vp[0]==vm[0], 'perturbed matching moment')
            vp=matvec(ap2,bp,vp); vm=matvec(am2,bm,vm)
        Hp=as_symmetric(ap2,bp); Hm=as_symmetric(am2,bm)
        assert np.linalg.eigvalsh(Hp).min()>1/3 and np.linalg.eigvalsh(Hm).min()>1/3
        assert np.linalg.eigvalsh(Hp).max()<2/3 and np.linalg.eigvalsh(Hm).max()<2/3
        t=4*np.pi*m
        gap=abs(amplitude(Hp,t))**2-abs(amplitude(Hm,t))**2
        assert gap>3/8
        totalgap=abs(0.25+0.75*amplitude(Hp,t))**2-abs(0.25+0.75*amplitude(Hm,t))**2
        assert totalgap>7/32
        perturb.append({'m':m,'perturbation_norm':float(max(map(abs,ed))), 'bulk_return_probability_gap':float(gap), 'reference_return_probability_gap':float(totalgap)})
    # General reconstruction: high-precision diagnostics, not exact assertions.
    recon=[]
    mp.mp.dps=300
    for T,B in [(1,F(1,8)),(2,F(1)),(4,F(100)),(8,F(1))]:
        M=ceil(16*T)
        a=min(B/F(M),F(1,16))
        # Working precision is charged to the proven coefficient amplification.
        mp.mp.dps=60
        logS=mp.log10(2)+M*mp.log10(2*mp.e*(1+mp.mpf(T)/(ff(a)*M)))
        work_digits=int(mp.ceil(logS))+200
        mp.mp.dps=work_digits
        aa=ff(a)
        R=mp.mpf(T)/aa
        c=[mp.mpc(1)]
        for j in range(M): c.append(c[-1]*(j-1j*R)/(j+1))
        weights=[sum(c[j]*comb(j,l) for j in range(l,M+1))*(-1)**l for l in range(M+1)]
        S=sum(abs(v) for v in weights)
        Sbound=2*(2*mp.e*(1+mp.mpf(T)/(aa*M)))**M
        assert S<=Sbound
        error=mp.mpf(0)
        coeff_error=mp.mpf(0)
        for j in range(65):
            x=mp.mpf(j)/64
            z=1-mp.exp(-aa*x)
            direct=sum(c[k]*z**k for k in range(M+1))
            synth=sum(weights[k]*mp.exp(-aa*k*x) for k in range(M+1))
            error=max(error,abs(direct-mp.exp(-1j*T*x)))
            coeff_error=max(coeff_error,abs(synth-direct))
        assert error<=mp.mpf(2)**(-M)
        assert coeff_error<mp.mpf('1e-140')
        recon.append({'T':T,'B':str(B),'degree':M,'spacing':str(a),'working_decimal_digits':work_digits,
                      'log10_actual_l1':mp.nstr(mp.log10(S),12),
                      'log10_upper_l1':mp.nstr(mp.log10(Sbound),12),
                      'max_grid_bias':mp.nstr(error,12),
                      'proven_bias_bound':mp.nstr(mp.mpf(2)**(-M),12),
                      'algebra_consistency':mp.nstr(coeff_error,6)})
    result={'status':'Finite checks only; not independent review, formal verification, or novelty clearance.',
            'exact_assertions_passed':exact_count,
            'exact_pair_instances':rows,
            'perturbation_diagnostics':perturb,
            'reconstruction_diagnostics':recon}
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'exact_models.json').write_text(json.dumps(models,indent=2)+'\n')
    print(json.dumps({'exact_assertions_passed':exact_count,
                      'spectral_pair_instances':len(rows),
                      'perturbation_instances':len(perturb),
                      'reconstruction_instances':len(recon)},indent=2))

if __name__=='__main__':
    main()
