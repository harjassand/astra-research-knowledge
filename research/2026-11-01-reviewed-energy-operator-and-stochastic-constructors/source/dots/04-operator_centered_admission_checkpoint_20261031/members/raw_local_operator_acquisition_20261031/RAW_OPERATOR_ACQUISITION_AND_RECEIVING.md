# Exact acquisition of local product-weight drift certificates

31 October 2026. Candidate implementation and receiving proof; independent review pending. This is a finite, known-model certificate finder/checker, not hardware calibration, a generic guard constructor, an optimal stability solver, or a new threshold theorem. It leaves all earlier frozen sources unchanged.

## 1. Input and actual executable output

`acquire_operator_certificate.py` accepts exact finite local matrices, in a declared tensor-product cell basis. Each complex entry is a pair of canonical rational pairs. The input includes:

- finite cell dimensions;
- the actual Hermitian source coefficient of each declared single-cell source times nonidentity system-Pauli coupling term, with its complete Pauli support;
- each local source Hamiltonian and a list of nonnegative rational rates multiplying dissipators of supplied local jump matrices;
- a requested positive physical gap kappa and a nonnegative physical activation cap a;
- an external task identifier and consumer-contract SHA, explicit local-size limits and LP search budgets.

A jump is represented by rate r and matrix L, meaning r D[L]; no square-root rate is approximated. The implementation supports cell dimension at most8, term support at most3, and local matrix dimension at most64, with tighter limits requested in each fixture. These are actual implementation caps, not physical necessities. It constructs no matrix of the total tensor-product source Hilbert space.

`acquire(spec)` returns CERTIFIED or UNKNOWN for valid inputs; malformed inputs raise InputError. UNKNOWN includes no common transparent sector, infeasibility in the restricted sufficient cone, a search-size/time limit, or an optimizer proposal failing exact checking. UNKNOWN is NOT instability or impossibility.

`verify_certificate(external_spec,record)` verifies successful supplied certificates independently of the LP solution. It reconstructs the source charges and every local matrix polynomial, checks their positivity and the global margins. It accepts valid PSD allocations even outside the finder's diagonally-dominant search cone. The caller must supply the actual external input; a certificate's own embedded task/hash does not establish what task was intended. The verifier does not verify UNKNOWN records as admission certificates. Exact recursive type comparison prevents bool/float aliases from passing as integers.

The executable output is a DRIFT certificate, not final circuit admission. In particular it does not inspect a complete gate/idle schedule, construct a fault-tolerant gadget, verify a consumer contract from its SHA, or execute a logical gate. Section5 specifies the additional receiving interface. Keeping these claims separate prevents a successful matrix proof from being mislabeled a complete physical machine.

## 2. Acquiring the transparent charge

For each cell i, stack the declared Hermitian coupling matrices B_(i,alpha), compute their exact rational complex nullspace, and let X_i contain a basis. Set

  P_i = X_i (X_i^dagger X_i)^(-1) X_i^dagger,  Q_i=I-P_i.

An empty coefficient list gives P_i=I. A zero-dimensional common kernel is reported UNKNOWN by this frontend; it is not a claim that no other encoding or analysis works. The code explicitly checks projector, Hermiticity and annihilation identities. Exact rational coefficients imply rational complex projectors, even though an orthonormal basis might require square roots.

Every declared B obeys B P_i=P_i B=0, hence B=Q_i B Q_i. This is a sufficient termwise transparent sector of the supplied expansion. Redundant Pauli terms that could cancel are not automatically combined; that can make the frontend conservative, never more permissive. There is no claim that the returned sector is the largest one obtainable by changing the physical decomposition, subtracting an unpriced mean or choosing a new encoding.

A conservative acquired norm for each Hermitian B is its maximum row sum of |Re B_ij|+|Im B_ij|. This is at least its spectral norm. The output records these rational bounds; it does not assume an optimal norm oracle. Any future grouping into a location uses sums of the relevant bounds.

The model is finite-operator only. No shared spectator is silently omitted from a supplied matrix. The separately reviewed spectator corollary requires explicit bounded spectator expansions or independently acquired uniform operator bounds. This program does not acquire unknown spectator norms or certify an experimental structural promise.

## 3. Local polynomial certificates and the global drift

For a local source term G_e on a support e, let

  V_e(u)=tensor_(i in e)(I+u_i Q_i),   0<=u_i<=1.

Compute its adjoint DIRECTLY from the supplied matrices:

  G_e^dagger(V)=i[H_e,V]+sum_j r_j[L_j^dagger V L_j
                                 -(L_j^dagger L_j V+V L_j^dagger L_j)/2].

No source-creating term is discarded. Seek a local real matrix M^e with nonnegative off-diagonal entries and local nonnegative activation coefficients a_i^e such that

  F_e(u)=sum_i (M^e u)_i Q_i tensor_(j!=i)(I+u_jQ_j)
          +sum_i a_i^e u_i V_e(u)-G_e^dagger(V_e(u)) >=0.             (1)

The diagonal of M^e can have either sign. Degrees are at most2 in each u_i. The code expands F_e in the tensor degree2 Bernstein basis

  B_k(u)=product_i binom(2,k_i)u_i^k_i(1-u_i)^(2-k_i), k_i=0,1,2.

For power coefficients p_alpha, the Bernstein matrix at k is

  C_k=sum_(alpha<=k) product_i [binom(k_i,alpha_i)/binom(2,alpha_i)] p_alpha.

This is an exact basis conversion. Every B_k is nonnegative on the cube. Therefore checking C_k>=0 for ALL 3^|e| matrices proves (1). Positivity only at cube vertices would not suffice; a test includes a degree2 polynomial positive at endpoints but negative inside.

The independent verifier uses exact Hermitian Schur complements. A negative diagonal fails. A zero diagonal with a nonzero row fails, by the corresponding2x2 principal minor. Zero rows are removed. A positive pivot reduces PSD to the PSD of its rational Schur complement. This handles singular matrices without an eigenvalue-gap or floating tolerance assumption.

Embed and sum M^e into a global M, and sum a_i^e at each cell. Verify all off-diagonal entries of M are nonnegative, every ROW AND COLUMN sum is at most -kappa, and each total activation is at most a. Multiplying each local inequality by the positive commuting outside weight and summing proves

  G^dagger(V_u) <= sum_i (M u)_i Q_i product_(j!=i)(I+u_jQ_j)
                    +sum_i a_i u_i V_u.                           (2)

Overlapping local generator supports are allowed. Their effects are summed, not factored into independent trajectories. All outside interactions remain present. A row-sum check alone would not provide the selected-volume estimate used below.

## 4. Actual finder, search price and incompleteness

The finder restricts each Hermitian C_k to a diagonally-dominant sufficient cone:

  (C_k)_ii >= sum_(j!=i)(|Re(C_k)_ij|+|Im(C_k)_ij|).

Two inequalities per absolute-value slack make this linear in M^e,a^e. Gershgorin, or the direct quadratic-form bound, proves PSD. The ordinary exact SymPy simplex solver minimizes the sum of activation allocations subject to these local inequalities and requested global margins. This objective does NOT maximize the certified gap or optimize the final physical admission parameter. The code is not a new LP/SDP method.

The requested activation cap is indispensable: an alleged negative drift can be compensated by an enormous activation allocation, which is not free cooling. In the trivial one-cell G=0,Q nonzero case, the small-u Q block forces a>=kappa. The code rejects a fake-loss attempt when the requested cap is below the gap. Source-creating drives can be accepted only with the activation they actually require in the checked inequality.

Search has explicit maximum LP variables, constraints and wall-clock seconds. Size refusal and timer expiry yield UNKNOWN. The timer is enforced on the main thread using the ordinary process timer; if a timer is already active or unavailable, the finder refuses rather than silently dropping the budget. These are LP-search bounds, NOT a claim that all preprocessing, rational bit growth or input I/O fits that wall-clock budget. Building the charges and coefficient matrices is paid separately. The executable has structural local matrix/support caps; large explicit graphs still incur their full inspection and LP costs.

SymPy's exact simplex is an ordinary component, not asserted to have polynomial worst-case execution time. Verification uses a finite number of exact local matrix operations and global row/column sums; bit sizes of the supplied proof and intermediate rationals are part of that cost. With maximum local dimension d_e and support s_e, there are sum_e 3^s_e PSD checks of dimension d_e, plus exact nullspace/Gram computations. For fixed local sizes this avoids exponential dependence on TOTAL device Hilbert dimension, but not explicit input size or difficult certificate search.

The installed/tested library is SymPy1.14.0. Its primary simplex documentation is https://docs.sympy.org/latest/modules/solvers/solvers.html#module-sympy.solvers.simplex . Bernstein positivity, common-kernel linear algebra, Gershgorin cones, rational Schur complements and Lyapunov inequalities are standard methods. A stronger ordinary SDP or SOS finder may succeed where this cone returns UNKNOWN; the exact checker can receive PSD allocations without claiming the finder is complete.

## 5. Receiving into the established all-selected amplitude bound

This paragraph proves the general finite-charge receiving step; it does not claim the executable has inspected its circuit premises. Supply an actual finite location/idle schedule, at most g active cells per location, duration at most tau, with each cell assigned to at most one simultaneous location. The actual unwanted local terms obey

  K_(l,i)=Q_i K_(l,i) Q_i,  ||K_(l,i)||<=c,

on that cell and the declared system patch. Source-independent actual gate residual has integrated norm at most epsilon_ctl per location. Intended system-only operations and their actual implementation costs are supplied. The full source generator is the declared local GKSL sum, with its initialized Markov fields; finite source/system/reference inputs may be arbitrary and correlated.

For selected locations complexify their unwanted terms by |z_l|<=R in ONE common jump-history dilation. Since every K_(l,i) commutes with V_u, its complex norm potential is at most2Rc Q_iV_u. Put v_i=2Rc on selected active incidences. In backward physical time solve

  dot u=M u+v(1+u), u(0)=0.

Metzler positivity and the row bound give, at a first boundary u_i=1,

  dot u_i <= -kappa+4Rc <= -kappa/2

provided R<=kappa/(8c). Thus0<=u<=1. The column bound gives ||exp(Mt)||_1<=exp(-kappa t), and u<=2 exp(M dot)*v. For k selected locations,

  sum_i u_i(initial)<=4Rc gk/kappa,
  integral sum_i u_i(t)dt<=4Rc gk tau/kappa.

Insert this backward weight into (2). The derivative terms cancel, leaving activation and actual control residuals. Hence the common initialized-field dilation obeys

  ||W(z)||^2 <= exp{[4Rc g(1+a tau)/kappa+2R epsilon_ctl]k}.

The already established multivariate Cauchy extraction yields

  ||E(S)|| <= [ exp{R[2cg(1+a tau)/kappa+epsilon_ctl]}/(R-1) ]^|S|,
  1<R<=kappa/(8c).                                               (3)

If no such R exists, this sufficient receiving route does not admit the chosen operating point. A positive drift certificate alone is NOT a small-error certificate. The optimized physical-unit corollary applies with gamma lambda replaced by kappa. The c=0 case is treated directly rather than by dividing by c.

The interface is the existing inclusive amplitude premise, not marginal fault probabilities, an automatic Pauli channel or a newly selected threshold. Actual codes, preparation/readout/reset, finite controls, support/fanout and consumer-gadget assumptions remain required. The program's contract SHA binds a declared consumer identifier, not a proof of that consumer.

## 6. Actual recovered and failed fixtures

The saved exact fixtures are generated by `test_operator_certificate.py`.

1. **Mixed transparent qutrit:** B=diag(0,0,1); losses |0><2| and |1><2|, injection rate1/100 through |2><0|; internal H=10^20(|0><1|+|1><0|). The program discovers P=diag(1,1,0), finds M=-1 and a=1/100 at requested kappa1. Removing H produces IDENTICAL allocations: its harmless bandwidth cancels in the actual generator polynomial, not through an assumed norm exemption. No pure preparation inside P is needed by the mathematical receiver.
2. **Known qubit model:** two raw qubits, each loss rate4 and injection1/100, hopping amplitude1/4. It recovers a valid global gap1, with hopping allocation M_edge having all four entries1/4 and zero activation. This matches the ordinary transport bound; loss allocations are conservative because the objective is activation, not maximum gap.
3. **Coherent source creation:** a raw X Hamiltonian plus loss10, coupling B=n. With activation cap1/10 the sufficient finder returns UNKNOWN. With cap2 it finds a certificate charging activation1. That certificate does not itself guarantee a useful R or small amplitude.
4. **Fake loss/bypass:** zero source generator cannot meet the requested gap1 at cap1/10. Adding a full-rank identity coupling destroys the common transparent sector and returns UNKNOWN. A non-diagonal coupling with a genuine kernel and rational rotated loss is successfully recognized without a supplied projector.

Tests include singular PSD matrices, interior-negative Bernstein polynomials, malformed/non-Hermitian matrices, negative rates, undeclared spectator fields, external model/task mutation, strict certificate-type mutation and finite LP-size refusal. Saved runtimes are local diagnostics, not asymptotic guarantees or hardware speed claims. The exact certificate identities, not floating simulations, carry acceptance.

## 7. Consequence and boundary

The acquired operation is now concrete: supplied finite local operators -> discovered transparent charges -> checked local matrix-polynomial drift -> a dimension-independent high-order receiver CONDITIONAL on an actual complete circuit schedule. It no longer assumes a good charge or transport graph merely because a scalar model labels them so.

It remains a sound-incomplete known-model analysis built from ordinary optimization tools. It does not learn local operators from experiments, exclude undeclared nonlocal terms, supply arbitrary spectator bounds, construct a physical guard from generic full-rank noise, or compete with actual leakage-reduction hardware without paying its control costs. A small source-creating residual must be included in the generator/activation certificate, not relabeled a commuting implementation error. Strong ordinary matrix-Lyapunov/SOS and fault-tolerance tools receive exactly the same input data; no superiority or novelty is inferred from this implementation.

## 8. Separate executable complete-schedule receiver

`receive_operator_schedule.py` now implements the additional finite schedule join, separately from the drift finder. Its external input includes the RAW model, a successfully checked drift certificate, and a complete schedule with system-qubit count, duration, intended gates/idles, actual control residual budgets and consumer amplitude budget. The raw and schedule task identifiers/contracts must agree.

It recomputes the assembled M and activation totals, derives their actual minimum negative row/column sum kappa and maximum activation a, and checks the raw certificate first. It maps each actual matrix-times-Pauli coupling to its acquired positive matrix norm bound, retaining the same source-cell index and full system-Pauli support. Triangle inequality makes this a valid per-location bound even when the actual matrices are noncommuting or have different signs.

For schedule checking and rational contour arithmetic ONLY, it then constructs a scalar BOOKKEEPING envelope with loss kappa, no transport, injection a and those norm coefficients. This is not a simulation, replacement channel, or claim that a qutrit source physically equals independent qubit loss. Section5 proves that exactly these scalar parameters receive the actual general-charge inequality. The frozen `acquire_local_admission.py` component, SHA256 `a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8`, is hash-checked before reuse.

That component verifies all system gate/idle coverage, patch supports, guard-to-location incidence and nonoverlap, intended constant-Pauli/idle operations and actual residual bounds. It computes c,g,tau,epsilon_ctl and uses the already proved rational exponential uppers9/7 or17/8. The wrapper outputs a full externally bound PASS or NOT_ADMITTED. Its `verify_certificate` checks a truthful record of either status; `verify_admitted` additionally requires PASS. The CLI verify mode requires actual admission. It labels source dimensions explicitly and does not relabel qutrits as physical qubits.

The saved complete fixture has a raw qutrit rank-2 transparent sector, two loss terms each rate10^8, injection1/100 and ground-sector Hamiltonian10^20. Its supplied actual one-qubit X gate has duration1 and unwanted Q tensor Z, with a declared zero implementation residual. The computed conservative drift gap is10^8 and the complete amplitude upper is303/2916666431, about1.04e-7, below the separately requested1e-6 budget. These are MODEL inputs, not measured or demonstrated hardware resources. The external evidence identifier for the zero residual is not experimentally checked. Tests reject missing idles, changed tasks/models, source fanout across simultaneous patches, unsupported reset targets and forged drift certificates; large declared control error produces NOT_ADMITTED.

The wrapper pays exact raw verification and complete explicit schedule inspection. Its reused scalar graph is only an O(number of cells) parameter envelope; actual raw matrix acquisition/search remains charged. This closes a known-model acquisition-to-scheduled-admission interface, not physical synthesis or an unprovided threshold consumer.

## 9. Review-discovered complex-arithmetic correction

The initial working implementation c49faf3743da82019e762c21a562956ed2830ddce9dfa2f6f3750796e2d60147 is preserved as `acquire_operator_certificate_pre_complex_normalization.py`. Independent review found that SymPy could leave exact complex-rational Schur complements and projector products unsimplified. Some valid complex Gram inputs then caused a TypeError/AssertionError or false rejection, rather than the advertised complete rational matrix check. This was not an unsound accepted certificate.

The current implementation canonicalizes real and imaginary rational parts of computed projectors, projector/annihilation products, PSD inputs and EVERY Schur-complement step. It also canonicalizes encoded matrix output. The reviewer's exact3x3 rank-one complex Gram common-kernel example and30 positive plus30 negative complex Gram cases are included in the author regression suite. The old bytes are not described as passing the repaired tests. No claim is made that generic symbolic algebra is a free positivity oracle; the corrected checker acts on exact rational-complex matrices.
