"""Reproducibility and limited smoke tests, not a numerical TV certificate."""
import json
from pathlib import Path
import numpy as np
from sampler import covariance_from_network,sample_centered_covariance,spectral_cubic
root=Path(__file__).resolve().parent
rng=np.random.default_rng(20261009)
for _ in range(20):
    assert not np.any(sample_centered_covariance(np.zeros((4,4)),rng))
T=np.diag(np.sqrt([.06,.025])).astype(complex)
U=np.array([[.6,.8j],[.8j,.6]])
T=T@U
K=covariance_from_network(T,[np.log(2),np.log(3)])
trials=6000
zero=0; total=0; maximum=0
for _ in range(trials):
    y=sample_centered_covariance(K,rng,check_physical=False)
    zero+=int(sum(y)==0); total+=int(sum(y)); maximum=max(maximum,int(sum(y)))
p0=float(np.linalg.det(np.eye(4)+K)**-.5)
frequency=zero/trials
stderr=float(np.sqrt(p0*(1-p0)/trials))
assert abs(frequency-p0)<6*stderr
first=np.random.default_rng(42); second=np.random.default_rng(42)
for _ in range(20):
    assert np.array_equal(sample_centered_covariance(K,first),sample_centered_covariance(K,second))
report={'status':'PASS','seed':20261009,'records':trials,'exact_ideal_vacuum_probability':p0,
        'empirical_vacuum_frequency':frequency,'binomial_standard_error':stderr,
        'sample_mean_count':total/trials,'initial_mean_energy':float(np.trace(K)/2),
        'maximum_observed_count':maximum,'S3':spectral_cubic(T),
        'scope':'Vacuum probability, deterministic seed, and execution smoke tests only; no certified TV bound for floats.'}
(root/'sampler_smoke_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
