# Independent review: cold odd-interaction selection and routing

Verdict: scoped mathematical PASS, including the explicit ordinary generalized-amplitude-damping comparator. Not a free redesign of a physical bath, not an arbitrary-input result, and not a new whole simulator.

Fully read source: ODD_INTERACTION_COLD_CHANNEL_AND_ROUTING.md, SHA-256 2256767076818bb2666ec87960aff112106521538fe611e8a33bc23578eebf1e. Review date: 2026-10-31. It receives the separately reviewed first-corrector identity.

## Selection and complete logical error

Odd K and source-off-diagonal F imply QVPQ=0. If each supplied jump has output wholly in P or wholly in Q, L†FL=0 individually. Thus B=0 exactly, even with QLQ recycling. The product of two off-diagonal source operators is block diagonal, so A=VF−P_embed D is QQ-supported, not only zero in stationary average. Its norm bound 8bs gives the expectation bound 8bs E/g. The last residual [L0,F]−FD is off-diagonal, of norm at most gamma0=2d/g+8bs^2, and consequently costs 2gamma0 sqrt(E/g). These support and expectation estimates remain valid with arbitrary references.

E0=0 plus H>=gQ forces an actual pure dark source marginal and therefore a product with the system/reference. It is an essential cold-source input premise. System-only instruments preserve unconditional source energy, so E<=4C^2/(lambda kappa^2) holds throughout. The initial endpoint corrector vanishes; the actual final-state endpoint costs 8sC/(lambda kappa sqrt(g)). Integrating A and the last residual, and adding the off-diagonal control defects, gives exactly the displayed coefficient

    8sC/(kappa sqrt(g)) + 32bs C^2 T/(kappa^2 g)
       +4C(gamma0 T+sum nu_j)/(kappa sqrt(g))

multiplying 1/lambda. Duhamel must use actual states before each insertion and effective backward contractions after it, as in the accepted first-corrector review. No postselected-outcome guarantee is implied. The inverse-rate estimate is for lambda>0. Source interventions and initially excited inputs do not inherit this cold bound.

## Changed-generator construction and access

Splitting L into PL and QL keeps sum L†L and therefore H unchanged. Since PHP+QHQ=H, it also keeps G†H unchanged. It does not generally keep G unchanged: recycling coherences are removed. K_odd=(K−RKR)/2 keeps KP and hence the leading effective stack, but changes the interaction if QKQ was present. The source correctly distinguishes this redesign from a mere choice of unraveling.

The flag-Hadamard/controlled-R/Hadamard circuit on the output of an acquired jump-stack block gives precisely PL and QL in two retained color branches, with unchanged supplied normalization. The two-arm LCU with coefficients 1/2 and −1/2 produces K_odd/alpha_K, not an unearned normalization by ||K_odd||. Acquired psi preparation implements R; its controlled execution, comparisons, uncomputation and synthesis are real costs. These are legitimate circuit operations for an already acquired simulation interface, not evidence that a passive bath offers physical jump routing or Hamiltonian sign reversal. Ordinary positive-time parity averaging would give the even part, so the source's explicit sign-access warning is necessary and correct.

## Qutrit fixture and ordinary winner

The three jumps give H=P1+P2 and G†H=−2pP1−2P2. For p<1, the second jump is genuine excited-sector recycling. The two QP coupling blocks are sigma_minus and sigma_plus/2, yielding b=s=C=1 and d=2/3 for H0=Z/3. The effective jumps are sqrt(2)sigma_minus and sigma_plus/sqrt(2). At p=1/2, kappa=1, gamma0=28/3, and the no-control time-one bound is (232/3)/lambda, agreeing with the stated numerical upper bound at lambda=10^6.

The effective channel is ordinary generalized amplitude damping with total population rate 5/2 and equilibrium ground probability 4/5, followed by the commuting Z rotation. The four displayed Kraus operators have the correct normalization and orientation. A two-ancilla branch construction uses one branch preparation rotation, two rotations and two CNOTs for the controlled damping rotation, one CNOT for emission transfer, two branch-controlled X conjugations, and one final Z rotation: at most five CNOTs and four one-qubit rotations before actual angle synthesis. It acts on unknown reference-entangled inputs. Summed unitary synthesis error at most epsilon_gate/2 yields channel error at most epsilon_gate. No source-history simulation is needed for this logical task.

The coherent-output merged comparison has the same H and drift but generally nonzero L†FL; splitting it is genuinely a different bath. The p→0 deterioration of this particular energy certificate is not a lower bound on actual return time. The source makes both distinctions explicitly.

## Scope

The new conclusion is a finite-rate cold logical-output certificate and a paid circuit-access redesign. Broader adiabatic elimination, Hamiltonian symmetrization and generalized amplitude damping are ordinary established ingredients. This receipt checks the mathematics and circuit accounting, not a new comprehensive literature survey. The direct effective ancilla channel is the stronger ordinary operation for the explicit fixture; no cooling novelty, generic cheap projector, physical sign-control acquisition, gate backend, or practical advantage is established.
