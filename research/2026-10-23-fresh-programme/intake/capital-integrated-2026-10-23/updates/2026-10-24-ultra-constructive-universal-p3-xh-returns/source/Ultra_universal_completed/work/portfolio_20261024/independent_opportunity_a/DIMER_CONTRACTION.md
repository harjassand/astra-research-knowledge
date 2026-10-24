# A computable contraction certificate for hard-projected fermionic states

24 October 2026. Internal construction and proof candidate. The general hard-core
sampler in `FIRST_CONSTRUCTION.txt` is **not** closed. The operation constructed
here evaluates a norm and constant-support spin observables in a checked
structured class. It preserves hard projection; it does not assume a smaller
partition oracle, a ground state, physical hardware or an optimal variational
ansatz. Historical priority and external acceptance are unknown.

## 1. Exact input and output

There are `n=2m` physical sites. Supply the entire symmetric, diagonal-zero
matrix `F in Q(i)^(n by n)`, with its entry bit lengths, and requested error.
Full occupancy and no double occupancy are imposed. Write

```
|psi(F)> = P_one exp(sum_ij F_ij c†_(i,up)c†_(j,down)) |vac>,
Z(F) = ||psi(F)||² = sum_(|S|=m) |det F[S,S^c]|².
```

In the physical site-ordered basis, determinant amplitudes have the known
fermionic ordering signs (which can depend on the configuration). They do not
affect this norm. Observable calculations below retain those signs explicitly.

The algorithm either returns `UNKNOWN`, or a checkable representation certificate
and a multiplicative `exp(+-epsilon)` approximation to `Z`. With that certificate,
it also gives additive-accuracy expectation values of any fixed-support Pauli
string and hence an explicit local Hamiltonian's variational energy. Reading the
whole input, matching, scaling, exact local arithmetic and precision are paid.
Zero entries are read, not inferred from a sampled support. No efficient general
sampler or complete recognition of contractible states is claimed.

## 2. Gauge invariance and acquisition of the reference

For any invertible diagonal `D`, let `F'=D F D`. Every half-filled determinant
satisfies

```
det F'[S,S^c] = (product_i D_i) det F[S,S^c].
Z(F') = |product_i D_i|² Z(F).
```

The whole physical projected state is multiplied by the same scalar: every
perfect-matching term uses each site exactly once. Thus the normalized state and
all its spin observables are unchanged. This is an exact full-occupancy identity,
not a claim about an unprojected Gaussian state or a doped state.

Suppose some diagonal gauge makes a perfect matching `M0` have edge amplitudes
one and makes the non-reference weighted row bound

```
rho = max_i sum_(j:ij notin M0) |F'_ij| < 1.
```

Then `M0` uniquely maximizes the product of edge magnitudes among perfect
matchings. An alternative matching changes at least two reference dimers, uses
at least two weak edges, and has product magnitude at most `rho² < 1` in the
gauge where `M0` has product one. Every perfect matching acquires the same factor
`product_i |D_i|` under the gauge, so the maximizing matching is the same in the
native input. In the much smaller certified regime below the objective gap is
constant. Approximate edge log weights to error at most `1/(100n)` and run an
ordinary maximum-weight **perfect** matching algorithm. Under the certificate
promise this recovers `M0`; outside it any candidate is simply checked later.
If the nonzero graph has no perfect matching, the projected state is zero.

Weighted matching is an existing polynomial-time primitive, not a proposed new
algorithm: [Edmonds 1965](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf).
Approximating logs of positive rational magnitudes to this precision has
polynomial bit cost. For complex entries one may use half the log of the rational
squared magnitude. No exact real-weight oracle is needed. The finite checker
uses exhaustive matching enumeration only on its small fixtures, rather than
claiming to implement the polynomial matching subroutine.

Here is a bounded-bit acquisition algorithm for a useful diagonal gauge after
`M0` has been found. Orient each reference pair as first/second, put
`sigma_i=+1/-1`, `a_first=1`, and `a_second=1/F_ref`. Reference edges then become
one under `diag(a)`. Parameterize the remaining scaling by

```
D_i = a_i 2^(sigma_i x_(dimer(i))).
C_ij = a_i a_j F_ij.
```

Let `Delta` be the maximum number of non-reference neighbors of a physical site.
Contract reference dimers and let `Dg` be the maximum degree of the resulting
simple graph. They are computed from the full input. `Dg=0` is an exact product
case. Otherwise set a rational target

```
rho_goal = 1/(384 Dg).
```

For each nonzero weak edge compute the integer
`w_ij=ceil(log2 |C_ij|)` by exact comparisons of squared rational magnitudes
with powers of two. Set `b=floor(log2(rho_goal/(2 Delta)))`. Solve

```
w_ij + sigma_i x_a + sigma_j x_b <= b.
```

This is an explicit difference-constraint problem on `2m` signed nodes. Introduce
potentials `u_(a,+),u_(a,-)`. For each inequality with right side `c=b-w_ij`, add

```
u_(a,sigma_i) - u_(b,-sigma_j) <= c,
u_(b,sigma_j) - u_(a,-sigma_i) <= c.
```

Bellman–Ford with a zero-weight source either exposes a negative cycle or gives
integer feasible potentials. Set `x_a=(u_(a,+)-u_(a,-))/2`. Adding the two displayed
inequalities proves that these `x_a` satisfy the original inequality. Round each
to the nearest integer. A weak edge's exponent increases by at most one, so

```
|F'_ij| <= 2^(b+1) <= rho_goal/Delta,
max_i sum_weak |F'_ij| <= rho_goal.
```

The potentials have simple-path magnitude at most
`O(m max_ij |b-w_ij|)`. Thus actual dyadic scalings and transformed rational entries
have polynomial bit length, not merely short descriptions of exponentially long
numbers. Reference amplitudes remain exactly one. The returned inequalities
and row bound can be checked directly; a failed check returns `UNKNOWN`.
For complex rational entries, magnitudes need not be rational. All algorithmic
uses of `rho` mean a verified **rational upper envelope** `rho_hat` for the row
sums: the per-edge dyadic bounds already suffice, or rounded-up square-root
intervals can be certified by squared rational comparisons. The convergence
test uses this upper envelope, not an exact rational sum of complex magnitudes.

There is also a finite-factor completeness statement. If, for this reference,
some continuous diagonal gauge has row bound at most
`rho_goal/(8 Delta)`, the constraints above are feasible: ceil-log loses less
than a factor two, the floor threshold at most another factor two, and rounding
at most a factor two. This is not a complete recognizer for arbitrary useful
gauges or projected states. The matching gap argument makes the reference
acquisition consistent on this promised robust class.

## 3. Exact signed double-matching representation

Work henceforth in a verified gauge with `F'=F0+E`, reference amplitudes one,
`E` zero on the diagonal and reference edges, bounded degree, and a computed
rational upper envelope `rho_hat>=max_i sum_weak |E_ij|`. Below `rho` denotes
this envelope whenever used in a computational convergence test.
For an unordered edge `ij`, use the unnormalized even bond creator

```
B†_ij = c†_(i,up)c†_(j,down) - c†_(i,down)c†_(j,up),  i<j.
```

Symmetry of `F'` and hard single occupancy give

```
|psi(F')> = sum_(perfect matchings M) (product_(ij in M) F'_ij) |M>,
|M> = product_(ij in M) B†_ij |vac>,       ||M||²=2^m.
```

The factor `m!` from expanding the exponential cancels its factorial. Even
creators on disjoint sites commute, but their amplitudes in a site-ordered spin
basis retain fermionic permutation signs. In particular one must not replace
all valence-bond overlaps by their magnitudes.

Expand the norm over an ordered pair of perfect matchings `M,N`. Contract each
reference dimer. Take connected components of the union of all non-reference
edges used by either matching. An inactive dimer is a common reference bond and
contributes exactly two to the overlap. Each active component `C` is a connected
set of `s=|C|>=2` reference dimers. Components are unique. Matching weights and
overlaps factor over their disjoint physical site sets, including their signs;
fermionic components have fixed even parity.

Define the explicitly computable activity

```
w(C) = sum_(M_C,N_C: connected weak support exactly C)
       conjugate(product_(e in M_C\M0) E_e)
       product_(e in N_C\M0) E_e
       <M_C|N_C>/2^|C|.
```

Then exactly

```
Z(F')/2^m = Xi = sum_(pairwise DISJOINT collections Gamma) product_(C in Gamma) w(C).
```

Compatibility is disjointness, not non-adjacency. Adjacent supports can coexist
when their connecting matrix edge is not selected. For `s` dimers, enumerate
local perfect matchings by the first unmatched site, and compute each local
overlap either by the transition loops with its sign or by explicit `2^s` bond
spin amplitudes. At fixed degree this is `exp(O_Delta(s))` arithmetic with
polynomial-size exact rational/complex data. No smaller projected partition is
queried. For a two-dimer example with weak opposite edges `lambda`,

```
Z/4 = 1-lambda²+lambda⁴.
```

Thus activities can be negative even for real symmetric inputs. This gas is not
a positive distribution from which one may sample configurations.

## 4. All-size activity bound and convergence

In one matching, let `A` be its active reference dimers. Both sites of each such
dimer use weak edges; there are exactly `|A|` weak edges. The total absolute
weight of weak perfect matchings on those `2|A|` sites is at most `rho^|A|`:
choose the first unmatched site, sum its partner weights (at most `rho`), remove
the pair, and induct. The intermediate unmatched set need not be a union of
complete dimers; the row bound still applies.

For two copies on component `C`, their active sets `A,B` satisfy `A union B=C`.
Since `|<M_C|N_C>|/2^|C|<=1`, summing the three possible active-copy statuses at
every dimer gives

```
|w(C)| <= h^|C|,                 h=2 rho+rho².
```

This is an absolute bound valid at every component size, with all interference
signs retained in the actual weight. It is stronger than counting each matching
by `(Delta+1)^s` and then using a maximum edge amplitude.

The number of connected sets of `s` dimers containing a fixed vertex is at most
`(4 Dg)^(s-1)`: encode a canonical spanning tree by a rooted plane tree and one
neighbor choice per child. With Kotecky–Preiss functions
`a(C)=|C|`, `d(C)=beta |C|`, define

```
x = 4 Dg exp(1+beta) h.
```

If `x<=1/2`, the per-vertex sum of absolute activities with the two tilts is at
most `x²/[4 Dg(1-x)]<=1/(8 Dg)<=1`. Summing over the vertices of a polymer
proves the KP inequality. Zero-weight dummy singleton polymers give the same
anchored bound for every vertex. Consequently the cluster expansion for `log Xi`
converges absolutely, `Xi!=0`, and omitting clusters of total polymer size at
least `K` costs at most

```
|log Xi - T_<K| <= m exp(-beta K).
```

This is a direct application of the established KP theorem, not a new general
cluster theorem. The native certificate is conservative but purely rational:
take integer `beta>=1` satisfying

```
4 Dg 3^(beta+1) h <= 1/2.
```

Since `e<3`, this suffices. The choice `rho_goal=1/(384 Dg)` guarantees such a
`beta=1`, because `h<=3 rho_goal` and the left side is at most `9/32`.
For smaller actual coupling the verifier can choose a larger integer beta.
Choose integer `K` with `m 2^(-beta K)<=epsilon`; this gives the desired log
error without an exact logarithm or real-precision oracle. The physical `Xi`
is positive, so its log branch is fixed by the positive reference product.

The governing algorithmic comparator is
[Mann–Minko, PRX Quantum 5, 010305 (2024)](https://arxiv.org/html/2306.08974),
which already gives KP-based approximation algorithms for quantum amplitudes,
norm-like expectations and partition functions. It may use the exact same
polymer representation; no advantage over an informed implementation of that
framework is asserted. The work here must stand on acquiring and verifying the
specific projected-state representation and its costs.

## 5. Explicit truncated computation, including repeated polymers

Computing an activity is not alone an evaluator. The following standard
connected-set implementation supplies the remaining operation. Introduce an
auxiliary `u` and give every activity the marker `w(C) u^|C|`. For a finite vertex
set `S`, let `Xi_S(u)` be its disjoint polymer partition. Form its formal log
modulo `u^K`, and set

```
ell(S;u) = sum_(T subset S) (-1)^(|S|-|T|) log Xi_T(u) mod u^K.
```

For disconnected `S` this vanishes because the restricted partition factors.
Its terms have degree at least `|S|`. Mobius inversion therefore gives

```
T_<K = sum_(connected S, |S|<K) ell(S;1).
```

For each such `S`, enumerate its connected polymer supports and local matching
pairs. Compute all restricted partition polynomials by subset dynamic
programming: at a chosen vertex it is either inactive, or belongs to one
polymer; multiply by the polynomial on the remaining vertices. Then compute
the formal log by its finite power series. This retains repeated polymers and
their incompatibility cumulants; it is not a sum of just the individual weights.

At fixed degree, the number of connected sets is `m exp(O_Dg(K))`; subset and
local-matching work are `exp(O_Delta(K))` per set. Exact arithmetic has polynomial
bit overhead in entry lengths and `K`. Thus the total work is polynomial in
the explicit input length, `m` and `1/epsilon`, for fixed degree and fixed
positive convergence margin. Exponentiating the real truncated log to a
declared rational precision gives the multiplicative norm approximation; the
known `2^m` and diagonal-gauge norm factor are included. No numerical optimum or
measured runtime advantage follows from this asymptotic statement.

## 6. Local observables without illegal conditional sampling

Direct spin-prefix conditioning can annihilate the reference singlet amplitude.
The above KP bound cannot be reused for every such conditional. Instead let
`P=P_1...P_r` act on `r` distinct sites, each `P_j` a Pauli matrix, with constant
`r`. For every sign string `s in {+-1}^r`, define an invertible local filter

```
t=1/20,  A_s=product_j(I+s_j t P_j),
Z_s=||A_s psi||²,      p=2t/(1+t²)=40/401.
```

Local spin filters preserve one particle per site, and therefore commute with
the hard projection. They factor across different physical sites. The filtered
reference norm of a dimer lies between `2(1-t)^4` and `2(1+t)^4`. Every filtered
matching overlap normalized by its corresponding filtered reference product
is bounded by

```
((1+t)/(1-t))^(4|C|) = kappa^(4|C|),  kappa=21/19.
```

The exact polymer factorization remains valid. Actual local weights are
computed by the filtered bond spin amplitudes, not a new Gaussian oracle.
Use `h_filtered=kappa^4 h`; since `kappa^4<3/2`, the base certificate above has
enough margin for integer `beta=1` in every filtered norm. For faster truncation
choose beta against this worst filtered envelope. The filtered reference product
is explicitly computed instead of retaining the unfiltered `2^m` factor.

Because the site operators commute and square to one,

```
A_s† A_s = (1+t²)^r product_j(I+s_j p P_j),
<P> = sum_s(product_j s_j) Z_s / [2^r (1+t²)^r p^r Z].
```

This is an exact finite sign average of positive norms; it never conditions on
a rare spin event. If every computed norm, including `Z`, has relative error
at most `delta<1/4`, the additive error in the reported expectation is at most

```
delta/(1-delta) [ ((1+t)²/(2t))^r + 1 ]
 = delta/(1-delta) [ (441/40)^r + 1 ].
```

Thus `delta=epsilon/[2((441/40)^r+1)]` suffices for additive epsilon. For a supplied
local Hamiltonian `H=sum_a h_a P_a`, estimate each Pauli expectation to accuracy
`epsilon_E/sum_a |h_a|`. The resulting variational-energy error is at most
`epsilon_E`, with all terms, matrix arithmetic and norm calls paid. This says
nothing about closeness of that variational energy/state to the true ground
state. No division by a possibly zero local probability has occurred.
For these calls use log-norm truncation/rounding error at most `delta/4` each;
the elementary exponential bounds then imply the required relative norm error.

## 7. Meaning, ancestry and limits

This is a closed, certificate-bearing norm/local-energy evaluator on bounded-
degree gauge-dimerizable inputs. It can apply on graphs with large treewidth;
it assumes a small verified bridge parameter rather than a small exact tensor
separator. The gauge acquisition is not a physical operation or an engineered
Gaussian bath: it is exact algebra on the supplied matrix. A classical or
quantum competitor is allowed all the same decomposition and gauge information.

The stronger direct quantum preparation competitor is
[Kang et al., arXiv:2606.06919v1](https://arxiv.org/html/2606.06919): arbitrary
Gaussian/BCS preparation followed by Gutzwiller amplitude amplification. It
already improves projection-query dependence from `1/p_success` to
`1/sqrt(p_success)`. For this fixed number sector the relevant success is
`Z(F)/det(I+F†F)`, not automatically their all-sector weight. That approach is
available outside the present certificate but may still have exponential cost.
Conversely ordinary cluster expansions, perturbation theory and tensor methods
are stronger incumbents than naive postselection in the present regime.

The small-coupling constants are conservative. This proof establishes no broad
physical phase, efficient generic projected-BCS sampling, noisy hardware
preparation, phase-diagram discovery, practical superiority, or historical
novelty. Near an entangled critical state the certificate may simply fail.
Norm/energy evaluation should not be inflated into a full sampler. The
random-Pfaffian method and its exponential variance witness remain preserved
as the earlier owned route; they are not the algorithm proved here.
