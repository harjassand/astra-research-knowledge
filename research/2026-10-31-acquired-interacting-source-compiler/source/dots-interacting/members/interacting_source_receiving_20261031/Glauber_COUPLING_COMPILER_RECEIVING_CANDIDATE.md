# Receiving an interacting Glauber source through established quantized couplings

31 October 2026. Receiving construction with explicit finite-bit acquisition, pending final whole-source review. The quantized-coupling mechanism and coupling-to-qsample return theorem are established prior work, not claimed as an Astra invention: Temme and Wocjan, Quantum 9, 1951 (2025), https://arxiv.org/html/2504.02651v2, especially the inverse-map Kraus construction, Lemma 16 and Theorem 20. The question here is whether its actual operations discharge the input requirements of the separately developed retained fast-source compiler.

## 1. Known input and classical coupling

Take n binary spins with a strictly positive known Gibbs distribution pi and reversible heat-bath flip rates r_i(x). For each fixed configuration of the other spins, the two flip rates sum to one. Each rate depends on at most k neighboring bits, with k bounded for an efficient local construction. Rate tables, stationary ratios, and their numerical precision are paid inputs.

Let c_ij bound the change in site-i conditional probability when only spin j changes. Require a certified column influence sum max_j sum_i c_ij <= 1-kappa, with kappa>0. Pairwise symmetric Ising interaction bounds are one sufficient way to certify this premise, not an assumption that every Gibbs model contracts.

The basic coupling flips both copies at site i with rate min(r_i(x),r_i(y)) if their bits agree, and flips the copies separately with the remaining nonnegative rates. If their bits disagree, each copy flips separately at its own rate. With Hamming distance h, its generator C obeys C h <= -kappa h: a disagreement disappears at rate at least one minus the conditional-probability difference, while an agreement creates a disagreement at rate equal to that difference. Summing the influence bounds gives the column-sum condition above.

## 2. Finite threshold maps and the acquired channel

For each site i and bit b, sort all values r_i(z,b) over local neighbor contexts z, adjoining zero. For an interval of width Delta, select a threshold u inside it and define a deterministic map f that flips bit b to 1-b when the site has bit b and r_i(z,b)>=u; all other labels are unchanged. The contexts do not include the updated bit. Zero-width intervals are omitted. Set R to the sum of all interval widths over i,b; n<=R<=2n.

Give each such map probability Delta/R. These maps form a random-map representation of the classical kernel P=I+Q_class/R. They have at most two preimages per label, found by checking the label and its one-bit-flipped neighbor. Evaluation, preimage enumeration, probabilities and stationary ratios are all local, explicit operations. There is no global conditional-inversion oracle.

For the map f define its unweighted inverse-map operator

T[y,x]=sqrt(pi_y/pi_x) 1{x=f(y)}.

Detailed balance and stationarity make Phi(rho)=sum_f (Delta_f/R) T_f rho T_f^dagger CPTP. Each T_f psi=psi for psi=sum_x sqrt(pi_x)|x>. Its adjoint preserves the diagonal observable algebra with forward kernel P because P is reversible. These are instances of the established quantized-grand-coupling construction.

Write M_f=T_f-I. In an enabled context with output bit b and a=1-b, its nonzero row is

|b>(sqrt(r_i(z,a)/r_i(z,b))<a|-<b|).

The equality uses detailed balance. Its context blocks are coherent; recording the full spin configuration as an environment color would be a different, potentially slow lift.

The weighted sum sum_f Delta_f M_f is Hermitian (the two directions have the same offdiagonal sqrt(r_i(z,0)r_i(z,1))). Trace preservation gives

sum_f Delta_f (M_f+M_f^dagger+M_f^dagger M_f)=0.

It follows exactly that

G := sum_f Delta_f D[M_f] = R(Phi-I).

Thus this collision realization is an exact uniformization of a local Lindblad source whose diagonal restriction is the ORIGINAL continuous-time Glauber generator Q_class. No time-discretization or replacement by a finite-time Glauber block is used.

## 3. Actual return certificate

The same random maps couple two classical copies. One step has Hamming contraction at most a=1-kappa/R. Consequently the probability of noncoalescence after m steps is at most n a^m, uniformly over initial labels.

The established quantized-coupling bound yields

(Phi^dagger)^m Q_psi <= min(1,n a^m/pi_min) Q_psi,
Q_psi=I-|psi><psi|.

For completeness, the source operator bound can be seen through the pair process started in pi tensor pi. Its marginals stay pi. If nu_m is its pair law, B_m=(Phi^dagger)^m |psi><psi| has entries nu_m(x,y)/sqrt(pi_x pi_y). The positive operator I-B_m annihilates psi and has trace

sum_x [pi_x-nu_m(x,x)]/pi_x <= Pr(X_m!=Y_m)/pi_min.

Bounding its largest eigenvalue by its trace gives the stated inequality. It tensors with an arbitrary reference; it is not merely a statement about diagonal initial source states.

A valid acquired return horizon is

m=ceil[(R/kappa) log(16n/pi_min)],

or any safely rounded certified upper bound. A known lower bound on pi_min suffices. This may be conservative; pi_min enters logarithmically in m, not as an exponentially slow physical rate.

## 4. Reference preparation and centered controls on a concrete admitted family

For an open one-dimensional Ising chain, square-root Gibbs preparation is an ordinary sequential conditional-amplitude circuit. Positive transfer-matrix messages compute each conditional spin probability; controlled one-qubit rotations prepare their square roots. This costs O(n) rotations plus the explicitly paid arithmetic/precision work. It is not inferred from a classical sampler. A rigorous finite-bit implementation must bound its total preparation error as part of the compiler budget.

If the local Boltzmann factors are positive rational input data and the source-diagonal Pauli coefficients are rational input data of bounded bit length, transfer-matrix products also compute the expectations of supplied spin-product strings with exact rational arithmetic, using inserted spin-sign diagonal matrices. Numerator/denominator bit lengths and the number of strings are paid. The source mean Hamiltonian can therefore be acquired for a sparse supplied diagonal Pauli coupling. Its nontrivial mean action remains in the physical Hamiltonian; centering does not erase that action. General graphs do not acquire efficient exact means or square-root preparation from this one-dimensional construction.

A conservative lower bound on pi_min follows directly from a bound on the finite input energy range. For bounded chain couplings and fields, log(1/pi_min)=O(n); this statement is not uniform over unbounded numeric inputs.

The actual Stinespring is acquired by the bound companion FINITE_BIT_THRESHOLD_STINESPRING_CONSTRUCTION.md, SHA256 d560f37e39a501a03d3c1c419bed8919eb5149cf9570076e04ce0ac48f2fd1a0. For each coherent input x, it prepares a rational table of the O(n 2^k) colors and at most two preimages, with amplitudes sqrt[(Delta_f/R)pi_y/pi_x]. Reversible evaluation of x=f(y) erases the old input and the auxiliary preimage slot. A finite binary rotation tree and exact rational predicates give polynomial gate/arithmetic cost in n, 2^k, explicit input bit length and log(1/zeta), without a minimum branch-probability promise. Its output supports for distinct inputs are disjoint, so the uniform operator error does not gain a sqrt(2^n) factor. Actual unitary reversal supplies W-dagger. The color state c has explicit positive amplitudes sqrt(Delta_f/R). Reference preparation and reflection remain separately paid. This is a complete circuit construction on paper, not an executed quantum gate backend. Efficient asymptotics require the stated context width and return/conditioning parameters to remain controlled; an exponentially small kappa is not declared cheap.

## 5. Binding to the retained fast-source compiler

For the physical model lambda G + H0_super + sqrt(lambda) V, use the exact identity G=R(Phi-I). In the previous pure-return compiler variables,

lambda_prime=lambda R,       b_prime=b/sqrt(R),
B_prime=b_prime^2 T=b^2 T/R.

The acquired reference, return horizon m, Stinespring and source-diagonal controls must be supplied with the total finite-bit errors charged. Their costs depend on n, local context width, input conditioning, return parameters and requested accuracy. They do not scale with the microscopic activity lambda merely because the source makes more transitions. The old compiler's explicit polynomial m and B_prime factors remain; this is not a small-constant resource claim.

Allowed classical controlled-process equivalence requires instruments whose ADJOINTS preserve the source-diagonal system-operator-valued algebra and have the prescribed classical restriction. The final physical classical source register is obtained by computational-basis dephasing or measurement of the lifted source output; the raw coherent lift is not asserted to equal the physical CQ density matrix. Arbitrary quantum-source coherences or exposing private artificial jump colors are not received. The full quantum compiler may have broader controls, but the equality to this classical physical source has this narrower scope.

## 6. Comparison and remaining evidence

Quantized coupling, qsample preparation and sparse local inverse-map implementation are prior methods. Dense CQ exponentiation already has logarithmic switching-rate dependence at full dimension. Ordinary stochastic-Liouville, multiscale, Fourier and tensor methods remain strong comparators. A sparse or local source does not make a noncommuting driven system easy by itself.

The possible additional consequence is a fully paid retained controlled simulator for this interacting source family using the previous centered fast-source compiler. This candidate still needs final whole receiving review. Its finite-bit circuit construction is explicit on paper; a working quantum gate implementation and concrete resource crossover remain unestablished. No novelty or practical advantage is established, and a polynomial asymptotic bound is not a civilisation-changing discovery.
