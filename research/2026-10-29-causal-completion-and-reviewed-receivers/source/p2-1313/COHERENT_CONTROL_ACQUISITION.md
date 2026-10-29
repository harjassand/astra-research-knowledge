# Coherent acquisition of periodic control: an explicit bridge and its fault boundary

Author: architecture challenge branch, 29 October 2026. This is new work; no predecessor is edited or re-reviewed. The root's native-control and causal-boundary constructions are separate subjects and are not independently validated here.

## 1. Scientific disposition

A coherent spin and conditional displacements can approximate a nonlinear periodic phase with its complete workspace returned approximately clean. Section 4 gives a fully specified, conservative finite circuit, uniform over the oscillator spectrum and all external references. It is an existence construction, not a competitive precision compiler: QSP is the stronger conventional compilation machinery when its signal access and synthesized phase list are supplied.

The decisive limitation is different. Exact cleanup of a bare controller does not certify fault containment. Section 2 constructs a finite-duration, bounded, coherent ancilla–memory coupling whose effect becomes a logical–memory interaction even after perfect cleanup. Angle slicing, fresh ancillas, and exact final reset do not suppress this channel at fixed total exposure. Conversely, native periodic control also has a direct logical fault channel when its coefficient fluctuates. Neither architecture acquires reliable control merely by removing measurements.

Section 3 supplies a useful exact boundary: a finite sequence of same-quadrature conditional-displacement queries and finite-dimensional ancillary rotations cannot implement a non-affine scalar phase while returning its workspace exactly to a fixed state on an open position interval. Approximation, noncommuting quadratures, additional physical nonlinearities, and different output interfaces remain available. This is a finite exponential-polynomial argument, not a no-go for approximate GKP computation or for general coherent control.

Conventions: [q,p]=i; Pauli eigenvalues are +/-1; exp(-i theta Z) has rotation angle 2 theta. An error bound on an initialized-input isometry is a complete vector/operator bound, stable under arbitrary independent reference. The corresponding channel half-diamond distance is at most that bound. No small bound here is a device error probability.

## 2. A controller can return clean while exporting a coherent logical fault

### 2.1 Give the conventional implementation its best possible copy interface

Let L be a logical qubit, a a controller qubit prepared in |0>, and M arbitrary retained quantum memory. Grant an exact parity-copy gate

    E = CNOT_(L -> a),       E Z_a E = Z_L Z_a.              (1)

The intended logical phase is implemented by E, a finite-duration Z_a rotation, and E again. This grant removes all source-code and imperfect-copy issues from the challenge. It therefore strengthens the comparator rather than attributing source imperfections to it.

During the rotation let

    H(t) = u(t) Z_a + lambda(t) Z_a tensor B_M,             (2)

where B=B^dagger is bounded, its free Hamiltonian is zero, and the scalar waveforms are integrable. This is already an admitted finite returning-memory example. Set theta=integral u and kappa=integral lambda. Commutativity makes the exact complete output on the initialized controller

    E U(T) E (|psi>_(LMR) tensor |0>_a)
       = [exp(-i theta Z_L) exp(-i kappa Z_L B_M)
                                      |psi>_(LMR)] tensor |0>_a.       (3)

R is an arbitrary logical/memory reference. Equation (3) is an operator identity on the whole initialized input. The workspace is exactly clean; no measurement or reset of it diagnoses the logical fault.

For m pieces, using a fresh |0> controller in every piece and the same retained B,

    product_j exp[-i theta_j Z_L] exp[-i kappa_j Z_L B]
       = exp[-i (sum theta_j) Z_L] exp[-i (sum kappa_j) Z_L B].        (4)

Relative coherent coefficient noise lambda(t)=eta u(t) gives kappa=eta theta independently of m. A fixed bounded noise amplitude during a fixed total central-rotation duration similarly has no 1/m improvement. At a maximum coefficient |u|<=u_max, that total duration is at least |theta|/u_max. Repeated copy/uncompute windows add exposure; they are not supplied at zero duration.

This is an existence counterexample for arbitrary coherent returning-memory noise. It does not assert that every controller error channel behaves this way or invalidate a biased stochastic model.

Composite control tailored to additional stationarity/symmetry assumptions, an acquired biased ancilla, or a fault-tolerantly encoded controller can change the answer. Those are distinct mechanisms with their own controlled couplings, preparation and reuse bills. The example is not a lower bound over all such implementations. It rules out inferring general fault suppression merely from same-axis angle subdivision and clean final workspace.

### 2.2 Complete-output witness

Take B=Z_M, memory |+>, and a maximally entangled logical/reference state |Phi>_(LR). Remove the intended logical rotation. The output is

    |Psi> = cos(kappa) |Phi>|+>
              - i sin(kappa) |Phi_Z>|->,                 (5)

where |Phi_Z>=(Z_L tensor I_R)|Phi> is orthogonal to |Phi>. For any logical-identity reference isometry acting only on memory and additional apparatus, its output has form |Phi>|omega>. Its overlap with (5) is at most |cos(kappa)|. Thus the best pure complete-output trace distance is at least |sin(kappa)| and the best phase-adjusted vector distance at least sqrt[2-2|cos(kappa)|]. These lower bounds are attained by retaining the unperturbed |+> memory in the reference when cos(kappa)>=0.

For an arbitrary mixed comparison state with logical/reference marginal |Phi><Phi|, the projector onto its orthogonal logical/reference sector gives the safe lower bound sin(kappa)^2. Do not replace that mixed-state bound with the pure-isometry metric without its premise.

After tracing M, this particular physical example is the logical dephasing channel with probability sin(kappa)^2. The complete output instead retains coherent logical–memory entanglement. These are different error descriptions.

### 2.3 Native controls retain the corresponding actuator channel

If a supplied bounded periodic operator F(q) equals Z_L tensor I_gauge on the protected band, then an actual coefficient error

    delta H(t)=lambda(t) F(q) tensor B_M                  (6)

has exactly the same logical action there. It is not a polynomial gauge error merely because F is smooth and bounded. A native-controller proposal must pay its integrated coefficient-error budget or protect that channel by another mechanism. Increasing the order of correction for polynomial source noise does not correct (6).

### 2.4 Scope of the strong conventional source

Singh, Royer and Girvin, *Phys. Rev. X* 16, 041018 (2026), DOI [10.1103/7jwl-k8xg](https://journals.aps.org/prx/pdf/10.1103/7jwl-k8xg), Sec. V D.2, derives angle slicing for a biased dominant-X ancilla and a binomial/random-walk model. That setting differs from (2). The paper explicitly omits reset errors in those simulations; Sec. V E.2 keeps the discrete-variable two-qubit gate as an additional error source. The source is a strong approximate-control alternative, not evidence for suppression of every coherent ancilla–memory interaction. Read scope and normalization conventions are recorded separately.

## 3. Exact clean-workspace boundary for a finite same-quadrature compiler

### Theorem 1

Let W(q) be a finite circuit on a finite-dimensional ancillary workspace. It is built from constant ancillary unitaries and queries whose matrix entries are finite sums of exp(i omega q), with real frequencies omega. Ordinary exp(i k q sigma_n) conditional displacements satisfy this premise; frequencies need not be commensurate. There is no q derivative or p query in this theorem.

For fixed normalized states |a_in>, |a_out>, define the actual initialized response globally by P(x)=<a_out|W(x)|a_in> for every real x. Suppose those states satisfy

    W(x)|a_in> = P(x)|a_out>                              (7)

for every x in a nonempty open real interval. Then (7) holds for every real x, and this actual response satisfies

    P(x)=exp(i phi) exp(i omega_0 x).                     (8)

Thus exact clean scalar nonlinear phase is unavailable from this finite same-quadrature query family, even when cleanliness was demanded only on an open guard interval.

This conclusion fixes the actual response, equivalently its unique exponential-polynomial continuation. It does not extend equality with an arbitrary prescribed target function beyond the intervals on which that equality was required. The different-band obstruction below requires the stated target on each of those bands.

### Proof

Every matrix entry of W is a finite exponential polynomial. Choose a constant output basis with |a_out> as its first vector. Each other component of W(x)|a_in> vanishes on an open interval. Its entire extension in complex x therefore vanishes identically. Unitarity for real x gives |P(x)|=1 everywhere.

Collect equal frequencies and write P(x)=sum_(j=1)^s c_j exp(i omega_j x), with distinct increasing omega_j and nonzero c_j. If s>1, the coefficient at the largest positive frequency omega_s-omega_1 in |P(x)|^2 is uniquely c_s conjugate(c_1), which is nonzero. Linear independence of distinct real exponential frequencies contradicts the constant value one. Hence s=1 and |c_1|=1. This proves (8).

For commensurate frequencies this is the familiar finite Laurent-polynomial argument. The proof above also covers arbitrary finite real query strengths. A constant final unitary absorbs a different fixed output workspace state.

### Reach and escape routes

A desired scalar phase exp[i theta f(q)] that is exactly one constant on one open protected band and a different constant on another cannot satisfy (8). An exact globally clean finite query implementation of that target therefore needs a different resource or output contract. The statement is about a scalar physical phase port, not every possible logical gate with a changed gauge state.

The theorem permits approximate clean workspace, bounded-error QSP, p/q interleavings, target-specific state optimization, measurement with retained failure records, an infinite-dimensional mediator, and a genuine nonlinear Hamiltonian. It also permits ordinary displacement phases and Pauli actions with a gauge change. It does not infer a lower bound on the number of queries for approximation. The finite-harmonic Hamiltonian exp[i theta sum_j a_j cos(k_j q)] is generally an infinite Fourier series after exponentiation; its provision is a different control resource from finitely many conditional-displacement queries.

QSP is the strong approximate escape. The polynomial/signal-processing machinery is already used and reviewed in the earlier coarse-readout package; no new phase-finding algorithm or optimized phase list is claimed here. Approximate signal synthesis still requires actual controlled queries, stable phases, duration and a controller-noise budget.

## 4. A complete finite cosine compiler from those same conventional ports

This section supplies an explicit conservative construction instead of assuming that a desired Fourier Hamiltonian is already an actuator. It is not claimed to be a new dispersive mechanism or an efficient substitute for QSP.

### 4.1 Bounded two-level model, with no source cutoff

Let a have Z|g>=-|g>, let Delta>0 and g>0, and set

    D_k = exp(i k q Z_a/2),
    H_k = (Delta/2) Z_a + g X_a + g D_k X_a D_k^dagger.    (9)

Every term in H_k is bounded on the full oscillator–ancilla space. In the position fiber x=kq its off-diagonal element is v(x)=g(1+exp(ix)), so

    |v(x)|^2 = 2g^2(1+cos x),
    E(x)=sqrt(Delta^2/4+|v(x)|^2).                        (10)

For the initialized ancilla, exact two-by-two exponentiation gives

    ||exp[-i H_k(x)T]|g> - exp[iE(x)T]|g>||^2
      = 2[1-Delta/(2E(x))] sin^2[E(x)T]
      <= 4|v(x)|^2/Delta^2.                              (11)

The elementary square-root remainder gives

    0 <= Delta/2+|v|^2/Delta-E <= |v|^4/Delta^3.           (12)

Choose a target theta>=0 and T=theta Delta/(2g^2). With r=g/Delta, equations (10)–(12) imply the uniform initialized-input operator bound

    || exp(-i H_k T) J_g
       - exp[i(Delta T/2+theta)]
                    J_g exp[i theta cos(kq)] ||
          <= 4r + 8 theta r^2 =: epsilon_disp.            (13)

J_g appends |g>. This retains the entire output ancilla; no population error has been promoted to an amplitude bound. Direct-integral uniformity makes (13) valid for all oscillator inputs, including arbitrary logical/reference entanglement, without a Fock or energy cutoff. Negative theta is obtained by reversing the complete bounded Hamiltonian, a separate acquired sign-control permission.

The initialized spin is a supplied pure port independent of the other inputs; an approximate preparation error must include its correlations with retained apparatus. The displayed global phase is known. If the whole operation is coherently selected by another register, that phase becomes relative and needs its corresponding calibrated selector phase correction.

For example, r <= min(epsilon/8, sqrt[epsilon/(16 theta)]) assigns epsilon/2 to each term in (13). At fixed available g the simulated interaction time is

    T=theta/(2gr).                                       (14)

Large detuning suppresses the initialized-spin error while lengthening this time. This tradeoff is not a claim about the optimal physical implementation.

### 4.2 Compile H_k using finite conditional-displacement queries

Write A=(Delta/2)Z, B=gX, C=gD_k X D_k^dagger. For h=T/M, use the finite Lie product

    U_M = [exp(-iAh) exp(-iBh)
                    D_k exp(-ighX) D_k^dagger]^M.        (15)

All factors are actual supplied port operations. The three commutator norms are

    ||[A,B]||=Delta g,
    ||[A,C]||=Delta g,
    ||[B,C]||<=2g^2.                                    (16)

The bounded-unitary product-formula integral and a telescoping sum give

    ||U_M-exp[-i(A+B+C)T]||
             <= T^2(Delta g+g^2)/M =: epsilon_PF.        (17)

Consequently (13) plus (17) is a fully explicit finite cosine phase gate with an approximately clean ancilla. Formula (15) has 2M conditional-displacement queries, M Z rotations and 2M X rotations before possible adjacent-factor cancellation. It uses one initialized qubit and no measurement, acceptance test, or discarded ancilla output.

This elementary compiler has a poor sufficient precision cost. Equation (17) is a method cost, not a query-complexity or device lower bound. QSP/Hamiltonian simulation and experimentally optimized hybrid controls are the stronger alternatives when available. The purpose of (15) is to make one acquisition route concrete and to prevent an ideal cosine interaction from being smuggled in as a free waveform.

### 4.3 Mixed harmonics and two-mode entangling targets

Replace kq by k_1 q_1+k_2 q_2. The same proof and bounds hold because the two position operators commute. The query factors exactly as

    D_(k1,k2)=exp(i k_1 q_1 Z/2) exp(i k_2 q_2 Z/2).      (18)

Thus the circuit supplies exp[i theta cos(k_1 q_1+k_2 q_2)] with the same initialized-spin approximation bound and twice as many conditional-displacement queries if the two interactions are sequential. A finite sum of q-only mixed harmonics can be implemented by concatenating these circuits because the target scalar phases commute. Their approximation bounds add on the complete initialized-input interface; each actual residual workspace must either be retained with a joint bound or be reset with its preparation/noise/retirement cost.

A single such Fourier phase is not automatically a protected logical ZZ gate. The root's independently authored band/finite-harmonic argument specifies when a sum of harmonics supplies that logical action. The present result acquires the scalar port only. In particular, it does not prove that errors during (15) inherit the simultaneous native Hamiltonian's error transparency.

### 4.4 Physical time and complete error ledger

The parameter T in (15) is simulated evolution time. It must not replace wall-clock time. Suppose available qubit Hamiltonian coefficients are bounded by Omega_z and Omega_x for Z and X, and |v_q| bounds the coefficient of qZ during a signal query. A serial implementation requires at least

    tau >= Delta T/(2 Omega_z) + 2gT/Omega_x
                                  + M |k|/v_q.          (19)

For a mixed query the last term becomes M(|k_1|/v_1+|k_2|/v_2). Switching, routing, free-motion compensation, pulse filtering and occupied-mode holding add their actual times. If these port operations are only available in an interaction picture, known drift over every interval and the physical residual in that frame must be included. A static laboratory spatial cosine is not thereby a stationary rotating-frame quadrature cosine.

For the ideal q-only circuit, every prefix commutes with q. On a qualified input isometry Q with ||qQ||<=F_q, a coefficient error delta d in a query exp(i d q Z) has complete vector error at most |delta d| F_q. Query calibration therefore contributes F_q sum_j |delta d_j| on ideal prefixes. A constant spin rotation angle error contributes at most its absolute angle error. The matching multi-mode bound uses sum_l |delta d_l| F_(q_l). Compact modular support alone is not a uniform bound on F_q.

For bounded arbitrary returning ancilla-memory interaction V_(aM)(t), after removing the common memory-only propagator, ordinary Duhamel gives the additional complete error bound

    epsilon_aM <= integral_0^tau ||V_(aM)(t)|| dt.        (20)

No independence, bath reset, or measurement assumption is needed for this bound. It can be unsuppressible as in (2)–(5); repeated small rotations do not improve (20) by themselves. Source terms with unbounded q/p are not covered by (20). They require an actual qualified-prefix/domain estimate for the full physical pulse schedule, or a separate acquired error bound. Known endpoint equality does not supply that estimate.

A sufficient complete gate error ledger is

    epsilon_gate <= epsilon_prep + epsilon_disp
          + epsilon_PF + epsilon_cal + epsilon_aM
          + epsilon_source/holding + epsilon_other_ports.            (21)

Only disjoint physical contributions are added. All final ancilla and returning-memory ports are retained. There is no postselection normalization. Exact input supply, pulse inversion, control delivery, spatial/period calibration, actual source holding and any later reuse/reset are substantive assumptions. No finite threshold or total workload advantage follows from (21).

## 5. Governing experimental comparator and what is not established

Matsos et al., [arXiv:2409.05455v1](https://arxiv.org/html/2409.05455v1), is a strong concrete hybrid-control comparator. It supplies phase-modulated spin-dependent forces, optimized finite-energy one- and two-qubit gates, and direct Bell-state preparation. Its SI2 uses a 50-level mode truncation and a third-order Lamb–Dicke/RWA model; the target cost averages six or 36 Pauli inputs. The main text specifies spin measurements after preparation and gate application, proceeding on spin-down. Those operations and that retained/accepted instrument must be included in a matched comparison. The Nature Physics publication exists at DOI [10.1038/s41567-025-03002-8](https://www.nature.com/articles/s41567-025-03002-8), but its final PDF was inaccessible here; the detailed scope statements in this paragraph are explicitly about the read preprint version.

These implementations show why direct hybrid compilation is a serious alternative to an invented ideal nonlinear port. They do not establish the root's complete-memory, within-pulse polynomial-error hypothesis for that port. Conversely, neither Theorem 1 nor the coherent-fault example refutes their actual targeted finite-energy or biased-noise results.

For a genuine improvement, a native periodic-control architecture must acquire the nonlinear operation with a smaller complete control/holding cost, or supply a protection mechanism for its own logical coefficient errors. The current exact causal/noise principle may still be foundational without that acquisition: it identifies a different allowed noise algebra and comparison interface. This branch does not turn that conditional principle into a hardware advantage.

## 6. Authored evidence and provenance

`native_control_checks.py` contains exact rational finite-matrix checks of the clean-controller fault export and finite Laurent response identities, followed by explicitly labeled floating-point two-level diagnostics for (11)–(17). The latter check selected parameter fibers; they are not interval enclosures or continuum proofs. Equations (11)–(17) have the analytic uniform proof above and do not depend on a bosonic truncation.

`SOURCE_READ_SCOPE.json` records the exact primary passages, source-version gap, dependency use and exclusions. `AUTHOR_RECEIPT.json` pins the resulting files. This is an author package, not its own independent review. Root's central native-control proof and the prior accepted QSP/SSS machinery remain separate authored/reviewed results.
