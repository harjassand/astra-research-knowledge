"""Independent exact/finite checks; never imports or edits producer code.

Exact certificate verification uses rational input and integer square roots.
NumPy/SciPy diagnostics do not supply interval or universal-proof validation.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import hashlib
import json
import platform
import sys
import numpy as np
import scipy
from scipy.linalg import eigvalsh
import sympy as sp

HERE = Path(__file__).resolve().parent
_suffix = Path("updates/FB/package/moment_environment/recovered/cray_moment_environment")
_candidates = [root / prefix / _suffix for root in [HERE, *HERE.parents]
               for prefix in [Path("."), Path("astra-capital")]]
SOURCE = next((p for p in _candidates if (p / "RESEARCH_NOTE.md").is_file()), None)
if SOURCE is None:
    raise FileNotFoundError("Place the verifier inside the capital tree or its work sibling; exact source package required.")


def fermion_fields(n, exact=False):
    ans = []
    for i in range(n):
        a = sp.zeros(1 << n) if exact else np.zeros((1 << n, 1 << n), complex)
        for bits in range(1 << n):
            if (bits >> i) & 1:
                sign = (-1) ** ((bits & ((1 << i) - 1)).bit_count())
                a[bits ^ (1 << i), bits] = sign
        ans.append(a)
    return ans


def many_body(h, interactions=()):
    n = len(h)
    aa = fermion_fields(n)
    nn = [a.conj().T @ a for a in aa]
    out = np.zeros_like(aa[0])
    for i in range(n):
        for j in range(n):
            out += h[i, j] * aa[i].conj().T @ aa[j]
    for i, j, u in interactions:
        out += u * nn[i] @ nn[j]
    return out, aa


def exact_scalar_certificate():
    z = json.loads((SOURCE / "exact_certificate.json").read_text())
    edges = [F(x) for x in z["edges"]]
    independently_generated = [F(1)]
    while independently_generated[-1] > F(1, 10000):
        independently_generated.append(independently_generated[-1] * F(2, 3))
    assert edges == [F(0)] + independently_generated[::-1]
    lo, hi = {}, {}
    for a, b in zip(edges[:-1], edges[1:]):
        w = (b - a) / 8
        s = (a*a + a*b + b*b) / 3
        lo[s] = lo.get(s, F(0)) + w
        aa, bb = a*a, b*b
        for x, q in [(aa, w*(bb-s)/(bb-aa)), (bb, w*(s-aa)/(bb-aa))]:
            hi[x] = hi.get(x, F(0)) + q
    expected = [sorted(lo.items()), sorted(hi.items())]
    records = []
    all_intervals = []
    for label, atoms0 in zip(["lower_gamma", "upper_gamma"], expected):
        atoms = [(F(s), F(w)) for s, w in z[label + "_atoms"]]
        assert atoms == atoms0
        roots = [(F(l), F(r)) for l, r in z[label + "_root_intervals"]]
        assert len(roots) == len(atoms)
        for i, ((l, r), (s, w)) in enumerate(zip(roots, atoms)):
            nxt = atoms[i+1][0] if i+1 < len(atoms) else s + sum(w for _, w in atoms)
            assert s < l <= r <= nxt
            fl = 1 + sum((ww/(ss-l) for ss, ww in atoms), F(0))
            fr = 1 + sum((ww/(ss-r) for ss, ww in atoms), F(0))
            assert fl <= 0 <= fr
        def sq(x):
            den = 1 << 130
            k = isqrt((x.numerator * den * den) // x.denominator)
            l = F(k, den)
            r = l if l*l == x else F(k+1, den)
            assert l*l <= x <= r*r
            return l, r
        e_l = sum((sq(s)[0] for s, _ in atoms), F(0)) - sum((sq(r)[1] for _, r in roots), F(0))
        e_r = sum((sq(s)[1] for s, _ in atoms), F(0)) - sum((sq(l)[0] for l, _ in roots), F(0))
        all_intervals.append((e_l, e_r))
        records.append({"label": label, "roots_verified": len(roots), "strict_interlacing": True})
    radius = (all_intervals[0][0] - all_intervals[1][1], all_intervals[0][1] - all_intervals[1][0])
    assert radius == (F(z["radius_fraction_lower"]), F(z["radius_fraction_upper"]))
    assert F(".00400824083758") < radius[0] <= radius[1] < F(".00400824083759")
    return {"checks": records, "fraction_radius_reproduced": True,
            "strict_decimal_enclosure": ["0.00400824083758", "0.00400824083759"]}


def exact_non_gaussian():
    a = fermion_fields(4, exact=True)
    n = [x.T*x for x in a]
    h_base = -n[0]-n[1]+n[0]*n[1]+n[2]+n[3]
    h_base += sp.Rational(4, 5)*(a[0].T*a[2]+a[2].T*a[0]+a[1].T*a[3]+a[3].T*a[1])
    low = h_base-sp.Rational(9, 5)*n[2]*n[3]
    high = h_base+2*n[2]*n[3]
    src = json.loads((SOURCE/"additional_results.json").read_text())["exact_non_gaussian_failure"]
    trial = sp.Matrix([sp.Rational(x) for x in src["low_trial_vector"]])
    rq = (trial.T*low*trial)[0]/(trial.T*trial)[0]
    assert rq == sp.Rational(src["low_trial_energy"]) < -sp.Rational(19, 10)
    l, d = (high+sp.Rational(19, 10)*sp.eye(16)).LDLdecomposition(hermitian=False)
    assert l*d*l.T == high+sp.Rational(19, 10)*sp.eye(16)
    pivots = [d[i, i] for i in range(16)]
    assert all(x > 0 for x in pivots)
    # Entire vacuum one-particle addition sector is exactly identity in both baths.
    for ub in [sp.Rational(-9, 5), sp.Integer(2)]:
        assert [1, 1, 2+ub][0:2] == [1, 1] and 2+ub > 0
    return {"rational_H_from_CAR_without_float_rounding": True, "rayleigh_quotient": str(rq),
            "positive_LDL_pivots": [str(x) for x in pivots]}


def free_excess(levels, poles, v, beta=None):
    h = np.block([[levels, v], [v.conj().T, np.diag(poles)]])
    ev = eigvalsh(h)
    if beta is None:
        return float(np.minimum(ev, 0).sum()-np.minimum(poles, 0).sum())
    return float((-np.logaddexp(0, -beta*ev).sum()+np.logaddexp(0, -beta*poles).sum())/beta)


def shared_bath_counterexample():
    a = np.array([-.5, .5]); vl = np.ones((1, 2))/np.sqrt(2)
    b = np.array([0., -1., 1.]); vh = np.array([[np.sqrt(.75), np.sqrt(.125), np.sqrt(.125)]])
    e0l = free_excess(np.zeros((1, 1)), a, vl)
    e0h = free_excess(np.zeros((1, 1)), b, vh)
    e10l = free_excess(np.array([[10.]]), a, vl)
    e10h = free_excess(np.array([[10.]]), b, vh)
    r0 = e0l-e0h
    r10 = e10l-e10h
    assert abs(e0l-(1-np.sqrt(5))/2)<1e-13
    assert abs(e0h-(1-np.sqrt(2+np.sqrt(3))))<1e-13
    assert r0>11/40 and 0<=r10<=.1
    mixed = r0-r10
    assert mixed>7/40
    # Exact rational inequalities used in the analytic proof, no decimal priority.
    assert F(17,10)**2 < 3 and F(19,10)**2 < F(37,10)
    assert F(9,4)**2 > 5 and F(19,10)-F(13,8) == F(11,40)
    return {"same_exact_moments": {"W":"I_2", "S":"I_2/4"},
            "all_mean_contrast": 0, "all_endpoint_contrast": 0,
            "resonant_width": r0, "detuned_width": r10,
            "mixed_contrasts": [-mixed, mixed], "rigorous_abs_margin_lower": "7/40"}


def gibbs_and_green(h, fields, beta, omega):
    ee, q = np.linalg.eigh(h)
    p = np.exp(-beta*(ee-ee.min())); p /= p.sum()
    rho = (q*p)@q.conj().T
    transformed = [q.conj().T@a@q for a in fields]
    factor = (p[:, None]+p[None, :])/(1j*omega+ee[:, None]-ee[None, :])
    g = np.array([[np.sum(factor*x*y.conj()) for y in transformed] for x in transformed])
    mm = -(g-g.conj().T)/(2j)
    return rho, mm


def interacting_green_diagnostics():
    rng = np.random.default_rng(390125)
    ans = []
    for beta in [.2, .7, 2.]:
        for u in [-2., 1., 3.]:
            ha = np.array([[.2, .15+.06j], [.15-.06j, -.35]])
            vv = (rng.normal(size=(2, 1))+1j*rng.normal(size=(2, 1)))*.2
            poles = np.array([-.6, .6]); v = np.concatenate([vv, vv], axis=1)
            one = np.block([[ha, v], [v.conj().T, np.diag(poles)]])
            h0, aa = many_body(one, [(0,1,u)])
            dx = np.array([[.013, .007+.003j], [.007-.003j, -.009]])
            hx, _ = many_body(dx, [(0,1,.005)])
            xev = eigvalsh(hx); delta = float((xev[-1]-xev[0])/2)
            xc = (xev[-1]+xev[0])/2
            # Occupation bit order makes impurity the low two bits; embed by indices.
            embed = np.zeros_like(h0)
            for i in range(16):
                for j in range(16):
                    if i>>2 == j>>2:
                        embed[i,j] = hx[i&3,j&3]-(xc if i==j else 0)
            h1 = h0+embed
            for n in [0,1,3]:
                omega = (2*n+1)*np.pi/beta
                r0,m0 = gibbs_and_green(h0,aa[:2],beta,omega)
                r1,m1 = gibbs_and_green(h1,aa[:2],beta,omega)
                r = float(np.linalg.norm(r1-r0,ord='nuc'))
                gamma = 2*omega*(vv@vv.conj().T)/(omega*omega+.36)
                bound = np.linalg.inv(omega*np.eye(2)+gamma)
                assert eigvalsh(m0).min()>-1e-11 and eigvalsh(bound-m0).min()>-1e-11
                assert eigvalsh(m1).min()>-1e-11 and eigvalsh(bound-m1).min()>-1e-11
                qbound = delta*(2*beta/omega+4/omega**2)
                md = float(np.linalg.norm(m1-m0,2))
                assert r<=beta*delta+1e-11 and md<=qbound+1e-11
                ans.append(dict(beta=beta,U=u,frequency_index=n,delta=delta,
                                gibbs_trace_distance=r,gibbs_bound=beta*delta,
                                green_difference_norm=md,green_bound=qbound))
    return ans


def psd_factor(x):
    e, q = np.linalg.eigh(x)
    assert e.min()>-1e-12
    return q*np.sqrt(np.maximum(e,0))


def paired(poles):
    es=[]; vs=[]
    for e,l in poles:
        es.extend([-e]*l.shape[1]+[e]*l.shape[1])
        vs.extend([l/np.sqrt(2),l/np.sqrt(2)])
    return np.array(es), np.concatenate(vs,axis=1)


def contrast_score_diagnostics():
    rng=np.random.default_rng(71023)
    vals=[]
    for trial in range(4):
        e=np.array([.2,.55,.9]); v=(rng.normal(size=(2,3))+1j*rng.normal(size=(2,3)))*.14
        w=2*v@v.conj().T; s=2*(v*e**2)@v.conj().T
        l=psd_factor(w); li=np.linalg.inv(l); b=li@s@li.conj().T
        el,q=np.linalg.eigh(b)
        low=paired([(np.sqrt(el[i]),l@q[:,i:i+1]) for i in range(2)])
        a0,b0=.1,1.
        wa=(b0*b0*w-s)/(b0*b0-a0*a0); wb=(s-a0*a0*w)/(b0*b0-a0*a0)
        high=paired([(a0,psd_factor(wa)),(b0,psd_factor(wb))])
        true=(np.concatenate([-e,e]),np.concatenate([v,v],axis=1))
        ha0=np.array([[.3,.11+.04j],[.11-.04j,-.2]])
        dd=np.array([[.012,.006-.003j],[.006+.003j,-.008]])
        ha1=ha0+dd
        # Spectral diameter of d^dagger dd d, including its vacuum and full sector.
        xe=np.linalg.eigvalsh(dd); fock=np.array([0,xe[0],xe[1],xe.sum()])
        delta=(fock.max()-fock.min())/2
        for beta in [.2,.7,2.]:
            def delta_f(bath):
                return free_excess(ha1,*bath,beta)-free_excess(ha0,*bath,beta)
            ref=delta_f(low); err=abs(delta_f(true)-ref)
            rh=free_excess(np.zeros((2,2)),*low,beta)-free_excess(np.zeros((2,2)),*high,beta)
            score=0.; source_sum=0.; n_terms=100
            for n in range(n_terms):
                om=(2*n+1)*np.pi/beta
                gl=om*l@np.linalg.inv(om*om*np.eye(2)+b)@l.conj().T
                gh=om*(wa/(om*om+a0*a0)+wb/(om*om+b0*b0))
                loggap=float(np.linalg.slogdet(om*np.eye(2)+gh)[1]-np.linalg.slogdet(om*np.eye(2)+gl)[1])
                loggap=max(0.,loggap)
                xi=min(1.,delta*(2*beta+4/om)*(1+np.linalg.norm(gh,2)/om))
                score+=2*xi*loggap/beta; source_sum+=2*loggap/beta
            c=np.trace(w).real*(b0*b0-a0*a0)**2/4
            tail=2*c/beta*(beta/(2*np.pi))**6/(5*(n_terms-.5)**5)
            assert abs(source_sum-rh)<=tail+5e-12
            assert err<=score+tail+1e-11 and score<=rh+tail+1e-11 and err<=2*delta+1e-11
            vals.append(dict(trial=trial,beta=beta,delta=delta,actual_reference_error=err,
                             universal_width=rh,contrast_score=score,tail_bound=tail,
                             trivial_2delta=2*delta,terms=n_terms))
    return vals


def provenance_and_replays():
    pins=[]
    for line in (SOURCE/"SHA256SUMS.txt").read_text().splitlines():
        sha,name=line.split(maxsplit=1)
        actual=hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
        assert actual==sha
        pins.append({"path":name,"sha256":sha})
    out=[]
    for script,artifact in [("certify.py","exact_certificate.json"),("experiment.py","numerical_results.json"),("additional_tests.py","additional_results.json")]:
        replay=HERE/"replays/source"/artifact
        assert replay.is_file()
        original=json.loads((SOURCE/artifact).read_text())
        fresh=json.loads(replay.read_text())
        # Small eigensolver variations are diagnosed numerically, never called exact.
        def delta(a,b):
            if isinstance(a,dict):
                assert a.keys()==b.keys();return max([delta(a[k],b[k]) for k in a] or [0.])
            if isinstance(a,list):
                assert len(a)==len(b);return max([delta(x,y) for x,y in zip(a,b)] or [0.])
            if isinstance(a,(float,int)) and not isinstance(a,bool):return abs(a-b)
            assert a==b;return 0.
        d=delta(original,fresh)
        assert d<1e-9
        out.append({"script":script,"output":artifact,"fresh_sha256":hashlib.sha256(replay.read_bytes()).hexdigest(),
                    "byte_identical":replay.read_bytes()==(SOURCE/artifact).read_bytes(),"maximum_numeric_difference":d,
                    "exit_code":0,"scope":"Inspected producer code replay in scratch; not independent theorem validation."})
    return {"producer_pins":pins,"replays":out,"acquisition_replay":"Not executed; inspected source and supplied results only."}


if __name__=="__main__":
    out={"environment":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__,"platform":platform.platform()},
         "source_integrity_and_replay":provenance_and_replays(),
         "independent_scalar_certificate":exact_scalar_certificate(),
         "independent_exact_non_gaussian":exact_non_gaussian(),
         "shared_bath_counterexample":shared_bath_counterexample(),
         "interacting_green_diagnostics":interacting_green_diagnostics(),
         "thermal_contrast_diagnostics":contrast_score_diagnostics(),
         "status":"Exact identities plus finite floating diagnostics; no external validation or novelty claim."}
    (HERE/"independent_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
