# Acquired direction-merged Gibbs source → native retained compiler

31 October2026. A concrete receiving corollary, not a new mixing theorem or quantization mechanism. This uses the direction-merged quantum generator itself, NOT the threshold-map channel and NOT a collision approximation.

## 1. Frozen premises

The local-energy source is ../local_gibbs_lift_20261031/DIRECTION_MERGED_LOCAL_ENERGY_CERTIFICATE.md, SHA8292664fbc215b131e006c9e931d41a658050b4fbfdf0bd375b378c64a87af2b, with DIRECTION_MERGED_ENERGY_INDEPENDENT_REVIEW.md SHAfa2f78f5dc2a18b44b50a370b890fe7e78b9e73c77679daab214fffcf5a19067.

The complete native receiver is NATIVE_FULL_FIRST_EVENT_RECEIVING.md, SHA f503c80089c85006856e6ca1ea8b536bb36e0aa4931db071320a33a056a07192, received by NATIVE_FULL_INDEPENDENT_REVIEW.md SHA0fa56f50ca5160cbbbe9dc51c360f2b34b9e9e301894dc49c9ce6288d8cafeed. Its ordinary LCHS kernel, complete first-event normalization, finite bridge/clock budgets, arbitrary-input count, and low-rate fallback remain binding. This corollary supplies actual source operations and parameter values, not another proof by assertion that a local Hamiltonian is easy.

## 2. Exact source family and certificates

Take an open chain of n binary spins s_i∈{+1,-1}, zero fields, and |J_i|<=1/40. Let

    pi(s)=Z^-1 exp(sum_(i=1)^(n-1) J_i s_i s_(i+1)),
    r_i(s)=pi(s^i)/(pi(s)+pi(s^i)).

At a fixed neighbor context z write r0=r_i(0,z), r1=r_i(1,z), so r0+r1=1. Define

    v_i(z)=(sqrt(r0),-sqrt(r1)), Pi_i=|v_i><v_i|,
    L_i,0=|1_i><v_i|, L_i,1=-|0_i><v_i|,
    H=sum_i Pi_i, G=sum_(i,a) D[L_i,a].

Controls on the at most two neighbors are implicit. All jumps annihilate psi=sum_s sqrt(pi(s))|s>, and sum L†L=2H. The received local-energy proof supplies

    (19/20)Q <= H <= nQ,
    G†H <= -(19/39)H,
    Q=I-|psi><psi|.

These constants are certified analytic bounds, not inferred from a finite spectral check. They hold for this native direction-merged generator. The threshold lift is different quantum dynamics even though it has the same classical diagonal restriction.

An especially clean exact-rational raw interface is an edge ratio q_i in [20/21,21/20], with weight q_i for equal neighboring bits and weight1 for unequal bits. Then J_i=(1/2)log q_i and |J_i|<1/40 since log(21/20)<1/20. This admits exact rational local ratios and all conditional probabilities without computing logarithms to certify the model. It is a sufficient subclass, not all of |J_i|<=1/40. Alternatively exact rational J_i with the stated bound receives ordinary certified exponential/logistic arithmetic. The former matches the exact-Fraction acquisition prototype's onsite(1,1), edge[[q_i,1],[1,q_i]] input format.

## 3. The actual source operations

For each fixed local context, a controlled one-qubit rotation prepares v_i(z) from |0>. Its adjoint maps v_i to |0>. Compose with the normalization-one block of |1><0| (or -|0><0|) to obtain the two stated L_i,a blocks. The rank-one block is an explicit constant-size unitary dilation with a failure flag; no normalized projection or unknown-state postselection is used. All context conditions act on at most three spins. Local rates are computed from at most two edge ratios; in the rational interface their exact bit lengths are polynomial in the supplied edge bit lengths. Rotations are synthesized to the allocated absolute tolerance. Zero/one probability branches, if supplied in a wider interface, must be handled explicitly; the present finite positive weak ratios avoid them.

Prepare a uniform color register over the 2n site/direction pairs and SELECT the corresponding local jump block. Keep the color as an OUTPUT register rather than unpreparing it. The successful rectangular block is

    (1/sqrt(2n)) sum_(i,a) |i,a> L_i,a.

Thus alpha_L=sqrt(2n) is an actually acquired stack normalization. Its controlled inverse is the reversal of this circuit, not an assumed inverse channel. A simple O(n) scan/routing implementation is sufficient; no free QRAM or unit-cost global select is assumed. Uniform non-power-of-two state preparation uses finite prefix probabilities and paid rotations. The nominal algebraic normalization may be approximated with certified arithmetic; a dyadic upper normalization can alternatively be used, with the corresponding h enlarged as required by the receiver.

Composing the stack with its adjoint acquires H=L†L/2 with alpha_H=n. The physical upper energy bound is h=n. Separate direct LCU over the n local projectors gives the same normalization. All source encodings therefore have polynomial n gate cost and logarithmic requested-precision overhead, rather than enumerating 2^n configurations.

There is a particularly simple exact reference preparation for this open zero-field chain:

    Pr(s_1=+)=Pr(s_1=-)=1/2,
    Pr(s_(i+1)=s_i | s_i)=q_i/(1+q_i).

The product of these transition probabilities is exactly pi, since the partition function is 2 product_i(1+q_i) in the rational-weight convention. Start with a fair superposition on the first spin and perform successive neighbor-controlled rotations with these conditional probabilities. This constructs the positive state psi, not a Gibbs sampler approximation. O(n) such rotations suffice; allocating operator error epsilon_prep/O(n) makes the preparation-unitary error at most epsilon_prep by telescoping. Reversal implements its inverse. Hence reflection about psi is acquired by preparation, reflection about |0^n>, and unpreparation. This costs polynomial n and log(1/epsilon_prep), with actual coefficient bit lengths paid.

For nonzero fields or periodic boundary conditions, one instead needs the already supplied transfer-message construction and its real arithmetic costs; they are not silently covered by this particularly simple sequential formula. This corollary's displayed implementation is the open zero-field chain.

## 4. A noncommuting system coupling with exact acquired centering

Let H0 act only on the retained system. Supply Hermitian system block encodings A_i with normalizations alpha_i, and define

    K=sum_i A_i tensor Z_i,    b=sum_i alpha_i.

A finite LCU over i acquires K/b, with all coefficient-state and system SELECT costs paid. No commutativity among the A_i or with H0 is required. Global spin flip preserves pi and changes every Z_i sign. Therefore <psi|Z_i|psi>=0 EXACTLY and

    P K P=0.

There is no omitted sqrt(lambda) mean Hamiltonian. This is structural centering of this specified coupling, not a claim that arbitrary observable means are free. General mean block compression is ordinary and accessible from psi and K, but any nontrivial resulting system action must be retained and paid.

The finite-bit source/coupling circuits approximate these exact nominal centered operators. Their small synthesis errors are allocated by the native receiver; exact nominal centering is not inferred from rounded gate matrices.

## 5. Received joint process and resource substitution

For any prescribed time T, rate lambda, target trace error epsilon, arbitrary joint source/system/reference input and p prescribed common joint CPTP instruments, apply the native receiver to

    lambda G - i[H0+sqrt(lambda)K,.].

The source parameters are

    g=19/20, kappa=19/39, h=alpha_H=n,
    alpha_L=sqrt(2n), b=sum_i alpha_i.

After the receiver's scale change they remain polynomial in n; B=b²T/g and mu=lambda*g*T. The resulting total overhead is polynomial in n,1+alpha_0T+b²T+p, input bit lengths, log(2+lambda*T), and log(1/epsilon), multiplied by the actual controlled system-operator and source-circuit costs. The exact polynomial, including conservative n-dependent Lyapunov count and stack normalization, is inherited from the whole receiver. It is NOT a practical gate estimate, an optimized n-scaling, or a new log(n) state-preparation claim.

The source is never reset at virtual interval boundaries. Its actual post-jump source state is retained, and arbitrary prescribed source operations are allowed for the QUANTUM task. The theorem does not expose the compiler's jump/time/color record or permit consumer interventions at those private times. The pure reference is used for reflections and certificates; the input source need not be psi.

## 6. Separate classical-noise interpretation

The adjoint of G preserves the source-diagonal system-operator algebra and restricts there to continuous-time heat-bath Glauber dynamics. The coupling sum A_i tensor Z_i and system Hamiltonian preserve that algebra too. Thus for an initially CQ source/system state, prescribed instruments whose ADJOINTS preserve this algebra, and a final dephasing/readout of the source label, the output is the exact classical-source-driven quantum process up to the simulator error. This includes appropriate label measurements and feedback with their full outcomes retained. It does not require the A_i to commute.

Do not identify the raw coherent source density with a classical probability distribution. Arbitrary joint quantum-source interventions remain valid for the quantum compiler, but generally cease to represent classical noise. For this classical comparison the physical source generator is exactly lambda times native heat-bath Q_classical, not a Poissonized block or a changed clock.

## 7. Scope and ordinary alternatives

The local-energy proof, reference preparation, local block encodings and complete native receiving theorem are separate premises now explicitly matched. The exact-Fraction threshold acquisition executable is useful shared raw-input arithmetic, but it does NOT implement these quantum rotations or the native simulator; its threshold channel must not be substituted for G.

Classical Glauber simulation, transfer matrices, exact small-system solvers, gauge optimization, elimination with certified boundary corrections, and general high-precision Lindblad algorithms remain strong comparators. The primary recheck is NATIVE_PRIMARY_COMPARATOR_RECHECK.md. No demonstrated practical advantage, priority, unknown-source-learning capability or universal fast-forwarding theorem follows from this corollary.
