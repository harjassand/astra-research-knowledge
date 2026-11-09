# Hard-cap and second-moment lower bounds

9 November 2026. Mathematical proof export. These two arguments were independently derived and checked. The source binding is recorded in PROVENANCE.json; exposition and cross-references have been adapted for this self-contained package. No execution or runtime measurement is asserted.

## Two preliminary boundaries

The original factory has no distribution-uniform second-moment bound. For L>=2 and P=Q, its first stage conditional on X=i has mean (L-1)/p_i. Conditional Jensen therefore gives

    E N_first^2 >= (L-1)^2 sum_(i:p_i>0) 1/p_i.

This diverges as one atom tends to zero even with fixed d=2. It is a defect of that original factory, not an impossibility for all algorithms; the local-cap construction repairs it.

Universal exact maximality is impossible in the finite-transcript sample-only model. At an equal full-support pair P=Q, a maximal coupling must never disagree. Every finite sample-word transcript that can occur at another full-support pair has positive likelihood at this equal pair. The independent auxiliary randomness has the same law. Thus a terminal disagreeing event of positive probability at another full-support pair would also have positive probability at equality. Formally, restrict to each finite query count and source/sample-word sequence and use mutual absolute continuity, then take the countable union. No such event is possible, so the algorithm would always retain X even for unequal full-support P,Q, contradicting the exact Q marginal. This explains the need for positive slack but does not determine its cost.

## 1. Hard-cap obstruction extends to adaptive source allocation

Consider any universally exact sample-only coupling procedure that uses at most M fresh oracle calls on every run. Its requests may adaptively alternate between P and Q and depend on all previous observations. Pre-generate M independent fresh P records and M independent Q records, and answer each requested call from the next unused record of its requested source. This exactly simulates the procedure. Including supplied X, it is processing a fixed collection of r=M+1 P records and s=M Q records; unused records are simply ignored.

For d>=2 and M>=1, the finite-categorical fixed-batch converse in EMPIRICAL_BATCH_CONVERSE.md applies. At P=Q uniform, exactness for every P,Q forces the conditional empirical marginal constraint, hence expected disagreement is at least the empirical total variation lower bound. With t=2M+1 and eta<(d-1)/(2d), the fourth-moment bound therefore requires

    2M+1 >= (d-1)/(3 eta^2) - d^2/[3(d-1)].

This is an Omega(d/eta^2) deterministic total-call cap requirement. Adaptively choosing the source does not evade it. At d=16, eta=1/100, this particular bound gives M>=24,997. It is weaker numerically than the 49,994-new-call lower bound for a specified fixed per-source allocation because the simulation supplies up to M records of each source. No sharp adaptive hard-cap constant is claimed.

M=0 cannot solve the universal exact-target task for d>=2, since the output then receives no information about Q. The hard-cap argument does not constrain the support of an unbounded stopping law, nor prove an O(d/eta) mean lower bound for all adaptive algorithms. Fixed-batch empirical coupling already provides an O(d/eta^2) deterministic-cap upper bound, so the worst-case inverse-eta exponent is settled at this level of comparison.

## 2. Binary second-moment obstruction

Here is a self-contained limitation on regular sample-only exact constructions. It does not assume the proposed walk algorithm. Fix P=Bernoulli(1/2), and let Q_theta=Bernoulli(1/2+theta) in a neighborhood of theta=0. The algorithm is one fixed sample-only procedure across these sources, takes actual X~P, and outputs Y with exact law Q_theta. It terminates almost surely and has E_0 exp(epsilon N)<infinity for some epsilon>0, where N is total fresh calls. This exponential-moment assumption is satisfied by the locally capped construction and by any claimed uniform exponential-tail construction. It is not silently assumed for every possible finite-mean stopping algorithm.

Let F=Y-X, taking values -1,0,1. Exactness gives E_theta F=theta. Let N_Q be the number of Q calls. At theta=0 write their outcomes as independent fair signs R_j=2Z_j-1. All P samples, source-selection bits and other independent auxiliary randomness can be included in the initial independent seed. Then N_Q is a stopping time for the revealed Q sequence with that seed, and its stopped likelihood ratio is

    L_theta = product_(j=1)^(N_Q) (1+2theta R_j).

Because the algorithm terminates under the nearby sources, stopped transcripts obey E_theta F=E_0(F L_theta). For sufficiently small |theta|, the likelihood and its derivative are dominated by a constant times N exp(2|theta|N), which is integrable by the assumed exponential moment. Differentiation is therefore justified, not merely formal. With

    S = 2 sum_(j=1)^(N_Q) R_j,

one obtains the exact score identity

    1 = E_0(F S).

At equality of sources the near-maximal condition gives delta_0=Pr_0(F!=0)<=eta. Wald's stopped second-moment identity gives E_0 S^2=4 E_0 N_Q. Hence Cauchy-Schwarz already forces

    E_0 N_Q >= 1/(4 delta_0) >= 1/(4 eta).

For completeness, a conservative fourth-moment bound is derived without importing a sharp martingale constant. Let M_n be a fair-sign walk stopped at N_Q, first truncated at a deterministic n. Expansion of its fourth power gives

    E M_final^4 = 6 E sum_(j<=N_Q wedge n) M_(j-1)^2
                 + E(N_Q wedge n).

If X_4=(E M_final^4)^(1/2) and Y_2=(E(N_Q wedge n)^2)^(1/2), Doob's L4 maximal inequality and Cauchy-Schwarz give

    X_4^2 <= (32/3) X_4 Y_2 + Y_2^2.

The positive quadratic root is less than 11, so E M_final^4 <=121 E(N_Q wedge n)^2. Passing to the limit by Fatou yields

    E S^4 <= 16*121 E N_Q^2 < 2048 E N_Q^2.

Holder applied to the score identity, with E|F|^(4/3)=delta_0, now gives

    1 <= delta_0^(3/4) (E S^4)^(1/4),
    E N_Q^2 >= 1/(2048 delta_0^3) >= 1/(2048 eta^3).

Therefore E N^2 has the same lower bound. No stronger distribution-specific rare-atom example is needed for this obstruction: it already occurs at the balanced binary pair.

Consequences:

- A family satisfying Pr(N>t)<=A exp(-t/B_eta) for every real t>=0, with A independent of eta, has E N^2<=2 A B_eta^2. Necessarily B_eta >= 1/[64 sqrt(A) eta^(3/2)]. In particular B_eta=O(1/eta) is impossible as eta tends to zero.
- More generally, O(1/eta) mean together with O(1/eta^2) second moment is impossible under the stated score regularity. If the mean is at most K/eta, the ratio E N^2/(E N)^2 is at least 1/(2048 K^2 eta).
- The locally capped construction has E N^2=O(eta^-3) for d=2, so its second-moment inverse-eta exponent matches this obstruction. This does not prove that its exponential-tail scale is optimal, nor establish the best dimension dependence or constants.
- The lemma does not assert score differentiation for an arbitrary finite-mean construction without additional regularity. The original rare-atom heavy-tail example and finite-transcript exact-maximality obstruction remain separate facts.

