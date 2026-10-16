"""Exact scalar rate/Chernoff arithmetic only. No generator, solver, or CDF."""
from fractions import Fraction as F
from math import ceil
import json
from pathlib import Path

CAP = 162
b = lambda n: F('2.676')*n*(n-1)+F('108.102')
a = lambda n: F('0.040')*n*(n-1)*(n-2)+F('37.881')*n
d = F('8.2207')
assert all(b(n+1)-b(n) == F('5.352')*n >= 0 for n in range(CAP))
assert all(a(n+1)-a(n) == F('0.120')*n*(n-1)+F('37.881') > 0 for n in range(CAP))
theta = 8*(b(CAP)+a(CAP))+20*d*CAP
assert theta == F(492588879, 250)
h=F(1, 10000)
mu=theta*h
assert 197 < mu < 198

# e = sum_{j=0}^3 1/j! + sum_{j>=4} 1/j!
#   < 8/3 + (1/24)*sum_{l>=0} 5^(-l) = 87/32.
# With k=m+1>mu, Chernoff at z=k/mu gives
# P(Pois(mu)>=k) <= exp(k-mu)*(mu/k)^k
#                    < (87/32)^(k-197)*(mu/k)^k.
def B(k, mean):
    assert k > mean > 197
    return F(87,32)**(k-197)*(mean/F(k))**k

results=[]
for power, k, shown in [(13,316,F(733,10**16)),(14,321,F(665,10**17))]:
    threshold=F(1,10**power)
    bound=B(k,mu)
    assert bound < shown < threshold
    assert B(k-1,mu) > threshold
    # The integer-ceiling theta also has the same sufficient m.
    mu_ceiling=F(ceil(theta),10000)
    assert B(k,mu_ceiling) < shown
    results.append(dict(tail_target=f'1e-{power}',k=k,m=k-1,power_blocks=k,
                        exact_bound=f'(87/32)^{k-197}*(492588879/({2500000*k}))^{k}',
                        rational_upper=str(shown),diagnostic_decimal=float(bound),
                        verified_exact_fraction_comparison=True,
                        preceding_k_fails_this_bound=True,
                        integer_ceiling_theta_same_degree=True,
                        hypothetical_10000_slab_uniformization_tail_upper=str(10000*shown),
                        hypothetical_10000_slab_sequential_matvec_count=10000*(k-1)))
report=dict(scope='scalar exact rational rate and Poisson Chernoff checks; no state solve',
            cap=CAP,sites=8,undirected_edges=10,
            birth_at_cap=str(b(CAP)),death_at_cap=str(a(CAP)),
            diffusion_exit_at_all_cap=str(20*d*CAP),
            theta_exact=str(theta),theta_decimal='1970355.516',
            theta_ceiling=ceil(theta),h=str(h),mu_exact=str(mu),mu_decimal='197.0355516',
            chernoff_exponential_upper='e < 87/32, using factorial series and geometric tail',
            results=results)
path=Path(__file__).with_name('poisson_specialization.json')
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
