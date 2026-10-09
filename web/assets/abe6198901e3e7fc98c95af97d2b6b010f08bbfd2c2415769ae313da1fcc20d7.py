"""Run: python demo.py. Produces exact rational samples and a normalizer estimate."""
from fractions import Fraction as F
from exact_completion import ExactCompletionSampler

X=[[F(4,5),0,F(1,5)],[F(3,5),F(1,5),0],
   [0,F(3,5),F(1,5)],[F(1,5),F(4,5),F(1,5)],
   [F(2,5),F(1,5),F(3,5)],[F(1,5),0,F(4,5)]]
sampler=ExactCompletionSampler(X,[0,0,1,1,2,2])
samples,work=sampler.sample(100,seed=123,max_trials=10000)
print('Exact acceptance lower bound:',sampler.acceptance_lower_bound)
print('First five designs:',samples[:5])
print('Sampling resource counts:',work)
z,accepted,budget=sampler.normalizer_estimate(F(1,5),F(1,20),seed=456,max_proposals=10000)
print('Estimated prior-weighted normalizer:',float(z))
print('Requested relative error <= 0.2, failure probability <= 0.05')
print('Estimator resource counts:',budget)
