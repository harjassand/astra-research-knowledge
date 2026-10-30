# A deterministic central-box event certifying every classical cycle

2026-10-30. Concrete nominal instrument construction and deterministic implication. The final signed expansion with all enlarged-box constants, and the recursive quantum scheduling interface, remain to be audited. No adaptive cavity is assumed.

## 1. Hardware, including an actual opportunity instrument

Use TWO_SUCCESS_CLASSICAL_CYCLE_LATCH.md. The visible commit resets c=0. Two later actual snapshot SUCCESS leaves are necessary to set c=2 and start the timer at 0. Snapshot/cleanup continues at all times, but its payload is identity on the snapshot when c=2. All visible writes are onsite and require the local ownership tag to be FREE.

Design the timer ITSELF as lambda(Phi_tick-Id), with a genuinely complete CPTP tick channel. On its colocated counter/stage registers define

    f(c,j) = j+1 if c=2 and j<n, and f(c,j)=j otherwise,
    K_(c,j) = |c,f(c,j)><c,j| tensor I_rest,
    Phi_tick(rho) = sum_(c,j) K_(c,j) rho K_(c,j)^dagger.

Then sum K_(c,j)^dagger K_(c,j)=I, and the resolved physical jumps are sqrt(lambda) K_(c,j). Their total source effect is exactly lambda I. The disabled/completed leaves are identity only ON THEIR SECTOR; the complete channel also dephases counter/stage sectors. That dephasing is included in the declared physical generator, not silently omitted. No claim is made that an arbitrary existing guarded LOAD process can be uniformized by adding imaginary ticks.

Entry into the active state c=2 is the actual SUCCESS leaf that resets the timer to stage 0. While active and incomplete, EVERY tick advances the timer; ownership tags do not block it. Neither snapshot attempts nor disabled commit opportunities modify the active stage. Only the actual completed commit exits c=2. Thus an active run really consumes every tick and requires exactly n of them. The tick records are actual nominal resolved onsite instruments, with no feedback from those records. All rates and finite dimensions are fixed before choosing the allowable perturbation strength.

Similarly design a complete onsite COMMIT-OPPORTUNITY channel at rate kappa. Let P_R project onto c=2 and timer n. Its noncommitting Kraus operators can be chosen as P_notFREE tensor I_payload and P_FREE(1-P_R) tensor I_payload. The enabled Kraus family acts only on P_FREE P_R, applies the declared finite classical commit map, and resets c/timer. Its summed source effect is P_FREE P_R. Thus the complete family sums to I; the family with tag FREE sums to P_FREE. A counted free opportunity after timer completion MUST commit unless another commit already occurred.

Crucially, the disabled leaves do NOT measure or reset X_x or the in-progress snapshot S_x. Measuring S_x during a locked reversible prefix could spoil exact rollback. The only disabled-sector dephasing here is the declared mode/tag projection; these projectors preserve the native prefix/ownership sectors. An enabled commit is allowed only when the tag is FREE, so it cannot intersect a legitimate snapshot prefix that owns this resource. This is a physical opportunity channel, not an assertion that an enabled jump fires instantly.

An actual finite all-state path to a free opportunity clears the finitely many incident snapshot owners, parks them along a selected finite record, and takes the onsite free leaf. The monitored-path construction therefore supplies a new finite-support killed witness and an exponential miss bound. One must instantiate its new constants. The hardware has only two-site Hamiltonians and onsite dissipators, with all declared registers grouped at fixed sites.

## 2. Fixed-grid timer regularity implies ALL run durations

Choose an integer n divisible by 400 for convenience and set

    T = 8n/(5 lambda),       delta = T/32,
    lambda delta = n/20.

Tile physical time by J_j=[j delta,(j+1)delta). Let N_x(J_j) count ALL timer ticks at x, including disabled ticks. Declare a tile timer-regular when

    19n/400 <= N_x(J_j) <= 21n/400.                  (1)

Every interval of length less than T/2=16 delta intersects at most 17 grid tiles. Its tick count is therefore at most 357n/400<n. Every interval of length 3T/4=24 delta contains at least 23 whole grid tiles, and hence at least 437n/400>n ticks.

Consequently, wherever the requisite intersecting/contained grid tiles are regular, EVERY timer run initialized at 0 takes between T/2 and 3T/4 to reach n, simultaneously for all starting times. No union bound over randomly selected timer starts or number of cycles is needed. A timer already at an arbitrary initial stage takes at most 3T/4 additional time.

The summed tick effect lambda I makes the total count a Poisson clock of rate lambda in the nominal instrument, even with an arbitrary retained reference and other Hamiltonians: the no-count loss is the scalar -lambda and the summed count gain has constant trace lambda. For disjoint sites/time intervals its joint exponential moment is the product moment, since each marked gain has scalar source effect and the unmarked evolution is trace-preserving. Chernoff's bound gives

    Pr[not (1)] <= 2 exp(-n/24000).                 (2)

The same statement is an effect-operator bound uniform in the incoming state. In a CP cavity containing the timer site, these declared nominal leaves remain actual summands and the bound is unchanged. They are not assigned to the unrestricted perturbed generator.

## 3. Fixed-grid service events

For every grid tile needed below require:

A. At least two actual snapshot SUCCESS leaves for the site observer, with the complete native witness/owner footprint protected.
B. At least one actual free COMMIT-OPPORTUNITY, using its new killed witness/owner footprint.

After an arbitrary instant, an interval of length 2 delta contains a complete grid tile. Thus A guarantees that c reaches 2 within 2 delta after a visible/physical commit, with the second success furnishing the fresh snapshot. After timer completion, B guarantees a visible/physical commit within another 2 delta, because c=2 and timer=n persist until such a commit.

Every fresh physical cycle therefore has duration at most

    2 delta + 3T/4 + 2 delta = 7T/8,

and at least T/2. Its snapshot precedes its commit by at least T/2. These are simultaneous deterministic statements for every cycle whose required tiles pass, not isolated tails conditioned on a later clock-selected event.

A first malformed snapshot may cause an initial physical commit that fails to change the represented X. That commit still resets c=0. The next full cycle is fresh, and the transition table's time-marking field then guarantees an actual represented switch. Two full upper-cycle spans are less than 2T, so a warm margin of 2T is sufficient for this particular stale-snapshot issue. Add the fixed native owner/forest flush margin required by the clean semantic compiler; that margin is not hidden inside the word SUCCESS.

## 4. Central-box implication

For a fixed central interval C=[a,a+T], protect the complete source/observer/commit witness patch over an enlarged interval

    C_plus=[a-W,a+2T],

where W is at least 2T plus the fixed owner/forest flush margin. The ACTUAL protected interval is the grid-rounded interval

    C_hat=[delta floor((a-W)/delta), delta ceil((a+2T)/delta)].

Require all timer-regularity, snapshot-service and free-opportunity tests on its full grid tiles, using consistent half-open endpoint conventions. This extends the cut by less than delta at each endpoint; a fixed-boundary jump is assigned consistently to one tile. Thus no nominal full-tile instrument is inferred from a cavity that cuts only part of that tile. The number of tests is a fixed constant once W/T and the hardware are fixed.

On this event, and under the native clean-history implication after the warm margin:

* all represented dwell periods entirely relevant to the central interval satisfy T_low=T/2 and T_high=T;
* the next two relevant represented switches have an actual common neighborhood snapshot strictly after the first switch and at least T_low/2 before the second;
* every snapshot is serializable because visible commits respect all read locks;
* the new Rand is supplied by the actual equal-rate resolved commit leaves;
* raw coherent prehistory does not become an assumed classical path: the good source operations preserve the visible-label algebra and snapshots explicitly pinch it.

To cover a Definition 7.19 computation test whose future interval has length 2T, use two adjoining central intervals or extend the central interval to 2T. The number of tiles and every halo-incidence constant remain fixed. A lower-dwell violation at a boundary is assigned to a central interval containing the two switches, with the one-tile endpoint enlargement paid explicitly.

Thus ANY violated primitive condition in the central interval implies at least one of a fixed finite collection of local noise, timer-count or actual service defects in C_plus. This is an all-cycles-in-box implication. It does not condition on the chosen cycle being clean.

Initial boundary qualification: the warm-margin statement requires that the entire protected past exists, in particular a>=W (with the grid-rounded lower endpoint nonnegative). It does not create a negative-time history. For boxes meeting time 0, one must either declare an initial-boundary exception or supply a correct physical initialization. Gacs Definition 7.19 sets sigma_1=0 and tests the FIRST switch when a=0, so its initial condition cannot use the first-stale/second-fresh allowance.

A concrete admitted clean initialization is: visible X in the declared encoded classical program configuration; c=0 and timer=0; all observer hubs ready with zero workspace; all resource tags FREE; monitors in their admitted ready state. Then the first two snapshot successes after time 0 are fresh, and the first visible commit satisfies the same snapshot/timer rule without a negative warm margin. Initial service/count boxes are tested only on [0,infinity). The preparation of this state is an explicit initialization interface, not a consequence of the timer theorem. Arbitrary uninitialized control at time 0 is not certified here, and protecting an unknown quantum input while control warms up remains a separate paid interface.


## 5. Parameter order is not circular

One may keep lambda and kappa fixed and increase n, making T proportional to n. The snapshot gate lists and the free-opportunity clearing path need not grow with n: their coherent edges commute with the timer except for the explicitly resolved SUCCESS/COMMIT resets. The total timer loss is lambda I and its unused branches are retained. The finite-path intensity and monitored block-norm estimates can therefore be chosen uniformly in n for this family, provided the timer is not unnecessarily synthesized as an n-step coherent snapshot circuit. Actual service constants must still be checked for this implementation.

Then the timer defect (2) and the service misses C exp(-r delta) both decrease with n. After choosing finite n and all hardware, choose the physical perturbation strength small enough for its enlarged-box cavity cost. No rate is sent to infinity, no local dimension grows with computation size, and no pre-existing numerical witness is reused without verification.

## 6. How this enters fixed-box signed accounting

At the physical level, keep the deterministic delta-grid. Define each central label's good comparison using a CP cavity on the full grid-rounded C_hat and the actual joint nominal instrument that accepts ALL its required service/timer tests. Overlapping labels share the same nominal records in each common cavity; forgetting tests gives compatible instrument marginals.

A bad central label is a union of at most M fixed tests or local noise restorations. Color the enlarged space-time supports so labels in one class have disjoint buffered witness patches and nonoverlapping relevant time slabs. The coloring number P is finite because both spatial footprints and the number of enlarged tiles are fixed. Expanding the M alternatives and selecting a color pays these constants once, rather than assuming independence of overlapping represented conditions.

For a timer-defect choice, use its uniform Poisson exponential-moment effect bound. For a service-defect choice, use its genuine killed witness. In the cavity all noise-restoration derivatives lie outside the still-cut witness supports, so they do not disturb these bounds. The mixed difference construction is the same type of compatible-family calculation as the reviewed CP-cavity theorem, but the resulting M, P, restoration-overlap K and numerical constants for these newly enlarged labels must be written and independently checked. No new adaptive on/off cavity is invoked.

## 7. What flattening this DOES and DOES NOT give

The source's canonical damage witnesses are pointwise sums of products. Whenever the higher witness lies in a fixed bounded coarse rectangle, replacing each primitive violation by the fixed-box implication above gives a finite Boolean witness on physical boxes. Intersections of enlarged lower supports require explicit packing; a source pair of disjoint windows is not automatically a pair of disjoint physical halos. This is a concrete input to the root's order-free Boolean renormalization, subject to its minimum-degree/overlap condition.

This local flattening does not by itself prove a global rate for one permanently assigned quantum module whose actual activation time can wander over an unbounded number of deterministic boxes. The classical source handles predictable random windows by its strong-trajectory contract; a signed-norm version or a complete deterministic spacetime renormalization/cut construction must still account for that selection. Similarly, it does not supply the missing bounded-skew schedule geometry or an encoded quantum gadget.

The advance here is the actual fixed-grid, all-cycles primitive receiving implication, with no selection on future cleanliness and no uncontrolled number of timer-start trials.
