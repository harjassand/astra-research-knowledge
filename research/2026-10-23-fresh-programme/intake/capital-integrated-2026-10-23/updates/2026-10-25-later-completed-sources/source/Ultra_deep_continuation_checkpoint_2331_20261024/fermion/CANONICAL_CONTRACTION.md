# Fixed-number contraction with holes in a projected pairing state

24 October 2026. Owned continuation; internal proof candidate. Old files remain
unchanged. This constructs a deterministic canonical-norm evaluator on an explicit
small-bridge class, including nonbipartite pairing graphs. It does not yet supply
a Born sampler, state preparation, a material ground state, or a practical win.

## 1. Question, resources and scope of the claimed operation

There are `n=2m` physical sites with local states empty/up/down; double occupancy
is excluded exactly. Supply the entire symmetric zero-diagonal rational-complex
pairing matrix `F`, its entry bit lengths, and an integer pair count `k`. Define

```
|psi_k(F)> = P_(N=2k) P_no-double exp(sum_ij F_ij c†_i↑ c†_j↓)|vac>,
c_k = ||psi_k(F)||²
    = sum_(I intersection J empty, |I|=|J|=k) |det F[I,J]|²,
Z(z) = sum_(k=0)^m c_k z^k.
```

For real `z>=0`, `Z(z)` is the squared norm with pair amplitudes multiplied by
`sqrt(z)`. At complex `z` it is the analytic polynomial continuation; it is NOT
the Hilbert norm of a complex-fugacity state (that norm uses `|z|`).

Fix a rational density margin `0<delta<1/2` and fixed degree bounds. The promised
native class has a perfect matching `M0` of unit reference amplitudes and weak
off-reference entries `E`, with maximum weak physical degree `Delta`, contracted
dimer-graph degree `D`, and a certified rational envelope `lambda>=max|E_ij|`.
Use exact squared comparisons or upward rational modulus bounds. The explicit
smallness test below is conservative. It applies on high-treewidth graphs and
does not assume a small exact separator. For `delta*m<=k<=(1-delta)*m`, the
operation returns a relative-`epsilon` approximation to `c_k`, with all matrix,
matching, local enumeration and precision costs paid. A failed certificate returns
`UNKNOWN`. Degree and density margin are fixed parameters, not uncharged growing
inputs in a uniform FPTAS claim.

The reference can be acquired by maximum-product perfect matching, as in the old
proof: in a unit-reference/weak-edge promise with `lambda<1`, any different perfect
matching loses at least two reference edges and has product at most `lambda²`.
Approximate log magnitudes and ordinary weighted perfect matching therefore find
the reference under a robust promise; verify its actual native entries afterward.
The theorem can equivalently accept a supplied matching and verify it. An ordinary
competitor receives exactly the same matching and all decomposition information.

Common reference magnitude `g` can be divided out of all of `F`: in a fixed-`k`
sector this changes only the scalar `g^k`. Reference phases of unit modulus can
be removed by known local occupation-phase rotations, transforming observables
accordingly. Arbitrary diagonal congruence `DFD` is NOT a free state gauge with
holes: it multiplies a configuration on occupied set `O` by `product_(i in O) D_i`.
Recovering the original state after such a transformation requires the inverse
local occupation filters. The old full-occupancy gauge certificate must not be
silently reused as a native small-bridge certificate here.

## 2. Exact partial-matching gas, with interference signs

For unordered `ij`, use the even unnormalized singlet creator
`B†_ij=c†_i↑ c†_j↓-c†_i↓ c†_j↑`, with fixed canonical fermionic order. Hard projection
turns the exponential into a sum over PARTIAL matchings `M`, with coefficient
`product_(e in M) F_e`. A matching with `q` bonds has squared norm `2^q`.

In the norm, a bra/ket pair `M,N` contributes only when their occupied site sets
are equal. They then have the same pair number `q`, and their contribution to
the polynomial has factor `z^q`. Contract the reference dimers. Connected
components of the union of the weak edges selected in either copy are the active
components. An inactive reference dimer is either empty in both copies, or has
the reference singlet in both copies. Its total contribution is

```
b(z)=1+2z.
```

For a connected dimer set `C`, `s=|C|>=2`, let `A_C(z)` be the exact finite sum
over local partial-matching pairs with the same occupied sites and connected
weak union exactly `C`. Include their weak edge weights, conjugate bra weights,
fugacity `z^q`, and signed local valence-bond overlap. Reference-edge weights are
one. Then

```
Z(z) = sum_(pairwise disjoint collections Gamma)
       [product_(C in Gamma) A_C(z)] b(z)^(m-sum_(C in Gamma)|C|).      (1)
```

There is no positivity assertion about `A_C`. Compatibility means disjoint
supports, NOT nonadjacency: adjacent components may coexist if their joining edge
is not selected. Formula (1) is a polynomial identity even when `b(z)=0`.
Only where `b(z)!=0`, put `w_C(z)=A_C(z)/b(z)^s` and `Xi(z)=Z(z)/b(z)^m`.

The all-size weak-power step is as follows. If one site of an active reference
dimer is occupied, it is weak-paired in BOTH copies. If both sites are occupied
and one copy is weak-paired, both sites of that copy must be weak-paired. Thus
every active dimer has at least two weak incidences across the pair `M,N`.
The total number of weak edges, counted across both copies, is at least `s`.

A partial matching on `2s` sites has at most `(Delta+2)^(2s)` recursive descriptions:
the first available site is empty, reference-paired, or weak-paired. An ordered
pair has at most `(Delta+2)^(4s)` descriptions. Its overlap is at most `2^s` in
magnitude by Cauchy, and its fugacity degree is at most `s`. Therefore, if
`lambda<=1` and `|z|<=R`,

```
|A_C(z)| <= a^s,
a = 2 (Delta+2)^4 max(1,R) lambda.                                (2)
```

This deliberately crude bound avoids an unproved row/orientation improvement
for partially occupied dimers. Local `A_C` are computed by actual partial
matching enumeration and signed overlaps in `exp(O_Delta(s))` exact arithmetic.
No smaller canonical or conditional partition oracle is used.

## 3. Quantitative sector certificate

Let

```
r_lo=delta/[2(2-delta)],  r_hi=(2-delta)/(2delta),
s0=1/8,   R=2 r_hi,
x=8 D 3^5 a,    S=x²/[4D(1-x)].
```

For `D=0` use the exact binomial product instead. For `D>=1` require the rational
tests

```
lambda<=1,  x<=1/4,
S<=delta/4096,
(D+1)a<=delta/16.                                                 (3)
```

They define a nonempty, size-independent native class at fixed degree/density
margin. The constants are not claimed useful for a specific material.

For `r in [r_lo,r_hi]` and `|theta|<=pi/2`, consider the logarithmic neighborhood
of radius `s0` around `log r+i theta`. It has `|z|<=R` and `|1+2z|>=1/2`: the
angular range is less than `3pi/4`, which stays a fixed distance from the negative
reference zero. Thus `|w_C|<=(2a)^s` uniformly there.

The number of connected sets of `s` dimers through a fixed vertex is at most
`(4D)^(s-1)`. KP with `a_KP(C)=|C|`, tail tilt `4|C|`, and `e^5<3^5` is certified
by `x` above. In particular, the per-vertex tilted polymer sum is at most `S`.
The standard rooted-cluster bound gives a single analytic branch

```
Q(t)=log Xi(e^t),      |Q(t)|<=m S,
|Q^(j)(t)|<= j! m S/s0^j                                      (4)
```

at the inner points. To see the first inequality, root every nonempty cluster at
a vertex in one of its polymers; the KP cluster sum rooted through a polymer is
bounded by that polymer's absolute activity times `exp(|C|)`. Summing through
vertices overcounts, hence bounds the absolute log sum by `mS`. The derivative
bound is Cauchy on the stated larger domain, not differentiation of unrelated
pointwise estimates. The same bound for the truncated tail is
`m exp(-4L)` before Cauchy, where `L` is total polymer-size cutoff.
Equivalently, add a zero-weight singleton test polymer at a chosen vertex with
KP parameter `a_test=S`. Its incompatibility sum is at most `S`; it contributes
zero to every other KP test. The standard KP cluster bound through this dummy
then gives the per-vertex log bound `S` directly, including the size tilt.

The familiar connected-support/Mobius implementation from DIMER_CONTRACTION
applies with these actual rational functions `w_C(z)`: enumerate connected supports
and their matching-pair polynomials, compute the disjoint gas on each small
support, and take its formal logarithm. Repeated polymers are included. Work is
`m exp(O_D,Delta(L))` with polynomial bit overhead. This algorithmic KP layer is
established machinery, in particular Mann--Minko, not a new cluster theorem.

## 4. A global bound through the reference zero

We do NOT evaluate `log Xi` at `z=-1/2`, and do not infer a full-circle KP bound
from (3). Use the unnormalized identity (1). For fixed union `U` of `s` active
vertices, encode each connected component by its canonical rooted spanning tree.
Each vertex chooses a neighbor as parent or a root symbol, so at most `(D+1)^s`
forests encode the possible component collections. Consequently (2) implies

```
|Z(z)| <= sum_s binom(m,s) [(D+1)a]^s |b(z)|^(m-s)
       = (|b(z)|+(D+1)a)^m,                  |z|<=R.               (5)
```

This bound also holds exactly at a zero of the reference polynomial. It is an
absolute bound, not an assertion that all norm configurations are positive.

For positive `r` in the bracket, set `p0=2r/(1+2r)`. Then
`p0 in [delta/2,1-delta/2]` and `p0(1-p0)>=delta/4`.
On `pi/2<=|theta|<=pi`,

```
|b(r e^(i theta))|/b(r)
 <= sqrt(1-2p0(1-p0)) <= 1-delta/4.
```

Real-positive KP gives `Z(r)>=b(r)^m exp(-mS)`. Combining with (3),(5) gives the
uniform characteristic bound

```
|Z(r e^(i theta))|/Z(r) <= exp(-delta m/8)           (outer arc).   (6)
```

For example the ratio before raising to `m` is at most
`(1-3delta/16) exp(S)<=1-delta/8`, using `S<=delta/4096`.
This is the repair of the negative-real reference-zero issue at density `1/2`.

## 5. Use the stronger acquired scalar-charge theorem

An initially contemplated local central-limit proof is unnecessary for the
basic conditioning bound. The older Astra N89 source proves real-negative roots
for the scalar pair-count polynomial for ALL opposite-spin `F` with repulsive
onsite weights, including the hard endpoint. Its hard-endpoint specialization
has a short direct proof, reconstructed here rather than assumed from a card.

For a general `n by n` opposite-spin `F`, form the `2n by 2n` Hermitian chiral matrix

```
H = [[0,2F],[2F*,0]],
S_A = U_A union V_(A^c),    |S_A|=n.
```

Expansion of the characteristic polynomial and Cauchy--Binet give

```
2^(-n) sum_(A subset[n]) det(x I_n-H[S_A])
 = sum_k (-1)^k c_k x^(n-2k)
 = x^n Z(-1/x²).                                                  (7)
```

Indeed a disjoint pair of row/column sets `I,J` of size `k` occurs with probability
`2^(-2k)`; the `2F` minor contributes `4^k |det F[I,J]|²`. Nondisjoint sets never
occur. These factors cancel exactly. Hermitian `det(diag(y)-H)` is real stable.
The operator `product_i(partial_Ui+partial_Vi)` followed by diagonal specialization
gives the left side of (7), up to `2^(-n)`, and preserves stability. For a positive
direction derivative, introduce one extra variable by shifting the two selected
coordinates together, differentiate, then specialize it to zero. The leading
coefficient is positive so the resulting polynomial is not zero. Thus it has
only real roots; (7) and `c_0=1` imply every zero of `Z` is strictly negative.

The primary closure facts are Borcea--Branden, arXiv:math/0607755v5,
Propositions 2.2 and 2.4, personally reopened with their proofs. The particular
canonical identity and its algorithmic limits are already retained in N89;
no new priority is claimed for them. Scalar charge real-rootedness is NOT
multivariate physical-occupation stability or a hard-configuration sampler.

For positive `r`, `Pr_r(K=j)=c_j r^j/Z(r)` is therefore Poisson-binomial and
unimodal. Its variance is at most `m/4` in our physical `2m`-site setting. If its
mean is within `1/4` of the desired integer `k`, the elementary N89 lemma gives

```
Pr_r(K=k) >= a_m := 3/[4(m+1)^2].                                (8)
```

For completeness: if a mode lies left of `k`, the entire tail `j>=k` has masses
at most `p(k)`, so `E K<=k-1+(m-k+1)^2 p(k)`. Use the lower mean bound. If a mode
lies right, apply the symmetric argument to `j<=k`. If `k` is a mode its mass is
at least `1/(m+1)`. This proves (8) without supplying the polynomial's roots.

The real-rootedness theorem does NOT itself count hard configurations. N89's
generic counting import covers only weaker onsite filters; its separate
bipartite hard transfer is a strong incumbent on that overlap. We do not relabel
those older results as our new canonical anti-concentration theorem.

## 6. A paid deterministic canonical coefficient algorithm

First acquire a positive rational tilt `r` with `|E_r K-k|<=1/4`.
From (4), `mu(r)=m p0(r)+Q'(log r)` and the endpoint mean error is at most
`mS/s0`, much smaller than the density margin. The two bracket endpoints therefore
straddle `k`. Differentiated truncated clusters compute `mu` to absolute error
`1/32` with cutoff `O(log m)` and paid multiprecision. Monotonicity is exact,
and `dmu/dr=Var(K)/r<=m/(4 r_lo)` by the scalar-charge theorem. Rational bisection
therefore obtains the stated accuracy in `O(log m)` evaluations: stop when an
estimate is within `1/8` of `k`, or when the bracket width is at most
`r_lo/(16m)`. Update the bracket only when the estimated sign is certified.
All tilt bit lengths are polynomial; no exact mean, root or sampling oracle is
assumed.

Let `N=m+1`, `theta_j=2pi j/N`, represented in `[-pi,pi]`. Because the polynomial
degree is at most `m`, the following finite Fourier inversion is EXACT:

```
c_k r^k/Z(r) = (1/N) sum_(j=0)^(N-1)
              [Z(r e^(i theta_j))/Z(r)] e^(-i k theta_j).          (9)
```

For the inner nodes use the complex sector-KP evaluator with relative error
`eta=epsilon a_m/64`, including the real normalizer. Since `Z` has nonnegative
coefficients, `|Z(r e^(i theta))|<=Z(r)` exactly. These relative errors give an
absolute error `O(eta)` in (9). Division by the DERIVED lower bound (8) is safe.
All outer nodes are replaced by zero, with total absolute error at most (6).

Use the Fourier branch only if the explicit rational upper bound
`2^(-floor(delta m/8))` is at most `epsilon a_m/64`. Otherwise evaluate the whole
canonical norm exactly by enumerating at most `3^(2m)=9^m` empty/up/down strings
and the appropriate determinant minors. A failed Fourier-branch test implies

```
m <= O_delta(log(m+1)+log(1/epsilon)+1)
  <= O_delta(log(1/epsilon)+1).
```

The second implication absorbs the logarithm into half the linear term outside
a fixed constant range. Hence that exact fallback is ALSO polynomial in
`1/epsilon`, at fixed density margin. It is essential when requesting finer
accuracy than the outer-arc bound permits. We do not silently discard a fixed
exponential error for arbitrarily small `epsilon`.

Approximate roots of unity and their phases with absolute error `O(eta/m)`.
Positivity gives `|z Z'(z)|<=m Z(r)` on the circle, so this is a sufficient
finite-precision prescription. One may evaluate normalized logarithms and the
known `b(z)^m` factor to avoid numerical overflow. Entries, exponentials and
roots of unity need polynomial bit precision including `O(m)` bits where an
intermediate relative value is exponentially small. Standard certified complex
arithmetic supplies this; no exact transcendental oracle is part of the input.
Finally multiply the acquired point probability by `Z(r)/r^k`. Error constants
above have ample slack for total relative error `epsilon` (or use epsilon/4
internally). If a reference magnitude was divided out, restore `|g|^(2k)`.

At fixed degree, density margin and certificate margin, `L=O(log(m/eta))`, so
the number of actual local activity computations and bit operations is polynomial
in explicit input length, `m` and `1/epsilon`. This is a deterministic FPTAS for
the promised canonical norm. Its exponent/constants depend on the fixed degree
and density margin. The small-bridge and native-matrix acquisition costs are
explicit inputs/verification, not experimental acquisition.

## 7. Physical meaning and the next unclosed observable gate

At `E=0`, the normalized fixed-`k` reference is the Dicke state of singlet pairs.
For normalized local pair operators `b_a†=|singlet>_a<empty|`, distinct dimers obey

```
<b_a† b_b> = k(m-k)/[m(m-1)],    <b_a>=0.
```

Thus fixed number already allows distant number-conserving pair coherence. This
reference is solved exactly by ordinary binomial/hypergeometric DP. Our nonzero
`E` class retains hard no-double occupancy and signed fermionic interference,
on potentially high-width nonbipartite graphs, with a certified canonical norm.
This is not a proof of superconducting stiffness, a parent-Hamiltonian ground
state, a material phase, or stability of the reference ODLRO under `E`.

The next useful operation is charge-conserving local/hopping/pair-transfer
observables, including two distant pair insertions. Their canonical numerators
must be contracted with marked defects and the same coefficient error control.
An invertible norm filter supported on a constant number of dimers is a plausible
route, but must retain its nonlocal marked block, complex-fugacity reference
zeros and outer-arc bound. A local-equivalence-of-ensembles slogan does not prove
uniform distant pair coherence. No sampler or general observable theorem is
claimed from the norm result alone.

## 8. Equally informed comparison and actual exposure

* Mann--Minko, PRX Quantum 5, 010305 (2024), arXiv:2306.08974, already supplies the
  abstract signed/complex-polymer approximation layer. A conventional implementation
  may use our exact same representation, charge theorem, decomposition and contour.
  This is an acquired state-specific interface, not a new generic KP algorithm.
* N89's whole governing `canonical_bcs_audit.txt` was read after the initial owned
  mechanism. Its scalar stability/near-mean lemma materially simplifies the proof
  above. Its real-rootedness is stronger and more general than the initially
  contemplated perturbative local CLT. N63/dossiers and the N89 bipartite/monomial
  routes delimit existing conditional canonical preparation methods; no import is
  applied outside its hard/soft and support assumptions.
* Pulvirenti--Tsagkarogiannis, arXiv:1105.1022v4, treats canonical cluster expansions
  for stable classical pair potentials at high temperature/low density. Its
  introduction and model/theorem setup were read. It is an equally informed
  foundational comparator, not a theorem directly about our signed projected
  fermion norm. Scola arXiv:2005.13931 was found as a canonical Ising/CLT comparator;
  its HTML failed retrieval, so its full proof was not used.
* Yang et al., PRB 107, 125128 (2023), arXiv:2208.04566v2, constructs projected
  d-wave fPEPS and evaluates thermodynamic-limit observables via tensor methods.
  Its introduction and method setup were read. Edegger et al., cond-mat/0506120,
  treats Gutzwiller fugacity/particle number with approximation and VMC. These
  precedents own the physical state class and fugacity idea. Our tiny-bridge
  certificate is not asserted to cover their cuprate-regime pair matrices.

Actual development inputs include root's outer-arc suggestion and four already
exposed Luna supports; the owner independently reconstructed the matching,
forest, stability and coefficient steps. Their checks are bounded corroboration.
The corpus remains pinned read-only at e606bfc587c76bdcae8b8fa3ec33e721efa2fbac.
Priority, external proof review, practical advantage and physical validation are
UNKNOWN. The old gauge, full-occupancy contraction and failed phase estimator
are protected, with no edits to their files.
