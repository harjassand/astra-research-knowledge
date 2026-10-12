#!/usr/bin/env python3
"""Reproducible floating-point falsification checks for thermal transport.

These checks are not interval certificates, formal proofs, or benchmarks of
large-system performance. The accompanying research_note.md gives the proofs.
Run: OPENBLAS_NUM_THREADS=1 python checks.py --output checks.json
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from scipy.integrate import quad, simpson, solve_ivp
from scipy.linalg import expm, expm_frechet

Mat = NDArray[np.complex128]
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)

def opnorm(a: Mat) -> float:
    return float(np.linalg.norm(a, 2))

def tracenorm(a: Mat) -> float:
    return float(np.sum(np.linalg.svd(a, compute_uv=False)))

def pauli(n: int, entries: dict[int, Mat]) -> Mat:
    out = np.ones((1, 1), dtype=complex)
    for j in range(n):
        out = np.kron(out, entries.get(j, I))
    return out

def embed_contiguous(a: Mat, n: int, first: int, k: int) -> Mat:
    return np.kron(np.eye(2**first), np.kron(a, np.eye(2**(n-first-k))))

def gibbs(h: Mat, beta: float) -> Mat:
    e, u = np.linalg.eigh(h)
    weights = np.exp(-beta * (e-e.min()))
    return (u * (weights/weights.sum())) @ u.conj().T

def phi(h: Mat, a: Mat, beta: float) -> Mat:
    e, u = np.linalg.eigh(h)
    gaps = beta * (e[:, None]-e[None, :]) / 2
    f = np.ones_like(gaps)
    np.divide(np.tanh(gaps), gaps, out=f, where=np.abs(gaps)>1e-13)
    return u @ (f * (u.conj().T @ a @ u)) @ u.conj().T

def transport(h: Mat, v: Mat, beta: float, rtol: float=2e-11) -> Mat:
    d = h.shape[0]
    def rhs(s: float, w: NDArray[np.complex128]) -> NDArray[np.complex128]:
        return (-beta/2 * phi(h+s*v, v, beta) @ w.reshape(d, d)).ravel()
    sol = solve_ivp(rhs, (0, 1), np.eye(d, dtype=complex).ravel(),
                    method='DOP853', rtol=rtol, atol=rtol/30)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:, -1].reshape(d, d)

def q_tail(t: NDArray[np.float64], beta: float) -> NDArray[np.float64]:
    odd = np.arange(1, 4096, 2, dtype=float)
    out = 8/np.pi**2 * (np.exp(-np.outer(t, odd)*np.pi/beta)/(odd**2)).sum(axis=1)
    out[t == 0] = 1.0
    return out

def make_chain(n: int) -> tuple[Mat, list[tuple[set[int], Mat]]]:
    terms: list[tuple[set[int], Mat]] = []
    for j in range(n):
        terms.append(({j}, (0.44+0.03*j)*pauli(n, {j:X}) +
                      (0.19-0.02*j)*pauli(n, {j:Z})))
    for j in range(n-1):
        for a, c in [(X, .35), (Y, .21), (Z, .28)]:
            terms.append(({j,j+1}, c*pauli(n,{j:a,j+1:a})))
    return sum((a for _, a in terms), np.zeros((2**n,2**n),complex)), terms

def reduce_patch(a: Mat, n: int, first: int, k: int) -> Mat:
    # All matrices passed here are identities on the complement. The 0,0
    # complement block therefore equals the patch operator exactly.
    ids = np.arange(2**k) * 2**(n-first-k)
    return a[np.ix_(ids, ids)]

def boundary_quadrature(h: Mat, v: Mat, boundary: list[Mat], beta: float,
                         n: int, first: int, k: int,
                         ns: int=13, nt: int=181) -> dict[str, float]:
    if not boundary:
        return {'L_numerical': 0.0, 'tail_upper_bound': 0.0,
                'eta_numerical': 0.0, 'time_cutoff': 0.0}
    vnorm = opnorm(v)
    tmax = beta/np.pi * math.log(max(2*vnorm,1)/1e-8)
    ts, ss = np.linspace(0,tmax,nt), np.linspace(0,1,ns)
    q = q_tail(ts,beta)
    svalues = []
    for s in ss:
        e,u = np.linalg.eigh(h+s*v)
        vm = u.conj().T @ v @ u
        gaps = e[:,None]-e[None,:]
        bs = []
        for t in ts:
            b = 0.0
            for sign in (-1,1):
                at = u @ (np.exp(sign*1j*t*gaps)*vm) @ u.conj().T
                full = embed_contiguous(at,n,first,k)
                b += .5*sum(opnorm(bi@full-full@bi) for bi in boundary)
            bs.append(b)
        svalues.append(simpson(q*np.asarray(bs), x=ts))
    tail = 2*vnorm*math.exp(-np.pi*tmax/beta)
    L = float(simpson(svalues,x=ss)) + tail
    return {'L_numerical': L, 'tail_upper_bound': tail,
            'eta_numerical': beta/2*L, 'time_cutoff': tmax}

def chain_checks() -> list[dict[str, float|int]]:
    n=5
    h,terms=make_chain(n)
    v=.4*pauli(n,{2:Z})+.25*pauli(n,{2:X})
    vn=opnorm(v)
    rows=[]
    for beta in (.5, 1., 2.):
        rho,target=gibbs(h,beta),gibbs(h+v,beta)
        w=transport(h,v,beta)
        scale=math.exp(-beta*vn/2)
        kg=scale*w
        kgout=kg@rho@kg.conj().T
        exact_id=tracenorm(kgout/np.trace(kgout)-target)
        for first,k in ((2,1),(1,3),(0,5)):
            r=set(range(first,first+k))
            hrfull=sum((a for supp,a in terms if supp<=r),np.zeros_like(h))
            bnd=[a for supp,a in terms if supp&r and not supp<=r]
            hr=reduce_patch(hrfull,n,first,k)
            vr=reduce_patch(v,n,first,k)
            kr=scale*transport(hr,vr,beta)
            krfull=embed_contiguous(kr,n,first,k)
            out=krfull@rho@krfull.conj().T
            p=float(np.trace(out).real)
            observed=tracenorm(out/p-target)
            delta=opnorm(kg-krfull)
            numerical=boundary_quadrature(hr,vr,bnd,beta,n,first,k)
            eta=numerical['eta_numerical']
            rows.append({'n':n,'patch_qubits':k,'beta':beta,
                         'w':2*vn,'success_probability':p,
                         'universal_success_floor':math.exp(-2*beta*vn),
                         'exact_transport_identity_error':exact_id,
                         'actual_operator_error':delta,
                         'state_trace_norm_error':observed,
                         'stability_bound_using_actual_operator_error':min(2.,2*delta/math.sqrt(p)),
                         'boundary_bound_numerical':min(2.,2*eta/math.sqrt(p)),
                         **numerical})
            tol=3e-8
            assert exact_id<tol
            assert observed<=2*delta/math.sqrt(p)+tol
            assert delta<=eta+tol
            assert p>=math.exp(-2*beta*vn)-tol
    return rows

def algebra_checks() -> dict[str,float|int]:
    rng=np.random.default_rng(20261012)
    worst_identity=0.
    worst_ratio=0.
    for _ in range(60):
        d=4
        def hermitian() -> Mat:
            a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
            return (a+a.conj().T)/6
        h,v,a=hermitian(),hermitian(),hermitian()
        beta=float(rng.uniform(.1,2.))
        e,de=expm_frechet(-beta*h,-beta*v,compute_expm=True)
        ph=phi(h,v,beta)
        rhs=-beta/2*(ph@e+e@ph)
        worst_identity=max(worst_identity,opnorm(de-rhs))
        # Moving-frame decomposition, with residual R=V-i[A,H].
        res=v-1j*(a@h-h@a)
        phr=phi(h,res,beta)
        gauge=1j*(a@e-e@a)-beta/2*(phr@e+e@phr)
        worst_identity=max(worst_identity,opnorm(de-gauge))
        k=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        k=k/(1.1*opnorm(k))
        kh=k+.04*(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
        kh=kh/max(1.,opnorm(kh))
        z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
        rho=z@z.conj().T; rho/=np.trace(rho)
        x=k@rho@k.conj().T; y=kh@rho@kh.conj().T
        p,q=float(np.trace(x).real),float(np.trace(y).real)
        delta=opnorm(k-kh)
        dist=tracenorm(x/p-y/q)
        bound=2*delta/math.sqrt(q)
        worst_ratio=max(worst_ratio,dist/bound)
        assert dist<=bound+1e-10
        assert abs(math.sqrt(p)-math.sqrt(q))<=delta+1e-10
    assert worst_identity<1e-9
    # Direct checks of the positive time-domain kernel and its first moment.
    def f(t: float) -> float:
        if t>100: return 0.
        x=np.pi*t/2
        return 2/np.pi*np.log1p(2/np.expm1(2*x))
    mass=2*quad(f,0,30,epsabs=1e-11)[0]
    moment=2*quad(lambda t:t*f(t),0,30,epsabs=1e-11)[0]
    return {'random_cases':60,'max_derivative_identity_operator_error':worst_identity,
            'max_postselection_error_to_bound_ratio':worst_ratio,
            'kernel_mass_beta_1':mass,'kernel_first_moment_beta_1':moment}

def lower_bound_checks() -> list[dict[str,float|int|str]]:
    out=[]
    # q=2^-k and exp(c)=2 make all reference and target probabilities rational.
    for k in (2,4,8,12,20):
        q=Fraction(1,2**k)
        refs=[]; ms=[]
        for ec in (Fraction(2),Fraction(1,2)):
            un=[Fraction(1),q,q/ec,q/ec]
            z=sum(un)
            refs.append([x/z for x in un])
            ms.append((ec+1)/(2*ec+1+q))
        tv=sum(abs(x-y) for x,y in zip(*refs))/2
        kl=sum(float(x)*math.log(float(x/y)) for x,y in zip(*refs))
        out.append({'beta_w_over_log2':k,'reference_TV_exact':str(tv),
                    'reference_TV':float(tv),'target_gap_exact':str(ms[1]-ms[0]),
                    'target_gap':float(ms[1]-ms[0]),
                    'KL':kl,'KL_divided_by_q':kl/float(q)})
    for q in (.25,.01,1e-5):
        for eps in (.016,.01,.001):
            c=30*eps
            mm=(np.exp(-c)+1)/(2*np.exp(-c)+1+q)
            mp=(np.exp(c)+1)/(2*np.exp(c)+1+q)
            def ref(t:float)->NDArray[np.float64]:
                x=np.array([1.,q,q*np.exp(-t),q*np.exp(-t)])
                return x/x.sum()
            pp,pm=ref(c),ref(-c)
            kl=float(np.sum(pp*np.log(pp/pm)))
            assert mm-mp>=3*eps-1e-12
            assert kl<=4*math.e*q*c*c+1e-12
    return out

def exact_three_site_certificate() -> dict[str, str | float]:
    """Exact rational Pauli arithmetic for a noncommuting patch certificate.

    Bounds ideal-filter localization error, not hardware/compiler errors.
    At beta=1/2 the final trace-norm upper bound is exactly 11977/150000.
    """
    terms = {
        'XII': Fraction(47,100), 'ZII': Fraction(17,100),
        'IXI': Fraction(1,2), 'IZI': Fraction(3,20),
        'IIX': Fraction(53,100), 'IIZ': Fraction(13,100),
        'XXI': Fraction(35,100), 'YYI': Fraction(21,100), 'ZZI': Fraction(28,100),
        'IXX': Fraction(35,100), 'IYY': Fraction(21,100), 'IZZ': Fraction(28,100),
    }
    perturb = {'IXI':Fraction(1,4), 'IZI':Fraction(2,5)}
    cyclic={('X','Y'):'Z',('Y','Z'):'X',('Z','X'):'Y'}
    def multiply(a: str, b: str) -> tuple[int,str]:
        power=0; word=[]
        for x,y in zip(a,b):
            if x=='I': word.append(y)
            elif y=='I': word.append(x)
            elif x==y: word.append('I')
            elif (x,y) in cyclic: power+=1; word.append(cyclic[x,y])
            else: power+=3; word.append(cyclic[y,x])
        return power%4,''.join(word)
    # Exact real coefficients of -i[H_R,V].
    comm: dict[str,Fraction]={}
    for a,ca in terms.items():
        for b,cb in perturb.items():
            phase,word=multiply(a,b)
            if phase in (1,3):
                comm[word]=comm.get(word,Fraction(0))+(2 if phase==1 else -2)*ca*cb
    c1=sum(abs(c) for c in comm.values())
    boundary_sum=2*(Fraction(35,100)+Fraction(21,100)+Fraction(28,100))
    beta=Fraction(1,2)
    eta=beta**3*boundary_sum*c1/12
    # v=sqrt(89)/20<1/2; exp(beta*v)<exp(1/4)<=1/(1-1/4)=4/3.
    trace_bound=2*eta*Fraction(4,3)
    assert c1==Fraction(1711,1000)
    assert trace_bound==Fraction(11977,150000)
    return {'beta':'1/2','patch_qubits':'3',
            'sum_boundary_term_norms':str(boundary_sum),
            'commutator_norm_upper_bound':str(c1),
            'filter_operator_error_upper_bound':str(eta),
            'state_trace_norm_error_upper_bound':str(trace_bound),
            'state_trace_norm_error_upper_bound_decimal':float(trace_bound),
            'scope':'Exact rational analytic localization bound; ideal Gibbs reference and ideal patch filter. Does not certify numerical ODE or hardware implementation.'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('checks.json'))
    args=parser.parse_args()
    result={'status':'floating-point falsification checks only; not interval certified',
            'seed':20261012,'algebra':algebra_checks(),
            'noncommuting_chain':chain_checks(),'commuting_lower_bound':lower_bound_checks(),
            'exact_rational_localization_certificate':exact_three_site_certificate()}
    result['all_assertions_passed']=True
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
