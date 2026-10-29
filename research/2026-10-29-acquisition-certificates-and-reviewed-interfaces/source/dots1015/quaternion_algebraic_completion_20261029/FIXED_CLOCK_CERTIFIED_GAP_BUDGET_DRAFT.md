# Fixed-clock approximate optimization with a certified gap budget

2026-10-29 — new author derivation, not yet reviewed. This is a conditional practical-interface opening, not a uniform positive-yield theorem for every structured source.

## Interface
Keep accepted finite FTPL,35 features, p, R and M. At each round run a solver under a PREDECLARED input-bit-bounded computation schedule. It always returns an actual rational unit quaternion q and a sound rational lower bound L on its rounded quartic query. Let e=F_query(q)−L>=0 be its certified optimization gap. A solver may fail to tighten the lower bound, but must never falsely call a local optimum global. A trivial coefficient-l1 lower bound and fixed rational candidate provide a universally finite fallback; a bounded exact SOS verifier can improve it. No action-dependent abort or elapsed-time exposure is allowed.

This construction does not yet supply the engineering clock/scheduler. It states what quantity a supplied finite-budget implementation must certify. Large gaps remain visible; no claim is made that all genuine inputs have small gaps.

## Variable-gap averaging lemma
Conditional on the actual past, couple each finite midpoint perturbation to a fresh continuous uniform box perturbation Z. Let e_t be the solver's actual certified rounded-query gap, including its private internal coins, and let mu_t=E[e_t | actual past]. The chosen action is pointwise epsilon(Z)-optimal for the continuous query with epsilon(Z)<=e_t+dR/M.

The accepted approximate-action finite-difference inequalities use only this pointwise gap at the current input. Averaging them therefore replaces a uniform epsilon by mu_t+dR/M:

 |E[x_t,i | past]−partial_i Phi(G_{t−1})|
 <= (mu_t+dR/M)/h+h/(4R).

Optimizing h gives at most sqrt((mu_t+dR/M)/R), or its minimum with1 because features lie in[0,1]. The current full-information feedback remains independent of all current solver/perturbation choices conditional on the past under the accepted private-current-choice source interface. Hence the additional conditional expected loss is at most720 times this bias.

## Expected actual-history bound
Let E_T=E sum_{t<=T} e_t. The same potential telescoping and Cauchy–Schwarz/Jensen argument yields fixed-comparator expected regret at most

 35R/4 + T*720²/(4Rp)
 +720 sqrt( (T/R)*E_T +35*T²/M ).

The exact conditional version has the sum of min(1,sqrt((mu_t+35R/M)/R)) instead. For M>=140T², midpoint contribution inside the last square root is at most1/4. The prior uniform oracle tolerance R/(4T²) implies E_T<=R/(4T) and recovers the earlier bounded approximate-oracle penalty. More generally, with R proportional sqrt(T), a sublinear average-loss penalty follows when E_T=o(T R).

These are expectations on the ACTUAL learner-induced histories, not counterfactual policy regret. A realized sum of certificates is NOT automatically a certificate of E_T or of the conditional means mu_t; any high-probability conversion or empirical certification needs its own martingale argument. This budget can enter the existing Poincare/guard expected-readiness transfer, but small E_T is an additional substantive condition, not acquired for free.

## What this changes and does not
A fixed computation budget need not abort the protocol or pretend every query was globally solved. It can expose its exact optimization shortfall and retain a rigorously conditional protection guarantee. This targets the private-clock obstruction more directly than padding to an enormous universal exact solve. The complete exact oracle remains the theory fallback. Large/non-SOS relaxation gaps, benign-unexcited objective directions, resource constants, physical control errors and current-source timing independence remain real obligations. No advantage over equally informed adaptive conventional baselines is asserted.
