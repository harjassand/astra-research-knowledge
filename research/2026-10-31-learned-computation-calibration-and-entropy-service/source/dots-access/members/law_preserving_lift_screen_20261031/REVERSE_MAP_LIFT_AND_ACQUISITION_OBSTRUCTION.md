# Law-preserving pure lifts: inverse fibres, conditional coalescence, and an acquisition obstruction

31 October 2026. Independent author construction and opportunity screen, pending review. No general efficient compiler is claimed. The algebra below identifies precisely which extra acquired operation a classical random-map certificate would need to supply.

## 1. Reverse random maps give an exact pure-fixed quantum lift

Let P be a finite column-stochastic kernel with a known strictly positive stationary law pi on its physical support X. Define its time reverse

    P_rev(x|y) = pi_x P(y|x)/pi_y.

Suppose a random-map representation of this REVERSED kernel is supplied:

    P_rev(x|y) = sum_a w_a 1{x=f_a(y)},   sum_a w_a=1.

Define psi=sum_x sqrt(pi_x)|x> and Kraus matrices

    K_a[y,x] = sqrt(w_a pi_y/pi_x) 1{x=f_a(y)}.             (1)

Every row of K_a has at most one nonzero input column. Consequently K_a^dagger K_a is diagonal. Its x diagonal, summed over a, is

    (1/pi_x) sum_(a,y) w_a pi_y 1{x=f_a(y)}
       = (1/pi_x) sum_y pi_x P(y|x) = 1.

Thus Phi(rho)=sum_a K_a rho K_a^dagger is CPTP. Moreover

    K_a psi = sqrt(w_a) psi,                              (2)

with the SAME positive phase convention for all a. The Stinespring reference vector is c=sum_a sqrt(w_a)|a>, and W psi=c tensor psi exactly.

For every diagonal source observable D=diag(d_y),

    Phi^dagger(D) = diag_x sum_y P(y|x)d_y.

Indeed all offdiagonal entries vanish row by row, and the diagonal entries follow Bayes' identity. The same argument holds for operator-valued diagonal observables on a coupled system. Therefore diagonal Hamiltonian couplings and instruments whose adjoints preserve that algebra retain the entire outcome-recorded classical controlled process. This does not identify arbitrary quantum source operations with the original classical task, or reveal the random-map Kraus label as a physical source event.

Zero-probability stationary labels must be handled by a separately specified extension or excluded support. Formula (1) does not divide by zero. Restriction to a support is not automatically an efficient membership/preparation operation.

## 2. The exact conditional coalescence certificate

For a length-m word a=(a_1,...,a_m), define w(a)=product_j w_(a_j) and the composed inverse map

    f_a = f_(a_1) o f_(a_2) o ... o f_(a_m).

Multiplying the Kraus matrices telescopes the pi factors:

    K_(a_m)...K_(a_1)[y,x]
        = sqrt(w(a) pi_y/pi_x) 1{x=f_a(y)}.                (3)

Call a word good when f_a is constant, with value z(a). Its Kraus product is rank one,

    K_word = sqrt(w(a)/pi_(z(a))) |psi><z(a)|.

It therefore contributes no output in Q=I-|psi><psi|. Let Y independently have law pi, and define

    rho_m = max_x Pr( word bad AND f_word(Y)=x ) / pi_x.  (4)

The trace effect of all bad Kraus words is diagonal with precisely these ratios as its entries. Hence

    0 <= (Phi^dagger)^m(Q) <= rho_m I.

Since Phi fixes the pure psi, the positive operator on the left annihilates psi; therefore

    (Phi^dagger)^m(Q) <= rho_m Q.                         (5)

This is the useful algorithmic power-return certificate if rho_m<=1/16. Coalescence in unconditional probability alone only gives the weaker bound

    rho_m <= Pr(word bad)/pi_min.

The pi_min factor is an upper-bound loss, not a universal necessity. Condition (4), rather than just a coupling-time tail, is the actual sufficient certificate received here. In some structured couplings the conditional ratio can be controlled without pi_min. Strong-stationary or conditional-uniform-root assertions must be proved for the chosen maps and direction; they cannot be inferred from the phrase 'coupling from the past'.

This is a sufficient lift, not a characterization of all quantum realizations. Failure of its coalescence certificate does not prove no other realization has rapid pure return.

## 3. What must actually be acquired

The isometry in (1) is

    |x> -> sum_(a,y:f_a(y)=x) sqrt(w_a pi_y/pi_x) |a>|y>.  (6)

Thus an implementation must coherently prepare a conditional inverse fibre. Evaluating f_a(y), sampling a, or obtaining a classical coalescent stationary sample does NOT by itself implement (6). The conditional normalization is exactly pi_x; naively preparing independent a,Y and postselecting f_a(Y)=x has success pi_x and introduces unpriced inverse-probability cost. A normalized postselected state is not an acquired deterministic Stinespring circuit.

Sufficient explicit inputs for this route are:

- a phase-consistent preparation of psi and c, plus their inverses;
- a coherent isometry (6), uniformly for superposed x, with paid error/cost;
- a certified bound (4) at an acquired m;
- actual coupling/control encodings and all existing compiler interfaces.

With these inputs, the previously proved pure-return compiler applies without enumerating all labels. But listing these operations is not acquiring them. Affine reversible fibre completion and structured shuffle circuits earned them in special cases; an arbitrary classical mapping program has not.

For comparison, a general pure-fixed lift can also be constructed from acquired coherent FORWARD transition states and acquired reverse conditional states

    |phi_y> = sum_x sqrt(pi_x P(y|x)/pi_y)|x>.

Prepare forward y conditional on input x, then apply on the retained input register a controlled unitary U_y mapping phi_y to a common |0>. The resulting W has W psi=|0> psi and exactly the diagonal transition law, because for each y the vectors U_y|x> are orthonormal. This construction again requires coherent conditional preparation. It also supplies no rapid pure-return bound merely from classical mixing; it is not a substitute for (3)-(5).

## 4. A rigorous oracle obstruction to promoting classical perfect sampling

Let an injective oracle f:[N]->[M] be given. A classical source that resets at every event to f(Z), Z uniform on [N], has one-query sampling cost and a one-step coalescent random-map realization: each map sends every input to f(z). Its stationary law is described succinctly as uniform on the image of f. On the ambient M-label register this law has zeros and an unknown support; it is not a strictly positive, known-coordinate stationary law. The reset kernel itself is defined on every ambient input, so classical forward simulation remains well-defined without deciding support. Its required square-root stationary state is

    psi_f = N^(-1/2) sum_z |f(z)>.

Preparing psi_f from the oracle is the Index Erasure problem, not the same operation as preparing N^(-1/2) sum_z |z>|f(z)> and discarding z. Thus a generic acquisition theorem that converts this classical generative description/perfect sampler into a cheap pure-reference preparation would solve Index Erasure.

Primary evidence: Ambainis, Magnin, Roetteler and Roland, 'Symmetry-assisted adversaries for quantum state generation', Theorem29, proves the familiar square-root query obstruction in the coherent workspace-clean model. Lindzey and Rosmanis, 'A Tight Lower Bound For Non-Coherent Index Erasure', ITCS2020 Theorem1, proves Theta(sqrt N) even allowing function-dependent garbage, under its stated sufficiently-large-range condition M>=N^(3 sqrt N). The latter range qualification is important: this source alone does NOT establish an exponential-in-log M noncoherent lower bound. For both citations here choose this sufficiently-large-range regime and a fixed small bounded error. No claim is made for all M>=N: when M=N the image is known and uniform-state preparation needs zero oracle queries. These are oracle-query results, not lower bounds for every explicitly inspectable polynomial circuit family.

Primary URLs inspected:
- https://arxiv.org/pdf/1012.2112 (Section7, Theorem29, coherent regime).
- https://drops.dagstuhl.de/storage/00lipics/lipics-vol151-itcs2020/LIPIcs.ITCS.2020.59/LIPIcs.ITCS.2020.59.pdf (Theorem1, noncoherent regime and range condition).
- https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.59 (author/publisher record).

The obstruction applies when 'known pi' means an acquired classical generative description, not a supplied coherent psi preparation. It does not directly lower-bound the strictly-positive known-coordinate input model of Sections1-3; changing the support representation would itself require an acquired indexing/interface operation. It does NOT refute a theorem that explicitly pays for psi, assumes uniform known full support with easy psi, or supplies conditional-fibre access. It also does not prove simulation of this classical source is hard: direct classical samples remain easy. What fails is an automatic cheap conversion to the particular pure-source interface.

## 5. Independent check of a continuous-time edge lift

Here is a complementary algebraic construction proposed by the parent, checked directly. Let q_yx>=0 for distinct x,y be a classical column-generator's rates, with strictly positive stationary pi. Set

    L_yx = sqrt(q_yx) |y>(<x|-sqrt(pi_x/pi_y)<y|),
    H_xy = -(i/2)[q_yx sqrt(pi_x/pi_y)-q_xy sqrt(pi_y/pi_x)] (x!=y),
    H_xx=0.

H is Hermitian. Every L annihilates psi. Stationarity gives

    (H psi)_x=-(i/2)[sqrt(pi_x) sum_(y!=x)q_yx
                   -(1/sqrt(pi_x))sum_(y!=x)q_xy pi_y]=0.

On diagonal D, the dissipator's xy entry is one half the bracket in H_xy times (d_x-d_y); i[H,D] contributes its negative. The remaining diagonal is the exact classical generator. Thus the Lindblad dynamics preserves the diagonal observable algebra with the required classical law and has pure fixed psi.

This establishes algebraic existence, not a cheap acquired source. Jump-stack and H access contain stationary ratios and possible edge enumeration, which must be paid. More importantly, attraction to psi can be dimension-slow even when the classical chain mixes instantly on its own scale.

Indeed with P=|psi><psi|,

    G^dagger(P) = sum_(x!=y) q_yx
      |sqrt(pi_y)x-sqrt(pi_x)y><sqrt(pi_y)x-sqrt(pi_x)y| =: R.

The other terms vanish because H psi=0 and L psi=0. For an irreducible finite chain, the underlying undirected graph is connected, so ker R is exactly span(psi). A lower bound R>=g Q implies (e^(tG^dagger)Q)<=e^(-g t)Q. But g need not track the classical spectral gap.

Explicit example: d labels, uniform pi, q_yx=1/d for every x!=y. The classical generator is uniform-reset minus identity, with gap1. Here H=0 and

    R = (1/d^2) sum_(x!=y)(|x>-|y>)(<x|-<y|) = (2/d)Q.

Therefore Q survival under this edge lift is EXACTLY exp(-2t/d), not merely bounded that way. Acquiring a1/16 return takes t=(d/2)ln16. In contrast, the nonlocal quantum reset generator rho -> |psi><psi|Tr rho - rho has the SAME classical diagonal reset law and Q survival exp(-t), with an easily prepared uniform psi. The failure is the chosen edge-local outlet, not impossibility of a better lift.

Thus a general edge lift can hide an exponential-in-register-size return cost even when stationary-state preparation is trivial. Coherently combining destinations or acquiring nonlocal outlets is a real computational operation. It must not be replaced by a norm estimate or an assertion that every classical rapidly mixing chain has an efficiently acquired rapidly pure-mixing completion.

## 6. Opportunity decision and ordinary baselines

Classical random mappings, coupling/coalescence, perfect sampling, conditional sampling, coherent state preparation, and the preceding pure-lift algebra are strong ordinary ingredients. This note does not claim novelty for those theories, nor for the existence of a lift. The actual next operation worth studying would be an efficiently acquired inverse-fibre/nonlocal-outlet construction with a conditional return certificate for a consequential raw-program class not already solved by its ordinary retained classical representation.

Without such a class, the broad proposal does not yet justify another compiler theorem. The two failures above are concrete: cheap classical perfect sampling need not acquire psi, and an easily acquired edge-local pure lift can lose a factor d in return time even for the uniform reset chain. The inverse-fibre theorem provides an exact receiving target, not a free acquisition algorithm. No additional workers, source-denial retries, uploads, or external communications were used.
