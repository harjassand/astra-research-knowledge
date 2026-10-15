# Independent stopped-replay and accumulated-homology audit

Date: 16 October 2026, Australia/Brisbane. Role: initial Sol 4, `replay`.
No other agents, chats, or delegated work were used.

**Verdict: scoped pass.** I find no invalid implication in the first-insertion
finite-torus replay, the whole-slab geometric transfer, or the component-local
decoder argument under the explicit inputs below. I give independent proofs,
including the cases of unrevealed same-layer zeros, seam crossings, component
mergers/splits, vanished syndromes, and nontrivial accumulated closed history.
The exact finite checks all pass. This does not certify the entire memory
theorem, historical novelty, or physical implementation.

There is no substantive repair to the theorem required by this audit. The
metric and locality conventions are essential: use Euclidean coarse spacetime
distance, ambient torus infinity distance for fine component diameters, a
fixed infinity-norm primitive patch, and a component-local small filling. An
arbitrary adaptive primitive patch or an arbitrary decoder with the same
syndrome boundary would not support these proofs.

## 1. Inputs and independence of the audit

I read in full:

- `THEOREM_AND_PROOF.md`;
- `lead/STOPPED_TORUS_REPLAY.md`;
- `lead/SLICE_TOKEN_INVARIANT.md`;
- `lead/LOCAL_DECODER_HAZARD.md`;
- `lead/READOUT_CONSTRUCTION.md`;
- `explanation/BETWEEN_SAMPLE_HALO_PROOF.md`;
- `sweep/HOMOLOGY_AND_SLAB_TRANSFER.md`;
- `spacetime/FINITE_TORUS_LIFTING_AUDIT.md`.

I also read `sweep/MONOTONE_ENVELOPE.md`, the winding-ribbon countermodel,
`explanation/PLANE_CHARGES_AND_RAW_OBSTRUCTION.md`,
`spacetime/UNPRUNED_WITNESS_ENTROPY_COUNTERMODEL.md`, and the saved coarsening
and decoder compatibility notes. All these paths are relative to
`research/2026-10-15-autonomous-frontier-v2/`. `INPUTS.json` records the exact
hashes examined. Prior auditors' verdicts and status labels are not premises
in the derivations below.

The one external cluster result used is the statement of
[Hartarsky--Toninelli, arXiv:2212.08437v2, Corollary 9.5](https://arxiv.org/html/2212.08437v2#S9.SS2).
I checked its CA definition, its definition of k-connectivity, and the
corollary against the primary HTML. It bounds the diameter of the maximal
fixed-k connected zero component in the stationary upper-invariant
trajectory of an attractive eroder with sufficiently small iid deaths.
The infinite-volume iid-death domination of a fixed-guard B field is an
explicit input here; this report does not independently prove the LSS theorem.

## 2. Literal contract for the probability bridge

Let `T_M=(Z/MZ)^4`, and let

    phi(x) = OR_j AND_(a in A_j) x_a

be a finite monotone rule on healthy bits, with nonempty finite A_j. Start
`theta(x,0)=1` and set

    theta(x,n+1) = (1-B(x,n)) phi(theta(x+.,n)).

Each B is the same fixed function of independent spatial primitive packets in
an infinity-norm guard of radius g, during slab n. Distinct slabs use disjoint
primitive increments. The function does not inspect the realized theta
history, the first-escape anchor, an adaptively selected component, or the
exterior state. Its infinite-lattice version is defined by the same local
function and primitive packet laws.

In the sweep application g is bounded by R+3 coarse cells. A packet can contain
all fine vertex clocks and all oriented face-noise clocks with bases in that
coarse cell. Packets are independent because these are independent primitive
streams indexed by their bases, even though the effects of face events and
the guards of different B flags overlap.

Use quotient Euclidean distance on `T_M x Z` and join zero vertices at
distance at most k. Require

    k >= max_(a in union A_j) sqrt(||a||_2^2+1),
    ell+k+g+2 < M/4.                                  (2.1)

The second inequality is a deliberately safe local-lift margin. For the
canonical choices `k=4R+4`, `ell=M/128`, `g<=R+3`, it holds for sufficiently
large M, independently of the storage horizon. No LSS assertion on the torus
is an input.

## 3. Independent proof of first-insertion localization and zero closure

Fix a finite horizon N. Compute the synchronous CA layer from the complete
preceding layer. Reveal its zero vertices in a fixed spatial order, complete
that layer, and continue chronologically. This is an ordering of already
determined outputs. It is not a change to the update dynamics.

Suppose the full revealed history first acquires a k-connected component of
diameter at least ell when p=(x,n) is inserted. Let C be its component just
after that insertion. Every preceding revealed component C_i has diameter
strictly below ell. A C_i joined to p contains q_i with `d(q_i,p)<=k`.
Consequently every q in it satisfies

    d(q,p) <= d(q,q_i)+d(q_i,p) < ell+k.

Only such components are joined by insertion of a single vertex. Therefore

    C subset B_(ell+k)(p).                             (3.1)

This holds when p merges arbitrarily many old components. It also holds if
some of their vertices have the same time n as p. It uses only their
pre-insertion diameter, not a bound on the number of components or their
intrinsic graph lengths.

Now take q=(y,t) in C. If it is a nonfault zero, the DNF conjunction indexed
by each j must fail. Choose a zero parent `(y+a_j,t-1)` from each A_j. That
parent has already been revealed: its layer is strictly older than t, and
all earlier layers were completed before layer t was started. It is k-near
q by (2.1), so it belongs to C. The same reasoning actually places every
zero-valued input parent of q in C, but one per conjunction suffices.

Recursion remains in C and strictly decreases time. It cannot terminate at a
zero in layer zero because layer zero is all one. Hence a finite certificate
terminates in B-forced nodes. There is no unsupported backwards cycle.

**Unrevealed parents attack.** Unrevealed zeros at time n can be outside C.
They cannot be parents of any already inserted output, because the CA reads
only the preceding layer. Zeros in older layers are all revealed. Thus this
attack does not invalidate closure. Replacing the synchronous block CA by a
rule that reads partially updated outputs would invalidate this particular
proof, but that replacement is not in the canonical theorem.

**Wrapped-component attack.** A C satisfying (3.1) has spatial coordinate
displacements less than ell+k from x. Under (2.1) its full spatial projection
lies in a patch of coordinate width below M/2. Edges and causal offsets in
this patch cannot acquire an unnoticed multiple of M. A component cannot
wind before the stipulated first escape without already violating this
localization. Large wrapped components at later times are permitted.

## 4. Fixed-anchor witness law, rather than a conditional law

Fix one candidate p=(x,n), before sampling any primitives. Take the
deterministic infinity-norm patch about x of radius `ell+k+g+2`, with the
natural local lift, and all primitive packets there in slabs 0 through n-1.
The patch projects injectively to the torus. Copy these packets to distinct
infinite-lattice locations and extend outside with fresh independent packets
having the original law. The resulting entire infinite primitive field has
its ordinary product law, unconditionally.

Consider the event W_p that there exists a finite vertex set W satisfying:

1. W is contained in the inner radius-(ell+k) spatial patch, in layers 1..n,
   contains p, and is k-connected;
2. its lifted diameter is at least ell, or conservatively it has a vertex at
   distance at least ell/2 from p;
3. every q=(y,t) in W is B-forced, or has in W a parent from every A_j.

Every B used in condition 3 has its full primitive guard in the copied patch.
Thus W_p is a local measurable event of the fixed packets. It does not ask
that W be the realized torus component, or that outside vertices be healthy.
The first-crossing event at p implies W_p by Section 3.

Run infinite theta from all ones with the copied-and-extended primitives.
Induct on t. A forced witness node is zero. At a nonforced witness node,
every DNF conjunction has its selected zero parent already replayed, so its
output is zero. Additional outside zeros cannot defeat a zero DNF output.
Therefore the whole W is contained in an infinite zero component containing
the fixed lift of p.

The lift preserves k-edges. Indeed, each coordinate difference of two lifted
vertices has magnitude less than `2(ell+k)<M/2`, so the lifted difference is
the periodic shortest difference. The same applies to a causal offset
a with `||a||_infinity<=k`. Distinct periodic images are not identified in
the infinite field. The lifted diameter cannot be smaller than the torus
diameter; with the stated margin they agree for pairs in C.

It follows that

    P(first crossing at p) <= P(W_p)
        <= P(infinite cold zero component at p reaches ell/2).   (4.1)

This inequality concerns unconditioned probabilities. A conditional
distribution given “p is the first crossing anchor” is unnecessary and would
generally not be product. Each of the `N M^4` candidate anchors may have its
own infinite extension. A simultaneous extension compatible with all anchors
is also unnecessary.

For contrast, two independent Bernoulli(1/2) variables and the adaptive choice
“take the first coordinate equal to one, otherwise the first coordinate” give
a selected one with probability 3/4. Copying a favorable adaptive primitive
patch would therefore bias its law. The canonical fixed-anchor union avoids
exactly that error.

## 5. Infinite comparison and the finite-horizon bound

Suppose each infinite B slab can be coupled below an iid Bernoulli(p) death
field, with p sufficiently small for the already fixed phi and k. Since the
whole B fields in different slabs are independent, independent copies of
this coupling make the death field iid in space and time. More deaths make
healthy bits smaller, so the iid-death cold CA has every replayed zero.

Independently sample its upper-invariant initial state and use the same
future iid deaths. The all-one initial state is pointwise above it; hence
the cold zero set in nonnegative times is contained in that stationary zero
set. Restricting a stationary trajectory to nonnegative times can only
decrease its connected components. The imported HT bound consequently gives

    P(W_p) <= p^(c(ell/2+1)),

uniformly in the candidate's deterministic time n. A union bound over the
finite set of candidate anchors yields

    P(any k-zero component has diameter >=ell through N)
      <= N M^4 p^(c(ell/2+1)).                         (5.1)

For ell=M/128 and fixed sufficiently small p, this is
`C N M^4 exp(-c' M)`. The proof never multiplies probabilities along an
adaptive actual-support genealogy and never reuses a primitive arrival as
an independent error. It supplies no bound uniform over all times on a fixed
finite torus. Eventual absorption into an all-zero state is consistent with
(5.1), whose right-hand side grows with N.

## 6. Whole-slab transfer, independently reconstructed

Let a=n Delta and `m=floor(Rb/2)`. For an envelope output at w, its possible
clock centers and old inputs are:

    center w:            inputs w, w-e_1, ..., w-e_4;
    center w-e_i-e_j:     inputs w, w-e_i, w-e_j, w-e_i-e_j.

There are exactly at most `5+6*4=29` event/input choices per step, so 35 is a
safe overcount. Both the input and center are at infinity distance at most
one from w. A clock has several outputs, but all are functions of pre-event
bits. A backward read step therefore goes to a strictly earlier time; a
single arrival cannot be traversed twice at the same time.

Define fast-bad by existence of any structurally admissible ordered m-event
chain from a target vertex, with all its times inside the entire slab. It is
not merely an ancestry event observed at the endpoint. Its first m centers
lie within m fine units of the target cell. Include also every birth meeting
the fixed guard. These are functions of fixed raw increments, independent of
the actual input state.

If eta_x(u)=1 for some u in the slab and the cell's B flag is zero, trace one
occupied old input backward through the most recent event updating the
current coordinate. An occupied own-site output has occupied old self; an
occupied upper-corner output has either occupied old self or its three
occupied sources. Each chosen step is a legal structural step. A birth before
m steps is in the protected guard and contradicts B=0. Reaching m clock steps
contradicts fast-bad absence. Thus the trace reaches a with an occupied
initial site within fewer than m fine units. This also treats a site that
simply waits through the slab with few or no clocks.

Its initial cell is within coarse infinity distance R of the target, using
the canonical conservative guard. Since zeta>=theta, this initial infected
cell is a theta zero at layer n. If B=1 instead, the target is a theta zero
at n+1 by construction. Therefore every occupied fine vertex at any time in
the slab has a representative zero at n or n+1 within coarse distance R.

Adjacent fine vertices have cell indices at infinity distance at most one.
Their representatives differ spatially by at most 2R+1 per coordinate and
temporally by at most one, so their Euclidean spacetime distance is at most

    sqrt(4(2R+1)^2+1) < 4R+4 = k.                     (6.1)

Consequently a connected fine syndrome component maps into one k-connected
coarse zero component. If fine endpoints have periodic infinity distance D,
their cell indices have periodic distance at least D/b-1. Moving both to
representatives loses at most another 2R, giving coarse diameter at least

    D/b - 1 - 2R.                                    (6.2)

For D=L/32 this exceeds M/128 once
`M/32-1-2R>M/128`, equivalently `M>(128/3)(2R+1)`.
The canonical large-M convention more than suffices. This is a pathwise
statement throughout the slab, not a sample-time assertion.

**Transient defect attack.** A face can be toggled twice inside a slab, with
empty syndrome at both sample times and nonempty syndrome between the two
faults. The first birth already puts B=1 in every relevant local target guard;
theta at n+1 is zero even if the actual endpoint is healthy. Such histories
are therefore not lost. The exact checker realizes this history across a
periodic seam and also clears the envelope before the endpoint.

The future proxy at n+1 is legitimate in a finite-horizon event inclusion.
It is not a predictable process for a compensator. No compensator is needed
when (5.1) already bounds escape over the entire physical history. For an
arbitrary T include the full final slab and enough comparison layers, as in
`N=ceil(T/Delta)+1`.

## 7. Repeated clocks and the actual Poisson bound

Fix a structural word of length m, including its specified clock centers.
It may revisit one clock location many times. Count strictly ordered tuples
of distinct arrivals at those centers in a slab of length Delta. The
factorial moment measure of a Poisson process, and independence between
different processes, give

    E[number of such ordered tuples] = (kappa Delta)^m / m!.  (7.1)

For the word using only one clock this is the identity
`E[binomial(N,m)]=(kappa Delta)^m/m!`, with `N~Poisson(kappa Delta)`.
Thus reuse of a clock *stream* is allowed; reuse of one clock *arrival* is
not. Markov and the structural union bound give

    P(fast-bad) <= b^4 (35 kappa Delta)^m/m!.

This bound includes every possible terminal observation time because the
tuple's largest time can be anywhere in the slab. There is no additional
uncountable union. Repeated clock locations do not produce an extra
independence hypothesis.

For slow finalization certificates, the enabling time at a site w depends
only on strict predecessor-site clocks. The envelope is spatially feed-forward:
the clock at w cannot affect any strict predecessor. Its next arrival after
that enabling time is therefore a fresh exponential service. Directed
certificate paths decrease height and do not revisit a site. The claimed
path-wise exponential moments concern these certificate services, not
arbitrarily selected actual correction times. Evaluating success by the
slab endpoint uses only increments up to that endpoint; no future service
is required to decide failure.

Half-open slabs remove the formal issue of a mark being at two endpoints;
fixed deterministic endpoints almost surely contain no Poisson mark anyway.

## 8. Independent local decoder construction and lift lemma

All chains below are over F_2 on the side-L cubical four-torus. Let
`s=partial E`, retaining all physical noise and correction faces in E.
Use vertex-connected components of the syndrome edge support.

Each component is a 1-cycle: a vertex cannot belong to two different vertex
components, so the even incidence condition `partial s=0` holds separately
in each. A component of ambient torus infinity diameter below rho=L/8 lies
within coordinate distance rho of any chosen vertex anchor. Lift each vertex
by its unique short coordinate displacement from that anchor. A lifted
edge cannot have displacement L-1: its endpoints differ by less than
2rho<L/2 in every coordinate. Hence every edge is a genuine unit edge in
the lift. Connectedness makes the lift unique up to a translation by L Z^4.

The full cubical coordinate hull of this lift is a contractible box. Choose
a deterministic filling of the cycle inside this hull. One explicit choice
is axial prism contraction. On cubical chains, projecting coordinate i to
the lower face has a prism homotopy satisfying

    partial P_i + P_i partial = id + pi_i.

Projecting a cycle in each of four coordinates and summing its prisms gives
a filling, since the final projected edge chain is zero. Every written face
lies inside the original hull. A different anchor changes the consistent
lift only by a period translation and leaves the projected hull the same.

Define D as the sum of these fixed component-local fillings whenever all
components have diameter below rho. Set D(0)=0. On other physically attainable
syndromes choose a fixed global filling. Existence of the latter is automatic
for reachable syndromes, since they are boundaries of E. This fallback need
not fill a homologically nontrivial large component individually.

The finite-horizon proof uses only the global-small regime. If one instead
wants a localized hazard statement allowing large components elsewhere,
the fallback must be a function only of the unchanged large residual. An
arbitrary global fallback of the whole syndrome would not support that
stronger localized statement. The canonical first-escape theorem does not
need it.

## 9. Universal transition proof for noise and one/two-face corrections

Set r=L/32. Suppose every pre-event component has ambient infinity diameter
below r. Let F be one physical noise face or one accepted sweep correction.
The latter is one positively based face, or two positively based faces
whose paired directions are disjoint. Every vertex of F lies in the common
unit coordinate cube based at its update vertex. This remains an embedded
unit box when its projection crosses a periodic seam. Null attempts have
F=0.

Let `s'=s+partial F`. Take all old components touching any vertex of F and
the vertices of F itself. Lift the event cube into the universal cover.
Each touched old component lies within coordinate distance less than r of
its contact vertex in that cube. Its consistent lift therefore lies in the
common box

    Q = product_i [v_i-r, v_i+1+r],

of coordinate width at most 2r+1. This width is below rho and below L/2 for
sufficiently large L. All relevant lifts are consistent in Q.

Every altered edge belongs to partial F and has both endpoints in the event
cube. No old component disjoint from that cube can be joined through a new
edge without having touched its endpoint already. Thus all affected new
components are assembled from touched old components and the changed edges,
inside Q. This includes splitting an old component into several new ones,
joining several old components into one, deleting a component completely,
and creating one from the empty syndrome. All new affected components have
diameter at most 2r+1<rho. Unaffected components retain their exact edge sets.

The decoder before and after uses its small-component rule everywhere. The
fillings of identical unaffected components cancel exactly because each
choice depends only on its component. Each affected old/new filling lies in
its own coordinate hull, which is a subbox of Q. Hence

    K = F + D(s) + D(s')

is supported in Q and

    partial K = partial F+s+s' = 0.

The box Q has zero second homology; equivalently its axial chain contraction
fills K by a 3-chain inside Q. Thus K is a stabilizer boundary in the torus:

    [F+D(s)+D(s+partial F)] = 0.                       (9.1)

This proves the required statement for *every* single-face noise event and
every legal one/two-face correction, not just the enumerated test patterns.
It does not depend on the number of earlier events, their clock schedule,
component labels, or the volume of E. A bounded closed F with empty boundary
would also be a boundary in its local cube; that case causes no exception.

The decoded class is

    H(E) = [E+D(partial E)].

Its increment at the event is exactly (9.1). Therefore it is unchanged at
every event while the stipulated precomponent condition holds. A finite
torus has finitely many primitive events on every finite physical time
interval, so induction from E=0 is valid. No historical faces are erased
from E merely because their syndrome cancels.

## 10. Exact pathological topology examples

The checker uses L=128, r=4 and rho=16. Let v have all four coordinates L-1,
so these examples cross torus coordinate seams.

- **Complete disappearance:** E=F=p_01(v). The old four-edge component is
  filled by that same face; after a noise cancellation or accepted correction
  the syndrome is empty. The decoded accumulated class stays zero.
- **Two-face disappearance:** E=p_01(v)+p_23(v). There are four outgoing
  edges and no incoming edge at v, so the prescribed consecutive pairing
  corrects both faces. Its degree-four syndrome component disappears.
  Equation (9.1) still holds.
- **Merge:** E=p_01(v-e_0)+p_01(v+e_0), F=p_01(v). Two vertex-disjoint
  square components become the perimeter of a three-face strip.
- **Split:** reversing that middle face toggle changes the strip's one
  component into two. Both transitions have zero homology increment.
- **A hidden historical membrane:** let T_01 be the complete coordinate
  2-torus at the other two coordinates L-1, and E=T_01+p_01(v). The
  syndrome is only the small four-edge hole boundary. D fills that hole,
  so the decoded accumulated class is already [T_01], not zero. Toggling
  F=p_01(v) makes the syndrome empty but preserves the nontrivial decoded
  class. This is a positive test that history was retained, not discarded.

For a closed 2-chain K the code separately evaluates the six dual-cut
cocycles: for each orientation ij, sum the ij faces with base coordinates
`x_i=x_j=0`, over all transverse coordinates, modulo two. Each cocycle
vanishes on a 3-cube boundary and evaluates to one on the corresponding
coordinate 2-torus. These six values classify H_2 of the four-torus. Thus
the finite checks do not infer homology merely from a decoder's claim that
it filled a cycle. Cube-boundary pattern checks also exercise nonzero
closed differences that must be stabilizer boundaries rather than zero
as chains.

## 11. Known countermodels independently placed at the correct boundary

For the width-one wrapping ribbon

    E=sum_(x mod L) p_01((x,0,0,0)),

the interior vertical edges cancel in partial E and the syndrome is two
straight 0-directed winding loops. At each loop vertex its incoming
0-edge is present, so the no-incoming guard suppresses every correction.
Each loop has ambient diameter floor(L/2), far above r. This exact fixed
syndrome refutes universal torus clearing. It does not refute (9.1) or
first escape from a cold state. The checker reproduces it for L=3..8.

For completeness, restricting errors to one ij plane gives the scalar
face-bit rule at vertex (a,b): no incoming syndrome means

    x(a-1,b)=x(a,b-1)=x(a-1,b-1)=q;

the nonnull correction occurs when x(a,b)=1-q and sets it to q. A wrapping
row together with a wrapping column of occupied faces cannot lose a face,
because each has an occupied west or south predecessor. Its interior can
fill to the entire logical 2-torus under a fair noiseless continuation.
But the initial seed already has a horizontal boundary path visiting all
L coordinate positions, so a component has ambient diameter floor(L/2).
This history lies outside the local-small hypothesis long before the final
hole disappears. The final-hole example in Section 10 confirms that its
last event need not be the event changing the decoded homology.

The quadratic raw-partner closure and cancelling-pair entropy constructions
attack an attempted `C^m` bound on *unpruned actual histories*. Two identical
face faults can cancel as chains while remaining two events in a historical
genealogy; this creates irrelevant witness decorations. The replay proved
here uses the monotone coarse zero component and an imported iid-death
cluster bound. It makes no `C^m` claim about the actual physical genealogy.
The countermodels therefore remain valid and their invalid counting shortcut
is not revived by this audit.

## 12. Exact checks, reproducibility, and remaining scope

Run from the repository root:

    python3 research/2026-10-16-adversarial-quantum-memory/replay/exact_replay_topology_checks.py

The script needs only Python's standard library. It writes `EXACT_CHECKS.json`
and aborts on any failed assertion. There are 13,056 single-face noise checks
and 3,120 accepted sweep checks, including 16 two-face corrections. Among
these are 928 nonzero closed transition differences, each of six faces;
all have zero homology. These counts exclude the additional named fixtures.

The topology part exhausts the 64 common-corner face subsets of a 4D unit
cube, the 512 planar 3-by-3 patterns, and the 64 face subsets of each of
the four 3D unit cube boundaries, at an ordinary location and a seam-crossing
location. It applies each named face noise event and every accepted sweep
attempt at their syndrome vertices. It independently checks the resulting
closed difference and all accumulated decoded homology coefficients.

The replay part exhausts all 4,657 histories with at most two primitive marks
on a 32-site one-dimensional torus over three slabs. Its attractive eroder
is `phi=x_0 OR x_1`, and correlated deaths are the literal fixed-guard rule
`B(x,n)=P(x,n) OR P(x+1,n)`. It finds 416 first escapes, including 39 seam
crossings and 161 cases with unrevealed same-layer zeros. Every stopped
component is checked for ancestor closure and consistent edge lifts and
replayed for both all-zero and all-one exterior primitive extensions. These
small tests challenge the deterministic bridge; they do not instantiate
the enormous fixed R and b of the actual 4D block construction and do not
numerically estimate an asymptotic threshold.

The source-level proof uses `k=4R+4`, not the smaller adjacency of the toy
enumeration. Equation (6.1) verifies the required norm conversion directly.
The whole-slab inclusion and decoder invariance then reduce logical change
to the same finite-horizon coarse escape event without a second time factor.

Still outside this audit: a complete independent proof of the LSS and HT
imports, numerical usable constants, the full quantum generator audit,
historical originality, perturbative robustness, noisy readout, fabrication,
and any costed physical implementation. Nothing in these checks makes those
claims current or established. Under the enumerated local primitive,
infinite comparison, and exact chain-model inputs, the stopped replay and
accumulated-homology endgame need no weakening of the canonical theorem.
