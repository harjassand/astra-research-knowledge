# Independent hidden matchgate audit and arithmetic construction

2026-10-27. `INITIAL_LOCKED_JUDGEMENT.md` was written before reading the parent's local criterion. This report subsequently audits it. No Astra scientific proof was imported; no protected producer folder was edited.

## Outcome

**The determinant beta criterion is correct at its stated generic/nonzero-CP-edge scope.** It is also necessary for compatible independent edge bases making generic ternary tensors even/odd matchgates. A uniform polynomial-bit modular construction follows. For rational inputs **F_(p²) suffices throughout**, including all CP factors, edge square roots and Pfaffians. An exponential characteristic-zero compositum is an implementation trap, not an obstruction to this operation.

This recognizes/evaluates a known heterogeneous-basis Pfaffian class. It is not a new tractability class or contraction method. The checked primary sources did not supply a theorem for this full raw-input, uniform exact-bit interface; that bounded search establishes neither priority nor novelty. Practical advantage, application breadth, physical significance and the original 100/100 mission remain UNKNOWN / NOT_ACHIEVED.

## Exact admitted class

Input: a closed planar trivalent graph with a valid cyclic embedding and rational 2×2×2 tensors. Every local hyperdeterminant must be nonzero. Absorb all component weights in the rank-two CP factors:

    T_v = ⊗_(legs e) u_(v,e,0) + ⊗_(legs e) u_(v,e,1).

For an oriented edge e=vw let M_e[a,b]=u_(v,e,a)^T u_(w,e,b). Require all four entries nonzero. This zero pattern is invariant under CP permutation/rescaling. Use incidences, rather than neighbor identities, if loops or parallel edges are admitted.

Let q_(w,e)(x)=det(T_w contracted with x on leg e), a RATIONAL binary quadratic, and define

    beta_v = product_(incident e=vw)
                 q_(w,e)(u_(v,e,1))/q_(w,e)(u_(v,e,0)).

The class C consists exactly of the above nondegenerate/nonzero-edge inputs with every beta_v=1. The proposed compiler returns UNKNOWN outside this precise admitted class. A failed representation test does not imply hardness or failure of other algorithms.

## Strongest established operation checked first

| Prior route | Established operation | Difference from present raw-input contract |
|---|---|---|
| Cai–Lu simultaneous realizability | Polynomial-time discovery of one common basis for symmetric signatures | Does not by its cited theorem discover independently varying edge bases for an arbitrary nonsymmetric instance |
| Common-basis equations at bounded arity | Nonsymmetric ternary signatures can also be tested with a fixed number of basis variables and bounded-degree equations | Stronger than comparing only with symmetric SRP, but still one common basis |
| Morton heterogeneous Pfaffian circuits | Different compatible edge basis types, odd signatures, fast Pfaffian evaluation | Basis types/compatibility form part of the described circuit; individual ternary realizability is not circuit recognition |
| Margulies–Morton linked ideals | Exact heterogeneous compatibility equations, solved computationally for particular families | No checked general polynomial-bit bound for the growing arbitrary linked instance |
| Chernyak–Chertkov local Wick gauges | Arbitrary graph-local paired inverse 2×2 gauges of planar free-fermion models | Already supplies the underlying tractability orbit, with the representation given/constructed |

Primary sources downloaded under `sources/`:

1. [Cai–Lu, ECCC TR06-145](https://eccc.weizmann.ac.il/report/2006/145/download), section 3.2 / Theorem 3.1, PDF pp.7–8. The input is symmetric signatures and the output one common basis. Journal successor: [JCSS 77 (2011)](https://doi.org/10.1016/j.jcss.2010.06.005).
2. [Morton, arXiv:1101.0129](https://arxiv.org/abs/1101.0129), Definition 4.6 / Theorem 4.7, PDF pp.15–16; Theorem 6.4 and its following compatibility qualification, pp.29–30. Heterogeneous compatible bases and their evaluation are prior.
3. [Margulies–Morton, arXiv:1311.4066](https://arxiv.org/abs/1311.4066), introduction and section 3; published [JSC 74 (2016)](https://doi.org/10.1016/j.jsc.2015.06.008). The linked-ideal method is a substantive recognition baseline. Its evaluation bound must not be silently used as its basis-discovery bound.
4. [Chernyak–Chertkov, arXiv:0902.0320v5](https://arxiv.org/abs/0902.0320v5), Theorem II.7 and local gauge section. The underlying free-fermion representation is established here.
5. For deterministic prime enumeration below: [Rosser–Schoenfeld (1962)](https://doi.org/10.1215/ijm/1255631807), Theorem 3 / corollary on p.69, gives the standard polynomial bound on the K-th prime.

The strongest checked baseline is therefore heterogeneous compatibility discovery by linked polynomial equations, not merely supplied-gauge FKT. This search does not exclude an older specialized treatment, or an existing combination of CP/gauge arithmetic and modular FKT supplying the identical operation.

## 1. CP construction, uniqueness and local exact arithmetic

Take first-leg slices A0,A1. Since det(A0+t A1) is a nonzero quadratic, one of t∈{0,1,2} gives invertible A=A0+t A1. At an odd good prime the same three distinct choices suffice. Put C=A1 A^(-1). Nonzero hyperdeterminant makes its eigenvalues lambda_0,lambda_1 distinct. They lie in a degree-at-most-two extension K_v/Q.

For an eigenvector matrix U and V=U^(-1)A, use these CP factors:

    leg 1, component s: (1-t lambda_s, lambda_s)^T;
    leg 2, component s: column s of U;
    leg 3, component s: row s of V, transposed.

Both tensor slices reconstruct exactly. If C01≠0, use eigenvectors (C01,lambda_s-C00). If only C10≠0 use (lambda_s-C11,C10). If both off-diagonals vanish, rational coordinate eigenvectors suffice. Thus no unspecified numerical eigenroutine or growing-degree elimination is hidden here.

Any rank-two CP decomposition must diagonalize this same simple-spectrum pencil. Its two summands are therefore unique up to common permutation and leg scalings whose product across the three legs is 1 for each component. This proves the Galois-permutation premise.

For exact preprocessing use the two-dimensional quadratic etale algebra A_v=Q[z]/(z²-d_v), d_v≠0. No integer factorization is needed. If d_v is a rational square this algebra splits; its two evaluations are the two CP label choices. The explicit chart is invertible in both branches and the tested properties are label-invariant. Coefficientwise identity tests are therefore sound in this split case too. One may instead treat rational eigenvalues directly.

## 2. The determinant ratio and nonzero tests

Expanding a contracted determinant gives

    q_(w,e)(x) = c_(w,e)
                    (x^T u_(w,e,0))(x^T u_(w,e,1)),

where c is the product of the other two leg determinants and is nonzero. Consequently

    r_(v,e)² = M10 M11/(M00 M01)
             = q_(w,e)(u_(v,e,1))/q_(w,e)(u_(v,e,0)).

At the other endpoint use M01 M11/(M00 M10). Thus beta_v uses ONLY A_v; no neighboring root embedding is required. Both q evaluations are nonzero exactly when all four edge pairings are nonzero. In A_v this is checked by rational norms.

Component rescalings multiply the three ratios by squares whose product is 1. Swapping a vertex's components inverts beta_v. Hence beta_v=1 is intrinsic and uses only a constant number of local quadratic-algebra operations per vertex.

## 3. Sufficiency and global sign

Choose r with r²=M10 M11/(M00 M01), and set s=M11/(M00 r). Dividing row 1 by r and column 1 by s makes each edge [[a,b],[b,a]], where a=M00 and b=M01/s. Restoring the removed factors gives vertex weight [1,g_v], with g_v the product of incident r/s values. If beta_v=1, then g_v²=1, so g_v=±1 in odd characteristic.

For each connected component,

    R = product_v g_v = product_e M11/M00,
    R² = product_v beta_v = 1.

In a characteristic-zero field this is exactly +1 or -1, without expanding the field. Swapping v's CP components changes R by 1/beta_v=1. Allowed factor normalizations cancel globally. Independent root/label choices therefore give the same rational sign.

An edge root sign flip toggles g at its two ends. A spanning-tree incidence solve removes all residual signs iff R=+1. If R=-1, global spin complement preserves symmetric edge weights and negates the vertex-weight product, proving the exact component partition ZERO. Loops toggle twice and do not alter this incidence argument. This is a solved zero case rather than an unresolved sign branch.

## 4. Necessity for the stated representation

Suppose paired local edge bases make every generic ternary tensor an even or odd matchgate. Pull parity diag(1,-1) back to each original leg and then to its CP basis. Each resulting operator S is a traceless involution. CP uniqueness says the three operators either preserve the two summands or swap them all. If they preserve the summands, all are diagonal with opposite eigenvalues; three such legs give opposite total eigenvalues on the two nonzero summands. The tensor could not be a parity eigenvector. Thus every leg operator has form

    S = [[0,r],[1/r,0]].

Edge compatibility S_v^T M S_w=M gives

    r_v r_w = M11/M00,       r_v/r_w = M10/M01.

Their squares give precisely the determinant ratios. The local parity eigenvalue requires product r_(v,e)=±1, so beta_v=1. Within the nondegenerate/nonzero-edge scope this exactly recognizes compatible independent-edge-basis even/odd matchgates. It does not classify gadget reductions or other tractable mechanisms.

## 5. Stronger finite-field lemma: F_(p²) throughout

Fix any odd good prime p. Every rational quadratic CP pencil splits in F=F_(p²), so all local factors are obtained in this same field. No discriminant-splitting condition in F_p is imposed.

For r²=q(u1)/q(u0), q has F_p coefficients. If the local CP pencil splits over F_p, choose the factors there. Then r²∈F_p, and every nonzero element of F_p is square in F_(p²).

Otherwise Frobenius exchanges the component directions. Write

    u0^p=c u1,      u1^p=d u0.

Applying Frobenius twice gives c^p d=1, hence d/c=1/(c c^p)∈F_p. Homogeneity gives

    (r²)^p = (d/c)²/r²,
    Norm_(F/Fp)(r²) = (d/c)².

For any x∈F*, Norm(x)^((p-1)/2)=x^((p²-1)/2). Thus x is square in F iff its norm is square in F_p. The displayed norm is a square, proving **r already exists in F_(p²)**. Then s, all symmetric edge entries, signs and Pfaffian arithmetic remain in F_(p²). Arbitrary normalization was retained through c,d. This local root lemma does not require beta=1.

This improves the safe degree-four upper bound in the locked initial note. Residue fields of many independent characteristic-zero quadratic fields may coincide; forcing their simultaneous characteristic-zero embedding is unnecessary. Exact rational recognition precedes modular arithmetic, so accidental modular beta equalities never authorize an instance.

## 6. Ordinary Fisher/FKT and its normalization

After removing residual signs, symmetric edge matrices have eigenweights w0=a+b and w1=a-b under orthogonal Hadamard. Each equality vertex becomes 1/sqrt(2) times even parity. The closed trivalent graph has even vertex count n, giving total scalar 2^(-n/2), which is rational. Invertibility of the CP leg matrices gives det M≠0; therefore w0,w1≠0.

Replace every original vertex by a triangle of weight 1. Original state 0 selects the external dimer edge; state 1 does not. Even parity leaves either zero or two triangle vertices needing internal matching, with exactly one matching. Hence

    Z = 2^(-n/2) product_e(w1_e)
              Z_dimer(Fisher graph; external weights w0_e/w1_e).

This is standard Fisher/FKT. The explicit embedding gives a planar Kasteleyn orientation. The known all-external perfect matching fixes the Pfaffian sign. Direct Pfaffian elimination costs O(n³) field operations and permits signed finite-field weights. No additional sqrt(2) extension is needed. Orientation, port order, sign and scalar prefactor are actual obligations, not supplied free data.

## 7. Uniform deterministic bit construction

Let S be total input bit length plus graph/embedding size. Clear the eight denominators separately at each vertex: T_v=A_v/D_v, with integer A_v and positive integer D_v. The answer is Z_int/product_v D_v. This preprocessing and its denominator sizes are polynomial in S.

First carry out exact local CP, nonzero and beta checks in A_v. Every formula involves one vertex and its three neighbors, with bounded algebraic/rational degrees. Coefficient bit sizes are polynomial in the corresponding local input bits; their total is polynomial in S (O(S) up to fixed constants for these formulas). No discriminant factorization or global compositum is needed.

Record a nonzero integer F_bad containing 2; nonzero discriminant numerators and required chart denominators; norms actually inverted in the charts; and numerator/denominators of the nonzero q-evaluation norms. Ignore irrelevant zero coefficients. Its logarithm is polynomial in S. If p does not divide F_bad, all symbolic decompositions reduce legally, local discriminants and CP edge pairings stay nonzero, and exact beta identities survive. Fresh modular chart choices also work by CP uniqueness.

Let H_v=max(1,max_x |A_v[x]|), m=|E|. Then

    |Z_int| ≤ 2^m product_v H_v,
    U = m + sum_v ceil(log2 H_v) + 2 = O(S).

There are at most floor(log2 |F_bad|) distinct bad prime divisors. Among the first

    K = U + ceil(log2 |F_bad|) + 2 = poly(S)

primes there are enough odd good primes for CRT modulus exceeding twice the absolute output bound. The K-th prime is O(K log K), so the numeric primes are polynomial in S, with O(log S) bits. No simultaneous-splitting prime, density assumption or GRH is used.

For a simple deterministic proof, enumerate a quadratic nonresidue in F_p and tabulate all p² squares in F_(p²). Every required root is then found in O(p²) field preprocessing and memory, polynomial in S because p is polynomial in S. Faster finite-field routines may improve this; the existence theorem does not need them. A sieve, local CP reconstruction, O(n³) Pfaffians and CRT all have polynomial bit cost. Check that each residue lies in F_p. Stop once the modulus exceeds the signed-integer bound, reconstruct Z_int uniquely, and divide by product D_v.

The complete accounting is: polynomial exact local preprocessing; orientation/reference matching once; polynomially many small-prime trials; O(p²+n³) operations on O(log S)-bit field elements per trial; polynomial CRT/output work. This is an unoptimized deterministic polynomial-bit bound, not a measured advantage.

**Zero residues and normalized marginals.** For the partition function, good primes with Z mod p=0 are valid CRT information and should be retained. Once exact integer Z≠0 has been established, marginal inversion can skip those primes. At most log2 |Z| additional distinct prime divisors are skipped; include this term, bounded by U, in the prime budget. If exact Z=0, normalized marginals are undefined. A routine must not search indefinitely for a nonzero residue, or report vanished pinned numerators as normalized zero marginals.

For an ORIGINAL edge-bit projector P, transform the pinned edge to N=diag(1,1/r)(C_v^T P C_w)diag(1,1/s), retaining incidence sign choices. The surrounding neutral zero-field model is invariant under global spin complement, so its numerator depends only on (N+XNX)/2=[[A,B],[B,A]], where A=(N00+N11)/2 and B=(N01+N10)/2. For background edge [[a,b],[b,a]] and exact Z≠0, the original pin marginal is

    (A/a) P_Ising(equal) + (B/b) P_Ising(unequal).

It is not generally a recovered CP-spin marginal. Standard Pfaffian derivatives may compute all the equal/unequal weights. This identity was derived for coordination; marginal reconstruction was not implemented in this folder.

The certificate may retain exact local quadratic identities/nonzero norms, prime exclusions, output bound and modular gauge/orientation/Pfaffian/CRT data. It needs no expanded characteristic-zero field. This certifies a representation and value on C; it does not claim an implemented end-to-end rational recognizer in this folder.

## 8. Executed discriminating calculation

`finite_field_gate_check.py` independently implements the modular stage through actual Fisher triangles, clockwise-odd face constraints, reference-matching sign and Pfaffian elimination. It does not call the parent's programs. Dense integer tensors are generated with determinant-one integer paired edge gauges; those matrices are then discarded, and CP is reconstructed from tensor entries. Independent integer truth enumerates the original parity network's cycle space.

The local even-parity entries are (1,1,1,d_v), with distinct prime d_v. Their hyperdeterminant square classes are the independent d_v, preserved by the integer gauges. Thus the characteristic-zero degrees below are exact, not numeric guesses.

| vertices | edges | char-0 CP compositum degree | p | nonsquare local discriminants mod p | exact integer Z | modular FKT residue |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 18 | 4,096 | 79 | 5 | 14,090,784 | 28 |
| 12 | 18 | 4,096 | 83 | 4 | 14,090,784 | 40 |
| 20 | 30 | 1,048,576 | 79 | 12 | 132,097,687,055,872 | 32 |
| 20 | 30 | 1,048,576 | 83 | 9 | 132,097,687,055,872 | 43 |

All dense tensor entries are nonzero. The entire modular pipeline used field degree TWO. Independent deterministic CP-label flips preserved the answers. Replacing one vertex by odd parity passed local balance and gave global sign -1 / exact zero. Truth enumeration used cycle dimensions 7 and 11.

An additional fixed-seed check used arbitrary dense integer tensor PAIRS, with no parity promise or hidden-gauge generator: 200 valid pairs out of 209 attempts at p=79 had all edge roots in F_(p²); 143 roots lay outside F_p. Nine attempts were excluded for singular pencils or zero CP edge entries. This supports section 5's arithmetic lemma; the proof is not the sample count.

`FINITE_FIELD_CHECK.json` records these results. The recorded run took approximately 0.30 seconds, only for these small checks and with no performance comparison. Exact characteristic-zero admission and full CRT are proved constructively above, but are not implemented/executed in this folder. The generated cases establish neither novel recognition power nor advantage.

## Matched comparison and final judgement

The fair ordinary operation on IDENTICAL dense input tensors is exact heterogeneous gauge discovery followed by the same ordinary Fisher/FKT, fields and CRT accounting. Supplied-gauge FKT alone omits the input-recognition interface. Conversely, factorization, admission, primes and reconstruction cannot be free for the proposed route. Once acquired, the representation is contracted by exactly the established comparator; there is no new contraction advantage.

The substantive completed internal mathematical audit supports the criterion and polynomial-bit construction at this exact scope. The feared global-field barrier is resolved constructively. Historical priority, a new computational class, practical speedup, useful non-generated workloads and physical capability remain UNKNOWN / NOT_ACHIEVED.
