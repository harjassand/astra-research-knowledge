#!/usr/bin/env python3
"""Independent audit harness for the specified certified two-kick benchmark.

The proof review is in CERTIFIED_KICK_PROOF_CODE_REVIEW.md. This harness
replays the Decimal calculations and crosschecks against high-precision scalar
functions and a separately constructed finite-Fock simulation. The latter
checks are diagnostics, not substitutes for interval or truncation proofs.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, getcontext
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "code/certified_continuum_kicks.py"
RECEIPT = ROOT / "data/certified_continuum_kicks.json"
FOCK_SOURCE = HERE / "independent_kick_fock_check.py"
FOCK_RECEIPT = HERE / "independent_kick_fock_check.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def qdecimal(q):
    q=F(q)
    return Decimal(q.numerator)/Decimal(q.denominator)

def encloses(interval, value):
    return interval.lo <= value <= interval.hi

def pi_agm():
    # Independent Gauss-Legendre iteration, not the root Machin formula.
    a=Decimal(1); b=1/Decimal(2).sqrt(); t=Decimal(1)/4; p=Decimal(1)
    for _ in range(10):
        anew=(a+b)/2
        b=(a*b).sqrt()
        t-=p*(a-anew)**2
        a=anew; p*=2
    return (a+b)**2/(4*t)

def direct_sincos(q):
    # No range reduction: use the original |x|<=238 argument. With precision
    # 180, even the largest transient Taylor terms leave far more than the
    # 48 decimal places used by the certified implementation.
    x=qdecimal(q); x2=x*x
    st=x; ct=Decimal(1); s=st; c=ct
    for j in range(1,1000):
        st=-st*x2/((2*j)*(2*j+1))
        ct=-ct*x2/((2*j-1)*(2*j))
        s+=st; c+=ct
        if j>abs(x) and max(abs(st),abs(ct))<Decimal('1e-150'):
            return c,s
    raise AssertionError('independent trig series failed to converge')

def direct_bessel(n,q):
    from math import factorial
    x=qdecimal(q); a=abs(n)
    term=(x/2)**a/Decimal(factorial(a)); ans=term
    for j in range(1,300):
        term=-term*x*x/(4*j*(j+a)); ans+=term
        if abs(term)<Decimal('1e-170')*max(abs(ans),Decimal('1e-300')):
            return -ans if n<0 and a%2 else ans
    raise AssertionError('independent Bessel series failed to converge')

def run():
    start=time.time()
    source_hash=sha(SOURCE)
    receipt_hash=sha(RECEIPT)
    saved=json.loads(RECEIPT.read_text())
    assert saved["source_sha256"] == source_hash

    spec=importlib.util.spec_from_file_location("audited_continuum_kicks",SOURCE)
    k=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)

    getcontext().prec=180
    assert qdecimal(k.PI_LO) < pi_agm() < qdecimal(k.PI_HI)

    pk,errs=k.packets()
    assert len(pk)==289
    assert all(type(a)==int for p in pk for a in p["M"])
    assert all(isinstance(p["c"],F) for p in pk)
    eps=(1+errs[0])*(1+errs[1])-1
    assert eps < 1
    assert 2*eps < F(1747,10**12)
    assert k.rational_out(eps)==saved["unnormalized_isometry_error"]
    assert k.rational_out(2*eps)==saved["polar_CPTP_half_diamond_bound"]
    for e,stored in zip(errs,saved["kick_errors"]):
        assert k.rational_out(e)==stored

    bessel_checks=[]
    for theta in k.THETA:
        for n in range(-k.K,k.K+1):
            center,radius=k.bessel_center(n,theta)
            exact_numeric=direct_bessel(n,theta)
            assert qdecimal(center-radius) <= exact_numeric <= qdecimal(center+radius)
        numeric_tail=2*sum(abs(direct_bessel(n,theta)) for n in range(k.K+1,k.K+101))
        rigorous_tail=k.tail(k.K,theta)
        assert numeric_tail<qdecimal(rigorous_tail)
        bessel_checks.append({"theta":str(theta),
                              "bound":str(rigorous_tail),
                              "partial_numeric_tail":str(numeric_tail),
                              "tested_coefficients":2*k.K+1,
                              "tail_status":"100-term high-precision diagnostic; proof is analytical"})

    zs=[("all",F(1)),("no1",F(2,5)),("no2",F(3,4)),("no12",F(3,20))]
    phases=set()
    exponents=set()
    for j,p in enumerate(pk):
        for _,z in zs:
            exponents.add(-(1-z)*p["norm"])
        for q in pk[j+1:]:
            re=k.V*(p["n"]*q["n"]+p["m"]*q["m"])+k.CRE*(p["n"]*q["m"]+p["m"]*q["n"])
            im=k.CIM*(p["n"]*q["m"]-p["m"]*q["n"])
            for _,z in zs:
                phases.add(q["phase"]-p["phase"]+z*im)
                exponents.add(-(p["norm"]+q["norm"])/2+z*re)
    for phase in phases:
        co,si=k.sincos(phase)
        co_numeric,si_numeric=direct_sincos(phase)
        assert encloses(co,co_numeric)
        assert encloses(si,si_numeric)
    for exponent in exponents:
        assert encloses(k.expreal(exponent),qdecimal(exponent).exp())

    mats={name:k.no_click(pk,z) for name,z in zs}
    assert [x.out() for x in mats["all"]]==saved["raw_gram"]
    patterns={
        "neither":mats["no12"],
        "only1":k.vecadd(mats["no2"],mats["no12"],-1),
        "only2":k.vecadd(mats["no1"],mats["no12"],-1),
        "both":k.vecadd(k.vecadd(k.vecadd(mats["all"],mats["no1"],-1),mats["no2"],-1),mats["no12"])
    }
    replayed=0
    for name,Q in patterns.items():
        assert [x.out() for x in Q]==saved["records"][name]["raw_effect"]
        probs={"zero":Q[0],"one":Q[1],"plus":(Q[0]+Q[1]+Q[2]*2)*F(1,2),
               "plus_i":(Q[0]+Q[1]-Q[3]*2)*F(1,2)}
        for state,p in probs.items():
            assert k.event_interval(p,eps).out()==saved["records"][name]["physical_exact_probability"][state]
            replayed+=1

    fock=json.loads(FOCK_RECEIPT.read_text())
    finest=fock["results"][-1]
    comparisons=[]
    for record,probs in finest["probabilities"].items():
        for state,value in probs.items():
            interval=saved["records"][record]["physical_exact_probability"][state]
            # Decimal.from_float converts the saved binary float exactly.
            v=Decimal.from_float(value)
            enclosed=Decimal(interval[0]) <= v <= Decimal(interval[1])
            assert enclosed
            comparisons.append({"record":record,"input":state,"fock_value":value,
                                "certified_interval":interval,"enclosed":enclosed})
    assert source_hash==sha(SOURCE)
    assert receipt_hash==sha(RECEIPT)
    result={
        "status":"PASS for specified benchmark; human derivation review separately recorded",
        "reviewer":"producer-workspace/knowledge_and_comparator",
        "completed_utc":datetime.now(timezone.utc).isoformat(),
        "source_sha256":source_hash,
        "receipt_sha256":receipt_hash,
        "audit_source_sha256":sha(Path(__file__)),
        "independent_fock_source_sha256":sha(FOCK_SOURCE),
        "independent_fock_receipt_sha256":sha(FOCK_RECEIPT),
        "source_unchanged_through_review":True,
        "receipt_unchanged_through_review":True,
        "exact_arithmetic_checks":{"integer_pauli_entries":True,
                                   "rational_bessel_coefficients":True,
                                   "eps_lt_one":True,
                                   "two_eps_lt_1_747e_minus9":True},
        "bessel_crosschecks":bessel_checks,
        "high_precision_scalar_diagnostics":{"decimal_digits":getcontext().prec,
                                             "pi_rational_bounds_enclose_independent_agm_pi":True,
                                             "trig_method":"direct original-argument Taylor; no shared range reduction",
                                             "exp_method":"same Decimal library at independent 180-digit precision",
                                             "distinct_trigonometric_phases_checked":len(phases),
                                             "phase_min":str(min(phases)),
                                             "phase_max":str(max(phases)),
                                             "distinct_exponential_arguments_checked":len(exponents),
                                             "exp_argument_min":str(min(exponents)),
                                             "exp_argument_max":str(max(exponents))},
        "root_interval_replay":{"raw_gram_exact_string_match":True,
                                "all_raw_effects_exact_string_match":True,
                                "physical_probability_interval_matches":replayed},
        "independent_fock":{"basis_cutoffs":[x["cutoff_per_mode"] for x in fock["results"]],
                            "successive_max_probability_changes":[x.get("max_probability_change_from_previous") for x in fock["results"]],
                            "finest_isometry_defect":finest["isometry_defect"],
                            "all_16_probability_values_enclosed":True,
                            "comparisons":comparisons,
                            "scope":"Finite-Fock convergence diagnostic only; no certified Fock-tail bound"},
        "physical_device_claim":False,
        "runtime_seconds":time.time()-start
    }
    dest=HERE/"certified_kick_audit.json"
    dest.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ["status","source_sha256","receipt_sha256","runtime_seconds"]},indent=2))
    print("scalar phases",len(phases),"exp arguments",len(exponents),"probabilities",replayed)
    print(str(dest))

if __name__=="__main__":
    run()

