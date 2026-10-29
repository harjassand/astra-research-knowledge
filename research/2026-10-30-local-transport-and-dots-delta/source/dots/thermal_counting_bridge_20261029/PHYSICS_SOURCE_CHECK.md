# Primary-source comparison for the thermal approximation

Checked 2026-10-29. This was a focused check, not an exhaustive novelty search.

## Directly read primary source

**Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe, Shuchen Zhu, _Theory of Trotter Error with Commutator Scaling_, Physical Review X 11, 011020 (2021).** Enhanced author version: _A Theory of Trotter Error_, arXiv:1912.08854v3.

* https://arxiv.org/pdf/1912.08854
* https://doi.org/10.1103/PhysRevX.11.011020
* Exact relevant places: abstract; introductory theorem Eq. (1), pp. 5–6; Section 3 on multiplicative/exponentiated error; Section 4.3, Lemma 14 and Eqs. (102)–(105), pp. 32–33; Appendix I, Eq. (287), p. 68.

The generic imaginary-time bound includes an exponential of time times the sum of summand norms. Their partition-function application uses relative eigenvalue perturbation and a multiplicative error operator involving conjugation by the full Hamiltonian. Equation (105) still contains an extensive-norm exponential. Therefore that displayed result, without an additional locality argument, does not directly supply the constant-in-volume step count required here. It is clear methodological precedent for multiplicative rather than additive errors, and for comparing spectra before partition functions. The proof in `PHYSICS_THEOREM.md` instead uses a relative **left** generator whose conjugations are entirely finite depth, then the Hermitian-part singular-value estimate and operator logarithm.

## Historical mapping precedent located, not relied on for our uniform bound

**Masuo Suzuki, _Relationship between d-Dimensional Quantal Spin Systems and (d+1)-Dimensional Ising Systems_, Progress of Theoretical Physics 56(5), 1454–1469 (1976).**

* https://doi.org/10.1143/PTP.56.1454
* https://academic.oup.com/ptp/article/56/5/1454/1860476

The primary publisher search result describes a general quantum/classical partition-function relation based on generalized Trotter products. The full publisher article was not retrievable through the web tool: its redirect to a CDN was inaccessible and marked non-retryable. Therefore no particular uniform-error theorem from this article is asserted or used.

## Relevant rigorous special-model precedent located

**Frank Göhmann, Salvish Goomanee, Karol K. Kozlowski, Junji Suzuki, _Thermodynamics of the spin-1/2 Heisenberg–Ising chain at high temperatures: a rigorous approach_, Communications in Mathematical Physics 377, 623–673 (2020), arXiv:1811.12020.**

* https://arxiv.org/abs/1811.12020
* https://doi.org/10.1007/s00220-020-03749-6

The primary abstract explicitly treats a high-temperature regime and rigorously justifies interchange of thermodynamic/Trotter limits and related transfer-matrix claims for the XXZ chain. This is not used as an all-temperature, arbitrary-graph theorem. Our finite-volume density bound does not rely on quantum transfer matrices or interchangeable infinite limits.

## Retrieval limitations, with exact scope

The author-hosted Childs PDF initially timed out; the arXiv copy was successfully read instead. APS's fulltext endpoint for _Partition-function estimation: Quantum and quantum-inspired algorithms_, DOI 10.1103/PhysRevA.107.012421, returned HTTP 401; that endpoint was not retried and its unread theorem is not relied upon. These do not block the self-contained proof.

## Conclusion

No directly read source was found already stating the exact arbitrary-bounded-degree, all-fixed-beta, volume-uniform bound used here. This is **not** evidence of novelty. The saved elementary proof closes the mathematical obligation without requiring a novelty finding. The computational consequence still requires separate scrutiny of the exact-counting theorem, constant-precision rounding, and linear-size signed-weight compilation.
