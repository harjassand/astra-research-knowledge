# Exact stabilizer extraction by Pauli-support span

1 November 2026. Independently derived solo construction. No external novelty
clearance, independent mathematical audit, physical-copy learning claim, or
general quantum-simulation advantage is asserted.

## The exact classical input and result

Input is a NONZERO open-boundary n-qubit MPS with Gaussian rational tensor
entries, maximum bond D, and the full exact tensor description supplied. There
is a deterministic polynomial-bit-time algorithm that returns the complete
signed Pauli stabilizer group by independent generators. It needs no magic gap,
sampling lower bound, heuristic prefix pruning, canonical form or truncation.

The proof gives O(n^2) parity contractions. A straightforward dense implementation
uses O(n^3 D^6) Gaussian-integer arithmetic operations and O(n D^4) memory, plus
polynomial GF(2) work. This can be MUCH more costly in D than the published
O(D^3) biased sampler. Polynomial exact work is not a practical-speed claim.

Clear one common denominator per tensor. This scales the whole vector by a
nonzero scalar and preserves stabilizers. The resulting Gaussian-integer input
has polynomial bit length in the original explicit input. No normalized square
roots need to be represented. Write c=||psi||^2>0 and

    f(v)=<psi|P_v|psi>,    v in F_2^(2n),

where P_v is the Hermitian tensor-product Pauli with interleaved labels (x_i,z_i).
Its coefficients are real integers, without any division by c or 2^(n/2).

## 1. Stabilizers are the annihilator of a support span

Let rho=|psi><psi|/c and W=span_F2{v:f(v)!=0}. The Pauli expansion of rho and
P_w P_v P_w=(-1)^[w,v] P_v show

    P_w rho P_w=rho  iff  [w,v]=0 for every v in W.

For this rank-one rho, the left condition is equivalent to P_w psi=+/-psi.
Hence the unsigned stabilizer space is EXACTLY W^perp under the symplectic form.
Recover each sign from f(w)/c, which must equal +/-1. Anticommuting Paulis cannot
share a nonzero eigenvector, so the recovered space is isotropic and has dimension
at most n. The rank-one hypothesis matters: the Pauli commutant of a mixed state
need not be an abelian stabilizer group.

## 2. A one-parity energy oracle recovers W

For an ordinary binary linear form u and a coordinate prefix p, suppose one can
compute exactly

    E(u,p)=sum_(v extends p, u.v=1) |f(v)|^2.

Only ONE parity condition is present. Start with the zero span S. Compute a basis
of the ordinary annihilator S^perp. For each basis vector u, test E(u,empty).
If all are zero, the support of f lies in the intersection of those hyperplanes,
which is S. Since S was built from actual nonzero coefficients, S=W and we stop.

Otherwise some test is positive. Fix successive coordinates (or quaternary Pauli
symbols), each time choosing the first extension with positive remaining energy.
The parent energy is the sum of its children's energies, so such a child exists.
At the end obtain v with f(v)!=0 and u.v=1. Since u annihilates S, v is outside S.
Adjoin v and repeat. There are at most 2n expansions and O(n^2) root parity tests.
Witness search uses polynomially many prefix queries, with no dependence on the
normalized mass of the witness. Exact positivity is the supplied computational
operation; this does NOT give a gap-free physical sampling algorithm.

## 3. The oracle is acquired from the actual MPS

If the input tensors are A_i^0,A_i^1, define

    B_i^P = sum_(s,t) (P)_(s,t) conjugate(A_i^s) tensor A_i^t.

Then f(v)=B_1^(P_v1)...B_n^(P_vn), with bond at most D^2. This Pauli-MPS
construction is established prior work, not a new ingredient claimed here.

For a chosen u let b_i(P)=u_i.v_i. Build suffix Gram environments

    R_(n+1,0)=1,   R_(n+1,1)=0,
    R_(i,p)=sum_P B_i^P R_(i+1,p XOR b_i(P)) (B_i^P)^dagger.

At a prefix, its accumulated row ell and parity b give the remaining energy as
ell R_(i,1 XOR b) ell^dagger. The scalar is nonnegative and vanishes exactly
when every allowed amplitude vanishes. These environments implement a width-two
parity automaton; their bond never grows with the number of queries. Constructing
all suffixes costs O(nD^6), and one full witness search from them costs only
O(nD^4) further work. It does not normalize a rare conditional distribution.

All entries involve products and sums of at most O(n) local tensor factors per
term, with at most exponentially many terms whose logarithmic count is polynomial.
Their integer bit length is O(poly(input length,n,log D)). Queries reuse the
original tensors. Thus the arithmetic bound also gives polynomial BIT complexity
on this explicit exact input, rather than a unit-cost real-RAM claim.

## 4. A short independently checkable completeness certificate

The output contains k independent signed stabilizers and 2n-k independent labels
whose Pauli coefficients are nonzero. Ordinary single-Pauli MPS contractions check
these facts. The nonzero labels force the full stabilizer dimension to be at most
k by Section 1, while the k verified generators force it to be at least k. This
certifies completeness without replaying any squared-energy zero test. The signs
of the returned Hermitian generators make each one a +1 stabilizer of psi.

## 5. A concrete failure permitted by prefix-generator pruning

Consider

    psi = [5|00>+(3+4i)|11>]/sqrt(50).

Its complete stabilizer is generated by ZZ. The first-qubit Pauli-energy
marginals are all exactly 1/4 and its Schmidt rank there is two. At the first
step of Liu--Clark Appendix F Algorithm 6, every I,X,Y,Z prefix meets the displayed
threshold. Stable descending sorting with the displayed I,X,Y,Z order keeps X,Y
as a maximal independent prefix set and drops Z. The next step only extends the
retained individual prefixes (with the identity understood). ZZ is no longer a
candidate. At the final threshold all nonstabilizers are rejected, leaving no
nonidentity generator.

This is a failure of a literal permitted tie resolution of the displayed
algorithm, not a claim about an unseen implementation. The paper does not specify
its ties. For any fixed choice of two local independent Paulis in this equal-weight
situation, a local Clifford rotation can place the unique exact stabilizer on the
omitted third Pauli. Keeping only a generating set of the UNKNOWN valid prefix
subset needs an additional completeness argument; ordinary linear dependence of
the larger retained candidate set does not supply it. The paper itself explicitly
discusses such a loss possibility and appeals to numerical benchmarks.

## 6. Matched primary comparison and actual controls

* Lami--Collura, arXiv:2401.16481 / PRL 133,010602: biased Pauli sampling and a
  finite retained-prefix resource. A useful efficient numerical method; the read
  argument does not supply this exact all-input guarantee.
* Tarabunga et al., arXiv:2401.16498v2: the Pauli-MPS above and iterative powering
  to isolate stabilizers. Appendix I.2 keeps a magic-gap dependence; intermediate
  exact bond can grow, and the claimed small maximum bond is reported empirically,
  not proved (their note 77). The present construction uses the ORIGINAL Pauli-MPS
  and no powering, compression or limiting fixed point.
* Liu--Clark, arXiv:2412.17209 / PRResearch 8,023116 (2026), Appendix F: a deterministic
  prefix procedure, with the unresolved generator-loss possibility quoted above.
  This comparison distinguishes procedural determinism from all-input completeness.
* Standard finite-dimensional linear algebra and weighted-automaton identity tests
  may offer other ways to acquire the same existential support queries. Historical
  novelty is NOT established by the comparison with these three papers.

The executable implementation passed independent dense checks of ALL 6,308 Pauli
words over the named small inputs, including complex signs and generic MPS. It
recovers n-1 generators for phase-GHZ examples at n=16,32,64 (bond two), with compact
completeness certificates. An exact two-qubit input with a 1,025-bit amplitude
has a needed parity mass below 2^-2040 and still takes five root contractions.
The latter is an explicit classical-arithmetic test, not a physical advantage.

Code: `work/mechanism_selection_20261101/exact_stabilizer.py` and
`exact_stabilizer_controls.py`. Bound results: `exact_stabilizer_controls.json`.
No general low-stabilizer-rank simulation theorem or physical fault-tolerance
claim follows. This remains the materially different constructive contender.

Primary sources read:

* https://arxiv.org/abs/2401.16481
* https://arxiv.org/html/2401.16498v2
* https://arxiv.org/abs/2412.17209
* https://journals.aps.org/prresearch/abstract/10.1103/ybnf-rjw8
