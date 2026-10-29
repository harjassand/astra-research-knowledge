# Physical response information: strongest primary comparators

2026-10-29. Targeted source check supporting `ENERGY_CLOCK_RESPONSE_OBSTRUCTION.md`. This is not an exhaustive historical survey. Only primary mathematical or physics sources are used for the claims below.

## The exact collision: the equilibrium-form response is already known

[Christian Maes and Bram Wynants, *On a Response Formula and Its Interpretation*, Markov Processes and Related Fields 16, 45–58 (2010)](https://www.math-mprf.org/journal/articles/id1201/), with [inspected author preprint arXiv:0910.2320](https://arxiv.org/pdf/0910.2320), explicitly studies

\[
W_h(x,y)=W(x,y)\exp\{h[bV(y)-aV(x)]\},\quad a+b=\beta.
\]

Its equation (10) is exactly the departure-rate case \(a=\beta,b=0\). The discussion following equation (20) explicitly states its equilibrium-form FDT and the all-orders stationary reweighting \(\rho_h\propto\rho e^{\beta hV}\), even when the unperturbed process is far from equilibrium. This is a direct collision, not a merely adjacent precedent. The nonuniqueness of the kinetic rule at fixed energetic ratio is also explicit. The present work should claim neither a new non-equilibrium FDT nor discovery that the energetic ratio underdetermines response.

## Strongest general theorem for the basic mechanism

[Amir Dembo and Jean-Dominique Deuschel, *Markovian perturbation, response and fluctuation dissipation theorem*, Annales de l'Institut Henri Poincaré, Probabilités et Statistiques 46, 822–852 (2010), DOI 10.1214/10-AIHP370](https://www.numdam.org/item/AIHPB_2010__46_3_822_0.pdf).

Theorem 2.10 derives the response/covariance identity for perturbations changing the invariant measure in a specified direction. Proposition 3.1 constructs the time-change family with generator \(e^{-f}L\); section 5 characterizes broad response freedom for jump processes. These results do not require the unperturbed semigroup to be symmetric. Their invariant-measure FDT is therefore the strongest conventional explanation of why canonical stationary reweighting alone does not identify thermodynamic equilibrium. The new note's causal observed-path pushforward is an application of this mechanism to hidden-model equivalence, rather than a replacement response theory.

## What physically specified inertia adds

[Marco Baiesi, Eliran Boksenbojm, Christian Maes, and Bram Wynants, *Nonequilibrium Linear Response for Markov Dynamics, II: Inertial Dynamics*, inspected author manuscript dated 2009-12-03](https://fys.kuleuven.be/english/staff/christ/files/pdf/pub/fdr-ii.pdf), introduction and section 3.

This work treats positions and momenta, with physical reversal changing momentum sign. The perturbation \(U(q)\mapsto U(q)-hV(q)\) is explicitly implemented as an additional force \(h\nabla V\) in the momentum equation, with bath friction and noise specified separately. Its nonequilibrium response contains entropic and dynamical-activity terms. This is a materially stronger action contract than simply naming a field conjugate to a coarse energy. The source does not justify imposing an all-even jump-rate tilt on a hidden odd-variable model; its equations show why the actual kinetic action must be supplied.

## Strongest quantitative conventional route under that physical contract

[Takahiro Harada and Shin-ichi Sasa, *Energy dissipation and violation of the fluctuation-response relation in nonequilibrium Langevin systems*, Physical Review E 73, 026131 (2006), DOI 10.1103/PhysRevE.73.026131; inspected arXiv:cond-mat/0510723](https://arxiv.org/pdf/cond-mat/0510723), introduction, equation (5), and the beginning of section II.

For its declared Langevin bath and force interface, the Harada–Sasa equality already gives the dissipated power from velocity fluctuations, mean motion, and response to the applied force:

\[
J=\sum_i\gamma_i\left[\bar v_i^2+
\int\frac{d\omega}{2\pi}\big(\widetilde C_{ii}(\omega)-2T\operatorname{Re}\widetilde R_{ii}(\omega)\big)\right].
\]

The derivation covers inertia as well as its overdamped limit. Its physical assumptions include the bath interpretation of eliminated degrees of freedom and the known force, friction, and noise structure. This is a stronger quantitative result than a generic response-based dissipation bound when that interface is actually available. Finite-bandwidth acquisition, noise, derivative estimation, and unobserved dissipative channels still have to be treated at their actual scope. The equality is not imported into an arbitrary hidden finite-state model by fitting a response curve.

The original [Harada–Sasa PRL 95, 130602 (2005)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.130602) was checked for metadata and abstract; the detailed mathematical comparison above uses the accessible primary 2006 derivation.

## Current detailed-balance-from-measurements theorem

[Eugenia Franco, Bernhard Kepka, and Juan J. L. Velázquez, *Characterizing the Detailed Balance Property by Means of Measurements*, Archive for Rational Mechanics and Analysis 250, article 25 (2026), DOI 10.1007/s00205-026-02183-7](https://link.springer.com/article/10.1007/s00205-026-02183-7), published April 3, 2026.

Their response functions are propagator entries measured after injecting or preparing one state, not derivatives under a thermodynamic energy field. Reciprocal response proportionality is necessary for ordinary detailed balance. Theorem 1.1 summarizes a sufficiency result requiring no cut vertices and stability under an admissible class of microscopic rate perturbations. Definition 4.1 specifies that class; Example 3.12 and section 4 exhibit failures without the extra conditions.

This theorem does not turn a finite collection of observed energy-field directions into robustness over an open microscopic rate class. Nor does ordinary weighted-generator symmetry identify generalized entropy when physical parity is unspecified. The five-state example in the new note has a hidden cut vertex, deliberately consistent with their obstruction. More generally, exact closure under observable clock changes says nothing about stability under their full admissible perturbation class.

## Research consequence

A weak physical response can break the passive completion if its calibrated kinetic action and thermodynamic interpretation exclude the competing completion. A failed FDT can then falsify equilibrium even with odd hidden states. But an operation that merely changes an observer-measurable clock cannot do so: its entire data law is already determined by the passive law. The exact arbitrary-protocol theorem and finite counterexample make that distinction explicit.

The next claimed addition must lie in acquiring or supplying a kinetic operation beyond that class, controlling its precision, or proving a consequence unavailable to the conventional FDT/Harada–Sasa/inverse-network route under the same information. The source check supports abandoning a generic response-first destination without treating physically specified response methods as ineffective.
