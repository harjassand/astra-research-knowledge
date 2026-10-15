# Prior-art comparison: finite-noise accretive diagonal-control obstruction

Date: 2026-10-15. This is a targeted comparison, not a literature-priority certification. No exact predecessor for the complete interface below was established. Absence from this search is not evidence of novelty.

## Interface being compared

The construction realizes the 2^m functions

F_s(u) = product_i [epsilon/(epsilon+u_i) if s_i=0; u_i/(epsilon+u_i) if s_i=1], epsilon=m^-2,

as c^T(A_s+P diag(u) P^T)^-1 b on [0,1]^m, with n=m+2 states and the same calibrated P,b,c for every hidden label s. The latest improved embedding has ||b||, ||c||, ||P|| at most one, controlled matrix norm O(1), strict accretivity margin Omega(m^-4), and condition number O(m^4). Coefficient descriptions remain polynomially bounded. These are the resource guarantees used in this comparison; the earlier large-port embedding is not needed for them.

The acquisition primitive is a noisy scalar steady-state response at an arbitrary adaptively selected global control. Bounded absolute noise and, separately, independent Gaussian noise yield exponential query lower bounds for constant-accuracy best-control decisions and uniform response prediction. Computation is unrestricted. An exact prime-coded response identifies the label in one query on the unperturbed promised family. This is an absolute-noise distinction, not exponential binary-description complexity: exponentially small tolerance can require only polynomially many precision bits.

The simultaneous regime of dimension-independent dissipation and unit-strength P is not settled by this construction. A rescaling that increases actuator strength cannot settle that narrower regime. Strict matrix accretivity also should not be advertised as a fabrication theorem or as proof of passivity for every chosen external input-output supply rate.

## 1. Closest structural realization lineage: passive products and Schur–Agler realizations

Ramlal Debnath and Jaydeb Sarkar, *Factorizations of Schur functions*, preprint 2019, published 2021. Theorems 2.2 and 3.2 give explicit colligation product constructions for multivariate Schur–Agler functions. Their discussion connects this to earlier products of colligations.

Primary sources:
- https://www.isibang.ac.in/~jay/papers/SA%20Final.pdf
- https://arxiv.org/abs/1908.01850
- https://digitalcommons.isical.ac.in/journal-articles/2005/

**Concrete overlap, by direct algebra:** Under z_i=(u_i-epsilon)/(u_i+epsilon), the gates become (1-z_i)/2 and (1+z_i)/2. The response is therefore a product of elementary one-variable Schur functions in separate variables. Cascade/product realization is established territory.

**Unresolved equivalence:** The cited construction has not been converted here into the exact n=m+2 realization with common ports, positive rank-one additive diagonal controls, O(1) controlled norm, unit-or-smaller ports, inverse-polynomial strict loss and polynomial conditioning. These guarantees do not follow merely by citing an abstract isometric realization. Conversely, no obstruction to obtaining them from that lineage was established. The improved bounded-port embedding strengthens the interface comparison but does not resolve priority. This is the most important remaining comparison before claiming novelty of the embedding.

## 2. General affine-pencil realization is old

Anthony Stefan and Aaron Welters, *Extension of the Bessmertnyi Realization Theorem for Rational Functions of Several Complex Variables*, 2021, Theorem 2, represents every multivariate rational matrix function as a Schur complement of an affine linear matrix pencil. The constructive proof uses sums, products, inverses and compositions and extends earlier Bessmertnyi work.

Primary source: https://arxiv.org/html/2010.08088v3

**Overlap:** Realization of rational gate products by linear pencils, including removal of nonlinear expressions through additional coordinates, is not itself a novelty claim.

**Missing guarantees:** The theorem does not impose positive rank-one diagonal variable coefficients, fixed common source/detector, strict accretivity, bounded ports or polynomial conditioning. Symmetric realizability is not positive-definite realizability. Its generality alone neither subsumes nor disproves the quantitative embedding here.

## 3. Exact algebraic learning and read-once determinants

Abhiram Aravind, Abhranil Chatterjee, Sumanta Ghosh, Rohit Gurjar, Roshan Raj and Chandan Saha, *Learning Read-Once Determinants and the Principal Minor Assignment Problem*, 2026, Theorem 1.1, gives randomized polynomial-time exact black-box learning of rank-one symbolic determinants and det(A+diag(y)), with unit-cost field operations and appropriate field-size assumptions.

Primary sources:
- https://www.csa.iisc.ac.in/~chandan/research/learning_ROD.pdf
- https://arxiv.org/abs/2603.04255

**Overlap and boundary:** This addresses a close algebraic matrix structure. Exponentially many principal-minor coefficients alone do not imply exact black-box acquisition hardness. Its primitive is a determinant rather than the scalar resolvent response here, and it is not a bounded-noise learning result. The construction's one-query exact recovery is consistent with this literature and makes precision/noise qualifications essential.

Earlier foundation: N. R. Aravind and Pushkar S. Joglekar, *On the expressive power of read-once determinants* (2015), Lemma 6, converts read-once formulas through occurrence-one branching programs into read-once determinants. This supports treating arithmetic-product representation alone as standard. It supplies neither the present accretivity/resource guarantees nor a noisy-query theorem.

Primary source: https://arxiv.org/pdf/1508.06511

## 4. Closest exponential statistical system-identification predecessor

Anastasios Tsiamis and George J. Pappas, *Linear Systems can be Hard to Learn* (2021), Theorem 3, proves exponential sample complexity even with inverse-polynomial distance from uncontrollability. Weakly coupled chains exponentially attenuate excitation; their discussion explicitly contrasts bounded input energy with exponentially large excitation.

Primary source: https://arxiv.org/html/2104.01120

**Actual interface:** Temporal state observations of x_(t+1)=Ax_t+Bu_t+Hw_t, bounded model norms and input energy, and estimation of A. This is an important predecessor for exponential statistical difficulty in finite-dimensional linear systems.

**Difference:** It does not establish arbitrary diagonal-configuration queries with a fixed scalar source/detector, order-one attainable response at a hidden corner, or constant-accuracy global control and uniform response-prediction objectives. Parameter-identification hardness does not automatically establish decision hardness. The present O(1)-norm and unit-port bounds sharpen this comparison but do not erase the different observation and intervention models.

## 5. Black-box control: exponential regret is not exponential query count

Xinyi Chen and Elad Hazan, *Black-Box Control for Linear Dynamical Systems*, COLT 2021, Section 5/Theorem 9, proves exponential regret over T=d/8 steps for unknown noiseless dynamics with B=I. The hard mechanism is exponential state growth before enough matrix-vector information is acquired.

Primary source: https://proceedings.mlr.press/v134/chen21c/chen21c.pdf

**Difference:** Its exponential quantity is loss/regret, not the number of queries. Its interaction is a single evolving trajectory and its challenge is stabilization. It does not provide the static, uniformly accretive, bounded-norm response-query obstruction here. It is related black-box control hardness, not an exact predecessor or contradiction.

## 6. What can and cannot be claimed

The zero-transcript counting and Gaussian null-reference change-of-measure steps are standard information-theoretic mechanisms. The partition of unity supplies the relevant per-query capacity bound; small hidden parameter count does not prevent that obstruction. There is no novelty claim for these proof templates.

A defensible description is:

> An explicit resource-accounted accretive additive-diagonal realization of a standard noisy hidden-needle obstruction, with common bounded ports and bounded controlled matrix norm.

The potentially useful mathematical contribution is the **joint interface guarantee**, including positive rank-one diagonal interventions, fixed ports, constant attainable contrast, inverse-polynomial strict dissipation and polynomial conditioning, rather than rational realization or exponential learning difficulty separately. Priority for that conjunction remains open, especially against passive-cascade/Cayley-transform constructions.

No exact passive Boolean-circuit predecessor meeting the full resource interface was established in this targeted pass. Broad circuit-synthesis existence statements should not be substituted for a quantitative comparison, and the lack of an exact match must not be used as evidence that none exists.

The Gaussian corollary proves hardness for a particular independent, unbiased, finite-variance noise model. It does not prove the same lower bound for every independent unbiased finite-variance distribution.

## Remaining focused priority check

Work out the elementary Schur-product cascade under the coordinatewise Cayley transform and compare its resulting pencil, state count, shared ports, loss, and condition number with the improved embedding. An explicit resource-preserving equivalence would identify a stronger predecessor; failure of one convenient conversion would not establish novelty. No additional broad search is needed to formulate this concrete outstanding comparison.
