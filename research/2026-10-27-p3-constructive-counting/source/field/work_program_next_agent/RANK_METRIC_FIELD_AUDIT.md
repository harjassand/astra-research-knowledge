# Independent audit: acquiring a hidden field cubic through an unknown low-rank quadratic defect

This note audits the root construction and its broader field-dimension version. It supplies a proof of the acquisition and reconstruction steps, independently executed exact checks, explicit point-counting costs, and a prior-art comparison. It does not claim a new Gabidulin decoder, a new hidden-field primitive, a practical speedup, or priority for the combined theorem.

## 1. Precise input and the theorem that survives the audit

Let `p : F2^n -> F2` be supplied as an exact Boolean polynomial of degree at most three, with description length `L`. An independently verified program-to-polynomial compiler may be used before this step, but its cost must be added; low-degree interpolation alone does not verify an arbitrary program's degree. The independent input count throughout is `n`.

Let `T` be the third difference tensor of `p`. Suppose it has zero radical and its computed centroid is a field `F` of degree `d` over `F2`. Then `n=bd`, and a field presentation and an `F`-module coordinate map `x <-> X in F^b` can be acquired in polynomial time. The field/module acquisition is audited separately in `FIELD_COMPILER_AUDIT.md`; it involves no enumeration of all `2^d` field elements.

The promised family consists of inputs for which, in some affine coordinates over this centroid field,

\[
p(x)=\operatorname{Tr}_{F/\mathbb F_2}P(X)+q(x),
\qquad \deg_F P\leq3,
\]

where `q` is a Boolean quadratic whose **actual alternating polar matrix** has rank `r`, and

\[
2r\leq d-3. \tag{1}
\]

Neither the coordinate map, `P`, `q`, nor its polar matrix is supplied. Affine terms may be placed in either summand. The field in this promise is the acquired centroid field, rather than an unspecified proper subfield.

**Audited theorem.** There is a deterministic algorithm that acquires an exact decomposition of this form in `poly(L+n)` bit time and counts the original Boolean outputs in

\[
\operatorname{poly}(L+n)+2^r\widetilde O\!\left(
2^{O(v)}d^{3v+7}v^{3v+5}3^{3v}2^{2v+4}\right),
\qquad v=b+1. \tag{2}
\]

The polynomial prefactor for emitting and adding characters can be absorbed into this bound. Equivalently, a safe uniform bound is

\[
2^{\,r+O(b\log n)}\operatorname{poly}(L+n). \tag{3}
\]

For fixed `b`, this is `2^r poly(L+n)`, using polynomial space. For growing `b`, the available point-counting backend has space `2^{O(b log n)} poly(L+n)`; polynomial space is not established by that backend. The algorithm is subexponential when both (1) and `r+b log n=o(n)` hold. For fixed `b`, `r=o(n)` eventually implies (1), but this implication must not be used when `b` grows.

Here `r` is even because the defect's polar matrix is alternating. The algorithm can use the maximal permitted decoding radius and report its acquired defect rank; the exact rank need not be supplied as input. If an input outside the promise happens to pass all the exact checks, the emitted decomposition still certifies a correct count with the cost determined by its actual acquired rank. Failed checks can return failure without a false count.

The improvement from the full-zeta bound is material. The counting task needs only `N_1`, so Proposition 36 of Lauder--Wan applies directly. Computing the full zeta function via their Theorem 37 would unnecessarily introduce a factor exponential in `b^2`.

## 2. The third tensor acquires the field and a canonical cubic lift

The quadratic error does not change `T`. A field scalar `a` in its centroid satisfies

\[
T(au,v,w)=T(u,av,w)=T(u,v,aw).
\]

In the acquired field/module basis define an `F`-valued trilinear form `A` by the nondegenerate trace pairing:

\[
\operatorname{Tr}(aA(u,v,w))=T(au,v,w)\quad\text{for every }a\in F.
\]

The centroid identities imply `F`-linearity in all three slots. Alternation follows from

\[
T(au,u,w)=T(u,u,aw)=0
\]

for every `a`, hence `A(u,u,w)=0`. Thus

\[
C(X)=\sum_{i<j<k}A(e_i,e_j,e_k)X_iX_jX_k
\]

is an acquired ordinary field cubic whose trace has exactly the original third tensor. Subtracting `Tr C` leaves a verified Boolean quadratic. All coefficient extraction and all identity checks take polynomial time in the explicit cubic description.

An ordinary field cubic remains an ordinary field cubic under an affine `F`-linear change of its coordinates. A change in the explicit field presentation conjugates coefficients by a field automorphism and preserves traces and ordinary total degree. Consequently the promise survives the acquired module basis, even though the original hidden coordinates are unknown.

This invariance does **not** assert that a representation of small degree over a proper subfield automatically has small degree over a larger centroid field. The theorem states the field match explicitly.

## 3. The residual quadratic belongs to an acquired rank-metric code, block by block

Let `B` be the alternating polar matrix of `p-Tr C` in the acquired binary coordinates. Under the promise,

\[
B=B_0+D,
\qquad \operatorname{rank}_{\mathbb F_2}D=r.
\]

Partition both matrices into `b` by `b` blocks, each of size `d` by `d`. Express a block by the trace pairing as

\[
B_{ij}(u,v)=\operatorname{Tr}(uL_{ij}(v)),\qquad u,v\in F,
\]

where `L_ij` is a unique binary-linear map `F -> F`. Computing it requires only the inverse of the trace Gram matrix. An invertible trace-pairing conversion preserves binary rank.

The field polynomial `P-C` has no cubic monomial involving three distinct field coordinates. Indeed such a monomial contributes a nonzero field third derivative, and the coefficients of the canonical lift were chosen to match that derivative exactly. Its possible remaining degree-three monomials are `X_i^3` and `X_i^2 X_j`; these are Boolean quadratics. Its ordinary field quadratics, linear terms and constants contribute no higher Boolean degree. The associated polar blocks satisfy

\[
L^0_{ij}(v)=a_{-1}v^{2^{d-1}}+a_0v+a_1v^2. \tag{4}
\]

The three terms have elementary origins:

* `Tr(c X_i X_j)` contributes `c v`.
* `Tr(c X_i X_j^2)` contributes `c v^2`.
* `Tr(c X_i^2 X_j)` contributes `c^{2^{d-1}}v^{2^{d-1}}`, using `Tr(z^2)=Tr(z)`.
* On a diagonal block, `Tr(cX_i^3)` contributes `c v^2+c^{2^{d-1}}v^{2^{d-1}}`.

For `d>=3`, the three Frobenius indices `-1,0,1` are distinct modulo `d`. On a diagonal block, symmetry makes the `-1` coefficient the adjoint of the `+1` coefficient, and alternation forces the index-zero coefficient to vanish. Conversely, these conditions describe exactly the self-blocks coming from `Tr(cX_i^3)`. Every alternating symmetric collection of blocks of the form (4) therefore has an ordinary field-cubic trace representation.

Precompose every block map by Frobenius:

\[
f_{ij}(X)=L_{ij}(X^2).
\]

For the unperturbed map this becomes

\[
f^0_{ij}(X)=a_{-1}X+a_0X^2+a_1X^4, \tag{5}
\]

because `X^(2^d)=X` on `F`. Evaluating (5) on any binary basis `g_1,...,g_d` yields a length-`d`, dimension-`3` Gabidulin code over `F`. The code and its evaluation points have been manufactured from the acquired field; neither is part of a supplied decomposition.

Each block error has rank at most the global rank `r`, since it is a row/column restriction of `D`. Frobenius precomposition is invertible, so it also preserves the block-error rank. The minimum rank distance of the code is `d-2`, and its unique decoding radius is

\[
t=\lfloor(d-3)/2\rfloor.
\]

Condition (1) therefore lets us recover every base block exactly, including diagonal blocks. Check the recovered global matrix for symmetry and zero diagonal, and check the rank of `D=B-B_0` exactly. These checks are necessary when running on arbitrary input; under the promise they all pass.

The global rank guarantee concerns the actual alternating polar defect. It is not interchangeable with the rank of an arbitrary symmetric completion of off-diagonal coefficients: removing its diagonal may increase rank. That different completion problem can require quarter phases and has no role in this real-Walsh argument.

## 4. Independent proof of the interpolation decoder

The decoder is established rank-metric machinery, included here to remove possible orientation and field-linearity ambiguities. Let `k=3`, `d>=k+2t`, and suppose received values are

\[
y_j=f(g_j)+e(g_j),\qquad \deg_q f<k,\qquad
\operatorname{rank}_{\mathbb F_2}e=s\leq t,
\]

where `deg_q` means the largest Frobenius exponent index in a linearized polynomial. Solve

\[
E(y_j)=N(g_j),\quad j=1,\ldots,d,
\qquad E\text{ monic},\quad\deg_qE=t,
\quad\deg_qN<k+t. \tag{6}
\]

Writing `E(X)=X^(2^t)+sum_{i<t}e_i X^(2^i)` makes (6) a linear system **over `F`**, with `k+2t` unknown coefficients. It is the left-error-annihilator formulation; one should not substitute the different right-hand-side interpolation from the title of Bombar--Couvreur's paper and incorrectly claim extension-field linearity for that other formulation.

The image of `e` has a monic annihilator of q-degree `s`. If `s<t`, compose a Frobenius power on the output to raise its q-degree to `t`; the resulting monic polynomial still vanishes on the same image. Thus (6) has a solution with `N=E o f`.

For any solution, let `H=N-E o f`. On `ker e`, a subspace of dimension at least `d-s>=d-t`, one has `H=0`. But `deg_q H<=t+k-1`. A nonzero linearized polynomial of q-degree `h` has at most `2^h` roots, so the inequality

\[
d-t>t+k-1
\]

forces `H=0`. Therefore every interpolation solution yields the same correct `f` by composition division. The relevant equation is

\[
N=E\circ f,
\]

with `E` on the **left**. If the leading term of `N` has index `t+j` and coefficient `c`, the next coefficient of `f` is the unique `a` satisfying `a^(2^t)=c`. This inverse Frobenius is computed by repeated squaring in `F`. Subtract `E o (a X^(2^j))` and iterate. Division and the final rank-distance check take polynomial time.

This proof covers all adversarial errors of rank at most the radius, including ranks strictly smaller than the chosen `t`. It requires no independence, genericity, random noise, or probabilistic success event.

## 5. Exact polynomial recovery and Walsh reconstruction

Choose a canonical quadratic `q_D` having polar matrix `D`, for example the sum of its upper-triangular monomials in the acquired binary coordinates. Then `p-q_D` has third tensor `T` and residual polar matrix `B_0`.

Section 3 supplies an ordinary field-cubic trace polynomial with these same top two differences. Their difference is Boolean affine, and every Boolean affine function of `F^b` is expressible as an `F`-trace affine function. A complete field polynomial `P_0` is therefore obtained either by the explicit block formulas or by an exact binary linear fit on all ordinary field monomials of total degree at most three. The number of monomials is `binom(b+3,3)`; each has `d` binary coefficient bits. Since every candidate has Boolean degree at most three, equality on all Boolean points of Hamming weight at most three proves global equality, by the restricted Boolean Mobius transform. This is a polynomial-size coefficient check, not sampled evidence.

When converting a Boolean constant one to a field constant, use an acquired element of trace one. If `d` is even then `Tr(1)=0`, so the field element one is not a valid automatic choice. Keeping an exterior binary sign is another exact solution.

For the quadratic `q_D`, put

\[
W_D(a)=\sum_{y\in\mathbb F_2^n}(-1)^{q_D(y)+a\cdot y}.
\]

Its support is the affine space

\[
S_D=\{a:a\cdot z=q_D(z)\text{ for every }z\in\ker D\}.
\]

The restriction of `q_D` to `ker D` is linear, so this space is nonempty. It has dimension `r`, and is acquired by solving the displayed binary linear equations. Each nonzero `W_D(a)` has magnitude `2^(n-r/2)` and a real sign `epsilon_a in {+1,-1}`. Ordinary exact quadratic elimination computes these signs in polynomial time. Fourier inversion yields the pointwise identity

\[
(-1)^{q_D(y)}=2^{-r/2}\sum_{a\in S_D}
\epsilon_a(-1)^{a\cdot y}. \tag{7}
\]

Consequently

\[
Z(p)=\sum_y(-1)^{p(y)}=
2^{-r/2}\sum_{a\in S_D}\epsilon_a
\sum_y(-1)^{\operatorname{Tr}P_0(X(y))+a\cdot y}. \tag{8}
\]

Each binary parity `a dot y` is a field-trace linear form, found with the same trace Gram inverse. Every leaf in (8) therefore remains a trace polynomial of ordinary field degree at most three. The `2^r` leaves can be generated and accumulated one at a time. Accumulating an integer numerator and dividing by `2^(r/2)` at the end avoids rational intermediate arithmetic; at most `O(n+r)` bits are needed for the accumulator. No complex or quarter phases occur.

Finally, the original output counts are `(2^n+Z(p))/2` and `(2^n-Z(p))/2`. The input coordinate map is invertible, so it introduces no change in multiplicity.

## 6. Exact leaf costs: direct point counting is sufficient

For a leaf polynomial `G` over `F=F_(2^d)`, define the Artin--Schreier hypersurface

\[
Z^2+Z=G(X_1,\ldots,X_b).
\]

It has `v=b+1` field variables and ordinary total degree at most three. For each `X`, there are two `Z` values precisely when `Tr G(X)=0`. Thus its affine point count satisfies

\[
N_{AS}=2N_0,\qquad Z(\operatorname{Tr}G)=N_{AS}-2^n. \tag{9}
\]

Lauder--Wan, Proposition 36 and the immediately following torus decomposition in Section 6.4, count `N_1` deterministically without a nonsingularity assumption. In their notation use extension degree `a=d`, variable count `v`, polynomial degree `D=3`, characteristic `p=2`, and extension index `k=1`. Their displayed direct-count cost, with the `2^v` torus decomposition and a safe `2^{O(v)}` allowance for uniform constants, is

\[
\widetilde O\!\left(2^{O(v)}d^{3v+7}v^{3v+5}D^{3v}p^{2v+4}\right).
\]

The displayed corresponding space is

\[
\widetilde O\!\left(2^{O(v)}d^{2v+4}v^{2v+3}D^{2v}p\right),
\]

and torus pieces may be processed sequentially. The modulus precision for `N_1` is `N=d(v+1)=O(n+d)`. The source uses ordinary exact arithmetic in finite unramified extensions and truncated rings, already charged in bit operations. Equation (9) is only integer subtraction.

Since `d<=n` and `v<=n+1`, the time and space are `2^{O(b log n)} poly(n)`. For fixed `b` both are polynomial. The full zeta function is unnecessary: Theorem 37 computes many extension-field counts to reconstruct a rational function, introducing a larger cost that the present task does not incur.

This note did not independently execute a general Lauder--Wan backend. The root work executes its narrower three-field-variable product-cubic/Dwork backend. The broader-`b` evaluator here is a theorem-level composition with the published exact algorithm; a practical claim would require implementation and equally informed competitors.

## 7. Independent executed checks

Run from the workspace root:

```sh
python work_program_next_agent/rank_metric_field_audit.py
```

The program implements its own finite-field linear solver, linearized interpolation, composition division, trace Gram conversion, quadratic Gaussian elimination and Walsh support construction. It is independent of the root decoder implementation. Its reused local dependency is `field_acquisition_audit.py`, which supplies finite-field arithmetic and binary linear algebra.

The saved result `rank_metric_field_audit_results.json` reports:

| Check | Exact cases |
|---|---:|
| Gabidulin decoding, all error ranks through the unique radius | 144 |
| Hidden field matrix fixtures | 16 |
| Independently decoded blocks | 144 |
| Pointwise Gaussian--Walsh reconstruction checks | 1,024 |
| Quadratic Gaussian sums compared with exhaustive enumeration | 56 |

Decoder fields have degrees `3,4,5,6,7,9,11`, with eight examples per permitted rank. The full matrix cases have `(d,r)=(7,0),(7,2),(9,2),(11,4)`, four examples each, and use `21,27,33` original inputs. Their base quadratics have binary ranks `20,26,32`; the tested errors have up to 270 nonzero scalar edges despite polar rank at most four. Thus they test a small-rank defect against a high-rank background, not an already low-rank complete quadratic.

The full matrix generator applies hidden invertible field changes to triple-product cubics, adds ordinary field quadratics and arbitrary dense alternating errors `U J U^T`, subtracts a canonical cubic lift, and decodes all nine blocks separately. Every base matrix and every global defect were recovered exactly. The Walsh tests additionally verify that every acquired binary parity converts to the correct field-trace linear form.

One implementation issue was found and repaired before the final run: linearized composition must skip trailing zero coefficients after allocating by actual degree. It did not alter any mathematical bound. All final assertions pass. No full truth-table point count, general Dwork backend, or practical speed comparison is claimed by this independent audit.

## 8. Prior art: the contribution cannot be described as the first hidden-field denoiser

Several ingredients and even the broad perturbation idea have direct precedents.

**Centroid field acquisition.** Magma's documented `TensorOverCentroid` explicitly rewrites a tensor over the residue field of its centroid and demonstrates recovery of a disguised `GF(2^10)` tensor. Brooksbank--Wilson and First--Maglione--Wilson provide the cited algebraic machinery. The acquired-field stage should be credited to this lineage. The separate elementary presentation audit only makes the polynomial cost explicit for this pipeline.

**Rank-metric decoding.** The interpolation in Section 4 is Gabidulin/Loidreau machinery. Bombar--Couvreur's primary paper reviews the relevant code, distance bound, trace adjoint and left-annihilator method before developing a different right-hand formulation. No new decoding radius or new code family is proved here.

**Internal HFE perturbations.** Ding--Schmidt (2005) already perturb hidden-field equations using a small-rank linear map. Dubois--Granboulan--Stern (2007) recover the perturbation kernel by differential analysis and then attack the underlying HFE pieces. Their model is a vector-valued quadratic public key built from a low ordinary-degree field map and perturbation through a low-dimensional internal image. Their analysis explicitly uses differential distributions for random secret keys and a probabilistic membership test. Thus the ideas of recovering an unknown perturbation and paying exponentially in its small dimension are established ancestry. The present all-errors guarantee comes from a different supplied observable: a scalar cubic's unchanged top tensor, which directly acquires a field and exposes a guaranteed decodable matrix code.

**Hat-plus and HFE-plus.** Faugere--Macario-Rat--Patarin--Perret (2022) add a small number of arbitrary quadratic forms with field-valued coefficients. The small parameter controls the output span of the perturbation, not the binary polar rank of each form. Their trapdoor inversion enumerates possible perturbation values, or annihilates their output span. This is a closely related replacement-and-reconstruction principle, but it is not the same input promise as a single scalar cubic with a low-rank binary polar defect.

**HFE-LL' is especially close.** Smith-Tone--Valenzuela (2025) explicitly recover the noise support of a hidden HFE map perturbed by products of binary linear forms, filter the perturbation, and recover an equivalent key. A scalar quadratic with polar rank `r` can be written, modulo an affine function, as `r/2` products of binary linear forms, so the *shape of the additive perturbation here is already present in LL'*. It would therefore be wrong to claim that low-polar-rank perturbations of hidden-field maps, or recovery of their hidden supports, are newly introduced by this work.

The official 2025 abstract and indexed model section were read; the PDF endpoint returned HTTP 403, and a complete audit of that paper's algorithms could not be completed through the available retrieval path. This limitation prevents a definitive first-priority conclusion. The official abstract already suffices to rule out a broad denoising novelty claim.

The narrower result supported by this audit is an explicit deterministic theorem for **one raw scalar Boolean cubic**, with a radical-free acquired centroid field, adversarial polar-rank error satisfying (1), exact acquired ordinary field degree at most three, and **exact counting** through (8)--(9). Standard HFE public maps provide many quadratic output coordinates and pose inversion/key-recovery problems; the cubic top tensor and fixed-dimensional point-counting interface are additional structure here. The inspected sources do not themselves state this counting theorem. That observation is not a proof of novelty or a claim to improve HFE cryptanalysis.

## 9. Boundaries that should remain explicit

* The algorithm has not acquired an arbitrary quadratic defect or an arbitrary small-rank decomposition outside its guaranteed decoding radius. A collision outside that radius obstructs unique recovery of the planted representation, not necessarily exact counting: a different valid acquired decomposition would still reconstruct the same function.
* The field and low-degree structure are acquired and certified, but the runtime theorem is for a structural family. It is not a general polynomial-time counter for Boolean cubics, circuits or SAT.
* Ordinary low degree over a small number of field coordinates is essential. A sparse field polynomial of exponentially large degree cannot be charged as though degree were its short description length.
* Restrictions by many arbitrary binary prefix constraints need not preserve a fixed number of field variables. Fast total counts do not automatically give fast prefix counting or self-reduction with the same bound.
* A scalar Boolean cubic already has substantial support whenever nonzero. Generic sampling or inversion of one output bit should not be advertised as a new capability on the strength of this counting result alone.

## Primary references

1. Alan G. B. Lauder and Daqing Wan, *Counting points on varieties over finite fields of small characteristic*, especially Proposition 36 and Section 6.4 (and Theorem 37 for comparison): https://arxiv.org/pdf/math/0612147
2. Maxime Bombar and Alain Couvreur, *Right-hand side decoding of Gabidulin codes and applications*, especially the preliminaries and discussion of Loidreau's left-hand decoder: https://arxiv.org/pdf/2112.07322
3. Magma handbook, `TensorOverCentroid`: https://magma.maths.usyd.edu.au/magma/handbook/text/672 ; cited bibliography: https://magma.maths.usyd.edu.au/magma/handbook/text/666
4. Jintai Ding and Dieter Schmidt, *Cryptanalysis of HFEv and Internal Perturbation of HFE*, PKC 2005: https://archive.ymsc.tsinghua.edu.cn/pacm_download/672/12592-dingjt6.pdf
5. Vivien Dubois, Louis Granboulan and Jacques Stern, *Cryptanalysis of HFE with Internal Perturbation*, PKC 2007, especially Sections 2--6: https://www.di.ens.fr/~stern/data/St118.pdf
6. Jean-Charles Faugere, Gilles Macario-Rat, Jacques Patarin and Ludovic Perret, *A New Perturbation for Multivariate Public Key Schemes such as HFE and UOV*, 2022, especially Sections 3.1--3.2: https://eprint.iacr.org/2022/203 ; author/project-hosted paper: https://vox-sign.com/files/hat.pdf
7. Daniel Smith-Tone and Cristian Valenzuela, *Cryptanalysis of the best HFE-LL' Constructions*, 2025, official abstract and metadata: https://eprint.iacr.org/2025/1362 ; indexed PDF model section also retrieved, but the complete PDF fetch was blocked.

