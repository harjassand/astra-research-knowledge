# Continuous-time and logical transfer for the monotone-envelope route

Status: complete proof candidate for review, not a historical-novelty certificate or a hardware claim. This companion assumes the exact envelope and the fixed primitive events of MONOTONE_ENVELOPE.md. Hartarsky-Toninelli Corollary 9.5 and infinite-volume Liggett-Schonmann-Stacey domination are imported theorems, not new claims.

## 1. Conventions and the native comparison

Take L=b M, with the constants b,R,C,s fixed as in the envelope note. Let Delta=C b/kappa. Fine spatial distances used for decoder geometry are ambient torus l_infinity distances. Coarse spacetime distances used for connectivity are Euclidean, with periodic spatial coordinates and integer time coordinates.

The fine envelope eta starts at zero. Its healthy coarse bits are zeta_(z,n)=1 exactly when all fine vertices in C_z are zero at time n Delta. Let B_(z,n) be the state-independent, local primitive bad flag in slab n. Define a native toroidal comparison theta by theta_0=1 and

    theta_(z,n+1)=0                         when B_(z,n)=1,
    theta_(z,n+1)=phi(theta_n shifted by z) otherwise.

The uniform block inequality and monotonicity imply zeta_n>=theta_n at every sampled time. Thus every fine infected cell at a sample is a theta-zero cell. We do not assert any finite-torus LSS domination.

Fix

    k=4R+4,       ell=M/128.

Assume M is sufficiently large compared with R, for example M>=1024(R+k+10). All such lower bounds are independent of time and of the noise realization.

## 2. Uniform occupied-set cover throughout a slab

Let S_n be the coarse cells containing at least one eta=1 vertex at any time in the CLOSED slab [n Delta,(n+1)Delta]. Then

    S_n subset N_R({z:theta_(z,n)=0})
                union {z:theta_(z,n+1)=0},                 (2.1)

where N_R is the spatial coarse l_infinity neighborhood.

Proof. Fix z in S_n. If B_(z,n)=1, theta_(z,n+1)=0 by definition. Otherwise there is no birth in the primitive guard and no m-event backward causal clock chain from any target vertex at any time in the slab, with m=floor(Rb/2). Trace an occupied target backward through its AND/OR dependency graph. If every relevant initial value were zero and there were no relevant birth, its value would remain zero because every update preserves the all-zero configuration. Therefore some initial eta=1 input or some birth is an ancestor. A birth within the guard is excluded. An ancestor outside the forced-input radius-R guard needs at least m causal events, since one event moves by at most two fine l_1 units; this is also excluded. Hence an initial eta=1 ancestor belongs to C_w for |w-z|_infinity<=R. Then zeta_(w,n)=0 and theta_(w,n)=0. QED.

The fast-event flag covers a terminal time anywhere in the slab. The Poisson ordered-tuple bound counts all sequences with event times in the slab, so this is stronger than observing eta only at its final endpoint.

For every z in S_n choose one representative theta-zero point q_z: either (w,n) with |w-z|_infinity<=R, or (z,n+1). If two fine occupied vertices are adjacent, their cells have coarse l_infinity separation at most one. Their representatives have spatial Euclidean separation at most 4R+2 and time separation at most one, hence spacetime separation less than k.

Consequently every connected fine syndrome component at any time in slab n maps into ONE k-connected spacetime zero component of theta. If the fine component has torus l_infinity diameter at least L/32, there are two representatives with spatial torus l_infinity separation at least

    M/32 - 2R - 1 > ell.                                 (2.2)

The loss of one coarse unit is the cell-boundary rounding error. Thus a large continuous-time syndrome component forces a large theta-zero spacetime component, even between observations. This uses the exact syndrome-to-eta pathwise domination.

## 3. First-large-cluster transfer from a torus to infinite volume

For a fixed integer N, reveal all theta-zero vertices in time layers 1,...,N, one layer at a time. Within each new layer use a fixed deterministic spatial order. Values in the layer have already been computed from the complete old layer; this reveal order does not change the PCA.

Stop when an inserted zero p=(z,n) first creates a k-connected component C with diameter at least ell. Prior to insertion every component has diameter below ell. Every point of the new component lies within ell+k of p: each old component attached to p contains a vertex within k of p and has diameter below ell. Therefore

    C subset B_(ell+k)(p),

and C has diameter at most 2(ell+k). This is a spacetime ball; in particular its spatial projection is inside a torus patch of radius ell+k.

The component is causally complete for zero replay. A non-forced zero at (x,t) means phi(theta_(t-1) shifted x)=0. For each forcing set A_j there is a zero predecessor (x+w,t-1), w in A_j. Every such predecessor is within Euclidean spacetime distance sqrt(4R^2+1)<k, is already revealed because its time is earlier, and therefore belongs to C. A forced zero needs only its primitive B flag. Recursively, every zero witness terminates at a forced B=1 point; there are no initial zeros.

For EACH fixed prospective anchor p, take a deterministic spatial l_infinity patch centered at z of radius ell+k+R+4. The witness's Euclidean radius ell+k also bounds its spatial l_infinity radius, and each primitive guard adds at most R+3 in that latter norm. The assumed lower bound on M makes the complete patch injective on the coarse torus. Copy all underlying Poisson clock and face-birth increments in that patch for times 0 through n Delta to an infinite Z^4 primitive field, and extend independently outside the patch. This infinite primitive field has exactly its usual iid law: the copied locations are distinct torus locations. The lift is performed per fixed anchor, before any probability union bound; the random witness does not choose the patch or condition its primitive law.

Construct infinite native comparison theta^infinity from this field, starting at all ones. Every B flag required by the lifted C is identical to its toroidal flag because its full primitive guard was copied. Induction in time replays every zero of C in theta^infinity. Extra zeros outside the patch only help: phi is monotone in healthy bits. Since the whole witness lies in a patch of spatial diameter below M/2, its lifted Euclidean distances agree with its torus distances. Thus the theta^infinity zero component of p has diameter at least ell.

Now apply infinite-volume LSS separately in every slab. The fixed-range fields B^infinity are dominated by iid Bernoulli Xi with parameter p(delta) tending to zero with the primitive marginal bound delta. The iid-death healthy PCA omega is below theta^infinity. Hence every lifted theta^infinity-zero witness is also an omega-zero witness.

Hartarsky-Toninelli Corollary 9.5 gives, for this attractive eroder phi and fixed k, constants c>0 and p_0>0 such that an upper-invariant iid-death trajectory has

    P[diameter of its zero component at p >= ell]
       <= p^(c(ell+1)),       0<p<=p_0.                  (3.1)

For the all-one initial trajectory, couple an upper-invariant initial state below all ones and use the same future Xi. Its zeros contain those of the all-one trajectory, so (3.1) also bounds the event needed here. The invariant law is used only as an analysis distribution; the physical memory is initialized in its code space, not in a Gibbs or stationary noise ensemble.

There are at most N M^4 anchor points. A union bound gives fixed constants C_1,c_1>0 with

    P[theta has a first k-zero component of diameter >= ell
      during layers 1,...,N]
       <= C_1 N M^4 exp(-c_1 M).                         (3.2)

This is a first-exit estimate for a finite torus over a finite time horizon. It does NOT assert uniform-in-time stationary stability on a finite torus. Indeed a finite death-only PCA can eventually enter its all-zero absorbing state.

## 4. A fixed decoder with local transition stability

For a closed edge syndrome s, use vertex-connected components of its edge support. Each component is itself a closed F_2 edge chain because boundaries at distinct vertex components cannot cancel.

Set

    rho=L/8,       r=L/32.

If every syndrome component has ambient torus l_infinity diameter below rho, define a deterministic decoder D(s) as follows. For each nonempty component C choose a deterministic anchor, lift its vertices and edges into the radius-rho torus coordinate patch around that anchor, and fill the cycle by a deterministic 2-chain inside its coordinate bounding box. A connected component in this small patch has a unique consistent lift up to translation by L. The full cubical box is contractible, so the required filling exists. Fix an order on faces and choose the first filling under any fixed finite search rule. Set D(s) equal to the sum of these component fillings. D(0)=0.

If some component is larger, use an arbitrary fixed global filling of s. Such a filling exists for physical syndromes because s=partial E for an accumulated physical error 2-chain E. If desired define the decoder arbitrarily on non-boundary syndromes, which do not occur in the stated model.

No efficiency or noisy physical implementation of D is claimed. It is a fixed final readout map independent of the error history.

**Local transition lemma.** Suppose every component of s has diameter below r, and F is the 2-chain of one local physical event. Both a noise face and a sweep correction of one or two positively based faces have vertex support in one unit l_infinity cube. Let s'=s+partial F. Then

    [F + D(s) + D(s')]=0 in H_2(T_L^4;F_2).             (4.1)

Proof. Let W be the vertex support of partial F. If partial F is empty, F is a closed chain supported in a unit contractible box and is already a boundary; no decoder component changes. Otherwise every old or new component whose filling can change intersects W. Components disjoint from W are unchanged as edge sets and their fixed decoder fillings cancel exactly.

Every affected old component lies within torus distance r of W. All new affected components use only those old components and the changed edges, so they too lie in the same neighborhood. Since W is in a unit cube, the union is contained in a single embedded coordinate box of side at most 2r+1. Each new affected component has diameter at most 2r+1<rho for sufficiently large L. Thus both decoder fillings use the small-component rule and remain within the coordinate hulls of their components. Those hulls, all affected old/new fillings, and F lie in this one common embedded box. The choice of anchor does not change that hull up to the unique common lift.

The chain F+D(s)+D(s') is closed because its boundary is partial F+s+s'=0. A closed 2-chain in a contractible cubical box is a 3-boundary. Therefore its torus homology is zero. QED.

This lemma controls the accumulated 2-chain, not merely the instantaneous syndrome. Let E_t be the sum of all physical noise and correction chains through time t. Its decoded homology is

    H_t=[E_t+D(partial E_t)].

Initially H_0=0. At every local event before a component reaches diameter r, (4.1) makes H_t invariant. A finite torus has finitely many primitive events in every bounded time interval, so induction over events is legitimate. Thus if no syndrome component ever reaches diameter r before T, H_t=0 throughout [0,T]. A long accumulated membrane cannot silently change logical homology while every local transition remains in this regime.

## 5. Candidate continual-noise memory consequence

Use the explicit parameter recipe in MONOTONE_ENVELOPE.md: s=1, C=10log(8)+2, fixed R>=ceil(280eC)+10, iid-death target p_*<min(p_0,1/2), its LSS primitive threshold delta_*, and fixed b making both clock error bounds at most delta_*/3. Define

    sigma_0 = kappa delta_*
              / [18 C b ((2R+5)b+3)^4].

This is strictly positive and independent of L. Assume

    lambda_X+lambda_Y <= sigma_0,
    lambda_Z+lambda_Y <= sigma_0.

For T>=0 take N=ceil(T/Delta)+1. If there is no large theta-zero component through layer N, Sections 2 and 4 show that the fixed decoder suffers no logical transition in that CSS sector by time T. Applying (3.2) to both sector marginals and using a union bound gives constants C_0,c_0>0 independent of L,T such that

    P[any decoded logical Pauli failure by time T]
       <= C_0 M^4 (1+T/Delta) exp(-c_0 M),   L=bM.        (5.1)

Shared Y births may correlate the sectors; the union bound does not require independence. One may take c_0 to be a fixed positive multiple of c_HT log(1/p_*)/128, reducing it by a further factor of two if using an anchor-to-point version of the imported diameter tail. For any fixed a<c_0, times T=Delta exp(aM) have failure probability tending to zero as M grows. In terms of L, this is exponential lifetime with exponent a/b. The constants and threshold may be astronomically poor; no practical advantage follows.

The supplied mathematical architecture is the time-independent, constant-range 4D toric sweep Lindbladian: six qubits per unit cell, local Hilbert dimension 64, at most 24-qubit jump support, seven active syndrome patterns per vertex per sector, and rate kappa per attempted vertex update. Neither b nor Delta is a controller size or physical clock. All encoded code-space states, including states entangled with an external reference, share the same classical Pauli-trajectory law because rates depend only on syndrome. On paths with no decoded logical failure the recovered logical channel is exactly the identity. Thus (5.1) also bounds entanglement infidelity, and twice its right-hand side bounds the diamond distance to the identity logical channel.

The theorem covers the specified independent local Pauli birth model and exact syndrome-conditioned correction jumps. It does not establish stability under arbitrary coherent perturbations of the generator. Preparing the code, implementing conditioned jumps, embedding a 4D graph in a physical 3D system, reservoir/reset/energy costs, calibration, and noisy readout are unacquired and UNKNOWN. Historical novelty remains a separate literature question. The candidate mathematical proof needs independent review, particularly the uniform primitive-event construction, fixed-patch zero replay, and component-filling geometry.

## 6. Primary sources used

- Kubica-Preskill, [A cellular automaton decoder for topological quantum codes, 1809.10145](https://arxiv.org/abs/1809.10145): sweep operation, causal geometry, and static decoding; not this continual asynchronous theorem.
- Drechsler-Oreg-Aharonov, [2610.05589v1](https://arxiv.org/html/2610.05589v1): exact CSS classical reduction and synchronous/Floquet results; asynchronous gap distinguished.
- Hartarsky-Toninelli, [Kinetically constrained models out of equilibrium](https://www.normalesup.org/~hartarsky/files/research/publi/KCM-CP.pdf), manuscript dated 11 March 2024, Section 9, Corollary 9.5: exponential tails for fixed-k connected spacetime zero components of an attractive eroder with sufficiently rare iid deaths. The proof uses Toom contours and their sink/size/count bounds.
- Liggett-Schonmann-Stacey (1997), Domination by product measures: infinite-volume finite-dependence domination. The current reconstruction uses the sufficient replacement lemma in REPLACEMENT_LEMMA.md.
