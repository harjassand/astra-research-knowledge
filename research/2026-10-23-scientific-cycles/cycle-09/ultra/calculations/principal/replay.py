#!/usr/bin/env python3
"""New bounded Cycle9 admissions; stdlib, exact rational/integer core.

Not a proof by enumeration. The all-parameter arguments are in PROOF.txt.
No predecessor scientific suite, molecular/engineering job or hardware is run.
"""
import argparse
from collections import defaultdict
from decimal import Decimal,localcontext
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math,random,time


def convolution(a,b):
    out=defaultdict(F)
    for i,p in a.items():
        for j,q in b.items():out[i+j]+=p*q
    return dict(out)


def exact_geometry():
    cases=orders=0
    for D in [2,3,4,6]:
        for L in range(2,11):
            # Unnormalized f_n=sum_x|xx0tail>, <f_i,f_j>=D^min(i,j).
            # Innovations f_n-f_(n-1) are orthogonal and have these norms.
            norms=[1]+[D**j-D**(j-1) for j in range(1,L+1)]
            for k in range(L):
                for ell in range(k+1,L+1):
                    for i in range(k+1):
                        assert D**min(i,ell)-D**min(i,k)==0
                    assert F(sum(norms[:k+1]),D**ell)==F(1,D**(ell-k))
                    cases+=1
            # Exact source order in the common Bell basis, reduced to the
            # leading-zero label j (all other patterns share the same density).
            for k in range(1,L):
                for d in range(1,L-k+1):
                    for j in range(L+1):
                        p=F(1,D**(2*(L-k))) if j>=k else F(0)
                        q=F(1,D**(2*(L-k-d))) if j>=k+d else F(0)
                        assert p>=F(1,D**(2*d))*q
                        orders+=1
    return dict(status='PASS',exact_Gram_projection_cases=cases,
                exact_source_order_cases=orders)


def global_control_checks():
    records=[]
    with localcontext() as ctx:
        ctx.prec=90
        for D,L,r in product([2,3,4,6],[2,4,7],[1,2,5]):
            for w in sorted({0,(L-2)//2,L-2}):
                pex=defaultdict(F)
                for k in range(1,L+1):
                    for j in range(k,L+1):
                        p=F(1,D**(2*(j-k)))
                        if j<L:p*=1-F(1,D**2)
                        n=max(1,j-w)
                        pex[max(0,n-k)]+=p/L
                assert sum(pex.values())==1
                c=F(1,D**(2*(w+1)))
                bad=(1-F(w+1,L))*c
                assert 1-pex[0]==bad
                dist={0:F(1)}
                for _ in range(r):dist=convolution(dist,pex)
                actual=Decimal(0)
                for e,p in dist.items():
                    z=(Decimal(1)-Decimal(1)/(Decimal(D)**e)).sqrt()
                    actual+=(Decimal(p.numerator)/p.denominator)*z
                lowers=[]
                for d in range(w+1,L):
                    cd=F(1,D**(2*d));q=1-F(1,D**(d-w))
                    lb=(r*cd)/(1+r*cd)*q*(1-F(d,L))
                    assert Decimal(lb.numerator)/lb.denominator<=actual+Decimal('1e-80')
                    lowers.append(lb)
                upper=1-(1-bad)**r
                assert actual<=Decimal(upper.numerator)/upper.denominator+Decimal('1e-80')
                records.append(dict(D=D,L=L,r=r,w=w,
                                    exact_error_upper=str(upper),
                                    exact_best_lower=str(max(lowers)),
                                    actual_joint_error_decimal=str(actual),status='PASS'))
    return records


def mgf_and_volume():
    beta=F(3,2)*F(3,4)**8
    tails=0;volumes=0
    for D in [2,3,4,6]:
        for n in [0,2,9,20]:
            law={n:F(1,D**n)}
            for j in range(1,n+1):law[n-j]=F((D-1)*D**(j-1),D**n)
            assert sum(law.values())==1
            assert sum(p*F(4,3)**g for g,p in law.items())<=F(3,2)
            joint={0:F(1)}
            for r in range(1,4):
                joint=convolution(joint,law)
                assert sum(p for g,p in joint.items() if g>8*r)<=beta**r
                tails+=1
        for r in range(1,5):
            for t in range(1,6):
                # New collective positive-composition weight, independently DP'd.
                dp={0:1}
                for _ in range(r):
                    nxt=defaultdict(int)
                    for s,v in dp.items():
                        for d in range(1,r*t-s+1):nxt[s+d]+=v*D**d
                    dp=dict(nxt)
                exact=sum(v for s,v in dp.items() if s<=r*t)
                formula=sum(math.comb(s-1,r-1)*D**s for s in range(r,r*t+1))
                assert exact==formula
                assert exact<=D**(r*t)*math.comb(r*t,r)<=(3*t*D**t)**r
                volumes+=1
    return dict(status='PASS',beta_exact=str(beta),
                exact_collective_geometric_tail_cases=tails,
                exact_weighted_composition_cases=volumes)


def collective_cauchy():
    rng=random.Random(2026102209);cases=0
    for D,L,r in [(2,2,2),(3,2,2),(2,2,3)]:
        total=r*L
        for kv in [tuple([1]*r),tuple([L]*r),tuple([1,L]*r)[:r]]:
            k=sum(kv)
            for n in [0,1,r]:
                rows=D**n;cols=D**total;bell=D**k;tail=D**(total-k)
                A=[[rng.randrange(-2,3) for _ in range(cols)] for _ in range(rows)]
                B=[[rng.randrange(-2,3) for _ in range(cols)] for _ in range(rows)]
                normA=sum(x*x for row in A for x in row)
                normB=sum(x*x for row in B for x in row)
                amp_sum=0
                for u in range(tail):
                    for v in range(tail):
                        amp=sum(A[y][x*tail+u]*B[y][x*tail+v]
                                for y in range(rows) for x in range(bell))
                        amp_sum+=amp*amp
                actual=F(amp_sum,D**(2*(total-k)+k+n))
                rhs=F(normA*normB,D**(2*total-k+n))
                assert actual<=rhs
                cases+=1
    return dict(status='PASS',exact_multicopy_product_Kraus_cases=cases,
                note='Unnormalized integer product maps; all-CP completeness proved analytically')


def chord():
    cases=0
    for x in [F(1,2),F(1,10),F(1,1000)]:
        h=math.log(1/float(x))
        for M in [1,2,3,8,64,1000,10**12]:
            lhs=min(F(1),M*x)
            rhs=float(x)+(1-float(x))*math.log(M)/h
            assert float(lhs)<=rhs+1e-13
            cases+=1
    return dict(status='PASS',finite_float_chord_admissions=cases,
                note='Exact convex-secant proof handles arbitrary finite E lnM; no E M assumption')


def threshold_posterior():
    cases=0
    for D in [2,3,4,6]:
        for L in range(2,21):
            for s in range(1,L):
                c=F(D**(2*s)-1,D**(2*L)-1)
                for j in range(1,L+1):
                    p=F(sum(D**(2*k) for k in range(1,min(s,j)+1)),
                        sum(D**(2*k) for k in range(1,j+1)))
                    assert p>=c
                    if j==L:assert p==c
                    cases+=1
    table=[]
    D=2;L=4;w=1;s=L-w-1;c=F(D**(2*s)-1,D**(2*L)-1)
    for r in [16,64,256,4096]:
        m=(r*(D-1))//(2*D*L)
        bound=max(0,1-math.exp(-((D-1)/D)*r/(8*L))-float((1-c)**m))
        table.append(dict(D=D,L=L,w=w,r=r,c_s_exact=str(c),m=m,
                          analytic_global_error_lower=bound))
    return dict(status='PASS',exact_threshold_posterior_cases=cases,
                strong_converse_formula_admissions=table)


def ceil_ratio(base,a,b=1):
    j=0
    while b<a:b*=base;j+=1
    return j


def resource_table():
    beta=float(F(3,2)*F(3,4)**8);rows=[]
    for D,L,r,eps in [(2,256,1,F(1,64)),(2,2**20,1,F(1,64)),
                      (2,2**20,10**6,F(1,64)),
                      (2,2**20,1,F(1,2**20)),
                      (6,2**20,1000,F(1,64))]:
        # Conservative necessary SEP threshold replaces beta^r by beta.
        target=math.log(L)+math.log(1-float(eps)-beta)/r-1
        lo,hi=0,L-1
        while lo<hi:
            mid=(lo+hi)//2;u=mid+9
            if u*math.log(D)+math.log(u)>=target:hi=mid
            else:lo=mid+1
        A=math.log(r/(8*float(eps)))/(2*math.log(D))
        cp=max(0,math.ceil(min(A,L/2))-1)
        lt=ceil_ratio(2,L+1)
        le=ceil_ratio(2,2*r*eps.denominator,eps.numerator)
        s=ceil_ratio(D,2*r*eps.denominator,eps.numerator)
        t=32*lt+128*le;Q=4*t+9*s
        rows.append(dict(D=D,L=L,r=r,one_global_epsilon=str(eps),
                         SEP_volume_necessary_w_float_admission=lo,
                         CP_neighbor_necessary_w_float_admission=cp,
                         Cycle8_exact_formula_upper_w=min(L-1,3*Q),
                         per_queue_parity_query_upper=Q,
                         original_mean_source_supply_nats=r*(L+1)*math.log(D)/2,
                         hidden_clock_access=0,extra_entangled_aid=0,
                         source_memory_local_dimension=f'({L}*{D}^{L})^{r}',
                         scope='Formula evaluation; no large quantum state/device simulated'))
    return rows


def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,
                                            default=Path(__file__).parent)
    out=p.parse_args().output_dir;out.mkdir(parents=True,exist_ok=True)
    wall=time.perf_counter();cpu=time.process_time()
    result=dict(status='PASS',geometry=exact_geometry(),
                CPTP_comparator_and_finite_r=global_control_checks(),
                volume_and_tail=mgf_and_volume(),
                Cauchy=collective_cauchy(),expected_log_aid=chord(),
                threshold_posterior=threshold_posterior(),
                matched_formula_table=resource_table(),
                scope='New finite admissions only; proof and all regime statements are analytic')
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    timing=dict(wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                old_scientific_suites_rerun=0,hardware_calls=0,paid_compute=0,
                total_discovery_inference_cost='UNKNOWN')
    (out/'TIMING.json').write_text(json.dumps(timing,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**timing)))


if __name__=='__main__':main()
