"""Exact finite witnesses for the renewal/Schur form identities.

No stochastic acquisition is run and no reviewed artifact is modified.
Infinite-dimensional validity is proved in RENEWAL_SCHUR_FORM_REVIEW.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from rational_linalg import Mat, diag, zeros, psd
from multiboundary_positive_events import inverse, power, source_fixture, sqrt_upper


def run():
    examples = source_fixture()
    # Symmetric entrywise nonnegative source with an indefinite hidden block.
    # Its two-step first-return tail is not positive semidefinite.
    examples.append(Mat([[F(1,3),0,F(1,10),0],
                         [0,F(1,3),0,F(1,10)],
                         [F(1,10),0,0,F(1,2)],
                         [0,F(1,10),F(1,2),0]]))
    records = []
    total_identity_checks = 0
    for example_index, a in enumerate(examples):
        r = 3 if example_index < 2 else 2
        n = a.rows
        ib = diag(*([1]*r))
        ih = diag(*([1]*(n-r)))
        identity = diag(*([1]*n))
        v = Mat([[F(j == k) for k in range(r)] for j in range(n)])
        t = a.extract(range(r), range(r))
        c = a.extract(range(r,n), range(r))
        b = a.extract(range(r,n), range(r,n))
        d = a*v-v*t
        rr = c.T*inverse(ih-b)*c
        ss = c.T*inverse(ih+b)*c
        gp, gm = ib-t-rr, ib+t-ss
        absorption = [1-sum((t+rr).a[j]) for j in range(r)]
        kp = min(absorption)
        km = min(2*t[j,j]+absorption[j] for j in range(r))
        assert kp > 0 and km > 0
        assert psd(gp-kp*ib) and psd(gm-km*ib)
        absdiag = diag(*absorption)
        minusdiag = diag(*(2*t[j,j]+absorption[j] for j in range(r)))
        assert psd(gp-absdiag) and psd(gm-minusdiag)
        q_formula = (rr+ss+rr*inverse(gp)*rr+ss*inverse(gm)*ss)/2
        m_formula = (inverse(gp)+inverse(gm))/2
        cross_formula = (inverse(gp)*rr-inverse(gm)*ss)/2
        source_inverse = inverse(identity-a*a)
        assert q_formula == d.T*source_inverse*d
        assert m_formula == v.T*source_inverse*v
        assert cross_formula == v.T*source_inverse*d
        total_identity_checks += 3
        m_bound = (1/kp+1/km)/2
        assert psd(m_bound*ib-m_formula)
        assert psd((inverse(absdiag)+inverse(minusdiag))/2-m_formula)
        row_return_bound = max(sum(row) for row in rr.a)
        even = (rr+ss)/2
        assert all(min(row) >= 0 for row in even.a)
        row_even_return_bound = max(sum(row) for row in even.a)
        scalar_q_bound = row_even_return_bound+m_bound*row_return_bound**2
        assert psd(scalar_q_bound*ib-q_formula)

        # A symmetric estimated-map error, unrelated to source dimension.
        delta = Mat([[F(j == k,1000)+F(abs(j-k)==1,2000)
                      for k in range(r)] for j in range(r)])
        proposed = t-delta
        d_proposal = a*v-v*proposed
        transferred = (q_formula+cross_formula.T*delta+delta.T*cross_formula
                       +delta.T*m_formula*delta)
        assert transferred == d_proposal.T*source_inverse*d_proposal
        q_bound = max(sum(abs(x) for x in row) for row in q_formula.a)
        delta_bound = max(sum(abs(x) for x in row) for row in delta.a)
        transfer_bound = (sqrt_upper(q_bound)+delta_bound*sqrt_upper(m_bound))**2
        assert psd(transfer_bound*ib-transferred)
        total_identity_checks += 1

        # Resolve both signs and both z-factors before taking Abel limits.
        for z in [F(1,2),F(9,10),F(99,100)]:
            rz = c.T*inverse(ih-z*b)*c
            sz = c.T*inverse(ih+z*b)*c
            gzplus, gzminus = ib-z*t-z*z*rz, ib+z*t-z*z*sz
            rz_source = inverse(identity-z*z*a*a)
            qz = (rz+sz+z*z*rz*inverse(gzplus)*rz
                  +z*z*sz*inverse(gzminus)*sz)/2
            mz = (inverse(gzplus)+inverse(gzminus))/2
            nz = z*(inverse(gzplus)*rz-inverse(gzminus)*sz)/2
            assert qz == d.T*rz_source*d
            assert mz == v.T*rz_source*v
            assert nz == v.T*rz_source*d
            total_identity_checks += 3

        # Finite-censor tails, including the non-PSD tail example.
        tail_checks = []
        for cutoff in [2,3,5]:
            rl, sl = zeros(r,r), zeros(r,r)
            for k in range(cutoff-1):
                term = c.T*power(b,k)*c
                rl = rl+term
                sl = sl+((-1)**k)*term
            rt, st = rr-rl, ss-sl
            survival_row = Mat([[1]*(n-r)])*power(b,cutoff-1)*c
            censored = survival_row.a[0]
            tau = max(censored)
            for j in range(r):
                assert min(rt.a[j]) >= 0
                assert sum(rt.a[j]) <= censored[j]
                for k in range(r):
                    assert abs(st[j,k]) <= rt[j,k]
            assert psd(tau*ib-rt) and psd(tau*ib+rt)
            assert psd(tau*ib-st) and psd(tau*ib+st)
            tail_checks.append({'cutoff':cutoff,'censored_norm_upper':float(tau),
                                'return_tail_psd':psd(rt)})
        if example_index == 2:
            assert not tail_checks[0]['return_tail_psd']
            assert (gm-km*ib).det() == 0  # The sharper Gershgorin margin is attained.
        records.append({'example':example_index,'boundary_dimension':r,
                        'total_state_dimension':n,'kappa_plus':str(kp),
                        'kappa_minus':str(km),'local_inverse_norm_upper':float(m_bound),
                        'parity_row_source_form_upper':float(scalar_q_bound),
                        'diagonal_sector_lower_bounds_verified':True,
                        'noncommuting_R_and_boundary_schur':rr*gp != gp*rr,
                        'finite_censor_checks':tail_checks,'all_exact_checks_passed':True})
    report = {'arithmetic':'exact standard-library Fraction',
              'new_algebraic_identity_checks':total_identity_checks,
              'examples':records,'stochastic_trials':0,
              'infinite_dimension_scope':'Ordinary Abel/form proof in companion note; finite checks do not prove the limiting theorem.'}
    Path(__file__).with_name('RENEWAL_SCHUR_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    run()
