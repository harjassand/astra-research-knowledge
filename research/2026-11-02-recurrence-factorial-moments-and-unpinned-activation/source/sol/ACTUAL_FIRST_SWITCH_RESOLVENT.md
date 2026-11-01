# Exact actual-time resummation of a carried-target cell

This is an author-derived resolvent representation of Kriebel's prior carried-target augmentation. It applies locally to every finite weakly reversible raw list, without restricting molecularity, linkage count or the number of evolving inventories. The representation is NOT a new recurrence premise.

At a marked state (x,t), set z=x−t. While the actual next source equals the carried target, z stays exactly constant and the target follows its finite raw linkage graph. Stop at the first reaction whose source differs from the carried target. Before that stop the physical states are z+j, j in the current linkage L; they are ACTUAL states visited by the process, rather than a frozen approximation to changing inventories.

Write a_s for the total outgoing constant from source s and K_L for the finite complex-graph generator with raw constants kappa. Put

    c_j(z)=(z+j)!/z!,
    alpha_(j,s)(z)=z!/(z+j−s)!   when z+j>=s, and 0 otherwise,
    D_j(z)=sum_(s!=j) a_s alpha_(j,s)(z).

The ACTUAL killed physical generator before the source switch is

    Q_z=diag(c_j(z)) [K_L−diag(D_j(z))].                         (1)

For each actual competing channel s->u, s!=j, its output has

    z_out=z+j−s,       carried target u,
    B_z[j,(z_out,u)] += kappa_(s->u) c_j(z) alpha_(j,s)(z).       (2)

This construction includes EVERY actual competitor and its actual changed inventory vector. In particular different outputs may shift several coordinates and have unrelated landing profiles. No h(z+nu)=h(z) or neighboring Green-entry comparison is assumed.

If all D_j vanish on the irreducible linkage, its finite translated complex cell is a closed physical communication class. Otherwise Q_z is a finite transient subgenerator. On an infinite physical class the former case is impossible, so the inverse is available and acquired from the raw list at every such marked state.

The complete normalization, clock and reward formulas are

    P_z=(-Q_z)^(-1) B_z,                  P_z 1=1,
    v_z=(-Q_z)^(-1) 1=E[tau_switch],
    E integral_0^tau f(X_s,target_s) ds =(-Q_z)^(-1) f_z,
    E[e^(−s tau) 1_output] =(sI−Q_z)^(-1) B_z,       s>=0.       (3)

Here f_z(j)=f(z+j,j); these are true PHYSICAL time rewards. The derivative at s=0 summed over outputs is -v_z. Higher moments and full phase-type tails are likewise available from the finite inverse. Equations (1)–(3) are finite equations, not an assumed stationary conditional law or an infinite-rate limit. The diagonal factor c_j must remain in the physical reward; discarding it would change the clock.

Polynomial clock bounds also follow without a gap. At integer states every nonzero raw propensity is at least kappa_min, and every total propensity is at most C(1+|z|)^D. A finite linkage path of at most m−1 own-source steps reaches one nonzero competing exit. The actual word/clock argument gives a finite polynomial upper bound for v_z and its bounded physical rewards. Equivalently its matrix-forest denominator has a positive witnessed exit forest. This is an existence and finite-state acquisition statement; its polynomial exponent and constants may be very poor.

## Why this resummation still does not solve the live obstruction

For the ordered degree-seven network, residual z=(0,n,n) makes every source-switch output coordinatewise at least z. Hence every first-switch entropy reward is nonnegative, and most are positive. The code acquires its exact symbolic physical v_z and normalized output kernel. It finds

    E_((z,0)) tau_switch ~ n/2,

while the first-switch entropy reward is outward. This is an actual slow activation layer, not an omitted mixing gap. It must be continued through repayment. The stopped A-return construction in `UNPINNED_ACTIVATION_CYCLE.md` does exactly that for its two-inventory diagnostic.

Thus the resolvent earns the actual-time local operation and data, but not a global boundary oracle. A recurrence proof would still need a weighted return inequality for the coupled output kernel or a different longer-cycle representation. The banked bulk theorem and pinned-controller theorem do not furnish it automatically.
