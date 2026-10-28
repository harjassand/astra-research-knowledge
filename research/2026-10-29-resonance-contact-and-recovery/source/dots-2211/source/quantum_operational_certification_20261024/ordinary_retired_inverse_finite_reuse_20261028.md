# Retired-record inverse reuse: quadratic service depth and a matching fixed-workload lower bound

28 October 2026. Candidate extension; separate internal review pending. Depends on the finite ordinary estimator in ordinary_retired_record_covariant_inverse_20261028.md, not on a fictitious independent error draw at each service slot.

## 1. One learned program, arbitrary common finite controller

Use the same unknown one-qubit Vtheta=exp(-i theta Z) calibration family and estimator, with positive contrast a. For J service slots, the SAME private learned inverse is reused. All calibration records and its classical program are inaccessible to the source and external controller; the service joint input/source memory is independent of training conditional on theta. The native service slots may have arbitrary coherent memory, respond to earlier outputs, and interact with any common adaptive/coherent controller. Conditional on the fixed theta, these underlying slot/controller maps do not depend on the learned program except through the deliberately inserted receiver operations. This excludes leaked estimator controls and correlated training/service memory.

At the actual physical ports each slot has native Vtheta after an arbitrary joint map A_j, followed by the learned inverse. Therefore its residual physical rotation is exp(i t Z/2), where exp(i t)=r exp(-i2theta). The reference replaces every such residual by identity, with the SAME native maps, controller and initial memory. J may be an upper bound; stopped histories can be padded with inactive slots.

For a fixed error t let F(t) denote the complete J-slot process after any permitted fixed tester, retaining any final registers of interest. All hidden memory dependence caused by earlier receiver errors is already inside F(t). It is not replaced by the reference memory trajectory.

## 2. A complete second-derivative bound

The rotation channel R_t=Ad_exp(i t Z/2) has generator L(X)=i[Z,X]/2. Its completely bounded trace norm satisfies ||L||diamond<=1; likewise ||L^2||diamond<=1. Differentiating the finite composition of CPTP maps gives J diagonal second-derivative terms and J(J-1) ordered cross terms. Every remaining segment is CPTP and hence a complete trace-norm contraction. Thus

 sup_t ||F''(t)||diamond <= J^2.                             (1)

The statement also covers classical-control blocks and a unitary dilation of measurements, provided the maps themselves are independent of t except at the declared recovery slots. Infinite-dimensional source memory can be handled with bounded complete trace-class maps; accessible input/output dimensions remain finite, or the same inequality is read tester-wise.

At grid angle theta=pi j/K, the acquired estimator's residual phase law is conjugation symmetric. Choose t in [-pi,pi], splitting any mass at the antipode equally between +pi and -pi; these represent the SAME channel, so this changes no physical process. Then E[t]=0. The fundamental theorem of calculus in the complete norm yields

 half ||E F(t)-F(0)||diamond
 <= (J^2/4) E[t^2]
 <= (pi^2/4) J^2 E sin^2(t/2)
 <= min(1, (pi^2/4) J^2 v/N), v=4/a^2-1.                 (2)

The min with one applies to the final physical-channel distance, not to an intermediate signed object. No Pauli CP decomposition of the native source is used. This is an averaged-process statement; retaining the calibration record restores the different loss and its earlier inverse-square accuracy obstruction.

For arbitrary theta, compare its training-record law with the nearest grid theta_0 while holding the ACTUAL underlying A_j and controller fixed. Record-law replacement costs at most sqrt(N)|theta-theta_0|. Changing the deterministic residual angle in J slots costs at most J|theta-theta_0| by a channel hybrid. Hence

 half ||actual averaged process-reference||diamond
 <= min(1, (pi^2/4)J^2 v/N + pi(sqrt(N)+J)/(2K)).            (3)

Choose power-of-two K >= max(4,(22/7)N(ceil(sqrt(N))+J)). The grid term is <=1/(2N). A supplied/acquired lower bound on a is needed to choose a certified requested-accuracy horizon; no automatic unknown-contrast stopping rule is supplied here. Source calls are O(a^-2 J^2/epsilon), with O(log N+log J) finite random bits per probe and explicit finite algebraic/synthesis costs inherited from the one-use source. Whole-protocol implementation/control discrepancy nu adds once. The program really is reused, not resampled independently without paying fresh calibration.

## 3. Independent programs do not improve total ordinary calls at this order

One may instead acquire J independent banks, one inverse per service slot, and keep each program inaccessible. With total N_total ordinary calls and equal bank sizes N_total/J, each average residual slot has error O(v J/N_total). Fresh independent program averaging can then be performed slot by slot even with source feedback, giving J times this allowance, O(v J^2/N_total). It may change constants or control engineering but does not automatically remove the quadratic total-call scaling. This argument requires the J training banks jointly independent of service memory and one another; recycling or bootstrapping the same data does not establish that premise.

## 4. A sharp fixed-workload minimax lower bound, with arbitrary collective decoder

The following is a specified workload lower bound, not a no-go theorem for every possible quantum computation or encoding.

Use the noise-free subfamily p=0, unknown Vtheta. Calibration is still N fresh ordinary single-qubit probes/readouts with arbitrary classical adaptation and fresh within-probe ancillas. Coherent storage/interrogation across calibration calls is excluded. After calibration, encode an unknown logical qubit by the known GHZ isometry |0>->|0>^J, |1>->|1>^J. Send the J physical qubits through J simultaneous native Vtheta calls. Their logical action is V_(J theta). Apply ANY collective CPTP decoder from all J outputs back to a logical qubit, chosen using the calibration record. Records are discarded from the final service metric. No intermediate echo is available in this fixed simultaneous workload. A different encoding/workload is not claimed to obey this lower bound.

Restriction of any collective decoder to the known two-dimensional code subspace gives an arbitrary qubit CPTP map D_y; no decoder family is omitted. Let e_theta(D) be its logical entanglement infidelity after V_(J theta). For theta=+delta,-delta, the two normalized unitary-Choi target vectors have overlap |cos(2J delta)|. Since the normalized Choi matrix of D is a density matrix, its total overlap with these two projectors is at most their largest eigenvalue 1+|cos(2J delta)|. Therefore

 e_plus(D)+e_minus(D) >= 1-|cos(2J delta)|.                   (4)

Entanglement infidelity is LINEAR in D, so its expectation over the actual record law is exactly the infidelity of the record-retired averaged channel. There is no Jensen reversal or conditional-norm substitution.

The calibration laws satisfy TV<=sqrt(N) sin(2delta), by the earlier fresh-probe root-fidelity argument. Integrating (4) against their overlap yields

 max_theta E e_theta(D_y)
 >= (1-TV) [1-|cos(2J delta)|]/2.

Take delta=1/[4 max(J,sqrt(N))]. Then TV<=1/2, Jdelta<=1/4, and sin x>=2x/pi gives the explicit bound

 max_(theta=+-delta) E e_theta(D_y)
 >= (1/(8 pi^2)) min(1,J^2/N).                              (5)

The half-diamond distance of the averaged logical channel from identity is at least its entanglement infidelity (measure the Bell projector). Thus (5) also lower-bounds that retired-record norm. For fixed small requested epsilon, this workload needs Omega(J^2/epsilon) ordinary calibration calls even with unlimited classical computation and an arbitrary collective final CPTP decoder. The equally informed conventional alternative is included. The target does not supply knowledge of theta; even promising just the two candidate angles does not evade the argument.

This matches the J and epsilon dependence of (3) on a non-noisy subfamily up to constants, not its unknown-contrast dependence or arbitrary hardware costs. Coherent multi-call calibration, access to source memory, changing the GHZ code, or allowing pre-noise echo operations are different resources/tasks and are not ruled out.

## 5. Useful failure and actual finite evidence

Even a symmetric two-point residual phase t=+-tau gives logical repeated-phase/GHZ loss sin^2(J tau/2), compared with one-use b=sin^2(tau/2). Their ratio tends to J^2 as tau->0. Retiring the sign does not make the J slots independent. This elementary fixture explains the mechanism; the stronger minimax assertion is proved separately in Section4.

The companion program tests arbitrary CPTP decoder projector inequalities and finite scalar constants. It also samples the actual finite-root ordinary estimator with individually generated Born outcomes, reporting the same-bank reused-phase losses for several J. Those numerical averages are mechanism checks, not a confidence-certified learner, hardware execution, or proof of historical novelty. All original sources remain unchanged.
