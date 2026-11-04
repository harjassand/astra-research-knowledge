# Independent adversarial audit

4 November 2026. Reviewed PROOF.md SHA-256: a5946b5d6ac0e86c763f165b112208dd171db64d74322aac8126606b7f9da917.

## Verdict and scope

The stated exact identifiability theorem, finite-control consistency test, and conditional statistical bound pass this independent algebraic review. No counterexample was found under the declared assumptions. This is not a certification of novelty, physical realizability, experimental advantage, or general hidden-state inference. The proof's opening “pending independent audit” status is superseded by this companion audit; literature priority remains unresolved.

The distinction between a sufficient topology for the physical inverse problem and a necessary topology for its unrestricted linear ray equations is important. A positive generator and matching response rays do not alone certify the claimed finite symmetric controls. These qualifications were communicated to the author and the finite-control check and broader edge-local interpretation were incorporated before the reviewed version was frozen.

## 1. Response identity, signs and directed rates

With column generators and b=e_b−e_a, the edge contribution b uᵀ has exactly the required two off-diagonal entries and their negative diagonal compensators. Subtracting stationary equations gives Wd=−(t−1)(uᵀπ')b, with the sign as written. W restricted to H={1ᵀx=0} is invertible because its sole nullvector is the normalized positive π, outside H. A zero response is equivalent to zero baseline edge current for a nonunit symmetric intervention. A nonzero response cannot have a vanishing coefficient in this identity.

For candidate V, A=V_H W_H^−1 preserves every measured incidence ray. Cycle dependencies force its eigenvalues to agree; connectivity through shared cycles propagates this equality. Spanning then implies A=cI. Conservation and Vπ=0 extend this identity to all of Rⁿ. This reasoning does not require V_H to be invertible. Consequently the unrestricted homogeneous reconstruction really has a one-dimensional nullspace, not merely uniqueness among nonsingular candidates. Positive off-diagonal rates force c>0. The procedure therefore recovers the two directed rates separately up to a common positive clock, rather than merely their sum or unoriented currents. Trace normalization only chooses units.

The triangle probabilities, response vectors, current direction comparison, current 1/3 and affinity log 8 were checked directly and are consistent with this convention.

## 2. Exact graph boundary

For a connected spanning measurement graph, let its graphic matroid have c components, treating a bridge as a singleton component. The incidence spans of these components form a direct sum of H. Indeed, any dependence among incidence columns is a circulation and decomposes into simple cycles, each lying in a single matroid component. Thus a putative relation between the component spans vanishes within each component separately.

Every incidence-ray-preserving linear map is scalar on each such component span, by the cycle argument, and conversely any independently chosen scalars on these direct summands preserve all rays. Hence the unrestricted ray reconstruction has exactly c degrees of freedom. Connected cycle matroid is necessary and sufficient for uniqueness of that unrestricted linear system. It is only a sufficient condition for the full physical inverse problem when additional known sparsity, zero-current equations, calibrated controls, or other measurements are available. The proof appropriately refrains from claiming the latter necessity.

An exact counterexample shows why merely spanning interventions are insufficient even with positive physical generators. Let

W=[−3,1,2; 2,−3,1; 1,2,−3],

V=[−3,1,2; 19/10,−16/5,13/10; 11/10,11/5,−33/10].

Both have stationary distribution (1,1,1)/3 and positive rates on the complete triangle. Observe only edge interventions 12 and 23. For W, doubling these barriers separately produces

π^(12)=(10,13,12)/35,  π^(23)=(12,10,13)/35.

The nonscalar generator V produces exactly the same two snapshots by symmetric barrier factors 13/6 and 128/51, respectively. To check: Vd_12=(1,−1,0)/5, its edge flux at π^(12) is 6/35, and Vd_23=(0,11/50,−11/50), its edge flux at π^(23) is 51/350. Substitution into the finite-response equation gives these positive factors. This is a counterexample to a stronger tree-spanning assertion, not to the theorem's cycle-connected hypothesis.

The figure-eight block-speed ambiguity, bridge zero-current argument, detailed-balance blindness, global time ambiguity, and outgoing-state scaling formula are valid. Hidden channels remain an independent obstruction to a thermodynamic interpretation.

## 3. Finite-control consistency and stronger controls

For recovered W and nonzero d with Wd=αb, set D=uᵀπ'. The proposed symmetric control exists precisely when D≠0 and t=1−α/D is positive and nonunit, subject also to normalized positive snapshots and a valid reconstructed generator. Necessity is the stationary identity. Sufficiency follows by direct substitution and irreducibility of the positively rescaled generator. Both α and D scale with W, so t is clock invariant. For d=0 the compatibility condition is j=0, not a division by D.

This test is essential: an abstract ray fit is not a finite-experiment certificate. Numerical division near D=0 requires a separate confidence analysis.

The Section 11 extension is valid. An arbitrary change confined to the two rates of one edge has image in span(b), whether or not its forward and reverse multipliers match. A nontrivial change to a single directed rate cannot leave the stationary law unchanged, because its source probability is positive. Thus symmetric-barrier equilibrium blindness must not be generalized to all edge-local control. No independent control magnitude calibration is needed for the ray theorem, but exact locality is still a strong physical requirement.

## 4. Noise and computational cost

The stated perturbation argument is valid: a unit least-residual vector for L+E has residual at most 2||E|| under L; projecting perpendicular to ker L bounds its sine angle by 2||E||/σ. Choosing the aligned sign yields Euclidean error at most 2√2||E||/σ. This is a projective error bound. Finite noisy positivity/sign decisions, trace normalization, relative errors on tiny rates, and classifying exact zero responses need additional margins.

For m+1 stationary settings, coordinatewise Hoeffding plus a union bound gives the stated η. Each response error is at most 2η even though responses share a baseline. There are n² uncertain stationarity coefficients and mn(n−2) response coefficients, so ||E||_F≤η sqrt[n²+4mn(n−2)] is correct in the declared row convention. It is conservative, not an optimized information bound. Effective independent samples, equilibration times and intervention cost are explicitly unpaid by the iid formula; σ can become arbitrarily small.

The exact rational system has n² variables and polynomially many constraints and can be solved in polynomial bit complexity in its rational input length using standard exact linear algebra. This does not mean exact stationary probabilities can be measured at polynomial physical cost, nor does it establish a conditioning-independent finite-precision algorithm.

## 5. Strongest comparators and priority limits

The forward static-response identity is established: [Aslyamov and Esposito, Physical Review Letters 133, 107103 (2024)](https://doi.org/10.1103/PhysRevLett.133.107103). The particularly close finite-control comparator is [Bebon and Speck, Physical Review Letters 136, 137401 (2026)](https://doi.org/10.1103/jcm3-57d8), [author manuscript](https://arxiv.org/abs/2602.20321). Their exact finite-edge mutual linearity covers arbitrary changes to either or both directed rates. The forward response-line observation must not be advertised as new.

Steady-state perturbation tomography is much older: [Kholodenko et al., PNAS 99, 12841–12846 (2002)](https://doi.org/10.1073/pnas.192442699) reconstructs normalized interactions through modular response analysis. The present operation is a particular exact linear Markov inverse problem with known incidence directions and cycle dependencies aligning otherwise unknown scales. This is a precise distinction, not a proven novelty or superiority claim. Projective-frame uniqueness and graphic-matroid cycle dependence are classical underlying mathematics.

The reset comparator is especially strong. Established reset theory includes [Rose, Touchette, Lesanovsky and Garrahan, Physical Review E 98, 022129 (2018)](https://doi.org/10.1103/PhysRevE.98.022129). For known Poisson reset rate r and selectable reset state i, stationarity directly gives P=r(rI−W)^−1 and W=rI−rP^−1. This checked inversion works at equilibrium and supplies an absolute clock, without the original graph's cycle condition. The algebra is an analytical comparator, not a claim that this source demonstrated an inverse instrument. Global reset and a calibrated clock differ materially from uncalibrated local barrier controls.

Well-resolved trajectories already yield rates from transition counts and residence times, with an absolute clock and no barrier interventions. In a driven unicyclic system, independently known forward/backward rate ratios plus a nonzero measured stationary current and π also determine every rate directly. At zero current the resulting formula is 0/0 and does not provide that recovery. Comparisons must charge these extra observations or calibrations explicitly, rather than claim a universal sensing advantage.

## Conclusion

The earned result is an exact conditional inverse theorem, an explicit finite-control certificate, and a transparent conditioning-dependent sampling bound. It survives the counterexamples tested here because its topology and control assumptions are restrictive and necessary for the particular proof. Neither priority, practical implementation, nor transformative consequence has been established. Further useful work is experimental control validation or a genuinely matched acquisition-cost comparison, not relabeling this algebra as a demonstrated new capability.
