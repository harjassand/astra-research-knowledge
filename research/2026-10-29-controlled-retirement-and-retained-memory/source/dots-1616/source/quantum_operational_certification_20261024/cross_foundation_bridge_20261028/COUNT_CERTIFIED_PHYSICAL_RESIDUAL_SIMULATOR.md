# Count-certified physical residual simulation without a Choi-interior premise

28 October 2026. **New theorem candidate; not yet independently received.** Earlier received exact CP-lift sources remain unchanged. This is a different guarantee: a fitted physical HQMM approximates the source's full **classical** transcript law; no exact CP realization of every source map inside its confidence interval is constructed. Unitary and other boundary maps are permitted. The price is exact certification of the fitted model's observable rank and its agreement with the same legal core, plus a generally prohibitive physical-model search. No novelty or practical advantage is asserted.

## 1. Supplied interface and acquired core

The stationary source has a finite native instrument library `z=(a,o)`, independent repeatable whole-process episode starts, and a supplied upper bound `r` on its observable rank for the entire declared action/test interface. A finite confidence pool covers every preparation, core test, shifted test and optional terminal test **before** data-dependent selection. These are the same substantive rank, stationarity, reset, classical-control and finite-interface premises as the acquired N952 positive-gauge/S7 sources. Counts do not prove absence of unseen modes.

Choose `r` legal normalized preparations `p_j`, including the empty preparation first, and `r` future event tests `f_i`, including the empty trace test first. Preparation outcomes are discarded; no uncharged postselection is allowed. Let

    H_ij = Pr(f_i | p_j),      H_z,ij = Pr(z then f_i | p_j).

The certified nonsingular core gives exact **preparation** coordinates

    C_z=H^(-1)H_z,       c_0=e_1,       m=1^T,
    m sum_o C_(a,o)=m.                                      (1)

For a true unnormalized history `h`, write `c_h=C_h e_1` and `p_h=m c_h`. These coefficients need not be nonnegative. The actual physical source and its legal future effects nevertheless give

    (H c_h)_0=p_h,       0 <= (H c_h)_i <= p_h.              (2)

This positivity is used only for **true prefixes**. It does not claim that all positive coordinate vectors represent physical states.

All fitted and true models use the same preparation/test *procedures*, not the same physical states. Candidate dimension `d` is a declared search resource; it need not equal `sqrt(r)` or the source's microscopic memory dimension. A supplied finite physical dimension upper bound on the source is needed only for the eventual-feasibility result in Section 6, not to verify one successful candidate.

## 2. The fitted physical candidate and its indispensable rank check

Supply actual full `d×d` CP instruments `Phi^f_z`, exactly trace-preserving on each branch sum, and a density `sigma_0`. Native maps may have zero Choi eigenvalues. Run each legal preparation symbolically on this candidate to obtain density matrices `sigma_j`; hence `sigma_1=sigma_0`. Form its exact `H^f,H^f_z` and require

    H^f invertible,      candidate observable rank <= r.     (3)

The rank is over the full declared future interface, including optional terminal-effect seeds. Nonsingularity gives rank at least `r`, so (3) certifies equality. Set

    C^f_z=(H^f)^(-1)H^f_z,       T(v)=sum_j v_j sigma_j.       (4)

The exact candidate quotient theorem then says that **every** future word functional applied to `T(v)` equals its `C^f` prediction. By finite sums and limits the same holds for any almost-surely terminating classical feedback continuation. In general

    Phi^f_z T(v) != T(C^f_z v)                              (5)

as physical matrices: their difference may be unobservable. Equality in (5) is NOT required. This is why merely forcing an invariant positive section would unnecessarily narrow the class.

For real `v`, positivity and normalization of the candidate preparations give

    ||T(v)||_1 <= ||v||_1.                                  (6)

A fitted physical continuation, including its complete record, is a CPTP map followed by a measurement. It therefore sends a Hermitian `T(v)` to a signed outcome measure of l1 norm at most `||v||_1`. This supplies the contractive **fitted suffix**. Fitted quotient maps themselves can have large l1 operator norms.

## 3. Explicit confidence and conditioning bill

For simultaneous count intervals `|H-Hhat|<=D_H`, `|H_z-Hhat_z|<=D_z`, all entrywise, compute

    U=Hhat^(-1),       A=|U|D_H,       ||A||_infinity<1,
    M=(I-A)^(-1)|U|.                                        (7)

Then `|H^(-1)|<=M`. A simple observable conditioning certificate is

    K_core = 1^T M 1.                                      (8)

It implies `||c_h||_1<=K_core p_h` from (2). A sharper finite alternative uses `R=M-|U|`, which bounds `|H^(-1)-U|`, and the `2^(r-1)` vertices of the positive cube:

    K_core = max_{v_0=1, v_i in {0,1}}
                   [ ||Uv||_1 + 1^T R v ].                 (9)

The maximum controls the whole cube by convexity. This is the same acquired inverse-core conditioning mechanism as S7, with the positive-history cube sometimes sharper than its general signed quotient norm; it is not a new source of conditioning.

For a certified physical candidate, define the computable residual bands

    E_z = M [ D_z + D_H |C^f_z|
                    + |Hhat C^f_z-Hhat_z| ],                (10)
    g_a = max_j sum_{o,i} E_(a,o)[i,j],
    b = (K_core/2) max_a g_a.                               (11)

The exact identity `H(C_z-C^f_z)=H_z-H C^f_z` proves `|C_z-C^f_z|<=E_z`. It charges every count, fit and repair residual, and jointly sums outcomes rather than checking only a nonselective map. All computations can be exact algebraic or certified outward rational intervals. Confidence is inherited from the finite data pool, for example rational upper bounds on Hoeffding widths `sqrt(log(2K/alpha)/(2N_s))`. Neither candidate search nor controller selection creates another statistical union bound when every data cut was already simultaneous.

## 4. Full-transcript theorem: true prefixes, fitted CP suffixes

**Theorem.** On that confidence event, for every classical feedback controller over the declared library, selected even after seeing the counts, true and fitted laws from their respective specified starts satisfy

    TV(P_true,P_fit) <= min(1, b E_true[L]),                 (12)

whenever the complete transcript has finite expected number `L` of active native calls and the stopping mechanism terminates the fitted physical model as well. A bounded horizon `H_max` gives `min(1,b H_max)`. If a calibrated independent abort coin of probability `delta` precedes every attempted native call, `gamma=1-delta`, then

    TV(full clocked transcript) <= min(1,b gamma/delta).     (13)

For `M_calls` concatenated memory-retaining clocked invocations from the same initial process start, the safe bound is `min(1,b M_calls gamma/delta)`. Retained memory is not reset between invocations. No condition `gamma b<delta` or Choi margin occurs, and no geometric-coupling improvement is inferred from this additive proof.

**Proof for finite horizon.** Telescope the complete word/tree probabilities using true operations before each switching node and fitted operations after it. At a true prefix `h`, action `a`, the local signed insertion in preparation coordinates is

    Delta_(a,o) c_h = (C_(a,o)-C^f_(a,o)) c_h.

Its fitted continuation has exactly the law obtained by applying the candidate CP suffix to `T(Delta_(a,o)c_h)`. By (6), contraction, (10) and (2), the joint l1 contribution at that node is at most

    sum_o ||Delta_(a,o)c_h||_1
       <= g_a ||c_h||_1 <= (2b) p_h.                        (14)

Sum true prefix masses only over active nodes. At depth `k` their sum is the actual probability of making native call `k`; summing gives `E_true[L]`. Divide l1 by two. Private controller randomization is a convex average, and the same future policy conditional on each full prefix is used in both models. The artificial intermediate hybrids need not be positive; the true and fitted endpoint laws are valid probabilities. Thus no signed-hybrid probability is ever used as a prefix weight.

For unbounded stopping, first truncate both record laws at depth `n` with a labelled censor outcome. The finite bound uses `E_true[min(L,n)]`. Almost-sure termination of both physical models removes their censor tails; monotone convergence gives (12). The independent clock ensures both termination and `E_true[L]<=gamma/delta` and yields (13). For several invocations, sum their true expected call counts. QED.

This is a scalar/classical transcript theorem, not a physical cq-state distance between source and simulator memories, not a quotient operator-norm bound for arbitrary signed initial states, and not an external coherent-reference guarantee. It covers whole rare histories without dividing by their probability, but does not give a uniform bound on normalized postselected histories. An unclocked controller that terminates only in the source needs a separate fitted-termination argument.

## 5. Input and genuinely final readout

The empty preparation fixes both starting coordinates to `e_1`; no initialization oracle is hidden. A declared randomized mixture of acquired preparations is also allowed if the same mixture initializes the candidate. A general new input-state interface is not automatically included.

For a truly final test `a`, let `q_ab` be its source effect row on the core preparations, and `q^f_ab,j=Tr(F^f_ab sigma_j)` for a genuine candidate POVM `F^f_ab>=0`, `sum_b F^f_ab=I`. Include these tests in the true and fitted rank interfaces. Simultaneous count/fit bands `|q_ab-q^f_ab|<=Q_ab` give a terminal debit

    b_term=(K_core/2) max_a max_j sum_b Q_ab,j.              (15)

Use the true-prefix/fitted-suffix telescope above for native calls and one final switch on the true terminal history. Their total TV is at most `b E_true[L]+b_term` (capped at one). No positive off-reachable extension of the exact source terminal rows is needed. This shortcut is **only** for a final readout: a memory-retaining repeated macro requires its complete instrument, not just effects.

Consequently this provider can feed the already received terminal-test/payload transfer, under that lemma's independent future datum, same physical terminal operations, finite acquired terminal library and paid planning premises. It does not strengthen that bridge into a process-tensor or arbitrary external-reference statement.

## 6. A finite candidate acquisition procedure, including boundary points

A local Kraus/Stiefel optimizer may propose candidates but is neither a feasibility proof nor a rank certificate. Here is an intentionally inefficient finite route. Supply: finite data with rational confidence endpoints; the normalized legal core (possibly selected from a predeclared finite pool); observable-rank upper bound `r`; and a finite Hilbert dimension upper bound `d` for at least one exact physical realization of the source interface. First apply (7). Failure is **UNKNOWN**, not evidence of larger rank or nonquantumness.

For a candidate dimension `d`, use real/imaginary matrix-entry variables for its state, full Choi matrices and optional final POVMs. Impose PSD (all principal minors, or equivalent existential factors), exact branch-sum TP, normalized initial state, and all measured probabilities inside their rational bands. Every finite native word probability and every normalized finite discard-preparation probability is polynomial in these variables. Known randomization probabilities in these procedures must be rational or exactly specified real-algebraic numbers; the latter can be encoded by polynomial equations and isolating intervals. Do not introduce conditional division or numerical rank thresholds.

Let `D=d²`. Reachable Liouville spans generated from the initial vector stabilize by word length `D-1`: if one stage does not grow, it is invariant thereafter, and a growing chain starts at dimension one. The dual span from trace and all final-effect seeds also stabilizes by `D-1`. Form the finite Hankel matrix of all such past/future pairs, and impose that all `(r+1)` minors vanish. Its rank is exactly the full candidate observable rank, so this is a finite exact rank certificate. The count-compatible core is nonsingular by (7); hence equality to `r` follows. For `s` native branches there are up to `sum_{l=0}^{D-1}s^l` past words and as many future words per effect seed; the list and the minors can be enormous.

These conditions define a rational semialgebraic set. On the source confidence event the true dimension-`<=d` realization supplies a real feasible point. A smaller source can be embedded as a block in dimension `d`, with arbitrary CPTP completion on its unused orthogonal block and coherences erased. Exact real-algebraic feasibility/sampling therefore supplies an **algebraic**, not necessarily rational, physical candidate, even when every feasible solution lies on a rank-deficient CP boundary. This uses the standard real-closed-field/semialgebraic algorithms, not an assumption that rational perturbations preserve rank. See [Basu's survey, Sections 2.1, 2.2 and 2.5](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf); algebraic-number representation, isolation, exact comparisons and bit cost are part of the computation. A finite resource-capped implementation may return UNKNOWN. There is no polynomial-time or practical solver claim.

A more compact equivalent existential witness can replace the word list. Write `G` for columns `sigma_j` in Liouville coordinates. For some `0<=k<=D-r`, introduce a kernel matrix `K` and matrices `M_z,L_z` such that

    tau K=0,       Phi^f_z K=K M_z,
    Phi^f_z G=G C^f_z+K L_z,       sigma_0=G e_1,             (16)

and every declared terminal effect annihilates `K`. Together with `H^f C^f_z=H^f_z`, physicality, and invertible `H^f`, these polynomial identities certify all future words by induction. Independence of `K` columns need not be imposed for soundness. Completeness follows by choosing a basis of the actual reachable unobservable subspace; its dimension is at most `D-r`. Enumerate the finitely many `k`. This avoids the explicit word expansion in the formula, not the nonconvex exact search or its bit complexity. Exact physical intertwining on the chosen core section is still not imposed.

A compatible candidate also yields a direct worst-case finite-data estimate, without a successful local optimum. Put

    B_z=M(|Hhat_z|+D_z).

The same Neumann bound applies to `H^f`, so `|C^f_z|<=B_z`, and compatibility implies

    E_z <= 2 M [D_z+D_H B_z].                              (17)

Thus (17) can certify the target error for **every** physical candidate feasible in the bands. With `J=||M||_(1->1)`, `h=||D_H||_(1->1)`, `d_z=||D_z||_(1->1)` and `s_z=||Hhat_z||_(1->1)+d_z`, the cruder scalar version is

    b <= K_core J max_a sum_o [d_(a,o)+h J s_(a,o)].         (18)

For example, if every uncertain entry has width at most `w`, then `h,d_z<=r w` and `s_z<=r+r w` for probability tables; all rank and inverse-core powers remain visible. Counts must make this bound (or the sharper residual bound) times the declared expected-call cap small. Equation (18) is an accuracy/conditioning bill, not a dimension-only sample guarantee.

For eventual accuracy, keep a truly nonsingular legal core and shrink simultaneous count bands. Any compatible candidate has `H^f -> H` and `H^f_z -> H_z`, hence `C^f_z -> C_z` uniformly under the acquired inverse bound. Equations (10)-(11) then give `b -> 0`; final bands similarly give `b_term -> 0`. With a fixed positive clock or fixed horizon, any target transcript error is eventually certified. This is conditional on the supplied dimension/rank bounds and an actually available sufficiently conditioned core. A finite pool need not contain such a core; rank discovery, unlimited dimension search, or a sample budget independent of conditioning is not supplied for free. A sequential scheme requires an explicit summable failure allocation across its rounds.

The output is a mathematical physical simulator and a classical planner. Classical numerical evaluation of it needs certified precision, and controller search can be exponential. If a physical implementation of the fitted simulator is requested, algebraic Kraus/state descriptions must be compiled and their **complete instrument** error, storage, gate count and synthesis precision charged. An additional per-step half-diamond synthesis error can be telescoped separately against the fitted physical process. Exact algebraic coefficients are not free laboratory controls.

## 7. Attempted breaks and relation to the existing results

1. **Drop candidate rank:** false. Source emits `0` forever. A two-state classical/quantum candidate starts in state 0, emits `0` and moves to state 1, then emits `1` forever. For the one-dimensional empty core, `H=H^f=1` and both one-step shifted tables agree exactly, so (10) is zero. Depth-two TV is one. The candidate's observable rank is two, violating (3). Matching a finite core without exhaustion is insufficient.
2. **Require physical section intertwining:** unnecessary. A qubit candidate with only deterministic unitary-X action and initial `|0><0|` has observable rank one and `C^f=1`, while `Phi^f T(1)=|1><1| != T(1)`. Its trace-zero kernel absorbs the difference; every observed continuation is still identical. Equation (16) uses `K=Z`, `Phi K=-K`, `Phi G=G-K`.
3. **Use fitted prefixes in (14):** unjustified without a physical lift of their coordinate error. The entire improvement comes from true positive prefixes and fitted physical suffixes. This orientation cannot silently be reversed.
4. **Return to a signed predictor:** S7 already controls its primitive error in the true quotient norm. Its clocked resolvent has `gamma e/(delta-gamma e)` and requires `gamma e<delta`; a signed predictor can expand. This source reuses S7's acquired core conditioning but imposes the additional physical-candidate/exact-rank obligation, replaces signed resolvent evaluation by CP suffix contraction, and proves classical full-law error from the fixed physical start. It does not repair a nonexistent norm defect in S7, nor dominate S7's stronger signed-input quotient-operator guarantee.
5. **Perturb a strict-interior lift to cover unitary maps:** not done. No correction to the true uncertain map is required. The fitted and source unitary channels may differ, yet the residual bound applies. Boundary physicality is certified on the candidate itself, not inferred from a Choi margin around its neighborhood.
6. **Free CP realization of an abstract quotient:** not assumed. [Monras–Winter, TQC 2014](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99) already studies finite CP realizations, reachable/observable quotients and the lifting obstruction. Here an actual full CP candidate is explicitly searched and checked. The transfer does not prove that every positive/operator-system quotient has a CP extension.
7. **Novel learning mechanism from renaming:** not claimed. [Srinivasan–Gordon–Boots, AISTATS 2018](https://proceedings.mlr.press/v84/srinivasan18a.html) already learns HQMMs without microscopic environment tomography; Kraus/Stiefel and Liouville/Choi methods can supply the same candidate. This is an expensive confidence-and-rank wrapper and a one-sided perturbation argument, not a new practical optimizer or a quantum advantage over equally informed conventional methods.

## 8. Provenance and verification status

Original S7 theorem was retrieved completely at Astra revision `b354d60874c165312fd33b5c031570c6983801e8`, source SHA `a968467bdfba55c314008566d6e9f1854cc3250612c842868088ef984cedf82d`, and saved with metadata as `imports/N952_S7_PREDICTIVE_OPERATION_THEOREM.txt`. Its late norm adjudication SHA is `519737f62abcf012c8b9274e1c7059f8e5cb1f0e5e798d6f48c20b6b5d7f6704`. The earlier positive-gauge theorem is preserved separately. This source has not run real-algebraic HQMM acquisition or obtained new source samples. `physical_residual_simulator_exact_check.py/.json` is an exact rational/algebraic diagnostic, **not count acquisition**: zero source calls, episode starts and RNG calls. Its qubit source and candidate have rank-four legal cores; every native branch has rank-one Choi matrix. The source's small rational unitary `((999999)I+(2000)iZ)/1000001` is fitted by identity, while unitary preparations and projective tests are shared. Hypothetical rational probability bands of width `10^-7` yield `K_core=5.000007000007`, local coefficient `b=0.0200449880280321`, horizon-11 full-record TV `0.002999975000159` below the uniform bound `0.220494868308354`, and clock bound `0.0400899760560642` at `delta=1/3`. The complete true-prefix/fitted-suffix telescope is checked with **zero exact residual**, including negative true preparation coefficients and feedback. The script also checks both counterexamples in points 1 and 2 above. These synthetic analytic bands carry no confidence/acquisition claim and demonstrate no resource advantage.
