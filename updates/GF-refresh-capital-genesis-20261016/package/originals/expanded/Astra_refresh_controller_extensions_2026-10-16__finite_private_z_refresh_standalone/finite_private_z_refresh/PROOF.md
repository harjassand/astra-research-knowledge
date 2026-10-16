# Finite-width private random-Z refresh with a charged concurrent interaction

Date: 2026-10-16. Conditional mathematical controller theorem. The delivered ideal and partial-node packets remain unchanged. No physical device, controller isolation, measured rate, or accessibility of a virtual parity operator is assumed established.

## 1. Actual finite-window contract

There are finitely many commuting parity involutions Z_i and a finite persistent bath/reference B. The initial state lies in a specified joint parity sector. The non-controller Hamiltonian is

    H_base(t) = H0(t) + sum_i V_i(t),

where H0 preserves all parities, V_i is odd only in parity i and preserves the others, and ||V_i(t)||<=j_i(t). Envelopes are deterministic and integrable. The coefficients and operators in H_base are fixed independently of all private controller choices. They may have arbitrary time-dependent couplings to bath operators; evolution remains linear with fixed operator coefficients independent of private seeds. They do not directly read private controller registers or inaccessible environments.

Coordinate i has one fixed window [l_i,r_i]. Its TRUSTED local controller privately samples lambda_i with a specified distribution, independently across i and independently of the initial bath/signs, and adds

    H_ctrl,i(t,lambda_i) = u_i(t,lambda_i) Z_i/2,

supported inside that window. The real waveform is integrable, with

    phi_i(lambda_i) = integral_(l_i)^(r_i) u_i(t,lambda_i) dt,
    eta_i = | E exp(-i phi_i) |.

For a direct finite-dimensional formulation take a finite distribution of lambda. General classical distributions are obtained by the corresponding channel/integral limit when the stated propagators and approximations exist. The actual private controller register and any discarded controller environment NEVER become accessible to H_base or subsequent controls. The only controller action on the retained system is the displayed Z_i term. Classical leakage, unintended bath-dependent phase terms, and controller-correlated errors are not covered.

The unknown V_i remains active during the finite window; it is not set to zero in the actual process. Define its before/window/after action budgets

    a_i = integral_0^(l_i) j_i(t) dt,
    c_i = integral_(l_i)^(r_i) j_i(t) dt,
    b_i = integral_(r_i)^T j_i(t) dt.

Windows may overlap and have different boundaries. The endpoint event is that every selected parity flipped. All probabilities average the actual private phase samples. There is no actual instantaneous partial-dephasing channel assumed inside a window.

## 2. Result

Let F(a,b,eta) denote the exact two-gap partial-node value from the preceding packet. Explicitly put p=sin²(min(a,pi/2)), q=sin²(min(b,pi/2)), Q=p+q-pq and

    F(a,b,eta) = Q + max_(0<=x<=1)
        [-pq x² + 2 eta sqrt(pq(1-p)(1-q)) x].

Define the finite-window certificate

    R_i = sin²(min(arcsin(sqrt(F(a_i,b_i,eta_i))) + c_i, pi/2)).

Then the actual endpoint all-flipped effect satisfies

    P_initial E_all-flipped P_initial
       <= (product_i R_i) P_initial.

The bound charges all concurrent own-coordinate interaction during each finite controller window. It is uniform over the allowed shared bath and reference. The product is not replaced by a global additive error depending on the sum of all window costs.

This R bound is a certificate, not a claim of exact finite-window optimality. At c_i=0 it reduces to the sharp partial-node product. The state-angle estimate by itself need not be jointly attainable with a specified controller waveform.

## 3. One-coordinate comparison, with privacy kept explicit

Fix any single-coordinate control strategy, including arbitrary bath memory and parity-preserving instruments. Purify all such instruments to fixed isometries, and purify the controller's classical mixture by a private register L. Its branchwise phase waveform is implemented by a controlled unitary on L and the private parity.

Construct a REFERENCE process by deleting only this coordinate's parity-odd interaction during its controller window. Outside the window the strategy and all prescribed operations are identical. During the reference window every other operation preserves Z, and every such operation acts as identity on L. Hence it commutes with the controlled random-Z evolution, not merely with its average.

The whole controlled phase can therefore be moved to the end of the reference window. The remaining window operations are parity-preserving, lambda-independent maps. Averaging the inaccessible controller register at that location gives the exact joint channel

    rho_01 -> (E exp(-i phi)) rho_01,
    rho_00 -> rho_00,  rho_11 -> rho_11

on the parity blocks, with identity action on the persistent bath. Its complex phase is a known deterministic parity-diagonal rotation. Composing or absorbing that rotation changes no odd-action budget, so the singleton upper bound depends only on eta=|E exp(-i phi)|.

The reference thus has the actual partial-dephasing node contract, actions a,b, and any additional parity-preserving maps before/after that node. Its endpoint-flip probability is at most F(a,b,eta).

This rearrangement remains valid for arbitrary causal prover strategies. A strategy can respond to quantum messages and its own measurement results, but after purification it is one fixed sequence of isometries independent of the unknown L. In the reference, where own odd rotations are absent during the window, that sequence remains parity preserving and commutes with L-controlled Z phases. We do NOT replace a strategy by one that is freely told lambda, and we do not condition a normalized state on favorable controller outcomes.

## 4. State-angle cost of the removed interaction

For normalized pure states write their projective angle as

    d(psi,chi)=arccos |<psi,chi>|,  0<=d<=pi/2.

During the window, actual and reference dilations differ only by the removed odd interaction. In a relative interaction picture its Hermitian generator has norm at most j(t). The projective speed of a normalized state generated by G is the standard deviation of G, bounded by ||G||. Integrating gives

    d(psi_actual,psi_reference) <= min(c,pi/2).

Equivalently, for a finite circuit, deleting a rotation of angle theta changes projective state angle by at most theta; the triangle inequality sums these changes, while common intervening isometries preserve overlaps. This also covers instrument dilations and arbitrary fixed adaptive strategies. Subsequent common isometries outside the window preserve the bound. Purification includes the inaccessible controller, so the comparison is unconditional over all phase samples.

For an orthogonal endpoint accept projector P, the distance from a state psi to the rejecting subspace is

    distance(psi,range(I-P)) = arcsin sqrt(<psi,P psi>).

The triangle inequality for distance to a subspace therefore gives

    arcsin sqrt(p_actual) <= arcsin sqrt(p_reference) + c,

whenever the right-hand side is below pi/2; otherwise use p_actual<=1. Combining p_reference<=F yields exactly R.

Zero/full probabilities and a saturated angle are handled by continuity and the trivial cap at one. No small-action expansion is used.

## 5. Why the finite-window certificates tensor

Use the independent private-parity testers of the ideal packet. Tester i now retains its own private phase register and applies its actual controlled Z waveform during its actual finite window. Between its budgeted X rotations, a fresh copied-parity message goes to the joint prover and is uncomputed on return. All prover-induced maps preserve the private parity, and every desired joint parity-diagonal bath unitary is implemented losslessly. The controller register is never among the messages.

All tester initial states, private random samples, waveforms and endpoint measurements are independent local factors. Their windows need not coincide. Section 3–4 bounds every single-tester strategy by R_i even if it uses arbitrary private memory and causal response.

Gutoski–Watrous positive strategy domination therefore gives

    T_i <= R_i S_i,

where T_i is the positive accept operator and S_i is normalized causal. Tensoring preserves the causal trace constraints and positivity. Pairing with any compatible joint prover bounds its all-pass probability by product_i R_i. The all-pass tensor theorem is established prior mathematics; the finite-controller embedding and local comparison specify why it applies to this contract.

Primary source: Gutoski and Watrous, *Toward a General Theory of Quantum Games* (2007), Theorem 9, printed p.13, https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf . The preceding ideal packet spells out the trace constraints and exact-budget Hamiltonian simulation.

### The simulation must not reveal the random phase

Remove only H0 in the interaction picture, NOT the private controller Hamiltonian. Since H0 is independent of all controller samples and preserves every parity, the transformed V_i remain sample-independent and the controller terms keep their local Z_i form. Pad sector dimensions if needed. Decompose each own-odd contraction into the mean of parity-diagonal conjugates of X_i as before. The associated prover controls depend on H0,V_i and the deterministic partition, never on lambda.

Keep the sampled controller phase evolution entirely inside the local testers. Refine a time partition containing every window boundary and Trotter the bounded interactions with the controller's integrable phase evolution. For finite phase support the partition can resolve all waveforms simultaneously. Each approximation has exactly the original before/window/after own-X actions. Convergence follows from the finite-action Dyson estimates on each branch; averaging finitely many branches preserves it. The operator-effect bound follows by convergence for arbitrary initial bath/reference vectors.

It would be invalid to remove the random controller first and then quietly give its phase-dependent conjugated V_i to an informed prover. The construction above avoids that change of information.

## 6. A finite amplitude/width specification, not measured hardware data

As an illustrative contract let the controller choose balanced phases phi=+theta or -theta, with 0<=theta<=pi/2, using a square pulse in a fixed window of width tau. Then

    H_ctrl = +/- theta Z/(2 tau),
    eta = cos(theta).

If the available controller Hamiltonian norm is at most Omega_max, the pulse specification requires

    tau >= theta/(2 Omega_max).

Here Omega_max is an angular-frequency Hamiltonian norm (with hbar=1), not a wall-energy or wall-power budget. In particular full isolated dephasing is obtained at theta=pi/2, with the amplitude constraint tau>=pi/(4 Omega_max).

If the concurrent own interaction envelope is bounded by J throughout the selected window, then c<=J tau and the certified bound is

    R <= sin²(min(arcsin sqrt(F(a,b,cos(theta))) + J tau, pi/2)).

Choosing the shortest square pulse allowed by this ideal amplitude constraint gives the conservative charged angle J theta/(2 Omega_max). The lower bound on tau does NOT imply a lower bound on the actual interaction error or action: J is an upper envelope, and the actual interaction may be smaller or vanish. For a specified probability target epsilon>=F, a sufficient envelope requirement is

    J tau <= arcsin sqrt(epsilon) - arcsin sqrt(F).

These are conditional design inequalities. No Omega_max, J, isolation performance, locality cost, or acceptable target is asserted for a real device. The required evidence would include the actual full-joint coupling, interaction envelope, pulse bandwidth/amplitude constraints, private-randomness isolation, and crosstalk behavior. The operator Z must itself be an available physical coupling if this is used as a hardware proposal; a virtual-seed parity label alone does not establish that accessibility.

## 7. Exact failure modes and scope

- If H0 or V is explicitly allowed to read lambda, the reference reduction can fail even at c=0. An unbounded parity-preserving baseline can apply the inverse private phase. The effective node is then no dephasing, rather than D_eta. For example, choose balanced phases +/-pi/2, c=0, a=b=pi/6, and the forbidden sample-dependent baseline H0=-H_ctrl in the window. The actual qubit endpoint probability is sin²(pi/3)=3/4, while the claimed private-refresh reference would give Q=7/16. This is an exact obstruction to dropping the independence condition.
- A controller environment that later reinteracts can enable a quantum eraser. An isolated reduced coherence multiplier does not establish the full process contract.
- Correlated phase registers across coordinates generally destroy independent tester factorization; retain a conditional joint bound or prove an appropriate correlation estimate instead.
- Generic finite-width noisy measurement hardware, arbitrary diamond-close channels, bath-dependent controller errors, or a presumed local Lindblad generator are not covered by this random-Z theorem.
- The actual odd interaction is permitted throughout the finite window, but its full norm action is charged. An unbounded or unmeasured interaction cannot be ignored because the isolated controller would dephase.
- Schedules, envelopes and controller distributions are fixed/exogenous and private as specified. No state-selected or adversary-selected refresh schedule is assumed covered.
- The previously delivered ideal and partial-node results remain unchanged. This finite-window certificate is not asserted to be sharp and does not establish experimental feasibility.
