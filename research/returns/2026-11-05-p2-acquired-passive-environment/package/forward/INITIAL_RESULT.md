# Initial forward result: adaptive transport races for equilibrium phase labels

## Actual operation and consequence
Assume fresh independent exact samples from each of two phase-conditional Gibbs laws mu_A=w_A/Z_A and mu_B=w_B/Z_B, evaluable unnormalized weights, and a differentiable invertible map T with evaluable inverse/Jacobian. Before each fresh attempt choose any map T_t and q_t in (0,1) using all past information. Define r_t(x)=w_B(T_t x)|det DT_t(x)|/w_A(x).

Choose source A with probability q_t; draw X from mu_A and accept with min(1,(1-q_t)r_t(X)/q_t), emitting label B. Otherwise draw Y from mu_B, accept with min(1,q_t/((1-q_t)r_t(T_t^{-1}Y))), emitting label A. Repeat after rejection. Maps/probabilities may keep adapting after every attempt.

Writing C_t=integral min(q_t w_A,(1-q_t)w_B(T_t x)|det DT_t|) dx, the conditional probabilities given the full past are

P(accept and emit B)=C_t/Z_A; P(accept and emit A)=C_t/Z_B.

Thus the next accepted label has P(B)=Z_B/(Z_A+Z_B), independent of the whole prior history, whenever the race terminates. Every accepted label is iid from the true equilibrium phase weights, despite arbitrary predictable learning. A fresh conditional sample from the emitted phase then gives an exact full equilibrium configuration. Reusing the accepted test point would be biased.

## Execution bill
With attempt success probability uniformly at least alpha, K labels cost at most K/alpha expected phase samples/maps/weight evaluations, plus K fresh conditional samples for full configurations. Fixed K yields Hoeffding half-width sqrt(log(2/delta)/(2K)). Perfect transport makes r constant and fair q gives alpha>=1/2. All training and exact/restarted conditional-sampling costs are additional. Generic within-phase MCMC is not automatically this resource.

## Honest boundary / novelty
This is a useful exactness theorem and complete operation-level construction, but I do not claim priority: targeted FEP, Bennett/MBAR, Bernoulli races and adaptive transport free-energy estimators are close established approaches. The strongest defensible contribution is the explicit history-adaptive race proof and execution/error account, not a claim to solve generic metastability. The physical obstacle is provisioning fresh phase-conditional samples and nonvanishing transported overlap.
