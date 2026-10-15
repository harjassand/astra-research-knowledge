# Bounded primary research-capital retrieval

**Result:** At the pinned OpenAI/math revision, I found no proof directly about planar rank-one-convex quartics, quasiconvexity of such quartics, null Lagrangians, or positive Stieltjes inverse operators. Two nearby proofs were worth retrieving: one gives total-variation control uniform over bounded Ising observables, and one gives same-patch elliptic inverse-boundary uniqueness. Neither supplies a justified transfer to the current candidate

\[
F=\alpha H+\frac{r(r-1)u^2}{6}+j^2+ruj,
\qquad \alpha\ge \frac{3r}{8(r+2)}.
\]

The catalogue's only `Stieltjes` hit is the full-relative-support theorem for admissible zero-temperature Sherrington–Kirkpatrick Parisi minimizers on `[0,1)` (CONTENTS lines 7043–7045). It concerns support of a minimizer's order-parameter measure, not inversion or positivity of a Stieltjes operator. The nearby planar Mumford–Shah result is a free-discontinuity regularity theorem with local weak-`L^4` gradient bounds (line 8872); it is not a quartic gradient-integrand convexity theorem. Quartic keyword hits elsewhere concern arithmetic and query complexity.

## Retrieved proof 1: bounded-observable conditional-law resolution

The pinned catalogue entry is *Buffered comparison and stopping-band resolution in critical Ising* (CONTENTS lines 5152–5154). Its exact theorem is for the critical nearest-neighbor Ising model on the square lattice, with zero external field except fields induced by prescribed boundary spins, under the plus-boundary reference law in a fixed larger square. The target and an inward or outward exploration band must have positive fixed clearances; the two contour levels lie in separated windows. For every `epsilon, eta > 0`, Theorem 9.1 constructs a finite descriptor from band spins, with exceptional probability at most `epsilon`, and a deterministic regular signed barrier for each good state. For every transcript in a good state, inserting plus pins and then minus pins changes the target law by total variation at most `eta` in aggregate, and the resulting target-side Gibbs law is the same across all transcripts in that state. This holds simultaneously for all bounded target observables, including mesh-dependent ones. The number of states and clearances are fixed before the mesh threshold. A different band law transfers only with a bounded density ratio; a changed distant continuation requires its own lookup values (Corollary 9.2).

The proof builds finite-graph pointwise likelihood-ratio bounds from FK connectivity, applies critical RSW estimates through positive-width collars, then uses ordered transmission, interface scaling limits, and finite covers of admissible slit data. The conclusion is a conditional-law approximation for a particular critical Ising Gibbs model. The only general interface is the standard one from total variation to bounded-test expectations. The candidate has no supplied encoding as critical Ising spins, a band transcript, a signed barrier, or a Gibbs continuation, and its polynomial variables and parameter `alpha` are not identified with any part of this construction. The theorem therefore provides neither a measurement protocol nor a rank-one-convexity/quasiconvexity result for `F`.

Source: [pinned PDF](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Buffered-comparison-and-stopping-band-resolution-in-critical-Ising-September-23-2026/paper.pdf). SHA-256: `d5167e3fe5fb85f402954437c9474fb3ccfa518f8a5e8be92d8d572475410947`. Local copy: `sources/buffered-comparison-stopping-band-critical-ising.pdf`. Inspected PDF pages 1–8 and 39–43, including Theorem 1.2, Theorem 9.1, Corollary 9.2, and their proof arguments.

## Retrieved proof 2: same-patch elliptic boundary determination

The pinned catalogue entry is *Determination of a metric and a unitary connection from one boundary patch* (CONTENTS lines 8838–8847), alongside the scalar anisotropic Calderón result (lines 8854–8856). Theorem 1.1 assumes a compact connected smooth manifold with smooth boundary and dimension `n >= 3`, a smooth Riemannian metric, and a smooth unitary connection on the trivial Hermitian rank-two bundle. At zero frequency it compares the full sesquilinear energy form

\[
\langle\Lambda_{g,A,\Gamma}f,h\rangle
=\int_M\langle d_Au_f,d_Au_h\rangle_g\,dV_g,
\qquad f,h\in C_c^\infty(\Gamma;\mathbb C^2),
\]

for all input pairs supported on one nonempty open boundary patch `Gamma`. Equality determines the metric and connection up to a diffeomorphism and unitary gauge equal to the identity on `Gamma` (Theorem 1.1, PDF pp. 1–2). The proof first recovers boundary jets from the local Dirichlet-to-Neumann symbol, attaches a common exterior cap to obtain equal Green matrices, and uses source evaluations to identify points and fibers. Sections 3–6 continue the identification across an interior frontier using separate-variable Green continuation and shrinking-sphere transfer/moment estimates; Section 7 removes the conformal factor and completes the boundary-fixed identification (PDF pp. 4–12, 45–48).

This is a strong exact inverse-measurement theorem, but its measurement is a complete zero-frequency boundary energy form for smooth elliptic coefficients. It is not a bounded-observable readout of a moving heat process or a Stieltjes inverse representation. Its `n >= 3` hypothesis also excludes direct use for a planar two-dimensional problem. No map from `F`, its rank-one directions, or its unknown quasiconvex floor to the metric/connection pair or boundary energy data is provided.

Source: [pinned PDF](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/paper.pdf). SHA-256: `8e1bdd3a9067234842406dba45efc9e8efae5be0cd72a6c09f6dceee8793badb`. Local copy: `sources/determination_metric_connection_one_boundary_patch.pdf`. Inspected PDF pages 1–12 and 45–48, including the exact theorem statement, data definition, key source/Green construction, conformal removal, and global completion.

## Scope and source pin

The catalogue was fetched from the immutable revision `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`, the supplied HEAD. Its raw-byte SHA-256 is `cc7c0b8a1cdedd845a777e77cf682657308503daf8346c1349e06e9259d063c2`; permalink: [CONTENTS.md at the pin](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/CONTENTS.md). Selective catalogue ranges read: 5152–5156 (Ising bounded observables), 7043–7047 (Stieltjes support), 8836–8857 (boundary measurements), and 8868–8875 (planar Mumford–Shah regularity).

**Capital disposition:** No justified transfer to the candidate's rank-one convexity or quasiconvexity claims, no support for a sharp `QCsharpfloor`, and no measurement-interface closure follows from these sources. This is a scoped retrieval result, not a claim that no such theorem exists outside the pinned catalogue.
