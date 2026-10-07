"""Formula diagnostics for the exact EB benchmark; standard library only."""

import json
import math
from pathlib import Path


def nb_cdf(k, m, mean):
    if k < 0:
        return 0.0
    if mean == 0:
        return 1.0
    q = mean / (mean + 1.0)
    logp = (math.lgamma(m+k) - math.lgamma(m) - math.lgamma(k+1)
            - m*math.log1p(mean) + k*math.log(q))
    term = math.exp(logp)
    total = term
    # Sum down from cutoff. In tested scaling cutoffs are close to the mean,
    # so the tail terminates quickly even when k is millions.
    for j in range(k, 0, -1):
        term *= j / ((m+j-1)*q)
        total += term
        if j < mean*(m-1) and term < total*1e-18:
            break
    return total


def benchmark(m, mean):
    if mean == 0:
        return 1-2.0**(-m), 0
    x = m*math.log1p(1/(mean+1)) / (-math.log1p(-1/(mean+1)**2))
    k = math.floor(x)
    return nb_cdf(k, m, mean)-nb_cdf(k, m, mean+1), k


def normal_limit(c):
    return math.erf(math.sqrt(c)/(2*math.sqrt(2)))


def check_small_direct(m, mean):
    risk, cutoff = benchmark(m, mean)
    q = mean/(mean+1)
    q2 = (mean+1)/(mean+2)
    p = (mean+1)**(-m)
    p2 = (mean+2)**(-m)
    dist = 0.0
    sign_crosses = []
    old_sign = p >= p2
    for k in range(20000):
        dist += abs(p-p2)/2
        new_sign = p >= p2
        if new_sign != old_sign:
            sign_crosses.append(k)
        old_sign = new_sign
        p *= (m+k)/(k+1)*q
        p2 *= (m+k)/(k+1)*q2
        if k > 100 and max(p,p2) < 1e-20:
            break
    assert abs(dist-risk) < 2e-12, (m,mean,risk,dist)
    assert sign_crosses == [cutoff+1], (m,mean,cutoff,sign_crosses)
    return {"m":m,"N":mean,"risk":risk,"direct_tv":dist,"cutoff":cutoff}


def stochastic_check():
    results = []
    mean = 2.5
    m = 4
    for seed_total in [0,1,2,7,20]:
        worst = 0.0
        for cutoff in range(101):
            seed_cdf = nb_cdf(cutoff-seed_total, m+seed_total, mean)
            vacuum_cdf = nb_cdf(cutoff,m,mean)
            worst=max(worst,seed_cdf-vacuum_cdf)
        assert worst < 2e-12
        results.append({"seed_total":seed_total,"max_cdf_excess":worst})
    return results


def main():
    direct=[check_small_direct(m,n) for m in [1,2,5,12] for n in [.1,1,3,10]]
    scaling=[]
    for c in [.1,1,4,16]:
        for n in [10,30,100,300]:
            m=round(c*n*n)
            risk,k=benchmark(m,n)
            a=(math.sqrt(n+2)+math.sqrt(n))/(2*math.sqrt(n+1))
            lower=-math.expm1(m*math.log(a))
            upper=math.sqrt(-math.expm1(2*m*math.log(a)))
            assert lower-2e-8 <= risk <= upper+2e-8
            scaling.append({"c":c,"N":n,"m":m,"risk":risk,"normal_limit":normal_limit(c),
                            "affinity_lower":lower,"affinity_upper":upper,"cutoff":k})
    data={"direct_checks":direct,"fock_stochastic_order":stochastic_check(),"scaling":scaling,
          "scope":"Numeric diagnostics only. No proof or physical channel simulation inferred."}
    out=Path(__file__).with_name("benchmark_diagnostics.json")
    out.write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({"direct_checks":len(direct),"stochastic_seed_checks":5,"scaling":scaling},indent=2))


if __name__ == "__main__":
    main()
