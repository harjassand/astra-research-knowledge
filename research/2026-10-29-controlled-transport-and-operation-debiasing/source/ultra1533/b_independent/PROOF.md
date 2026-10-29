# Does ramification port a modular tensor algorithm to characteristic zero?

2026-10-30. This was a constructive attempt to replace an unsuccessful
ordinary lift by a genuinely different coefficient operation. The intended
capability was repeatable acquisition of characteristic-zero bilinear
algorithms from modular discoveries. The new mechanism was to admit
ramification (for example adjoining a square root of 2), not to repeat a
plus/flip search or a mod-4 test.

The attempt reaches a decisive failure for the acquired published seed.
The result below excludes **every finite ramification with this integral
reduction**, and explains which additional infinitesimal freedom would have
been needed. It does not exclude another reduction, coefficients with bad
reduction, or a characteristic-zero rank-47 algorithm globally.

## 1. The operation that ordinary lifting leaves unpaid

Let

`F(f)=sum_(r=1)^R a_r tensor b_r tensor c_r`

and let `T` be an integer target tensor. At an exact binary decomposition
`f0`, choose its 0/1 integer representative `fbar` and define

`J=dF(f0)`, `E=(T-F(fbar))/2 mod2`.

The familiar unrestricted mod-4 lift exists exactly when `E in im J`.
This is an established Hensel step, not the proposed new operation.

To see why this alone does not settle ramification, set `pi^2=2` and write
`f=fbar+pi x+pi^2 y (mod pi^3)`. The first two conditions are

`Jx=0`, `Jy+Q(x)=E`,

where `Q(x)` is the sum over terms of

`da tensor db tensor c + da tensor b tensor dc
                          + a tensor db tensor dc`.

A nongauge vector in `ker J` could therefore change the ordinary obstruction
through `Q(x)`. Failure of the ordinary linear step is not, by itself, a
proof that this quadratic problem fails. No such shortcut is used here.

The distinction is real even for the elementary equation `x^2=2`: its
binary point `x=0` has zero Jacobian and no mod-4 lift, but has the exact
ramified lift `x=sqrt(2)`. The tangent-spanning hypothesis paid below is
what excludes this possibility for the acquired tensor point.

We acquired the WHOLE kernel and tested whether it contains any direction
beyond exact symmetries. For the native input it does not. The next lemma
shows why that removes all ramification, not just this quadratic ansatz.

## 2. Gauge-complete tangent lemma

The lemma is stated for any prime `p`, any integer polynomial system
`F(f)=T`, and a point `f0` over `F_p`. Suppose there is a finite collection
of transformations defined over `Z_(p)`, with denominators invertible near
their identity, having the following properties:

1. Each transformation is the identity at parameter zero.
2. It preserves the solution set `F(f)=T`, and every congruence version of
   that equation. Equivariance with an invertible target representation
   fixing `T` suffices; `F` itself need not be pointwise invariant.
3. Their tangent vectors at `f0` span ALL of `ker dF(f0)`.

Let `fs` be ANY integral tuple with reduction `f0` such that
`F(fs)=T (mod p^s)`. Put

`Es=(T-F(fs))/p^s mod p`.

**Lemma.** If `Es` is outside `im J`, then there is no solution over any
mixed-characteristic discrete valuation ring `R` with residue characteristic
`p`, finite `e=v_R(p)`, and reduction `f0`. In fact a solution is impossible
already modulo `pi^(es+1)`, where `pi` is a uniformizer. The conclusion
holds after ANY residue field extension.

**Proof.** Work in `R/(pi^(es+1))`, where `p=u pi^e` with `u` a unit.
Suppose there is a solution `f`. We successively apply the exact
transformations to make

`f=fs (mod pi^k)`

for `k=1,...,es`. The first assertion holds by the common reduction.
If `k<es` and the assertion holds at `k`, write
`f=fs+pi^k x (mod pi^(k+1))`. Polynomial expansion and `2k>=k+1` give

`F(f)=F(fs)+pi^k Jx (mod pi^(k+1))`.

Since `F(fs)-T` is divisible by `pi^(es)` and `k+1<=es`, `Jx=0` in the
residue field. The tangent-spanning premise remains true over that field:
it is a rank equality for finite matrices over `F_p`. Choose a linear
combination of the supplied tangent generators equal to `-x`.

Lift these finitely many residue coefficients to `R` and compose the exact
transformations with parameters `pi^k` times those lifts. Their leading
effect is `-pi^k x`; products of two such perturbations occur only at order
`pi^(2k)>=pi^(k+1)`. Their denominators are units. The transformed tuple is
still a solution and now agrees with `fs` modulo `pi^(k+1)`.

After finitely many such corrections,
`f=fs+pi^(es) y (mod pi^(es+1))`. At this last order the equation requires

`Jy=u^s Es`

in the residue field (up to the harmless consistent sign convention).
The right side is a nonzero scalar multiple of a vector outside `im J`,
which is impossible. Inconsistency of a linear system over `F_p` persists
over every field extension. This proves the lemma. No completeness,
convergence, norm, or unbounded iterative-limit premise was used. End proof.

**Consequence for a positive porting algorithm.** Under the same tangent
premise, a ramified lift can never rescue ANY failed ordinary Hensel step.
If a mixed-characteristic solution with this reduction exists, every
ordinary step from every already acquired integral approximation is
solvable. Differences between solutions of a step lie in the gauge tangent
and can be removed by the supplied transformations at that order. Thus
branching into coefficient extensions is not new existence leverage at a
gauge-complete point. This is a formal local statement. It does not provide
a rational height bound, terminating rational reconstruction, or a complex
algorithm from an infinite p-adic series.

## 3. Exact symmetries for the acquired matrix tensor

The 4-by-4 target uses the cyclic coefficient convention

`T=sum_(i,j,k=0)^3 E_ij tensor E_jk tensor E_ki`.

For invertible four-by-four matrices `P,Q,R`, apply to every term

`a -> P a Q^-1`, `b -> Q b R^-1`, `c -> R c P^-1`.

The induced tensor representation fixes `T` over EVERY commutative ring:
the three sums contract `Q^-1 Q`, `R^-1 R`, and `P^-1 P` to identities.
These transformations preserve the solution set, not arbitrary represented
tensor values. For each term also use

`(a,b,c) -> (s a,t b,(s t)^-1 c)`

with unit `s,t`; this transformation does preserve the represented tensor
itself. All identity-near transformations are defined by finite matrix
inversion and unit division, valid in every ring used in the lemma.

Their tangent vectors, for arbitrary four-by-four `X,Y,Z`, are

`da=Xa-aY`, `db=Yb-bZ`, `dc=Zc-cX`,

and the two per-term scaling directions. At characteristic two minus equals
plus. There are `3*16+2*47=142` listed generators, with rank at most
`142-3=139` because the central matrix/scaling parameters are redundant.
We do not infer equality from this parameter count; it is acquired below.

## 4. Actual native computation

The input is the authors' published `factorizations_f2.npz`, key `4,4,4`,
shape `(3,16,47)`, SHA256
`70f09f349d8d2874ef0e0e089459c7320f5aa3eef277df5ffa67f573709db2da`.
Attribution: Fawzi et al., *Nature*610 (2022), the official Google DeepMind
AlphaTensor repository; nonsoftware materials are supplied under CC-BY4.0.
Its original source/license and prior acquisition are retained in the
read-only sol23 source receipt. This run reuses those acquired bytes.

`ramified_probe.py` is a new standalone exact GF(2) computation. It does not
import the previous tangent compiler. It reconstructs the integer tensor,
all 4,096 coefficient equations, every Jacobian column, the entire kernel,
and all the exact-symmetry tangent generators above. The parameter order is
term, mode, entry. Python integers encode exact binary vectors; NumPy is
used only for the finite integer arrays and tensor products/sums.

The acquired result is

| Quantity | Exact value |
| --- | ---: |
| Tensor coefficients | 4,096 |
| Factor parameters | 2,256 |
| Jacobian rank | 2,117 |
| Kernel dimension | 139 |
| Listed exact-symmetry generators | 142 |
| Their rank | 139 |
| Kernel basis vectors outside their span | 0 |

Every computed kernel vector and every symmetry generator is separately
checked to have zero Jacobian image. Kernel vectors are obtained from
tracked generating-column dependencies. Every one is reduced by the
symmetry basis. Thus all tangent directions are acquired and accounted for;
there is no unsearched nongauge subspace being set to zero by an ansatz.

The old mod-4 obstruction is recomputed. To expose a directly consumable
witness, the final run constructs a binary tensor functional `ell` and
checks all 2,256 identities

`ell(J_column)=0`, while `ell(E)=1`.

It has 255 nonzero entries. The explicit dual, kernel basis, symmetry
generators, and defect are in `RAMIFICATION_WITNESSES.json`; hashes alone
are not substituted for these mathematical witnesses.

The final exact run took `0.0328371 s` after imports. The first successful
run took `0.0349093 s`; it was retained, then repeated once specifically to
export the new dual obstruction witness. One preceding command failed
before reading the input because of an incorrectly resolved relative path;
that path was corrected. No new source case, random pool, tuning, or
nonlinear characteristic-zero search was run.

## 5. Decisive conclusion and exact exclusions

Apply the lemma at `p=2,s=1`. There is no integral rank-47 tensor
decomposition over ANY finite ramified extension of a mixed-characteristic
valuation ring reducing to the acquired binary seed. More strongly, if
`2=u pi^e`, it already fails modulo `pi^(e+1)`. In particular, adjoining
`sqrt(2)`, `i`, or higher finite ramification cannot repair this reduction.

The same conclusion holds for any residue-field extension and for a
reduction in the orbit of the displayed target-preserving matrix/unit
symmetries and term permutations: lift that invertible residue symmetry,
apply its inverse first, and use the lemma at the original seed.

The conclusion does NOT exclude:

* a different binary rank-47 decomposition outside this orbit;
* a characteristic-zero scheme with different/bad PROJECTIVE reduction;
* paths that change rank, global searches, or other components;
* a characteristic-zero rank-47 algorithm, a better large-matrix exponent,
  or practical matrix multiplication gains.

The concrete positive hypothesis was that ramification could activate a
quadratic repair hidden from the ordinary tangent image. At this seed every
available first-order deformation is gauge, so exact finite gauge removal
closes that hypothesis at EVERY finite ramification order. The general
criterion changes which modular points merit such a search: nongauge
infinitesimal directions are necessary for a genuinely ramified escape,
though they are not sufficient. No new characteristic-zero algorithm was
acquired. Continuing this same ramified seed search is not justified.

## 6. Individual coefficient poles are not a projective escape here

There is a second possible escape to check rather than silently assume
away: perhaps coefficients with even denominators approach the same binary
factor DIRECTIONS, with cancellations between divergent terms. That issue
is distinct from integral lifting.

**Projective lemma.** Suppose the reduced rank-one TERM tensors
`tr=ar tensor br tensor cr` of a modular decomposition are linearly
independent. Let a decomposition over the fraction field of a discrete
valuation ring have the same projective factor reductions, term by term.
Then unit and possibly nonunit per-term factor rescalings convert it to an
integral decomposition reducing to the original modular decomposition.

**Proof.** Normalize each factor separately to a primitive integral vector
whose nonzero reduction is exactly its prescribed modular factor. A term
then has the form `kr ar_tilde tensor br_tilde tensor cr_tilde`, with
arbitrary nonzero coefficient `kr` in the fraction field. If the smallest
valuation `w` among the `kr` is negative, multiply the tensor equation by
`pi^(-w)` and reduce. The integral target disappears; the nonzero unit
residues of those `kr` attaining the minimum give a nontrivial linear
dependence among the corresponding `tr`. This contradicts independence.
Thus all term valuations are nonnegative.

Reduce the original equation. Its target is `sum_r tr`. Independence makes
this coefficient representation unique. Every term must consequently have
valuation zero and coefficient residue one. Absorb each unit `kr` into its
third primitive factor. The resulting integral tuple reduces exactly to
the given modular decomposition and represents the same target. End proof.

`projective_probe.py` acquires the new native premise, without repeating
the Jacobian search: the 47 term tensors have binary column rank47. The
script exports all term columns and pivot rows in `PROJECTIVE_PROBE.json`.
This additional exact run took0.00604351s after imports.

Combining the two lemmas therefore rules out even a fraction-field
decomposition with poles in individual factors whose PROJECTIVE factors
specialize to this native point (or to its stated symmetry orbit). Merely
allowing `1/2` coefficients while keeping these projective limiting factors
cannot evade the failure. A target-preserving fraction-field isotropy may
also be applied first: if its transformed factors had this specialization,
they would be forbidden by the same argument.

This still does not exclude bad-reduction boundary configurations with
linearly DEPENDENT limiting term tensors, or different modular algorithm
points. Such dependence allows cancellation of leading poles; it is an
actual missing representation for a new search, not a resource supplied by
the native array. The projective statement is valuative in characteristic
two, not a statement about a Euclidean neighborhood of complex algorithms.
