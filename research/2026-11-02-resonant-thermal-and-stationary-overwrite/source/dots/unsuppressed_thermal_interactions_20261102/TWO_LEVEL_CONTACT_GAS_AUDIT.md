# Independent audit: enlarged-contact two-level gas

2026-11-02. Root's enlarged-contact construction is simpler and stronger than the previous generic hyperforest route. The exact factorization and sufficient two-species KP conditions below check out against the earned dictionary in
`producer-workspace/EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md`.

The older forest notes remain exploratory scaffolding and are NOT needed for this proof. No counterterm K^-2 clock family is used.

## 1. Contact regrouping is an exact change of source components

For each elementary V label lambda retain its owned clock set R_lambda from the earned dictionary. Define clock contact `T_lambda=N1(R_lambda)` in the native clock-overlap graph, and include its marked data and bath supports in the full contact set. Change BOTH definitions together:

- USED-label components are connected components in the graph of intersecting full contact sets;
- source compatibility is disjointness of those same full contact sets.

The owned columns of Gamma remain `C_Gamma=union R_lambda`; they are NOT enlarged to all T_Gamma. The clock contact is `T_Gamma=N1(C_Gamma)`. Contacts can overlap inside a component, and C_Gamma can be disconnected; neither is a problem.

Every original Dyson history still has a unique USED-label component decomposition. Compatible sources have disjoint original marked supports, so separate syndrome closure and scalar reduction of small sources from the earned dictionary still apply. Enlarging the component graph only merges previously separate closed pieces; it does not split any closure constraint.

A native source–source sign could be nontrivial only if some owned clock of one source neighbors an owned clock of the other. Their N1 contacts would then intersect, contradicting compatibility. Thus compatible source–source native pair factors are IDENTICALLY ONE. Hard-core contact exclusion is their only direct interaction.

A background singleton rod lives on a single clock x. It can see a source only if x lies in T_Gamma (owned-column deletion is included). Because compatible T_Gamma are disjoint, it sees AT MOST ONE source.

## 2. Exact singleton resummation

For fixed compatible source histories, the reference background rod expansion has connected-cluster measure phi(dT). Each source modifies a background cluster by

`B_Gamma(T)=product_(r in T) h(Gamma,r)`.

This is zero if any rod lies on an owned column; otherwise it is a product of native pair signs. In every case B_Gamma is in {0,+1,-1}. Therefore

`log Xi_background_modified = integral phi(dT) product_Gamma B_Gamma(T)`.

For a singleton T={r}, at most one source can have B_Gamma(r) != 1. Consequently

`product_Gamma B_Gamma(r)-1 = sum_Gamma [B_Gamma(r)-1]`.

All singleton responses factor EXACTLY into individual source measures:

`z'_Gamma = z_Gamma * exp{ integral_singletons z(dr)[B_Gamma(r)-1] }`.

The integral is over all ordinary rods and wraps, including real excited-clock histories. No singleton is omitted, and its exponent is not expanded into a new interaction between sources.

## 3. Source activity has no beta*M0 self-energy burden

Let M0=2g²/t, J0=2g²/(tK), h_nv=M0-J0, and

`delta_beta=integral_beta^infty rho(l)dl <= (4/3) M0 exp(-beta*t/K²)`.

On an owned column the nonwinding singleton response is exactly deletion, giving

`exp[-beta integral_0^beta rho_nv(l)dl] <= exp[-beta h_nv+beta delta_beta]`.

On an unowned contact column, nonwinding singleton weights are positive and B is +/-1, so their response factor has modulus <=1. Wrap singleton weights are also positive and flux-independent; their response factors, whether on owned or unowned columns, have modulus <=1.

Only winding singletons can have signed weights. On an unowned contact column their absolute response costs at most exp(2 beta J0). On an owned column deletion costs at most exp(beta J0). These can be combined with the raw clock trace, rather than charged twice:

raw source trace <= `K^c exp(beta M0*c)`;

owned nonwind deletion leaves <= `K^c exp[beta(J0+delta_beta)c]`;

owned winding deletion adds at most exp(beta J0*c), and unowned winding response at most exp[2beta J0(|T|-c)].

Thus a safe compact bound is

`K^c exp[2 beta J0 |T| + beta delta_beta*c]`.

This is valid with arbitrary numbers/times of prescribed matrix-unit insertions because the full K-level Schatten bound controls their product without K per insertion. Bath path factor is d_B^h after the earned onsite normalization.

For m distinct USED labels, c<=b_c*m, |T|<=b_T*m, h<=b_B*m, and the exact repeated-insertion sum from the earned dictionary gives

`integral |z'_Gamma| <= q_norm^m`,

`q_norm = K^(b_c) d_B^(b_B)
          exp[2 beta J0 b_T + beta delta_beta b_c]
          [exp(beta epsilon_d)-1]`.

Here epsilon_d and the elementary-label counts MUST include the physical-to-dressed Pauli/matrix-unit l1 decomposition overhead. Additional fixed data-state conventions are charged explicitly as in the original dictionary. The expression is polynomial in K only if b_c and those overheads are controlled independently of K.

## 4. Residual clusters are independent complex-Poisson EVENTS

Keep only original background connected clusters with n(T)>=2 as a second species of polymer, with activity phi(dT). Set

- event–event pair factor h(T,T')=1, even if their physical supports overlap or the event labels coincide;
- source–event factor h(Gamma,T)=B_Gamma(T);
- source–source factor zero for intersecting full contacts and one otherwise.

The event gas is an ordinary complex Poisson gas: summing any number of events gives

`exp{integral_(n>=2) phi(dT) product_Gamma B_Gamma(T)}`.

Dividing by the event-only partition function subtracts `integral_(n>=2) phi(dT)` from the exponent. This exactly reproduces the residual background response. Event overlap is allowed because events represent connected terms of a logarithm, not independent physical rod histories. Adding an event hard core would be WRONG.

Every new pair factor has modulus <=1. The exact two-level representation therefore falls directly under the same continuum complex-measure KP theorem as the original rod gas. No generic cumulant bound, positivity of event activities, or many-body interaction theorem is needed.

## 5. Weighted event pressure and its uniform-K bound

Give an event charge `a_event(T)=gamma*n(T)`, gamma>0. Define

`P_gamma = sup_x integral_(T:n>=2, some rod on x) |phi|(dT) exp[gamma*n(T)]`.

Apply the original rod theorem with the background rod measure inflated by exp(gamma), and use its rooted >=2 bound. Marking a rod on x may overcount an event but cannot undercount it. With the corresponding a0,b from the inflated KP point,

`P_gamma <= exp(gamma){ beta*p_gamma + exp(a0) W(b) }`,

`p_gamma=exp(a0)M0(b)-M0`,

`p_gamma/J0 <= 192 x_gamma`, `x_gamma=D exp(gamma)*eta²`,

under the earlier sufficient a0<=log2, b/mu<=1/2 conditions. Extra desired spatial weights can be inserted in the inflation consistently. The wrap term is retained; it need not be pretended to vanish.

Hence P_gamma is O(beta*x_gamma*J0) plus the explicit small wrap term, uniformly in K. There is no beta*M0 term: every event contains at least two rods, so the large singleton pressure has already been resummed.

## 6. Explicit new KP conditions

Let:

- b_T be the maximum clock-contact count per elementary label;
- b_full be the maximum FULL contact count per label (clock, data, and bath nodes);
- ell_full be the maximum number of elementary labels whose full contact contains one specified support node;
- Delta_contact be the degree of the enlarged elementary-label contact graph;
- C_contact be a connected-set counting constant, e.g. a padded e*max(Delta_contact,1).

Take a compound-source charge

`a_source(Gamma)=A*m(Gamma)`,

`A=1+4 b_T P_gamma`.

Set Q=q_norm*exp(A), or Q=q_norm*exp(A+kappa_source) if an extra per-label spatial/filling weight is needed. The total source activity touching any fixed support node is bounded by

`G(Q)=ell_full * Q/(1-C_contact*Q)`, provided C_contact*Q<1.

This follows by selecting one USED label touching the node and summing connected label sets. It includes all repeated insertions through q_norm; no extra time-order factorial remains.

For an event T with n rods,

`integral_sources |z'_Gamma| exp[A*m] |h(Gamma,T)-1| <= 2n*G(Q)`.

A source can interact only by having its clock contact meet one of the event's rod clocks. Require G(Q)<=gamma/4; this gives at most half of a_event(T).

For a source Gamma,

`integral_events |phi| exp[gamma*n] |h(Gamma,T)-1| <= 2 b_T m P_gamma`.

The source–source hard-core contribution is at most

`b_full*m*G(Q)`.

Require b_full*G(Q)<=1/2. Then the sum is at most

`m[1/2+2b_T P_gamma] < A*m`.

Thus the following explicit sufficient inequalities close the two-species KP criterion:

`C_contact Q<1`,

`G(Q) <= min(gamma/4, 1/(2b_full))`,

with A, Q, q_norm, and P_gamma as above, AND the separately required inflated original rod KP/cold conditions.

A simple conservative choice is to demand

`Q <= min{1/(2C_contact), gamma/(8 ell_full), 1/(4 b_full ell_full)}`.

These inequalities produce a nonzero perturbation admission at each fixed beta J0 and fixed physical/dictionary resources. The source exponent involves beta J0, not beta J0 K.

## 7. Boundaries of this audit

The audit establishes exact contact ownership/factorization, the residual event encoding, the normalized source activity bound, and the explicit scalar two-species KP gate. The existing downstream scalar/logical-root and syndrome-influence consumers must still be applied with the ENLARGED contact-count constants and the new singleton-resummed source dependence.

Resummed source activities depend on the original source's filling neighborhood plus the O(m) contact fluxes contributed by singleton winding factors. That is not one stabilizer monomial, but it is a local scalar function with the displayed uniform norm bound. Large sources remain bounded logical/operator roots as in the earned dictionary; a matrix-valued cluster theorem is not silently asserted.

All original positive compilers remain intact. This audit does not establish useful laboratory temperatures at K=180, Gibbs preparation, a counterterm-enhanced family, or a universal K-polynomial total resource cost when dressed source supports themselves grow with K.
