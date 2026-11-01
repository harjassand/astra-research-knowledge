# Preserved v1 wording finding

V1 SHA256: `e7d5f6bc094651fccfa14a508e010cb3904b3e89a018a9b83a7e169c4488637e`.

Its unqualified-looking final assertion that sampled drift cannot yield pointwise exponential CTMC drift is not true for every chain satisfying the consumer hypotheses.

Take the ordinary immigration–death chain on nonnegative integers: birth rate λ>0 and death rate μn, μ>0. It has the required Poisson population domination. Set d=log(4)/μ, δ=1/2, and any 0<a<1. At time d,

N_d = Bin(n,1/4) + Pois(m),  m=3λ/(4μ).

A Chernoff bound at log 2 gives

P(N_d>n/2) <= e^m [5/(4 sqrt(2))]^n <= e^m exp(−c n^a),

for n>=1 and c=log(4 sqrt(2)/5)>0. Thus (H) holds with constant block duration. Nevertheless V(n)=e^{θn} has the genuine pointwise drift

LV(n)/V(n) = λ(e^θ−1) + μn(e^{−θ}−1),

which is uniformly negative outside a finite set for every θ>0. Its multiplier is exactly one.

This is a scope counterexample, not a counterexample to the stationary-moment consumer. The root's repair correctly says that this consumer does not itself assert such a pointwise drift, and any nonexistence claim for a particular network requires that network's separate obstruction. The original bytes and repair diff are retained. The rate2 network's (H) remains unverified.
