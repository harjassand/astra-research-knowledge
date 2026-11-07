# Principal independent initial construction

Date: 7 November 2026. This records the principal construction developed before peer results were opened. An incoming auditor freeze notification arrived immediately before this file was written; the constructions below were already developed and are recorded without importing that notification's construction.

## Target and governing capital

Replace a stipulated macroscopic Markov cooling primitive by finite local physical collisions, and prove logical protection using local weighted inequalities rather than global dynamics approximation. Governing previous theorem: sources/PRIOR_THERMAL_SERVICE_THEOREM.md; previous positive-rate code, dual-sector stabilizer energy, warm basin, short selected-CCZ pulses and isolated encoded ports retain their exact scopes. The old bilayer, three-body microscopic clock and present stabilized-code service are separate contracts.

## Independent candidate 1: exact thermal collisions

For a Pauli P_a and positive integer d, set A=P_a Pi_{a,-d}; A dagger=P_a Pi_{a,+d}. Couple a fresh qubit of gap Jd, thermal excitation r_d=(1+exp(beta Jd))^{-1}, by H_int=kappa(A tensor sigma_plus+A dagger tensor sigma_minus). It conserves memory plus ancilla energy. At angle theta, q=sin(theta)^2, the reduced update has downward probability (1-r_d)q, upward r_d q. For V=exp(sU), its exact Heisenberg action is V[1+q(1-r_d)(exp(-sd)-1)Pi_down+q r_d(exp(sd)-1)Pi_up]. No Markov limit is needed.

Color full read/change neighborhoods into a fixed number of layers. A full round has bounded circuit depth and O(n) local gates. All ancillas start independently thermal. On an initial syndrome of low energy U, at least kappa U chosen labels improve. Represent transitions with independent uniforms. A downward-success coin of probability q/2 is guaranteed when an initially active label remains active; any flip is dominated by an independent coin of probability at most 2q; an upward flip by probability q exp(-beta J). An initial improving label can be spoiled only by an earlier neighboring flip. Thus a trajectory obeys Delta U <= -sum_active Z_h + sum_neighbor_pairs Z'_j Z_h + D sum Z_h^+. Apply Holder to three terms and edge-color dependency pairs into bounded matchings. Candidate bound: Phi_round^* exp(sU) <= exp[-a q U+(C_1 q^2+C_2 q exp(-beta J))n] exp(sU), a=kappa(1-exp(-3s))/6. Exact constants and coin construction still require checking. This is a candidate until that check and logical-basin closure.

## Independent candidate 2: multiplicative local robustness

Let W be an ideal bounded-depth Stinespring block on memory and local ancillas. W dagger exp(sU) W is the exponential of a commuting sum of bounded positive terms with bounded enlarged supports. In the interaction frame of W, a local implemented generator error N_X has the same bounded-body property. Factor the energy terms disjoint from X. Complete cb norm control and bounded local energy yield a relative quadratic-form inequality N_X^*F <= C_s ||N_X||cb F, F=W dagger exp(sU)W. Summing a per-site integrated budget eta gives E_error^* F <= exp(C_s eta n)F. Hence implemented blocks satisfy tilde Phi^* exp(sU) <= exp(C_s eta n) Phi^* exp(sU). Fixed local errors affect the source term in a Lyapunov inequality, without requiring exp(-cn) global simulation accuracy.

Local reset channels admit a related comparison: the Choi matrix of a full-rank thermal replacement R_tau is positive definite; sufficiently small local diamond error implies CP order tilde R <= (1+C epsilon)R_tau, with constants depending only on fixed local dimension and lambda_min(tau). Product local reset channels then cost exp(C epsilon n). This is a complete channel statement with arbitrary reference, but requires fresh independent environmental modules. Reduced-channel accuracy does not establish a joint system-bath renewal contract.

## Main unresolved operation

An energy moment bound at round endpoints does not by itself establish logical identity across a trajectory that exits and returns. Projections at each microstep make the future observable nonlocal and obstruct a naive finite-depth comparison. Possible repair: use inner/outer energy cutoffs, sparse upward-branch instruments and local-fault expansions to bound all intermediate excursions, then construct a positive subchannel on the common logical module. Need distinguish sparse CP instrument faults from general coherent retained-bath errors. No completed service claim until this is closed.

## Explicit cooling-source avenue

Use Merkli's uniform-in-time theorem only for a constant-dimensional reset cell coupled to its own fresh thermal bosonic reservoir. Choose fixed coupling for fixed reset precision, and fixed reset waiting time. A qubit diamond estimate follows from fixed-dimensional norm conversion. A reservoir must not later return to interact with memory. One-use reset modules or a flow-through thermal source avoid illicit reuse of an initially product-bath theorem, but all thermal cells, bath renewals, switching, discarded entropy and factory space/time must be charged. Idle preprepared cells cannot be presumed noiseless for the whole service lifetime.

## Capability and obstruction tests

Any finite collision/reset/control schedule compiles to an ordinary active circuit with constant overhead per fixed local module. Scalability alone therefore does not earn an advantage over matched active fault tolerance. Native selected diagonal CCZ operations do not establish universal processing. Encoded noisy ports can add paid active processing but those resources already enable known schemes. Potential new foundational contribution is a complete local weighted-drift implementation theorem, if the basin/logical and physical source contracts close. Useful small-body geometry, honest reusable cooling with memory, a noisy clock/schedule contract, and full-cost gain remain open.

## Status

Exact single collision: elementary proved operation, subject to full algebra check.
Round drift and complete physical service: candidates.
Weighted local comparison: proof mechanism to audit, not a claimed novel established theorem yet.
Microscopic reusable factory and resource advantage: open.
