# Blind stationary tomography from unlabelled edge interventions

4 November 2026. Research theorem; see companion AUDIT.md for independent review. No priority or physical-performance claim. The central missing operation is identifying which transition each local intervention changed, rather than assuming those targets were calibrated. Graphic-matroid reconstruction is an explicitly established subroutine, not a new result here.

## 1. Contract and theorem

Observe n named states, n≥4. An unknown irreducible continuous-time Markov generator W uses the column convention: 1ᵀW=0, off-diagonal entries nonnegative, Wπ=0, and π is a positive probability vector. Its complete transition graph is unknown.

Each of m interventions changes only the two rates on an unknown unordered pair e={a,b}, multiplying both by an unknown factor t_e>0, t_e≠1. Both rates on every intervened pair are strictly positive. Different interventions affect different pairs. The selected pairs form an unknown simple spanning 3-vertex-connected graph G. Every selected edge has nonzero baseline stationary current. Additional unperturbed transitions are allowed, and need not form a bidirected graph.

The data are π and the separately indexed post-intervention stationary distributions π^(e). The experiment index is known, but neither endpoint of its target pair is known. All states remain correctly named across measurements. Exact data and the model/control promises are assumed for the first theorem.

**Theorem.** These data determine the full W up to one positive scalar and determine the unordered target pair for every intervention. Both the graph of selected targets and all directed rates, including unperturbed rates, are recovered in polynomial rational bit time from exact rational data, using established graphic-matroid reconstruction. The n=3 case also holds when all three pairs are intervened with nonzero responses.

This removes target labels, not the edge-locality promise. A generic perturbation affecting many transitions is outside the model. Complete positive rates do not guarantee nonzero currents; detailed balance is an excluded case for symmetric barriers.

## 2. Response geometry

Orient an unknown edge from a to b and set b_e=e_b−e_a and u_e=W_ba e_a−W_ab e_b. With d_e=π^(e)−π, subtraction of stationarity gives

W d_e=−(t_e−1)(u_eᵀπ^(e)) b_e=α_e b_e.

On H={x:1ᵀx=0}, W is invertible. The response is zero exactly when the baseline current u_eᵀπ is zero: a zero current leaves π stationary after the scaling, while an unchanged π requires (t_e−1)u_eᵀπ=0. Therefore every assumed active d_e is nonzero, α_e is nonzero, and

d_e=α_e W_H^−1 b_e.

Consequently linear independence of any selected set of response columns is equivalent to independence of the corresponding incidence columns. Their labelled column matroid is exactly the cycle matroid M(G). The unknown nonzero response amplitudes and their signs do not change it. The response columns span H, and distinct targets give distinct projective lines.

## 3. Recovering the abstract target graph

A linear-independence oracle for the response columns is obtained by exact rational rank computations. The input is promised graphic. Established polynomial-time graphic-matroid reconstruction returns a graph H_G with an edge carrying each original experiment index and the same cycle matroid. Isolated vertices are omitted.

Whitney's uniqueness theorem implies that a simple 3-vertex-connected graph is determined by its edge-labelled cycle matroid up to a vertex relabelling. Hence H_G is isomorphic to G, with the supplied experiment indices respected. Its n vertices may initially have arbitrary abstract labels.

An alternative explicit matrix route first chooses a response basis and expresses every other column in it. The support of each coordinate vector gives its fundamental circuit. Under the graphic promise these fundamental circuits determine the corresponding binary representation, which can be passed to a binary graphic-matroid reconstruction algorithm. This step does not claim that an arbitrary real matrix can be certified graphic merely by discarding coefficient signs and magnitudes. The full candidate is checked later.

The oracle and graphic reconstruction steps are established algorithms. They do not require enumeration of all circuits. Their use here is a reduction of the physical inverse problem to a known computational primitive.

## 4. Reconstructing the map before knowing state labels

Let P be the unknown permutation matrix mapping the named physical vertices to the arbitrary abstract labels chosen for H_G. Its oriented incidence columns b'_e equal ±P b_e.

Solve a homogeneous linear system in an n by n matrix K:

1. 1ᵀK=0.
2. Kπ=0.
3. Kd_e is parallel to b'_e for each experiment e.

Condition 3 is linear: set (Kd_e)_i=0 outside the two abstract endpoints. Condition 1 then enforces opposite endpoint components. A nonzero solution exists because K=P W is one.

**Rigidity lemma.** If a spanning graph has connected cycle matroid, every linear map A:H→H preserving each of its incidence rays is cI_H.

For each simple cycle, the incidence columns have a unique dependence up to scale. Applying A to that dependence forces all ray eigenvalues on the cycle to agree. Chains of cycles sharing edges propagate equality throughout a connected cycle matroid. Its columns span H. This argument allows zero eigenvalues and does not assume A invertible.

A 3-vertex-connected graph has connected cycle matroid. Given any K solving the system, define A=P^−1 K_H W_H^−1. It preserves the physical incidence rays, so K_H=cP W_H. Since Kπ=Wπ=0 and every vector decomposes uniquely into H plus a multiple of π, K=cP W on the full space. Thus the homogeneous system has exactly a one-dimensional nullspace, including singular candidate matrices. Compute any nonzero rational basis vector for it.

## 5. Positivity fixes the physical labels

The unknown permutation is a row permutation, not a simultaneous row-and-column relabelling: measured probability coordinates and the columns of K retain their original named-state coordinates.

Each column of W has exactly one negative entry, its diagonal, and all other entries nonnegative. Because every vertex of the intervened 3-connected graph has at least three incident bidirected edges, each column also has at least three strictly positive entries. For the n=3 triangle there are at least two.

Choose the sign of K so that each column has exactly one negative entry. This choice is unique: the opposite sign has at least two negative entries in every column. Let r(j) be the row of the negative entry in column j. Since K=cP W with c>0, r(j) is precisely the abstract row P(j), and these rows form a permutation.

Reorder the rows by setting V_ij=K_(r(i),j). Then V=cW with c>0. Each abstract edge {p,q} now maps to physical target {r^−1(p),r^−1(q)}. Fix −tr V=1 if desired; this merely selects a clock convention.

This is stronger than identifying the target graph up to an unobservable state permutation: physical state names are aligned by the generator sign pattern. It does not require unequal baseline probabilities. A uniform π is permitted.

## 6. A completely explicit complete-graph algorithm, including n=3 and n=4

If the selected target graph is K_n, graph reconstruction can be described without a general matroid subroutine. For two response lines, declare them adjacent when some third observed response makes a linearly dependent triple. Two distinct incidence lines of K_n admit such a third line exactly when their edges share a vertex. Thus this gives the line graph L(K_n).

For n≥4, examine triples of line-graph vertices that are pairwise adjacent and whose three response vectors are linearly independent. Such a triple is a three-edge star, not a triangle: three pairwise incident graph edges either share one vertex or form a triangle, and only the latter are dependent. For each star seed, include the seed and every line-graph vertex adjacent to all three seed elements. This produces precisely the full star at that vertex. No edge not incident to the center can meet all three distinct spokes.

Deduplicating these sets gives exactly n stars. Every observed edge belongs to exactly two of them, so the stars serve as abstract vertices and their pairwise memberships identify the edge targets. Enumeration is polynomial in m and n. For n=4, both stars and triangles have size three, but the independence test distinguishes them; merely searching for maximal cliques of size three would be incorrect.

For n=3, assign the three experiments arbitrarily to the three edges of an abstract triangle. Every permutation of its three edges is induced by a vertex permutation. Sections 4–5 then recover the unique physical generator and labels. No n=2 symmetric-barrier analogue is asserted, because an irreducible two-state chain has zero stationary current.

## 7. Finite physical consistency and limitations

After recovering V and each pair, calculate α_e from Vd_e=α_e b_e and D_e=(V_ba e_a−V_ab e_b)ᵀπ^(e). Compatibility with a positive nonunit symmetric barrier requires D_e≠0 and

t_e=1−α_e/D_e>0,  t_e≠1.

These values are invariant under the common clock. Conversely these conditions, a valid irreducible generator, positive normalized snapshots and positive rates on selected pairs ensure the reconstructed scaled generator annihilates π^(e), so they suffice for each finite intervention. This is a model-consistency check, not proof that an actual apparatus changed no other rates.

The true selected graph need not equal the full generator graph. A selected spanning 3-connected subgraph suffices even when other positive rates are present. Neither graph has to be planar.

Three-connectivity is a sufficient uniqueness condition for the abstract graph, not an asserted necessary condition for the entire inverse problem. Below it, graphic matroids can admit Whitney twists and other 2-isomorphic representations. The positivity and finite-control conditions might remove some such ambiguities; no complete classification is proved here. A cycle-connected graph suffices once targets are labelled, but does not by itself establish this blind graph-reconstruction argument. Graphs with articulation blocks can retain independent clock ambiguities even with target labels.

Missing interventions, unrecognized duplicate targets, zero-current responses, hidden states, changing state definitions, unobserved parallel channels and multi-edge controls require additional analysis. Exact duplicate rays can be collapsed under the locality promise, but the stated noise contract assumes distinct targets. Absolute time remains unknowable from these stationary snapshots alone.

## 8. A conditional noise theorem

Exact dependence tests are discontinuous. No noise-independent finite-sample guarantee follows from the exact theorem. The following explicit margins describe one sufficient regime.

Let D be the n by m matrix of true responses. Define gamma>0 as a lower bound on the smallest singular value of EVERY independent column submatrix with at most n−1 columns. This is a theoretical margin assumption, not a quantity claimed to be certified from finite data. A response near zero or an almost dependent independent set can make gamma arbitrarily small.

The rank margin can be related to ordinary physical conditioning rather than treated as an unexplained minimum over many sets. Put d_min=min_e ||d_e||_2 and kappa=||W_H||_2 ||W_H^−1||_2. Then gamma=d_min/(sqrt(2) n kappa) is a valid conservative lower bound. Indeed, for any forest incidence matrix B_F and edge vector x, removing an edge and summing the vertex divergence over one side of its tree gives ±x_e. Cauchy–Schwarz yields |x_e|≤sqrt(n)||B_F x||_2; summing over at most n−1 edges gives ||B_F x||_2≥||x||_2/n. Also ||d_e||_2≤sqrt(2)|alpha_e| ||W_H^−1||_2. Applying these inequalities to D_F=W_H^−1 B_F diag(alpha_e) gives the asserted lower bound. This does not claim that kappa is known from the uncalibrated finite data.

Suppose each baseline and intervention probability coordinate is estimated to error at most eta. Every response coordinate then has error at most 2eta. A column submatrix of at most n−1 columns has operator error at most 2n eta. If 2n eta<gamma/4, singular-value thresholding at gamma/2 correctly answers every independence query: an independent submatrix has smallest singular value at least 3gamma/4 after perturbation, while a dependent one has smallest singular value at most gamma/4. Sets larger than n−1 are automatically dependent. Computing singular values within gamma/8 preserves the decision. Thus the graphic reconstruction uses the same labelled matroid as in the exact experiment.

Once its abstract graph is recovered, let L be the exact linear system of Section 4 in the stated unweighted row convention, with one-dimensional kernel spanned by K_0=P W/||W||_F. Let sigma>0 be its smallest nonzero singular value. The estimated system obeys

||Lhat−L||_2 ≤ eta A_0,  A_0=sqrt[n²+4mn(n−2)].

Choose a unit vector Khat whose residual is within rho of the minimum residual for Lhat, and write E=eta A_0. Its residual under L is at most 2E+rho. After aligning the mathematical sign with K_0,

||Khat−K_0||_F ≤ sqrt(2)(2E+rho)/sigma

whenever the bound is informative. Denote this upper bound by delta.

For each column of K_0, take its negative-entry magnitude and its second-largest positive entry. Let zeta>0 be a lower bound on all these quantities. It exists under the theorem but may be tiny. If delta<zeta/3, choose the orientation of Khat for which each column has exactly one entry below −zeta/2. The correct orientation has one such entry, while the opposite orientation has at least two. Those entries identify exactly the physical row permutation. Row reordering then gives a unit-Frobenius representative of W with error at most delta. Small inferred off-diagonal entries may still have wrong signs; exact support recovery and a nonnegative projection need additional error margins or a separate constrained fit.

An optional elementary generator repair sets each off-diagonal estimate to its positive part and then replaces every diagonal by minus its column's off-diagonal sum. Relative to the true unit-Frobenius generator, its Frobenius error is at most sqrt(n)delta: positive-part clipping does not enlarge the off-diagonal error, and Cauchy–Schwarz bounds the squared diagonal error by n−1 times the total squared off-diagonal error. This guarantees a conservative nonnegative-rate generator, not exact stationarity at the noisy baseline. Irreducibility additionally requires that enough connecting rates remain positive, for example an error margin below the minimum rate on a known bidirected spanning subgraph.

For trace normalization of the raw row-reordered unit-Frobenius estimate (before the optional generator repair), put tau=−tr(W/||W||_F). For sqrt(n)delta≤tau/2, its Frobenius error after normalization is at most 2delta/tau+2sqrt(n)delta/tau². If instead normalizing the repaired generator, replace delta throughout this trace bound and its prerequisite by sqrt(n)delta; that repaired matrix is not generally unit-Frobenius. Neither normalization recovers an absolute physical clock.

With N iid state observations in each of m+1 settings, Hoeffding and a union bound give

eta=sqrt{log[2n(m+1)/alpha]/(2N)}

with probability at least 1−alpha. This produces a complete conditional sample requirement by imposing the displayed gamma, sigma and zeta inequalities and a numerical residual tolerance rho. There is no claim that these margins are uniformly bounded, that iid samples are physically free, or that a finite noisy sample can prove an exact dependence without the structural promise and separation margin.

## 9. Complexity and strongest existing methods

Exact rational rank computations, a polynomial number of graphic-matroid oracle calls, and the n²-variable reconstruction system use polynomial bit complexity in the rational input length. The complete-graph special algorithm is explicit polynomial enumeration. Under the noise-margin contract, singular values and the least-residual vector can be approximated to the requested absolute tolerances by standard polynomial-precision linear algebra. Runtime charges those tolerance bit lengths; sample cost can be very large as the physical margins shrink.

The principal combinatorial operation is old. Bixby and Cunningham, *Converting Linear Programs to Network Problems* (1980), https://doi.org/10.1287/moor.5.3.321 , recover network structure after row operations and column scaling. Seymour, *Recognizing graphic matroids* (1981), https://doi.org/10.1007/BF02579179 , provides the established graphic reconstruction primitive. Whitney's graph uniqueness and the classical graphic-matroid theory provide the three-connectivity step. A modern direct comparator using matroid reconstruction for an unlabelled inverse problem is *Reconstruction in One Dimension from Unlabeled Euclidean Lengths* (2024), https://doi.org/10.1007/s00493-024-00119-x . This proof does not claim those principles as new.

Markov static response and finite-edge response lines are also established: Aslyamov and Esposito (2024), https://doi.org/10.1103/PhysRevLett.133.107103 , and Bebon and Speck (2026), https://doi.org/10.1103/jcm3-57d8 . Steady-state perturbation inference predates this construction, including modular response analysis and its identifiability theory. The earlier labelled stationary-barrier argument supplied the cycle rigidity step used here.

The proposed acquisition distinction is that endpoint labels are not supplied: an unordered family of unknown local pair perturbations can reconstruct the physical named-state generator, under a three-connected spanning coverage promise. Direct transition trajectories still identify rates and their absolute clock without these controls. Calibrated reset-to-state experiments give W=rI−rP^−1 from n stationary snapshots and work at equilibrium, but supply global reset control and a known clock. Labelled edge-control reconstruction avoids the present graph-recognition and noise-margin burden. No end-to-end advantage over these stronger measurements has been established.

The result is a conditional blind-identification theorem and algorithm, not proof that unknown interventions are local, that such a family can be produced experimentally, or that this assembled contract has not appeared elsewhere. Priority and operational consequence remain open gates.
