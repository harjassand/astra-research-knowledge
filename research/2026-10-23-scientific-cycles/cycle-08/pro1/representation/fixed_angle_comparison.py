#!/usr/bin/env python3
"""One fixed-angle comparator/cost evaluation; not a code compiler or theorem test."""
import argparse
import datetime
from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb
from pathlib import Path
import hashlib
import json
import resource
import time

def run():
    start=time.perf_counter()
    with localcontext() as ctx:
        ctx.prec=90
        D=Decimal
        l=D(2).ln()
        beta=D(1)/512
        b=beta*beta
        delta=b*b/512
        q=D("0.5")-delta
        c=-b/128
        x=q*q
        y=q*(1-q)/2
        z=(1-q)*(1-q)/4
        def entropy(probs):
            return -sum(p*p.ln()/l for p in probs if p)
        h2=lambda p:entropy([p,1-p])
        pair=entropy([x]+[z]*4+[y+c]*2+[y-c]*2)/2
        four=pair+x*y*(1-h2((1+c/y)/2))/2
        new_floor=l*beta**3/8192
        previous_floor=l*beta**(D(7)/2)/16384
        pair_coarse=beta**4/1024
        old_four_upper=beta**4/256
        k=int(1/(4*beta))
        collision=sum(Fraction((k-1-n)*comb(n,n//2),2**n)
                      for n in range(0,k-1,2))
        v=Fraction(k*(k-1),8)-collision/8
        vd=D(v.numerator)/D(v.denominator)
        kappa=l*vd*b*b*(1-b)/16
        moment_t=kappa/(2*k*k)
        gap=kappa*kappa/(4*k*k)
        code_rank=3**k
        tighter_floor=l*vd*b*b/(32*k)
        data={
          "date_brisbane":"2026-10-22",
          "precision_decimal_digits":ctx.prec,
          "beta":str(beta),"b":str(b),"k":k,
          "v_k_exact":str(v),
          "new_uniform_excess_guarantee":str(new_floor),
          "new_exact_v_entropy_lower":str(tighter_floor),
          "pair_actual_entropy_excess":str(pair-D("1.5")),
          "four_call_actual_entropy_excess":str(four-D("1.5")),
          "pair_old_coarse_guarantee":str(pair_coarse),
          "cycle7_old_coarse_guarantee":str(previous_floor),
          "four_call_analytic_upper_used":str(old_four_upper),
          "new_guarantee_over_actual_four_call_rate_excess":str(new_floor/(four-D("1.5"))),
          "same_device_input_rank":str(code_rank),
          "kappa_selected":str(kappa),
          "lyapunov_t":str(moment_t),
          "one_minus_lambda":str(gap),
          "type_dimension_over_t":str(D(code_rank+16)/moment_t),
          "scientific_scope":"Evaluation of closed formulas and theoretical existence constants at ONE angle; no optimization, code construction or physical performance measurement.",
          "comparison_scope":"Explicit retained pair and nonscalar four-call codes; not optimum over all fixed-four-call inputs.",
          "rigorous_comparison":"The source proves four-call excess < beta^4/256 and new floor exceeds that at beta=1/512 independently of decimal rounding.",
          "inference_discovery_review_costs":"Unknown; process timing is only this evaluation."
        }
    data["wall_seconds"]=time.perf_counter()-start
    data["max_rss_kib_linux"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    data["source_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return data

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    data=run()
    text=json.dumps(data,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end="")

