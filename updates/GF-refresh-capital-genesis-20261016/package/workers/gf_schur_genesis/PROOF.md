# Exact separation and generator screening for unequal product Schur kernels

16 October 2026. Independent derivation from the supplied exact two-gap formula. This document establishes conditional mathematical consequences of that formula. Historical novelty, independent external verification, and physical capability are UNKNOWN.

The source worktree is read-only, pinned by the parent task to `f937563cbc5d2249b8e0dd96bcbd3b8f78eb85c6`. Inputs are the supplied originals, especially `general_schur_refresh_audit/PROOF.md`, `HOMOGENEOUS_SYMMETRY.md`, and `refresh_robustness_packet/refresh_robustness_packet/resolution_gate/RESULT.md`. No peer worker outputs were used to derive Sections 1--6. The parent's independently discovered singleton calculation was subsequently disclosed; a comparison is recorded separately.

## 1. Frozen optimization and phase/sign audit

Let `alpha=pq`, `h=sqrt(pq(1-p)(1-q))`, `Q=p+q-pq`. Label the full sectors by subsets `S` of `[m]`, with empty label good. In the real nonnegative product case,

```
C_ST = product_{a in S symmetric_difference T} eta_a,   0<=eta_a<=1.
c_S=C_S,empty,  B=C_bad,bad.
f(z)=2h Re(c^*z)-alpha z^*Bz,  ||z||_1<=1,
F=Q+max f.
```

For independent complex binary factors `[[1,conjugate(xi_a)],[xi_a,1]]`, put `eta_a=|xi_a|`, choose phases `d_S=product_{a in S} xi_a/eta_a` (an arbitrary unit phase at zeros), and `D=diag(d_S)`. Then `C_xi=D C_eta D^*`. Its blocks satisfy `c_xi=D_bad c_eta`, `B_xi=D_bad B_eta D_bad^*`; substituting `z=D_bad x` preserves the objective and complex l1 constraint. Thus the **value** depends only on the magnitudes. This includes negative real multipliers and does not replace a complex kernel by its real part.

For the real kernel, write `z=x+iy`. The objective equals `2h c^T x-alpha x^TBx-alpha y^TBy`. Replacing `z` by `x` increases it weakly and does not increase l1. Hence the value algorithm below may use real atoms `+e_S,-e_S`, while the sparse separation theorem also handles complex coefficients.

If `alpha=0` or `h=0`, the optimum improvement is zero. If all multipliers are zero, `c=0`, again giving `F=Q`. If some multiplier has magnitude one, a singleton has `c_S=1`. Positivity gives `B>=cc^*`, so the exact improvement is

```
max_{0<=r<=1} (2hr-alpha r^2),
```

attained by that singleton with amplitude `r=min(1,h/alpha)` when `alpha>0`. This handles a singular boundary without using an inverse.

For arbitrary `v`, the supplied tangent certificate is

```
g(v)=hc-alpha Bv,
max f <= alpha v^*Bv + 2 ||g(v)||_infinity.
```

For feasible `v`, the certified value interval has width

```
Delta(v)=2||g(v)||_infinity - 2 Re(g(v)^*v) >= 0.       (1)
```

All infinity norms in this document exclude the good label unless explicitly marked otherwise. Omitting that exclusion gives a different and usually looser certificate.

## 2. Active-generator screening: an exact global identity

Partition the generators into `A` and `E` (retained and excluded). Let `v` be supported only on labels `(T_A,empty_E)` with `T_A` nonempty. Define the retained residual including its good coordinate:

```
g^A_s = h C^A_s,empty - alpha sum_T v_T C^A_s,T,
d_A = g^A_empty = h-alpha sum_T c^A_T v_T,
M_A = max_{s nonempty in A}|g^A_s|,
mu_E = max_{a in E} eta_a,  with mu_E=0 if E is empty.
```

Tensor factorization gives, for every label,

```
g_(s_A,s_E)= (product_{a in s_E} eta_a) g^A_s_A.
```

Since all nonempty excluded products are at most `mu_E`, and an excluded singleton attains `mu_E`,

```
||g_bad_full||_infinity = max(M_A, mu_E |d_A|).        (2)
```

This identity is exact for arbitrary complex coefficients `v`, includes zero and unit multipliers, and assumes the full binary label set. If sectors are absent, using the right side remains an upper certificate but equality can fail.

Consequently, an exact retained optimizer satisfying the l1 KKT conditions with multiplier `lambda>=0` remains an exact full optimizer **if and only if**

```
mu_E |d_A| <= lambda.                                (3)
```

Here the retained KKT conditions are `|g^A_s|<=lambda`, `g^A_s=lambda sign(v_s)` on real nonzero coordinates, and `lambda(||v||_1-1)=0` (complex signs have the corresponding phases). If `||v||_1=1`, its full certificate gap is exactly

```
2 max(0, mu_E |d_A|-lambda).
```

For an interior retained optimum `lambda=0`, the gap is `2mu_E|d_A|`. An interior optimum generally changes when even small additional multipliers are introduced; screening is not inferred from smallness alone.

For necessity, if the condition fails, take the sector with no retained bits and a single excluded bit attaining mu_E. Its gradient modulus exceeds lambda. The feasible direction from v toward the l1 atom aligned with that gradient has strictly positive objective derivative. Thus the zero-extended retained optimizer is no longer globally optimal. This does not rule out another sparse optimizer.

This gives an operation: optimize only a chosen small generator set, then certify the *full* model by its retained residual and the largest excluded multiplier. Full inter-bad-sector enumeration or tomography is unnecessary under the product-channel premise. A generic explicit retained calculation costs exponentially in `|A|`, not in `m`; the excluded maximum costs O(m). Section 4 supplies a different exact separation method when the retained candidate is sparse.

## 3. Arbitrarily many unequal generators with an exact constrained three-sector optimizer

Take

```
p=q=10/21, alpha=100/441, h=110/441, t=h/alpha=11/10,
eta_1=4/5, eta_2=3/4.
```

On the labels `1,2,12`, let

```
c=(4/5,3/4,3/5),
B=[[1,3/5,3/4],[3/5,1,4/5],[3/4,4/5,1]],
v=(19/34,36/85,-3/170).
```

Then `||v||_1=1`, and direct rational multiplication yields

```
t c-Bv = (273/3400) (1,1,-1),
t-c^Tv=147/425.
```

Thus its retained KKT conditions hold with `lambda=alpha*(273/3400)`. It is the unique retained optimizer because the two-generator C, and hence B, are positive definite. The negative pair coefficient is nonzero; a singleton-only optimizer cannot attain this value.

By (2)--(3), **any number** of additional independent generators with

```
0<=eta_a<= (273/3400)/(147/425) = 91/392,
```

leave this exact full optimizer and value unchanged. Complex or signed extra multipliers are allowed after the phase gauge, with the same magnitude condition. No equality of the additional multipliers is required. The full optimum remains in the constrained regime because already

```
t[(1+4/5)(1+3/4)-1]=473/200 > 1.
```

The value is

```
F=Q+alpha[t c^Tv+273/3400]=7763/8330=1109/1190.
```

This is a global infinite family, not an extrapolation from finite examples. The bounded receipt uses 64 distinct positive magnitudes: `4/5,3/4`, followed by `j/300` for `j=1,...,62`; their maximum `31/150` lies below `91/392`. It computes the full tangent norm without constructing any of the `2^64-1` bad-coordinate arrays. Tests at and immediately beyond the threshold check exact equality and exact failure of this candidate's certificate. Failure beyond the threshold concerns this candidate, not the existence of another tractable optimizer.

Under the unchanged full-joint/privacy/commutation/ordering and causal-tester prerequisites of the supplied coordinate-product theorem, n coordinates in this family therefore have endpoint-all-bad probability at most `(1109/1190)^n`. The bound is uniformly sharp over adequate unrestricted finite equality-witness models, not for every prescribed overlapping projector family. Screening any number of the permitted extra generators does not change this constant. This is an endpoint product consequence, not a syndrome-history completion or a memory-lifetime theorem.

## 4. Exact sparse separation with arbitrary unequal multipliers

Let `v` have N distinct nonzero support labels `T_1,...,T_N`; coefficients can be complex. For each generator a form its support-bit pattern

```
b(a)=(1_{a in T_1},...,1_{a in T_N}) in {0,1}^N.
```

Partition the generator positions into the nonempty pattern classes `A_b`. Let g be their number, so `g<=min(m,2^N)`. This grouping does **not** require equal multipliers and is **not** permutation averaging of the objective.

First assume all eta are strictly positive. Set

```
E_b=product_{a in A_b} eta_a,
x_b(S)=product_{a in S intersect A_b} eta_a.
```

For a general sector S,

```
c_S=product_b x_b,
C_S,T_l= product_{b:b_l=0} x_b * product_{b:b_l=1} E_b/x_b.
```

Holding the other group variables fixed, the residual is `A x_b+B/x_b`, with possibly complex constants A,B. With `u=log x_b`,

```
|A exp(u)+B exp(-u)|^2
=|A|^2 exp(2u)+|B|^2 exp(-2u)+2 Re(A conjugate(B)),
```

which is convex in u. Therefore its maximum on an interval occurs at an endpoint. A coordinate-by-coordinate replacement proves that the maximum residual modulus over a product of such intervals is attained at a vertex.

For each group, all subset products lie in `[E_b,1]`. Both endpoints correspond to actual sectors: select all or none of its generators. But using only these endpoints and removing the all-none vertex is **not sufficient**, because the unconstrained maximum can occur at the excluded good label.

To enforce a bad label, anchor one group b as nonempty. Its nonempty subset products lie in

```
[E_b, mu_b],  mu_b=max_{a in A_b} eta_a,
```

whose endpoints are also attainable: select all, or a single maximum-multiplier generator. Every nonempty sector lies in at least one anchored box. Maximize on each box by its vertices. All the resulting vertices are actual nonempty sectors, so the relaxation is exact.

**Sparse separation theorem.** The full bad-coordinate residual maximum is attained among these sectors:

1. choose every pattern class either all or none, excluding the empty sector;
2. choose one pattern class as an anchor and select only its largest-multiplier generator; choose every other class all or none.

There are at most

```
2^g-1 + g 2^(g-1)                                  (4)
```

candidates before duplicate removal. For N=0 there is one pattern class and the oracle returns the largest singleton multiplier, as it must.

**Zero/unit boundaries.** Replace `eta_a` temporarily by `eta_a+epsilon(1-eta_a)`. This makes every multiplier positive, preserves their order and a fixed chosen maximum index in each class, and tends to the original vector. The finite candidate list is then independent of epsilon. Every individual residual and its finite maximum are continuous. Taking epsilon down to zero proves the same theorem at zeros; ones are already allowed in the positive proof. The implementation evaluates the original product kernels and never divides by eta or E.

**Costs.** Patterns and bitmasks require O(mN) bit inspections. Directly evaluating every residual costs O(mN) multiplications per candidate; stored subset products and group factors can reduce this, but are not needed for the bound. Evaluate `v^*Bv` in O(mN^2) multiplications. Storage can be O(mN+N^2+g), streaming the candidates instead of storing their list. Costs depend exponentially on g, and in the worst case doubly exponentially on N. This is an exact fixed-support certificate, not a polynomial algorithm in N or an unqualified practical speedup.

For fixed N, it is polynomial in m and does not construct an exponential sector representation. Unequal generator parameters do not destroy this reduction. Its controlling structure is the pattern of a sparse candidate, rather than symmetry of the physical channel.

## 5. A certified approximation construction for every unequal kernel

After the phase gauge, restrict to real v and use Frank--Wolfe on the real l1 ball. At any iterate the exact linear oracle is `s=sign(g_S)e_S`, where S maximizes `|g_S|`; Section 4 computes it from the support. The certificate gap is precisely (1). Both objective and certificate use sparse products.

The following elementary iteration bound is included to specify the precision dependence; it does not turn the construction into a practical generic solver. Let `0<epsilon<alpha`; for epsilon at least alpha use the supplied O(m) resolution bracket. Start at v=0 and run K open-loop updates with `gamma_k=2/(k+2)`, k starting at zero. Each update adds at most one support label.

Because B is a unit-diagonal Gram matrix, `||x||_B<=||x||_1` and thus `||s-v||_B<=2`. Concavity gives

```
f(v+gamma(s-v))=f(v)+gamma Delta(v)-alpha gamma^2 ||s-v||_B^2
              >=f(v)+gamma Delta(v)-4alpha gamma^2.        (5)
```

Let e_k=max f-f(v_k). Since `Delta>=e`, (5) implies

```
e_(k+1) <= (1-gamma_k)e_k+4alpha gamma_k^2.
```

After the first full step, `e_1<=alpha`: `max f<=2h mu`, while that atom's objective is `2h mu-alpha`. Induction with the displayed recurrence proves

```
e_k<=16alpha/(k+2), k>=1.
```

Run `K=ceil(32alpha/epsilon)` such updates. The unobserved primal error is now at most epsilon/2. Continue, checking the exact gap before each update. If it exceeds epsilon, take `gamma=epsilon/(8alpha)`. Equation (5) shows objective improvement at least `epsilon^2/(16alpha)`. More than `8alpha/epsilon` such improvements would exceed the remaining error. Therefore a certificate gap at most epsilon is found after at most

```
ceil(32alpha/epsilon)+floor(8alpha/epsilon)+2          (6)
```

oracle calls/updates, up to the harmless convention of counting the final gap check. The support size is bounded by the same number. Exact line search or fully corrective optimization can improve iterates, but the proof needs neither and assumes no solver success flag.

Combining (4) and (6) is an explicit deterministic approximation construction with arithmetic cost

```
f(alpha/epsilon) * polynomial(m),
```

where a very large possible f grows doubly exponentially in alpha/epsilon. This is fixed-parameter tractability with respect to requested relative-to-alpha resolution in an arithmetic model, **not an FPTAS** and not an efficient general algorithm at tight precision. The supplied width-alpha bracket remains preferable when it already resolves the decision. Sparse instances and the exact screen (2) can be much cheaper than this worst-case bound.

For rational magnitudes, rational p,q, and rational step sizes, all iterates are rational; h lies in a single fixed quadratic extension. Exact comparisons can be made there, and product numerator/denominator lengths and iterate bit growth must be charged. The bounded tests choose p=q, so h is rational and use only Python Fraction. No polynomial bit-cost claim is made for arbitrary unspecified real or complex inputs. Certified interval evaluations can replace exact algebraic comparisons, with their error added to the gap and their bit costs stated.

## 6. Relation to established machinery and physical costs

The tangent bound and Frank--Wolfe method are established convex-optimization tools, not inventions claimed here. Jaggi (2013), Section 2 and Theorems 1--2, gives general sparse primal/dual certificate convergence; Section 5 supplies its own sufficient bound. Safe variable elimination using l1 dual/KKT inequalities is also established; El Ghaoui--Viallon--Rabbani, Section 2.1--2.2, is a direct predecessor. The application-specific content asserted relative to the supplied packet is the product-factorized excluded-generator identity and the sparse product-kernel separation proof, which certify exponentially many omitted coordinates together. Historical priority for even these special identities is UNKNOWN.

Schur multiplier cb-norm/factorization machinery is not the requested endpoint optimizer: a unit-diagonal positive kernel defines a unital CP Schur map, whose operator/cb norm is one. That common norm does not distinguish the differing endpoint values. Davidson--Donsig, Theorem 1.1, records the classical factorization/PSD equivalences. Similarly, diagonalizing the product kernel by Walsh characters gives eigenvalues `product_a(1+/-eta_a)`, but the sector l1 ball is not invariant under that transform, and the bad-label exclusion remains. A spectrum alone does not solve the l1 problem.

Gatermann--Parrilo's established averaging theorem explains the supplied homogeneous reduction. Unequal eta generally remove its permutation invariance. Section 4 uses a different identity of sparse residuals and does not average unequal channel parameters. Generic SOS/moment hierarchies can certify polynomial inequalities on the Boolean cube, but require a stated degree and size; their existence supplies no polynomial-in-m exact oracle for this problem. No complexity lower bound for this special product problem is claimed.

Under the already-specified full-joint product channel, synthesis can be described without listing C: for real eta, apply each commuting generator's private random conjugation `((1+eta)/2)id+((1-eta)/2)Ad_G` independently. This is an O(m) classical description and uses m independent random choices and m conditional generator operations. Its physical duration, energy, native implementation of G, private discards, baseline evolution during pulses, and persistent bath action remain model-dependent costs. m reduced coherence measurements do not certify this full-joint promise.

The mathematical equality witness for a sparse optimizer needs amplitudes on its few chosen sector labels, but implementing the allowed arbitrary good/bad-odd coupling to those amplitudes may require nonlocal or high-weight controls. Sparse classical representation does not prove a cheap physical control operation. The source full-channel/privacy/commutation/ordering assumptions and causal-product prerequisites are retained unchanged. This work proves neither syndrome-history/support completion nor a device memory theorem.

## 7. Reproduction and failure scope

`check_exact.py` uses only the Python standard library. It compares the compressed residual oracle with full bad-sector enumeration for bounded rational real and Gaussian-rational complex coefficients, including zero/unit boundaries and the good-label exclusion. It checks phase-gauge algebra, the exact screen, the three-sector family, a failing tail beyond its threshold, and exact FW certificates. `results.json` contains all deterministic cases and exact fractions.

These tests check finite identities and implementation consistency; the arbitrary-m conclusions follow from Sections 2, 4, and 5. Primary fulltexts are stored only in `acquired_excluded_from_publication`, with retrieval receipts and hashes. They are not relicensed or included in any proposed publication artifact.
