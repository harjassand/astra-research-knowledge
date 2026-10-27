# Targeted prior mechanisms: dense affine and quadratic structure

27 October 2026. Focused continuation of `work_output_agent/PHASE_PRIOR_ART.md`.
This note distinguishes established algorithms, transfers derived here, and the
remaining missing step. No simulator or asymptotic algorithm was executed in
this literature task. This is not a comprehensive priority search.

## 1. Verdict and the strongest relevant prior competitor

I found no primary result in this search giving exact worst-case
`poly(L) 2^{o(n)}` evaluation of an arbitrary dense quadratic background plus
`n^{1+o(1)}` fixed-locality non-Clifford phases, without additional structure.
Existing algorithms already handle dense affine descriptions while charging
the original number of inputs. Thus the comparison must not suggest that a
wire-count circuit-to-CNF encoding is the only previous route.

**Lokshtanov–Paturi–Tamaki–Williams–Yu (SODA 2017), Theorems 1.2 and 1.4.**
For systems over `F_2` supplied as sums of products of affine linear forms,
Theorem 1.4 exactly counts in deterministic time

    poly(u) 2^{n - n/(1100 log(s/n) + O(1))},

where `s` is the total number of product gates and `u` the description size.
The proof branches on products of independent affine forms, either removing
a product or increasing the rank of accumulated linear constraints. Its
branches partition the solution set, so the counting version is exact.
For fixed degree, their Theorem 1.2 already gives a constant exponential
saving `2^{(1-c_k)n+o(n)}` with `c_k>0`, after polynomial-size expansion.

Primary paper, actually read:
<https://people.csail.mit.edu/rrw/polyEqSoda2017Submit.pdf>

**Application calculated here.** A dense binary quadratic polynomial has the
raw representation

    Q(x) = c + sum_i x_i (a_i + sum_{j>i} B_ij x_j).

Thus `Q` plus `m` sparse nonlinear monomials is a sum of at most `n+m`
products, with description length `O(n^2 + k m)` field symbols. Fixed-degree
dense affine preprocessing also expands in polynomial time. These algorithms
do not give the sought subexponential exponent, but they are materially
stronger competitors than naive truth-table enumeration or gate-variable
encoding. When comparing fixed-degree instances, do not label
`2^{n-o(n)}` as the best prior bound merely because that is the value of
Theorem 1.4 for growing `s/n`.

**Dense cubic baseline.** Dalzell–Harrow–Koh–La Placa, Quantum 4, 264 (2020),
Appendix B specializes the deterministic polynomial method to cubic binary
gap computation, obtaining the familiar approximately `2^{0.9965 n}` bound.
The construction forms a modular polynomial representation of partial sums
and evaluates it on all remaining assignments; it uses exponentially large
coefficient tables. This is a useful established comparator for dense cubic
instances, not an original-input subexponential theorem.

Primary paper, Appendix B read selectively:
<https://quantum-journal.org/papers/q-2020-05-11-264/pdf/>

## 2. Exactly what dense affine preprocessing already permits

The following identities are elementary transfers, not novelty claims. Let
`A: F_2^n -> F_2^r` have rank `rho`, and let `b in F_2^r`. Compute a full-row-rank
matrix `H` with kernel `im(A)` by Gaussian elimination; write `c=r-rho`.
For any phase function `F` on `r` feature bits,

    sum_x F(Ax+b)
      = 2^{n-rho} sum_{z: Hz=Hb} F(z)
      = 2^{n-rho-c} sum_{u in F_2^c} (-1)^{u.Hb}
          sum_{z in F_2^r} F(z) (-1)^{(H^T u).z}.

Each inner binary character splits into unary phase factors, regardless of
the density of `H`. All divisions can be deferred until the integer numerator
is reconstructed. Hence, when `r=O(n)`, `c=o(n)`, and the local phase list has
the required support, this gives `2^{c+o(n)}` time from the phase theorem.
A single square invertible affine map costs no enumeration at all.

Raw XOR/NOT programs can be compiled into `A,b` by propagating actual affine
coefficient vectors, at polynomial cost in their description and `n`.
For many dependent output features, the codimension `c`, not just rank,
is the obstruction in this particular character-enumeration implementation.
Acquiring a sparse basis of the dual code can avoid enumerating its whole
dimension; that is the parent construction being audited separately, not a
claim established by this note.

## 3. Affine-quadratic closure is real, but not arbitrary additive closure

The usable algebraic object is

    lambda * 1[A z = b] * i^{c + sum_j alpha_j z_j
                                  + 2 sum_{j<l} beta_jl z_j z_l}.

**Geerts et al., arXiv:2610.00547v1, Section 7** gives a modern explicit
formulation: affine support and a quadratic phase modulo four, with even
cross coefficients, are closed under product and Boolean marginalization.
The nonscalar representation has `O((|z|+1)^2)` bits; scalars are stored exactly
in `Z[i,2^{-1/2}]`. Section 7 explicitly says this represented class is not
closed under arbitrary pointwise addition. Its closure recovers ordinary
Clifford simulation without a width bound.

Primary text, Section 7 read:
<https://arxiv.org/html/2610.00547v1>

**Older constructive machinery.** De Beaudrap–Herbert, Quantum 6, 803 (2022),
maintains quadratic-form expansions
`C sum_{x in F_2^r} i^{x^T Q x} |Ax+b>` with computed affine maps and phase
matrices. Their stabilizer-operation algorithms take `O(n r) <= O(n^2)`
time per operation and exploit sparse or low-rank representations when
present. Global phase is tracked, which matters when the result is later
combined with non-Clifford amplitudes.

Primary paper, representation and complexity sections read:
<https://arxiv.org/pdf/2109.08629>

**Transfer limit.** The replacement algorithm manufactures rational linear
summaries and then conditions on their ordinary integer values. Those fibers
are generally not affine spaces over `F_2`. Further, truncated factors
`1+V(G-1)` and their sums of coefficient polynomials are not necessarily
affine-quadratic factors. Therefore it is invalid to replace the source's
independent-group summation step by “Gaussian elimination” without proving
a new closure/evaluation lemma for these actual objects.

One small diagnostic illustrates the mismatch. For
`Q(x,y)=x^T C y`, the sign matrix `((-1)^{Q(x,y)})_{x,y}` has real rank
`2^{rank_F2(C)}`. Gaussian elimination can sum this matrix globally, but it
does not factor it into a small number of independent group functions when
`C` has large cross rank. This is an obstruction to that factorization route,
not a lower bound on all algorithms.

## 4. Concrete payoff of a successful dense quadratic extension

Here is a precise transfer from standard magic-state injection and the
affine-quadratic closure above. It makes the outstanding target consequential.

Consider a raw circuit with any number of Clifford gates and `t` diagonal
gates of fixed locality at most `k`, with phases among fixed `2^b`-th roots.
Let `r` be the sum of those diagonal-gate localities, so `r <= k t`.
For a diagonal gate `D`, introduce the resource `D|+^k>`, apply CNOTs from
the data bits to the resource bits, and postselect the resource bits to zero.
On data basis vector `|x>`, this gadget acts as `2^{-k/2}D|x>`.
This fixed-postselection identity needs no assumption about feedforward
corrections or the Clifford hierarchy level.

After all replacements the remaining circuit `C` is Clifford. For fixed
original computational-basis boundaries `x,y`, define

    K(z) = <y,0^r| C |x,z>.

Contract the Clifford part symbolically to acquire

    K(z) = lambda 1[A z=b] i^{q(z)}.

If the resource phases are `zeta^{F(z)}`, with `F` a sum of `t` local terms
on disjoint resource blocks, the original amplitude is exactly

    <y|U|x> = lambda sum_{A z=b} i^{q(z)} zeta^{F(z)}.

The injection multiplier `2^{r/2}` cancels the `2^{-r/2}` from the resource
state coefficients. Keep `lambda` separately in its exact scalar encoding.
With `c=rank(A)<=r`, Fourier-expand the affine indicator:

    <y|U|x> = lambda 2^{-c}
      sum_{z in F_2^r, u in F_2^c}
         i^{q(z)} zeta^{F(z)} (-1)^{u.(Az+b)}.

This has at most `2kt` summation bits, `t` disjoint fixed-locality resource
phases, and an arbitrary dense Clifford quadratic background. Enlarge the
fixed root order to include fourth roots if necessary. Compilation and exact
scalar bookkeeping are polynomial in the full raw circuit size. The inner
unnormalized root sum has cyclotomic coordinates bounded by `2^{r+c}`;
normalization does not demand precision proportional to the original
Clifford gate count. Requested marginals use the doubled resource variables
and the same Clifford projector contraction, still `O(t)` bits.

Consequently a uniform dense-background counter in `2^{o(N)}` for `N` bits
would imply exact `poly(L) 2^{o(t)}` simulation of these Clifford+diagonal
circuits, independent of their Clifford/Hadamard count. For real Clifford
plus CCZ gates, the irreducible test is already an arbitrary dense binary
quadratic phase plus `t` disjoint cubic phases. This payoff is conditional
on the missing counter; the injection reduction itself is established
machinery, not a new solver.

Primary ancestry: Bravyi et al., Quantum 3, 181 (2019), Section 2.3.1 describes
fixed-postselection magic-state injection and the normalization issue; its
Section 2.3.2 also gives sums over Clifford operators for diagonal gates.
<https://arxiv.org/pdf/1808.00128>

## 5. What existing non-Clifford algorithms establish

Exact stabilizer decompositions remove Clifford gate count from the
exponential parameter long before the present work. They supply an essential
competitor, not the desired `2^{o(t)}` guarantee for linear `t`.

Qassim–Pashayan–Gosset, Quantum 5, 606 (2021), gives exact decompositions
of `t` copies of the T magic state using `O(2^{0.3963t})` stabilizer terms.
One exact output amplitude can be obtained by summing the exact Clifford
amplitudes of those terms. The paper's quoted fast output-probability routine
uses a relative-error norm estimator; do not silently relabel it exact.
Exact marginal probabilities can instead require pairwise terms unless
additional structure is used.
<https://quantum-journal.org/papers/q-2021-12-20-606/>

Kissinger–van de Wetering–Vilmart, TQC 2022, gives partial and graphical
stabilizer decompositions with a comparable exponent and concrete ZX
simplification. It supplies a constructive exact decomposition and strong
practical competitor for selected circuits. Their favorable hidden-shift
experiments do not establish a worst-case `2^{o(n)}` theorem when the T count
is proportional to `n`.
<https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2022.5>

For `t=o(n)`, an exponential-in-`t` simulator already gives original-qubit
subexponential time. For `t=Theta(n)`, its general guarantee remains
exponential in `n`. For `t=n^{1+o(1)}`, it need not even improve on
state-vector enumeration. Conversely it handles arbitrarily long Clifford
segments, so it is not uniformly dominated by the current bounded-Hadamard
phase theorem.

## 6. Already-solved structured dense-background cases and next tests

**Independent cubic spaces.** Bläser–Gullans–Hangleiter–Liu–Qiao,
arXiv:2609.39918v1, Lemma 40/Theorem 41, evaluates a cubic phase with arbitrary
quadratic background in `O(2^{n-h} n^3)` when an `h`-dimensional independent
space is supplied: enumerate its complementary coordinates and perform
quadratic Gauss sums. Theorem 67 acquires planted spaces of dimension
`h>(1/2+epsilon)n` in `O(h n^3 2^{n-h})`, with high probability under the
specified planted distribution. Neither statement manufactures a suitable
space for every sparse-cubic input.

The same paper announces, as Theorem 37, expected
`2^{0.552n+O(sqrt(n))}` exact counting for general cubic gaps, but attributes
the underlying result to a work in progress. No proof of that announced
bound was located or reviewed here; it should be labeled accordingly.
<https://arxiv.org/html/2609.39918v1>

**A computable low-rank transfer.** Let the polar matrix of a binary quadratic
`Q` have rank `r_Q`. Gaussian elimination constructs the Walsh support of
`(-1)^Q`: an affine subspace of size `2^{r_Q}`, with computable signed
coefficients of magnitude `2^{-r_Q/2}` after normalized Fourier transform.
Thus a dense `Q` with `r_Q=o(n)` costs `2^{r_Q}` calls to the local phase
counter, each with at most `n` extra unary characters. This is a valid
`2^{r_Q+o(n)}` hybrid and uses a rank actually computed from the input.
It is a routine consequence of quadratic Fourier analysis and the new phase
counter, not a solution at full quadratic rank.

**Best focused target.** Seek a representation that preserves affine-quadratic
closure while processing the sparse non-Clifford factors, or a manufactured
common summary whose fibers admit exact quadratic weighted summation. It must
charge the cost of finding that summary and the dimensions of all remaining
character spaces. A dense quadratic normal form alone moves the difficulty
into dense affine arguments of the nonlinear factors; arbitrary additive
mixtures of affine-quadratic factors can again have exponential size.

The concrete falsification family is the dense quadratic background with
disjoint cubic blocks from Section 4. Any proposed general Gaussian repair
should first solve that family without enumerating `Theta(t)` independent
resource choices or assuming a favorable basis/width.
