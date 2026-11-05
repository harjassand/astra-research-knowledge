# Sources, standard inputs, and comparison

## Analytic inputs used

1. **Positive-field Ising uniqueness.** J. L. Lebowitz and A. Martin-Löf, “On the Uniqueness of the Equilibrium State for Ising Spin Systems,” *Communications in Mathematical Physics* 25 (1972), 276–282. https://sites.math.rutgers.edu/~lebowitz/PUBLIST/jll.pub_83.pdf . Its Theorem 1 together with the Lee–Yang theorem gives uniqueness at nonzero uniform field. This input is used for the ordinary comparison Ising model only.

2. **Lee–Yang theorem.** T. D. Lee and C. N. Yang, “Statistical Theory of Equations of State and Phase Transitions. II. Lattice Gas and Ising Model,” *Physical Review* 87 (1952), 410–419. https://doi.org/10.1103/PhysRev.87.410 . Supplies the familiar nonzero-field differentiability input for the ordinary ferromagnetic Ising comparison.

3. **Stochastic comparison.** R. Holley, “Remarks on the FKG Inequalities,” *Communications in Mathematical Physics* 36 (1974), 227–231. https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/holley.pdf . The manuscript gives the common-uniform heat-bath comparison directly; it does not assume FKG or attractiveness of the target induced interaction.

4. **Polymer expansion.** R. Kotecký and D. Preiss, “Cluster expansion for abstract polymer models,” *Communications in Mathematical Physics* 103 (1986), 491–498. The manuscript explicitly checks the criterion with an exponential size margin, uniformly after anchors are forbidden.

5. **Two-replica disagreement uniqueness.** J. van den Berg, “A uniqueness condition for Gibbs measures, with application to the 2-dimensional Ising antiferromagnet,” *Communications in Mathematical Physics* 152 (1993), 161–166. https://ir.cwi.nl/pub/2298/2298D.pdf . Theorem 1 states the independent-realization no-infinite-disagreement criterion. The manuscript supplies the finite-component swap proof and covariance extension in its own local representation.

6. **Disagreement percolation framework.** J. van den Berg and C. Maes, “Disagreement Percolation in the Study of Markov Fields,” *Annals of Probability* 22 (1994), 749–763. https://ir.cwi.nl/pub/1472/1472D.pdf . This is established methodology, not a novelty claim.

7. **Conditional auxiliary mixing.** The Dobrushin uniqueness/comparison criterion is used only after an explicit single-edge influence calculation. Appendix B proves the row sum is at most 6ta<0.0006 and describes the resulting geometric influence-path bounds.

## Comparison and limits of novelty

- Á. Perales-Eceiza, T. Cubitt, M. Gu, D. Pérez-García and M. M. Wolf, “Undecidability in Physics: a Review,” *Physics Reports* 1138 (2025), 1–29, https://arxiv.org/abs/2410.16532 , surveys the surrounding undecidability results and open finite-temperature/noise questions. It does not supply the construction proved here.

- J. Bausch, T. S. Cubitt, A. Lucia, D. Pérez-García and M. M. Wolf, “Size-driven quantum phase transitions,” *PNAS* 115 (2018), 19–23, https://doi.org/10.1073/pnas.1705042114 , supplies an earlier quantum example of noncomputably growing crossover scales. This manuscript does not claim that general phenomenon is new.

- L. Gayral, M. Sablik and S. Taati, “Characterisation of the set of ground states of uniformly chaotic finite-range lattice models,” *Nonlinearity* 38 (2025), 075011, https://doi.org/10.1088/1361-6544/addbb8 , establishes broad computability statements for pressure and Gibbs sets and studies zero-temperature chaoticity. Pressure computability is compatible with undecidability of the uniqueness property considered here.

- Fawzi, Fawzi and Scalet, “Certified algorithms for equilibrium states of local quantum Hamiltonians,” *Nature Communications* 15, 7394 (2024), https://arxiv.org/html/2311.18706v2 , give certified equilibrium algorithms. Their observable decision promise requires all translation-invariant states to lie on one side of a threshold or all to lie on the other. The nonhalting branch here contains both positive and negative magnetization states, so it does not satisfy that promise. This established computability result is therefore not a contradiction.

- M. Gu, C. Weedbrook, Á. Perales and M. A. Nielsen, “More Really is Different,” *Physica D* 238 (2009), 835–839, https://arxiv.org/pdf/0809.0151 , and M. Gu and Á. Perales, “Encoding Universal Computation in the Ground States of Ising Lattices,” *Physical Review E* 86, 011116 (2012), https://arxiv.org/abs/1204.1084 , concern ground-state encodings. They are close conceptual predecessors but do not supply the positive-temperature all-Gibbs uniqueness result here.

The proposed contribution is the finite-integer-energy classical construction whose accepting certificates trigger a full all-Gibbs uniqueness and connected-clustering distinction at fixed positive temperature. The paper includes the complete finite compiler and analytic bridge, rather than appealing to a numerical phase diagnosis. The literature comparison is not an externally verified priority claim.

**Status:** Research proof with independent internal mathematical review only. External peer review and formal machine verification remain outstanding.
