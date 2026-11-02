# Independent adversarial audit

2026-11-02. Audited `RESULT.md` and `verify_torus.py`; added `audit_checks.py` without changing either original file.

## Verdict

**The conditional, one-sector ANY-LS decoder-stability transfer is sound**, provided the explicit matrix/locality premises below hold uniformly. It is stronger than an abstract homology-duality assertion: it constructs sparse finite-range cochain maps and both chain homotopies, supplies a syndrome-correct transferred decoder, and establishes an exact identity of logical jumps. It neither proves equality of Gibbs laws nor needs that equality. It does not establish the explicit ell=8 family's admission to these premises or independently establish a dynamical lifetime theorem.

## Primary-source comparison

Checked [2512.21922v1](https://arxiv.org/html/2512.21922v1): equations (3.3)–(3.8) give exactly the triangular coordinates and two differentials in RESULT; Proposition 3.9 splits horizontal blocks by closed cells; Propositions 3.12–3.16 supply the compatible augmentations and vertical exactness under their hypotheses. Theorem 3.17 concerns logicals, distance, expansion and decoding, not thermal lifetime. Its §2.1 assumes incidence numbers 0 or ±1. Import this incidence convention, or replace it with direct verification of the actual matrix blocks. Topological acyclicity of a general CW presentation alone must not silently justify the unweighted face-poset differential.

## Precise sufficient premises

1. Fixed dimension, bounded numbers of faces/cofaces and bounded stalk dimensions, in uniformly local coordinate bases. All basis conversions used in declaring physical coordinates must have uniformly bounded support and bounded-local inverses. Locality means the specified cell-incidence metric; Euclidean locality additionally needs a controlled physical embedding.
2. Actual horizontal blocks have square-zero differential, degree-zero kernel equal to the specified constant-vector embedding, and no higher cohomology. Actual vertical blocks have square-zero differential, degree-zero kernel equal to the prescribed dual-stalk restriction embedding, and no other cohomology. Check every boundary and junction type, not merely bulk types or global Betti numbers.
3. The complementary differentials commute and satisfy `dv iA = iA dA`, `dh iB = iB dB` for the actual physical and dual complexes. A kernel identified only abstractly with an isomorphic vector space is insufficient.
4. The chosen B decoder is syndrome-correct and its single-coordinate logical-jump bound holds for **every valid LS(p) syndrome distribution**, uniformly over physical coordinates. A theorem only about B's Gibbs distribution cannot be substituted.
5. A's syndrome law is LS(q), and A bath jumps have uniformly bounded support. Bounds on physical B syndrome-column weight and all transfer-map sparsities are uniform. The temperature is fixed with `0 < p = r q^(1/c) < 1` in the range of the B theorem.

These premises are directly testable/identifiable and do not assume the desired metric or thermal conclusion.

## Algebra and locality audit

The degreewise decomposition `V = im d ⊕ H ⊕ L`, with `d:L→im d` inverted, produces normalized contractions while preserving grading. Using separate bounded blocks is essential. The HPL series terminate because the relevant factors lower a nonnegative horizontal or vertical index. Since the prescribed inclusions already intertwine the complementary differential and `h i=0`, the perturbed inclusions remain unchanged and the induced differentials are the intended physical ones.

Substitution into the total-complex contraction identities gives, on all cochains,

```
F = PB iA,  G = PA iB,
H = PA HB iA,  K = PB HA iB,
I + GF = dA H + H dA,
I + FG = dB K + K dB.
```

Both homotopies are necessary evidence for the asserted homology isomorphism; the first alone would prove only one-sided invertibility. The construction actually supplies both. At fixed dimension all products have bounded length. Row and column bounds `3 M^6` for F,G and `9 M^11` for H,K at t=2 are valid crude bounds. Each factor acts within a bounded closed-cell/costar incidence neighborhood, so products also have uniformly bounded radius. None of this permits a level-dependent number of coarse-graining compositions.

## Decoder identity audit

For valid A syndrome s,

```
RA(s) = G¹ RB(F²s) + H²s
```

has syndrome s: `dA G RB(Fs)=GF s`, and the first homotopy supplies `dA Hs=s+GF s` because `dA s=0`. No linearity of RB is needed. For any physical error e, expansion and cancellation give the exact cochain identity

```
JA(s,e) = G¹ JB(F²s,F¹e) + dA⁰ H¹e.
```

Hence logical nontriviality is equivalent under the induced isomorphism. This establishes transfer to the original physical Z sector when its boundary complex is A; naming the dual code's sector by analogy is not an adequate substitute for this identification.

## Probability audit

For each occupied output bit of F²S, select an occupied input in its row. At most `r^|T|` choices occur, and column weight c forces at least `|T|/c` distinct selected inputs. The union bound gives `LS(min(1,r q^(1/c)))`. It does not assert a Gibbs pushforward.

For a fixed valid translation t of weight at most k, the mixture

```
(1-p^k) delta_0 + p^k Law(S+t)
```

is LS(p): outside supp(t), occupancy forces occupancy of S; multiplication by p^k pays for all possibly forced translated coordinates. This holds also when T lies entirely inside supp(t). Both components are valid syndromes, including zero. Therefore a distribution-uniform instability bound on the mixture implies a translated-event bound `p^(-k) epsilon`. Telescoping a fixed error of weight L uses fixed prefix translations, each of support at most wL, yielding `L p^(-wL) epsilon`. The argument does not condition on decoder history and does not incorrectly claim shifted laws stay LS(p). For L=0 the jump vanishes and should be handled directly. The endpoints p=0,1 need not be used in the fixed-positive-low-temperature conclusion.

The cited Gibbs-to-LS statement is independently justified as follows. For a linear syndrome code C and weights `q_i∈[0,1]`, fix occupied coordinates T. The numerator is `(product_T q_i)` times a weighted enumerator of an affine coset on the remaining coordinates. The corresponding linear subcode has at least that enumerator: finite Fourier expansion has nonnegative factors `1±q_i`, and the zero coset maximizes the sum. The denominator includes the enumerator of this linear subcode. Thus the probability is at most `product_T q_i`. This requires a linear allowed-syndrome space and the stated product weights/equal sector degeneracies, not statistical independence.

## Executable checks

`python verify_torus.py` passed unchanged, reproducing all reported row/column weights and both homotopies. Its local elimination is genuinely per closed cell/costar, not a global homology solver. The assembled all-degree arrays are acceptable here, but explicit grading checks were missing; these were added separately in `audit_checks.py`.

`python audit_checks.py` additionally passed:

- Degree preservation of F,G and degree −1 of H,K and the local homotopies.
- Syndrome correctness on all 256 valid A torus syndromes.
- All 4,608 exact jump identities (256 syndromes × 18 physical coordinates) with a deliberately nonlinear, syndrome-dependent B decoder.
- A negative control: omitting H²s fails syndrome correctness on **255 of 256** valid syndromes for this construction.

These tests are useful adversarial evidence, not a family certificate. They do not test nonconstant stalks, atlas junctions, recursive size uniformity or an ANY-LS witness theorem.

## Boundary of this verdict

The core transfer lemma passes. RESULT §8's specific witness enumeration is not independently recertified by these torus tests; its applicability still requires the deterministic witness lemmas and instability implication for the exact decoder/family. A full two-sector lifetime claim additionally needs the second sector, the relevant dynamical theorem and rate bounds, and a size comparison to preserve a stated exponent. No such claim follows from homology equivalence alone.
