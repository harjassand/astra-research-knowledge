#!/usr/bin/env python3
"""Independent finite arithmetic checks of the three-state hybrid obstruction.

Uses only Python's standard library. Numerical checks supplement the proof;
they do not certify its universal quantifiers.
"""
from decimal import Decimal, localcontext
import json
from pathlib import Path
from time import perf_counter

def rowmul(v, A):
    return [sum((v[i]*A[i][j] for i in range(3)), Decimal(0)) for j in range(3)]

def matmul(A, B):
    return [[sum((A[i][k]*B[k][j] for k in range(3)), Decimal(0))
             for j in range(3)] for i in range(3)]

def propagate(v, A, n):
    while n:
        if n & 1:
            v=rowmul(v,A)
        A=matmul(A,A)
        n >>= 1
    return v

def tv(v, pi):
    return sum(abs(x-y) for x,y in zip(v,pi))/2

def fmt(x):
    return format(x, ".18E")

def run():
    started=perf_counter()
    outputs=[]
    with localcontext() as ctx:
        ctx.prec=350
        one=Decimal(1)
        half=one/2
        K=one
        c=K/4
        b=one-(-c).exp()
        alpha=half
        eps=Decimal(".01")
        c0=b*(one-alpha)/2
        p0=min(one/4,(-c).exp()*b)
        for text in [".05",".02",".01",".005",".002",".001"]:
            p=Decimal(text)
            assert 0<p<=p0
            s=p*(-2*c/p).exp()
            r=p*(-c/p).exp()
            pi=[p,s,one-p-s]
            q=[r,b,one-b-r]
            w=[pi[i]/q[i] for i in range(3)]
            D=sum(pi[i]*w[i].ln() for i in range(3))
            assert D<=3*K/4 and all(x>0 for x in pi+q)
            assert w[0]>=max(w[1:])
            G=[[Decimal(0) for j in range(3)] for i in range(3)]
            for i in range(3):
                for j in range(3):
                    if i!=j:
                        G[i][j]=q[j]*min(one,w[j]/w[i])
                G[i][i]=one-sum(G[i])
            L=[
                [one-s/(2*p),s/(2*p),Decimal(0)],
                [half,Decimal(0),half],
                [Decimal(0),s/(2*pi[2]),one-s/(2*pi[2])],
            ]
            H=[[alpha*G[i][j]+(one-alpha)*L[i][j]
                for j in range(3)] for i in range(3)]
            HG=alpha*(one-p)*(-c/p).exp()
            HL=(one-alpha)*half*(-2*c/p).exp()
            h=HG+HL
            assert abs((one-H[0][0])-h)<Decimal("1e-340")
            max_stationarity=max(abs(rowmul(pi,H)[j]-pi[j]) for j in range(3))
            max_balance=max(abs(pi[i]*L[i][j]-pi[j]*L[j][i])
                            for i in range(3) for j in range(3))
            assert max_stationarity<Decimal("1e-340")
            assert max_balance<Decimal("1e-340")
            assert rowmul(q,H)[0]>=c0
            LG=matmul(L,G)
            GL=matmul(G,L)
            hG=(one-p)*(-c/p).exp()
            hL=half*(-2*c/p).exp()
            steps=[]
            for n in [3,100,10000,1000000]:
                global_v=propagate(q,G,n)
                hybrid_v=propagate(q,H,n)
                lg_v=propagate(q,LG,n)
                gl_v=propagate(q,GL,n)
                lower=c0*((n-1)*(one-h).ln()).exp()-p
                lg_lower=b/2*(one-hG)*(
                    (n-1)*((one-hL).ln()+(one-hG).ln())).exp()-p
                gl_lower=b*b/2*(
                    (n-1)*((one-hL).ln()+(one-hG).ln())).exp()-p
                tol=Decimal("1e-320")
                assert tv(hybrid_v,pi)+tol>=lower
                assert tv(lg_v,pi)+tol>=lg_lower
                assert tv(gl_v,pi)+tol>=gl_lower
                steps.append({
                    "global_proposals":n,
                    "pure_imh_tv":fmt(tv(global_v,pi)),
                    "mixture_tv_after_n_total_steps":fmt(tv(hybrid_v,pi)),
                    "mixture_lower_bound":fmt(lower),
                    "local_then_global_tv_after_n_cycles":fmt(tv(lg_v,pi)),
                    "local_then_global_lower_bound":fmt(lg_lower),
                    "global_then_local_tv_after_n_cycles":fmt(tv(gl_v,pi)),
                    "global_then_local_lower_bound":fmt(gl_lower),
                })
            log10_insufficient=None
            if c0>eps+p:
                threshold=(c0/(eps+p)).ln()/(-(one-h).ln())
                log10_insufficient=fmt(threshold.log10())
            outputs.append({
                "p":str(p),"s":fmt(s),"r":fmt(r),
                "forward_KL":fmt(D),
                "hybrid_exit_probability_from_trap":fmt(h),
                "log10_mixture_insufficient_step_threshold":log10_insufficient,
                "stationarity_residual":fmt(max_stationarity),
                "local_detailed_balance_residual":fmt(max_balance),
                "checks":steps,
            })
        result={
            "K":str(K),"c":str(c),"proposal_entrance_mass_b":fmt(b),
            "mixture_alpha":str(alpha),"accuracy":str(eps),
            "first_step_guaranteed_trap_mass":fmt(c0),
            "explicit_admissible_p_upper_bound":fmt(p0),
            "precision_decimal_digits":350,
            "numerical_check_not_universal_proof":True,
            "all_finite_assertions_passed":True,
            "families":outputs,
        }
    result["elapsed_seconds"]=perf_counter()-started
    return result

if __name__=="__main__":
    result=run()
    out=Path(__file__).with_name("independent_counterexample_results.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
        "output":str(out),
        "all_finite_assertions_passed":result["all_finite_assertions_passed"],
        "elapsed_seconds":result["elapsed_seconds"],
        "p_0.001":result["families"][-1],
    },indent=2))

