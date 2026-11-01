# Independent audit: coherent-noise Lyapunov memory criterion

2026-11-01. This is a mathematical audit of the abstract criterion, not an audit or construction of an actual code/controller family. No prior-art novelty, hardware locality, practical threshold, or implementation claim is certified.

## Status and frozen versions

The original supplied ROOT_CONSTRUCTION.md SHA256 6b93ba1dd6aa72a64af2c20709d10c0dc9e783ddecb6cc5e8ed45aada0fa69fe has a FALSE one-step-shell dissipator comparison. I supplied an exact counterexample immediately. The root preserved that version as ROOT_V1_BOUNDARY_SHELL_UNCORRECTED.md and revised the draft. I then read and SHA-verified corrected ROOT_CONSTRUCTION.md SHA256 7119e5b7f4a7571cdfb8b2d2ea6a42cb0a24235df5499cb966f422a721dca8c7.

The corrected two-step-shell comparison is valid, with explicit constants derived below. Subject to the precise diagonal-projector/subsystem hypotheses below, the abstract conditional exponentially long decoded-memory conclusion is sound. The existence of a code family earning those hypotheses remains wholly unreceived here.

## Exact counterexample to the original one-step shell

Take two syndrome qubits, W=Hamming weight, cutoff B=2, Q=span{00,01,10}, admitted moves X1,X2 and b=1. Let J=X1+X2 and rho=|00><00|. Then

    D[J](rho)-D[QJQ](rho)=-|11><00|-|00><11|,

whose trace norm is 2, while the one-step exit shell W>=B-b has population zero. The cross term is from J†J=2I+2X1X2. This also defeats a same-shell small-time Duhamel argument, not merely a loose pointwise constant. A spectator protected logical system can be tensored on without changing the example. The exact rational script two_step_counterexample.py verifies the matrix identity. The counterexample does NOT refute the repaired exponential conclusion: replacing b by 2b in the shell changes only a fixed prefactor.

## Precise hypotheses needed for the subsystem/local-controller formulation

1. The finite-system potential W is diagonal in a specified commuting syndrome/configuration algebra. It is nonnegative, and the initial encoded subspace has W=0 and lies in Q. Every admitted Pauli component changes W by at most the same n-independent b. Q is the below-cutoff reachable component projector and commutes with W.
2. The flatness condition concerns the SAME admitted alphabet and an explicitly specified protected subsystem. Canonical path recoveries must make every compressed admitted Pauli QPQ equal to identity on that protected subsystem tensor an operator on syndrome/gauge. Closed paths may act on gauge, not on protected information. This is stronger than a bare code-distance statement unless the low-potential path premise is independently earned.
3. Each ideal cooling jump is a SINGLE fixed Pauli times a local diagonal pattern projector, sqrt(r_j) P_j Pi_j. Pi_j must commute with W and Q and be logical-trivial in the decoded factorization. For example it may be a function of the joint commuting syndrome/register observables. Including all its Pauli components in the admitted alphabet can establish the logical condition. A full-system syndrome projector is NOT local merely because its scalar rate is computed locally; the root correctly removed that original notation.
4. The total enabled rate must obey an OPERATOR inequality on Q, sum_j r_j Pi_j >= c kappa W, or the equivalent pointwise inequality in the entire common configuration basis, including every allowed gauge/register configuration. An average over classical gauge configurations would not establish a statement for coherent gauge states. Each enabled pattern must lower W by at least d0 on every configuration in its support.
5. The actual system-bath evolution must exist as a CPTP propagator. Bounded measurable time-dependent interactions suffice in an appropriate bath interaction picture; no smoothness or bandwidth bound is needed. Only bath-only Hamiltonians are free to be removed. A logical system Hamiltonian that happens to commute with W is not an uncharged bath term.

These are clarifications of what the abstract proof uses, not earned properties of the proposed witness-register instance. In particular register errors and all local Pauli components must be included in b, the alphabet, the rate premise, and the holonomy premise.

## Weighted algebra checked

For a Pauli P permuting syndrome sectors, weighted conjugation has norm <=exp(ab/2), while

    ||F^-1/2 [F,P] F^-1/2|| <=2sinh(ab/2).

The coefficients are differences of exp(plus/minus a Delta W/2), so these bounds hold even with syndrome-dependent Pauli phases. Tensoring arbitrary bounded bath operators multiplies the norm by their operator norm. Summing a self-adjoint interaction V gives the stated u_H=2h sinh(ab/2).

For a general jump J, define A=F^1/2 JF^-1/2 and B=F^-1/2[F,J]F^-1/2. Direct expansion yields

    F^-1/2 D[J]^*(F) F^-1/2=(A†B+B†A)/2.

With l1(J)=sum_P |j_P|, ||A||<=exp(ab/2)l1(J) and ||B||<=2sinh(ab/2)l1(J). Their product is (exp(ab)-1)l1(J)^2, exactly the claimed u_D coefficient. This does not require J to be Hermitian or Pauli. The scalar-coefficient jump model in the draft is sufficient; operator-valued bath jump coefficients would require their own explicitly stated norm-sum contract.

Compression of the full dissipator is NOT the proof of its reflected bound. Rather, since [Q,F]=0, weighted A and B for the compressed jump are QAQ and QBQ on Q, so their norms cannot increase. The same direct argument applies to compressed Hamiltonians.

## Reflected drift and protected subsystem

For an ideal jump P_j Pi_j, L_j†L_j=r_j Pi_j is diagonal, and the downward support condition gives its contribution <=-r_j(1-exp(-ad0))Pi_j F. Summing the operator rate premise proves the negative drift. In particular, ideal jumps restricted to Q have exactly the same generator action on Q-supported states as the original jumps: outputs remain in Q and the diagonal anticommutator does not introduce an off-block cross term. Merely knowing that a GENERAL jump maps Q into Q would not by itself imply this equality.

Splitting at W=theta n proves the draft's drift inequality with g=c kappa theta(1-exp(-ad0)). Adding the weighted perturbation inequality and assuming u<g gives

    tr(F rho_ref(t)) <= C_a exp(a theta n),
    C_a=1+g/(g-u),

uniformly in time for an initially W=0 state. This constant is conservative but valid. For r=1,2 the shell projection P_r=Q 1_{W>=B_n-rb} therefore satisfies

    p_r(t)<=C_a exp[-a((beta-theta)n-rb)].

Under the flatness and diagonal-projector hypotheses every reflected system term is identity on the protected logical subsystem tensor a syndrome/gauge/bath operator. Hence the reflected propagator preserves the reduced protected-logical/reference state exactly, including coherent and entangled gauge states. No Gibbs distribution or stationarity argument is needed.

## Correct two-step dissipator comparison

Let R=I-Q, rho=QrhoQ a density operator (including any reference and bath), and P2=Q 1_{W>=B_n-2b}. For a perturbing jump J put

    L=QJQ, E=RJQ, Z=(J†J-L†L)Q.

Any one- or two-Pauli path starting below B_n-2b stays in the below-cutoff component. Therefore E=EP2 and Z=ZP2. This statement includes the Pauli products in J†J without requiring those products to be directly executable moves. Norms satisfy ||E||<=||J||, ||L||<=||J||, and ||Z||<=2||J||^2.

For any operator X=XP2, the trace-Hilbert-Schmidt inequality gives

    ||X rho||_1 <=||X|| sqrt(tr(P2 rho)).

Now write the difference of jump-output terms as

    J rho J†-L rho L†=E rho J†+L rho E†.

Its trace norm is <=2||J||^2 sqrt(p2). The anticommutator difference is -(Zrho+rho Z†)/2 and contributes at most 2||J||^2 sqrt(p2). Thus

    ||(D[J]-D[QJQ])(rho)||_1 <=4||J||^2 sqrt(p2).

This holds with arbitrary bath/reference tensor factors for the stated jump model. Since ||J||<=l1(J), summing gives 4 gamma n sqrt(p2). The Hamiltonian difference on a Q-supported state has only off-block terms and contributes <=2 h n sqrt(p1)<=2 h n sqrt(p2).

## Duhamel, output error, and lifetime

Extend the reflected generator to the full system by its Q-compressed Hamiltonians/jumps, retaining the bath-only generator. Its evolution from a Q-supported input stays in Q. Actual and extended reflected propagators are CPTP. Variation of constants and trace-norm contraction on Hermitian differences give

    ||rho_actual(T)-rho_ref(T)||_1
      <= n(2h+4gamma) integral_0^T sqrt(p2(t)) dt
      <= n(2h+4gamma) T sqrt(C_a)
                       exp[-a((beta-theta)n-2b)/2].

Ideal cooling contributes zero to this generator difference, by the single-conditional-Pauli argument above. The bound is dimension-independent and remains valid after adjoining arbitrary reference systems.

Choose a terminal decoding channel equal to canonical protected-subsystem decoding on Q, with any CPTP extension outside Q. Trace-norm contraction and exact reflected logical preservation give the same bound on decoded protected-logical/reference error; it may of course be capped at 2. For a fixed bath state independent of logical input, this is the usual restricted-code diamond/output-channel bound. For initially correlated logical/bath states it is still a uniform pointwise joint-state/output guarantee, but one should not pretend correlated initialization automatically defines a system-only channel.

For fixed a, beta-theta>0, u<g and fixed target error, the bound permits T proportional to exp[a(beta-theta)n/2]/n, with fixed coefficient exp(-ab)/[(2h+4gamma)sqrt(C_a)]. This is a CONDITIONAL information-theoretic memory criterion. The terminal decoder may be nonlocal and computationally expensive unless separately constructed.

## Scope of acceptance

The current additive Hamiltonian-plus-Lindblad noise model is covered. Arbitrary coherent miscalibration of controller jumps is NOT automatically an independent positive noise dissipator: its cross terms require a separately proved weighted-drift and boundary budget, as the author notes. Likewise no actual Tanner/witness code family, extensive move count, flat low-potential basin, efficient decoder, Euclidean locality, or microscopic noise implementation is certified here.

The original boundary claim was broken and is preserved. The repaired abstract boundary-to-logical argument has no remaining algebraic obstruction found under the precise hypotheses listed above. This receipt should travel with those hypotheses, not be cited as an unconditional quantum-memory construction.
