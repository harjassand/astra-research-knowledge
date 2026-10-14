# Carrier-gated glide ordering for retained defect removal

## Status and result

This work defines a constrained optical glide/reaction model and proves when control can change which reaction is selected. It does **not** establish a new practical materials operation. Optical carrier control of species-dependent dislocation mobility in ZnS is already experimentally reported; the proposed new step is to use a limited illumination schedule to change the first compatible reaction and then retain that endpoint. No mapped network, reaction kernel, noise law, or retained endpoint for that step has been acquired.

The central result is an exact obstruction and a positive geometric witness. If every allowed control multiplies the *whole* state generator by a positive scalar, all eventual reaction probabilities are invariant: the control changes the clock only. If the control changes the direction of the glide vector field, or changes relative reaction hazards, selection can change, but only when the resulting controlled path or committor reaches the desired retained endpoint before competing sinks. A nonzero two-species mobility determinant is therefore a route-level lead, not an endpoint certificate.

This is scoped against existing capital records. N777 already records the general common-committor invariance and a residual identity for controlled Markov generators. N783 requires an acquired reaction, configuration-level kernel/reward, retention and matched controls. The result below is a dislocation-specific physical model and exact geometry example; it does not claim those abstract results as new.

## 1. One-input glide and reaction model

The material state is

\[
X=(G,q,c,T,d,w),
\]

where `G` is the current dislocation graph (segments, nodes, slip planes, Burgers vectors, line senses, stacking faults and boundaries), `q=(s_i)` are glide coordinates, `c` is the carrier/core-occupation state, `T` is the specimen temperature field or its resolved reduced state, `d` is accumulated damage, and `w` is the accumulated plastic distortion and other specimen history. Including `G,d,w` prevents treating a changed specimen as a replay of the original initial state.

For segment `i`, let `b_i` be its Burgers vector, `xi_i` its unit line direction, `Pi_i` its slip plane, `g_i` its allowed glide direction, and `L_i` its active length. The resolved Peach–Koehler force per unit length is obtained from the *same* applied-plus-internal stress tensor,

\[
f_i^{PK}=((\sigma_{ext}+\sigma_{int}(G,q))b_i)\times\xi_i.
\]

An overdamped glide coordinate has drift

\[
\dot s_i=M_i(c_i,T,G)\big[g_i\cdot f_i^{PK}-f_i^{pin}(s_i,c_i,T,G)\big]+\eta_i.
\]

The corresponding spatial velocity is tangent to `Pi_i`; climb is excluded unless vacancies or another measured climb process are added as a separate state transition. Mobility, pinning, force, reaction barrier and noise are *not* independent control knobs. They are functions of the shared specimen state and the common applied stress. Under dark equilibrium conditions, an Einstein relation may constrain noise and mobility if its assumptions are verified. Under illumination the model leaves the covariance `A(c,T,G)` to measurement; it does not impose a thermal fluctuation law on a driven carrier population.

The only optical input is a global flux `Phi(t)` satisfying

\[
0\leq\Phi(t)\leq\Phi_{max},\qquad \int_0^{T_f}\Phi(t)\,dt\leq D_{max}.
\]

It changes carrier occupations through capture and release transitions, for example `rate_cap,i = alpha_i Phi` and `rate_rel,i = r_i(T,G)`. These coefficients must be acquired for the chosen sample; this notation does not assign them values. Illumination also changes the heat equation,

\[
C_{th}\dot T=P_{abs}(\Phi,c,G)-G_{th}(T-T_{bath})+P_{diss},
\]

and can change pinning, core reconstruction, reaction barriers, carrier noise and damage. Thus a light pulse is one coupled intervention, not a free choice of each `M_i` or `f_i`. A global stress tensor may be held fixed or optimized over a measured safe set in every comparator, but no per-dislocation force is granted.

For a reaction `r`, the incoming and outgoing graph states must obey

\[
\sum_{i\in in(r)} b_i=\sum_{j\in out(r)}b_j,
\]

and the line connectivity, slip-plane intersections, core structure and any swept stacking fault must also be compatible. Its rate `k_r(X,Phi)` is enabled only in the measured encounter region and is part of the same carrier/thermal model. A legal reaction can leave a nonzero product dislocation, a junction or a fault; Burgers conservation is necessary, not sufficient, for annihilation.

The target `A` is a specified harmful defect absent at a declared post-treatment hold time, with the final Burgers content and fault structure identified and the prescribed damage/plastic-distortion limits met. Add a protocol-phase/clock state to `X`; neither first contact nor a transient reaction product is itself `A`. The process continues through the declared dark/operating hold, and only then enters a terminal qualified-target or competing set. The competing set `F` includes a residual harmful junction or fault, unacceptable new defects, and an unqualified out-of-view or boundary event. Boundary export can be a separately defined useful endpoint, but it is not silently counted as annihilation. A one-time release of stored strain energy is not renewable input.

The hybrid process has generator

\[
\mathcal L^{u}f=b^{u}\cdot\nabla_q f+\tfrac12 A^{u}:\nabla_q^2f
 +\sum_{r\in\mathcal R(G)}k_r^{u}(X)\big[f(J_rX)-f(X)\big]
 +\mathcal L^{u}_{c,T,d,w}f,
\]

where the action `u` consists of the single illumination flux and any globally applied stress allowed by the experimental contract. `J_r` is the full post-reaction state update, including history. The equation is a model contract, not a calibrated generator.

## 2. Selection theorem and time-change obstruction

Let `A` and `F` be disjoint absorbing target and competing sets for the full state process, and let `tau` be the first hitting time of either. Assume the process is nonexplosive, `tau` is almost surely finite under the policies considered, and the stopped generator identity is integrable. For a fixed admissible control `u0`, its target committor is

\[
h_0(x)=\Pr_x^{u_0}(X_\tau\in A),\quad h_0|_A=1,\quad h_0|_F=0,
\qquad \mathcal L^{u_0}h_0=0.
\]

For any predictable switched policy `pi`, Dynkin's formula gives the exact identity

\[
\Pr_x^{\pi}(X_\tau\in A)-h_0(x)
=\mathbb E_x^{\pi}\!\int_0^\tau (\mathcal L^{u_t}h_0)(X_t)\,dt. \tag{1}
\]

**Proof.** Apply the stopped martingale/Dynkin identity to `h_0(X_{t\wedge\tau})`, then take the limit as `t` increases. The terminal value is the indicator of `A`, and the initial value is `h_0(x)`. The control is allowed to alter the complete generator, including drift, diffusion and reaction rates; the cost is not hidden in the identity. ∎

Equation (1) is a complete test for a specified switched policy: it changes eventual selection exactly when its expected integrated committor defect is nonzero. If `L^u h_0 >= 0` on the reachable states for the applied schedule, with strict inequality on a state visited for positive expected time, that schedule strictly improves target probability. Sign changes require evaluating the integral; the determinant alone cannot do that.

There is also an exact all-control obstruction. Eventual target selection is invariant under **every** admissible switching policy from every transient state if and only if all constant-control committors coincide. Equivalently there is a common function `h` with the correct boundary values and `L^u h=0` for every admissible `u`. One direction follows by Dynkin's formula for every policy. For the other, equality of all constant-control committors supplies that same `h`, which is harmonic for each constant generator and therefore for any predictable switch. This is the committor statement already represented in capital N777.

In particular, if `L^u=a_u(x)L^0` with `a_u(x)>0`—the entire generator is scaled, including all reaction channels—then `h^0` is common-harmonic. Likewise, for deterministic glide `dot q=f_u(q)=a_u(q)f_0(q)` with `a_u>0`, every switched trajectory traces the same oriented integral curve with a different clock. If a dislocation is pinned (`a_u=0`) the control can stall it, but stalling alone cannot create another path. Finite observation-time yields can differ through censoring; that is timing, not a changed eventual reaction choice.

For a finite-state discretization of the augmented model, the maximal eventual target probability `V` is characterized by the reachability Bellman equation

\[
\max_{u\in U(x)}(Q^uV)(x)=0\quad(x\notin A\cup F),\qquad V|_A=1,\;V|_F=0. \tag{2}
\]

With the usual finite absorbing-chain conditions, an optimal stationary state-feedback selector exists. If only an open-loop schedule is physically available, define `V_OL(x)=sup_{Phi(·)} Pr_x^Phi(A)` over that schedule class, with time and remaining dose included in the state; its open-loop advantage over the best constant illumination is exactly `V_OL(x) > max_u h^u(x)`. Equation (2) characterizes the larger feedback class, not an unmeasured imaging oracle. Both comparisons become decidable only after the physical generators and legal action set are acquired; identity (1) is the exact policy-level diagnostic.

For two locally constant glide modes on a two-coordinate encounter manifold, the matrix determinant

\[
\Delta=v_1(0)v_2(1)-v_2(0)v_1(1)
\]

tests whether their drift vectors are collinear. `Delta=0` is a path-steering obstruction in this reduced drift model. `Delta!=0` permits different path slopes but is not sufficient for selection: the reachable path must reach a compatible target capture set before every competitor, while surviving pinning and noise. A reaction-rate effect can change selection even when `Delta=0`, but only if the full generators cease to share a committor.

## 3. Burgers-compatible target and competing reaction

Here is an exact crystallographic compatibility check for one fcc/zinc-blende `{111}` slip plane. It is a topology module, not a claim that these lines have the optically measured Zn/S core labels in a particular ZnS/GaP specimen. With `n=(1,-1,-1)` and vectors in units `a/2`, set

\[
b_A=[110],\qquad b_{B}=[\bar1\bar10],\qquad b_C=[\bar10\bar1],\qquad b_R=[0 1\bar1].
\]

Each dot product with `n` is zero. The target reaction obeys `b_A+b_B=0`. A competing encounter obeys `b_A+b_C=b_R\ne0`; the pair has produced a nonzero perfect dislocation rather than removed all Burgers content. All three perfect vectors are allowed `a/2<110>` vectors in the same plane, and `|b_R|^2=a^2/2 < |b_A|^2+|b_C|^2=a^2`, so a residual reaction is not ruled out by the elementary elastic `b^2` comparison. Actual line continuity, core/fault energies and whether the mapped network permits either encounter remain separate obligations.

This catches a common false positive: two mobile partial/dislocation classes can meet and lower a visible count without eliminating the topological defect. The supplied physical ledger's partial-pair example has the same lesson: `[1,-2,1]/6 + [2,-1,-1]/6 = [1,-1,0]/2`, not zero. Final characterization must identify the product, not infer annihilation from contrast loss or a change in line length.

## 4. Decisive dimensionless switching witness

Consider a reduced encounter plane `q=(x,y)` with one global normalized light level `phi in [0,1]`, fixed stress geometry, and the *coupled* witness law

\[
\dot q=v(\phi)=(2-\phi,1).
\]

The dark and full-light vectors are `(2,1)` and `(1,1)`, so `Delta=1`. These values are dimensionless geometry for an existence/counterexample, not material parameters or a fit. The sign is chosen to match the reported ZnS trend that illumination suppresses the Zn-core mobility more strongly than the S-core response. In an actual fit, `v(phi)` would come from one carrier/force/pinning model; one cannot choose its components separately.

Take a first target-reaction capture disk centered at `T=(3,2)` with radius `1/5`, and a competing residual-junction capture disk centered at `F=(2,4/3)` with radius `21/100`. The coordinates are deliberately stated as a reduced model witness; their mapping to dislocation positions is unmeasured. Reaching `T` is only the desired first reaction, not a retained-target certification; the post-treatment hold and terminal readout remain outside this deterministic geometry example.

* Dark for one normalized time unit, then full light for one unit has dose `1` and path `(0,0)->(2,1)->(3,2)`. It reaches the target center. The exact squared distance of the closer segment from the failure center is `1/18`, greater than `(21/100)^2`, so the path avoids that sink.
* Reverse the two pulses, keeping the same duration and dose: `(0,0)->(1,1)->(3,2)`. The closest squared distance to the failure center is `1/45 < (21/100)^2`; the competing reaction occurs first.
* Every constant flux, including an optimized constant value, has a ray with slope `m=1/(2-phi)` in `[1/2,1]`. If such a ray intersects the target disk, its distance to `T` gives `|3m-2|/sqrt(1+m^2)<=1/5`. Since `sqrt(1+m^2)<3/2`, this implies `17/30<m<23/30`. At `x=2`, before the ray reaches the target disk (`x>=14/5` there), its vertical offset from `F` is `<1/5<21/100`. Thus **every constant-flux ray that can reach the target hits the competing sink first**. Dark stress schedules that only multiply both rates by a common nonnegative scalar remain on the dark ray and miss the target disk.
* The constant dose-matched level `phi=1/2` reaches `(3,2)` at time `2`, but its straight ray passes through `F`; matching the final displacement or total photon dose does not match the selected reaction.

The exact checker verifies the Burgers sums, all glide-plane dot products, both pulse-order clearances, the all-constant obstruction bound and the proportional-response falsifier. Its output is [geometric_witness.json](results/geometric_witness.json); code is [reaction_control.py](code/reaction_control.py). A bounded path perturbation smaller than `sqrt(1/18)-21/100` preserves the successful route's sink clearance, but Brownian/non-equilibrium noise is unbounded and must be integrated with an acquired covariance and reaction kernel. This example proves conditional controllability in a reduced model. It does not predict a ZnS yield.

## 5. Falsifiers, controls and costs

The candidate operation fails in several exact ways. If light changes both glide rates by the same positive factor, the determinant is zero and all pulse schedules trace the same ray. If either needed glide coordinate is pinned throughout the allowed flux/temperature window, the target is unreachable. If the target and competing capture sets do not correspond to Burgers- and line-compatible reactions, no mobility ratio can make them valid. If noise or pinning moves trajectories across the event-order margin, the deterministic witness says nothing about yield. If illumination alters target and competitor reaction barriers in a way that makes `L^u h` common-harmonic, equation (1) says the changed velocity still cannot improve eventual selection. Finally, a first-hit target is not retained repair until the product remains absent after controls return to the specified operating condition.

The equal-information comparison must include:

1. **Optimized dark:** optimize the allowed global stress/time/thermal schedule with `Phi=0`, under the same maximum stress, mechanical work, time, specimen-temperature and readout constraints. In the dimensionless witness the stress direction is fixed and only its common nonnegative magnitude can vary, so every dark trajectory remains on the `(2,1)` ray. A richer dark stress actuator could steer the path and must be included in the actual comparator. If no independent mechanical actuator is available, dark optimization is over the real thermal cycle and stop time only; do not posit one.
2. **Optimized constant illumination:** scan every allowed constant flux and duration under the same maximum fluence, total duration, carrier preparation and specimen-temperature limits. The dose-matched constant is a separate arm.
3. **Dose-matched order controls:** compare `dark->light` with `light->dark` at equal total fluence, duration, applied stress history and, where possible, matched `T(t)`. Add a dark heater with measured `T(t)` and a constant-average-flux arm. Equal photon dose alone does not equal carrier occupancy or heat history.
4. **Readout and history:** beam-off during actuation if the instrument permits; acquire identical beam/readout dose controls because electron imaging can itself generate carriers. A reaction permanently changes the state. Randomize matched pre-mapped network windows/specimens to one treatment each; do not call successive cycles on the same evolving network independent trials.

For each accepted endpoint, charge and report optical-source wall energy, absorbed optical energy as an internal partition, heating and cooling, applied electrical energy if used, mechanical work `sum_i integral L_i tau_i v_i dt`, imaging/readout, control electronics, sample preparation and failed/damaged material. Do not add absorbed energy a second time to wall input. The swept slip contributes plastic distortion approximately `Delta beta^p = V^{-1} sum_i L_i Delta s_i b_i tensor n_i` (with signs and segment geometry resolved); the target Burgers sum being zero does not imply zero macroscopic shear. Report target yield, residual-junction/fault rate, out-of-view/boundary events, damage, `Delta beta^p`, retention and total input per retained target.

## 6. What is established, what is missing, and the next experiment

The primary ZnS work provides a real actuator lead: 365-nm light selectively suppresses glide of Zn-core dislocations relative to S-core dislocations, while the dislocations obey crystal-specific line/Burgers/plane constraints. At the class level this is already evidence of a nonproportional mobility response; it is not the measured two-coordinate control determinant for a particular interacting pair. The study also reports strong pinning, uses 350 °C annealing followed by room-temperature imaging, and corrects mobility comparisons for cycle-dependent strain. It does not establish switching among competing, Burgers-certified reactions in a fixed network. Its optical treatment is a coupled carrier/thermal/stress process; its reported individual-segment mobility is not a configuration-level reaction committor.

The unmeasured coupling is the **same-network map**

\[
\Phi(t)\longmapsto\big(c_i,T,\tau_i^{PK},f_i^{pin},A_{ij},k_{target},k_{competitor},G_{after}\big)
\]

for the actual interacting line segments and their history. In particular, the needed quantity is the measured committor defect `L^Phi h_dark` along reachable configurations, or enough state-resolved rates/geometry to calculate it. A species mobility determinant is not that quantity. The current optical study's measured Zn/S classes are tied to line direction, Burgers vector, plane, core termination and strain state; one cannot freely assemble the two classes into a convenient reaction pair.

**Strongest next experiment:** on the established ZnS/GaP optical platform and its demonstrated 350 °C glide-cycle regime, first map a real small dislocation network before assigning any target. Determine its line directions, Burgers vectors, slip planes, core classes, pinning points and at least one genuinely compatible target reaction plus a distinct competing reaction. If no such mapped network exists, stop at mobility characterization. For a qualifying network, use matched pre-mapped network windows or sister specimens, one irreversible treatment per window. Run randomized dark-optimized, constant-flux sweep, equal-dose `dark->light`, equal-dose `light->dark`, constant-average-flux and dark-heater arms; use 365 nm and only the source's characterized flux range until a new safe range is measured. Match the 350 °C cycle, stress/strain history, time and readout dose; measure actual specimen temperature and carrier-sensitive response. Keep the imaging beam out of the actuation interval when possible and quantify any beam-induced glide.

After treatment and a declared dark/operating-condition hold, use multiple diffraction conditions/Burgers circuits and fault-sensitive imaging to classify true annihilation, residual-product/junction formation, surface export, out-of-view motion and contrast loss. Compare the **retained target committor/yield** and full plastic-distortion/damage/work ledger against the optimized controls. The experiment passes only if the switched policy changes the retained endpoint distribution at matched information, dose/work and heat; movement, a nonzero determinant, or a favorable first encounter alone does not pass.

No novel capability, throughput, power advantage, or historical priority is claimed. Current status: `source_derived_unreviewed` physical premise plus a new exact but dimensionless model witness; material validity and useful reaction selectivity remain `UNKNOWN`.
