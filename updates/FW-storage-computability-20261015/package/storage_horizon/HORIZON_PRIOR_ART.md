# Horizon truncation: primary-source comparison

Research date: 15 October 2026. Scope: targeted comparison for an explicit finite-horizon approximation of free-duration constrained required-supply/available-storage values associated with the quartic G in SOURCE_QC_REPORT.md. Historical novelty of the precise proposed theorem remains unverified. This is not an exhaustive priority search.

## Assessment

The broad argument is a quantitative cut-and-paste/turnpike mechanism with substantial prior art. A defensible narrower contribution is the explicit finite-horizon modulus for this particular degenerate, non-polyconvex quartic on the full critical trace space, including mean drift. The sources below do not by themselves establish that exact result; that distinction is not evidence that nobody has proved it elsewhere.

## 1. Closest abstract storage theorem

Arjan van der Schaft, “Cyclo-Dissipativity Revisited,” IEEE Transactions on Automatic Control 66 (2021), 2920–2924, Theorem III.3.

- DOI: https://doi.org/10.1109/TAC.2020.3013941
- Primary full text: https://pure.rug.nl/ws/portalfiles/portal/202805011/Cyclo_Dissipativity_Revisited.pdf

Under reachability from and controllability to a reference state, nonnegative closed-loop supply is equivalent to the constrained available-storage/required-supply inequality. Both constrained value functions are signed storage functions; the proof concatenates entry and return paths. It does not supply a quantitative horizon-truncation modulus.

Use **constrained available storage**, with the return endpoint fixed at zero, rather than unrestricted available storage. The paper distinguishes these functions explicitly.

### Signed cyclodissipativity caveat

In the supplied G report, p₀(U₊)<0 and quartic homogeneity imply that p₀ is globally unbounded below. Therefore Willems’s original nonnegative-storage/minimum-storage-reference-state framework does not apply literally on the full state space. The natural structure is cyclodissipativity, or signed/pre-dissipativity terminology where defined, based on nonnegative closed-loop action. Endpoint-dependent coercivity comes from gluing a return path. A bounded endpoint ball does not automatically bound every intermediate state of every arbitrary-duration path.

## 2. Closest infinite-dimensional turnpike mechanism

Emmanuel Trélat and Can Zhang, “Integral and measure-turnpike properties for infinite-dimensional optimal control systems,” Mathematics of Control, Signals, and Systems 30:3 (2018), Theorem 1, Remark 5, Theorem 2.

- DOI: https://doi.org/10.1007/s00498-018-0209-1
- Primary full text: https://www.ljll.fr/trelat/fichiers/TrelatZhang_MCSS2018.pdf

Theorem 1 uses bounded-time entry/exit controllability to construct bridge–turnpike–bridge competitors. Remark 5 replaces bounded running costs by uniformly finite-cost controllability in autonomous problems. Theorem 2 derives a quantitative measure-turnpike bound from strict dissipativity and bounded storage: time away from an ε-neighborhood is bounded through the dissipation modulus. These are close precedents for “coercive energy bound ⇒ good slice ⇒ cheap bridge.”

The stated conclusions concern normalized long-time values or turnpike occupancy, not the absolute error between free-duration constrained storage and its finite-horizon truncation. Global storage bounds, the admissible-state framework, and controllability assumptions must be checked rather than silently imported. Theorem 2 uses free endpoint states so that a steady-state competitor is admissible; fixed endpoint variants need the bridge hypotheses.

## 3. Value-function convergence and endpoint patching

David Angeli and Lars Grüne, “Dissipativity in Infinite Horizon Optimal Control and Dynamic Programming” (2024), Theorems 5.4–5.5 and Proposition 5.9.

- Primary article: https://link.springer.com/article/10.1007/s00245-024-10103-y

They prove uniform convergence of modified Bellman iterations under equicontinuity and existence of a continuous shifted-Bellman solution. Proposition 5.9 derives equicontinuity by patching trajectories using uniform incremental controllability continuous in cost. The setting is discrete-time, finite-dimensional, with compact state/input constraints. This does not automatically cover a bounded ball of W^(3/4,4), which is not strongly compact, nor the specific free-duration cutoff. It reinforces that controlled endpoint patching and value-function convergence are established techniques.

## 4. Classical lineage

Jan C. Willems, “Dissipative dynamical systems, Part I: General theory,” Archive for Rational Mechanics and Analysis 45 (1972), 321–351.

- Primary article: https://doi.org/10.1007/BF00276493
- Author-hosted original PDF: https://homes.esat.kuleuven.be/~sistawww/smc/jwillems/Articles/JournalArticles/1972.1.pdf

This is the classical origin of available storage, required supply, and their extremal-storage inequalities. Cite for lineage, with the signed/cyclodissipative qualification above. The targeted comparison did not establish an explicit general truncation rate from this original paper.

## What the proposed G theorem still has to establish

These are deductions about the supplied setup, not claims quoted from the prior-art papers:

1. Uniform gradient-energy control of approximate minimizers despite arbitrarily long duration.
2. A good slice controlled in a topology strong enough to permit a quantitatively cheap entry/return.
3. A bound for the slice’s mean using its distance from the prescribed terminal endpoint. A mean-zero Poincaré estimate alone cannot handle this neutral mode.
4. An explicit ramp duration balancing 120[|B|²|C|²/L + |C|⁴/L³].
5. A uniform absolute-value error bound over a critical trace ball, without compactness or existence of an optimizer.

The proposed route uses a low-transverse-energy slice in the last H units, a mean ramp plus a unit entry strip, and a lower bound on the dropped prefix obtained by closing it with a cheap return. The estimate |C|⁴ ≤ H³E uses the prescribed terminal mean and the energy of the retained terminal segment. The resulting admissible duration is bounded by H+1+L. The proof and explicit constants should be checked independently of this literature comparison.

## Suggested positioning

“We obtain an explicit horizon-truncation estimate for the constrained storage values associated with G. The proof quantitatively implements standard cyclodissipative concatenation and turnpike slicing, with a separate treatment of the neutral mean mode.”

Avoid claiming a new general turnpike principle or a finite evaluation algorithm. A horizon cutoff alone does not discretize the remaining infinite-dimensional variational problem, particularly given the supplied report’s finite-Fourier obstruction.
