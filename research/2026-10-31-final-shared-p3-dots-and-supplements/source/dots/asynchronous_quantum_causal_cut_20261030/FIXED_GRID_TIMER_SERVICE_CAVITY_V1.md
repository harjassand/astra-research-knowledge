# Fixed-grid timer and service tests in the CP-cavity expansion

2026-10-30. Candidate exact extension of the reviewed deterministic-box cavity algebra to the declared timer/opportunity hardware. No adaptive cavity, full Gacs simulation or quantum threshold is asserted. The new hardware's killed-witness constants and geometric incidences remain explicit inputs to instantiate and review.

## 1. Fixed elementary tests

The time grid has spacing delta. An elementary label a=(owner/type,j) occupies J_j and has a complete physical cut patch S_a. It is one of:

* SNAP: at least two actual snapshot SUCCESS leaves;
* FREE: at least one actual free COMMIT-OPPORTUNITY;
* TICK: total tick count N(J_j) lies in [19n/400,21n/400].

Every patch includes its test witness and the full semantic owner/read/write footprint needed by the central-box implication. There is no selected random on/off time. Each nominal record counter is initialized at the deterministic grid boundary and forgotten afterward. Common records are used when two tests count the same instrument, so their instrument marginals are compatible.

Assume the actual new SNAP and FREE instruments have finite-support killed witnesses

    alpha I <= Z_a <= I,       K_a^* Z_a <= -r Z_a,     (1)

using the minimum alpha,r across their finitely many types. They must be proved for the new hardware; no old numerical coefficient is imported.

## 2. The timer event has an exact operator bound

The timer is the actual complete CPTP channel specified in CENTRAL_BOX_ALL_CYCLES_V1.md. Its tick gain J_x has

    J_x^*(I)=lambda I.

Marking every tick by e^theta gives the tilted generator

    L_theta = L + (e^theta-1) J_x.

For a nominal/cavity evolution in which this tick instrument is retained,

    L_theta^*(I)=lambda(e^theta-1) I.                  (2)

All other trace-preserving terms, including arbitrary joint bath/Hamiltonian terms, annihilate I. Thus the full count generating function is the scalar Poisson generating function, as an effect-operator identity. For multiple distinct timer sites or disjoint fixed intervals, the corresponding terms add. This proves the joint generating function directly; classical independence is not a premise.

Let mu=lambda delta=n/20 and e=1/20. Optimizing theta=log(1+e) or theta=log(1-e) yields the two Chernoff effects. In particular the CP/TNI timer-deviation map obeys

    ||T_bad||_diamond <= p_tick=2 exp(-n/24000).       (3)

This is uniform in the incoming system, bath and reference. No nominal tick record is assigned to the unrestricted perturbed generator; the instrument exists in the relevant cavity because the timer jumps are onsite nominal summands.

## 3. Mixed service/count estimates, with a finite packing loss

Choose a fixed packing number P such that, among simultaneous labels in one tile, at least 1/P have disjoint buffered patches and no nominal term meets two selected service-witness supports or a selected service support and selected timer site. Multiple test types at one site are included in this packing cost.

For a packed collection of service misses and timer deviations, expand each timer deviation into its upper/lower alternative. Let theta_x have the corresponding sign. The product service witness W=product Z_a satisfies, in the killed-and-tilted cavity evolution,

    K_theta^* W <= [-r m_service + sum_x lambda(e^theta_x-1)] W.  (4)

Indeed the ordinary nominal product-witness identity gives the service drift, and the separated tick gain has J_x^*(W)=lambda W. Outside-cavity perturbations annihilate W, since their total action is outside its physical support. The service comparison costs alpha^(-m_service) once over the tile. The final threshold factors exp(-theta_x threshold_x) and the two alternatives give (3) for each selected timer.

Consequently, with

    p0=max(alpha^(-1)exp(-r delta), 2exp(-n/24000))<1,
    p=p0^(1/P),

the joint CP/TNI map requiring failures of any set S of elementary labels is bounded by p^|S|. In each tile retain a packed subcollection and forget all other failure restrictions, which can only increase a positive effect. Successive tiles start in arbitrary incoming states; the uniform bound composes without an independence assumption.

Equation (4) also proves the weighted bound needed between Duhamel insertions. Other instrument filters are projections/functions of their own passive records. They commute with the selected weights and are contractive. Extra counters do not change the action on W tensored with identity on those counters.

## 4. Compatible cavities and mixed restoration

For a finite set A of elementary labels, remove perturbations on the union of their S_a during their fixed tiles using the reviewed complete-site CP projections E_S. In that cavity retain the actual nominal records and accept every A test. Call the resulting CP/TNI map G_A. G_empty is the actual unmodified channel. The maps G_A are not asserted to be subchannels of G_empty.

Define B_F=sum_(A subset F)(-1)^|A| G_A. As in the reviewed cavity theorem, compatible same-cavity record marginals give

    B_F = sum_(R subset F) D_R H_(F\R),              (5)

where H_S retains the S cavity cuts and requires all S tests to fail, while parameters x_i restore the noise for i in R. Every interpolation generator is a convex combination of union-cavity generators, hence CPTP. The local restoration derivatives act outside every still-cut S support, including the physical supports of the selected service/count witnesses. They act trivially on the passive records and commute with their weighting congruences.

Let v=max |S_a|. Let K be the maximum number of simultaneous elementary patches met by one perturbation support, D the corresponding finite label-overlap degree, and B=2^(D+1) a conservative partition count. Set

    q=2^K v eta delta <=1.

Each nonzero generator derivative involves at most K restored labels and has integrated cb norm at most q. Applying (4) between insertions retains the FULL p^|S| factor: no witness conversion is paid per insertion. The same bounded-overlap Duhamel/set-partition count as in the reviewed theorem gives

    ||D_R H_S||_diamond <= p^|S| B^|R| q^(|R|/K),
    ||B_F||_diamond <= epsilon_elem^|F|,
    epsilon_elem=p+B q^(1/K).                         (6)

The retained bath is not reset. The count tilts are positive weights on actual cavity records, not hidden stochastic faults of a signed perturbation.

## 5. Central labels are one explicit OR regrouping

Let J_c be the elementary labels needed to certify central cell/time label c, including the warm margin, endpoint enlargement and every owner-flush test. There are constants

    |J_c|<=M,       each elementary label belongs to <=R0 sets J_c.

For an elementary exact-fault set R, set b_c(R)=1 exactly when R intersects J_c. Its Boolean polynomial is

    b_c=1-product_(a in J_c)(1-r_a),

with coefficient l1 norm at most C=2^M-1 and minimum degree 1. Apply the root's exact global Boolean regrouping ONCE. It gives an exact central fault expansion with inclusive strength

    epsilon_central <= C epsilon_elem^(1/R0).        (7)

This is a fixed initial overlap loss, not a fault-suppression recursion: 1/R0 is not claimed to exceed one. Its strength can still be made arbitrarily small before the computation is chosen. Source higher-level damage witnesses must thereafter be checked on the central variables with their own geometric incidence; one may not silently identify disjoint source rectangles with disjoint original physical halos.

Whenever c is good in an exact-fault term, every elementary label in J_c is good, so the corresponding comparison histories satisfy the central all-cycles implication. No conditioning on a retrospectively selected clean cycle is used.

## 6. Parameter order and scope

The tick rate can remain bounded by a fixed lambda0 while n and hence delta grow. Snapshot gates use c only as a read-only control and do not synthesize the timer register into an n-long coherent circuit. The free-opportunity test does not require timer readiness; its source effect is kappa P_FREE. A selected finite clearing/snapshot path can forbid ticks for its fixed duration at cost at least exp(-lambda0 times duration), independent of n. Its scalar complete-reset losses and Hamiltonian norms are also independent of n. This is the structural reason uniform service constants are available for this family; their monitored-path instantiation must be checked, not assumed from a generic dimension-dependent theorem.

Choose finite hardware/n/delta and witnesses first, then choose eta to make q small. All constants are independent of computation size. Equations (6)-(7) are for a deterministic finite box universe and the specified nominal instruments.

This note does not yet prove the Gacs canonical simulation has been fully flattened with suitable minimum degree at every recursive level. It also does not establish bounded local schedule skew on a two-dimensional leveled quantum fabric, random quantum activation-window selection, the full-port exRec premise, or actual encoded gate/output interfaces. Those are separate semantic/resource obligations.
