# Independent receipt: efficient adaptive local matrix query

**RECEIVED in its stated local-query scope.** 28 October 2026.

Received source: `ordinary_adaptive_pure_matrix_query_20261028.md`, SHA-256
`483a8507c4ca0dfef510c888a2fc755e84b653bcee81a0329830d152b9ed3968`.

The mathematical receiver construction, paid source cap, all-history moment transfer, finite known-basis implementation and mixed-state reduction are supported by independent review. This is not a hardware/circuit benchmark, a generic global encoder-acquisition theorem, an exactly unbiased estimator, a PSD estimator, or a novelty claim.

## 1. Independent core checks

The separate `ordinary_adaptive_pure_known_center_independent_audit_20261028.md` receives the ideal known-center calculation and documents the finite-binomial proof. Its independent script passed 189 exact rational binomial cases and 480 covariance cases using a real-coordinate representation rather than the author's complex formula. It includes 20 null-observable fixtures. The maximum exact-formula numerical residual was 7.11e-15. This is independent finite algebra, not simulated hardware evidence.

In particular, centered outcomes are NOT circular. For xi=w-z,

    Sigma=E xi xi*,    Pi=E xi xi^T=-zz^T.

For Hermitian B and the degenerate ordered-pair statistic W, direct expansion gives

    Var Tr(BW)=[Tr(B Sigma B Sigma)+(z*Bz)^2]/[m(m-1)].

Indeed for h_12=Re(xi_2* B xi_1), E|xi_2*Bxi_1|^2=Tr(B Sigma B Sigma), whereas E(xi_2*Bxi_1)^2=(z*Bz)^2. The pair average has variance E h_12^2/binom(m,2). Its covariance with every linear sample-mean statistic vanishes by conditioning on the other, mean-zero pair variable. Thus the U-statistic proof correctly retains pseudocovariance and does not replace the actual coupled estimator by independent block estimates.

The audit requested one interface clarification: the implemented bound must be stated as MSE around the true state, not merely conditional variance, before averaging latent purifications. The received source now states this stronger bound in (12) and (13). The existing calculation already proves it with the same constant100. No source-cost change was required.

## 2. Coarse center and all records

The paid cap n0=ceil[320 Dplus log(12Dplus/beta)] is exactly the received finite-Clifford confidence construction at pure infidelity1/4, with operator perturbation threshold1/8 and backward arithmetic error1/8. Projecting its classical vector into the known original product space cannot reduce overlap with a true vector in that space. A fixed fallback makes the zero-projection history defined.

The deterministic trace-norm cap M=10lD is valid even on bad-center records. The definitions of beta and l imply ideal bias below zeta/4 and MSE at most24r_O/m+83Tr(O^2)/m^2. These bounds explicitly average bad histories; no observable success certificate is assumed. The total source cap includes the center bank, all m vector outcomes and all l Bernoulli outcomes.

## 3. Finite Gaussian/QR implementation

The Gaussian tail and small-residual probabilities are valid for every QR step, including its final one-dimensional complex residual. The perturbation recurrence compares true orthogonal projectors, and its L^d amplification needs O(d log(B/a)+log(d/(a kappa))) bits, not exponentially many physical operations. Quantile sampling can be truncated and rounded with polynomial-bit inverse-CDF arithmetic because the bounded-interval inverse density is exp(O(B^2)); B^2 is itself polynomial in the dimension and precision logarithm. Bad tails/guards use bounded fallback records.

The implementation argument couples numerical unitaries and finite measurement outcomes; it never asserts small total variation between a continuous Haar seed and a discrete seed. A matched basis outcome perturbs w by O(sqrt(d)kappa), hence the final matrix by O(lD kappa); mismatch/failure histories are charged using the deterministic2M output cap. The available inequalities allow smaller sub-budgets than their displayed upper bounds, covering known center rotations, binary measurements, Fourier synthesis, arithmetic and the other channel errors. With theta<=zeta/(10^6 l^2D^2m^2), the transfer consumes only a small fraction of the slack from83 to100 in the MSE coefficient. A polynomial known-unitary synthesis theorem is used, not an oracle for an unknown unitary.

The companion check independently verifies conservative rational QR recurrences and complete probability/bias/error budgets. These are mathematical resource checks, not execution of a full Schur/QR circuit.

## 4. One purification and the rank-at-most extension

The primary [Pelecanos–Spilecki–Tang–Wright Theorem1.1 and Section3.3](https://arxiv.org/html/2511.15806v1) explicitly give one efficient receiver channel whose output is an average of N copies of the same random purification. The governing programme import is Section2 of `direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md`; it also records the rank-at-most extension. The primary source was directly inspected, rather than inferred from a secondary description.

Here is an independent continuity proof of that extension. For rank(rho)=t<=r, choose a proof-only r-dimensional subspace S containing supp(rho). Define rho_e=(1-e)rho+e Pi_S/r. These states have rank r. Their canonical purifications in S tensor C^r converge as e decreases to zero, and applying the same Haar unitary on the r-dimensional environment preserves convergence. Both the finite-dimensional fixed CPTP channel applied to rho_e^tensorN and the averaged pure-copy outputs therefore converge. Their equality passes to rho. No unknown basis S or source environment is supplied to the implemented channel; this is only a proof of its action.

The algorithm applies that channel ONCE, before splitting coarse and fine copies. Conditional on the one latent purification, the remaining copies are homogeneous and independent of earlier measurement records in the required way. Separately generated purifications are never identified. For Otilde=O tensor I_r, the target mean and first moment term equal Tr(rho O) and Tr(rho O^2) for every purification, while Tr(Otilde^2)=r Tr(O^2). Thus conditional MSE averages without an extra latent-state variance. Only the coarse classical computation is padded; projecting its vector back preserves the exact r Hilbert-Schmidt factor.

## 5. Received claim and exclusions

With all N=n0+m+l calls paid, the resulting Hermitian mixed-state estimate has trace-norm mean bias at most zeta and

    E[Tr(O(rhohat-rho))^2]
      <=100[Tr(rho O^2)/m+r Tr(O^2)/m^2].

The finite receiver is polynomial in the charged dimensions, bank size and precision logarithms under the already received common-frame/compiler interfaces. For the ordinary loss state, no source reference is introduced; the source preparation remains the ordinary six-state experiment. The strongest equally informed conventional learner can use the same construction.

No simultaneous all-decoder confidence event, Loewner envelope, global encoder query-count, rank-weighted cross-encoder amortization, or model-coverage claim is received here. Those require separate proofs. The earlier fixed-design lower bound and coarse-model policy traps remain intact.
