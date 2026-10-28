# A count-certified CP predictive realization: a restricted positive result

28 October 2026. Local derivation and synthetic count replay, not an independently received theorem, hardware experiment, or historical novelty claim. The protected encoder/recovery programme is unchanged. This is a sufficient certificate for a **full matrix-algebra predictive gauge**, not a solution for general quantum observable quotients.

## Result and inherited interface

Yes: finite ordinary episode counts can certify an exact virtual quantum instrument and a nearby implementable predictive model without identifying physical memory. The sufficient class has observable rank `r=d²`, an invertible real gauge into all Hermitian `d×d` matrices, and a robust Choi-positivity witness. Complete classical transcript error then contracts. A count-only qubit fixture below passes and excludes **every four-state classical HMM realization**, while not excluding larger HMMs.

The acquisition premises remain substantial: a declared finite stationary action/outcome library; independent repeatable **whole-process** starts; an exact architectural upper bound `r` on observable rank; and a finite candidate pool of legal normalized preparations and future event tests. The simultaneous confidence event covers the pool before selecting a core or gauge. These are inherited from `imports/N952_POSITIVE_GAUGE_THEOREM.md`, source SHA256 `8f3e50d85cc58803f29cda029e22c535d20fd2affc2779bf65bc8ad9b681fbef`, Astra revision `fb960ac7b07b766d5703c43efbee8cd9d4492718`; import metadata records the source route and freshness. No weakening to single-trajectory/no-whole-reset learning is made.

Choose `r` normalized preparations, with the empty preparation first, and `r` future tests including trace. Let `H` and `H_z` be their exact ordinary event probabilities, with `z=(a,o)`. Invertibility of `H`, together with the rank upper bound, makes the preparation coordinates exact:

    C_z = H^(-1) H_z,    c_initial=e_1,    trace(c)=1^T c.

This is an observable quotient, not an identification of its physical density operators.

## 1. Full Hermitian gauge and interval certificate

Fix a Hilbert–Schmidt orthonormal Hermitian basis `F_mu` of `Herm(d)` and write `X(x)=sum_mu x_mu F_mu`, with trace row `t_mu=Tr F_mu`. Choose an invertible real `S` satisfying

    1^T S=t,       c=S x,       sigma_0=X(S^(-1)e_1) >= 0.

Then `Tr sigma_0=1` exactly. Define `W_z=(HS)^(-1)H_z S`. It acts on every Hermitian matrix by `Phi_z(X(x))=X(W_z x)` and has a unique complex-linear extension. Its input-first, unnormalized Choi matrix is

    J(W_z)=sum_mu,nu (W_z)_mu,nu F_nu^T tensor F_mu.

It is Hermitian for real `W_z`, and `||J(B)||_F=||B||_F`. The same isometry holds for an equally scaled orthogonal basis, using the dual basis in the first tensor factor; the fixture uses `I,X,Y,Z`, duals `I/2,X/2,Y/2,Z/2`.

Suppose simultaneous count bounds give `|Hhat-H|<=D_H`, `|Hhat_z-H_z|<=D_z`. For a selected `S` set

    Vhat=Hhat S,  D_V=D_H |S|,  U=Vhat^(-1),  A=|U|D_V.

The computable sufficient check `||A||_infinity<1` proves actual invertibility and

    |(HS)^(-1)| <= M=(I-A)^(-1)|U|.

Take any real fitted maps `Wtilde_z`, including repaired ones. Put

    R_z=Vhat Wtilde_z-Hhat_z S,
    E_z=M [D_z|S| + D_V|Wtilde_z| + |R_z|].             (1)

Then `|W_z-Wtilde_z|<=E_z`. Indeed, multiply the difference by `HS`, insert `Vhat Wtilde_z`, and bound its three residual terms. Inverse bounds follow by an absolutely dominated Neumann series. The repair residual is never free.

Let `kappa_z` be a certified rational upper bound on `||E_z||_F`. Consequently

    -kappa_z I <= J(W_z)-J(Wtilde_z) <= kappa_z I.

Require exact fitted instrument constraints and initial positivity:

    J(Wtilde_z)>=0,
    sum_o Tr_output J(Wtilde_(a,o))=I for every a,
    sigma_0>=0, Tr sigma_0=1.                           (2)

Finally require a verified Choi lower bound

    J(Wtilde_z) >= m_z I,       m_z >= kappa_z.          (3)

Equations (1)–(3) certify that the **exact** `Phi_z` are CP. True causality implies `t sum_o W_(a,o)=t`; hence their sums are TP. Individual branches are automatically trace-nonincreasing. A PSD fitted Choi matrix alone is not this certificate.

Products of the exact virtual maps reproduce every legal word probability from `sigma_0` by the coordinate identity. Positivity and trace normalization therefore give a valid HQMM representation of the actual classical process, including all feedback controllers using the library. This requires no CP map, isometry, or state reconstruction between virtual and physical memory. The initial state is exact because the empty preparation is in the core, not an estimated independent tomography output.

Known identically zero branches can be omitted with zero uncertainty. Otherwise the stated scalar-radius test is an interior certificate. It generically cannot certify unitary/rank-deficient Choi maps from unconstrained two-sided finite-width boxes; a verified structural face/support restriction would be extra input.

## 2. Contractive error, and the distinction between two bounds

Define the joint quantum-to-classical-quantum instrument channel

    I_a(X)=direct_sum_o Phi_(a,o)(X).

Choi domination by `kappa_z I` bounds the diamond norm of a Hermiticity-preserving branch difference by `d kappa_z`; a positive/negative Choi majorant is a feasible norm bound. Thus a usable local half-diamond error is

    t_* = min(1, (d/2) max_a sum_o kappa_(a,o)).         (4)

A tighter rigorously verified norm optimization may replace (4). Both models are CPTP at each chosen action. In the direct-sum state indexed by the **entire classical history**, contractivity and a hybrid argument give

    TV(full transcript through H native steps) <= min(1,H t_*).   (5)

The controller may be chosen after the data and adapt at every prefix. Its conditional action maps are blockwise CPTP, so no policy union bound or normalized rare-history estimate is needed.

A second, stronger structural conclusion is available when (3) holds. Set

    epsilon=max_z kappa_z/m_z <=1.

For `epsilon>0`, every exact instrument has the common-CP decomposition

    Phi_z=(1-epsilon) Phi_tilde_z + epsilon R_z^CP,
    R_z^CP=[Phi_z-(1-epsilon)Phi_tilde_z]/epsilon.

Each residual is CP because its Choi matrix is at least `(epsilon m_z-kappa_z)I`; its branch sum is TP by **both exact trace identities**. Therefore the whole actual virtual process is identical to the fitted process until the first state-independent residual-mixture flag. This proves

    TV(full transcript) <= 1-(1-epsilon)^H.             (6)

This is not an inference from classical maximal coupling of quantum states. The explicitly certified CP mixture is its premise. It also shows `t_*` can be replaced by `min(t_*,epsilon)`.

With an independent known abort coin `delta` before every native attempt and `gamma=1-delta`, and retaining memory on abort, a controller can only shorten the geometric number of calls. Hence the full terminal transcript satisfies

    b_add=min(1,gamma t_*/delta),
    b_mix=gamma epsilon/(delta+gamma epsilon),
    TV <= min(b_add,b_mix).                             (7)

For `M` adaptive sequential invocations retaining memory, the safe bounds are

    TV <= min(1, M gamma t_*/delta, 1-(1-b_mix)^M).      (8)

Do **not** replace the last term by `1-(1-b_add)^M`: trace-distance proximity alone supplies no common positive quantum substate. No signed-resolvent smallness condition `gamma e<delta` occurs. Norm conversion and inverse-core conditioning have not disappeared; they are explicit in (1), (4), and the Choi margins.

Although these inequalities hold for the abstract CP maps with a common abstract ancillary input, the observed words certify their correspondence to the source only for acquired classical interfaces from the supplied process start. They imply neither physical-memory trace distance nor a guarantee for a physical external coherent reference, arbitrary new quantum inputs, or new coherent interventions.

## 3. Input and terminal-readout interfaces

The guaranteed physical initial interface is the fixed repeatable whole-process start, plus its legal classical continuations. Legal normalized core preparations and their known classical mixtures are included. An additional preparation setting requires its test vector `h_b` to be acquired and covered by the same rank promise. Its coordinates are `x_b=(HS)^(-1)h_b`; a repaired fitted vector has the analogous residual bound

    |x_b-xhat_b| <= M[D_b+D_V|xhat_b|+|Vhat xhat_b-hhat_b|].

Its density positivity and initialization error must then be charged. A catalogue of classical preparation labels does not define a CP input channel on an arbitrary physical datum or its reference.

A genuinely terminal test need not admit post-terminal interventions. Acquire its outcome-probability row `g_b` on the core preparations instead of a shifted `H_z`. Its exact virtual effect is

    B_b=sum_nu (g_b S)_nu F_nu     (orthonormal basis).

A fitted/repaired effect has radius `beta_b` at least the Euclidean norm of `D_gb |S|` plus its charged coordinate repair. Then `||B_b-Bhat_b||_infinity<=beta_b`. Require `Bhat_b>=beta_b I` and `sum_b Bhat_b=I` exactly. This certifies a true virtual POVM, with terminal measurement-channel half-diamond error at most `sum_b beta_b/2`. Add its worst selected-terminal error to (5) or (7). For the Pauli convention use dual basis `F_nu/2`, so the Frobenius radius is `||D_gb|S|||_2/sqrt(2)`.

The observable-rank/core promise must include **all these terminal effects**; a new terminal test can reveal previously invisible modes. Alternatively one may treat terminal tests as repeatable native CP instruments, if post-terminal tests are actually legal and their shifted counts/rank assumptions are paid. The separate root note `TERMINAL_TEST_PREDICTIVE_RECOVERY_TRANSFER.md` uses full transcript control to bound an ordinary terminal test risk and then averaged Bell recovery risk for a future independently held datum. This certificate can supply its hypothesis, but the current fixture does not acquire that additional recovery/test library.

## 4. Implementable acquisition, search cost, and sufficient regime

A finite candidate algorithm is: declare candidate preparations/tests; acquire ordinary joint-event counts with simultaneous intervals; select a nonsingular core; try a finite list of trace-compatible gauges; fit/repair Choi matrices under (2); evaluate (1)–(3); return an accepted model and error or `UNKNOWN`. At fixed gauge, fitting Choi matrices with exact branch-summed TP is a convex semidefinite problem. Searching the gauge is nonconvex and has no polynomial or dimension-free guarantee here. Every candidate, matrix inversion, repair, norm calculation and proof witness is part of computation.

A conventional HQMM learner can propose a gauge: compute its virtual states for the selected preparation words; if their coordinate matrix `P` is invertible, set `S=P^(-1)` and then validate solely against the acquired intervals. Candidate generation need not be statistically independent of counts, since the confidence event covers the original event probabilities uniformly. It remains a heuristic unless search termination is separately justified.

For a fixed nondegenerate core and a gauge with strictly positive initial density and Choi margins, a finite sufficiently accurate count table eventually certifies the model. With widths `eta`, the inverse-conditioning terms are `O(eta)` near that fixed instance. For target margin `m`, a sufficient per-setting Hoeffding count scales as `O(K_cond² m^(-2) log(K/beta))`; obtaining target additive clock error `b` additionally pays the sensitivity needed for `t_* <= b delta/gamma`. `K_cond` includes the actual matrix/basis/gauge norms, not a hidden universal constant. Enumerating a dense rational gauge family can establish eventual acceptance in an open rationally approximable regime, but its unbounded search cost is not an efficient discovery theorem.

The fitted instrument is an ordinary HQMM: propagate a `d×d` density matrix classically, or decompose its PSD Choi matrices into Kraus operators to implement an abstract quantum simulator. Neither method implements the unknown physical environment or supplies an actual recovery circuit.

## 5. Executed synthetic count-only separator

Files are in `cp_predictive_fixture/`: `generate_counts.py`, `counts.json`, `certify_counts.py`, `certificate.json`, and `replay.log`. The generator alone contains the plant; the learner imports only the integer count table, its experiment declarations, and standard arithmetic libraries. Sampling is by aggregate binomial/multinomial draws, not a claim that billions of laboratory interventions or individual simulation trajectories were executed.

The plant is a qubit with initial `I/2`, three reset channels to `(I+sigma_j/2)/2`, three binary test-and-reset instruments

    X -> Tr[((I +/- sigma_j/2)/2) X] I/2,

and a deterministic depolarizing rotation with Bloch multiplier `r=4/5`, rotating the x-y plane by `cos(theta)=3/5`, `sin(theta)=4/5`. Its eigenvalues are `1,4/5,(4/5)(3/5 +/- 4i/5)`. All branch Choi matrices are strictly positive: rotation minimum `1/10`, reset minima `1/4`, and test minima `1/8`. Preparations are empty/x/y/z reset, and tests are trace and the three positive test outcomes. The exact core determinant is `1/512`, so the process has observable rank four.

There are 12 base settings and 84 shifted settings, each representing `10^8` independent whole-reset episodes. The table therefore represents **9.6×10^9 starts and 2.52×10^10 native calls**. Base settings cost 21 calls per common shot count; shifted settings cost 231. The 156 nontrivial event probabilities use width `3/10000`; known deterministic trace probabilities have zero width. Hoeffding plus a union bound gives

    Pr(confidence failure) <=312 exp(-18) <4.752×10^-6.

Three predeclared virtual core Bloch radii `1/4,1/2,3/4` are checked; `1/2` is selected by the lowest certified local bound. At every candidate the initial virtual density is exactly `I/2`, and every fitted action's branch sum is TP exactly. Choi lower witnesses use numerical eigenvalues **only to propose rational numbers**, followed by exact rational principal-minor verification. Frobenius radii use integer-square-root upper bounds, not floating acceptance tests. The successful replay gives

    ||A||_infinity <0.015627,
    epsilon =59681/197200                ~0.302642,
    t_* =910133/20000000                  =0.04550665,
    b_add at delta=2/5 =2730399/40000000   =0.068259975,
    b_mix =179043/573443                  ~0.312225.

The additive contractive bound is stronger here. These large represented sample costs prove no practical sampling advantage.

The same count-only replay excludes any four-state classical HMM for the acquired process. Any nonnegative `4×4` matrix `Q` satisfies

    (Tr Q)^2 <=4 sum_i Q_ii² <=4 Tr(Q²).

For the exact rotation map, `Tr W=69/25`, `Tr(W²)=801/625`, giving a strict violation gap `1557/625`. A four-state realization of this rank-four process is minimal and therefore its deterministic rotation matrix must be similar to `W`. Similarity preserves the two traces, giving a contradiction.

The replay also verifies the exclusion directly from the count intervals, without importing that spectrum. If `|W-Wtilde|<=E`, then

    a=sum_i E_ii,
    b=2 sum_ij |Wtilde_ij| E_ji +sum_ij E_ij E_ji,
    Tr W >= Tr Wtilde-a,
    Tr(W²) <= Tr(Wtilde²)+b.

It verifies positive lower trace and a rational gap

    (Tr Wtilde-a)^2 -4[Tr(Wtilde²)+b] >2.08818.

Thus the accepted quantum cone is not merely a rephrasing of a four-vertex positive gauge. **No statement excludes a larger classical realization, establishes a general quantum advantage, or compares optimized learning costs.**

## 6. Conventional baselines and the unresolved boundary

Monras–Winter, *Quantum Learning of Classical Stochastic Processes: The Completely-Positive Realization Problem*, TQC 2014, Sections 3–6, already formulate quasi-realizations, equivalent CP realizations, semidefinite-representable cones and quotient operator systems. Their Section 5 explicitly distinguishes CP on a quotient from existence of a CP lift; Theorem 6 gives a stronger lifting-cone characterization. The present invertible `d²` construction sidesteps—not solves—that quotient-lifting problem. [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol027-tqc2014/LIPIcs.TQC.2014.99/LIPIcs.TQC.2014.99.pdf).

Srinivasan–Gordon–Boots, AISTATS 2018, Sections 3–4 and Algorithm 2, already parameterize HQMMs by Kraus instruments, compute word probabilities by unnormalized density updates, and learn parameters by iterative constrained likelihood optimization. Their models do not require recovering microscopic environmental variables. The fair comparison is a confidence wrapper around such a learner, not a claim that conventional methods demand physical tomography. [Primary paper](https://proceedings.mlr.press/v84/srinivasan18a/srinivasan18a.pdf).

Adhikary–Srinivasan–Gordon–Boots, AISTATS 2020, Definition 5 and Theorem 1, explicitly give Liouville HQMMs with PSD Choi matrices, TP normalization and PSD initial states, relating them to observable operator models. They also develop Stiefel-manifold learning. Consequently “Hermitian predictive gauge” and “CP rather than negative probabilities” are not new mechanisms. The bounded contribution here is the count/inverse/repair certificate, its explicit controller error accounting, and this narrowly separating replay; historical novelty is unestablished. [Primary paper](https://proceedings.mlr.press/v108/adhikary20a/adhikary20a.pdf).

The decisive unresolved issues are an acquired efficiently discoverable cone for **arbitrary observable quotients**, lower-rank/boundary processes, affordable well-conditioned experiment design, and any physical coherent input/output interface beyond declared task tests. The exact rank promise, whole-process resets, selected-model conditioning and policy-planning costs remain. Failure returns `UNKNOWN`, not nonexistence of a quantum model. These restrictions keep this a serious bounded alternative, rather than a purported solution of unknown quantum noise in general.
