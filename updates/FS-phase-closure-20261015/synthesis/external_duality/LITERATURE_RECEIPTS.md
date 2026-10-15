# Primary-source proof receipts for the frozen-direction dual

Read date: 15 October 2026. Main proof: `POSITIVE_GROUND_STATE_AND_ATTAINED_DUAL.md`. Source claims, internal reconstructions, and historical novelty remain separate.

## Applicable primary Harnack theorem

E. DiBenedetto and N. S. Trudinger, [Harnack inequalities for quasi-minima of variational integrals](https://ems.press/content/serial-article-files/17564?nt=1), Annales de l'Institut Henri Poincare, Analyse non lineaire **1**(4) (1984), 295-308.

Actual source inspected: Section 4, equations (4.1)-(4.5), Lemma 4.1, and Corollary 3. Printed pages 305-307 were rendered and visually read. The structural growth permits a signed `b|u|^p` term; additive forcing zero gives homogeneous Harnack. Its proof explicitly extends the estimates to exponent at least the spatial dimension. The new report verifies these assumptions for the scalar shifted amplitude functional and obtains positivity. This paper's authors are DiBenedetto-Trudinger; Giaquinta-Giusti are cited predecessors.

The separately saved `ROUGH_DIRECTION_EXTENSION.md` additionally derives the logarithmic Caccioppoli/Morrey proof directly. The primary theorem's displayed `b in L^1` condition for exponent larger than the dimension independently matches its rough coefficient `|Dn|^4`; no bounded derivative or smooth positive reference is inserted.

## Hidden convexity and Picone prior art

L. Brasco and G. Franzina, [Convexity properties of Dirichlet integrals and Picone-type inequalities, arXiv:1403.0280v2](https://arxiv.org/html/1403.0280v2).

Actual read: Sections 2-3 on convexity/Picone equivalences and Section 5.1, Theorem 5.1 and proof, especially its use of strict positivity and the normalized eigenfunction comparison. Their stated scalar gradient integrand is nonnegative, convex and homogeneous. The current application has a signed vectorial polynomial with varying prescribed direction; its scalar rank-one reduction and lower-order growth establish the additional interface. Hidden convexity, Picone uniqueness and ground-state comparison are established principles. No invention of those principles or historical priority is claimed.

## Pedregal's exact remaining proof obligation

P. Pedregal, [Morrey's conjecture: rank-one convexity implies quasi-convexity for two-dimensional, two-component maps, arXiv:1905.06571v4](https://arxiv.org/html/1905.06571v4).

Actual read: Proposition 6.1, its setup (6.3)-(6.9), Step 2 through Claim 6.5 and the full-span inference, and Step 3 through the end of the proof. In the retrieved HTML these are approximately lines 475-608. The report isolates terminal straddling as a missing quantified feasibility lemma and gives an exact homogeneous linear toy showing why span is insufficient. No counterexample to Proposition 6.1 was constructed; neither the claimed complete theorem nor a community-acceptance judgment is imported.

## OpenAI Math revision verification and actual proof comparator

Repository: [openai/math](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a).

Main was fetched afresh and is still `1581d4cbdd69a0faf34b2089614fe2a814316a6a`. Its current preprints tree is `df0564b2deaab87e07854b6344d8c2f037682e77`, identical to the old navigation snapshot. Thus the earlier complete preprints tree is verified unchanged, rather than assumed current. The old snapshot is used for navigation; the new proof reads below were retrieved from the current pinned revision.

Actual proof read in `Sharp-one-dimensional-Lieb-Thirring-inequalities-for-matrix-potentials-October-5-2026/build/sections/`:

- [`spectral.tex`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Sharp-one-dimensional-Lieb-Thirring-inequalities-for-matrix-potentials-October-5-2026/build/sections/spectral.tex), lines 1-80 and 196-231: quadratic form compactness; explicit positive `sech` ground state and `Q*Q-1` factorization.
- [`field.tex`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Sharp-one-dimensional-Lieb-Thirring-inequalities-for-matrix-potentials-October-5-2026/build/sections/field.tex), lines 1-140: regularized matrix field, convergent odd-tail cancellation, and primitive by trace differentiation.

The former is a concrete logarithmic-derivative comparator; the latter explicitly discharges its own exactness/primitive obligation. Neither is a theorem about arbitrary planar quartic gradients. The current proof uses the applicable scalar variational Harnack theorem and supplies its own weak flux identity. The complete matrix Lieb-Thirring theorem was not independently audited or imported. `action-framework.tex` was acquired but is not a proof premise.

## Input-source scope

The new phase-density note and checkpoint were read in full. Their perspective and Picone proofs were reconstructed where used; the coupled-phase interval result and numerical searches were not used as premises. The automatic `mu_F>0` classification observation is deliberately not imported: every positive theorem here states `mu_F>0` explicitly.

This is selective primary-proof inspection, not a complete priority audit. External correctness and historical novelty remain UNKNOWN. Downloaded source snapshots are local research inputs, excluded from the authored deliverable inventory.
