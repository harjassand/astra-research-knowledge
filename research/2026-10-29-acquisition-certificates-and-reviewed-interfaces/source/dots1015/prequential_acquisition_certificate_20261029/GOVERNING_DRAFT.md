# Prequential acquisition-only certification for an arbitrary adaptive learner
2026-10-29. NEW load-bearing simplification; independent receiving review pending.

## Mechanism
The accepted acquisition-only protocol already chooses every current frame BEFORE its fresh private role and product-probe settings/outcomes. Evaluate the probe estimator at THAT current frame, rather than at a final retrospectively chosen frame. This elementary prequential order makes the existing learning bank an unbiased estimate of the actual selected loss. No FTPL regret, optimization-gap certificate or retrospective empirical minimization is needed for SOUNDNESS. A good learner still matters for yield. This is not a novel general statistical principle, not independent holdout, and not evaluation of a future frame using past records.

Retain the accepted service/outer-code/control interfaces and the fine filtration of acquisition_only_quantum_certificate_20261029/GOVERNING_v1.md. Use n even, m=n-1, alpha=2^n/Catalan(n/2); at the fixed four-spin port m=3,alpha=8 and cheap logical Pauli pads suffice. The learner may be any causal rule with finite execution and a valid current frame; fresh key/role privacy and pre-call process boundary remain required. Its current frame can depend on previous acquisition data, but not on the current role, probe settings or outcomes.

## Direct observed counter
For edge i at round t and its CURRENT rotation C_it, retain the actual native probe estimator

 d_hat_it(C_it)=3/4-(9/4)yz C_ab-(81/4)yzuv C_ab C_cd.

Here indices and signs are the actual product-probe/readout record in the inherited convention. Conditional on fine past and current candidate, its expectation is the actual fine-conditional star defect delta_it(C_it). Each entry of a rotation is in [-1,1], giving d_hat in [-87/4,93/4]. No IID/reset assumption is used.

Let I_t be the private LEARN indicator with probability p, and define

 W_t=I_t/p sum_i d_hat_it(C_it),
 D_t=sum_i delta_it(C_it)-W_t.

After current candidate selection but before current role/probe sampling, E[D_t|history,candidate]=0. W_t lies in [-87m/(4p),93m/(4p)], including its SERVICE value zero; hence the conditional range length of D_t is at most 45m/p. Hoeffding's conditional lemma, composed across the two-stage candidate/probe filtration, yields

 Pr[sum_t D_t > (45m/p)sqrt(T ln(1/delta_L)/2)] <= delta_L.

Stopping at J services, cap T or a neutral resource abort is handled by zero terms afterwards. No source call or probe is invented; hypothetical post-stop candidates are unnecessary. Therefore the observable bound

 U_pre=max(0, S_pre+(45m/p)sqrt(T ell_L/2)),
 S_pre=sum_(actual LEARN rounds) sum_i d_hat_it(C_it)/p,
 ell_L>=ln(1/delta_L),

upper-bounds the actual selected fine-history cumulative loss with probability at least 1-delta_L. Counter values may be negative; clipping is safe on the good event. If rational rotations are used, S_pre is exactly rational; otherwise verified upper arithmetic is required. To avoid unbounded denominator growth, each W_t may be rounded UP to a fixed public dyadic grid; the resulting sum upper-bounds S_pre and conservatively retains the same theorem, with at most T gridunits of excess. Rounding does not alter the martingale used in the proof.

## Quantum acceptance and all-input lift
Use only LEARN and SERVICE, p+s=1. With the same accepted virtual-fault CP refinement, the binary service-fault martingale gives, with probability >=1-delta_F,

 V_bad <= s alpha sum_ti delta_it(C_it)+sqrt(T ell_F/2).

Accept a completed verified outer block exactly when

 s alpha U_pre+sqrt(T ell_F/2)<=t_correctable,

and no code/resource abort occurred. Otherwise reject. Then for EVERY initial payload-memory state and permitted arbitrary causal source,

 Pr[accept and V_bad>t_correctable] <= delta_L+delta_F.

The entire accepted fine-filtration/all-input CP-effect/QEC proof applies afresh: A_bad*(I)<=delta I, with delta=delta_L+delta_F, and

 (1/2)||A_accept-id_payload tensor B_actual_accept||diamond<=delta.

The virtual good/bad service labels are proof-only and retained pad keys must NOT enter the filtration. The actual coarse-memory filter is used. There is no normalized postselected-error guarantee absent a success lower bound. Source can always abort; no fixed-port capacity or practical advantage follows.

## What changes and what does not
This removes the necessity of certified optimization for operational SOUNDNESS and eliminates the width/stability/gap penalties of the retrospective FTPL certificate. It does not improve the learning rule itself, show favorable noise or predict future channels. Any purported implementation that selects C_t after seeing the current probe invalidates the conditional-mean step.

For T=120,p=1/3,m=3, the confidence radius is still large: 405 sqrt(60 ell_L), so the existing short trajectory is not expected to certify. The negative practical conclusion remains, but the asymptotic certificate overhead is O(sqrt(T)), with no solver-gap condition. Strong conventional adaptive learners can use exactly this interface. Direct full-path tests can still have substantially smaller constants; no advantage over them is claimed.

Dependencies: inherited native unbiased product-bank estimator and any-source star-to-raw-loss transfer; accepted acquisition-only service/QEC/all-input proof and its cheap four-spin Pauli implementation. These remain at their accepted scope. This note does not broaden source privacy, SPAM, memory retirement or control assumptions.
