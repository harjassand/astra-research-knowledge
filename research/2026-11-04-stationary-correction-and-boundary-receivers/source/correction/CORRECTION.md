# Correction: direct endpoint recovery by a classical maximum principle

4 November 2026. This corrects the significance and acquisition mechanism of the earlier blind stationary tomography packet. Its theorem remains valid, but its graphic-matroid reconstruction is unnecessary. A simpler same-data operation also weakens the sufficient graph assumption from 3-vertex-connectivity to biconnectivity. The maximum principle itself is established mathematics, with directly relevant stationary-response prior below. No priority claim is made for its inverse-problem application.

## 1. Exact operation and proof

Use the column convention for an irreducible finite Markov generator W: off-diagonal entries are nonnegative, 1ᵀW=0, and Wπ=0 with π>0. An intervention changes only the two directed rates on {a,b}; symmetric multiplication of those rates by an unknown positive factor is a special case. Let π′ be its stationary distribution and d=π′−π. Assume d≠0. Subtracting stationarity gives

W d = α(e_b−e_a), with α≠0.

Define h_i=d_i/π_i and L=W diag(π). Since L1=0, at every state i,

(Lh)_i = Σ_(j≠i) W_ij π_j (h_j−h_i).

Thus h is harmonic at every nontarget state. Assume, for this pair, that the baseline positive-rate support contains a spanning bidirected graph which remains connected after deleting either a or b. A spanning biconnected bidirected graph suffices simultaneously for every target pair.

Reverse the names a,b if necessary so α>0. At b the displayed sum is positive, so b cannot maximize h. At a it is negative, so a cannot minimize h. If a nontarget i maximized h, its harmonic equation, a sum of nonpositive terms with positive coefficients along bidirected edges, would force every neighboring value to equal that maximum. Propagate along a path from i to b avoiding a. All internal vertices are nontargets, so b would also maximize h, a contradiction. The analogous argument along a path avoiding b excludes a nontarget minimum. Hence

argmax_i h_i = a, and argmin_i h_i = b,

uniquely. Their unordered pair is the intervention target, regardless of its unknown amplitude or sign. Computing π′_i/π_i gives exactly the same extrema. This uses the measured state names directly and needs no graph reconstruction or row-permutation alignment.

## 2. Full generator reconstruction with the weaker assumption

Assume n≥3 and the selected distinct active bidirected pairs form a simple spanning biconnected graph. Every selected intervention has nonzero response; symmetric barrier controls therefore still require nonzero baseline current. Extra unperturbed transitions, including one-way transitions, are allowed.

Recover every pair by Section 1. Solve the homogeneous linear system in K:

1ᵀK=0, Kπ=0, and (Kd_e)_i=0 outside the recovered pair e.

The true W is a nonzero solution. Let H={x:1ᵀx=0}. Irreducibility makes W restricted to H invertible. For any solution K, the map A=K_H W_H^−1 preserves every selected incidence ray, because d_e=α_e W_H^−1 b_e. On a simple cycle, the unique dependence among incidence columns forces all ray eigenvalues to agree, including possible zero eigenvalues. In a biconnected graph, cycles linked by shared edges connect the entire cycle matroid, so the eigenvalue is a common scalar c. Incidence columns span H. Consequently K_H=cW_H; Kπ=0 extends this to K=cW on the full space.

The linear-system nullspace is therefore one-dimensional. Choose the sign with negative diagonal and nonnegative off-diagonal entries, and normalize −tr K=1 if desired. This determines all directed rates up to one positive clock scale. Exact rational division, comparisons, and Gaussian elimination give polynomial rational bit complexity. No assertion that biconnectivity is necessary for every possible physical inverse problem is made.

The same finite-control compatibility test from the earlier proof remains required if data are not simply promised to satisfy symmetric control: orient b_e=e_b−e_a, extract α from Vd_e=αb_e, and set D=(V_ba e_a−V_ab e_b)ᵀπ′. A positive nonunit symmetric factor exists exactly when D≠0 and t=1−α/D is positive and not one. The test is invariant under scaling V.

## 3. Noise and operational limitations

Let r=min_i π_i>0. Suppose each baseline and perturbed probability coordinate is known within η<r/2. For ĥ_i=π̂′_i/π̂_i−1,

|ĥ_i−h_i| ≤ 2η/r + 2η/r² = B.

Indeed split the ratio error into the numerator error divided by π̂_i and π′_i times the reciprocal-denominator error, using π′_i≤1 and π̂_i≥r/2. If the minimum gap, over all experiments, between the unique maximum and the second-largest h value and between the second-smallest value and the unique minimum is g>2B, the endpoint assignment is unchanged. Arithmetic error in the ratios must be added to B. This is a sufficient, conservative bound, not an optimal acquisition rate.

For independent stationary samples, coordinate concentration and a union bound provide η=sqrt(log(2n(m+1)/δ)/(2N)) from N samples for each condition. Correlated trajectories require an additional justified effective-sampling analysis. After target assignment, rate stability still depends on the nonzero singular gap of the labelled reconstruction system. Neither biconnectivity nor exact identifiability guarantees favorable finite-data conditioning. Small probabilities, nearly tied extrema, weak interventions, near-equilibrium currents and poorly conditioned rate reconstruction can make acquisition expensive.

The operation does not recover absolute time, verify locality of arbitrary uncontrolled interventions, identify hidden states, or supply unknown experimental access. It still assumes a fully observed common state coordinate system and separately accessible stationary laws.

## 4. Corrected strongest-baseline and significance assessment

Hunter, *Stationary Distributions and Mean First Passage Times of Perturbed Markov Chains*, Research Letters in the Information and Mathematical Sciences 3 (2002), 85–98, Corollary 4.1.2 and the discussion on page 93, explicitly places the extrema of relative stationary changes at the two perturbed destination states for a two-entry, single-row discrete-time perturbation. Its relative-response geometry is directly relevant to the forcing identity above. The CTMC pair-local proof and strictness condition are supplied here to avoid relying on a change of conventions. This is not a newly discovered maximum principle.

Primary full text: https://mro.massey.ac.nz/server/api/core/bitstreams/8b373271-6b75-456d-84ab-1ecfd6b7cd19/content

Thus the strongest same-data comparison is a classical relative-response maximum principle followed by labelled linear inverse reconstruction, rather than a difficult blind graph-learning problem. Established static-response formulas and the earlier cycle-ray rigidity calculation supply the remaining framework. The older comparison against general blind time-series network identification remains contextual, but is not the decisive baseline for endpoint acquisition.

The old packet's mathematical reconstruction remains correct. Its proposed combinatorial machinery should not be presented as an essential new enabling capability. The corrected outcome is a simpler exact inverse reconstruction under explicit control and observability assumptions, with weaker sufficient connectivity. We have not established literature priority for the combined inverse theorem, an experimental advantage, or transformative practical significance. The prior packet should be read together with this correction rather than promoted independently.
