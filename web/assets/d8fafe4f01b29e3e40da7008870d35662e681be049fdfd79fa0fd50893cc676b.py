"""Reproduce the collective-thermal-state noise-threshold diagnostics.

All tests in this file are newly implemented for this investigation.
Numerical diagnostics are not a proof or external verification.
Reproduction environment: Python 3.13.5; numpy, scipy, sympy versions in requirements.txt.
"""
from __future__ import annotations
import json, math, platform, sys
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from scipy import __version__ as scipy_version
from scipy.integrate import quad
from scipy.linalg import eigh
from scipy.special import logsumexp

I2 = np.eye(2, dtype=complex)
PAULI = [np.array([[0,1],[1,0]],complex),
         np.array([[0,-1j],[1j,0]],complex),
         np.diag([1.,-1.]).astype(complex)]


def spin_operators(n: int) -> list[NDArray[np.complex128]]:
    if not isinstance(n,int) or not 1 <= n <= 10:
        raise ValueError('Dense diagnostic supports integer 1 <= n <= 10.')
    out=[]
    for pauli in PAULI:
        a=np.zeros((2**n,2**n),complex)
        for i in range(n):
            term=np.array([[1]],complex)
            for j in range(n): term=np.kron(term, pauli/2 if i==j else I2)
            a+=term
        out.append(a)
    return out


def _langevin(x: NDArray[np.float64]) -> NDArray[np.float64]:
    z=np.asarray(x,dtype=float); out=np.empty_like(z); small=np.abs(z)<1e-3
    y=z[small]
    out[small]=y/3-y**3/45+2*y**5/945-y**7/4725
    y=z[~small]; out[~small]=1/np.tanh(y)-1/y
    return out


def _langevin_prime(x: NDArray[np.float64]) -> NDArray[np.float64]:
    z=np.asarray(x,dtype=float); out=np.empty_like(z); small=np.abs(z)<1e-3
    y=z[small]; out[small]=1/3-y*y/15+2*y**4/189-y**6/675
    y=z[~small]; e=np.exp(-2*np.abs(y)); out[~small]=1/y**2-4*e/(1-e)**2
    return out


def _log_sinhc(x: NDArray[np.float64]) -> NDArray[np.float64]:
    z=np.abs(np.asarray(x,dtype=float)); out=np.empty_like(z); small=z<1e-3
    y=z[small]; out[small]=y*y/6-y**4/180+y**6/2835-y**8/37800
    y=z[~small]; out[~small]=y-np.log(2*y)+np.log1p(-np.exp(-2*y))
    return out


def block_stats(M: NDArray[np.float64], beta: float):
    """log Z_j(beta), mean Jz, variance Jz, and <Jx^2>, j=M/2."""
    M=np.asarray(M,dtype=float); L=M+1; j=M/2
    if beta==0:
        v=j*(j+1)/3
        return np.log(L),np.zeros_like(M),v,v
    x=abs(beta)/2
    logz=np.log(L)+_log_sinhc(L*x)-_log_sinhc(np.array(x))
    mean=-np.sign(beta)*(L*_langevin(L*x)-_langevin(np.array(x)))/2
    var=(L*L*_langevin_prime(L*x)-_langevin_prime(np.array(x)))/4
    # Use direct finite sums to suppress subtraction cancellation at tiny blocks.
    for ii in np.flatnonzero(M<=12):
        m=np.arange(int(M[ii])+1,dtype=float)-j[ii]
        p=np.exp(-beta*m-logsumexp(-beta*m))
        mean[ii]=p@m; var[ii]=p@(m-mean[ii])**2
    x2=(j*(j+1)-mean**2-var)/2
    return logz,mean,np.maximum(var,0),x2


def spin_weights(n: int, cutoff: float=16.0):
    """Exact relative Schur weights, truncated only for n with long tails.

    w(M+2)/w(M)=((M+3)/(M+1))^2*(n-M)/(n+M+4).
    The returned tail upper bound is the conservative Hoeffding bound
    (M_next+3)*exp(-M_next^2/(2*n)), clipped at 1.
    """
    if not isinstance(n,int) or n<1: raise ValueError('n must be a positive integer')
    first=n%2
    last=min(n, int(math.ceil(cutoff*math.sqrt(n))))
    last-= (last-first)%2
    M=np.arange(first,last+1,2,dtype=float)
    logw=np.zeros(len(M),float)
    if len(M)>1:
        m=M[:-1]
        logw[1:]=np.cumsum(2*np.log((m+3)/(m+1))+np.log((n-m)/(n+m+4)))
    logw-=logsumexp(logw)
    nxt=last+2
    logtail=-math.inf if last==n else min(0.,math.log(nxt+3)-nxt*nxt/(2*n))
    return M,logw,logtail


def exact_depolarized_filtered_moments(n:int, nu:float, lam:float, t:float, cutoff:float=16.):
    """Finite-n sector formula; filter exp[t Jz/(2 sqrt(n))].

    Reports (sum_a Var(Ja))/n after normalization, the unnormalized
    filter moment, and physical all-success probability in logarithms.
    This is NOT a sampled diffusion or a Gaussian approximation.
    """
    if not nu>0: raise ValueError('This finite-temperature diagnostic requires nu>0.')
    if not 0<=lam<=1: raise ValueError('lam must lie in [0,1].')
    if not math.isfinite(t): raise ValueError('t must be finite.')
    M,logw,logtail=spin_weights(n,cutoff)
    beta=math.log1p(1/nu); h=t/math.sqrt(n)
    A=1+(1-lam*lam)*math.sinh(h/2)**2
    Ap=(1-lam*lam)*math.sinh(h)/2
    App=(1-lam*lam)*math.cosh(h)/2
    b=2*math.atanh(lam*math.tanh(h/2)) if lam<1 else h
    bp=lam/A; bpp=-lam*Ap/(A*A)
    logz0,*_=block_stats(M,beta)
    logz,m,v,x2=block_stats(M,beta-b)
    lw=logw+logz-logz0; lnorm=float(logsumexp(lw)); p=np.exp(lw-lnorm)
    mean_o=float(p@m); var_o=float(p@(v+(m-mean_o)**2)); x2_o=float(p@x2)
    var_z=n*(App*A-Ap*Ap)/(2*A*A)+bp*bp*var_o+bpp*mean_o
    x2_out=n/4+(lam*lam/A)*(x2_o-n/4)
    mean_z=n*Ap/(2*A)+bp*mean_o
    logmgf=n*math.log(A)/2+lnorm
    # The original tail bound alone does not control a postselected state.
    # For the positive tilt / beta-b>0 regime used in the truncated tests,
    # bound the reweighted omitted mass before quoting a filtered tail.
    filtered_logtail=None
    filtered_tail_zero=logtail == -math.inf
    if not filtered_tail_zero and b>=0 and beta-b>0 and logtail<0:
        upper=math.exp(logtail); next_M=float(M[-1]+2)
        filtered_logtail=min(0.,logtail-b*next_M/2
            -math.log(-math.expm1(-(beta-b)))-math.log1p(-upper)-lnorm)
    return {'n':n,'nu':nu,'lambda':lam,'t':t,
            'variance_sum_per_n':(2*x2_out+var_z)/n,
            'variance_x_per_n':x2_out/n, 'variance_z_per_n':var_z/n,
            'mean_z_over_sqrt_n':mean_z/math.sqrt(n),
            'log_unnormalized_filter_moment':logmgf,
            'log_physical_success_probability':logmgf-abs(t)*math.sqrt(n)/2,
            'schur_tail_log_upper_bound':None if logtail == -math.inf else logtail,
            'schur_tail_exactly_zero':logtail == -math.inf,
            'filtered_sector_tail_log_upper_bound':filtered_logtail,
            'filtered_sector_tail_exactly_zero':filtered_tail_zero,
            'included_spin_sectors':len(M)}


def maxwell_tilt(b: float):
    """Mean and variance for density proportional x^2 exp(-x^2/2-b*x)."""
    if b<0: raise ValueError('Only nonnegative tilt is needed.')
    # x=z/(1+b) keeps quadrature on an O(1) scale even for large b.
    s=1+b
    vals=[quad(lambda z,k=k: z**(k+2)*math.exp(-z*z/(2*s*s)-b*z/s),
               0,np.inf,epsabs=2e-12,epsrel=2e-12)[0]/s**(k+3) for k in range(3)]
    mean=vals[1]/vals[0]; var=vals[2]/vals[0]-mean*mean
    mgf=math.sqrt(2/math.pi)*vals[0]
    return mean,var,mgf


def limit_variance(lam: float,t:float):
    mean,var,mgf=maxwell_tilt(lam*t/2)
    return 3*(1-lam*lam)/4+(lam*lam/4)*var


def stationary_dense(n:int,nu:float,spins=None):
    if nu<=0: raise ValueError('nu must be positive in dense finite-temperature check.')
    J=spin_operators(n) if spins is None else spins
    C=sum(a@a for a in J)
    vals,U=eigh(C)
    j=np.round(2*(np.sqrt(1+4*np.maximum(vals,0))-1)/2)/2
    M=2*j
    beta=math.log1p(1/nu)
    logz,*_=block_stats(M,beta)
    f=(M+1)*np.exp(-logz)
    F=(U*f)@U.conj().T
    m=np.diag(J[2]).real
    e=np.exp(-beta*m/2)
    rho=(e[:,None]*F)*e[None,:]/2**n
    return (rho+rho.conj().T)/2,J


def local_channel(rho:NDArray[np.complex128],n:int,probs):
    """Apply a supplied Pauli channel at every site, without 4**n Kraus enumeration."""
    probs=np.asarray(probs,float)
    if probs.shape!=(4,) or min(probs)<-1e-14 or not np.isclose(sum(probs),1):
        raise ValueError('Pauli probabilities must be nonnegative and sum to one.')
    out=rho.copy()
    for i in range(n):
        terms=[]
        for pauli in [I2]+PAULI:
            op=np.array([[1]],complex)
            for k in range(n): op=np.kron(op,pauli if k==i else I2)
            terms.append(op@out@op.conj().T)
        out=sum(p*a for p,a in zip(probs,terms))
    return out


def dense_filter_moments(rho,J,t):
    n=int(round(math.log2(len(rho))))
    m=np.diag(J[2]).real; e=np.exp(t*m/(2*math.sqrt(n)))
    rr=(e[:,None]*rho)*e[None,:]; z=float(np.trace(rr).real); rr/=z
    means=np.array([np.trace(rr@a).real for a in J])
    variances=np.array([np.trace(rr@(a@a)).real for a in J])-means**2
    return float(sum(variances)/n),means/math.sqrt(n),z


def partial_transpose(rho,n,sites):
    axes=list(range(2*n))
    for i in sites: axes[i],axes[n+i]=axes[n+i],axes[i]
    return rho.reshape([2]*(2*n)).transpose(axes).reshape(rho.shape)


def symbolic_tests():
    import sympy as sp
    x,nu=sp.symbols('x nu',real=True)
    tests=0
    for M in range(1,13):
        b=nu-(M+2*nu)*x+(M-1)*x*x
        D=x*(1-x)*(nu+x)
        Bs=[sp.binomial(M,k)*x**k*(1-x)**(M-k) for k in range(M+1)]
        for k,B in enumerate(Bs):
            rhs=-(nu*(M-k)*(k+1)+(nu+1)*k*(M-k+1))*B
            if k>0: rhs+=nu*(M-k+1)*k*Bs[k-1]
            if k<M: rhs+=(nu+1)*(k+1)*(M-k)*Bs[k+1]
            assert sp.expand(b*sp.diff(B,x)+D*sp.diff(B,x,2)-rhs)==0
            tests+=1
    return tests


def run():
    out={'status':'new internal numerical/symbolic checks; no external validation',
         'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy_version}
    out['exact_symbolic_bernstein_identities']=symbolic_tests()
    from fractions import Fraction
    exact_lam=Fraction(29,50); exact_t=100
    upper=3*(1-exact_lam**2)/4+Fraction(12,exact_t**2)
    assert upper==Fraction(4989,10000) and upper<Fraction(1,2)
    out['rational_asymptotic_filter_example']={
        'lambda':str(exact_lam),'t':exact_t,'variance_limit_upper_bound':str(upper),
        'separable_bound':'1/2','strict_margin':str(Fraction(1,2)-upper),
        'scope':'Exact arithmetic for a proved asymptotic bound, not an explicit finite-N threshold.'}

    dense=[]; maxerr=0.; mindense=1.; minppt=1.
    for n in range(2,8):
        for nu in [0.2,1.,3.]:
            rho,J=stationary_dense(n,nu)
            assert abs(np.trace(rho)-1)<2e-12
            mindense=min(mindense,float(np.linalg.eigvalsh(rho).min()))
            minppt=min(minppt,float(np.linalg.eigvalsh(partial_transpose(rho,n,[0])).min()))
            for lam in [1/math.sqrt(3),0.58,0.7,1.]:
                probs=[(1+3*lam)/4]+[(1-lam)/4]*3
                rn=local_channel(rho,n,probs)
                for t in [0.,0.3,1.7]:
                    got,means,z=dense_filter_moments(rn,J,t)
                    formula=exact_depolarized_filtered_moments(n,nu,lam,t)
                    err=abs(got-formula['variance_sum_per_n']); maxerr=max(maxerr,err)
                    assert err<2e-10,(n,nu,lam,t,got,formula)
                    assert abs(math.log(z)-formula['log_unnormalized_filter_moment'])<2e-10
                    dense.append({'n':n,'nu':nu,'lambda':lam,'t':t,'abs_error':err})
    out['dense_formula_checks']={'count':len(dense),'max_abs_error':maxerr,
         'min_input_eigenvalue':mindense,'min_singleton_PT_eigenvalue':minppt}
    rng=np.random.default_rng(8102026)
    S=np.outer(np.array([0,1,-1,0],complex)/math.sqrt(2),
               np.array([0,1,-1,0],complex)/math.sqrt(2))
    pairerr=0.
    for _ in range(500):
        p=rng.dirichlet(np.ones(4))
        ls=np.array([p[0]+p[1]-p[2]-p[3],p[0]-p[1]+p[2]-p[3],p[0]-p[1]-p[2]+p[3]])
        tau=local_channel(S,2,p)
        mineig=float(np.linalg.eigvalsh(partial_transpose(tau,2,[0])).min())
        prediction=(1-float(ls@ls))/4
        # This expression is the smallest PT eigenvalue for same-channel singlet outputs.
        pairerr=max(pairerr,abs(mineig-prediction))
        assert abs(mineig-prediction)<2e-13
    out['pauli_pair_PPT_checks']={'count':500,'max_abs_error':pairerr}
    cases=[]
    for lam,t in [(1/math.sqrt(3),50.),(0.58,50.),(0.59,25.),(0.6,18.),(0.62,12.),(0.7,0.)]:
        lim=limit_variance(lam,t)
        for n in [100,10000,1000000,100000000]:
            r=exact_depolarized_filtered_moments(n,1.,lam,t)
            r['limiting_variance_sum_per_n']=lim
            cases.append(r)
    out['large_n_diagnostics']=cases
    out['tilted_gamma_second_moment_bound_checks']=[]
    for b in [0.1,0.5,1,2,5,10,50,100]:
        mean,var,_=maxwell_tilt(b)
        bound=12/(b*b)
        assert var+mean*mean<=bound*(1+1e-10)
        out['tilted_gamma_second_moment_bound_checks'].append({'b':b,'second_moment':var+mean*mean,'bound':bound})
    Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    print(json.dumps(out['dense_formula_checks'],indent=2))
    print(json.dumps(out['pauli_pair_PPT_checks'],indent=2))
    print('symbolic Bernstein identities:',out['exact_symbolic_bernstein_identities'])
    for r in cases:
        if r['n']==100000000: print({k:r[k] for k in ['n','lambda','t','variance_sum_per_n','limiting_variance_sum_per_n']})
    return out

if __name__=='__main__': run()
