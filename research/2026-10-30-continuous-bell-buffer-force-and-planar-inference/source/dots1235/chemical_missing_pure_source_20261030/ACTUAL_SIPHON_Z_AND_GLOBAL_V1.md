# Actual siphon-aware complementary value and global synthesis
Status: personal derivation, not independently reviewed. This file, LOCAL_OCCUPATION_LEMMA_V1.md, REFINED_FIRST_RESET_LEMMA_V1.md and ACTUAL_SEED_REPAIR_V1.md form the new candidate proof. No previous review receipt is extended automatically.

## Family and target statement
Fix d>=2, integers q>m>=2, and fixed positive coefficients. The homogeneous degree-m fast composition graph is finite and strongly connected, contains mA and A+(m-1)X_i for each reservoir i, every complex contains A, and each A+(m-1)X_i has a positive-rate edge increasing its A count. All fast complexes carry common catalyst qB. Add the actual connector 0->A+B->mA+qB->0.

The candidate statement is: this countable mass-action chain is nonexplosive; every closed communicating class is positive recurrent; and each class's invariant law has finite E exp(theta(N+B)) for every fixed theta>0. No global irreducibility, dimension-uniform constants, arbitrary state-dependent rates, or general weak-reversibility theorem is claimed.

## 1. Exact activity structure
Let I indicate that some fast COMPOSITION source is enabled and h=q-m. Put Z=B-N-hI. Any enabled fast firing produces its product complex, which is again a source. Conversely, if a firing could turn an inactive predecessor into an active successor, the predecessor was already enabled for that firing. Hence fast firings preserve I. Strong connectivity and at least two distinct complexes ensure outgoing edges; self-loops can simply be discarded.

Adding A cannot disable a source. An inactive activation creates at least m A and therefore enables mA. If A>=1 and the state is inactive, then A<=m-1 and every reservoir coordinate <=m-2. Thus

    inactive with A>=1 => N<=K:=(m-1)+(d-1)(m-2).

Inactive A=0 states can have arbitrarily large N and are NOT put into this finite head. For N>K, an A=0 state becomes active after one actual immigration. Set H=K+m.

Exact Z increments remain: fast0; immigration -h if it activates and0 otherwise; inactive activation0; active activation+h; clearing -h if its target is active and0 otherwise.

## 2. Uniform active episodes from occupation, not strict-power clearing
Remove the common catalyst temporarily. The local logarithmic lemma supplies a bounded clearing mean for all sufficiently large active N. For the finitely many smaller active states, an enabled complex can follow a directed complex path to mA, and then clear, with positive probability. This proves finite killed means on each finite active state space; take their finite maximum. No small inactive state is included. Therefore

    sup_active E tau_clear<=C.

The clearing compensator gives E int(A)_m<=1/k_D. Since A<=C_m[1+(A)_m], normalized A-occupation before clearing is also <=C. Restore the catalyst and stop at the first actual connector event. Uniformly over every active composition and B>=q,

    P(immigration first)<=CB^-q,
    P(activation first)<=CB^(1-q),
    E(first connector time)<=CB^-q.

These estimates have NO hidden N factor. They are the exact replacement for the old pure-source uniform polynomial mean argument.

## 3. Actual fixed-Z blocks with the infinite inactive siphon
Take Z=z large, so B>=z. If N>H and the state is active, prescribe clearing before a birth. With probability at least1-Cz^{-(q-1)}, it occurs. If the target is active, this is a down exit. If it is inactive, its new N=N_old-m>K, so it necessarily has A=0. Its next event is immigration at rate k_I; this turns activity on and gives a down exit. Its constant waiting time is included. If the initial state has N>H and is inactive, it likewise has A=0 and the next immigration directly gives a down exit.

For N<=H use the finite protocol: from an active state prescribe clearing; from inactive A>=1 prescribe activation then clearing. If neither gives a down exit, the latter pair reduces N by one. At most H such pairs reach an inactive A=0 state or a down exit. At A=0 prescribe immigrations until activity turns on. At most m immigrations are needed since mA is a source. The first immigration is compulsory; each of at most m-1 remaining immigration races wins with probability >=c/z against activation. N remains bounded throughout this head protocol, so all constants are uniform. A failure ends the block and starts a new block at the same z if no residual exit occurred.

Consequently, uniformly over every initial hidden composition,

    P(block down)>=cz^{-(m-1)},
    P(block up)<=Cz^{-(q-1)},
    E(block duration)<=C.

The large inactive tail is explicitly handled, not assumed finite or invariant. Only active activation can be an up exit. Conditional renewal, without independent blocks, gives first actual nonzero residual exit time sigma_z and

    P(Z_sigma=z+h)<=Cz^{-(q-m)}=Cz^-h,
    E sigma_z<=Cz^{m-1}.

## 4. Nonexplosion is independent of this renewal
For V_0=1+N+B the fast contribution is0. The connector satisfies

    L V_0<=C+CAB-c(A)_m(B)_q<=CV_0.

When B<q or A<m the positive product is at most linear in V_0. On A>=m,B>=q, factorials dominate fixed multiples of A^m B^q and the negative product controls AB. Finite sublevels and stopped localization prove nonexplosion for the actual unrestricted chain, without recurrence or any previously finite stopped value.

## 5. The complementary actual stopped value
Take the same alpha as in ACTUAL_SEED_REPAIR_V1.md, so 0<alpha<1 and alpha h<gamma. For phi(z)=Gamma(z+1)^alpha, the actual residual-exit kernel satisfies

    E phi(Z_sigma)/phi(z)
        <=Cz^{-(1-alpha)h}+Cz^-alpha h ->0.

The same holds for (1+z)^(m-1)phi(z). Choose z0 large and kill on Z<=z0. The per-excursion cost bound Cz^{m-1}phi(z), followed by positive kernel iteration, constructs

    W_Z=E int_0^{tau_{Z<=z0}}phi(Z_s)ds
       <=C(1+Z)^(m-1)phi(Z),
    L W_Z=-phi(Z) on Z>z0.

Set W_Z=0 below threshold. Only active activation enters its positive domain from outside. Its target Z lies in a fixed finite band, while hidden N and B may be arbitrarily large. Thus the exact exterior leakage bound is (LW_Z)^+<=CAB, NOT finite support.

## 6. Joint global drift and moment claim
The personally derived N-directed actual value in ACTUAL_SEED_REPAIR_V1.md satisfies

    LW_r=-phi(r) above r0,
    W_r<=C(1+r)^(m-1+alpha h)phi(r),
    (LW_r)^+<=C below r0.

Both values have the first-holding lower bound phi(residual)/[C(1+N+B)^(m+q)]. This follows directly from their stopped-cost definitions and the polynomial total reaction intensity.

Writing a=(m-1)/(q-1)<1, one has r=N-aB+O(1), Z=B-N+O(1), and

    max(r,Z)>=(1-a)/(3+a)(N+B)-C.

Hence V=W_r+W_Z is normlike. When both residuals are high its drift is negative. When Z is at or below threshold and the total count is large, r is a positive linear fraction of the total and -phi(r) dominates the possible polynomial CAB leakage. When r is at or below threshold, -phi(Z) dominates the bounded leakage from W_r. Both residuals below threshold imply a finite set. Consequently for every theta>0 there is a finite set F_theta such that

    LV<=-exp(theta(N+B)) outside F_theta.

The standard stopped Foster argument on a countable, locally finite, nonexplosive chain yields positive recurrence on each closed communicating class, and its occupation version yields the stated invariant exponential moments. One must use stopped cycle occupations/regeneration, not assume pi(V)<infinity in order to integrate LV. Finite closed classes are immediate; infinite closed classes meet the appropriate finite Foster set. The full state space need not be irreducible.

## Review boundary
The new load-bearing inputs are the local relative occupation proof, the first-reset kernel comparison, and actual inactive seeding repair. This file's complementary trace replaces the pure-source finite-inactive-state premise by a separately treated infinite A=0 siphon. General weakly reversible recurrence, arbitrary missing-source graphs, and novelty remain open. Prior pure-source independent receipts are unchanged.
