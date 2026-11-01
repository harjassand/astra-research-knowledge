# Root construction: finite-patch positive correctors for microscopic sources

2026-11-01. New proposed route, not yet a received theorem. It replaces independent classical clock laws by an actual finite-time microscopic service bound. The bounded-arity construction remains banked unchanged.

## 1. Microscopic sequential source worth testing

Combine a probe, cache and finite phase label into one explicitly charged O(w)-level apparatus per bounded-weight check. Each gate phase has ground and excited slots. A resonant two-body apparatus/data Hamiltonian

 H_j=g sum_b |e_j,b><g_j,b| tensor P_j^b+h.c.

is followed by an onsite decay

 L_j=sqrt(gamma) sum_b |g_(j+1),b><e_j,b|.

The reservoir must preserve probe coherence across b: its collective transition is a real symmetry/indistinguishability requirement, not separate which-b emissions. Prefix labels of e_j and g_(j+1) agree, so this decay is dressed-logically benign. H_j applies the next prefix coherently. Start/preparation and final cache write are actual onsite instruments, with finite impurity and response charged. No particle-number sector or high-order virtual Raman amplitude is assumed; apparatus levels and selective couplings are counted. This is not a physical qubit-rail encoding.

Assign the same remaining-work charge to g_j and e_j; the decay lowers it by one. With A=sum_j |e_j><g_j|U_j and C=i(A-A-dagger), H=g(A+A-dagger), the earlier current-Lyapunov method may prove global activity evacuation: [H,Q]=[C,Q]=0, LQ=-gamma N_exc; the cross terms in LC are exchange terms because [sum A,sum A]=0. They can be bounded by excitation occupation at bounded overlap degree. This is a promising exact microscopic reuse, not yet a per-sensor refresh theorem.

The decisive next lemma is uniform conditional stage completion despite neighboring quantum operations. An invertible coupling gU connects every ground amplitude to an emitting excited slot. A finite-time observability bound should depend on the actual neighboring commutator/local coupling scale B, not on the bandwidth of the whole environment. A short-time bound of order gamma*g^2/B^3 per window O(1/B), if proved for arbitrary coherences, gives exponential completion tails for a finite number of stages. This lemma is under construction; a classical exponential waiting time is NOT being assumed.

## 2. General positive local corrector lemma

Consider a bounded-degree graph of finite-dimensional systems with bounded finite-range Lindblad terms. Let 0<=e_x<=I be a local physical cache-mismatch observable. Suppose the ACTUAL source generator obeys, for a finite T independent of graph size,

  exp(T L_source^*) e_x <= epsilon I

as an operator inequality on arbitrary source/data states in its admitted protected sector. This is the substantive service premise to earn, not a stationary mean.

Take a radius-R patch and its truncated generator L_R. Define

  H_x(T,R)=integral_0^T exp(t L_R^*) e_x dt.

Then H_x is positive, supported on that finite patch, and ||H_x||<=T. Exactly,

  L_source^* H_x = -e_x+exp(T L_R^*)e_x
                    +(L_source^*-L_R^*)H_x.

A bounded-local Lindblad Lieb-Robinson estimate controls BOTH the finite-time evolution difference and the boundary-generator term. Therefore, for R large enough at fixed T,

  L_source^* H_x <= -e_x+(epsilon+delta_R) I,

where delta_R decreases exponentially in R after paying the finite-time and graph-growth constants. A representative bound has the form C(1+T)exp[v_mu T-(mu-log d)R], choosing mu>log d. The exact constants and assumptions must be bound to an actual locality theorem before use.

This is not a global channel approximation with error epsilon*T_storage. Once earned, it is a time-independent OPERATOR generator inequality that can be used for arbitrarily long storage. The patch radius and computation may be enormous constants; report them rather than call the construction practical.

If every source term preserves each dressed base stabilizer and the cache/clock observable commutes those labels, the truncated evolution and H_x preserve the same labels. This gives the component commutation needed by the existing protected-memory consumer. A noncommuting physical cache phase must be checked explicitly; one cannot infer this from scalar W conservation alone.

## 3. Controller join without pretending cache writes are free

An asynchronous Boolean verifier can read a stable classical cache sector without changing H_x if H_x is block diagonal in every cache label. This must follow from the actual source dynamics; it is not a free readout assumption.

Cache overwrites can raise Boolean consistency. One conservative alternative to the exact weighted t/xi equations is to price ALL active-source exposure, not only wrong reports. Suppose

  L_source^*(epsilon E_B) <= epsilon B g sum_x A_x,

with physical active projectors A_x. Construct additional positive finite-patch correctors for A_x from an actual uniform small-duty bound. Then their negative -A_x term pays this leakage; their floor is proportional to the actual dilute activity. With epsilon proportional to actuator rate/g, the normalized floor can be O(r*tau), not a free zero.

Scale H_x by a restoring coefficient A of order the actuator rate. Its positive maximum is at most A T per source, and all locality/incidence constants are charged. After source parameters fix a small service floor, the actuator rate can be chosen sufficiently smaller than 1/T to keep the positive apparatus density below the logical barrier. Actual hardware noise is evaluated AFTER these choices. Slowing actuators does not solve a prespecified nonzero noise budget.

## 4. One route to the missing finite-time service premise

Use independent bounded-rate physical pump attempts and a uniform conditional completion tail, if the microscopic lemma in section1 is proved. Quantum trajectories may then count start/end events without assuming independent quantum states or progress clocks. The active flag is a genuine phase-subspace projector conserved by Hamiltonian motion, changed only by starts/exits.

An initially arbitrary apparatus must first flush; no initial readiness is assumed. A later complete collision-free prepared experiment gives the exact parity/cache instrument. The probability of bad cycles can be upper-bounded by actual overlapping active episodes and finite preparation/readout impurity. If completion tails are uniform conditional on the past, start rates bounded by r imply duty O(r tau) and pair activity O(r^2 tau^2), allowing correlated lifetimes. A last-window argument aims for

  exp(T L_source^*)e_x <= [C exp(-c r T)
                 +C(r tau+p_impurity) log(1/epsilon)] I.

This is a TARGET bound requiring a CP/event proof, not established here. It must cover wrong reports after an earlier correct one; a positive chance of one good report alone does not prove the desired small final mismatch. Likewise initial clock coherences cannot simply be called a classical mixture unless the observable dynamics permits that dephasing exactly.

## 5. Why this route has potentially greater consequence

The Raman latch is a useful alternative and revealed real leakage and overlap failures, but its service can be suppressed by a high-order virtual amplitude. A resonant sequential source plus the finite-patch positive-corrector principle could remove both that suppression and the independent-clock premise. If the actual microscopic service and reservoir symmetry are earned, it would connect real two-body interactions to the already received autonomous-memory consumer. Until then, this remains a constructive research direction, not a new completed capability or novelty claim.
