# Exact accepting pins and undecidable Gibbs uniqueness at fixed positive temperature

Research manuscript, 5 November 2026. Provisional proof with independent internal review; external peer review is outstanding.

## 1. Theorem and proof organization

There is an effective procedure taking a Turing machine and input to a two-dimensional translation-invariant finite-alphabet, finite-range physical interaction with finite nonnegative integer energies, at the fixed inverse temperature beta=1, such that:

- **Nonhalting:** the model has distinct translation-invariant Gibbs states whose means of the explicit on-site spin s are respectively positive and negative. Their equal mixture has nondecaying connected spin correlations.
- **Halting:** the model has exactly one Gibbs state, including among non-translation-invariant states. Every pair of bounded local physical observables has exponentially decaying connected correlations in that state.

The dimension, support shapes, inverse temperature and local energy values are fixed. The alphabet varies effectively with the machine. No halting-time estimate selects any coupling. In particular Gibbs uniqueness, and the stated full-clustering-versus-coexistence promise, are undecidable in this family.

Appendix A gives the complete finite accepting-tableau compiler and its soundness/completeness proof. Appendix B gives the finite integer-energy Fourier construction, explicit auxiliary mixing and polymer-expansion bounds, and the projection/lift theorem for every physical Gibbs state. These appendices include the details needed here; the proof does not rely on an earlier bilayer symmetry theorem, an equilibrium recoloring argument, or translation invariance of the unknown Gibbs state. Standard analytic inputs are identified in Section 10.

The new operation is strict positive-field comparison followed by a subcritical two-replica defect bound in the local spin/tile representation. This supplies actual full uniqueness, rather than only elimination of a selected broken symmetry.

## 2. Physical construction

Let T_M be the compiled labeled Wang set, t=|T_M|. Its finite nonzero-edge components with vacuum exterior are precisely accepting computation rectangles, with one marked anchor per component. Let G=(Z/2Z)^m label the edge colors by distinct real characters, exterior color zero being the trivial character. For tile z, let Chi_z(g) be its four-edge character product.

Use ONE Ising spin s_v in {−1,+1} and set

    I_z(s_v)=1                         if z is unmarked,
    I_z(s_v)=1[s_v=+1]                 if z is marked,
    F_v = sum_{z in T_M} Chi_z(g) I_z(s_v).

Set C0=10000(t+1), D=C0+t, and b_v in {1,...,D}. The physical site energy is

    E_v=0 if b_v<=C0+F_v, and E_v=1 otherwise.

Give each nearest-neighbor spin mismatch energy K=20. Store east/north edge variables at their lower/left endpoint, as described in Appendix B. Then the site alphabet has size 2D|G|^2; the site factor has support {v,v−e1,v−e2}; spin factors are nearest-neighbor. All physical energies are in the fixed finite set {0,1,20} before terms on common supports are combined.

Summing b gives C(1+aF_v), where

    C=C0+t exp(−1),
    a=(1−exp(−1))/C,
    u=ta<10^(−4).

The conditioned auxiliary-edge Dobrushin row sum is at most 6u<0.0006, unchanged by the eligibility replacement. The accepting-polymer gas has activities w_gamma=a^{|gamma|}, with anchor eligibility 1[s_anchor=+]. For every n the number of labeled n-site species containing a specified site is at most (16t)^n. Consequently the same uniform convergent cluster expansion applies.

With all dangling group edges freely summed, the exact auxiliary partition function is

    Xi_V(s) = sum_{P compatible, supports contained in V}
                 product_{gamma in P} w_gamma 1[s_anchor(gamma)=+].

Every physical Gibbs state, with no TI assumption, projects to the single-Ising specification multiplied by the limiting Xi ratios and has a canonical positive finite-polymer lift

    rho(ds,dP)=nu(ds) Q_s(dP).

Given s, Q_s is the unique low-activity hard-core gas with the allowed anchors. Given P, the spins have the nearest-neighbor Ising specification with s=+ forced at every occupied anchor. Appendix B proves the arbitrary-state projection and canonical lift in detail, using an all-plus spin reference in each finite change region.

## 3. Local spin/tile DLR for every canonical lift

This section removes a potentially serious gap: a Gibbs statement about finitely many polymer species cannot simply be called a local tile DLR statement without a proof.

Encode P by a tile letter z_v in {vacuum} union T_M. Its finite nonzero-edge components specify its polymer species uniquely. On the joint finite site alphabet (s,z), impose the nearest-neighbor color-matching rules, vacuum exterior color zero, and the on-site rule that a marked tile requires s=+. Give each occupied tile energy −log a and each spin mismatch energy K. This is a local hard-constraint proof representation, not the physical finite-energy model.

The canonical law is supported on configurations having only finite accepting components. This subset is preserved by any admissible finite spatial modification. Indeed an edit in a finite set Lambda can meet only finitely many old components, each finite. A new component that meets Lambda can use only the modified sites and finitely many old components touching its boundary. Their union is finite. A new infinite component cannot be created. The finite-component compiler therefore applies to every new component.

The separate conditionals of rho imply exact finite-move weight ratios:

1. Removing/inserting an entire eligible polymer gamma has odds w_gamma, whenever compatible with all other polymers.
2. An allowed finite spin change at fixed polymers has the usual Ising weight ratio and must obey the occupied-anchor pins.

Take any admissible finite spatial change from (s,z) to (s',z'), supported in Lambda. Remove all old polymers whose supports meet Lambda. There are finitely many. Every surviving outside portion has a nonzero boundary edge toward Lambda; its unchanged outside endpoint forces it into a final component meeting Lambda. Thus the final polymers meeting Lambda restore all temporary exterior changes. Change the spins in Lambda; no unaffected polymer has an anchor there. Insert all final polymers whose supports meet Lambda. These moves are all permitted. The old and new involved supports lie in some finite, possibly much larger, deterministic box on each event specifying the finite old/new species lists.

There are countably many such lists. On each corresponding measurable event the spatial replacement is a fixed finite composition of elementary insertion/removal and spin transformations. Their Radon–Nikodym ratios multiply and telescope to

    exp(−Delta H_Ising) a^{Delta(number of occupied tiles)}.

All temporary changes outside Lambda are restored; the final ratio is precisely the local spin/tile Gibbs ratio on Lambda. For fixed initial and final local patterns the replacement is injective, so the images of the countable partition are disjoint. Summing the finite-composition identities therefore gives the same ratio for the full local replacement.

These ratios identify the conditional law on every finite Lambda among all compatible fillings. No omitted infinite sector occurs because finite edits preserve the canonical finite-component subset. Thus rho satisfies the SAME nearest-neighbor local spin/tile DLR specification for every physical Gibbs state, including non-TI states.

## 4. One accepting species gives a strictly positive comparison field

Assume M halts and choose any one finite accepting species gamma_* of activity w_*>0. Its size is finite but need not be bounded effectively from M. Set

    zeta = sup_x sum_{eta containing x} w_eta
         <= sum_{n>=1}(16ta)^n < infinity.

Fix every spin other than s_x. In a finite free polymer volume, changing s_x from − to + permits precisely the species anchored at x. Such species are mutually incompatible. Hence the partition ratio is exactly

    R_x = Xi(s_x=+)/Xi(s_x=−)
        = 1 + sum_{gamma anchored at x} w_gamma
                  Q_{s_x=−}(no polymer intersects gamma).

The statement passes to the canonical infinite volume by the uniform activity tails and the convergent partition ratios. For any finite support S, the vacancy bound is

    Q_s(no polymer intersects S)
       >= exp(−sum_{eta intersects S} w_eta)
       >= exp(−|S| zeta).

For example, order the relevant species and use their conditional occupied odds at most w_eta, so conditional absence probabilities are at least 1/(1+w_eta); take the convergent product. This works for forbidden anchors as well.

Therefore

    R_x >= 1+w_* exp(−|gamma_*| zeta) = exp(2h_*),
    h_* := (1/2) log(1+w_* exp(−|gamma_*| zeta)) > 0.       (4.1)

Every target spin single-site conditional probability is consequently at least the ordinary ferromagnetic Ising conditional with mismatch cost K and uniform field h_*, evaluated at the same neighboring spins.

The target spin specification need not be attractive. Attractiveness of the LOWER ordinary Ising specification suffices: if target configuration s is pointwise above reference configuration t, then

    target P(s_x=+ | s elsewhere)
      >= Ising(h_*) P(t_x=+ | t elsewhere).

For any finite region, couple the heat-bath chains using common uniform updates, putting minus boundary spins on the reference chain. Order is preserved, and finite-state positivity gives stochastic domination of stationary laws. Integrate the target exterior conditionals and take the region to infinity. Ordinary Ising at h_*>0 has a unique Gibbs state, so every target spin Gibbs marginal dominates that state. By ferromagnetic field monotonicity and the h down to zero limit, it also dominates the zero-field Ising plus state:

    nu >=_st mu_Ising,0^+.                                (4.2)

This argument uses standard positive-field Ising uniqueness but no quantitative bound depending on h_*. The field can be arbitrarily small. Its strict positivity selects the plus comparison state; all quantitative estimates below are for the fixed K=20 zero-field plus state.

## 5. Independent coverings of minus spins and occupied tiles

### 5.1 Exact finite-box Ising contour gas

In an Ising box with all-plus exterior, mark each dual edge crossing a disagreeing primal bond. The finite marked dual graph is even: every dual vertex has degree0,2,or4. Define a contour to be a nonempty CONNECTED component of this graph, retaining degree-four vertices rather than resolving them ambiguously into simple loops.

Different contours share no dual vertex. Conversely any compatible family of finite connected even dual graphs with filled hulls inside the box determines a unique spin assignment with plus exterior. Its relative weight is exactly the product of exp(−K n_gamma), where n_gamma is the contour's number of edges. This is an ordinary hard-core gas. Deleting a whole connected even component leaves an allowed family, even when components are nested. Its occupation conditionals are bounded by exp(−K n)/(1+exp(−K n)). Thus its species indicators are dominated by independent Bernoulli indicators with those probabilities.

Every minus site lies in the filled hull of at least one contour. Use an iid soup containing all finite contour species, not only the ones inside the finite box. Coupled subsequential limits of finite-plus-box spin laws and this fixed soup law give a coupling of the zero-field Ising plus state with the soup in which every minus site is covered. To justify passage of coverage to the limit, first truncate the contour sizes and then use the uniformly summable rooted large-contour probability. No unproved assertion about an infinite contour representation is needed.

For upper bounds below use independent occupation probabilities z_gamma=exp(−Kn), larger than the exact Bernoulli parameters if desired.

### 5.2 Rectangles and independence

For every fixed complete spin configuration, the canonical accepting-polymer gas has occupied-species conditionals at most w_gamma/(1+w_gamma). It is therefore dominated by an iid species field with these probabilities, or with the larger probabilities w_gamma. The dominating iid field has the same law for EVERY complete spin configuration and may be coupled independently of it.

First couple a target spin configuration s with an Ising-plus comparison configuration eta using (4.2). Next sample the canonical polymers and their iid upper field with a coupling depending on s alone, whose upper-field marginal is independent of s. Thus this rectangle soup is also independent of eta. Finally sample the contour soup conditional on eta from the Ising-plus coupling, using no rectangle randomness. The contour and rectangle soups are independent in their joint marginal. The target's minus sites lie inside the contour-hull union, and its occupied tile sites lie inside the rectangle-soup union.

For two independent target canonical states, perform independent copies of this coupling. Their sitewise disagreement set

    D={(s,z) differs between the replicas}

is contained in the union of TWO independent contour-hull soups and TWO independent rectangle soups. Outside this union both replicas have precisely the same local state (+,vacuum). Controlling minus sites alone would not suffice because occupied tile supports transmit local interactions; they are included explicitly.

## 6. A uniform subcritical bound with nearest-neighbor adjacency included

Inflate each hull or rectangle support S to S^+, its closed nearest-neighbor one-step neighborhood. A nearest-neighbor path in the original bad-site union is contained in an intersection-connected chain of these inflated supports. For a soup species with inflated support S and upper occupation probability z_S define

    B = sup_x sum_{S contains x} |S| z_S 2^{diam_infinity(S)}.

The sum includes species labels and all four soups separately. Inflation increases cardinality by at most 5 and the rooted count by at most 5. It increases infinity-diameter by at most 2.

For a rectangle with n sites, rooted species count is at most (16t)^n, its cardinality is n, and its uninflated infinity-diameter is at most n. The TWO rectangle soups therefore contribute at most

    B_rect <= 200 sum_{n>=1} n (32ta)^n
            < 200 (0.0032)/(1−0.0032)^2 < 0.645.           (6.1)

For a contour with n>=4 edges, its filled hull has at most (n+1)^2 sites and infinity-diameter at most n. If a hull contains a specified site, some dual vertex lies within a box with at most (2n+3)^2 choices. The number of connected n-edge graphs containing a specified dual vertex is at most16^n: a deterministic doubled-edge traversal gives a walk of length2n, with at most4 choices per step, determining the graph. Dropping evenness only increases this bound. Hence the TWO contour soups contribute at most

    B_contour <= 200 sum_{n>=4} (n+1)^2(2n+3)^2
                                      (32 exp(−20))^n.   (6.2)

Using exp(20)>2^20, the geometric parameter in (6.2) is below 1/32768. The polynomial-geometric series is less than 10^(−10), already far below the margin in (6.1). In particular

    B < 2/3.                                             (6.3)

The arithmetic is to be certified by the accompanying exact-rational checker, not inferred from a simulation.

Here and below an inflated-soup component means a component of the INTERSECTION graph of occupied inflated supports. It does not mean an arbitrary nearest-neighbor component of their union. The required implication is that a nearest-neighbor path in the ORIGINAL uninflated bad-site union gives an intersection chain of inflated supports.

For completeness, consider an intersection chain of distinct occupied inflated supports beginning at 0 and ending at x. If their diameters are d_1,...,d_k, then sum_i d_i>=||x||_infinity. Independence bounds the chain probability by the product of species probabilities. Summing after multiplying by 2^{sum_i d_i}, and at each overlap choosing a site in the preceding support, gives at most B^k. Allowing repeated chains only increases this numerical sum; independence was only used for the distinct-species chains. Thus

    P(an intersection chain of inflated supports joins 0 to x)
       <= sum_{k>=1} B^k 2^{−||x||_infinity}
       < 2 times 2^{−||x||_infinity}.                    (6.4)

A union bound over sites arbitrarily far away implies that all intersection components of occupied inflated supports have finite spatial union almost surely. Local finiteness follows from the rooted activity sums, so these components also contain finitely many species. Every nearest-neighbor disagreement component is contained in such a spatial union and is therefore finite. Formula (6.4) supplies the required uniform exponential bound for the original disagreement connection event.

## 7. Finite replica swaps prove uniqueness and clustering

Let rho_1,rho_2 be canonical local spin/tile lifts of any two physical Gibbs states. Under their independent product, all disagreement components are finite by Sections 4–6.

For a bounded local observable f supported in A, exchange the two replicas on the union K of disagreement components meeting A. This is a finite union of finite components. Across every boundary edge of K, the two replicas agree. Consequently swapping their entire spin/tile labels on K preserves the product of their local Gibbs weights, including the hard constraints. On-site factors and edges inside K simply exchange; crossing-edge factors exchange because the outside labels coincide.

The disagreement set itself is unchanged by swapping, so the event specifying K is invariant. For each finite K, the product DLR equation makes the swap measure-preserving on that event. Summing over the countably many finite K gives a measure-preserving transformation that changes f(replica1)−f(replica2) to its negative. Thus rho_1(f)=rho_2(f). Local observables determine the measure, so the canonical local spin/tile law is unique. This is uniqueness within the canonical class containing all physical lifts, not a claim about unrelated hard-tile Gibbs sectors supported on infinite tile components.

For its unique law rho, take two independent copies. For f,g supported in A,B,

    Cov_rho(f,g)
      = (1/2) E[(f_1−f_2)(g_1−g_2)].

The same swap changes the first difference's sign and leaves the second fixed unless a disagreement component joins A to B. Therefore

    |Cov_rho(f,g)|
      <= 2 ||f||_infinity ||g||_infinity P(A connected to B in D)
      <= 4 ||f||_infinity ||g||_infinity |A||B|
                         2^{−dist_infinity(A,B)}.         (7.1)

This is an explicit two-replica disagreement argument, related to the established disagreement-percolation uniqueness criterion, rather than an inference from a unique FK backbone or from small one-site defect density alone.

## 8. Transfer to full physical uniqueness and all-observable clustering

Every physical Gibbs law has the unique spin marginal just established. Conditioned on the complete spins, the auxiliary group law is the unique uniformly Dobrushin Gibbs law, and the multiplicities have their explicit independent local conditional kernels. Thus the full physical Gibbs law is unique. Existence is standard for a finite-alphabet finite-range finite-energy specification; uniqueness also makes the state translation invariant.

For clustering, let F,G be bounded local PHYSICAL observables, with supports A,B separated by distance r. Write

    Cov_mu(F,G)
      = E_nu[Cov_mu(F,G | complete spins)]
        + Cov_nu(Fbar,Gbar),
    Fbar(s)=E_mu[F | complete spins].

The uniform conditioned auxiliary Dobrushin matrix, of row sum below0.0006 and fixed finite spatial range, bounds the first term exponentially in r. The local multiplicity kernels do not add a long-range interaction.

The same comparison estimate gives exponential quasilocality of Fbar as a function of the complete spin configuration. If two configurations agree in the ell-neighborhood of A, their Fbar values differ by at most C_A ||F|| exp(−c_aux ell), uniformly in M. Only local factors outside that neighborhood change, and the Dobrushin influence-path sum bounds their effect near A. Fix an arbitrary exterior reference to approximate Fbar by a spin-local function Fbar_ell on that neighborhood, with this uniform sup-norm error, and do the same for Gbar.

Take ell=floor(r/3). The truncated supports remain separated by at least r/3 up to a fixed collar. Apply (7.1) to these spin-local functions. Their support cardinalities grow only polynomially in r; that factor is absorbed into a smaller exponential rate. Adding the truncation errors and the conditional-covariance term proves

    |Cov_mu(F,G)| <= C_{A,B} ||F||_infinity ||G||_infinity exp(−c r),

for a universal c>0 and constants computable from support geometry and the displayed uniform estimates. No lower bound on h_* or on the first accepting activity is used in these rates.

## 9. Nonhalting branch and undecidability

If M does not halt, no finite accepting species exists. The exact Xi ratios are one. Every physical spin marginal is then the ordinary zero-field Ising specification at mismatch cost K=20, and the Ising plus and minus states each lift to physical Gibbs states via the unique conditional auxiliary law. Both lifts are TI.

The same bare-Ising contour cover already proved in Section 5 gives an explicit plus-phase minority-spin bound

    delta_I <= sum_{n>=4}(2n+3)^2(16 exp(−20))^n
             < 121 (2^(−16))^4/(1−2^(−15)) < 10^(−16).

Here exp(20)>2^20 and the consecutive ratio of the polynomial factor is below 2 for n>=4. Thus the plus/minus spin means have magnitude at least 1−2 delta_I. In the plus state a union bound gives E[s_0 s_x]>=1−4 delta_I at every separation, and the spin-flipped minus state has the same two-point function. The equal mixture of their physical lifts has spin mean zero and connected correlation at least 1−4 delta_I>0.99 at every separation. The on-site spin s is a physical observable, not a dual tile or an abstract order parameter.

Thus halting implies full uniqueness and full connected-correlation clustering, while nonhalting implies coexistence and a physical TI Gibbs witness with nondecaying connected correlations. An algorithm deciding either promised alternative would decide halting.

The proof is about a variable effective alphabet, exact finite-energy tables, and beta=1. It does not establish fixed-alphabet undecidability with bounded integer energies and fixed supports, robustness under arbitrary perturbations, an experimentally feasible simulator, or any computable crossover scale. Full uniqueness and exponential equilibrium clustering do not by themselves supply the finite-size or dynamical guarantees not supplied by the equilibrium estimates here.

## 10. Standard inputs and literature boundary

- Appendix A supplies the finite accepting-tableau grammar. Appendix B supplies finite-group orthogonality, the conditional auxiliary Dobrushin estimate, the positive polymer projection, and its converse. The physical pin mask is explicit in Section 2.
- Ordinary ferromagnetic Ising uniqueness at nonzero uniform field is a standard Lee–Yang consequence. A primary uniqueness reference is J. L. Lebowitz and A. Martin-Lof, *On the Uniqueness of the Equilibrium State for Ising Spin Systems*, Commun. Math. Phys. 25 (1972), 276–282: https://sites.math.rutgers.edu/~lebowitz/PUBLIST/jll.pub_83.pdf .
- The finite-volume stochastic comparison is the standard Holley/common-uniform heat-bath argument; the proof in Section4 explains why target FKG is unnecessary. R. Holley, *Remarks on the FKG Inequalities*, Commun. Math. Phys. 36 (1974), 227–231: https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/holley.pdf .
- Two-independent-realization disagreement uniqueness is established methodology, not a novelty claim. See J. van den Berg, *A uniqueness condition for Gibbs measures, with application to the 2-dimensional Ising antiferromagnet*, Commun. Math. Phys. 152 (1993), 161–166, https://ir.cwi.nl/pub/2298/2298D.pdf ; and J. van den Berg and C. Maes, *Disagreement Percolation in the Study of Markov Fields*, Ann. Probab. 22 (1994), 749–763, https://ir.cwi.nl/pub/1472/1472D.pdf . The exact finite-component swap argument is given here rather than assuming an unmatched theorem for the polymer representation.
- The potential new contribution is the combination that turns arbitrarily small positive accepting activity into an all-Gibbs-state uniqueness/clustering distinction for a strictly positive classical physical model at fixed temperature. Priority and external correctness remain subject to independent scrutiny.

## 11. Scope of verification

Independent internal proof reviews checked the finite compiler, arbitrary-state physical projection and local tile lift, positive-field comparison, exact even-component contour representation, independence of the upper soups, overlap-chain bound, replica swaps, and physical clustering transfer. These are internal mathematical reviews, not external peer review or machine-checked formal verification. The numerical and finite combinatorial programs supplied with this manuscript verify stated constants and finite implementations; they are not evidence of nonhalting or a substitute for the infinite-volume proofs.

The interaction alphabet can be extremely large even for a small input machine. No laboratory feasibility or efficient finite-size algorithm is claimed.

## Appendix A. Complete finite accepting-tableau compiler


### 1. Result and scope

For every machine/input pair (M,w), the algorithm below produces a finite alphabet of edge colors, a distinguished color 0, and a finite set of labeled Wang tiles. Every finite nonzero-edge-connected component in a color-matching configuration on Z², with vacuum outside the selected tiles, is a solid rectangle of width and height at least two. It contains exactly one marked tile. Its rows encode a genuine bounded-width computation of M from w, and its final row contains a genuine halting state. A finite component exists if and only if M halts on w.

There is no additional possibility of a finite headless cycle, a ring with a hole, or a nonaccepting component. Different rectangles may touch across zero-colored edges without being in the same component.

This is a finite-component statement, not a claim that all bi-infinite matching configurations are accepting rectangles. Infinite planes, strips, and periodic winding components are not excluded by the grammar. They must be handled by the separate uniform auxiliary mixing/projection argument. In particular, a free-dangling-edge Fourier identity must not be replaced by a periodic-volume identity without accounting for winding terms.

### 2. Normalize the machine without a cleanup assumption

A cleanup sweep and an all-ACCEPT top row are unnecessary. A finite horizontal automaton can check that the top row contains exactly one halting head and no other head.

First make halting absorbing and complete the transition table on every nonhalting state/symbol pair. A missing transition of the original machine can be redirected to the distinguished halt state if that is its halting convention. Introduce a distinct absorbing reject state.

A two-sided tape is represented on a one-sided physical tape. Physical cell j >= 0 stores a pair (A_j,B_j), representing original cells j and -j-1. A head has a machine state and a track bit A or B. Its moves are:

- Track A, original right: physical right, keep A.
- Track A, original left away from j=0: physical left, keep A.
- Track A, original left at j=0: stay in the same physical cell, switch to B.
- Track B, original left: physical right, keep B.
- Track B, original right away from j=0: physical left, keep B.
- Track B, original right at j=0: stay in the same physical cell, switch to A.

The transition writes only the selected component of the symbol pair. Each physical cell carries a permanent bit b, equal to one exactly at j=0. This makes the move rule local. The other component of a pair is retained. Thus one original step is one physical step, including a track switch at the origin.

On an interval of width W, a move through the right wall instead leaves an absorbing reject head at its source cell, after the prescribed write. It cannot create a halt head. A physical move through the left wall is likewise rejecting, although valid folded histories never request one. Importantly, overflow takes precedence even if the same original transition changes the state to HALT. This only rejects some narrow certificates; a sufficiently wide interval reproduces every finite genuinely halting history.

The finite cell alphabet Sigma consists of:

- A pair of tape symbols, the bit b, and no head.
- A pair of tape symbols, the bit b, a machine state (including HALT and REJECT), and a track bit.
- A poison letter for each b, used only to totalize malformed local inputs.

Let # be an outside-wall symbol, not in Sigma.

### 3. A completely local radius-one update

The deterministic map F: (Sigma union {#})^3 -> Sigma is needed only on triples whose center lies in Sigma. It is defined as follows, with a deterministic poison convention on malformed cases.

Every nonhalting/nonreject head computes its write, new state, new track, and physical displacement from its old state, selected tape symbol, track, and permanent bit. HALT and REJECT compute a stay-put identity update. A head's proposed motion can be computed from its own letter alone; whether the target is # is then visible in its centered triple.

For a center letter x:

1. Its output symbol pair is its own prescribed write if x carries a head, and its unchanged pair otherwise. Its permanent bit is copied.
2. A head whose displacement is zero remains at the center with its new state/track.
3. A head moving into an outside wall remains at the center as REJECT.
4. A head moving to an actual neighbor leaves no head at its old cell.
5. An incoming head proposal from the left or right neighbor installs that proposal's new state/track at the center, using the center's output symbol pair.
6. Conflicting head proposals, an incoming head entering an already occupied center, any poison in the triple, or other malformed symbol data produce the poison letter with the center's permanent bit. Any case not covered above is assigned this same poison output.

For the valid one-head configurations reached from the prescribed initial row, rules 1-5 alone apply. Their output has exactly one head: an ordinary simulated head, HALT, or absorbing REJECT. The global update is precisely the bounded-width folded simulation. The table is finite and effective. There is no nondeterministic choice of a purported successor.

The poison behavior is not relied upon to establish soundness: the exact bottom row and the deterministic one-head invariant already exclude all malformed histories.

### 4. Two explicit finite row automata

Let P be the finite folded input prefix of length ell >= 1. At cell zero it contains the initial head on track A and permanent bit one. All other prefix cells have no head and bit zero. Unused tape components are blank. Let z be the blank, headless, bit-zero cell letter. The bottom-row language is exactly

    P z*.

The geometric width restriction already requires W >= 2. In particular, the bottom automaton does not accept a prefix of P. The DFA states are 0,...,ell plus a rejecting sink. From state i<ell, the only nonrejecting letter is P_i and the next state is i+1. From state ell, the only nonrejecting letter is z and the state remains ell. Start state is 0; sole accepting state is ell. Undefined transitions enter the rejecting sink, which is never accepted.

The top-row DFA has states unseen, seen, and dead. A headless nonpoison letter leaves unseen or seen unchanged. A HALT-head letter changes unseen to seen. A second HALT head, any other head, or any poison enters dead. Start is unseen; sole accepting state is seen. Thus its language has exactly one HALT head and otherwise plain tape letters.

For interior rows use the one-state DFA that accepts every letter in Sigma. Tile conditions separately require the permanent bit of the center letter to be one exactly in the leftmost column, at every height.

### 5. Complete finite tile generation algorithm

A candidate tile is the finite tuple

    (h,v,p,x,q,k_minus,k_plus),

where h is L,I,R; v is B,I,T; p,q are in Sigma union {#}; x is in Sigma; and k_minus,k_plus are states of the row DFA selected by v. Enumerate all such tuples and retain exactly those satisfying:

1. p=# iff h=L, and q=# iff h=R. Thus all other p,q are in Sigma.
2. The permanent bit of x is one iff h=L.
3. k_plus is the DFA transition from k_minus on letter x, and neither state is dead/rejecting.
4. If h=L then k_minus is the DFA start state.
5. If h=R then k_plus is an accepting DFA state.

Put y=F(p,x,q). The four edge colors are the following finite tuples, with every displayed tuple a nonzero color:

    West  = 0                  if h=L,
            (H,v,p,x,k_minus)  otherwise.
    East  = 0                  if h=R,
            (H,v,x,q,k_plus)   otherwise.
    South = 0                  if v=B,
            (V,h,x)            otherwise.
    North = 0                  if v=T,
            (V,h,y)            otherwise.

H and V are distinct formal tags. The single symbol 0 is distinct from every tuple, including tuples carrying blank tape letters or numerical DFA state zero. Mark the tile iff (h,v)=(L,T).

This algorithm is the tile set; it only enumerates finite alphabets and evaluates finite transition tables. It is not an oracle for whether an accepting rectangle exists. Labeled duplicates with the same four colors may be retained as distinct tile species, or deduplicated together with their mark. Retaining them merely changes positive multiplicities, never the existence or validity of a component. For a quantitative Fourier implementation, use the count of retained labeled types consistently.

### 6. Proof that all finite components are accepting rectangles

Every selected tile has at least one nonzero horizontal edge and one nonzero vertical edge. At a nonzero edge, color matching forces a selected neighboring tile in the same component.

Take a finite component and a tile at its minimum y-coordinate. Its south edge must be zero, so it has v=B. Follow its horizontal nonzero edges. Finiteness forces a row beginning with h=L and ending with h=R, with h=I between them. Every nonzero horizontal edge carries v, so the whole row has v=B. Neither an internal gap nor a premature L/R is possible: zero cannot match a nonzero color.

Every cell of this bottom row has a nonzero north edge. The matching row above has exactly the same h sequence, because vertical colors carry h. Its leftmost and rightmost cells therefore cannot extend the row horizontally. Horizontal colors give it one common v, which is I or T because its south edges are nonzero. Repeat. Finiteness forces a T row, and a T row has no nonzero north edge. There can be no extra cells connected beyond the resulting rectangle: its complete exterior boundary is color zero. A hole, a ragged row, or a branch would contradict this induction. Because L and R are distinct choices, and B and T are distinct choices, both dimensions are at least two.

In each row, matching overlapping horizontal colors forces the stored triples to be the consecutive triples of one word x_0...x_(W-1), with # immediately outside the two ends. The DFA states match too. Consequently the bottom word is exactly P z*, the top word contains exactly one HALT head, and each interior word has no extra filter.

Vertical matching forces x_i of the next row to equal F of the preceding row's triple, for every i. The bottom row is the true initial one-head configuration, so induction gives the unique finite-interval simulation. A right-wall collision enters REJECT forever and cannot meet the top filter. Hence a valid rectangle certifies genuine halting before any boundary failure. The marked tile is exactly its unique top-left corner.

Conversely, if M halts after t original steps, choose W >= 2 large enough to contain every folded position used by those steps and the complete input. The bounded-width simulation then reaches HALT with no rejection. Stack the initial configuration and its successive images, continuing the absorbing halt state if needed so that height is at least two. Take its first row as B, last row as T, and all others as I. Their overlapping triples and accepting DFA runs give exactly the prescribed tiles and matching colors. This constructs a finite component.

### 7. Reproducible finite checks

The accompanying `check_explicit_tableau_grammar.py` implements the finite tile generator, including the folded local update. Its rectangle counter assembles actual Wang colors without calling the machine update or row DFA. It compares those counts with independently iterated histories for seven machines, widths 2–4 and heights 2–5. A separate exhaustive status enumeration permits vacuum and side-touching rectangles and checks every closed assignment in the listed small boxes. The ancillary polynomial identity is checked at the current C0=10000(t+1). The saved results report the actual checks performed. These finite checks supplement, and do not replace, the arbitrary-machine proof above.

The physical pin eligibility and finite integer-energy realization are specified in Appendix B. They do not alter this tile compiler.


## Appendix B. Integer-energy realization, auxiliary mixing, and the positive projection

This appendix supplies the complete analytic passage from the finite-energy physical model to the positive accepting-polymer representation. It applies to arbitrary Gibbs states, without translation invariance or extremality. The finite-tableau compiler in the preceding appendix supplies the only combinatorial input: finite nonzero-edge-connected matching components are precisely accepting rectangles, each with one marked anchor, and such a component exists if and only if the encoded machine halts.

### A. Physical alphabet and exact integer-energy realization

Let T be the finite labeled tile set and put t=|T|. Each tile z has four edge colors c_N(z),c_E(z),c_S(z),c_W(z); color 0 is the exterior color. Choose G=(Z/2Z)^m large enough to assign a distinct character chi_c:G->{−1,+1} to every edge color, with chi_0 identically one. On each undirected lattice edge place g_e in G, and at each site v place one spin s_v in {−1,+1} and one multiplicity variable b_v in {1,...,D}, where

    C0=10000(t+1),       D=C0+t.

For an unmarked tile put I_z(s_v)=1. For a marked tile put I_z(s_v)=1[s_v=+1]. Define

    Chi_z(g)=product_{e incident to v} chi_{c_e(z)}(g_e),
    F_v(g,s)=sum_{z in T} Chi_z(g) I_z(s_v).

All characters are real signs, so F_v is an integer and |F_v|<=t. Give the site factor the energy

    E_v(g,s,b)=0 if b_v<=C0+F_v(g,s), and 1 otherwise.

The threshold lies between C0−t and C0+t=D, so it specifies a valid finite table. Give each nearest-neighbor edge the energy

    20 * 1[s_v!=s_w].

Thus every physical local energy is a finite nonnegative integer. In particular the physical model contains no hard constraint or noninteger microscopic coupling.

At inverse temperature beta=1, summing b_v gives exactly

    sum_{b_v=1}^D exp(−E_v)
      = (C0+F_v)+(t−F_v)e^−1
      = C [1+aF_v],
    C=C0+t e^−1,
    a=(1−e^−1)/C.

Write f_v(g,s)=1+aF_v(g,s). The constants C are independent of the spins and group variables. With u=ta,

    a<1/C0,       u<10^−4,       1−u<=f_v<=1+u.               (A.1)

The occurrence of e^−1 and a in the summed representation is an exact consequence of summing states with energies zero and one, not a choice of noninteger energy.

For an ordinary site alphabet store the east and north group variables at their left and lower endpoints. The alphabet has cardinality 2D|G|². The factor at v reads only the site coordinates at v,v−e_1,v−e_2, and the Ising interactions are nearest neighbor. These interaction support shapes are fixed independently of the machine. Denote the spin Hamiltonian by H_0(s)=20 sum_{<v,w>}1[s_v!=s_w]. Its equivalent Ising exponent coefficient is J=10.

### B. Exact free-boundary Fourier identity

For a finite set V of factor centers, freely integrate all edges incident to V with normalized counting measure on G:

    Z_V(s)=integral product_{v in V} f_v(g,s) dg.

Expand each factor as one plus the sum of its labeled tile terms. Each term selects at most one tile at each selected site, contributes a per selected tile, and contributes its anchor eligibility indicator if that tile is marked. On an edge joining two selected sites, character orthogonality gives

    |G|^−1 sum_g chi_c(g)chi_d(g)=1[c=d].

If only one endpoint is selected, including at a dangling boundary edge, its integral is 1[c=0]. The surviving selections are consequently exactly color-matching finite selected configurations with exterior color zero. The compiler identifies their nonzero-edge components as accepting rectangles. Distinct components are site-disjoint; they may touch across edges on which both colors are zero.

Let gamma denote a whole labeled accepting rectangle, including its support and its unique anchor. Put w_gamma=a^{|gamma|}. The exact identity is

    Z_V(s)=Xi_V(s)
      =sum_{P compatible, every gamma contained in V}
           product_{gamma in P} w_gamma 1[s_anchor(gamma)=+1]. (B.1)

All terms on the right are nonnegative. The signs present before the group integrations have disappeared by orthogonality, not by approximation.

The boundary convention matters. Fixing dangling group variables can leave unmatched nonzero characters, and infinite matching configurations can contain infinite components. Neither fact is suppressed by assertion. Sections C–E identify the specification of every physical Gibbs state using mixing of the actual strictly positive group-variable model before invoking (B.1).

### C. Uniform conditioned auxiliary Dobrushin estimate

Fix an arbitrary complete spin configuration s. The group-variable model has factors f_v in [1−u,1+u]. Put R=(1+u)/(1−u). Changing one group edge variable g_f can influence the conditional distribution of a distinct edge variable g_e only when e and f share a vertex. If they do, exactly one factor common to their incident vertices changes. The ratio of the new and old unnormalized single-edge conditional weights lies in [R^−1,R].

The elementary likelihood-ratio bound says that two normalized probability measures whose unnormalized density ratio lies in [m,M] have total variation distance at most

    (sqrt(M/m)−1)/(sqrt(M/m)+1).

It follows here that the single-edge influence coefficient is

    c_ef <= (R−1)/(R+1)=u.

Each square-lattice edge has at most six distinct neighboring edges sharing an endpoint. Therefore the Dobrushin row sum is

    alpha=sup_e sum_{f!=e} c_ef <=6u<0.0006<1.              (C.1)

This estimate is independent of the spin configuration, group size, machine, volume, and group boundary values. The usual influence-path proof of the Dobrushin criterion now gives a unique conditional group-variable Gibbs law Q_s^g. Explicitly, an influence path reaching a changed boundary kernel from an edge at distance d in the edge-adjacency graph has length at least d; the total weight of length-l paths is at most alpha^l. For a bounded function A supported on a finite edge set E_A, one obtains the convenient comparison bound

    |E_fixed A−E_free A|
       <= |E_A| osc(A) alpha^d/(1−alpha),                    (C.2)

where d is the minimum edge-adjacency distance from E_A to the region where the kernels differ. Constants or an extra fixed boundary collar may be enlarged without changing the statement. Free integration of dangling edges, fixed boundary values, and omission of factors outside a larger box all differ only near that boundary.

In particular, the finite free-boundary expectations of any fixed local A converge to E_{Q_s^g}A uniformly in s. The same influence-path estimate gives exponentially decreasing conditional covariances and exponentially local dependence on changes in the spin configuration: changing s at a site changes only its one group factor. These uniform estimates are the auxiliary inputs used later when transferring clustering back to physical observables.

### D. Explicit low-activity polymer expansion

The number of connected n-site subsets of Z² containing a prescribed site is at most 16^{n−1}, hence at most 16^n. Indeed choose a deterministic spanning tree and traverse it from that site, obtaining a nearest-neighbor walk of length 2(n−1); the walk reconstructs its visited site set. Each support has at most t^n tile labelings. Accepting rectangles are a subset, so

    sup_x sum_{gamma containing x} w_gamma e^{2|gamma|}
       <= sum_{n>=1}(16e²ta)^n.

Define

    rho=16e²ta<0.012,
    delta=rho/(1−rho)<0.01215<1/80.                          (D.1)

The inequality rho<0.012 follows directly from ta<10^−4 and e²<7.5. If gamma is a fixed polymer, incompatibility means site overlap, and therefore

    sum_{eta incompatible with gamma} w_eta e^{2|eta|}
       <= |gamma| delta < |gamma|.                          (D.2)

This checks the Kotecky–Preiss condition with size function A(eta)=|eta| even after replacing every activity w_eta by w_eta e^{|eta|}. Turning any anchor eligibility from one to zero only decreases the left side. Thus all bounds hold uniformly over every complete spin configuration and every subset of forbidden anchors.

For clarity, the cluster formula being used is

    log Xi_V(s)=sum_{k>=1} 1/k!
       sum_{gamma_1,...,gamma_k contained in V}
          phi^T(gamma_1,...,gamma_k)
          product_i [w_gamma_i 1{s_anchor(gamma_i)=+1}],

where

    phi^T(gamma_1,...,gamma_k)
       =sum_{connected graphs H on {1,...,k}}
            product_{ij in E(H)}(−1[gamma_i incompatible gamma_j]).

A species is incompatible with itself, as appropriate for this usual repeated-label cluster formula. Condition (D.2) gives absolute convergence and the rooted bound for the exponentially inflated activities. Summing first over a root polymer containing a prescribed site gives a finite bound by the left side of (D.1) on the absolute cluster weights meeting that site, with exponential weight in their total polymer sizes. Overcounting a cluster by the possible roots is harmless.

Every nonzero connected cluster has connected union of its supports. Assign its negative log-weight contribution to that union. The cluster formula therefore defines an absolutely summable, translation-invariant induced spin interaction, with an exponentially weighted diameter norm. It gives uniform convergence of local spin-change partition ratios, as well as uniform convergence of finite-species marginals of the free-boundary polymer gases.

Write Q_s^p for the resulting canonical infinite-volume hard-core gas. Its finite-species DLR conditional occupation odds are w_gamma 1[s_anchor(gamma)=+1] when gamma is compatible with the other occupied species, and zero otherwise. The expansion gives the unique small-activity gas and its exponential size tails. In particular its configurations contain only finite accepting polymers. These statements concern the positive abstract gas, not the signed expansion at fixed group variables.

The standard cluster-expansion input is R. Kotecky and D. Preiss, “Cluster expansion for abstract polymer models,” Communications in Mathematical Physics 103 (1986), 491–498. Equations (D.1)–(D.2) check its hypotheses with a generous numerical margin.

### E. Projection of every physical Gibbs state

Let mu be any Gibbs state of the finite-energy physical model. Sum the local multiplicity variables. The remaining joint spin/group law has the positive factors f_v and the bare Ising interaction H_0. Conditional on the complete spins s, its group-variable law satisfies the conditional group DLR equations. Section C gives uniqueness, so

    mu(dg | s)=Q_s^g(dg)                                    (E.1)

for almost every s. No translation invariance or special boundary construction has been used.

Let Lambda be a finite spin region. Fix two assignments eta and eta' in Lambda and a common complete exterior configuration xi. Set s=eta xi, s'=eta' xi, and define the bounded positive local ratio

    L_{s,s'}(g)=product_{v in Lambda} f_v(g,s')/f_v(g,s).

The joint finite-spin-change Radon–Nikodym identity, followed by disintegration using (E.1), gives for the spin marginal nu

    nu(eta'|xi)/nu(eta|xi)
       =exp(−H_0(eta'|xi)+H_0(eta|xi)) E_{Q_s^g}L_{s,s'}.     (E.2)

Finite physical energies ensure that all finite-block spin conditionals are strictly positive. This identity is first understood for almost every exterior xi. The uniform comparison below supplies its everywhere-defined quasilocal version.

In a free group box V containing Lambda,

    E_{Q_{V,s}^{g,free}}L_{s,s'}
       =Z_V(s')/Z_V(s)
       =Xi_V(s')/Xi_V(s).

Uniform conditioned group mixing therefore proves the all-boundary identity

    E_{Q_s^g}L_{s,s'}
       =lim_{V increasing to Z²} Xi_V(s')/Xi_V(s).            (E.3)

The limit is uniform in s,s' with this fixed change region. Combining (E.2)–(E.3) identifies every physical spin marginal as Gibbs for H_0 plus the induced cluster interaction of Section D.

This is the point at which arbitrary physical boundaries are handled. One does not apply the free Fourier formula directly to a fixed-boundary or infinite dual tiling. First the strictly positive auxiliary model removes its boundary influence from local ratios; only then is the exact free Fourier identity used.

### F. Canonical positive lift and cancellation of its normalizers

Fix a finite Lambda and exterior spin configuration xi. Use the reference eta^* identically + in Lambda, and set s^*=eta^* xi. For another assignment eta put

    B(eta)={v in Lambda:eta_v=−1},
    E_B={P:no occupied polymer has its anchor in B}.

The gas at s=eta xi is exactly the reference gas conditioned on E_{B(eta)}, since these are precisely the anchor eligibilities that have been removed. In every finite free polymer volume,

    Xi_V(eta xi)/Xi_V(s^*)=Q_{V,s^*}^p(E_{B(eta)}),
    Q_{V,eta xi}^p=Q_{V,s^*}^p( · | E_{B(eta)}).

Although E_B concerns infinitely many possible species, its anchors lie in the finite set B. Exponential rooted activity tails approximate it uniformly by cylinder events involving finitely many species. The finite-volume identities thus pass to the limit:

    b_eta=Q_{s^*}^p(E_{B(eta)})>0,
    lim_V Xi_V(eta xi)/Xi_V(s^*)=b_eta,
    Q_{eta xi}^p=Q_{s^*}^p( · | E_{B(eta)}).                  (F.1)

Positivity does not depend on a formal series. For every species its full-conditional occupation probability is at most w_gamma/(1+w_gamma), so sequential conditioning and continuity from above give

    Q_{s^*}^p(E_B)
      >= product_{anchor(gamma) in B}(1+w_gamma)^−1
      >= exp(−sum_{anchor(gamma) in B}w_gamma)>0.

By the projection formula, the spin conditional kernel is

    nu(eta|xi) proportional to exp(−H_0(eta|xi)) b_eta.        (F.2)

Define the canonical joint law

    nu_hat(ds,dP)=nu(ds) Q_s^p(dP).

Multiplying (F.1) by (F.2) cancels b_eta exactly. Conditional on xi,

    nu_hat(eta,dP|xi)
      proportional to exp(−H_0(eta|xi))
              1[E_{B(eta)}](P) Q_{s^*}^p(dP).

Consequently, given all polymers and exterior spins, the spins in Lambda have precisely the bare Ising conditional law with + forced at the occupied anchors:

    weight(eta | xi,P)
      =exp(−H_0(eta|xi))
         product_{v in Lambda:some gamma in P anchored at v}1[eta_v=+1]. (F.3)

Given all spins, the polymer law is the positive canonical gas Q_s^p. In particular its finite removal/insertion odds are exactly the positive activities with the displayed anchor eligibility, with no division by a vanishing activity.

Encode P as a local tile configuration: put its tableau label at each occupied site and the vacuum label elsewhere. Every sampled component is finite. These conditional identities define the canonical positive representation used in the main proof. The further assertion that this encoded joint law obeys the spatially local spin/tile DLR equations, for every physical Gibbs state, is proved explicitly in Section 3 of the main proof by finite spatial updates and the absence of infinite components. It is not inferred merely from separate block conditionals or from a translation-invariant variational principle.

The positive representation is a representation of the spin marginal. It is not a pointwise positive expansion of a fixed physical group-variable configuration.

### G. Converse physical lift and exact nonhalting specialization

We record the converse without relying on a specially chosen physical boundary. Let nu be a Gibbs state of the induced spin specification. Define its spin/group lift by

    mu_0(ds,dg)=nu(ds) Q_s^g(dg).

For a finite spin change s to s', multiplication by the local ratio L_{s,s'} sends Q_s^g to a Gibbs law for the group interaction at s'. Uniqueness from Section C therefore gives the exact finite-perturbation identity

    Q_{s'}^g(dg)
       =L_{s,s'}(g) Q_s^g(dg)/E_{Q_s^g}L_{s,s'}.              (G.1)

The spin odds in the induced specification are (E.2). Multiplying them by (G.1) cancels the expectation in numerator and denominator. Thus the conditional spin-change odds in mu_0, given the group variables, are exactly

    exp(−H_0(s')+H_0(s)) L_{s,s'}(g),

which are the required physical spin/group odds. The conditional group DLR equations already hold by construction. These positive finite-coordinate kernels determine the joint finite-volume Gibbs law: one may update the finitely many spins and group coordinates successively, and the resulting finite-state heat-bath chain is irreducible. Hence mu_0 is Gibbs for the positive spin/group interaction.

Finally, conditional on (s,g), restore the b_v independently with probabilities proportional to exp(−E_v(g,s,b_v)). This recovers a Gibbs state of the original finite-energy physical model. It also shows uniqueness of a physical Gibbs lift once its spin marginal is fixed, because both its conditional group law and its conditional multiplicity kernels are unique.

If the machine does not halt, the accepting-polymer family is empty. Equation (B.1) then gives Xi_V(s)=1 for every finite V and every spin configuration. The induced interaction is identically zero, and (E.3) makes every auxiliary correction to the spin odds equal to one. Therefore every physical spin marginal is an ordinary zero-field Ising Gibbs state at J=10. Conversely, the preceding construction lifts every such Ising state to a physical Gibbs state.

In particular both the plus and minus Ising phases lift, and are distinct at K=20. Translation covariance of the unique group kernels preserves translation invariance of these witnesses. This conclusion is exact; possible infinite matching patterns in a formal dual description do not change it.
