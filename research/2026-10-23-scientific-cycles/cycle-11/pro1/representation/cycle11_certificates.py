#!/usr/bin/env python3
"""Cycle11 certificates using only the Python standard library.

The preserved Cycle10 JSON is read, not recomputed. New calculations display
the rate-depth envelope, check its optimizer independently by bisection, and
check the exact binomial law for the pure-push example. Diagnostics are not
all-length proofs or physical large-input constructions.
"""
from pathlib import Path
from decimal import Decimal as D, getcontext
from math import comb
import argparse, hashlib, json, platform, resource, time

ROOT=Path(__file__).resolve().parents[1]
EXPECTED="9ef0b6cd6d35b1fa5021403e1691c00384886b1a1ecd41b893b2336070685112"

def h2(p):
    return -sum(x*x.ln()/D(2).ln() for x in (p,1-p) if x)

def envelope(b,v):
    a=1-b; ell=D(2).ln()
    if v>=a/3:
        return D(0),D(3).ln()/ell
    z=((9*b*b*v*v+8*a*a*(1-v*v)).sqrt()-3*b*v)/(2*a*(1+v))
    lam=z.ln()
    return lam,((3*b+a*(z+2/z)).ln()+lam*v)/ell

def bisect_optimizer(b,v):
    a=1-b
    def derivative(lam):
        z=lam.exp()
        return a*(z-2/z)/(3*b+a*(z+2/z))+v
    if derivative(D(0))>=0:
        return D(0)
    lo,hi=D(0),D(2).ln()/2
    for _ in range(280):
        mid=(lo+hi)/2
        if derivative(mid)>0: hi=mid
        else: lo=mid
    return (lo+hi)/2

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path(__file__).with_suffix(".json"))
    args=parser.parse_args()
    started=time.perf_counter()
    getcontext().prec=90
    path=ROOT/"dependencies/cycle10/representation/capacity_comparison.json"
    raw=path.read_bytes(); source_hash=hashlib.sha256(raw).hexdigest()
    assert source_hash==EXPECTED
    inherited=json.loads(raw)
    dstar=3/(2*D(2).sqrt())-1; ell=D(2).ln()
    records=[]
    for old in inherited["observations"]:
        den=int(old["beta_denominator"])
        if den<32: continue
        b=D(1)/(den*den); upper=(1+dstar*b).ln()/ell
        rec={
            "beta_denominator":den,"b":str(b),
            "cycle11_sublinear_depth_upper_excess":str(upper),
            "cycle10_proved_uniform_lower_excess":str(ell*b/(2**20)),
            "cycle10_unsimplified_lower_excess":old["cycle10_exact_floor"],
            "cycle10_inner_k":old["cycle10_k"],
            "strongest_retained_unrestricted_lower_name":old["best_retained_certificate"],
            "strongest_retained_unrestricted_lower_excess":old["best_retained_excess"],
            "old_certificate_scope":"Values read unchanged. Matching resource-class lower here uses the actual Cycle10 code."
        }
        assert D(old["cycle10_exact_floor"])<=upper
        records.append(rec)
    optimizer_checks=[]
    for b in (D(0),D(1)/1024,D(1)/262144,D(1)/4,D(1)):
        a=1-b
        for v in sorted(set([D(0),a/12,a/6,a/4,a/3,D("0.5")])):
            lam,cost=envelope(b,v); numeric=bisect_optimizer(b,v)
            assert abs(lam-numeric)<D("1e-75")
            if b==0 and v<=D(1)/3:
                assert abs(cost-(h2((1+v)/2)+(1+v)/2))<D("1e-75")
            if v==0:
                assert abs(cost-(D("1.5")+(1+dstar*b).ln()/ell))<D("1e-75")
            optimizer_checks.append({"b":str(b),"v":str(v),"lambda":str(lam),
                "upper_rate":str(cost),"bisection_error":str(abs(lam-numeric))})
    pure_push=[]
    for b in (D(0),D(1)/4,D(1)/262144):
        a=1-b
        for n in (1,2,8,32):
            probs=[D(comb(n,j))*(a**j if j else 1)*(b**(n-j) if n-j else 1) for j in range(n+1)]
            mass=sum(probs); mean=sum(j*p for j,p in enumerate(probs))
            entropy=-sum(p*p.ln()/ell for p in probs if p)
            assert abs(mass-1)<D("1e-75") and abs(mean-a*n)<D("1e-75")
            assert entropy<=D(n+1).ln()/ell+D("1e-75")
            pure_push.append({"b":str(b),"N":n,"bath_mean_depth":str(D("0.5")+mean),
                "bath_purifier_entropy_upper":str(entropy),
                "entropy_upper_log2_N_plus_1":str(D(n+1).ln()/ell)})
    out={
        "precision_decimal_digits":getcontext().prec,
        "scope":"New scalar algebra and exact binomial diagnostics; not proofs or physical large-input constructions; predecessor suites not replayed.",
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "inherited_json_sha256":source_hash,
        "inherited_json_usage":"Historical values read unchanged; original proof source preserved.",
        "small_b_upper_coefficient":str(dstar/ell),
        "guaranteed_lower_coefficient":str(ell/(2**20)),
        "certificate_comparisons":records,"optimizer_checks":optimizer_checks,
        "pure_push_checks":pure_push,"all_checks_pass":True,
        "observed_script_body_seconds":time.perf_counter()-started,
        "peak_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python":platform.python_version(),"dependencies":"Python standard library only",
        "unknown_costs":["discovery","inference","total review","efficient code construction"],
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"output":str(args.output),"all_checks_pass":True,
        "optimizer_cases":len(optimizer_checks),"pure_push_cases":len(pure_push),
        "observed_script_body_seconds":out["observed_script_body_seconds"],
        "peak_rss_kib_linux":out["peak_rss_kib_linux"]}))
if __name__=="__main__": main()

