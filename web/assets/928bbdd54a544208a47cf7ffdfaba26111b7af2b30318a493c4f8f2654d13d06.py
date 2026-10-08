"""Independent exact finite checks; not a proof of asymptotics or priority."""
from math import comb, log, sqrt, exp, isqrt
from fractions import Fraction
import json


def m(r, s):
    assert 0 <= s <= r and (r-s)%2 == 0
    k=(r-s)//2
    return comb(r,k)-(comb(r,k-1) if k else 0)


def run():
    exact=[]
    for n in range(1,25):
        spins=list(range(n%2,n+1,2))
        mu={s:m(n,s) for s in spins}
        f=[Fraction(1)]
        for J in range(1,n+1): f.append(f[-1]/(2*J+1))
        Z=sum((2*J+1)*m(2*n,2*J)*f[J] for J in range(n+1))
        joint=Fraction(0)
        recovered=[Fraction(0)]*(n+1)
        for a in spins:
            for b in spins:
                for J in range(abs(a-b)//2,(a+b)//2+1):
                    w=mu[a]*mu[b]*(2*J+1)*f[J]/Z
                    joint+=w
                    recovered[J]+=w
        assert joint==1
        assert all(recovered[J]==(2*J+1)*m(2*n,2*J)*f[J]/Z for J in range(n+1))
        for J in range(n+1):
            # Trace normalization of the fully separable magnetization-J twirl.
            assert sum(m(2*n,2*L) for L in range(J,n+1))==comb(2*n,n-J)
            assert Fraction(comb(2*n,n-J),m(2*n,2*J))==Fraction(n+J+1,2*J+1)
        exact.append(2*n)

    low_ratio=(float('inf'),None)
    worst_deficit=(float('-inf'),None)
    low_spin_tail_ratio=(0.,None)
    parity_cases=set()
    c=exp(-2)/2
    A=64*exp(2)
    Ctail=(log(A)+1)/3
    for n in range(1,129):
        spins=list(range(n%2,n+1,2))
        mu=[m(n,s) for s in spins]
        pref=[0]
        for v in mu: pref.append(pref[-1]+v)
        for s,v in zip(spins,mu):
            assert v <= 4*2**n*(s+1)/(n+1)**1.5
        assert m(2*n,0) >= 4**n/(2*(n+1)**1.5)
        for J in range(n+1):
            den=m(2*n,2*J)
            numer=[]
            for b,v in zip(spins,mu):
                lo=abs(b-2*J)
                hi=min(n,b+2*J)
                if lo>hi:
                    numer.append(0)
                else:
                    lidx=(lo-n%2)//2
                    hidx=(hi-n%2)//2
                    numer.append(v*(pref[hidx+1]-pref[lidx]))
            assert sum(numer)==den
            expected=sum((u/den)*log(b+1) for b,u in zip(spins,numer))
            deficit=0.5*log(n+1)-log(J+1)-expected
            assert deficit <= Ctail+1e-12
            if deficit>worst_deficit[0]: worst_deficit=(deficit,[n,J])
            if J<=isqrt(n):
                ratio=den/((2*J+1)*m(2*n,0))
                assert ratio>=c
                if ratio<low_ratio[0]: low_ratio=(ratio,[n,J])
                accum=0
                for b,u in zip(spins,numer):
                    accum+=u
                    tr=(accum/den)/(((b+1)/sqrt(n+1))**3)
                    assert tr<=A+1e-12
                    if tr>low_spin_tail_ratio[0]:low_spin_tail_ratio=(tr,[n,J,b])
                parity_cases.add(n%2)
    return {'status':'all assertions passed','exact_factorial_N':exact,
            'fixed_sector_and_uniform_bound_n_range':[1,128],
            'half_size_parities_checked':sorted(parity_cases),
            'minimum_checked_low_J_multiplicity_ratio':low_ratio,
            'largest_checked_conditional_log_dimension_deficit':worst_deficit,
            'largest_checked_low_J_cubic_tail_ratio':low_spin_tail_ratio,
            'analytic_c':c,'analytic_A':A,'analytic_Ctail':Ctail,
            'note':'Exact rational/integer identities are exact; reported logs and inequalities use floating arithmetic and are only diagnostics.'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
