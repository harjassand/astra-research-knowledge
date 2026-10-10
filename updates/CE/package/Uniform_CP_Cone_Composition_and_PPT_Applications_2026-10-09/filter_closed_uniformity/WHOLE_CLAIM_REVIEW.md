# Focused adversarial review: Kraus-word bootstrap and full uniformization

9 October 2026. Scope: one independent check, first of the rank-one Kraus-word
bootstrap and then, by explicit extension of the assignment, of Sections 4–7
of `FULL_SEMIALGEBRAIC_MAPPING_CONE_UNIFORMIZATION.md`.

## Verdict

**The proof passes this focused review under its exact stated hypotheses.**
No invalid norm comparison, loss of complete positivity, wrong zero-set
inclusion, circular induction, or hidden map-dependent final exponent was
found. In particular, the cyclic-corner direct-sum step and the use of the
full-Kraus-rank quantum Wielandt exponent are valid. The subsequently
requested check of the PPT corollary also passes; Section 9 verifies its
pointwise input using the published HRSF theorem and dimension induction.

This is a mathematical proof check, not formal verification or a priority
assessment. It does not weaken the premise: every map of the closed convex
semialgebraic CP mapping cone, including non-TP filtered maps, must have a
finite EB power. Section 9 establishes that premise for the PPT cone by
the specified published-input chain. No claims in Park's Section 5 were
reviewed or used. The conservative constants in the main proof suffice;
the improvements recorded below are optional.

## 1. Kraus lift, including singular reference Choi matrices

Let `N=d^2`, and pad a rank-one Kraus factor `W0` to `r=d^4` columns. The
Caratheodory bound is justified in the real affine space of trace-d Hermitian
`N`-by-`N` matrices, of dimension `d^4-1`: a separable Choi matrix is a convex
combination of at most `d^4` pure product projectors after normalization.

In the polar factorization `W0=sqrt(J0)V`, one has `VV*=P`, where `P` is the
support of `J0`. If `k=rank(J0)`, the complement of the initial space of `V`
has dimension `r-k`, at least `N-k`. Thus `V` extends to `U` with `UU*=I_N`,
while `sqrt(J0)U=W0`. Consequently

    W=sqrt(J)U,   WW*=J,
    ||W-W0||_F^2=||sqrt(J)-sqrt(J0)||_F^2.

No invertibility of `J0` or continuous choice of `U` is required.

For completeness, the needed square-root inequality has a short finite-
dimensional proof. Put `A=sqrt(J)`, `B=sqrt(J0)`, `R=A-B`, `Q=A+B`, and
diagonalize the Hermitian `R`, with eigenvalues `lambda_i`. Since `Q>=+R`
and `Q>=-R`, `Q_ii>=|lambda_i|`. Since
`A^2-B^2=(RQ+QR)/2`, trace-norm domination of the absolute diagonal gives

    ||J-J0||_1 >= sum_i |lambda_i| Q_ii
                 >= sum_i lambda_i^2 = ||R||_F^2.

Finally `||J-J0||_1<=sqrt(N)||J-J0||_F=d g`. This verifies equation (1).
The inequality is the alpha=1/2 case of the Powers–Størmer trace inequality;
its established form is also recorded in the primary research article
[Aggarwal–Singh, arXiv:1606.03913](https://arxiv.org/abs/1606.03913).

The stated bound `b<=2d sqrt(g)` is valid. An optional sharper bound follows
from `s2(K_i)<=||K_i-K_i^0||_op` and `s1(K_i)<=||K_i||_F`:

    b=sum_i s1(K_i)s2(K_i)
      <=sqrt(d)||W-W0||_F<=d sqrt(g).

The proof never needs this improvement.

## 2. Rank-one truncation and the positive EB approximation

For the top singular truncation `L` of `A`, write

    a=s1(A)^2,   t=sum_(j>=2) sj(A)^2.

The vectorizations of `L` and `A-L` are orthogonal, so the squared
Frobenius norm of the projector difference is exactly `2at+t^2`. Since
`t<=(d-1)s2(A)^2` and `s2(A)^2<=a`, this is at most
`(d^2-1)s1(A)^2s2(A)^2`. Thus the constant `sqrt(d^2-1)` is correct and
sharp: equality holds for `A=I_d`.

The exterior-square representation obeys `wedge^2(AB)=(wedge^2 A)(wedge^2 B)`.
Consequently summing the wordwise bound yields

    ||J(Psi^n-E_n)||_F <=sqrt(d^2-1)b^n.

Here `E_n(X)=sum_w L_w X L_w*` is genuinely CP and EB. There is no signed
decomposition being mistaken for a CP map. The exponential number of Kraus
words is harmless for an existence proof, and no semialgebraic selection of
their singular vectors is needed.

An additional useful fact is `L_w*L_w<=A_w*A_w`. Therefore
`E_n*(I)<=I`: the chosen approximation is trace-nonincreasing. The main
proof does not rely on this extra fact.

## 3. Positivity margin, squaring, and the conservative threshold

Reshuffling the Choi matrix gives the superoperator matrix without changing
its Frobenius norm. For `Delta=T-E`, this proves

    ||Delta(rho)||_op<=delta ||rho||_F<=delta,
    ||Delta*(I)||_op<=sqrt(d)delta.

Thus `delta<=f/2` gives `E(rho)>=fI/2`, while
`delta<=1/(2sqrt(d))` gives `E*(I)>=I/2`. Both conditions follow from the
main threshold because `f<=1/d` for a TP map.

For a Holevo decomposition with trace-one preparations,

    E(X)=sum_a tr(F_a X)sigma_a,

the differences in

    E^2 >=_EB (f/2)[X -> tr(E*(I)X)I] >=_EB (f/4)D_I

have explicit positive measure-and-prepare decompositions. This is EB
order, not merely positivity order or CP order.

The induced Hilbert–Schmidt norm of a CPTP map is at most `sqrt(d)`.
It is enough to prove this on Hermitian matrices by trace-norm contraction.
For `X=A+iB` with `A,B` Hermitian, both input and output Frobenius norm
squares split into the sums for `A` and `B`, so complexification does not
cost an extra constant. The identity

    T^2-E^2=T(T-E)+(T-E)E

therefore gives exactly the stated error bound
`(2sqrt(d)+delta)delta`.

The elementary separable ball of radius `1/d^2` is valid: expand a Hermitian
perturbation in orthonormal Hermitian product bases, use
`sum |z_ab|<=d^2||Z||_F`, and express each
`I tensor I +/- H_a tensor G_b` as the average of two positive product
matrices. Thus

    delta <= f/[4d^2(2sqrt(d)+1)]

indeed proves `T^2` EB. All normalization factors match the unnormalized
Choi convention `J(D_I)=I tensor I`.

Optional: because the particular `E_n` is trace-nonincreasing, its induced
Hilbert–Schmidt norm is also at most `sqrt(d)`. This improves the composition
bound to `2sqrt(d)delta`, but changing constants is unnecessary.

## 4. Compressed cones and invariant corners

The compressed cone is closed because it is the **preimage** of `C` under
the continuous linear embedding

    theta -> Ad_V theta Ad_(V*).

It is semialgebraic and convex by the same description. CP pre/postfilters
on `M_r` lift to CP filters on `M_d`, proving the mapping-cone property.
Its equality with the compression image follows from filtering by the
projection `VV*`; it is not an appeal to the false general claim that a
linear image of a closed cone is closed. Powers telescope through the
embedding, so pointwise eventual EB passes to the compressed cone.

Changing the isometry `V` by an ambient unitary gives the same identified
cone. Consequently the smaller-dimensional exponents depend on the rank
and induced cone, not on the continuously varying invariant subspace.

For invariant `P`, every Kraus operator is upper triangular. On an input
in `P M Q`, the output is supported in `P M`, and its `P M Q` component is
`T(X)=sum A_i X C_i*`. The `P M P` component cannot later feed a cross
component. Hence the cross component of the nth power is exactly `T^n`.

If `T` is nonzero, product unitaries span the entire operator space on
`Hom(QH,PH)`. Nondegeneracy of the trace pairing supplies a block-unitary
postfilter for which the new cross operator has nonzero trace, hence a
nonzero eigenvalue. Its powers cannot vanish. On the other hand, an EB map
with invariant `P` has zero cross transfer: invariance forces each positive
Holevo summand either to have output supported on `P` or effect supported
on `Q`. Thus the filtered map would violate the pointwise premise.

The resulting `T=0` is exactly orthogonality of the Kraus-index coefficient
spaces of the `A_i` and `C_i`. A unitary Kraus rotation therefore yields
`Phi=F+G`, with `F` output-supported on `P`, `G` input-supported on `Q`,
and `GF=0`. The identities and orientations in
`EXACT_BOUNDARY_REDUCTION.md` are correct. For
`n=N_p+N_q+1`, every surviving word `F^(n-j)G^j` contains either
`F^(N_p+1)` or `G^(N_q+1)`, so every summand is EB. No membership of `F`
or `G` in `C` is assumed.

## 5. Cyclic decomposition really yields a direct sum

A primary source is [Carbone–Jencova, arXiv:1905.00857](https://arxiv.org/pdf/1905.00857),
Definition 1, Proposition 5, and Corollary 2, pages 9–10. Applied to the
irreducible unital adjoint `Phi*`, these give nonzero orthogonal cyclic
projections summing to identity, with `Phi*(P_j)=P_(j-1)`. Irreducibility
of the finite-dimensional TP map supplies a faithful invariant state.
The number `h` of projections is at most `d`; if the map is nonprimitive,
`h>=2`.

Here is the required translation into Kraus support, so there is no
Heisenberg/Schrodinger ambiguity. If `x` lies in `P_(j-1)H`, then

    sum_i ||P_j K_i x||^2
        =<x,Phi*(P_j)x>=||x||^2=sum_i ||K_i x||^2.

The nonnegative omitted squared norms must each vanish. Therefore every
`K_i` maps `P_(j-1)H` into `P_jH`. Every `h`-letter Kraus word is consequently
block diagonal in these projections.

Put `Psi=Phi^h`. For `i!=j`, block-diagonality implies

    Psi(P_i X P_j)=P_i Psi(P_i X P_j) P_j.

The invariant-corner lemma applied to `P_i` makes its cross transfer into
`P_i M (I-P_i)` zero. Since the displayed output has **no other possible
support**, its entire value is zero. Diagonal corner inputs remain in
their own corner. Thus `Psi` is precisely the direct sum of its diagonal
compressed maps; there is no hidden diagonal output from a cross input.

Each corner has dimension below `d`. The same lower-dimensional inductive
exponent `N_*` therefore gives `Phi^(h N_*)` EB. Along with the reducible
bound, `N0=max(2N_*+1,dN_*)` works for all nonprimitive TP members. A maximum,
rather than a common multiple of periods, is sufficient because every
later power of an EB map remains EB.

## 6. Full Choi rank, the global zero set, and exponent quantifiers

The relevant primary statement is [Sanz et al., arXiv:0909.5347v2](https://arxiv.org/pdf/0909.5347):
Theorem 1 bounds the **full Kraus-span index** by
`i(A)<=(d^2-r+1)d^2<=d^4`. Proposition 3 identifies finite `i(A)` with
primitivity; the definition in Section II says the Kraus span remains full
at all later lengths. Choi rank equals the dimension of that span. Thus
for `q=d^4`, `lambda_min J(Phi^q)>0` exactly for primitive CPTP maps.
Proposition 1 alone would not provide the needed equivalence; Proposition
3 belongs in the citation.

The parameter set `K=C intersect TP` is compact because its Choi matrices
are positive with trace `d`; it is closed and semialgebraic. Both

    f(Phi)=lambda_min J(Phi^q),
    h(Phi)=2d sqrt(g(Phi^N0))

are continuous and semialgebraic. The previously proved boundary theorem
gives precisely `f^(-1)(0) subset h^(-1)(0)`, the correct direction for
the compact semialgebraic Lojasiewicz inequality. It yields **one pair**
`A,alpha>0` on all of `K`, with `h<=A f^alpha`. This is stronger than and
does not follow merely from separate curvewise estimates.

The zero-set form of that inequality is, for example, also stated in
[Ferrarotti et al., Ann. Scuola Norm. Sup. Pisa (2002), Lemma 2.1](https://www.numdam.org/article/ASNSP_2002_5_1_1_1_0.pdf).
Their variant has weaker continuity hypotheses; the continuous compact
case used here is the standard special case after scaling.

One now chooses `n` **after** `A,alpha,N0,q` are fixed, requiring
`alpha n>1` and `N0 n>=q`. Then one chooses a single small `epsilon>0`
so that `sqrt(d^2-1) A^n epsilon^(alpha n-1)<=1/kappa_d`.
These choices do not depend on `Phi`.

The output margin for `Phi^(N0 n)` is the same `f(Phi)`, because its final
`q` steps act on a density matrix and
`Phi^q>=_CP f(Phi)D_I`. There is no additional `n`-dependent loss of the
positivity margin. The Kraus-word lemma therefore proves a common power
in the whole small-f region, including the zero set via `N0`.

On `f>=epsilon`, `Psi=Phi^q` obeys
`epsilon D_I<=_CP Psi<=_CP dD_I`. The faithful-word bound has the claimed
constant: its condition `q_noise^m beta^2 d^4<=alpha^2`, with
`alpha=epsilon`, `beta=d`, becomes
`(1-epsilon/d)^m d^6<=epsilon^2`. A single finite `m` exists. Taking the
maximum of the two resulting EB exponents gives one exponent on all of
`K`. No pointwise-to-uniform compactness assertion is used without the
quantitative neighborhood argument.

## 7. Non-TP extension and absence of circularity

A nonzero cone contains `D_I`: choose a positive input `X0` and positive
functional `F` for which `c=tr(F Phi(X0))>0`. The CP maps
`B(X)=tr(X)X0` and `A(Y)=tr(FY)I` satisfy `A Phi B=cD_I`. Rescale in the
cone. Thus `Phi_epsilon=Phi+epsilon D_I` lies in `C` and has strictly
positive Choi matrix.

The required faithful left eigenmatrix can also be obtained without a
strong Perron-theory formulation. On the compact convex density set,

    X -> Phi_epsilon*(X)/tr(Phi_epsilon*(X))

is continuous, with positive denominator and strictly positive output.
A fixed point gives `Y_epsilon>0` and
`Phi_epsilon*(Y_epsilon)=r_epsilon Y_epsilon`, `r_epsilon>0`.
The stated filtered similarity then has adjoint fixing `I`, and is CPTP.

The filters telescope in its powers. Invertible CP filters and positive
scaling preserve EB in both directions, so its common TP exponent also
works for `Phi_epsilon`. The same exponent is independent of both `Phi`
and `epsilon`; letting `epsilon` tend to zero works by closedness of the
EB cone. The filters may become ill-conditioned in this limit; no uniform
bound on them is needed.

The induction is noncircular: in dimension `d`, the boundary argument
uses the **entire** already-proved theorem only in dimensions below `d`.
It then proves the TP theorem in dimension `d`, and only afterward extends
it to arbitrary maps in that same dimension.

## 8. Small numerical stress test and limitations

The deterministic companion script is `verify_kraus_word_bootstrap.py`;
results are in `kraus_word_bootstrap_verification.json`. It ran locally
using NumPy, with seed `930173` and absolute tolerance `2e-11`:

- 20 channel/reference cases in dimensions 2, 3, and 4
- 54 word-depth checks and 7,218 explicitly formed Kraus words
- Both singular and full-rank EB reference Choi matrices
- Maximum resolved error/bound ratio about `0.866027`
- Maximum resolved composition-error ratio about `0.331193`
- Exact truncation-constant saturation for identity matrices in dimensions
  2, 3, 4, and 7
- Two successful conservative squaring certificates for primitive,
  initially non-EB qubit channels

The last family is
`Psi=(1-epsilon-epsilon^2)Dephase+epsilon Id+epsilon^2 D_I/2`.
Its one-step Choi partial transpose has eigenvalue
`epsilon^2/2-epsilon<0`, and it is primitive because of the depolarizing
term. At `epsilon=0.01`, `n=3`, the measured approximation error is about
`1.414216e-6`, below the conservative threshold `2.448541e-6`; the test
therefore checks the ingredients of the certificate for `Psi^6`.

These are known EB references, not nearest-EB optimizations. Eight bounds
fall below the absolute numerical resolution and are recorded as such;
relative ratios there are deliberately null, since subtraction roundoff
can exceed a true error of order `1e-18`. Those cases are not relative-
precision validations. The numerical test is supplementary evidence only;
the analytical arguments above establish the inequalities.

## 9. PPT corollary: published input and exact pointwise induction

This final extension of the same review checks only the dependency chain
in `PPT_POINTWISE_DEPENDENCY_CLOSURE.md`. The local source was
`private_sources/hanson_rouze_franca_v2.pdf`, arXiv:1902.08173v2 dated
3 March 2020, SHA-256
`f0025c8302f546eef29f25e4126eb2f2c146d2368fd3dbc876dc216e9b04f12a`.
The published article is [Hanson–Rouze–Stilck Franca, Annales Henri Poincare
21 (2020), 1517–1571](https://link.springer.com/article/10.1007/s00023-020-00906-4).

Theorem 3.14, on page 34 of the supplied preprint, applies to a CP map
with strictly positive left and right eigenmatrices at its spectral
radius and says that the PPT condition implies eventual EB. Proposition
3.13, on pages 32–34, verifies that the left-eigenmatrix similarity is
TP, has a faithful invariant state, preserves PPT and EB, and telescopes
under iteration. Theorem 3.10 is the faithful-channel input. The quoted
dependency is therefore the arbitrary-CP theorem, not a substitution of
a unital-only result.

For an irreducible CP map with positive spectral radius, the required
eigenmatrices are faithful. Indeed positive-map Perron theory gives
nonzero positive semidefinite eigenmatrices at that radius; the support
of such an eigenmatrix is invariant. Irreducibility forces full support.
The adjoint is irreducible as well: a common invariant subspace for all
adjoint Kraus operators would give a common invariant orthogonal
complement for the original Kraus operators. This proves the same
faithfulness for the left eigenmatrix. Thus the published theorem applies
to every irreducible PPT CP map with positive radius.

For the reducible case, the zero-product-vector argument can be made
unambiguous entrywise. Choose a basis adapted to the invariant projection
`P`, put `Q=I-P`, and write `K_i=[[A_i,B_i],[0,C_i]]`. Use the unnormalized
Choi convention of the main proof and partial transpose on its input
factor. Its entries satisfy

    J(Phi)_(a p; b j)=sum_i K_i[a,p] conj(K_i[b,j]),
    J(Phi)^Gamma_(a p; b j)=J(Phi)_(a j; b p).

For basis indices `q in Q`, `p in P`, the diagonal entry
`J(Phi)^Gamma_(q p; q p)=sum_i |K_i[q,p]|^2` is zero. Since
`J(Phi)^Gamma>=0`, the corresponding row and column are zero. For
`a in P`, `j in Q`, their entries give

    0=J(Phi)^Gamma_(q p; a j)
      =sum_i C_i[q,j] conj(A_i[a,p]).

Taking complex conjugates yields every coefficient of
`T(X)=sum_i A_i X C_i*`; hence `T=0`. This proof works regardless of
partial-transpose convention after the corresponding index swap. It
does not assume trace preservation or faithfulness.

The CP split from Section 4 of this review now applies. The compressed
maps on `P` and `Q` remain PPT. Inducting only on dimension gives finite
exponents `N_P,N_Q` for these individual maps, and the positive word
expansion gives exponent `N_P+N_Q+1` for the original map. Base dimension
one is immediate. If the spectral radius is zero, Cayley–Hamilton on the
`d^2`-dimensional matrix space gives `Phi^(d^2)=0`, which is EB. These
cases exhaust arbitrary PPT CP maps. No uniform exponent was imported
into this pointwise induction.

Finally, the PPT cone meets every hypothesis of the main theorem: it is
closed, convex and semialgebraic by the two Choi positivity inequalities.
It is a CP mapping cone because for CP `A,B`,

    transpose compose A compose Phi compose B
      =(transpose compose A compose transpose)
         compose (transpose compose Phi) compose B

is CP, and `transpose compose A compose transpose` has conjugated Kraus
operators. Rectangular compression preserves PPT by the same local-
filter argument. Thus the checked main theorem yields a common finite
`N(d)` for all PPT CP maps on `M_d`, including non-TP maps.

**Scope conclusion:** this review now covers the stated PPT corollary
through HRSF Theorem 3.14 and the explicit corner induction. It does not
review Park's Section 5, establish priority, prove `N(d)=2`, give a useful
numerical bound on `N(d)`, or prove a claim for arbitrary nonstationary
products of different PPT maps. No additional numerical work was used.

## Recommended final presentation adjustments

1. Cite Sanz et al. Proposition 3 alongside Theorem 1; keep the distinction
   between minimum-output positivity and full Choi rank explicit.
2. Include the short cyclic Kraus-support/direct-sum explanation from
   Section 5 above, rather than leaving it implicit.
3. State induction over the full non-TP theorem, and keep the whole-cone
   pointwise premise visible. For the PPT corollary, use the exact
   published-input chain checked in Section 9. No novelty conclusion is
   part of this review.

No substantive mathematical repair was required by this check.

Completion check: the main file's final revision incorporates the cyclic
support explanation, Proposition 3 citation, elementary normalization, and
self-contained separable-ball and faithful-word appendices. The later
explicitly requested PPT-corollary dependency check is completed in
Section 9 above and supersedes the original narrower scope statement.
