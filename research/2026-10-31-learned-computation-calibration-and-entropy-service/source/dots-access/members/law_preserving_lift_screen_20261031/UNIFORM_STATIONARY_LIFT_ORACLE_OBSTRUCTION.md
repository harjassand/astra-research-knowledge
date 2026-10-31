# A uniform-stationary acquisition obstruction: a pure law-preserving lift coherifies the kernel

31 October 2026. Author proof, pending independent review. This is a lower bound in an explicit oracle-access model, not a claim that all inspectable classical programs are hard to lift or that their classical dynamics are hard to simulate.

## 1. A rigidity identity for any such lift

Let P(y|x) be a finite classical kernel with strictly positive stationary pi. Suppose a CPTP channel Phi has Kraus operators K_a and satisfies both:

1. Its adjoint preserves the full source-diagonal observable algebra with the exact specified law:

       Phi^dagger(|y><y|) = sum_x P(y|x)|x><x|.

2. It fixes the pure reference psi=sum_x sqrt(pi_x)|x>.

Pure fixedness implies K_a psi=c_a psi for a normalized environment vector c. For each fixed output label y, introduce environment vectors

    v_yx = sum_a K_a[y,x]|a>.

Assumption1 gives their orthogonality and lengths:

    <v_yx,v_yx'>=0 for x!=x',       ||v_yx||^2=P(y|x).

Assumption2 gives

    sum_x sqrt(pi_x) v_yx = sqrt(pi_y)c.

Taking the inner product with v_yx yields the exact overlap identity

    A_yx := <c,v_yx> = sqrt(pi_x/pi_y) P(y|x),
    A = diag(pi)^(-1/2) P diag(pi)^(1/2).                (1)

Thus ANY acquired Stinespring isometry W of this kind block-encodes the balanced classical kernel as A=(<c| tensor I)W. This is not peculiar to the reverse-map construction or its choice of Kraus operators. It uses adjoint-algebra invariance, stronger than merely matching transition probabilities on diagonal input states.

## 2. A rapidly coalescing known-uniform family

Let d=2^n and let f:[d]->[d] be an unknown oracle permutation. Access is the usual reversible evaluation oracle

    O_f |x,z> = |x,z xor f(x)>.

This oracle is self-inverse but is NOT the in-place permutation unitary |x>->|f(x)>; it does not supply f^(-1). Define

    P_f = (U_f + J)/2,
    (U_f)_(y,x)=1{y=f(x)},       J_(y,x)=1/d.

A forward classical step either evaluates f(x) or draws a fresh uniform label. The stationary law is the strictly positive, explicitly known uniform law on the full d-label register. Its pure square-root state psi=|+>^n is free up to n Hadamards.

The forward random-map representation is also explicit: with probability1/2 apply f; otherwise choose z uniformly and apply the constant map x->z. A word containing a reset is constant. Consequently the maps coalesce after m steps except with probability2^-m, uniformly over every pair of initial states. Classical mixing and perfect-sampling resources do not grow with d except for writing an n-bit label and the forward oracle call. The reversed kernel uses f^(-1), however; its random-map evaluation is not supplied for free by the forward coupling certificate.

## 3. An acquired pure lift would invert f

Suppose an acquisition procedure, using O_f, produces a coherently executable Stinespring unitary U_W extending a W satisfying the two conditions in Section1 for P_f. Let q_acq be the number of forward-oracle queries used to acquire a classical circuit description and any reusable classical advice, and q_use the worst-case query cost of one use of that circuit. We require a coherent reversible clean-ancilla implementation, so its inverse is actually available by reversing its gates. An irreversible channel-only box, or a consumed unknown quantum program whose inverse cannot be executed, is not the promised interface. The total acquisition and execution oracle queries are charged. Since pi is uniform, (1) becomes

    (<c| tensor I)W=P_f.

The reference vector c need not be granted as free advice. Apply W to psi; its output is exactly c tensor psi. Unprepare the known psi on the source, obtaining c with clean source workspace. This uses one W invocation.

Given a target label y, prepare c tensor |y>, apply U_W^dagger, and project onto the initially clean Stinespring ancillas. The unnormalized remaining source state is

    P_f^dagger |y> = (1/2)|f^(-1)(y)> + (1/(2d))sum_x |x>.

Measure the source and the clean-ancilla flag. The unconditional probability of obtaining the correct inverse x=f^(-1)(y) together with success is

    (1/2+1/(2d))^2 >= 1/4.                             (2)

Verify any candidate using one call to O_f, and repeat a constant number of times. This gives bounded-error permutation inversion using only a constant number of W/W^dagger invocations plus their acquisition and c-preparation costs. No unnormalized postselection is being treated as deterministic; the success probability is explicitly constant.

The reduction is robust to refinable circuit synthesis: approximate the ideal W and its inverse in operator norm, and c preparation in vector norm, by sufficiently small fixed constants, for example a combined amplitude error at most1/16. The correct-output amplitude remains at least7/16, so constant repetition still gives bounded-error inversion. Arbitrarily precise or exact synthesis is not required for the obstruction.

## 3a. Robust approximate reference, without approximate diagonal-law assumptions

A stronger obstruction retains exact adjoint-diagonal law but allows an approximately pure reference. Assume W is an exact acquired isometry with the exact law P_f and there is a unit environment vector c0 for which

    ||W|s> - c0 tensor |s>||_2 <= epsilon,   |s>=|+>^n,

where epsilon<=1/4. Let v=(I_env tensor <s|)W|s>, and choose c=v/||v||. This phase choice minimizes the product-state distance, so the same epsilon bound holds with c. Also

    ||v|| >= 1-epsilon^2/2.

One W invocation followed by projection of the source onto the known s prepares c with probability at least (1-epsilon^2/2)^2. Failure is simply an abort; no amplitude amplification or unpriced expected waiting is used.

For each y let r_y=sum_x v_yx-c. The product-distance premise gives sum_y ||r_y||^2<=d epsilon^2. Exact diagonal-law invariance still makes the v_yx orthogonal, so, with A_yx=<c,v_yx>,

    sum_x |A_yx-P_f(y|x)|^2
        =sum_x |<r_y,v_yx>|^2
        <= (max_x P_f(y|x)) ||r_y||^2 <= ||r_y||^2.

Hence ||A-P_f||_F^2<=d epsilon^2. For a uniform target y, the L2 average of the error in the correct-inverse amplitude is at most epsilon. The correct amplitudes of P_f are at least1/2, so the L2 triangle inequality shows that the average unconditional inverse success after preparing c is at least (1/2-epsilon)^2. Including the c-preparation flag yields

    Pr(correct inverse, averaged uniform y)
       >= (1-epsilon^2/2)^2 (1/2-epsilon)^2.             (3)

This is a positive constant for epsilon<=1/4. The attempt uses one W, one W^dagger, and one forward oracle query to verify the result; it has bounded query count, not only bounded expected count.

To receive a fixed-target DISTRIBUTIONAL inversion lower bound, let f be uniform over permutations and choose an independent uniform output XOR shift z. Supply f'=f xor z to the lift acquisition and use target y'=y0 xor z. Then f' and y' are independent uniform variables, and a correct inverse is exactly f^(-1)(y0). A query to the XOR oracle for f' uses one query to O_f followed by a known XOR shift on the answer register. On a verified successful inversion return the parity of the inverse; on failure guess a fair parity. If the inversion success is s>0, this decision has distributional success1/2+s/2. The primary distributional lower bound below therefore applies without an uncharged amplification loop or a worst-case/average-case substitution.
This robustness statement does not cover an approximately correct diagonal process without additional norm/error hypotheses. Ordinary refinable synthesis of the declared isometries can be separately made accurate to a small constant, preserving the constant success margin.

## 3b. A fast pure lift exists, but its access is the expensive operation

There is no existence obstruction for this family. The channel

    Phi_f(rho) = (1/2) U_f rho U_f^dagger
                 + (1/2) |s><s| Tr rho

has the exact prescribed diagonal law, fixes s, and satisfies Phi_f^dagger(Q)=Q/2. Four steps supply the1/16 pure-return certificate. But U_f here is the IN-PLACE permutation unitary, whose acquisition from forward XOR evaluation is precisely not free. This example separates the return horizon from the cost of the acquired channel realization.

## 4. Primary lower bound and exact consequence

Ambainis, *Quantum lower bounds by quantum arguments*, quant-ph/0002066, Section6.2 Theorem7, proves the standard Omega(sqrt d) quantum query lower bound for permutation inversion. For the approximate-reference average-target step, Nayak, *Inverting a permutation is as hard as unordered search* (2011), Corollary1.2, explicitly supplies an Omega(sqrt d) lower bound for deciding the parity of a fixed target's inverse with any constant distributional advantage over random guessing on uniform permutations. Its oracle is the value/XOR query interface. Both primary texts were inspected:

    https://arxiv.org/pdf/quant-ph/0002066
    https://www.math.uwaterloo.ca/~anayak/papers/Nayak11.pdf

The output-shift and verified-parity reduction in Section3a matches this distributional scope directly.
Applying that theorem to (2) gives

    q_acq + 2 q_use + 1 = Omega(sqrt d),

with the constant depending only on the fixed positive decision advantage. No repetition is necessary for the distributional parity reduction. The one attempt uses one W to acquire c, one W^dagger for inversion, and one oracle verification. No online-only lower bound is asserted after arbitrary uncharged preprocessing.

In particular there is no generic poly(n)-query front end, from the stated forward-oracle classical program and coalescence certificate alone, that acquires this pure, full-diagonal-law-preserving quantum source interface. This holds despite trivial full-support pi, cheap psi, and constant-scale forward coalescence. It does not need the unknown-support qualification of the separate Index Erasure example.

The lower bound charges preprocessing. A procedure that first learns a full permutation/inverse table can reuse it cheaply afterward; that does not violate the claim. Conversely a per-use lower bound that ignored expensive retained preprocessing would be false. The input model does not supply an inverse oracle, in-place U_f, a conditional inverse-fibre isometry, or f-dependent advice for free. Supplying any of those can remove the obstruction and must be an explicit resource choice.

This is an oracle barrier, not an unconditional lower bound against reading and analyzing every explicitly written circuit for f. A structured circuit may provide a cheap inverse, and reversible permutations already given as in-place circuits are an especially simple case. Nor is this a lower bound on every simulator of the classical process or every allowed system observable: the elementary forward classical step and stationary sampling remain easy. The obstruction targets the proposed acquired PURE quantum realization preserving the full diagonal adjoint law.

## 4a. The forced overlap does not fix purification

The identity A=P does not determine the return behavior of Phi. On one uniform bit let P=J=(I+X)/2 and s=|+>. Both

    Phi_1(rho)=(rho+X rho X)/2,
    Phi_2(rho)=|+><+|Tr rho

have the same exact diagonal law, the same pure fixed s and overlap A=J. Yet Phi_1 preserves |-><-| and never absorbs that Q state, whereas Phi_2 resets it immediately. Thus acquiring balanced-kernel access and classical mixing is still insufficient to earn the pure-return certificate. Choosing an environment/complement realization that actually purifies is a separate operation. This failure remains even when reverse access and stationary-state preparation are trivial.

## 5. Consequence for choosing the next operation

Forward coupling/coalescence and known stationary amplitudes are not enough to acquire the desired interface. The reverse-map inverse-fibre requirement is not just an artifact of one construction: the overlap identity forces balanced-kernel coherent access for every pure-fixed full-law lift.

This sharpens the worthwhile structural question: which succinct programs supply an efficiently acquired balanced-kernel/inverse-fibre operation or equivalent coherent outlet, together with a conditional return certificate? Affine deadbeat synthesis supplies such operations for its specific program class; a general forward perfect sampler does not. Before developing another class, compare total acquisition and retained reuse with ordinary forward simulation and any available inverse/conditional-sampling algorithm. No superiority or foundational practical capability is established by this negative result.
