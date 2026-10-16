# A monotone binary envelope for the asynchronous sweep

Status: exact pathwise domination and a fixed-constant coarse forcing construction. The candidate probability and logical transfer are written in HOMOLOGY_AND_SLAB_TRANSFER.md; No historical-novelty or physical-implementation claim is made. See STATUS.md for the current review scope.

## 1. Physical process being bounded

On the 4D cubic toric code, a syndrome is a closed F_2 edge chain. At a rate-kappa clock at vertex v, do nothing if any incoming edge is violated. Otherwise pair the nonempty even set of outgoing violated edges in a fixed order and flip the corresponding one or two positively based plaquettes. This is the previously specified trailing-vertex sweep. Use the same rule on the dual lattice for the other CSS sector.

The physical realization has six qubits per cell, dimension 64, seven active jump patterns per primal/dual vertex, and at most 24 qubits in a jump's support. All parameters are independent of L. Independent single-qubit Pauli rates are lambda_X, lambda_Y, lambda_Z; the sector birth rates are lambda_Z+lambda_Y and lambda_X+lambda_Y per plaquette. The auxiliary envelope below is an ANALYSIS VARIABLE, not a noiseless physical controller or a stored clock.

The target initialization is any encoded code-space state. Its initial syndrome and initial envelope are identically zero. A fixed, ideal final syndrome decoder may be used at readout. Implementing that decoder noisily is not included.

## 2. Exact binary map

Let eta in {0,1}^{Z^4} mark vertices that may carry syndrome. Use the same rate-kappa vertex clocks as the physical sweep. At a clock at v, evaluate ALL right-hand sides on the OLD configuration, then update simultaneously:

    eta'_v = eta_v AND (OR_(i=1..4) eta_(v-u_i)),

    eta'_(v+u_i+u_j)
      = eta_(v+u_i+u_j)
        OR (eta_v AND eta_(v+u_i) AND eta_(v+u_j)),  i<j.

Leave every other vertex unchanged. A physical plaquette birth sets all four of its corner eta values to 1, regardless of whether that Pauli event added or canceled actual syndrome edges.

The old-state convention is essential. In particular, the first assignment must not erase eta_v before evaluating the six upper-corner additions.

Every coordinate of this map is an AND/OR polynomial, so the map is monotone under coordinatewise order. The noise map is also monotone.

## 3. Pathwise domination theorem

If the vertex support of the physical syndrome s is contained in {eta=1} initially, it remains contained there under every common sequence of physical births and sweep clocks.

Proof at a correction clock. If the physical syndrome has an incoming edge at v, that edge has a predecessor vertex v-u_i in its support. Both eta_v and that predecessor eta are 1, so the envelope cannot erase v. If there is no incoming edge, cycle parity makes the outgoing degree even. A nonempty outgoing set is acted on, and all actual syndrome incident to v is removed, so the envelope is free to erase v. The two adjacent vertices of a flipped plaquette already belong to the input syndrome support. The only possibly new vertex is v+u_i+u_j. Its creation requires both outgoing input edges, hence eta_v=eta_(v+u_i)=eta_(v+u_j)=1, and the envelope includes it. The physical rule uses at most two pairs, while the envelope includes all six possible pairs. Noise is dominated by setting all four corners to 1. Induction gives the result. QED.

This is a domination of the actual ongoing-noise dynamics, not an identification with a synchronous fine-lattice round.

## 4. Causal geometry of the envelope

Every new upper corner needs the other three corners of that plaquette already occupied. Therefore a finite coordinate box containing eta remains invariant in the absence of outside births.

Every update that can change eta at w reads only sites coordinatewise <= w. Specifically, the death update reads w and its four immediate predecessors. A corner-addition update reads w, w-u_i, w-u_j and w-u_i-u_j. Thus the envelope is spatially feed-forward on the infinite lattice. This property is stronger than monotonicity alone.

If all immediate predecessors of w have become permanently healthy (eta=0), no corner-addition can reinfect w. Its own next clock clears w. Consequently the earlier directed-last-passage certificate applies to arbitrary finite binary islands, not just cycle supports. This observation is used below only to verify a forcing configuration, not as a standalone stability inference.

Two infinite healthy halfspace facts are available:

1. eta=0 on {x_i>=0} stays zero there forever without noise. Any corner addition outside {x_i<0} would require an already occupied source with the same x_i coordinate.
2. If eta=0 on {h(x)<=-s b}, h(x)=sum_i x_i, then each target vertex of rank at most (s+4)b above that plane clears after a directed last-passage time. The predecessors below the plane are permanently healthy. There are finitely many relevant predecessors for each target.

## 5. A concrete coarse forcing map

Partition Z^4 into cells C_z=b z+{0,...,b-1}^4. Define healthy coarse bits

    zeta_z(t)=1 iff eta_x(t)=0 for every x in C_z.

Choose a fixed integer s>=1, a fixed C>2(s+4)log(8), and a fixed integer

    R >= max(s+5, ceil(280 e C)+10).

Then choose an integer b>=4, fixed independently of L, and let Delta=C b/kappa. These are proof parameters; the physical generator has no time dependence or access to this sampling grid. For the torus theorem restrict explicitly to L=b M. No claim for every indivisible L is needed.

Inside the coarse guard |z|_infinity<=R, define five finite forcing sets:

    A_i={z: |z|_infinity<=R, z_i>=0}, i=1,...,4,
    A_5={z: |z|_infinity<=R, sum_i z_i<=-s}.

Let

    phi(zeta)=OR_(j=1..5) AND_(z in A_j) zeta_z.

This is a binary monotone synchronous local map and a deterministic eroder of finite zero islands. Here is a direct proof, avoiding any need to identify minimal forcing sets. For a finite nonempty zero set Z_n, let M_i(n)=max_{z in Z_n} z_i and m(n)=min_{z in Z_n} h(z). Any zero output at z requires a zero predecessor z+w in every A_j. The A_i predecessor has w_i>=0, so M_i(n+1)<=M_i(n). The A_5 predecessor has h(w)<=-s, so m(n+1)>=m(n)+s. Every remaining zero satisfies h(z)<=sum_i M_i(0). Thus no zeros remain after at most 1+(sum_i M_i(0)-m(0))/s steps. The finite support of phi ensures all intervening zero sets are finite. This verifies the attractive-eroder hypothesis used later.

Equivalently, the convex hulls of A_1,...,A_5 have empty intersection: the first four require all coordinates >=0, whereas the fifth requires their sum <=-s.

The proposed comparison is one-sided:

    zeta_(z,n+1) >= phi(theta_z zeta_n)

outside a rare local bad event, uniformly over ALL input configurations. It does not assert that the microscopic Poisson sweep implements phi as a round.

## 6. Uniform good events, with fixed guard sizes

For target cell C_z use the forced-input guard of coarse radius R. Use a larger PRIMITIVE guard of coarse radius R+2: the union of cells C_w with |w-z|_infinity<=R+2. Its fine side length is (2R+5)b. A physical face whose vertices meet this guard has its base in a box enlarged by at most one fine unit in each coordinate. The conservative count 6((2R+5)b+3)^4 therefore bounds all such face births.

For each target and each time slab of length Delta, the primitive good event consists of:

- no physical plaquette birth whose vertices meet the primitive guard;
- successful clearance of every target site for the lower-h healthy-halfspace forcing configuration;
- no m-event backward causal clock chain ending at ANY target vertex at ANY time in the whole slab, where m=floor(R b/2).

The slow event is defined through the finite predecessor DAG of the lower-h last-passage certificate; every relevant vertex is within fine l_1 distance (s+4)b of the target, hence inside the primitive guard. The first m backward events of a causal chain have displacement at most 2m<=Rb, so their clock locations also lie inside this guard. Therefore all three bad flags depend only on the fresh, local primitive Poisson increments. They do not depend on the input configuration.

For the four coordinate-halfspace forcing configurations, infinite-volume invariance is deterministic. For the lower-h configuration, a union bound over b^4 target vertices gives the schedule error bound

    delta_slow <= 2 b^4 exp(((s+4)log(8)-C/2)b).

For backward dependence, a target site can be updated by its own clock or one of six lower-corner clocks. Each such event reads at most five sites, so 35 is a valid overcount of predecessor choices per causal step. All right-hand sides use the pre-event state, so a single event cannot produce an instantaneous chain through its multiple outputs. With m=floor(R b/2), a conservative path-count bound is

    delta_fast <= b^4 (35 kappa Delta)^m/m!
               <= b^4 (35 e C b/m)^m.

This union bound already permits the terminal time to be anywhere in the slab: it counts all ordered m-tuples of events in a slab of length Delta. It is not merely a terminal-observation bound. Since Rb>=4, m>=Rb/4, and the displayed choice of R gives

    delta_fast <= b^4 2^(-m).

The physical-birth contribution is bounded by

    delta_noise <= lambda_sector * 6((2R+5)b+3)^4 * Delta.

All constants are independent of L. First choose C,R; then choose a sufficiently large but fixed b; finally choose a sufficiently small positive lambda_sector/kappa. The total primitive bad-event probability can thereby be made arbitrarily small.

Why this event is uniform in the input: for a given A_j, use monotonicity to replace the input by the maximal infection configuration which is healthy on A_j and infected elsewhere. Inside the forced-input guard it is dominated by the corresponding infinite halfspace configuration. For A_5, any fine vertex with h(x)<=-s b has sum_i floor(x_i/b)<=-s, so the guaranteed fine healthy region contains this halfspace wherever it meets the guard. The absence of an m-event backward chain prevents an outside input or outside birth from affecting a target at any time in the slab. The clearance certificate and path exclusion use only fresh clocks, not the actual state or a past-dependent event. Thus the same primitive good event proves the one-sided forcing inequality simultaneously for all five alternatives and all input configurations.

Write B_(z,n)=1 for the union of the three bad flags. Its marginal is bounded by delta_slow+delta_fast+delta_noise. First choose C,R; then increase the fixed b until the first two terms are as small as required; then choose a strictly positive upper bound on lambda_sector/kappa to make the third term sufficiently small. This order is consistent despite extremely poor constants.

## 7. Fault correlations and infinite-volume product domination

A translated B_(z,n) depends only on primitive increments at coarse distance at most R+3 during slab n. In infinite volume each field B_n is therefore finite-range dependent, and the entire fields for distinct slabs are independent. A residue coloring of period 2R+9 in every coordinate gives chi=(2R+9)^4 colors whose primitive supports are disjoint. In infinite volume, for a finite prescribed set S of bad coarse spacetime locations,

    P[S all bad] <= delta^(|S|/chi),

by taking a color class containing at least |S|/chi locations and multiplying their independent primitive event probabilities. The same bound holds conditionally on the complete primitive past before each slab. This is a local-stochastic bound, not independence of all coarse faults. No residue-color argument is asserted on an arbitrary finite torus.

More directly, the Liggett-Schonmann-Stacey finite-dependence theorem on Z^4 supplies a coupling

    B_(z,n) <= Xi_(z,n),

where the Xi within a slab are iid Bernoulli(p(delta)) and p(delta) tends to zero as delta tends to zero, for this fixed dependence range. Since the B fields use independent increments in different slabs, choose these couplings independently slab by slab. The Xi are then iid in space AND time. This is an analysis coupling; no physical processor performs it.

An explicit quantifier/rate recipe is useful. Set s=1, C=10log(8)+2, and any integer R>=ceil(280eC)+10. This fixes phi, k=4R+4, the spatial dependence range, and therefore the Hartarsky-Toninelli death threshold p_0. Fix p_* in (0,min(p_0,1/2)). The infinite-volume LSS theorem supplies delta_*>0 such that a primitive marginal bound delta_* suffices for domination by iid Bernoulli(p_*). Choose a fixed integer b>=4 such that BOTH

    2b^4 exp(((s+4)log(8)-C/2)b) <= delta_*/3,
    b^4 2^(-floor(Rb/2))          <= delta_*/3.

Finally define the positive sector threshold

    sigma_0 = kappa delta_*
              / [18 C b ((2R+5)b+3)^4].

For lambda_sector<=sigma_0, delta_noise<=delta_*/3 and the total primitive marginal is at most delta_*. The CA and LSS thresholds depend on R,s, but NOT on b, L, kappa, or the physical history. Thus this ordering has no circular choice of parameters. The physical threshold is a fixed positive multiple of kappa, although no numerical usable value is supplied by the abstract imported theorems.

Let theta be the native coarse comparison, initialized at all ones, updated by

    theta_(z,n+1)=0                       if B_(z,n)=1,
    theta_(z,n+1)=phi(theta_n shifted z)  otherwise.

The block inequality gives zeta_(z,n)>=theta_(z,n) pathwise. In infinite volume the iid-death process omega driven by Xi satisfies omega<=theta. Hartarsky-Toninelli Corollary 9.5 then bounds all fixed-k connected spacetime zero components of omega exponentially in their diameter, for sufficiently small p(delta). The all-one initial process dominates the upper-invariant initial process used in that corollary, using the same future deaths; this is solely a distributional comparison.

On a finite torus use native B-driven theta. To apply the infinite-volume theorem, lift the underlying primitive Poisson field in a fixed, injective anchor patch, with the extra R+3 guard, and extend outside independently. Replay the causally complete first-large-cluster witness in infinite-volume theta, then apply LSS there. This avoids asserting product domination on a finite torus and avoids the false claim of a uniform-in-time torus stationary cluster bound. Details are in the transfer companion and the stopped-torus proof.

The constants can be extremely poor: large guards increase chi, and making delta^(1/chi) small may require an enormous fixed b and a correspondingly tiny positive physical-noise threshold. No practical rate or resource advantage follows from an existence bound of this form.

## 8. Scope of the probability and logical transfer

Binary Toom stability at one site alone is insufficient. The needed imported result is the stronger spacetime-cluster bound in Hartarsky-Toninelli Corollary 9.5. The companion gives a stopped finite-torus transfer, the occupied-set cover for the entire time slab, and a fixed local-filling decoder whose decoded homology cannot change at any local physical jump while syndrome components remain small.

The proposed complete mathematical consequence, subject to independent audit of these steps and the exact imported theorem hypotheses, is a bound of the form

    P[any decoded logical failure by time T]
       <= C0 M^4 (1+T/Delta) exp(-c0 M),  L=b M,

for strictly positive, L-independent Pauli birth rates sufficiently small relative to kappa, starting at any encoded code-space state. C0,c0,b,Delta are fixed in L and may be impractically poor. This file does not promote that candidate to historical novelty or to acquired physical memory hardware.

The proposed genuinely new proof principle is the exact monotone envelope plus a one-sided block forcing comparison. Historical novelty has not been established. The present scope does not rely on a stationary Gibbs initialization, a Floquet schedule, or a noiseless physical classical layer.

## 9. Sources and boundaries

- [Kubica–Preskill, 1809.10145](https://arxiv.org/abs/1809.10145): known sweep operation and static perfect-syndrome threshold.
- [Drechsler–Oreg–Aharonov, 2610.05589v1](https://arxiv.org/html/2610.05589v1): quantum/classical reduction; synchronous and Floquet results leave the time-independent nonthermal gap.
- [Swart–Szabo–Toninelli, 2202.10999v1](https://arxiv.org/pdf/2202.10999v1): continuous-time contours in this exact version. Current v3 has a different scope. Its generic asynchronous-eroder warning is respected; no general eroder transfer is invoked above.
- [Gray, 1999, chapter 18](https://doi.org/10.1007/978-1-4612-2168-5_18): continuous-time stability criteria. Only the publisher abstract and the precise discussion in Swart et al. were retrieved so far; the full chapter has not been read.
- [Hartarsky-Toninelli, Kinetically constrained models out of equilibrium](https://www.normalesup.org/~hartarsky/files/research/publi/KCM-CP.pdf), author manuscript dated 11 March 2024, Section 9, especially Corollary 9.5: exponential spacetime zero-component diameter tails for every fixed connectivity radius of an attractive eroder with sufficiently rare iid deaths. Its Section 8 already uses LSS in a block comparison.
- Liggett-Schonmann-Stacey (1997), Domination by product measures: fixed finite dependence plus sufficiently high one-site healthy marginals yields high-density product domination on Z^d. Parent source audit checks the exact primary theorem.

Physical 3D embedding, conditioned-jump fabrication, code preparation, reservoir reset/energy, calibration and imperfect readout remain unacquired. Their full costs are UNKNOWN.
