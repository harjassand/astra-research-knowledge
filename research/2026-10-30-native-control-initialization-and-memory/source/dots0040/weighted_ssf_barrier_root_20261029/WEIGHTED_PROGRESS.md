# Tuned connected-animal progress for small-component SSF configurations
2026-10-29 23:36 UTC. Root candidate proof, to be independently checked. This is an actual weighted-drift construction, not an assumption of a favourable Lyapunov function.

## A. Abstract finite geometry and inputs to verify for SSF
Let x be a bit configuration on a bounded-degree graph of check vertices. Every enabled correction h flips a nonempty set D_h, of size k_h<=k, which is a clique in this graph. It removes m_- occupied vertices and adds m_+ empty vertices, with

 d_h=m_--m_+ >= beta k_h >0.

There is one actually chosen accepted correction per active hub, with attempt rate at least lambda>0. Each check vertex belongs to at most nu possible D_h (all hubs, not only currently active ones). Constants are independent of volume.

For the configuration under consideration require a partition of its occupied checks into S_C, indexed by small reduced-error components, with containers J_C satisfying:

1. J_C are connected, pairwise disjoint, and contain exactly S_C among occupied checks.
2. |J_C|<=b0 |S_C|.
3. Active hubs are assigned uniquely to components. All their D_h lie in J_C, and their number g_C>=kappa |S_C|.
4. Every active D_h contains at least one occupied check (automatic from d_h>0).

These are not intended as new assumptions of quantum-error-correcting capability. For the expander SSF application: take error components in a sufficiently enlarged fixed incidence graph; include every check/read/candidate footprint in the underlying finite-radius geometry. Define J_C as the fixed-radius check neighbourhood containing the supports of every candidate whose read footprint meets C. Choosing components using twice this radius makes different J_C disjoint; choose the check graph's fixed power so J_C is connected and D_h is a clique. Bounded degree gives |J_C|<=D0 |C|. A subset of a minimum-weight representative is reduced, so FGL confinement gives |S_C|>=h|C| and b0=D0/h. FGL candidate mass plus bounded candidate multiplicity gives kappa, and complete read-footprint separation makes these genuinely active moves for the global syndrome, not counterfactual restricted moves. This application/interface must be independently verified; all error components must lie below the stated FGL cutoff.

### Explicit SSF container construction
For each data vertex v let Gamma(v) be its incident checks, R_h the full read footprint of hub h, and B_h the union of checks consulted/changed by its candidate family. Define

 J_v=Gamma(v) union union_(h:v in R_h) B_h.

Connect data vertices u,v whenever J_u intersects J_v, and include any other already required bounded-radius footprint edges. Every J_v and every degree remain uniformly bounded. For error components C in this data graph put J_C=union_(v in C)J_v. Distinct J_C are disjoint by construction. Choose the check graph to include cliques J_v and J_v union J_u for each data edge; then every J_C is connected. This is still a fixed bounded-degree graph, independent of the particular error.

A violated check in J_C must have an incident error vertex u; since Gamma(u) is in J_u, intersection forces u into C. Thus the occupied checks of J_C are precisely sigma(E_C), with no outside cancellation. An active hub must read at least one erroneous vertex, because an all-zero consulted syndrome admits no strictly improving move. If it read erroneous vertices from two components, their J sets would both contain B_h and intersect. Therefore each active hub is assigned uniquely, all its changed-check sets lie in J_C, and its global decision equals the decision for E_C alone. FGL candidate mass, at most M candidates per hub and at most B checks per candidate, gives g_C>=c1|sigma(E_C)|/(BM). Set kappa=c1/(BM). Confinement and bounded |J_v| give b0 as above.

## B. Full, untruncated animal potential
For every nonempty connected set A of check vertices put

 f_A(x)=exp(a|A|) theta^{|A|-|A intersect supp(x)|},
 V(x)=sum_A f_A(x),
 W(x)=sum_A |A| f_A(x),

where 0<theta<1 and a=c log(1/theta), 0<c<1. Sums are over ALL finite-volume connected animals, not a cutoff truncation. Let A0 bound the number of size-m animals rooted at any vertex by A0^m. In particular V(0)=O(number of checks) if A0 theta^{1-c}<1. The potential may be exponentially large on dense configurations; that is intentional.

## C. Per-move monotonicity with strict slack
Fix one accepted flip D, |D|=k_D. An animal A increases only if it contains t added and r removed vertices with t>r. It then intersects D, so B=A union D is connected. Every such B strictly decreases, since it contains all changes. Directly,

 f_B(pre)/f_A(post)
 =exp[a(k_D-r-t)] theta^{m_+-r}
 >= exp(a m_-) theta^{m_+}=:R_D.

For the inequality, substitute a=c log(1/theta): the ratio's exponent is minimized at t=m_+, r=0, since c<1. A fixed B has at most 2^{k_D} source preimages A. Targets B are never increasing animals, so no circular charge occurs. If

 R_D >= 2^{k_D+1}/(1-theta^{d_h}),

all positive increments consume at most half the negative increment of their targets. All other negative increments can be retained or dropped. Thus

 V(x xor D)-V(x)
 <= -(1-theta^{d_h})/2 sum_(connected B containing D) f_B(x)
 <= -(1-theta)/2 sum_(connected B containing D) f_B(x).    (1)

A single choice c>(1-beta)/(1+beta), followed by sufficiently small theta, enforces the displayed R_D inequality uniformly for every accepted move of bounded size. Indeed log R_D >= (k_D/2)[c(1+beta)-(1-beta)] log(1/theta). This is compatible with vacuum summability because c<1.

Truncating the animal sum prematurely invalidates this argument: A union D may lie outside the truncation. The full finite-volume sum is essential here.

## D. Aggregate weighted coverage: one-component completion
Define

 Dsum(x)=sum_B f_B(x) n_contained(B),
 n_contained(B)=#{active h:D_h subset B}.

We prove W<=C1 Dsum+C0 N_chk, with constants independent of volume and component sizes.

Choose eta in (0,1-c). Sparse animals with |S intersect A|<eta|A| obey f_A<=theta^{(1-c-eta)|A|}. Their total contribution to W is at most

 C0 N_chk,  C0=sum_(m>=1) m[A0 theta^{1-c-eta}]^m,

finite for sufficiently small theta.

For a dense animal let n_intersect(A)=#{active h:D_h intersects A}. Call it rich if n_intersect(A)>=kappa eta |A|/4. Assign its weight to these intersecting hubs. For each such h, B=A union D_h is connected, and

 f_B>=theta^{(1-c)k}f_A.

There are at most 2^k preimages for fixed h,B. Hence rich-animal weight contributes at most

 C_rich Dsum,
 C_rich=4*2^k theta^{-(1-c)k}/(kappa eta).

For a non-rich dense animal, call component C poor for A if

 n_C(A):=#{active h assigned C:D_h intersects A}
       <(kappa/2)|S_C intersect A|.

The occupied-check mass in non-poor components is at most 2 n_intersect(A)/kappa <eta|A|/2. Therefore

 sum_(C poor)|S_C intersect A| >=eta|A|/2.              (2)

For each poor C, at least kappa|S_C|/2 active hubs have D_h wholly outside A. Each contains an occupied check, and incidence is at most nu, so

 |S_C\A|>=kappa|S_C|/(2nu)>=alpha |J_C|,
 alpha=kappa/(2nu b0).

Complete ONLY this component: B=A union J_C. It is connected because S_C intersects A for the nonzero charges in (2). Put j=|J_C|. Added occupied checks number at least alpha j; added total vertices number at most j. Consequently

 f_B/f_A >=theta^{-[alpha-(1-c)]j}.

Choose c>1-alpha, and put xi=alpha-(1-c)>0. Fixed C,B have at most 2^j preimages A. If 2 theta^xi<=1, summing these sources gives at most |S_C| f_B. Since |S_C|<=g_C/kappa, and all g_C hubs have D_h subset J_C subset B, summing C charges distinct actual active hubs, not an uncontrolled number of components. Combining with (2), poor dense animals contribute at most

 C_poor Dsum,   C_poor=2/(eta kappa).

Thus with C1=C_rich+C_poor,

 W(x)<=C1 Dsum(x)+C0 N_chk.                           (3)

No completion by the whole union of all components, no extensive preimage factor, and no supplied weighted expansion theorem is used.

## E. Actual clean generator drift
Each active hub occurs at rate >=lambda. Equation (1) and then (3) give

 L_SSF V <=-lambda(1-theta)Dsum/2
          <=-kappa_V W+b_V N_chk,
 kappa_V=lambda(1-theta)/(2C1),  b_V=kappa_V C0.        (4)

Parameter selection is noncircular: choose c in (max{(1-beta)/(1+beta),1-alpha},1); choose eta=(1-c)/2; then choose theta small for the per-move charge, vacuum/sparse-animal convergence and 2theta^xi<=1. All choices depend only on the fixed code/interface constants, not volume or cutoff.

Equation (4) holds on the stated small-component configurations. It is NOT claimed globally: trapping syndromes outside that basin can violate strict drift. It is also not a statement that an arbitrary finite HGP fixture meets the expander hypotheses.

## F. Consequential next steps, not silently imported
For syndrome-diagonal V, the exact local-orbit operator inequalities in coherent_basin_barrier_20261029 bound continuous local Hamiltonian/Lindblad perturbations by a constant times W. If the container interface and a high-V logical/exit boundary are verified, (4) supplies the previously missing clean drift for a killed-basin coherent-noise proof. Neither a physical projection onto the basin nor a Pauli-noise approximation would be required. The physical finite-rate controller still needs a separate service/hypocoercivity transfer; (4) is for ideal atomic SSF operations.
