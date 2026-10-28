# Ordinary prequential recovery with a private terminal payload time

28 October 2026. **NEW PROOF CANDIDATE; independent review pending.** No new source samples. Received locality/selector manuscripts and the 12:15 archive remain unchanged. This is a slower, different architecture: one logical qubit, a fixed encoder, one known physical output patch, arbitrary retained source memory, and ONE terminal payload. It does not import iid Bures acquisition, the growing-selector reset assumption, a learned predictive process model, or a future-window certificate.

## 1. What is supplied, what is learned, and what is compared

The source has a known physical output register P of w qubits, d=2^w. At call t its complete causal CPTP map takes the new logical input L and all retained memory M to P and new memory M'. It may depend on time and exposed past controls. M includes every source-accessible classical or quantum record; its dimension is unrestricted and is not reconstructed. No fresh input label, measurement choice, learner's current decoder, or private terminal time is leaked to the source except through the specified quantum input and explicitly declared public interface. In particular the payload and probe use the SAME complete source port/map at a given history; a separate externally controlled payload channel is excluded.

The learner knows the physical register and can prepare ordinary single-qubit Pauli eigenstates and measure physical Pauli words by local one-qubit controls. It learns a CPTP decoder D:P→one qubit. An exact Choi description is not a supplied recovery oracle: it is computed from the actual finite integer records below and compiled with a paid error budget.

A newly supplied payload Q, with arbitrary retained reference R, has its FULL joint QR state initially product with the source memory and all acquisition randomness. It is held in trusted isolated storage until its use. This fresh-input independence is a real premise; pre-existing payload–source correlations are not covered by this theorem. All source calls and intervening classical computations have a fixed, publicly specified schedule independent of the secret terminal time until its current source call is complete. Delaying or routing the current source call differently because it carries the payload would violate the premise. The recovered output is isolated before any later untrusted interaction. The protocol can stop then; no post-payload learning or repeated service is claimed.

For mathematical analysis define a length-N ALL-PROBE process with the same source, learning rule, and measurement instruments. Let h denote its complete actual classical record before call t, p_t(h) its probability, and E_(t,h) the CPTP channel from a new independent qubit to P obtained by supplying the actual conditional memory state. The source need not have a classical hidden state: conditional density operators here result from actual exposed instruments, not conditioning on nonexistent microscopic records.

The comparator is a FIXED decoder D evaluated on these ACTUALLY VISITED histories:

    R_N(D)=(1/N)sum_t E_h[1−F_e(D E_(t,h))].             (1)

It is not the counterfactual occupation law obtained by changing an earlier control policy, deploying D on previous data, or resetting the memory. The basic theorem competes with inf_D R_N(D), where D is fixed before the random trajectory. It does not claim regret against a hindsight decoder chosen separately for each realized path. A stronger common-algebra corollary below identifies a single decoder that is optimal at every visited history.

## 2. Actual single-copy records and conditional unbiasedness

Use the normalized, output-first Choi convention

    J_D>=0, Tr_output J_D=I_d/d, Tr J_D=1,
    D(r)=d Tr_input[J_D(I_2 tensor r^T)].                 (2)

The feasible set K is known, compact, convex, has Frobenius diameter at most sqrt(2), and has the rational interior point J_1=I_(2d)/(2d). The squared distance of J_1 to every J in K is at most1.

At probe t choose j uniformly from X,Y,Z and s uniformly from ±1, independently of the past, and input |j,s>. Choose a physical Pauli word W uniformly from {I,X,Y,Z}^w, independently of the source and input. Measure its nonidentity factors by local Pauli settings and retain their parity b in {−1,+1}; for W=I set b=1. The actual record (j,s,W,b), or the full local outcomes from which b is computed, is sufficient. This is not an oracle revealing a Pauli coefficient. Only one actual source output is used.

For the current conditional channel let r_(j,s)=E_(t,h)(|j,s><j,s|). Since the Pauli expansion is r=(1/d)sum_W Tr(Wr)W, the actual random matrix rhat=d b W is unbiased for r_(j,s). Define

    g_t=−(d^2/2) s b (sigma_j tensor W^T).                (3)

Every entry is a rational Gaussian integer times a known rational scale. Conditional on the ACTUAL prior record,

    E[g_t|h]=gradient_J p_(t,h)(J),
    p_(t,h)(D)=1/2−(1/12)sum_(j,s)
                         s Tr[sigma_j D(r_(j,s))]
               =(2/3)[1−F_e(D E_(t,h))].                (4)

The second equality is the exact six-state-to-Bell identity for every trace-preserving qubit channel, including nonunital ones. Equation(4) requires neither iid calls nor a source-memory reset. It uses fresh labels and an actual CPTP channel for the NEW independent input. A learner may retain its own recorded labels/outcomes; correlations of those records with M are already in h.

The gradient bounds are deterministic:

    ||g_t||_F^2=d^5/2,
    ||g_t||_op=d^2/2.                                   (5)

Set G=d^2 2^ceil(w/2), so ||g_t||_F<=G and G^2<=2d^5. This integer choice keeps the steps below rational. It is deliberately not the best possible shadow/online-learning dimension constant.

## 3. Finite online CPTP update, with no unphysical iterate

Choose N to be a power of4, and eta=1/(G sqrt(N)). Before the current source call, J_t is fixed using only previous probe records. After a probe (never after the payload), let Y_t=J_t−eta g_t and return a rational J_(t+1) in K satisfying

    ||J_(t+1)−Y_t||_F^2
        <=min_(J in K)||J−Y_t||_F^2 + xi,
    xi=1/(16N^2).                                      (6)

This is a known finite convex quadratic problem, not an optimization over the unknown source. The Frobenius norm square has a standard Schur-complement SDP epigraph. The feasible Choi set has a known interior center. A deterministic polynomial-cap weak SDP solve followed by the EXACT rational Choi repair from the received local-CPTP ERM addendum gives a physical rational iterate at prescribed precision. To make this import explicit, use its unnormalized variable K=dJ, approximate minimum eigenvalue and TP residual at most delta, and

    Khat=Ktilde+(I_2/2) tensor (I_d−Tr_output Ktilde),
    Kphys=(Khat+4delta I_(2d)/2)/(1+4delta),
    Jphys=Kphys/d.                                      (7)

The received repair bounds give ||Jphys−Ktilde/d||_F<=9delta. Here ||Y_t||_F<=2. On the relevant unit-trace near-feasible ball, the squared-distance objective changes by at most100delta for delta<=1/100. Thus choose delta<=xi/1000 and the solver objective slack <=xi/4, with a known-center perturbation allowance <=xi/4. The repaired feasible result satisfies(6). Exact rational positivity/TP certificates are checked. Numerical inability to deliver the promised certificate is not a new statistical event: it belongs in the explicitly supplied implementation contract; a safe replacement channel stays physical but does not inherit an unearned optimization guarantee.

To avoid recursive denominator growth, fix delta=xi/1024 and require the solver output BEFORE(7) to lie on a prescribed dyadic entry grid of mesh u<=min{delta/(64d),xi/(1024d)}. Round real and imaginary components with exact Hermitian symmetry. A 2d-dimensional matrix changes by at most4d u in operator norm and its output partial trace by at most8d u. Start the solver with residual tolerance delta/2 and objective slack xi/8; these rounding changes fit the preceding delta and objective allowances. The grid is fixed by d,N, not by earlier denominator lengths. Applying(7) then gives every iterate a denominator dividing the same explicit product of the grid denominator, d and the denominator/numerator of1+4delta. Thus each iterate and each Y_t has polynomial bit length in log d and log N. This is a finite classical-output requirement of the paid convex solver, not ideal exact spectral projection.

The received import is `ordinary_local_mixed_gauge_cptp_erm_addendum_20261028.md`, SHA1c77dc05f10750e0c53ce51a6c9676f529883f421b4f8ac472d610de62d3959c, §1. Only its finite known-center solver/Choi-repair/compilation machinery is used, NOT its iid state-acquisition theorem. No source eigenvalue floor is supplied.

Here is a direct regret proof, so no online-learning black box is needed. Let P_t be the exact Euclidean projection of Y_t onto K. Strong convexity and the projection variational inequality give ||J_(t+1)−P_t||_F<=sqrt(xi). Since both are in K, for any fixed J_* in K,

    ||J_(t+1)−J_*||_F^2
      <=||J_t−eta g_t−J_*||_F^2+3sqrt(xi).

Expand, sum, and use the initial distance bound and(5):

    sum_t <g_t,J_t−J_*>
      <=1/(2eta)+(eta/2)NG^2+3N sqrt(xi)/(2eta)
      <=(11/8)G sqrt(N) <2G sqrt(N).                    (8)

This is a PATHWISE inequality for the acquired gradients. Conditional unbiasedness then implies, for each fixed decoder D,

    (1/N)sum_t E[p_(t,h)(D_t)−p_(t,h)(D)]
                   <=2G/sqrt(N).                       (9)

Taking the infimum over fixed D in the EXPECTED occupation objective is valid. Replacing it by a random future-selected trajectory minimizer would require a separate uniform martingale argument and is not asserted.

Standard projected online convex learning is a conventional method, not a priority claim. The original primary source is [Zinkevich, *Online Convex Programming and Generalized Infinitesimal Gradient Ascent*](https://www.cs.cmu.edu/~maz/publications/techconvex.pdf). The CMU primary technical report, Algorithm1 and Theorem1 (PDF pages4–5), was retrieved and read; the author ICML PDF endpoint first returned502. The load-bearing statistical proof here is(3)–(9) for the actual quantum instruments and finite repaired iterates; no claim of separation from the strongest conventional learner is made.

## 4. Private terminal-time transfer: an actual channel, not a future prediction

At initialization choose T uniformly from{1,...,N}, independently of the source, payload/reference and probe coins. It uses exactly log2(N) private fair bits. At calls t<T perform the probe and update above. At call T use the independently held payload through the SAME source port, apply the previously fixed decoder D_T, isolate its output, and terminate. Never measure the unknown payload as a probe and never update from it. J_T is frozen before the current source call. The schedule of preprocessing and decoder compilation is identical on probe and payload prefixes; any relevant physical controls are completed before role-dependent operations, or concealed under the trusted interface assumption.

For each fixed t, conditional on T=t the entire first t−1 process is exactly the all-probe process. The payload/reference remains untouched and product with its source memory. Thus the actual averaged payload channel is EXACTLY

    Lambda=(1/N)sum_t sum_h p_t(h) D_(t,h) E_(t,h).       (10)

This is an equality of CPTP maps on the input qubit, hence persists after tensoring any reference. The source can discriminate quantum inputs within its CPTP map; nothing assumes it fails at doing so. What is excluded is an additional side channel telling it to apply a different complete map when T=t. No equivalence of probe-versus-payload post-call memory instruments is needed: the payload is terminal. There is no counterfactual use of the current unknown datum as a gradient.

By linearity of Bell fidelity and(4),(9),

    1−F_e(Lambda) <=inf_D R_N(D)+3G/sqrt(N).              (11)

For 0<epsilon<=1, take N to be the least power of4 at least(6G/epsilon)^2. Then statistical excess is at mostepsilon/2, N<144G^2/epsilon^2<=288d^5/epsilon^2, and the actual protocol uses at mostN COMPLETE source calls, including its ONE payload. The mean call count is(N+1)/2; the worst-case cap remainsN. A whole-process operational discrepancy at mostepsilon/2 gives final expected Bell loss <=inf_D R_N(D)+epsilon. If epsilon is compared with a gate-level imperfection budget, both the actual learned service and the intended reference experiment must use the declared common ideal-interface convention; implementation error is not silently absorbed twice.

Equation(11) is an averaged terminal-service guarantee. It does not certify every terminal time, every observed record, a particular final frozen decoder on future calls, or an indefinitely reusable source. No postselection/acceptance denominator is present. For an arbitrary untwirled qubit payload, Bell loss gives the usual dimension-dependent continuity bound, not the same numerical diamond error. An OPTIONAL conventional private logical Pauli twirl of the terminal service preserves Bell fidelity and makes the averaged qubit channel Pauli, for which half-diamond distance to identity equals its Bell loss; this changes the service, costs fresh trusted input/output Pauli controls and two private bits, and does not furnish a guarantee conditioned on the retained key.

## 5. A genuine retained-gauge CP process with a common per-history oracle

One concrete supplied family is a fixed unknown unitary U:L tensor G→P, dim G=d/2, together with arbitrary causal CP maps

    G_(alpha,t,h_public): M→G tensor M', alpha=I,X,Y,Z,
    sum_alpha Tr_G G_alpha trace preserving,

such that the COMPLETE source map on even correlated L,M inputs is

    Efrak_t =Ad_(U tensor I_M') composed with
                 sum_alpha (Ad_(P_alpha) tensor G_alpha). (12)

The source may keep coherent quantum memory, prepare correlated/noncommuting gauge states, and change them with time or exposed history. No gauge spectrum floor, flag, or environment reconstruction appears. Assume the CP-order dominance G_I−G_alpha is completely positive for each alpha. This strong uniform operator promise is not inferred from finite records. It implies for every conditional memory state sigma that the emitted gauge operators H_alpha=Tr_M' G_alpha(sigma) obey H_I>=H_alpha. One could separately impose the earlier conditional contrast CP margin, but the slower learner above does not need it.

The fixed ideal decoder D_*(r)=Tr_G(U†rU) is then optimal among ALL CPTP decoders P→qubit at each actual history. To prove the comparison, feed a Bell half through the channel. Before U the joint state is sum_alpha Phi_alpha tensor H_alpha. For any decoder, let E=(id_R tensor Dtilde†)(Phi_0), with Dtilde=D composed with Ad_U. Then E>=0 and Tr_R E=I_(L G)/2. The Bell diagonal blocks T_alpha=Tr_(R L)[(Phi_alpha tensor I_G)E] are positive and sum_alpha T_alpha=I_G. Its Bell fidelity is sum_alpha Tr(H_alpha T_alpha)<=Tr H_I. D_* attains equality. Consequently

    inf_D R_N(D)=R_N(D_*)
      =(1/N)sum_t E_h[1−Tr H_(I,t,h)],                  (13)

and(11) learns to within epsilon of the strongest known-noise terminal oracle on the SAME occupation law. This does not compare to a policy that changes the source's earlier memory evolution. If the source is exactly logical-noiseless (only alpha=I), the oracle risk is zero even when fresh gauges have tiny, vanishing, or adversarially changing supports.

## 6. Why a deterministic train-then-use cutoff fails

Here is an exact finite-dimensional obstruction, not a lower bound against every randomized algorithm. Let w=2, one gauge qubit, and two worlds U_0=I and U_1=CNOT_(G→L). A retained classical timer emits gauge |0> for the first K calls and gauge |1> at call K+1; all Pauli noise is identity, so the source has contrast1 and dominance, and U_b is fixed in each world. Both worlds produce IDENTICAL quantum input/output experiments for every possible first-K logical probe strategy. At the deterministic payload call they apply respectively I or X to the logical state, with the same gauge |1>. Any one learned terminal decoder therefore has average Bell fidelity at most1/2 across the two worlds (their uniformly averaged logical channel is complete X dephasing); at least one world has Bell loss >=1/2 while its informed decoder has zero loss.

This example uses a legal CP memory timer. It does not prove impossibility for private randomized stopping: a timer that attacks one designated time only hits that time with probability1/N under uniform T. The prequential mechanism explicitly pays for early, poorly learned payload slots instead of claiming post-training gauge coverage.

## 7. Finite physical resources and scope

* At mostN actual source calls, one ordinary logical qubit input per call, w physical output qubits per call. No protected entangled calibration reference. The unknown payload is held in trusted storage for at mostN−1 call/computation periods; its idle error is paid in the whole-process budget.
* Each probe uses at mostw one-qubit Pauli measurement settings, at mostw local measurement results, and a parity computation. There is no cross-copy quantum memory. The learner stores an O(d^2)-entry rational Choi iterate and current records; retaining all raw audit data costs O(Nw) bits plus labels. Source memory is retained by the source, not assumed reset or available to the learner.
* N polynomial-cap quadratic SDP updates, each in dimension2d and precision polynomial in log N, log d and the declared physical error budget. This is polynomial in d, exponential in w. Classical compilation time counts toward the payload-storage duration. A common public padded schedule prevents computation duration from leaking the current role.
* Each rational feasible decoder has the received exact algebraic Stinespring realization with environment dimension at most2d and a unitary embedding of dimension at most4d, using at most two additional local reset qubits. Dense local synthesis costs O(poly(w)4^w) elementary gates before precision/routing overhead. If all J_t are compiled before each current call to equalize timing, charge ALL N compilations and their classical cost; only the terminal recovery must be coherently applied. No free arbitrary-channel receiver primitive is assumed.
* W takes2w fair bits and s one bit. To draw j, use two-bit rejection (reject value3), with R=ceil log2(2N/nu_rng) retries per potential probe; total failure <=N4^(−R)<=nu_rng. T uses log2 N bits. Cap all samplers in advance and use a physical replacement on exhaustion; charge its at-mostnu_rng utility loss within the single operational allowance. The cap is log2 N+N(2w+1+2R) bits, plus any optional terminal twirl. No confidence-independent infinite rejection loop.
* There is NO iid confidence allocation hidden in(11): it is an expectation bound from conditional unbiasedness and pathwise regret. RNG/compiler/storage errors use one declared whole-process discrepancy allowance. A confidence statement about a completed all-probe window can be added by martingale methods, but it does not become a per-history certificate for the randomly terminated payload.
* Fixed encoder and known local output patch remain premises. This does not inherit the earlier m-dimensional selector search, unknown interval localization, multiple compatible logical outputs, or finite-time tail theorem without new work. The stronger equally informed conventional baseline is exactly online convex decoder learning from the same local tomographic records; no computational or experimental advantage over it is claimed.

The complementary acquired predictive-process construction in `cross_foundation_bridge_20261028/TERMINAL_TEST_PREDICTIVE_RECOVERY_TRANSFER.md` acquires a richer planning interface but pays its whole-process-start/core/conditioning promises. Here no process model or whole-process restart is acquired; the service is only a privately timed one-shot terminal payload on the ongoing all-probe trajectory. Existing Astra N1023 role-sealing/coarse-instrument machinery is prior, separate scope. A fresh connector check at14:08 UTC reported current revision fb960ac7b07b766d5703c43efbee8cd9d4492718; its current capsule explicitly distinguishes actual complete-call boundaries from merely matching input marginals. This candidate does not rebrand that mechanism.
