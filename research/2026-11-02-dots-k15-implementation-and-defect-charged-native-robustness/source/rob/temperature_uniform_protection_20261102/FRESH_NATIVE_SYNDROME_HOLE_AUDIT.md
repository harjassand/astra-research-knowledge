# Fresh audit: syndrome-sensitive holes for the SAME native clock Hamiltonian

2026-11-02. Independently reviewed `ROOT_NATIVE_SYNDROME_SENSITIVE_HOLES.md` against the earned full-column/prefix dictionary, exact singleton/event construction, resonant moment bounds, and the new commuting defect-trace/character interfaces. Subsequently checked the complete `NATIVE_HOLE_TRANSFER_CONSTRUCTOR_CHECK.md`; its pointwise envelope and all event rows agree with this independent derivation.

**Verdict:** the proposed scalar three-species construction closes under the explicit additional SMALL event-pressure margin described below, together with the already admitted trace/character interfaces. It uses the same weak-endcap native Hamiltonian and generic dressed perturbation dictionary; it does not invoke the commuting positive-hole operator identity for that Hamiltonian. The proof must keep a common pointwise source envelope and unexpanded contact function, not merely a family of integrated bounds at fixed syndrome. Those properties follow from the exact dictionary as detailed here.

This is an admission on a strengthened parameter region, not the entire older native KP region. In particular beta J D eta² must be small enough. No all-low-temperature fixed-v claim follows.

## 1. Exact finite-time cancellation

Write M0_a=integral rho_a, Jb_a=integral_0^beta rho_w,a, hb_a=integral_0^beta(rho_a-rho_w,a). Then

`delta_a=M0_a-hb_a-Jb_a=integral_beta^infinity rho_a`.

For an owned clock, raw semigroup growth exp(beta M0_a), nonwinding singleton deletion exp(-beta hb_a), and winding deletion exp(-beta Jb_a s_a) combine exactly to

`exp(beta delta_a) exp[2beta Jb_a q_a]`, q_a=(1-s_a)/2.

No infinite-time J was substituted for Jb here. Wrap singleton deletions are flux-independent and have modulus at most one, so dropping them is conservative. Exterior contact winding response has logarithm `s_a integral rho_w(B_pin-1)`, with B_pin in {0,+1,-1}. Its modulus is at most1 for s_a=+1 and at most exp(2beta Jb_a) for s_a=-1. Exterior nonwinding and wrap responses again have modulus at most one.

The spectral tilt c_a=t_a/K_a² gives

`delta_a <=(4/3)M0_a exp(-beta c_a)`.

In the heterogeneous equal-J family, `M0_a=J K_a<=JM` and `c_a>=JM/(2eta²)`, so

`delta_max <=(4/3)JM exp[-beta JM/(2eta²)]`.

Thus beta delta_max is a genuinely decaying tail cost under the cold admission, not a beta J constant cost. Additive reference energies are EXACTLY `B_a=2beta Jb_a`, with B_min bounded below by the earlier uniform winding-tail estimate.

## 2. Generic prefix dictionary and the necessary common envelope

A concrete full-column source label retains its V repetition counts, ordering, full clock/bath paths, and resulting data word E. Do not integrate different resulting E words into a fictitious single character. Separate source closure follows from disjoint affected-check sets, exactly as in the earned dictionary.

Every native closing hop inside that source contributes a stabilizer on an owned clock; reordering it past source V Paulis changes scalar commutation signs, not the initial syndrome dependence outside its owned set. Thus the exact source factor is

`chi_E(sigma) f_Gamma(sigma restricted to T_Gamma)`

for a closed scalar E, with T_Gamma the original enlarged clock contact. The remote character is that of the ORIGINAL finite-support V data word E. It is not a new word obtained by Fourier-expanding a polynomial stabilizer filling.

For a fixed trajectory, absolute raw path weights are independent of syndrome: all syndrome factors and Pauli reorder factors have modulus one. Multiply this common absolute measure by the owned nonwinding/winding deletions and extract `exp(sum_(a in T) B_a q_a)`. The exterior singleton inequalities above are pointwise in the trajectory. Consequently the residual local function has a COMMON syndrome-independent majorant whose integral is

`q_native^m`,

`q_native=M^b_c d_B^b_B exp(beta delta_max b_c)[exp(beta v_dict)-1]`.

This proves integral-of-the-supremum control needed for subsequent syndrome-dependent swallowing. Merely knowing sup_s integral|z_Gamma(s)| would not have sufficed. All actual dictionary/support constants remain charged.

Keep the residual contact function unexpanded. After swallowing, its arguments are internally determined. A contact-bit Fourier expansion is unnecessary and would only add fixed exponential-in-m overhead; a full-filling truth table would be invalid resource accounting.

## 3. Exact unnormalized three-species identity

Let nu_+(E) be the original native connected clock-cluster measure at all-positive flux, restricted to n(E)>=2 rods. Its syndrome dependence is the character `chi_Eclock(sigma)` of winding clock labels, supported on at most n(E) checks. Flux-independent native pair signs are already included in nu_+.

Before grouping, the full trace, up to common singleton constants and logical multiplicity, is exactly the sum over valid additive-reference defect configurations D and compatible source configurations Gamma of

`exp[-sum_a B_a sigma_a] product_Gamma z_single,Gamma(sigma)`

multiplied by

`exp{integral nu_+(dE) chi_Eclock(sigma) product_Gamma B_Gamma(E)}`.

This follows by multiplying the old normalized source response back by the native partition function: its event-only denominator cancels. Do not retain that denominator a second time. The exponential is represented by independent complex events with event/event factor1, including overlapping or coincident event labels.

Swallow every defect polymer whose occupied TOP support intersects any source T_Gamma, merging source components connected through such defects. Then sigma on each source contact is determined entirely by swallowed defects. Its bounded residual contact function becomes part of the group's internal activity. Events do not change sigma and do not create extra dependence of this function.

If the group has m distinct source labels and swallowed defect mass M, at most d_c m occupied bits are in released contacts. For heterogeneous B_a>=B_min, remaining thermal weight is bounded by

`q_native^m exp[-B_min(M-d_c m)_+]`.

This uses B_min only on genuinely retained bits; no B_max times hole-capacity penalty is required. The finite-capacity entropy/charge calculation from the previous audit applies with b_c replaced by d_c.

All original source and defect compatibility rules, including residual hole/top contacts, must be retained. Group/defect and group/group source-character phases are the prior asymmetric ones. Event/group factors are exactly

`[product_(sources Gamma in group) B_Gamma(E)] chi_Eclock(tau_group)`,

and event/ordinary-defect factors are `chi_Eclock(tau_defect)`. Every factor is 0 or +/-1. Grouping is uniquely reversible from its original source trajectories and canonical defect constituents. No clock level, wrap or multiple-rod correction has been dropped.

## 4. Explicit new KP rows, not merely plausible locality

Use charges a_s m+a_d M for groups, a_d M for ordinary defects, and gamma n(E) for events. Define the ACTUAL inflated local event row

`E_gamma=sup_a integral_(E containing a rod on a) |nu_+|(dE) exp[gamma n(E)]`.

The earned native estimate gives

`E_gamma <=exp(gamma){beta p_gamma+exp(a0_gamma)W(b_gamma)}`,

`p_gamma/J<=192 x_gamma`, with x_gamma=D exp(gamma)eta² (including any additional spatial inflation consistently). Apply the corresponding inflated native KP and wrap conditions, not just the uninflated ones.

For a group root, a nontrivial event pin requires a rod on one of at most d_c m source-contact clocks. A nontrivial event character requires a winding rod on one of its M occupied top checks. Union bounding the two signs gives the exact sufficient row bound

`integral_events |nu_+| exp(gamma n)|h(group,E)-1| <=2(d_c m+M)E_gamma`.

For an ordinary defect root the bound is `2M E_gamma`.

For an event root with n rods, nontrivial interaction with a group occurs through either (i) a source-contact port at a rod clock or (ii) an occupied swallowed top check at a winding clock. These are at most2n anchors. Interactions with ordinary defects use at most n top anchors. Hence the reverse row is

`<=C n (delta_group+delta_defect)`,

where these are the corresponding entropy/charge-weighted rooted densities. They can be made arbitrarily small by small q_native and cold B_min. There is no event/event row.

Reserve, for example, half the group/defect charges for the already audited hard-core and asymmetric source-character rows, and require

`2d_c E_gamma<=a_s/4`, `2E_gamma<=a_d/4`,

`C(delta_group+delta_defect)<=gamma/2`.

The old rows can be fitted into the remaining fractions by strengthening their cold/source margins. These are genuine sufficient three-species KP conditions. Event pressure must be SMALL: its being finite does not suffice. Its O(beta J x_gamma) growth is precisely the new upper-temperature-range obstruction as beta grows at fixed clock parameters.

At fixed target beta J above the code's cold threshold, shrinking eta makes event pressure and wraps small, while beta delta_max vanishes exponentially. The prefix dictionary does not depend on eta. Thus these conditions are simultaneously admissible without an additional exp(C beta J) multiplier on beta v. Actual source/dictionary/contact constants may still scale badly with K and D.

## 5. Scalar functions, logical exceptions, and observable tilts

Remote character contacts are still handled componentwise for each ORIGINAL closed source E. A decorated group may span long distances through swallowed traces; no polynomial-radius(m) filling theorem is applied to the whole group. Events need no compressed character lemma: their winding-check support is directly at most n.

Classify all sufficiently large memory-touching original source components as exceptional, including accidentally scalar ones. In the canonical decoder frame, a centralizer Pauli E acts as its norm-one logical matrix times the scalar commutation character against the canonical correction. For a logical E this commutation phase need NOT be linear on arbitrary syndrome sums. Exact canonical reverse assembly nevertheless gives D(XOR tau_gamma)=XOR D(tau_gamma) on COMPATIBLE trace collections: component corrections are replayed unchanged, the physical lift is linear, and at most one terminal bag is present. That restricted additivity is what earns exact pairwise exceptional character factors. The forward adjoint source-to-defect estimate works for this local Pauli whether or not it is a stabilizer. Reverse filling estimates are used only for small scalar background words. Event interactions and the extracted contact function remain scalar. Thus the same group KP bounds apply to excluded matrix groups as test roots. Relative matrix remainder bounds are memory-anchored, not bath-volume-anchored.

For a diagonal syndrome observable exp(t N_T), tilt each defect-bearing object by exp(t|T intersect tau|). Events and source-only objects receive no direct tilt. Reserving t mass-tail slack keeps the same three-species KP rows valid, including the event reverse row, and supplies relative exceptional bounds for BOTH tilted and untilted traces.

As before, the scalar truncated gas is not automatically a probability law. First bound the modulus of its tilted/untilted ratio by exp(delta_t|T|); then compare both traces to the actual positive Gibbs traces with relative errors r_t,r_0. Only then apply Markov:

`Pr_actual(T subset syndrome) <=exp[-(t-delta_t)|T|] (1+r_t)/(1-r_0)`.

This is a multiplicative correction, not an additive bad-event floor. Actual witness enumeration and the decoded commutator/projector consumer remain required downstream inputs.

## Final scope

This is a same-native-H analytic transfer within the exact weak-endcap clock model, using its already proved full-spectrum trajectory dictionary. It does not replace the native H by a commuting effective Hamiltonian and does not invoke positive commuting hole deletion on native H. All multi-rod native corrections are retained as the third species. It admits a finite-temperature beta-v window only with the explicit additional event-pressure margin; it is not uniform as beta tends to infinity with fixed nonzero v or fixed eta. Counterterm-enhanced clocks, restricted laboratory interactions, physical WRITE/readout, realistic bath acquisition, practical constants, and historical novelty are outside this audit.
