# A constant-signal physical quadratic episode-length boundary

28 October 2026. **New candidate theorem; independent receiving pending.** Root proposed the forward-orbit/reset mechanism and the two-shift simplification below. Its harmonic/difference-set quantum mechanism has close prior art, explicitly credited in Section 7; **no novelty claim** is made. This is a concrete resource boundary for the declared interface, separate from the received rank/core-free short-word modulus theorem. It is not a total learning-resource or quantum-advantage claim.

The valid Jordan-state predecessor (SHA `3ab6c977f6361d1fe47f7443f8dd55959b0eabae1d9f76c446f3931bd2a5fa63`) remains in `PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH_jordan_state_version.md`. Its explicit-diagonal simplification is preserved in `PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH_explicit_diagonal_version.md`; both distinguish first at length r. The present two-shift version loses one delay step but has simpler physical states and a larger constant gap. The earlier tiny-signal construction is preserved separately; none of these historical files acquires a receipt automatically.

## 1. Main statement and sharp native interface

For every prime power q, put

    d=q+1,       r=q²+q+1=d²-d+1.                         (1)

There are two stationary dimension-d physical HQMMs, differing only in their initial densities, with two common native actions: (a) one **forward** unitary channel, or its specified weakly depolarizing version; (b) a fixed binary test followed by reset to one common state. All action/outcome words of total native length at most `r-2` agree exactly. Every classical feedback episode bounded by that length therefore has the same full record law. A specified word of length `r-1=d²-d` has binary-law TV at least

    3/32       with the unitary action,
    3/64       with the weakly depolarizing action.         (2)

The initial states are at least `I/(2d)`. Both test/reset branches have unnormalized Choi floor `1/(4d)`. In the depolarizing version, the forward channel has Choi floor `1/(2rd)`: **every native branch is strictly CP-interior**, with its dimension-dependent margin fully charged.

The library supplies no free inverse, arbitrary hidden-memory gate/readout, coherent control of the actions, or flag revealing the forward channel's mixture. Powers cost their actual number of native calls. A matrix description does not grant an inverse on inaccessible memory. An inverse would break this example in two calls; it is explicitly absent.

Any number of independently whole-process-reset acquisition episodes, each of length at most `r-2`, has an identical joint training-record law in both worlds, even when episodes are chosen adaptively. Thus some world has expected TV error at least `3/128` for prediction of the specified `(r-1)`-call binary law in the interior version (`3/64` in the unitary version). This is a lower bound on **maximum episode length**, not shots or computational complexity. It persists if the learner knows both candidate models and only needs to determine which initial world is present.

## 2. A standard, finite algebraic difference-set construction

Choose a Singer perfect cyclic difference set `D={e_0,...,e_(d-1)}` modulo r, so

    {e_i-e_j mod r : i!=j}={1,...,r-1}, once each.         (3)

For completeness, take `F_(q³)`, its subfield `F_q`, and a primitive multiplicative element g. The quotient `F_(q³)^*/F_q^*` is cyclic of order r. Let D contain the residues e such that

    Tr_(F_(q³)/F_q)(g^e)=0.                               (4)

The trace-zero hyperplane has `(q²-1)/(q-1)=q+1` projective points. For a nonidentity quotient element u, the functionals `Tr(x)` and `Tr(ux)` are independent: dependence would force u into `F_q` by nondegeneracy of the trace pairing. Their kernels intersect in one one-dimensional `F_q` subspace, hence one projective point, proving (3). The finite-field trace is a nonzero map for this separable extension; multiplication by a nonzero field element then proves nondegeneracy. This does not assume `Tr(1)!=0`, which would fail in characteristic three.

Irreducible-polynomial search, primitive-element verification and exact enumeration of (4) are finite, paid algebraic operations. This is the standard [Singer construction](https://doi.org/10.1090/S0002-9947-1938-1501951-4), also described in the directly consulted modern primary source [Herron, Section 1.4 and Proposition 2.1](https://arxiv.org/pdf/2502.09536); the original 1938 full text was not obtained here.

Set

    zeta=exp(2 pi i/r),     U=diag(zeta^e_i),
    |s>=(1,...,1)/sqrt(d),  tau=I/d.                      (5)

All entries are algebraic. By (3), for every integer t,

    |<s|U^t|s>|²
      =[d+sum_(ell=1)^(r-1) zeta^(ell t)]/d²
      =1                         if r divides t,
       (d-1)/d²                  otherwise.              (6)

The roots need not have prime order; the complete root sum proves this for composite r as well. This is the familiar harmonic equiangular-frame overlap identity, used here only in the explicit form (6).

## 3. Explicit full-rank states and interior test/reset

Define two states and one common binary effect:

    |psi_j>=U^j|s>,
    rho_j=tau/2+|psi_j><psi_j|/2,      j=1,2,
    E=I/2+|s><s|/4.                                      (7)

Both states have trace one and satisfy `rho_j>=I/(2d)`. E has eigenvalues `3/4,1/2,...,1/2`; its complement has eigenvalues `1/4,1/2,...,1/2`. There is no Jordan decomposition, spectral normalization or hidden preparation oracle in these algebraic descriptions. Their preparation/synthesis costs, if implemented, remain real resources.

The binary native action is

    b,1: Phi_(b,1)(X)=Tr(EX)tau,
    b,0: Phi_(b,0)(X)=Tr((I-E)X)tau.                      (8)

Its Choi matrices are `E^T tensor tau` and `(I-E)^T tensor tau`, each at least `I/(4d)`, and their sum is TP. After either outcome the normalized memory is exactly tau. A later test on tau has outcome-1 probability

    p_reset=Tr(E tau)=1/2+1/(4d),                         (9)

not one half. Both worlds have exactly the same complete physical instruments and differ only in rho_j.

## 4. Forward action and exact first-test laws

The unitary version uses the one-outcome action `a:X -> UXU†`. The interior version instead uses

    a: Psi_a(X)=alpha UXU†+beta Tr(X)tau,
    beta=1/(2r),       alpha=1-beta.                     (10)

No output flags the mixture component. Its unnormalized Choi matrix is

    alpha |U>><<U|+(beta/d)I_(d²),

so it is TP with floor `beta/d=1/(2rd)`. Both versions preserve tau. In formulas below take alpha=1 for the unitary version. After k forwards,

    Psi_a^k(rho_j)=tau+(alpha^k/2)
                         [U^(k+j)|s><s|U^(-(k+j))-tau]. (11)

Combining (6), (7) and (11) gives the exact rational first-test law

    p_j(k)=1/2+1/(4d)
             +alpha^k [r 1_{r divides(k+j)}-1]/(8d²).    (12)

For `0<=k<=r-3`, neither k+1 nor k+2 is a multiple of r, so the two laws agree. At `k=r-2`, the second state reaches the return peak and the first does not. Their probability difference is

    p_2(r-2)-p_1(r-2)=alpha^(r-2) r/(8d²).              (13)

Every exact early zero is preserved by weak depolarization; there is no nearly singular Vandermonde inversion or approximate cancellation assumption.

## 5. Full short records and adaptive acquisition

A word with no b has probability one. If its first b follows k forward calls, its first outcome law is (12). After that b, either outcome leaves tau in both worlds; every later forward preserves tau and every later test has the common law (9) and resets again. Thus matching the first test proves equality of the **whole word**, including multiple tests, not merely the final marginal.

Every word of length at most `r-2` first tests after at most `r-3` forwards, so all such words agree. The same argument covers bounded classical feedback and early stopping: before the first test all forward records are deterministic; at the first test both worlds have equal outcome probabilities; afterward both have the same memory. Private randomization cannot reveal the initial world.

For independently reset training episodes, condition on the complete earlier training record. The next selected short episode still has the same conditional law in both worlds. Induction gives identical full acquisition records for any finite number of whole-process starts and any adaptive choice of short episodes. The conclusion also holds for an almost-surely finite stopping rule, by cylinder-event equality. Postselecting a short classical record does not help because its joint event probabilities agree; all restart attempts remain paid. Native b is only the common-tau reset (8); the separately supplied whole-process start restores the world's rho_j.

This argument is about the declared classical interface. It does not assert physical-memory trace-norm equality, coherent-reference equivalence, or equality under extra terminal measurements.

## 6. Constant gap, prediction consequence, dimension and clock

The word `a^(r-2)b` has length `r-1`. Its binary-law TV is exactly

    v_d=r/(8d²)                                  (unitary),
    v_d=[r/(8d²)](1-1/(2r))^(r-2)                 (interior). (14)

Since `r/d²>=3/4` and Bernoulli's inequality gives `(1-1/(2r))^(r-2)>1/2`, these are at least `3/32` and `3/64`. The latter is a dimension-uniform constant signal despite every native Choi being full rank. The forward Choi floor shrinks as `Theta(d^-3)`; no dimension-independent mixing margin is granted.

An estimator receiving identical training-record distributions has the same output distribution in the two worlds. Pointwise triangle inequality, then expectation, shows the sum of its two expected TV errors for this target is at least v_d; at least one is at least `v_d/2`. A common deterministic guaranteed-error output cannot have error below `v_d/2` in both worlds. This is not a lower bound against a learner allowed occasional longer episodes, richer access, or a different prediction target.

With a fixed pre-call abort clock of survival gamma, the specified word survives with probability `gamma^(r-1)`. All earlier abort records agree, so its full clocked-record TV is exactly `gamma^(r-1)v_d`. A fixed positive abort probability therefore does **not** inherit a dimension-uniform constant-risk lower bound. Abort probability of order `1/r` retains constant survival but pays expected duration of order r.

For any supplied dimension upper bound `D_max>=3`, choose the largest power of two `q<=D_max-1`. Then actual dimension `d=q+1<=D_max`, `q>(D_max-1)/2`, and first distinguishing length `r-1=q²+q=Omega(D_max²)`. The source already lies in the promised class; no padding or extra state is assumed. Thus the worst-case episode-length order is quadratic for all large supplied dimension bounds, not only isolated exact dimensions.

## 7. Close prior art, scope and verification

The quantum harmonic mechanism is established prior art, not a new invention by terminology. [Mereghetti–Palano (2002), Section 2 and Theorem 2.3](https://doi.org/10.1051/ita:2002014) directly constructs periodic quantum-automaton events using Fourier coefficients, difference covers, phase differences and positive-operator decompositions; its `O(sqrt(period))` state bound was verified in the [public primary full text](https://cdn.sciengine.com/doi/pdfView/72767B2A6A314F249B84DADD1A3E1A4B). [Bertoni–Mereghetti–Palano (2003), *Golomb rulers and difference sets for succinct quantum automata*](https://doi.org/10.1142/S0129054103002060) is an even closer Singer/difference-set antecedent: its primary abstract explicitly discusses periodic quantum events and the projective construction for `n=q²+q+1`. Its full paper has not been read here, so no finer distinction or priority claim is inferred from the abstract. The present proof specializes familiar harmonic structure to an explicit two-world, full-rank, constant-signal forward/test-reset acquisition boundary and spells out the adaptive-record and clock interfaces.

The `O(d²)` exact short-word upper is conventional quantum-automata linear algebra. [Li–Qiu, Theorem 5](https://arxiv.org/pdf/quant-ph/0604085) gives `n_1²+n_2²-1` for quantum sequential machines. The separately received short-word modulus theorem adds a paid semialgebraic stability procedure; the present example explains why its quadratic experiment-length order cannot in general be replaced by a dimension-independent or linear bound in this declared interface. This is an order comparison, not a matching constant or sample/computation optimality claim.

`physical_quadratic_length_exact_check.py/.json` verifies finite fields, ordered differences, exact cyclotomic overlap identities, rational first-test laws and margins, full short words and selected feedback records. Numerical matrix replays are supplementary, not exact PSD certificates. There are zero source calls, episode samples, RNG calls or hardware executions. Independent receipt is pending; no earlier module's receipt is inherited.
