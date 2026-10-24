# Acquired local reproducibility without global rank or an initializer

24 October 2026. The owned question/representation is in `FIRST_CONSTRUCTION.md`; the root-proposed retained-context refinement and its literal prompt are preserved in `RETAINED_CONTEXT_ACQUISITION.md`. Earlier scientific files are unchanged. This theorem is a physical-interface substitution, not a solution to finite recognition of arbitrary hidden dimension.

## Physical interface, and the boundary of completeness

Let B be a finite collection of native binary memory cells, with known finite parent sets N_i for i in B. Each legal local control a has an unknown stationary Bernoulli response

    Pr[X_i(new)=1 | complete past and current parent bits, a]
       = p_i^a(X_(N_i)).                              (1)

Selected cells can be pulsed synchronously: their new values are conditionally independent given the old field and controls. A cell stays fixed between requested update pulses. Repeated local sensing is nondemolition, takes paid time, and has bit-error probability at most e_s<1/2 conditional on the true fixed bit and the full physical/noise history. Conditional independent errors suffice. The sensor/clock/sufficiency statements are **supplied physical contracts**. A marginal error ceiling, a changing bit during repeated reads, unmodelled local memory, or simultaneous-control cross-talk not represented by (1) invalidates the certificate.

The architecture need only be complete at the controlled cells and at the finite causal cone of the subsequent experiment. The exterior can have arbitrary hidden dimension and history, and can supply arbitrary nonanticipating boundary-bit trajectories. No small global Hankel rank, global state dimension, exterior transition model, full-field state read, or reset is supplied or inferred. What is excluded is a direct hidden influence into a trained cell that bypasses its stated current parent bits, or a future control that violates the stated local causal graph. Finite observations cannot certify absence of such an influence.

The apparatus offers actual noisy local read sums and site-selective parallel pulses. It does not offer true local contexts, conditional-context preparation, transition probabilities, the contracting modes or a latent sampler. Hold/read latency and site-update count are resources even when many pulses are performed in parallel. During the eventual guard preparation there are no state/bath readouts. Its deterministic public control vector and fixed completion time may remain visible. Intrinsic transition noise is the stipulated unmonitored stochastic channel; conditional claims exposing its microscopic realization are not covered.

## Retained observation protocol

Fix a collar C containing B and all parents of B, candidate controls U, an odd sensor repetition r, first-visit quota m, table width w, and exploration cap T. These are fixed before the experiment. Start from the existing unknown device state. No initializer call is made.

In each exploratory round: read C r times per bit while the native cells are held; take majority labels; apply a fixed public scheduled mode at every cell in C using the old configuration; then read B r times. For each (site i, control a, majority-labelled context z), retain the first m majority-labelled response bits. Stop when all required rows are filled or at T rounds. The actual schedule must offer all declared site/control pairs; it need not guarantee every context. Data-dependent acquisition completion time and its entire measurement record are public calibration information, not themselves claimed to be a reset. The later fixed-time preparation is a separate operation.

There are at most L=T(|C|+|B|) majority decisions. For each fixed-bit decision, Hoeffding-Azuma on the conditional read-error indicators gives

    Pr[wrong majority] <= exp[-2r(1/2-e_s)^2].

Thus any context or response-bit misclassification has probability at most

    alpha_s = L exp[-2r(1/2-e_s)^2].                  (2)

On the event of no misclassification, a row's visit is selected before its fresh update noise and its response has constant conditional mean p_i^a(z). For each row the first m responses therefore satisfy

    Pr[row completed AND |p_hat_i^a(z)-p_i^a(z)|>w]
       <= 2 exp(-2m w^2).                            (3)

This does not condition on eventual visitation. Formally preassign a fresh Bernoulli(p_i^a(z)) tape to every row and consume its next bit on a visit; the first m tape bits obey Hoeffding whether or not they were all consumed by T. Alternatively augment missing post-cap row responses by proof-only Bernoulli bits and apply the martingale bound. These augmentations are not physical observations and do not fill missing data. A coupling of the all-correct sensing path to this ideal context-labelled trajectory gives the union of (2) and (3), without assuming independence between read and update errors beyond the specified fresh conditional update law.

Let M=sum_(i in B) |U| 2^|N_i|. With probability of **return and invalid table** at most

    alpha = alpha_s + 2M exp(-2m w^2),               (4)

every returned response interval [max(0,p_hat-w),min(1,p_hat+w)] covers the true p_i^a(z). Incomplete rows force UNKNOWN. No conditional-on-return confidence or uniform success/runtime bound follows from (4). Without a visitation floor, some rows can be rare or impossible. There is no context sampling oracle hidden in the protocol; all missed, excess and failed visits are paid.

For intervals [L_i^a(z),U_i^a(z)] define the upper influence on parent j by

    Cbar_ij^a = max_(z,z' differ only at j)
                 max(U_i^a(z)-L_i^a(z'), U_i^a(z')-L_i^a(z)). (5)

Then the true single-bit influence C_ij^a is at most Cbar_ij^a. Each boundary site's row includes **all** its parents, including exterior ones. Positivity and simultaneous coverage make subsequent data-dependent mode selection valid. Choose a deterministic mode a_i at each site minimizing the certified row sum, or any other explicit robust selector. If q=max_i sum_j Cbar_ij^(a_i)<1, this has acquired a local contraction certificate. Failure to certify q<1 or the requested finite target tolerance returns UNKNOWN; it does not prove no other preparation is possible.

## Guard coupling and the exact boundary term

Freeze the selected mode vector. For two arbitrary input histories/configurations and arbitrary exterior processes satisfying the input contract, couple the fresh Bernoulli update at i with the same uniform U_i in the two mathematical worlds. A coordinate telescoping gives

    |p_i(x)-p_i(y)| <= sum_j C_ij 1{x_j != y_j}.

Consequently, with D_t(i)=Pr[X_i(t)!=Y_i(t)], A=Cbar_(B,B), and b_i=sum_(j outside B) Cbar_ij,

    D_(t+1)|B <= A D_t|B + b,   D_0|B <= 1.         (6)

This uses no description of the exterior; its disagreement is bounded by one. A componentwise sharper executable bound is

    v_0=1,   v_(t+1)=min(1,A v_t+b).                (7)

Monotonicity and D_t<=1 prove D_t<=v_t by induction. This clipped finite-matrix recursion is the used certificate. It remains a sound upper bound even where a scalar summary is loose.

For the simple scalar comparison, unroll (6):

    D_k|B <= A^k 1 + sum_(s=0)^(k-1) A^s b.

The first term is at most q^k. To bound the second, normalize each complete row Cbar_i by q and add a cemetery probability to obtain a substochastic dependency walk. Read the edges backwards along physical parents. If tau is the first step at which this walk leaves B, then

    sum_(s=0)^(k-1) (A^s b)_i
       = E_i[q^tau 1{tau<=k, exit before cemetery}]
       <= q^d(i,B^c),                              (8)

where d is the shortest directed parent-path length to the exterior. First-exit events are disjoint and tau>=d. This is why no 1/(1-q) factor appears. A bound on internal row sums alone would not justify (8); the exterior-parent weights are included in the acquired q. For no path to the exterior use q^infinity=0. The q=0 case follows directly: one update erases every local dependency. Thus

    D_k(i) <= q^k + q^d(i,B^c).                    (9)

This is the standard Dobrushin/PCA disagreement mechanism; its physical inputs are acquired here rather than supplied response tables.

## Future experiment and reference semantics

Fix a future causal protocol observing only A_visible, running at most H synchronous physical updates and using legal modes on the stated graph. All choices depend only on the common future local observations, frozen calibration information and independent policy randomness. No distant measurement or guard-bath key is a continuation input. Let F be its full backward causal cone at the guard boundary. The guard must contain F.

Once the two prepared configurations agree on F, common future transition/measurement noise and common policy randomization give the same complete future visible transcript. Therefore

    TV(future transcript laws) <= min(1,sum_(i in F) v_k(i)). (10)

This is uniform over all incoming histories and all such future policies/events. It has no transcript-outcome-count factor. On a nearest-neighbor graph, a radius-R guard with R>=H yields the coarser bound

    TV <= min(1, |F| [q^k+q^(R-H+1)]).             (11)

For a general directed graph use actual parent paths, not an unjustified Euclidean radius. |B|, |C| and |F| are resource factors. Bounded degree alone allows exponential volume growth with radius; polynomial growth requires additional geometry such as a fixed-dimensional lattice.

The result is local finite-horizon reproducibility, not a global reset or an unbounded-horizon statement. The exterior can retain the full prior history. There is not generally an autonomous Markov kernel on B alone if its exterior evolves. Choose as reference the same finite preparation/future procedure applied to any actual anchor field/history with its specified exterior process. Equation (10) bounds all other permissible inputs against that reference. The anchor need not be known or independently preparable by the learner. This supplies an operational family with diameter epsilon, not a learner-known exact target law or an exact sampler from a prescribed distribution. A target requiring a different fixed preparation still needs a matching argument.

In the executed source, the actual initial existing field is zero, unknown to the learner. The post-execution scorer uses the guard procedure from that anchor with unchanged zero exterior. No copy of that reference field or exact reference probability enters learning or execution. Future evaluation instead continues from the actual retained field after acquisition and previous trials, with its exterior uncleared.

For one fixed future event per block, let p_star be the reference event probability after the frozen learned guard procedure. Given a true calibration confidence event and any entire accessible prior, (10) gives |E[Y_i|past]-p_star|<=epsilon. Hence

    Pr[return AND |mean(Y)-p_star|>epsilon+tau]
      <= alpha + 2 exp(-2N tau^2),                  (12)

and sum the latter tails across declared blocks. Do not condition this failure probability on return. The Y_i are not assumed iid; no N-trial joint-law closeness is asserted. The evaluated event is a raw noisy sensor output and can include local feedback. Its sensor noise is part of its physical observable law. It is distinct from acquisition's majority errors used to identify native contexts.

## Costs and comparison

Acquisition pays its realized T_run|C| update pulses, T_run synchronous rounds, r T_run(|C|+|B|) raw reads and hold/read latency, all surplus observations, table counters, interval arithmetic and robust mode selection. There are zero full-initializer calls and no supplied visitation-rate guarantee. Storage for the streamed sufficient statistics is O(M log m), plus supplied graph/control metadata; processing every read/count remains computation. Table size is exponential in local parent count.

Every guard use pays k|B| update pulses and k synchronous rounds, with no controller-selection random bits or internal readout. Intrinsic stochastic updates still need the physical noisy device; Python PRNG time is not a measured hardware cost or proof of bath independence.

An equally informed conventional local conditional-table learner can retain the same data, form the same intervals, choose the same modes and reproduce exactly this certificate. UCRL2-style count estimation and PCA/Dobrushin coupling are strong established ingredients. This is not a claim of superiority over those methods or of historical novelty. The capability change relative to the previous rank-two result is that observed local structure can acquire target-specific preparation along one retained trajectory, without a global rank promise, full initialization or a randomized-controller-word record. The supplied local causal/sensor/clock completeness remains substantive.

A full-initializer comparator is legal only if that capability is supplied separately. For the same finite anchor-reference task it can initialize the anchor then run the same guard procedure. At requested total error E>epsilon and confidence beta, compare n_guard>=log(2K/beta)/(2(E-epsilon)^2) with n_init>=log(2K/beta)/(2E^2), not identical trial counts by fiat. Repeated lifetime cost also includes acquisition, k|B| pulses, read latency, future-program costs and any different sample count. Physical initialization/actuation/read costs have not been measured here. A stateful local model-based competitor may predict some tasks more cheaply without manufacturing repeatability; it is not restricted to building a full global Hankel matrix.
