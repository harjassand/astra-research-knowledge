# Exact reference-adapted Gibbs duality and constructive ascent

24 October 2026, root derivation. Finite dimensions; natural logs. The general Gibbs variational principle and relative-entropy data processing are standard. Historical originality of this particular packaging is NOT established.

Let N:A→B be a channel, keep an arbitrary fixed finite reference R, and let a>=1. For normalized faithful X_BR define

 G_X=a (N* tensor id)(log X)−(a−1) I_A tensor log X_R,
 Phi(X)=Tr exp G_X,
 F(rho)=S(rho_AR)−a S((N tensor id)rho)+(a−1) S(rho_R).

Then the exact identity is

 sup_X log Phi(X) = sup_rho F(rho).

The output space can be restricted to the support of N(I) if necessary. Boundary states are obtained by faithful approximation. No interchange of a minimum and maximum is used.

## Proof and explicit witness transfer

For omega=(N tensor id)rho and tau=rho_R=omega_R, Gibbs gives

 log Phi(X)=sup_rho [S(rho)+a Tr omega log X−(a−1)Tr tau log X_R].

The bracket is exactly

 F(rho)−a D(omega||X)+(a−1)D(tau||X_R).

By relative-entropy data processing it is at most F(rho)−D(omega||X). This proves one direction. For the other, put X=omega (or its faithful approximation): the two relative-entropies vanish. Thus an entropy upper bound is EQUIVALENT to the explicit exponential upper bound, despite the appearance of a specially chosen reference marginal.

This corrects the earlier statement in wh3_gibbs_trace_construction.md that the exponential candidate might be strictly stronger. For W3 and a=2, its constant is exp(−ln3)=1/3, so it is exactly the same squashing question, expressed in a different representation.

For any given X, the Gibbs maximizer Y=exp(G_X)/Phi(X) is an actual input state. It obeys

 F(Y)−log Phi(X)=a D((N tensor id)Y||X)−(a−1)D(Y_R||X_R)
                  >=D((N tensor id)Y||X).

Consequently a violating X gives a violating physical input Y with at least as large a violation. Conversely a violating rho gives X=N(rho) whose exponential objective is at least F(rho). This is a positive, same-channel witness transfer, not a formal nonpositive lift or an acquired experiment.

## A monotone finite-dimensional search operation

Set X_next=(N tensor id)Y. Applying the preceding inequality and the converse bound yields

 log Phi(X_next)−log Phi(X) >=D(X_next||X)>=0.

Thus alternation X→Gibbs input Y→channel output X_next monotonically increases the dual objective. This is an ordinary alternating variational/Blahut–Arimoto-type construction; no global-optimum or speedup claim follows. It may approach a singular boundary or a nonglobal stationary point. Positive observed increments are numerical diagnostics unless bounded arithmetically.

## Every faithful stationary point is self-consistent

Let T_X be the derivative of log at X (the positive BKM inverse-mean operator). The trace-one gradient of log Phi is

 a T_X(q)−(a−1)I_B tensor T_XR(q_R),  q=(N tensor id)Y,

The variable is X_BR. Stationarity sets this gradient to I_BR by homogeneity. Since T_X(X)=I and T_XR(X_R)=I, pairing the residual equation with delta=q−X gives

 a g_X(delta,delta)−(a−1)g_XR(delta_R,delta_R)=0.

BKM data processing implies the left side is at least g_X(delta,delta), which vanishes only when delta=0. Hence X=N(Y) at every faithful stationary point. This does not classify stationary points or prove global maximality.

## Operational and novelty boundary

Reference dimension, matrix exponentials/logarithms, conditioning and stopping tolerances are real computational resources. No universal complexity guarantee follows. Berta–Sutter–Walter's Quantum Brascamp–Lieb Dualities (2023), Corollary3.10, is a close primary ancestor for entropy/exponential formulations. Any claim of algorithmic novelty must also compare existing quantum Blahut–Arimoto/alternating-optimization methods before promotion.

## Actual receiving calculation, 16:51 UTC

wh3_gibbs_ascent.py/json implements the proved update for W3, a=2, and three declared starting states. Two interior starts (reference dimensions3 and4) reached stationary tolerance after31 and34 steps at logPhi≈−ln3. The rotated antisymmetric start hit the declared eigenvalue-conditioning boundary after5 steps, with logPhi still below−ln3; it was stopped as numerically inconclusive, not a mathematical exclusion or an automatically resumed job. Total elapsed .03036seconds, Linux peakRSS49280KiB. Tiny negative KL/increment values around1e−15 were recorded as floating roundoff, not exact inequalities.

This source is a concrete use of the variational construction. It does not turn convergence into proof or establish an implementation advantage. The closest ordinary algorithmic antecedents include Ramakrishnan, Iten, Scholz and Berta, Computing Quantum Channel Capacities, arXiv:1905.01286, and the Bregman-proximal formulation arXiv:2306.04492. Liu–Hayashi arXiv:2609.09731 explicitly warns that monotonicity and stabilization alone do not imply global optimality; its convex-objective guarantees have not been established for this entropy objective. Primary metadata/abstracts were retrieved; no claim of a full methodological novelty comparison has been made.

## Fixed physical reference and additional linear observables

The same proof works with an arbitrary fixed Hermitian input term H0: add Tr rho H0 to F and H0 to G_X. The relative-entropy defect, witness conversion and monotone alternating step are unchanged. For a faithful physical reference omega_A, take

 H0=log omega_A−a N*(log N(omega_A)).

The primal objective then is exactly

 a D(Nrho || N(omega_A) tensor rho_R)
     −D(rho || omega_A tensor rho_R).

Thus the representation is not restricted to maximally mixed physical references or unital channels. It still requires a genuine reference-preserving local channel and the actual product reference with rho_R. It does not establish a contraction value for a new channel. For general channels, restrict to the support of N(omega_A) where necessary. This is a direct extension of the proved identity, not a separate experiment.
