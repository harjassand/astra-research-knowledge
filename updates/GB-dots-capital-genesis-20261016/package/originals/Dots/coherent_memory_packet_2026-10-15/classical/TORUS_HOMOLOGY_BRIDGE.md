# Stopped torus replay and accumulated-homology bridge

Pin: 3e8a972f2924272e1a89859d2f556b5b1f91d501.

## Outcome and exact scope

The deterministic global bridge reconstructs: absence of a macroscopic coarse zero component over all relevant layers forces every instantaneous syndrome component to stay small, and then a fixed component-local decoder preserves the homology of the entire accumulated error/correction chain. Neither the accumulated chain's support nor its age needs to remain small. The finite-torus probability adapter uses a deterministic prospective-anchor patch, not an adaptively selected patch or periodic iid extension.

The proof below is conditional on the already specified envelope domination, uniform primitive forcing, local fresh flags, and an infinite-volume anchored spacetime cluster tail. It does not independently establish the imported cluster tail, the bad-flag probability bound, or the quantum-to-Pauli/bath transfer. No external scientific validation or physical conclusion is claimed.

## Source inspected

Sources: the canonical THEOREM_AND_PROOF.md and these source files, all under updates/FZ-positive-memory-genesis-20261016/package/derived/located_prior_capital/research/2026-10-15-autonomous-frontier-v2/:

- lead/STOPPED_TORUS_REPLAY.md
- sweep/HOMOLOGY_AND_SLAB_TRANSFER.md
- lead/READOUT_CONSTRUCTION.md
- sweep/MONOTONE_ENVELOPE.md

Source verdicts and prior audit agreement are not premises. This reconstruction uses the explicit definitions, local maps and chain operations.

## 1. Replay contract

Let the healthy-bit process on (Z/MZ)^4 obey theta(z,n+1)=(1-B(z,n)) phi(theta_n shifted by z), starting from theta_0=1. The rule is a finite monotone DNF OR_j AND_(a in A_j). Each B(z,n) is the same fixed measurable function of independent primitive packets within coarse spatial infinity radius g=R+3 in its slab, both on the torus and on the infinite lattice. Copies used in different slabs have the required product law.

Use Euclidean spacetime distance with shortest periodic spatial differences, and k=4R+4. Every parent offset (a,-1) has Euclidean length at most sqrt(4R^2+1)<k. Put ell=M/128, and require ell+k+g+2<M/4, together with the size inequalities below. Assume the infinite cold native process has anchored k-zero-component diameter tail f(u), uniformly in the deterministic anchor. This is the exact probabilistic input to the replay adapter.

## 2. First insertion localizes a complete witness

Reveal zero vertices layer by layer and in a fixed spatial order within each layer. The CA outputs were determined from the preceding layer before this reveal order is applied. Stop at the first inserted zero p=(x,n) producing a k-connected component C of diameter at least ell.

Every component before insertion had diameter below ell. Each old component merged into C contains a vertex within k of p; hence all of it is within ell+k of p. This remains true when arbitrarily many old components merge. Thus C lies in that spacetime ball. The triangle inequality and diam(C)>=ell give some point of C at distance at least ell/2 from p.

For any node (y,t) of C with B(y,t-1)=0, the vanishing DNF requires at least one zero parent from every forcing set A_j. Every such chosen parent lies in the fully revealed older layer and is k-near the child, so it belongs to the same C. Recursion decreases time; since theta_0=1, it can terminate only at nodes forced by B=1. Partial revelation of the current layer does not omit any parent. This closes the necessary zero ancestry, not the full backward light cone.

## 3. Deterministic-anchor copying preserves the law

Fix a prospective p=(x,n) before seeing the random primitives. Copy every primitive packet in the deterministic spatial infinity patch of radius ell+k+g+2 about x, for slabs 0,...,n-1, to its infinite-lattice lift; extend outside with independent ordinary packets.

The patch injects into the torus because its radius is below M/4. Consequently copied packets are distinct original independent variables. The extended infinite field has its ordinary law. The construction is not conditioned on p actually being the first-crossing anchor.

Consider the local witness event that there exists a finite C in the inner patch, containing p, k-connected and reaching distance ell/2 from p, such that every node is either forced by its local flag or has a parent in C from every DNF term. The actual first-crossing event at p implies this witness event. All needed flags use packet guards inside the outer copied patch and hence agree with their infinite versions.

Induction in the layer number forces every lifted witness node to be zero in the infinite cold process. Extra exterior zeros can only help. The whole inner patch has coordinate diameter below M/2, so the lifted displacements preserve every relevant torus distance and k-edge. Thus its infinite zero component at p has diameter at least ell/2. Therefore

P(first crossing occurs at fixed p) <= P(local witness at p) <= f(ell/2).

The first event itself need not be locally measurable; its inclusion in the explicitly local witness event is sufficient. Independent extensions for different prospective anchors need not be mutually compatible. Union bounding their separate probabilities gives

P(any coarse component reaches diameter ell through layer N) <= N M^4 f(ell/2).

No stationary finite-torus estimate, random-region copying or independence of periodically repeated packets is used.

## 4. Whole-slab cover really includes transient syndromes

Let S_n be the coarse cells containing infection at any time in the closed slab [nDelta,(n+1)Delta]. The previously verified structural dependency bound gives

S_n subset N_R({theta_n=0}) union {theta_(n+1)=0}.

If B(z,n)=1 the next-layer point (z,n+1) is zero regardless of whether the actual infection cancels before that sample. If B(z,n)=0, an occupied target must trace through the finite all-zero-preserving computation tree to an initially occupied vertex inside radius R: no guarded birth or length-m exterior path is available. Its initial cell has zeta=0 and hence theta=0. This argument applies to any slab time and pre-jump limit, not just the endpoint.

Choose one zero representative q_z for each z in S_n: either (w,n) with wrapped infinity distance <=R, or (z,n+1). No predictability assumption is needed; this is a deterministic event inclusion. Adjacent fine vertices have coarse cell separation at most one. Their representatives therefore have spacetime distance at most sqrt(4(2R+1)^2+1)<k. A connected instantaneous syndrome component, whose vertices are in the infection envelope, maps into one connected coarse zero component.

For fine vertices x in C_z and y in C_w,

d_L,infinity(x,y) <= b d_M,infinity(z,w)+(b-1).

This follows by choosing a shortest wrapped coarse displacement in each coordinate and allowing the within-cell offsets. The triangle inequality for representative shifts then shows that fine syndrome diameter at least L/32 implies representative spatial diameter greater than or equal to M/32-1-2R. Require

M/32-1-2R > ell=M/128.

Hence absence of coarse components of diameter ell keeps all fine instantaneous syndrome components below r=L/32 at every covered time. At n=0 no representative can be an initial zero, since theta_0=1; any infection must be covered by a bad flag and its layer-one representative. For coverage through T, N=ceil(T/Delta)+1 safely includes the next-layer representatives even at an exact slab boundary. Poisson marks at deterministic boundaries are a common null event, and the fixed half-open convention removes ambiguity.

## 5. Short lifts and a fixed component-local decoder

For a vertex-connected syndrome component with ambient torus infinity diameter below rho=L/8, choose an anchor and lift every vertex by its unique short displacement from it. Lifted coordinate differences lie below 2rho<L/2, so torus adjacent vertices lift to actual unit lattice edges, not long wrapped edges. Its cycle lifts consistently. Changing the anchor changes this lift only by a global period translation. In particular the projected coordinate hull is independent of that choice.

Each component is individually a 1-cycle because boundary cancellation cannot occur between disjoint vertex components. Its lifted coordinate hull is a contractible cubical box. Fill it by the source's fixed-order axial prism contraction: successive coordinate projections obey boundary P_i + P_i boundary = id + pi_i; summing the prisms makes boundaries telescope to the cycle. The filling stays inside the hull. Apply the same rule independently to every small component. Identical components receive identical fillings regardless of other components or error history.

Let D(s) be the sum of those fillings when all components have diameter<rho, and a fixed global filling for other boundary syndromes; D(0)=0. The fallback is not invoked in the transition below.

## 6. Every small-component local transition changes only a boundary

Suppose all pre-event components of s have diameter<r=L/32. A physical event contributes a 2-chain F supported in one unit coordinate cube U, covering both a single face fault and the specified two-face sweep. Put s'=s+boundary F.

Every old component that can change meets vertices of boundary F. Any old component disjoint from these vertices is untouched and cannot be joined by a new boundary edge. Its component and fixed filling therefore cancel identically between D(s) and D(s'). Disappearing components, newly created components, splitting and merging are all included among the remaining affected pieces.

Choose a lift of U. Every vertex of an affected old component is within wrapped distance<r of some contact vertex in U. Lift it into the common box U+[-r,r]^4. That lift is unique: this box has width 2r+1<L/2, so two period-separated lifts cannot both occur there. Edges lift as actual unit edges. Every new affected component uses only these old edges and the changed local edges, and therefore lies in this same box B.

All new affected components have diameter at most 2r+1<rho when L>16, since 2r+1=L/16+1 and rho=L/8. This explicit condition is included in the source's sufficiently-large-size regime; unaffected components remain below r. Thus D(s') also uses only small-component fillings. Its component lifts agree, up to period translation, with the common B lift; all their coordinate hulls and all affected old/new fillings stay in B. F does too.

The uncancelled chain K=F+D(s)+D(s') is therefore supported in B, and boundary K=boundary F+s+s'=0. A closed 2-chain in this contractible full cubical box is a boundary of a 3-chain. Its homology class on the torus is zero. If boundary F=0, the syndromes and decoders coincide and F itself is already a boundary in its unit box.

## 7. Historical accumulation and the conditional classical bound

Let E_t be the sum modulo two of every physical fault and correction face through t, including faces whose syndrome has since disappeared. Then s_t=boundary E_t and the decoded class is H_t=[E_t+D(s_t)]. Exact code initialization gives E_0=0 and H_0=0.

A finite torus has finitely many primitive events in every bounded time interval almost surely. At each local event while the pre-event syndrome components are small, Step 6 gives H_after+H_before=[K]=0. Induction over the entire history preserves H_t=0. A large accumulated membrane cannot silently acquire a nontrivial logical class through a succession of these small-component transitions. A nontrivial logical membrane with a tiny present boundary is possible as a static chain, but cannot be reached from E_0=0 without leaving this regime.

Combining Steps 2-7 gives the conditional classical implication

P(any decoded homology change by T) <= N M^4 f(M/256),
N=ceil(T/Delta)+1,

for one sector. If f(u)<=exp(-a(u+1)) with a>0 fixed, this has the required polynomial-in-volume, linear-in-time prefactor and exponential-in-M suppression. Cross-sector dependence can be handled by a union bound. This is a global classical bridge conditional on the stated tail and primitive assumptions; it is not by itself a quantum diamond-norm theorem or a physical-memory validation.

## Remaining assumptions

Separate internal proof-checkers independently attacked the replay and local-homology arguments. Replay checking confirmed fixed-anchor law preservation, ancestral closure in older layers and lift geometry; local-homology checking confirmed the common box and cancellation, with the explicit L>16 caveat recorded above. This is corroborating internal reconstruction, not independent external scientific review. For an actual anchored diameter tail the replay preserves the full witness diameter and permits the stronger f(ell); the displayed f(ell/2) is intentionally conservative and also covers a radius-tail convention. A tail for only one time anchor or an unrelated initial law would not suffice.

The infinite-volume eroder cluster tail, its constants and version; quantitative marginal bounds for the literal primitive flags; exact syndrome-to-envelope inclusion; the input-independent quantum Pauli-trajectory reduction; and the stronger arbitrary-channel/persistent-bath interface remain distinct requirements. The argument also requires exact initial code state, a fixed ideal component-local decoder, bounded local event support, and sufficiently large compatible sizes L=bM. No counterexample under the literal deterministic bridge hypotheses was found.


