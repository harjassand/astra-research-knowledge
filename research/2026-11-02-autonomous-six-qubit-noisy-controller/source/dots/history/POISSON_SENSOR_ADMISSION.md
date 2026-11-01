# Actual finite-state Poisson source potential, with two necessary corrections

Reconciled derivation, 2026-11-01 16:35–16:39 UTC. Uses root's controlled-Pauli algebra and the finite clock/flag protocol, not independent-origin evidence.

## A. Exact observables

Let P_p(x) be probe p's already-applied Pauli prefix, with prefix I before extraction and prefix S_p after completion. Keep prefix S_p through readout/return; the next preparation resets the phase label to prefix I. For any data check S_s define
Sbar_s(x)=S_s product_p Z_p^[omega(P_p(x),S_s)].
Root's factor-hop algebra transports Sbar_s exactly. Completed probe reset/readout leaves it unchanged because omega(S_p,S_s)=0. Let Z_(cache,s) encode cached sign and
 e_s(x)=(I-Z_(cache,s) Sbar_s(x))/2.
These are positive projectors, mutually commuting. Cache overwrite is their only ideal nontransporting step.

Define an ARMED mask a_p(x): 1 after preparation and through the BEFORE-readout phase, 0 immediately after readout and throughout return. Define
 r_p(x)=a_p(x)(1-B_p) [I-X_p P_p(x)]/2.
This is a positive projector, including classical masks. In the ideal collision-safe legal-clock sector:
* own controlled-Pauli hops transport r_p;
* disjoint/noninterfering operations preserve it;
* a mark setting B_p=1 kills it;
* target readout kills its armed mask;
* atomic probe preparation plus B_p clearing creates r_p with conditional expectation epsilon_p I, epsilon_p=(1-s_p)/2, on the destination armed phase.
Preparation and flag clearing should be atomic, or their intermediate reactivation term must be included separately.

**Correction 1:** The unmasked defect (1-B_p)(1-X_p S_p)/2 is NOT conserved after readout until next preparation. Once A_p goes low, a legitimate new neighboring extraction can change it. Kill r_p at readout; do not price it through return.

At accepted readout, no interfering partial probe exists in the ideal legal sector. Thus Sbar_p=S_p there. Measuring X_p and overwriting the cache gives the exact Heisenberg identity
 E_readout^* e_p(destination)=(I-X_p S_p)/2=r_p(source),
where B_p=0 and a_p=1 on this accepted branch. Sum both measurement outcomes; there is no assumption that the syndrome or probe is classical.

## B. The finite classical generator is physically specified

For target p, x contains its own and direct-overlap neighbors' clock phases and active bits, and B_p. Neighbor bad bits are unnecessary: they never affect neighbor clock hazards or active-bit updates. Scans by checks outside this neighborhood may change neighbor bad bits, but therefore do not change x. Neighbor scans of p and p's scans of neighbors are included. Clock hazards are kappa because all phase operations are TP channels and all branches advance.

This closes a finite generator Q on x in the ideal valid-clock source. If physical clock patterns/phase-inconsistent active flags are included, their extra effects must be treated as illegal sectors or explicitly added to this generator; they must not be quietly identified with legal phases.

Let A be the set of target accepted-readout transitions. Define the killed backward generator
 (K_A f)(x)=sum_(x->y notin A) q_xy[f(y)-f(x)] - sum_(x->y in A) q_xy f(x).
The local finite-word minorization proved in CLOSED_FINITE_CLOCK_FLAG_PROTOCOL.md makes this killed chain transient from every legal initial x. Therefore the UNIQUE finite solution
 t=-K_A^{-1} 1
exists, t(x)>0, and t(x)<=T/p_word. This is an actual finite matrix determined by specified local rates, not an inferred marginal collision probability.

For V_p=t(x)e_p(x), exact transport plus accepted overwrite gives
 L_ideal V_p = -e_p + g(x) r_p,
where
 g(x)=sum_(x->y in A) q_xy t(y).

**Correction 2:** The gain uses t at the POST-readout destination y. In general replacing it by t(x) at the source is wrong.

## C. Second killed reward equation cancels the bad-report gain

On armed, unmarked states define K_D by killing the same finite chain at any transition that marks B_p or performs target readout; preparation/return states lie outside this armed domain. Let
 xi=-K_D^{-1} g.
This is finite and nonnegative because every independent nonblocking target clock reaches readout in bounded expected time, even if no mark occurs. A crude bound is xi_max <=g_max times the maximal mean remaining armed duration.

Set xi=0 off the armed-unmarked domain and W_p=xi(x)r_p(x). All nonkilling ideal steps transport r_p. At mark/readout the destination W_p is zero. At preparation r_p is born with mean epsilon_p I. Consequently the exact operator identity on the ideal collision-safe legal sector is
 L_ideal W_p = -g(x)r_p + b_p(x) I,
 b_p(x)=sum_(prep transitions x->y) q_xy epsilon_p xi(y).
Therefore
 L_ideal [t e_p + xi r_p] = -e_p + b_p(x) I,
with 0<=b_p(x)<=kappa_prep epsilon_p xi_max (one prep phase).

This explicitly charges finite reset purity. It does NOT assert that accepted reports are correct. It pays their probe-defect contribution before they overwrite the cache. An independent readout bit-flip probability eta gives E^*e'=eta I+(1-2eta)r; for eta<=1/2 the same construction yields an additional upper floor <=eta g_max. Arbitrary detector/helper noise needs its actual local generator bound, not an independent-bit-flip assumption.

All coefficients are local finite constants depending on rates, weight, degree, and apparatus. Summing over p gives an exact mean source Foster bound with extensive, explicitly priced purity/readout floors, before other controller/data terms and illegal sectors are added.

## D. Illegal sectors and exponential lift are not silently solved

For arbitrary clock/flag states, write the exact generator equality as the legal terms above plus R_illegal. R_illegal consists of: unmarked interfering hops; invalid clock steps/phase jumps; premature reset; corrupted active/bad masks; and the actual helper/data perturbations. Each is supported on a bounded local neighborhood and has finite norm bounded using t_max and xi_max. This identifies what must be dominated; it does not prove an already-negative illegal-sector drift. Clock sorting and collision penalties must be separately shown to pay those contributions.

The mean potential is positive, but a full exponential lift needs care. Each r_p commutes with every e_s: the data commutation sign omega(P_p,S_s) cancels the sign from X_p against the Z_p factor in Sbar_s. However r_p and r_q can anticommute on unmarked-overlap configurations when their partial Paulis anticommute. They commute on the ideal collision-safe sector because the dangerous armed masks are deactivated. Thus one cannot globally invoke a commuting-potential exponential lemma on arbitrary corrupted flag states. Options are an explicit safe-sector mask plus a proved penalty for mask transitions, or a genuinely noncommuting local exponential estimate. This is a real remaining proof obligation.

## E. Scope

Earned: explicit finite generator; unique Poisson/reward coefficients; exact legal-sector Heisenberg cancellation; finite preparation/readout floor; no global runtime approximation; no collision-independence assumption. The corrected armed mask removes a concrete counterexample to the initially suggested defect lifetime.

Not earned: domination of all illegal source configurations, a microscopic two-body realization of clock-labelled GKSL channels, or a global exponential-memory theorem. Those cannot be supplied merely by the mean source identity or marginal service minorization.
