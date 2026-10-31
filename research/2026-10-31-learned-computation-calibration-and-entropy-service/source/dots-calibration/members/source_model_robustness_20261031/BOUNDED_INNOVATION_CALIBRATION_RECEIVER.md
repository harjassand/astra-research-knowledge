# Calibrating bounded-width innovations for a reusable fast-source model

31 October 2026. Author construction, pending independent review. This is a receiving theorem for a known mechanism with an unknown innovation law, not identification of an unrestricted hidden process. The estimator and its concentration inequality are ordinary finite-alphabet statistics. The additional consumer is the separately reviewed complete-CQ perturbation bound.

## 1. Known mechanism and unknown parameter

The fully observed state is x in GF(2)^n. At each clock event it updates by

    y = F x + G r + beta,

with known binary F, G, beta. F is invertible, G has k independent columns, 1<=k<=n, and the controllability matrix [G,FG,...,F^(n-1)G] has rank n. Innovation words r in GF(2)^k have an unknown, fixed law p, are independent across events, and are independent of prior source/system states and interventions. The clock rate lambda is known separately. These are structural promises, not statistical conclusions from a finite transcript.

The known reference P0 uses u(r)=2^-k; the actual kernel Pp uses p. Let m be any acquired controllability horizon for which [G,...,F^(m-1)G] has rank n; m=n always suffices. Binary elimination computes such a horizon in polynomial n time. Denote by pi the uniform law on all n-bit states and by Pi=pi 1^T its reset matrix.

For every fixed r, x -> F x+G r+beta is a permutation. Consequently Pp pi=pi for EVERY p, without estimating p or a stationary distribution. Also

    x_m = F^m x_0 + sum_(j=0)^(m-1) F^j beta
                    + sum_(j=0)^(m-1) F^j G r_(m-1-j).

Under u the last sum is uniform on the image of the controllability matrix, hence uniform on GF(2)^n. Thus P0^m=Pi.

For any fixed x, injectivity of G makes r -> F x+G r+beta one-to-one. Therefore the column difference is exactly

    sum_y |Pp(y|x)-P0(y|x)| = sum_r |p(r)-u(r)|,
    eta := ||Pp-P0||_1 = ||p-u||_1.

This equality does not require enumerating 2^n source states. It fails as stated for a noninjective G; this receiver requires an acquired basis of the actual innovation coordinates rather than silently identifying redundant coin laws.

## 2. Acquiring innovation samples

Compute a binary left inverse J with JG=I_k. Given a complete transition pair (x,y), verify that v=y+Fx+beta lies in im G and recover r=Jv. Failure of this consistency check causes ABORT. Passing the check does not establish the iid/model promise.

Two valid access protocols are:

1. Prepare/reset x=0 and request independent one-step samples, paying each preparation, query and readout.
2. Observe N consecutive complete clock transitions of a trajectory, including every self-loop clock event. Recover r from each consecutive pair. Under the stated iid innovation premise these recovered words are iid p even though the source labels are dependent. No reset is required.

A change-only record does NOT meet protocol 2: conditioning on a visible change biases the innovations and alters event counts. Finite-bandwidth observations that miss events are also outside the theorem. Waiting time, detector/readout access and clock acquisition are separate resources; N independent records are not cost-free at high lambda. The theorem assumes exact observed bits, not noisy state readout.

## 3. A finite-sample upper confidence bound

Write D=2^k and let p_hat be the empirical law of N>=1 recovered innovations. Define

    r_N = sqrt( 2 [D ln 2 + ln(1/delta)] / N ),   0<delta<1,
    eta_hat = sum_r |p_hat(r)-1/D|,
    U = min{2, eta_hat+r_N}.

For every fixed law p,

    Pr( ||p_hat-p||_1 > r_N ) <= delta.                 (1)

Proof: for a real vector v, ||v||_1=max_(s in {+1,-1}^D) sum_r s_r v_r. For each fixed sign vector, the sample variables s_(r_j) lie in [-1,1]. Hoeffding's one-sided bound gives exp(-N t^2/2) for a deviation t. Union over 2^D sign vectors gives 2^D exp(-N t^2/2), proving (1). This finite argument includes zero-probability symbols and unknown support; it does not assume a lower bound on p_min.

On the single event E={||p_hat-p||_1<=r_N}, triangle inequality yields eta<=U. Use an upward certified rational approximation r_bar>=r_N in an executable test; replace U by min(2,eta_hat+r_bar). Logs/square roots may be computed with directed interval arithmetic. For a simpler purely conservative schedule one can specify a rational r_bar and choose an integer N certified to satisfy N r_bar^2/2 >= D ln2+ln(1/delta). No real-number equality or exact logarithm oracle is needed. eta_hat is exactly rational from integer counts.

## 4. Actual PASS/ABORT consumer

Fix in advance a resource envelope: total physical evolution time T, at most p_slots prescribed CQ instruments, an acquired bound b for the centered source-diagonal Hamiltonians H_x, and model-error budget epsilon_model>0. Assume exact uniform centering,

    2^-n sum_x H_x=0,       ||H_x||<=b.

Set

    C = 72(p_slots+1)m + 4096 b^2 m^2 T,
    eta_target = min{1/(4m), epsilon_model/C}.

PASS precisely if U<=eta_target, and otherwise ABORT. Use upper bounds on C and lower bounds on eta_target for safe finite arithmetic. On E and PASS, the reviewed theorem COMMON_STATIONARY_CQ_ROBUSTNESS.md gives, uniformly over arbitrary reference systems, initial CQ states, and all prescribed outcome-retaining CQ instruments in the envelope,

    || Process(Pp) - Process(P0) ||_(complete CQ trace) <= epsilon_model.  (2)

The interventions may act on labels and system, and adapt to retained outcomes or the public calibration record. They must be CQ-preserving, have the same interpretation for both models, and remain within the fixed resource envelope. Sparse source snapshots are permitted; public microscopic event paths are not an output promised by the fast-source compiler. Unknown quantum backaction is not acquired from transition records.

If the already acquired ideal P0 simulator has uniform execution error epsilon_exec for that chosen experiment, replace its right side by epsilon_model+epsilon_exec. Its actual gates, source preparation, Hamiltonian encodings and control implementations remain paid. The estimator does not implement this quantum simulator.

The uniform-r affine realization is acquired using the existing classical-law-preserving synthesis, not by assuming an arbitrary raw CNOT dilation resets quantum memory. Its pure-return horizon can be taken at most n. That quantum horizon and the classical m above may differ; use n for both if a common conservative parameter is wanted. Replacement preserves the classical diagonal process, not arbitrary coherences or the private original coin record.

## 5. Statistical meaning, public reuse and margins

The false-PASS event {PASS and eta>eta_target} has probability at most delta. This is an unconditional statement over training, NOT a posterior guarantee for every accepted transcript, and NOT automatically a delta guarantee conditional on PASS.

A rigorous output comparison can retain the whole public calibration transcript. On ABORT, both the real and comparison experiments output the same abort flag. On PASS, compare the ideal-P0 simulator with the actual Pp controlled process, using the same transcript-dependent consumer and initial-state preparation. The full trace-norm distance of the joint transcript/output experiments is at most

    epsilon_model + epsilon_exec + 2 delta.             (3)

Indeed E makes (2) uniform even for transcript-dependent consumers, while the bad training mass contributes at most twice its probability. Conditioning on acceptance instead yields the conservative bound

    epsilon_model + epsilon_exec + 2 delta/Pr(PASS),

when Pr(PASS)>0; rare acceptance cannot be ignored.

If the actual eta satisfies the sufficient margin eta<=eta_target-2 r_bar, then E implies eta_hat+r_bar<=eta_target, so Pr(PASS)>=1-delta. In that model subset the conditional bad-training probability is at most delta/(1-delta). A useful parameter choice is r_bar<=eta_target/4: every eta<=eta_target/2 is accepted with probability at least 1-delta. Merely choosing N cannot ensure acceptance when the actual law is too far from uniform.

The same event E certifies the model parameter for arbitrarily many later adaptive finite uses; it does not incur a fresh statistical delta each time. However physical model discrepancy accumulates across experiments, and numerical execution errors must be allocated separately. For a finite lifetime budget T_total and total instrument/segment count, choose eta_target from that whole budget, or sum the per-experiment deterministic bounds. No fixed nonzero eta grants unlimited total-time epsilon accuracy. Publicly disclosing p_hat is harmless to this reasoning because it uses a uniform parameter event, not a private empirical-support indistinguishability assertion. Postselecting on rare later outcomes can still magnify conditional error.

## 6. Coupling acquisition and means

For a supplied rational sparse source-diagonal Pauli list,

    K = sum_j theta_j S_j tensor Z^(v_j),

uniform pi gives mean zero for each nonidentity source string v_j and mean one for the identity string. The exact system mean is Hbar=sum_(v_j=0) theta_j S_j, after rational cancellations. Acquired LCU access to K_centered=K-Hbar tensor I has normalization at most 2 sum_j |theta_j|; this is a safe accessible b, not a magically computed smaller operator norm.

The physical model is H_system + sqrt(lambda) Hbar + sqrt(lambda) K_centered. Both compared laws have the SAME uniform stationary law, so they have exactly the same mean. The common mean can be included in H0 without affecting the perturbation proof, but its real simulation action is paid. A scalar system identity is removable under an explicit global-phase convention. A nontrivial mean is not erased. Thus rate-independent MODEL ERROR does not imply rate-independent total gate cost in the presence of a large unremoved mean.

More generally, known uniform-state preparation and an acquired K block encoding give ordinary compression access to Hbar without computing a classical numerical mean. Exact numerical mean evaluation, certifying zero, sharper normalization and implementing its evolution are distinct tasks; no generic efficient Boolean counting claim is made.

## 7. Resources and strongest ordinary alternatives

For r_bar proportional to eta_target, the sufficient sample count is

    N = O( [2^k + ln(1/delta)] / eta_target^2 ).

This is exponential in the innovation width k, explicitly. It has no 2^n table and no microscopic-rate factor lambda. Rank/left-inverse/controllability acquisition is polynomial in n,k. Each record costs polynomial(n,k) bit arithmetic to extract its innovation; exact counts need O(D log(N+1)) bits using a dense histogram, or a sparse dictionary with the missing-symbol contribution to eta_hat counted analytically. A full data record itself costs O(N n) bits in the pair protocol unless processed in a stream. Acquisition calls, resets if used, all-tick observations, and wall time are not hidden by the statistical count.

A conventional active or fully observed linear-system estimator with the SAME mechanism and records obtains exactly this p_hat and confidence interval. No learning superiority is claimed. A conventional retained-model simulator can use the same ideal affine reference, the same robustness theorem, direct microscopic trajectories, dense matrix methods for small full dimension, or reduced-memory/adiabatic techniques when their assumptions and errors are met. Direct classical trajectories pay for roughly lambda T microscopic source events unless additional structure is exploited; their system propagations and precision are separate. That observation is not a lower bound on all ordinary algorithms.

The previously reviewed fast-source compiler supplies one conditional quantum execution route with polynomial acquired-return/coupling costs and logarithmic rate/precision overhead in its specified centered interface. This calibration receiver earns a missing near-model parameter certificate for bounded k; it neither implements that compiler nor establishes a practical advantage. At small k and moderate requested model accuracy it can make calibration costs independent of microscopic event count. At high accuracy N still grows as inverse square error (and with the whole lifetime envelope), potentially overwhelming any logarithmic-precision execution improvement.

The source comparison is deliberately constructive: the estimation step is the elementary Hoeffding union-sign argument proved above, and the consumer is the separately reviewed common-stationary perturbation theorem. Standard mixing-sensitive Markov perturbation theory remains a strong ordinary comparator, as discussed with primary sources in that theorem. No novelty inference follows from this conjunction.

## 8. Binding boundaries and references

Received proof: COMMON_STATIONARY_CQ_ROBUSTNESS.md, SHA256 467b02dac2c0b5326ce2de8356b4255c49ad1d68f081e840c11bdd024b99ac01. Independent receipt: COMMON_STATIONARY_CQ_INDEPENDENT_REVIEW.md, SHA256 13b1a285ee3865775760308ee808652d98c29c224d7d45d4f318e43e694b1610.

Acquired ideal mechanism: ../clifford_source_acquisition_20261031/AFFINE_PROGRAM_REALIZATION_SPECIFICATION.md, SHA256 9e810f64f08ead6182627693747d71dc34f767fdf0797d8d00df3f9628340f0e; its separate mathematical and executable receipts do not certify a completed quantum execution implementation.

Ordinary primary perturbation comparisons already inspected in the received proof:
- Mitrophanov, Sensitivity and convergence of uniformly ergodic Markov chains (2005): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/26A9854BCB8D103B3A63A9B272616EC0/S0021900200001066a.pdf/sensitivity_and_convergence_of_uniformly_ergodic_markov_chains.pdf
- Szehr and Wolf, Perturbation Bounds for Quantum Markov Processes and their Fixed Points (2013): https://arxiv.org/html/1210.1171

Outside scope: unknown F/G/beta; noninvertible F without another known common stationary law; dependent/state-dependent innovations; a changed clock rate; missed self-loops; noisy or latent labels; uniform-TV estimation of arbitrary n-bit kernels; arbitrary unknown couplings/backaction; arbitrary quantum-source controls; per-transcript posterior truth; free infinite-duration reuse; physical event-path disclosure; and a claim of practical superiority.
