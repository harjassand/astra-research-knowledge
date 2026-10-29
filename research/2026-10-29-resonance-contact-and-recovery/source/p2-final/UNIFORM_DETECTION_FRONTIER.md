# Exact detector-efficiency correction to the passive noise–memory frontier

Root construction, 29 October 2026 Australia/Brisbane. Status: authored corollary; independent review pending. This supplies a matched inefficient-detector comparison and an explicit role for the real feature Gram matrix. It concerns a specified pure-loss detector model, not a general device error rate.

## 1. Model and exact feasibility

Use the fixed passive/vacuum/linear-statistic receiver of the noise-path theorem, with ideal lossless retained modes for this section. Every homodyne detector has the same known efficiency eta in (0,1], modeled as a pure-loss channel immediately before an ideal homodyne. Loss inputs and fresh detector ancillas are independent vacuum. Input capture before the declared ports is not included. The target is an unbiased final Gaussian POVM with original-field features f_t and added covariance N. Put

    R=sum_t Re Gram(f_t), Omega_t=Im Gram(f_t).

**Theorem.** This target is feasible with retained counts q_t if and only if there exist the same skew path S_t and real matrices B_t satisfying

    S_0=S_T=0, rank S_t<=2q_t,
    Gamma_t=S_t-S_(t-1)-Omega_t,
    B_t+i Gamma_t>=0,
    sum_t B_t = eta N-(1-eta)R.                              (1)

Thus a single finite matrix correction transforms the inefficient-detector problem into the ideal passive synthesis problem. Unlike the ideal uncertainty cost, the extra detector term depends on the **real** feature Gram R as well as the commutators.

### Proof

A fixed causal passive network followed by destructive homodyne can be represented by one passive transformation of all arrivals and fresh vacua followed by the corresponding commuting measurements. This is a Heisenberg representation, not a physical permission to retain all arrivals. Append the same eta loss before tracing every unmeasured output; this does not change the measurement channel because tracing after a trace-preserving loss is unchanged.

Uniform pure loss on all output modes commutes with every passive interferometer. Moving it through the global passive network therefore places one eta attenuator on each original input and each fresh vacuum input. The latter remain vacuum. The actual physical receiver and its cut memories are unchanged by this equivalence.

Let f'_t and N' denote the signal features and vacuum measurement covariance of the corresponding ideal-detector network with the same classical reporting coefficients. The attenuated original field gives

    f_t=sqrt(eta) f'_t,
    N=N'+(1-eta)Re Gram(F')
      =N'+(1-eta)R/eta.                                  (2)

The ideal path theorem applies to f'_t=f_t/sqrt(eta) and noise N'. If its skew path and covariance pieces are S'_t,N'_t, set S_t=eta S'_t and B_t=eta N'_t. Rank is unchanged and its semidefinite conditions become exactly (1).

Conversely, given (1), divide S_t and B_t by eta and compile the ideal receiver for f'_t=f_t/sqrt(eta). Implement that passive receiver with the stipulated efficiency eta on each detector. Equation (2) gives precisely the desired unbiased target and covariance N. This proves sufficiency without an active amplifier or an uncounted quantum bypass.

The characteristic-function identity holds on every normal input with every reference. Covariance still is not an unrestricted trace-distance distance from a sharp measurement. Individual readout deadlines and physical memory decay are separate constraints.

## 2. Sharp weighted cost

For positive definite W, let F_q(W) be the ideal path optimum at retained bounds q_t:

    F_q(W)=inf_S sum_t Tr|i W^(1/2)Gamma_t W^(1/2)|.

The inefficient-detector optimum is exactly

    min Tr(WN)=[F_q(W)+(1-eta)Tr(WR)]/eta.                 (3)

The ideal rank-constrained path may still be difficult to optimize. Equation (3) does not remove that difficulty. It separates the irreducible uniform detection term from the ideal causal uncertainty allocation.

This also explains why a nearly commuting field with large real feature norm is not automatically easy to measure physically. Ideal homodyne can have zero added uncertainty on such features, but inefficient collection/readout adds the explicit R term. No bound on photons or injected source energy is inferred merely from R without a matched physical model.

## 3. Matched lossy Bell comparison

For the two-bin target (Q_1+Q_2,P_1-P_2), R=2I and local commutators are J,-J. With zero retained quantum modes, the ideal minimum trace is 4. Equation (3) therefore gives the **exact passive no-memory optimum**

    min Tr N=4(2-eta)/eta,
    N_local=2(2-eta)/eta I,                               (4)

attained by local heterodyne and linear addition. This comparator includes all calibrated fixed passive local Gaussian measurements, including anisotropic alternatives. It is stronger than comparing only a chosen local circuit.

Now use the independently constructed early-record/tap receiver in `noise_challenge/LOSSY_BELL_WITH_EARLY_RECORD.md`, with one physical memory attenuator of transmissivity tau and uniform detector efficiency eta. Its actual covariance is

    N_tap=2(2-tau-eta)/eta I.                             (5)

Thus

    N_local-N_tap=(2tau/eta)I.

For every tau>0, the constructed receiver beats the optimal no-memory passive trace-noise budget under these matched detector assumptions. This is an exact added-measurement-noise comparison, not a total computing-error comparison. The early-record receiver is not proved globally optimal among all possible coherent memories.

If the memory-loss environment is an independent centered thermal Gaussian state with occupation n_e, the receiver adds `2(1-tau)n_e I`. It beats the same no-memory optimum exactly when

    tau/eta > (1-tau)n_e.

This threshold belongs to this specified measurement, supplied Gaussian storage channel and receiver construction. It is not a universal physical memory threshold. Unknown calibration, source coupling and collection before the declared input remain additional terms.

## 4. Limits and ancestry

The lower bound in (4) is **passive** under compulsory inefficient homodyne. Active phase-sensitive amplification before detection can change the detector penalty and is not in this comparator's allowed operations. The ideal Gaussian universality theorem does not preserve a fixed lossy hardware topology, so there is no contradiction.

The tap/feedforward mechanism has established quantum-limited-amplifier ancestry in Josse et al. (2006). It is used here as the strongest conventional ingredient rather than claimed as a new amplifier. Kwiatkowski et al. (2022) study separability of Gaussian measurements after Gaussian error channels; their task and gains differ from this fixed unbiased covariance objective. The present corollary uses the established commutation of uniform loss with passive optics together with the new causal noise-path criterion.

The complete raw record of the constructed lossy receiver and its source-erasure comparison are in the cited operation proof. A matching two-dimensional covariance does not by itself certify equality of that larger record. Preparation, finite bandwidth, local-oscillator resources, source memory, readout/reset and reuse remain physical costs.
