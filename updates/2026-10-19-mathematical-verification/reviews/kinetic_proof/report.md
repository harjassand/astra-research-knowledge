> Public selected edition of the 19 October audit. Original review SHA-256: `2938c353195e328fc8feeca215d68e85c3640e31e7ff464509a62908aea9bb1c`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# Independent finite-ramp theorem review

19 October 2026. Originally private review by `kinetic_proof_19`.

**Verdict: the stated existential finite-menu theorem is supported by an independently reconstructed argument. No material counterexample or proof gap was found under its stated waveform and observation contract.** The derivative rank, constant-seed construction, generic finite-menu choice, local positive realization, smooth endpoint refinement, and all-word equality can all be justified directly. This is a model-based independent mathematical audit, not external peer review, proof-assistant verification, physical validation, or a novelty assessment.

The decisive qualification is the admitted nuisance class: the two competing models can have different unknown four-rate waveforms, and outward and return responses are independent repeatable waveforms within each model. A waveform is fixed after construction and shared by time dilation across the selected menu. It is not fixed in advance by the experimenter, shared between the competing models, required to be monotone, constrained by a prescribed envelope, or supplied by a known common scalar response law.

## Review isolation and evidence

I read only these three source files, in this order:

1. `MAIN_RESULT.md`.
2. `workers/kinetic_frontier/THEOREM.md`.
3. `root/SHARED_WAVEFORM_ACCESSIBILITY.md`.

I did not read the original collision or realization audit reports/programs, current reviewers' work, or the exact collision-certificate implementation. The source theorem's descriptions of other audits were not counted as verification. I reconstructed the algebra and local-rank proof below, then wrote the standalone standard-library `independent_exact_check.py`. It imports no source modules. All writes made by the original audit were confined to its private review directory.

Source SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `MAIN_RESULT.md` | `ebc0b822761eb3d98efb4b3a24a5623a87746ee5a39dedffd92e858c740b243c` |
| `workers/kinetic_frontier/THEOREM.md` | `a3383e0215400ed6e8a3082e2d3ab8941d9bb2cc96ce5bc0d75d56be2788b5b2` |
| `root/SHARED_WAVEFORM_ACCESSIBILITY.md` | `e027dc729959a8ee7bcbb76838192a7ad3864156c690af069efe2041443e5a08` |

The separate general Lie-accessibility theorem in the third file is not needed for the constant-seed proof reconstructed here. I do not use its agreement as evidence for the collision theorem.

## Exact supported theorem

For each fixed finite nonempty set of distinct durations

\[
\mathcal D=\{d_1,\ldots,d_k\}\subset(0,\infty),
\]

there exist four distinct positive A rates \(\lambda_i\), four distinct positive B rates \(\mu_i\), and two orders of the same four anonymous pairs \((\lambda_i,\mu_i)\), namely \(\sigma=1423\) and \(\tau=2314\), such that:

- The four ratios \(\mu_i/\lambda_i\) are pairwise different.
- Each order has an outward waveform \(k^{\omega,+}:[0,1]\to(0,\infty)^4\) and a return waveform \(k^{\omega,-}\), each fixed and bounded, and each used at every duration in \(\mathcal D\) by the equation \(R'=d Q(k(u))R\).
- These waveforms can be smooth and identically equal to the prescribed pure rates in neighborhoods of the corresponding endpoints.
- With preparation \(e_1\) in either allowed starting pure mode and noncompletion readout \(c=\mathbf1^T\), both models have equal terminal probabilities after every finite legal word. Holds may have arbitrary nonnegative durations; every ramp duration must be in \(\mathcal D\).

A legal word respects the mode: A holds occur at A, outward ramps take A to B, B holds occur at B, and return ramps take B to A. An instantaneous A/B switch or an interrupted ramp is not an additional legal operation. The empty duration menu is a trivial order-ambiguity case and does not need the rank formula.

The rates and all four waveforms may depend on \(\mathcal D\). The proof does not supply one pair for every positive duration simultaneously. The conclusion also applies to adaptively selected endpoint experiments restricted to the same menu, as detailed below.

This matches the scope in `MAIN_RESULT.md:9-23`, `THEOREM.md:17-21`, and `THEOREM.md:185-205`.

## Independent reconstruction: exact branch and residues

Choose \(a>0\) and \(0<x<y\), and write

\[
\lambda=(a,a+x,a+y,a+x+y),\qquad S=2a+x+y.
\]

The blocks \(\alpha=(1,4)\) and \(\beta=(2,3)\) each have sum \(S\), with products

\[
p=a(a+x+y),\qquad q=(a+x)(a+y)=p+xy.
\]

For \(t\) close to 1, continue each rate to the corresponding root of

\[
X^2-SX+t p=0\quad(i\in\alpha),\qquad
X^2-SX+t q=0\quad(i\in\beta).
\]

All roots are simple at \(t=1\), because \(x<y\). Consequently the labelled \(\mu_i(t)\) are smooth, positive, and mutually distinct on some open neighborhood of 1.

If \(r_i=\mu_i/\lambda_i\), each satisfies

\[
\lambda_i r_i^2-Sr_i+t(S-\lambda_i)=0.
\]

For distinct \(\lambda_i,\lambda_j\), equality \(r_i=r_j=r\) would give \(r^2=t\) by subtraction, then \(r=t\) by substitution. Positivity gives \(t=r=1\). Thus every sufficiently close \(t\ne1\) has four pairwise distinct ratios. This is an exact argument, not a first-order separation estimate.

For any ordered distinct rate vector \(k\), let \(V(k)\) be its unit lower triangular eigenvector matrix. Solving the bidiagonal eigenvector recurrence gives

\[
V_{pq}=\frac{\prod_{j=q}^{p-1}k_j}{\prod_{j=q+1}^{p}(k_j-k_q)},\quad p>q,
\qquad Q(k)V=V\operatorname{diag}(-k).
\]

The two factors relevant to preparation and readout are

\[
(V(k)^{-1}e_1)_i=\prod_{j<i}\frac{k_j}{k_j-k_i},\qquad
(cV(k))_i=\prod_{j>i}\frac{k_j}{k_j-k_i}.
\]

The mixed coefficient for a label \(i\) is therefore

\[
C_i^\omega=(cV_B^\omega)_i((V_A^\omega)^{-1}e_1)_i
=\prod_{j\text{ before }i}\frac{\lambda_j}{\lambda_j-\lambda_i}
 \prod_{j\text{ after }i}\frac{\mu_j}{\mu_j-\mu_i}.
\]

For \(i\in\alpha\), the entire cross-block contribution of \(\beta\) after \(i\) is

\[
\frac{\mu_2\mu_3}{(\mu_2-\mu_i)(\mu_3-\mu_i)}
=\frac{tq}{tq-S\mu_i+\mu_i^2}
=\frac{q}{q-p}.
\]

Moving that block before \(i\) gives \(q/(q-p)\) using the A rates instead. The same argument gives \(p/(p-q)\) for the other block. The order within each block is preserved. Hence \(C_i^\sigma=C_i^\tau\) for every label, throughout the branch. No unknown waveform has yet been assumed obtainable at this stage.

This independently supports `THEOREM.md:27-69` and the spectral factors used at `THEOREM.md:73-93`.

## Independent reconstruction: constant-seed endpoint rank

I use the actual physical durations \(d_l\); writing them as \(D_lL\) makes no difference. For one ordered rate vector \(\lambda\), fix the positive constant seed \(k(u)=\lambda\), with \(Q=V\Lambda V^{-1}\), \(\Lambda=\operatorname{diag}(-\lambda)\). Let \(B_i=\partial Q/\partial k_i\) and \(H_i=V^{-1}B_iV\).

The diagonal identity for any bounded waveform is

\[
\log R(d_l)_{ii}=-d_l\int_0^1k_i(s)\,ds.
\]

Thus the ambient smooth tied-diagonal manifold has four common hazard coordinates and six strict-lower coordinates for each duration, of dimension \(4+6k\). Its coordinate chart can be taken to be the four common log-diagonal slopes and the \(6k\) raw strict-lower entries. It has no further equality constraints arising from stochastic column sums: completion is the missing mass, and the restrictions on that mass are inequalities.

Right-trivializing the endpoint derivative and reflecting normalized time by \(u=1-s\) gives

\[
Z_l:=V^{-1}\delta R(d_l)R(d_l)^{-1}V
=d_l\sum_i\int_0^1e^{d_l\Lambda u}H_i e^{-d_l\Lambda u}
                 \delta k_i(1-u)\,du.
\]

For \(p>q\), put \(\Delta_{pq}=\lambda_q-\lambda_p\). Then

\[
(Z_l)_{pq}=d_l\sum_i(H_i)_{pq}
        \int_0^1e^{d_l\Delta_{pq}u}\delta k_i(1-u)\,du.
\]

This fixes the spectral-gap sign explicitly; a different trivialization or unreflected time changes the exponent representation but not the rank argument. Since all matrices being conjugated are lower triangular,

\[
(H_i)_{pp}=-\delta_{ip},\qquad (H_p)_{pq}=-V_{pq}\ne0\quad(p>q).
\]

The second identity follows directly from the \(p\)-th row of \(V^{-1}(e_{p+1}-e_p)\): it equals \(-1\), with \(e_5=0\). Thus every strict-lower mode has at least one nonzero control coefficient; there is no missing root caused by commutation or a hidden diagonal gauge.

Suppose all \(6k\) nonzero frequencies \(d_l\Delta_{pq}\) are distinct. An output covector in the derivative's left kernel gives, for each input \(i\), a function

\[
f_i(u)=-a_i+\sum_{l,p>q} b_{l,pq}\,d_l(H_i)_{pq}
                         e^{d_l\Delta_{pq}u}.
\]

If this annihilates arbitrary controls, linear independence of distinct real exponentials and the constant function gives \(a_i=0\) and \(b_{l,pq}(H_i)_{pq}=0\) for every \(i\). Choosing \(i=p\) gives \(b_{l,pq}=0\). Therefore the derivative is onto.

More decisively, no infinite-dimensional implicit-function theorem is needed. Put \(N=6k+1\), \(h=1/N\), and allow each stage rate to vary independently on each of the \(N\) equal subintervals. A covector in the finite Jacobian's left kernel has

\[
\int_{jh}^{(j+1)h} f_i(u)\,du
=-a_i h+\sum_{l,p>q}b_{l,pq}d_l(H_i)_{pq}
 \frac{e^{d_l\Delta_{pq}h}-1}{d_l\Delta_{pq}}
 (e^{d_l\Delta_{pq}h})^j=0
\]

for \(j=0,\ldots,N-1\). These are exactly a square Vandermonde system with distinct nodes \(1\) and \(e^{d_l\Delta_{pq}h}\). Every nonconstant integral prefactor is nonzero. The preceding coefficient argument then proves rank \(4+6k\) for this finite parameterization.

Conjugation by \(V\) and multiplication by the invertible seed endpoint are tangent-space isomorphisms and preserve the common-diagonal relations. This rank is consequently the rank of the physical endpoint map into the stated manifold, not a rank computed in an enlarged unphysical output space.

This independently supports `THEOREM.md:103-119`. It does not infer constant-seed regularity from the separate Lie-accessibility theorem.

## Every fixed finite menu admits a suitable seed

For \(\sigma\), the six strict-lower signed gaps are

\[
\{-(x+y),-x,+y,-y,+x,-(y-x)\}.
\]

Directly computing the gaps for \(\tau\) gives the same multiset. No two different forms in this list are positive scalar multiples as formal linear forms in \(x,y\). Therefore, for different pairs of duration and root, an equality

\[
d_l L_r(x,y)=d_j L_s(x,y)
\]

cannot be an identity unless both the root and duration are identical. Each possible collision thus excludes at most a proper line in the \((x,y)\) plane. There are finitely many collisions to exclude. A finite union of proper lines cannot cover the nonempty open cone \(0<x<y\). After avoiding them, \(a>0\) is free because it changes no gap.

Hence the rank hypothesis can be achieved for both orders simultaneously for **every fixed finite positive menu**, even if a particular numerical seed would resonate with that menu. This is an existence argument for arbitrary real durations, not just rational or integer multipliers. It independently supports `THEOREM.md:131-135`.

## Finite-dimensional IFT and actual positive waveforms

For each order, define, at every menu duration,

\[
F_l(t)=V_B(t)E_lV_A^{-1},\qquad
G_l(t)=V_AE_lV_B(t)^{-1},\qquad
E_l=\operatorname{diag}(e^{-d_l\lambda_i^\omega}).
\]

Unit lower triangular eigenbases imply \((F_l)_{ii}=(G_l)_{ii}=e^{-d_l\lambda_i^\omega}\). Thus both target tuples lie exactly in the tied-diagonal manifold. They vary smoothly with \(t\), and at \(t=1\) both are the genuine seed tuple \((e^{d_lQ(\lambda^\omega)})_l\).

Choose an invertible \((4+6k)\)-column minor of the finite Jacobian above and freeze all other interval parameters. The ordinary finite-dimensional inverse-function theorem gives a local smooth right inverse for the endpoint map into manifold coordinates. Every target tuple sufficiently close to the seed has a preimage with one piecewise-constant waveform shared across the full menu. Since the seed parameters have a strict positive margin, the chosen neighborhood lies in the positive rate cone and all finitely many interval rates remain bounded.

Apply this separately to outward and return targets in each of the two orders. There are only four local neighborhoods. Their inverse images along the smooth branch contain a common open interval about \(t=1\). Intersect also with the interval where the B rates are positive and distinct, then select \(t\ne1\). This is the crucial last quantifier step: a single nontrivial branch point works for all four required waveforms and all menu members. No prescribed positive contrast floor is asserted.

Targets being close to positive physical seed propagators is not, by itself, used as a feasibility argument; the onto endpoint derivative and finite-dimensional inverse function theorem supply the actual functions. Conversely, arbitrary target tuples away from this local neighborhood are not claimed obtainable.

This independently supports `THEOREM.md:78-99`, `THEOREM.md:117-119`, and `THEOREM.md:187-191`.

For the smooth endpoint refinement, choose a finite set of rate-control variations giving the above invertible minor. Approximate them in \(L^1\) by smooth bumps compactly supported in \((0,1)\). At the fixed seed, every derivative entry is integration against a bounded continuous kernel, so the finite Jacobian changes continuously under these approximations. A sufficiently close smooth bump family retains the invertible minor.

Choose \(\chi\in C^\infty([0,1])\) **identically 0 near 0 and identically 1 near 1**, and use the outward base

\[
k_0(u,t)=\lambda+(\mu(t)-\lambda)\chi(u).
\]

For return interchange the endpoints. Add only the interior bump family. At \(t=1\) the base is the same constant seed, so the parameterized finite-dimensional IFT again realizes the exact targets for nearby \(t\). The bumps vanish near both ends, so the rates equal the required pure rates there and all derivatives glue to the adjacent holds. Uniform positivity follows from continuity on the compact interval and the strict seed margin.

The source's phrase “flat at both endpoints” at `THEOREM.md:177` is enough for derivative matching at the endpoints; the stronger “equal near both endpoints” in `MAIN_RESULT.md:19` is obtained by the explicit plateau choice just given. This is a small specification clarification, not an obstruction or change to the theorem. The smooth corollary is local existence and is not certified by the separate explicit five-piece numerical box.

There is a stronger limitation on **these exact smooth targets** than merely “monotonicity is not established.” At \(t\ne1\), every \(\mu_i\ne\lambda_i\): equality for even one component in \(\mu_i(S-\mu_i)=t\lambda_i(S-\lambda_i)\) would force \(t=1\), because \(\lambda_i(S-\lambda_i)>0\). Both target diagonals fix

\[
\int_0^1 k_i(u)\,du=\lambda_i
\]

in normalized time (equivalently, integrated hazard \(L\lambda_i\) over baseline length \(L\)). A continuous waveform joining unequal endpoint values \(\lambda_i,\mu_i\) and confined between them must have mean strictly inside that interval: continuity gives a positive-measure deviation toward \(\mu_i\), while the pointwise envelope prevents compensation past \(\lambda_i\). Consequently, for **each component and each direction**, these chosen targets require some rate below \(\lambda_i\) if \(\mu_i>\lambda_i\), or above \(\lambda_i\) if \(\mu_i<\lambda_i\). They necessarily leave the endpoint rate interval, and no monotone endpoint-matching waveform can realize them. The positive local IFT construction allows precisely such small interior compensations. This is a limitation of the explicit spectral targets, not a refutation of the admitted-class theorem and not a proof excluding every alternative ambiguity construction under monotonicity or an endpoint envelope.

## Every word, reverse coefficients, and adaptive experiments

Use eigenbases with columns reordered by the anonymous rate label. Then every A hold is diagonal in the A basis, every B hold in the B basis, and every ramp maps between these bases through \(E_l\). Matrix multiplication cancels every internal basis and leaves one diagonal product. Its entries depend only on the label's \(\lambda_i,\mu_i\), the total A and B hold durations, and the selected ramp durations; they do not depend on the order of the chain.

It remains to check **all four start/end mode cases**, rather than only an A-to-B surface. Let

\[
a_i^X=(cV_X)_i,\quad b_i^X=(V_X^{-1}e_1)_i,\quad
H_i^X=a_i^Xb_i^X\quad (X=A,B).
\]

The static coefficients

\[
H_i^A=\prod_{j\ne i}\frac{\lambda_j}{\lambda_j-\lambda_i},\qquad
H_i^B=\prod_{j\ne i}\frac{\mu_j}{\mu_j-\mu_i}
\]

are independent of serial order and nonzero. A-to-B words have coefficient \(C_i=a_i^B b_i^A\), already proved equal. B-to-A words have coefficient

\[
a_i^A b_i^B=H_i^A H_i^B/C_i,
\]

which is therefore equal too. A-to-A and B-to-B words use the static coefficients. This proves every legal word, including arbitrary repetitions and return loops. It does not require an inverse physical flow, literal waveform time reversal, or commutation of the physical generators.

Equivalently, set \(s_i=b_i^{A,\tau}/b_i^{A,\sigma}\). Static and mixed residue equalities imply that this equals \(b_i^{B,\tau}/b_i^{B,\sigma}\). With labelled eigenbases \(W_X^\omega\), the gauges

\[
T_X=W_X^\tau\operatorname{diag}(s_i)(W_X^\sigma)^{-1}
\]

satisfy \(T_Xe_1=e_1\), \(cT_X=c\), intertwine the corresponding hold generators, and obey

\[
T_BF_l^\sigma=F_l^\tau T_A,\qquad
T_AG_l^\sigma=G_l^\tau T_B.
\]

These identities make all-word equality exact. A similarity gauge by itself would not establish physical waveform existence; the IFT step above provides that separately.

For adaptive sequences of fresh experiments with endpoint completion readout, condition on the existing transcript. The strategy chooses the same next legal word under both models (or the same conditional randomization), and that word has exactly the same Bernoulli law. Induction gives identical transcript laws for every finite trial budget. If survival is read at successive boundaries in the same absorbing trajectory, joint histories are also determined by the prefix survival probabilities; these are equal for every prefix. Thus endpoint-based adaptive operation choices still do not distinguish the pair. This does not cover observations within ramps, calibrated internal trajectories, or durations outside the fixed menu.

Because the transcript distributions are equal, a classifier for the two distinct orders has worst-case success at most \(1/2\). This is the elementary exact-identical-distribution bound, not a new quantitative estimation theorem. It independently supports `THEOREM.md:193-199` and `MAIN_RESULT.md:83`.

## Independent exact check and what it does not check

The original audit executed the standalone `independent_exact_check.py`. From this public release directory, reproduce that check through the disposable runner:

```text
python3 -B verify.py --replay exact
```

The underlying `independent_exact_check.py` uses only `fractions.Fraction` and a new implementation of bidiagonal eigenvectors, inversion, Gaussian rank, determinants, and labelled gauges. Its recorded result is `independent_exact_check.json`, with status `PASS`.

It independently constructs the rational conic point

\[
\lambda=(1,3,8,10),\qquad
\mu=(740,2224,5883,7367)/737,\qquad
t=545158/543169,
\]

and verifies exactly:

- Both block sums equal 11 and both block products have the same scale \(t\ne1\).
- The four response ratios are pairwise distinct.
- Forward and reverse mixed coefficients agree between orders.
- The A and B gauges preserve preparation/readout and intertwine the hold generators and outward/return target matrices.
- For each order and duration multipliers \((1,2)\), a 13-interval seed has exact derivative rank 16 in the physical tied-diagonal tangent space. The check constructs a nonzero 16-by-16 minor; its rational determinant is nonzero by exact arithmetic. The two baseline orders are \((1,10,3,8)\) and \((3,8,1,10)\). Each baseline duration is \(13\log 2\), so all exponential moment integrals are rational after the harmless diagonal-coordinate normalization.

The rational nonclock point tests algebra only. I do **not** claim that this moderately sized perturbation lies in the unspecified local realization neighborhood. Existence of a sufficiently small nonzero perturbation follows from the proof above. I did not verify the original source's \(2^{-128}\) branch point, five-interval Jacobian, contraction radii, Hessian bounds, or four explicit Banach boxes. Those are additional quantitative claims outside this review's evidence.

## Scope corrections and remaining boundaries

No material correction to the existential theorem is required. The following qualifications are essential to the result I actually support:

1. The frequency separation is a **sufficient chosen-seed condition**, not a claim that every distinct-spectrum constant seed is regular for every duration menu. One first fixes the menu, then chooses the rate gaps to avoid its finite collision set.
2. The result is \(\forall\mathcal D\;\exists\) rates and waveforms, not \(\exists\) one pair for all \(d>0\). The local neighborhood and admissible response contrast can shrink drastically with the menu. There is no uniform contrast lower bound.
3. Endpoint plateaus should be chosen explicitly to obtain equality near the pure endpoints. Flatness at the isolated endpoint alone is a weaker property, although sufficient for smooth gluing there.
4. Shared diagonal hazards are handled exactly, including after smooth endpoint matching. For these specific targets the mean is the A endpoint rate, so every nontrivial smooth component must depart beyond the A endpoint away from its B endpoint. Monotone or endpoint-envelope-confined realization of these targets is impossible; other target constructions under such restrictions are not assessed.
5. The four unknown waveforms are model-specific and direction-specific. Imposing a shared calibrated physical response path across hypotheses, or a literal outward/return time-reversal relation, is an additional problem not settled here.
6. All-word equality applies to legal completed operations and endpoint completion readout. It does not extend to zero-duration switching, sub-ramp timing observations, other internal readouts, or adaptive introduction of unrestricted new ramp durations.
7. The theorem is an exact mathematical nonidentifiability result for the admitted model class. Its historical novelty, external correctness assessment, physical validity, practical importance, and a useful contrast regime remain separate questions.

## Line-level source evidence map

| Source location | Claim audited | Independent disposition |
| --- | --- | --- |
| `MAIN_RESULT.md:9-23` | Finite-menu statement and quantifiers | Supported with the legal-mode and model-specific waveform contract stated above. |
| `THEOREM.md:17-21` | Generator, preparation/readout, bounded positive dilation contract | Used as the model definition. |
| `THEOREM.md:27-69` | Equal-sum product branch; unequal ratios | Reconstructed exactly. |
| `THEOREM.md:73-99` | Eigenbases, diagonal spectral targets, constant seed | Reconstructed exactly; mixed-resolvent notation is unnecessary for the stronger gauge proof. |
| `THEOREM.md:103-119` | Rank \(4+6k\), finite partition, positive local preimages | Reconstructed with an explicit right-trivialized derivative and Vandermonde dual-kernel argument. |
| `THEOREM.md:125-135` | Signed gaps; arbitrary finite menu | Both order gap multisets recomputed; finite forbidden-line argument valid. |
| `THEOREM.md:175-183` | Smooth matching refinement | Supported by compactly supported bump approximation and finite-dimensional parameterized IFT; use endpoint plateaus for neighborhood equality. |
| `THEOREM.md:63-69,80-82,175-191` | Endpoint-envelope limitation of these smooth targets | Independently deduced: every B endpoint differs from A while both directions have A mean hazard, forcing each smooth component outside its endpoint rate interval. |
| `THEOREM.md:187-199` | Return realization and every-word equality | Reconstructed, including reverse coefficients and all four start/end modes. |
| `MAIN_RESULT.md:83` | Adaptive endpoint indistinguishability and \(1/2\) worst-case bound | Supported by conditional-transcript induction under the fixed interface. |
| `MAIN_RESULT.md:65-79`, `THEOREM.md:139-171` | Particular quantitative \(2^{-128}\) witness and Banach boxes | Not independently tested in this review; not needed for the existential theorem. |

**Final status:** independently supported existence theorem within the exact stated model; zero material flaws found; one minor endpoint-plateau specification clarification and a necessary endpoint-envelope departure for the chosen smooth targets. This review adds an independent model-based mathematical audit and exact algebra/rank checks, not external peer review or formal proof.
