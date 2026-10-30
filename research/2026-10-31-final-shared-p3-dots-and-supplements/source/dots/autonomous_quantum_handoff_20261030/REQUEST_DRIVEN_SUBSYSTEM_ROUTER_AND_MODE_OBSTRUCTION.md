# An actual request-driven subsystem router, and its persistent-mode obstruction
2026-10-30. New construction/negative result. No change to accepted continuous memory/recipient sources. This is on-chip quantum routing, NOT LOCC or arbitrary logical computation.

## 1. Why this is the stronger immediate comparator

The earlier fixed finite-group frame theorem protected several already encoded blocks under externally supplied absolute targets. For a bank handoff one needs only ONE protected factor and an arbitrary uninitialized spare, not a second encoded block, an encoded Bell resource, or a prepared gate state. A fixed local SWAP frame gives a moving SUBSYSTEM code through all partial routes. It also permits a real finite three-state actuator and phase-resolved vacant-bank resets. The nontrivial receiving question is autonomy/persistent mode and consumer causal order, not whether a coordinate change exists.

An irreversible partial LOCC teleportation route is substantially harder. Once only some physical columns are teleported, the natural code stabilizers generally straddle old Q and remote B. For example, the repetition-code parity becomes Z_(Q,remaining) Z_(B,transferred). Measuring either factor locally reveals logical information; measuring their product nondestructively is an additional nonlocal quantum operation unless further entanglement-assisted machinery is paid. This is not a no-go theorem for all resource-assisted protocols, but it prevents treating an arbitrary partially teleported state as an ordinary zero-code B memory or assuming its mixed stabilizer checks are free LOCC. Existing raw signed-gauge complications also remain. The explicit on-chip quantum link avoids this missing operation at a clearly different resource cost.

Error-transparent/moving-code control already exists conceptually. The primary-source comparison in `reusable_frame_primary_comparison_20261030` explicitly records that earlier ETH constructions transport code/error sectors, and that a finite uniform gate history can be compressed classically. No novelty, universal gate set or computational speedup is claimed here. The earned addition sought is an autonomous local, fault-accounted physical I/O contract with no controller drain or initialized spare.

## 2. One protected code and an uninitialized spare

For each resource column i supply physical factors Q_i,B_i of the same finite dimension and one clock with labels 0,e,1. The bank B can be in an arbitrary fixed state, entangled with retained auxiliaries/bath; it is not an encoded or pure resource. Initially the protected unknown logical input is encoded on Q, native controllers are ready, and routing clocks are 0. Logical input may be entangled with its reference, but the initial spare/apparatus is fixed independently of it, as in the memory theorem.

Let S_i be physical SWAP(Q_i,B_i). Define

    U_0=I, U_e=U_1=S_i,
    G_i=sum_(c=0,e,1) U_c tensor |c><c|,
    G=product_i G_i.

The moving code projector is exactly

    P_move=G(P_code,Q tensor I_spare tensor I_clock)G^*.

It is a subsystem code even for coherent clock labels. On a fixed label string, each protected physical qudit lies in Q_i for c_i=0 and B_i for c_i=e,1. A code-check factor sigma_Q,i becomes P_0 sigma_Q,i+(P_e+P_1)sigma_B,i. Products remain local on the original bounded-size resource neighborhoods, now paired cells.

Conjugate the ACTUAL native memory generator on canonical Q by this fixed G, leaving the canonical spare alone. A native hub/resource Hamiltonian stays two-site: hub plus one paired Q/B/clock resource cell. Hub resets and actual monitors retain their allowed local support. The enlarged cell dimension is a fixed factor, not growing with N or command history. All actual perturbations, including on the routing clock and spare, retain bounded-body joint norm under the onsite G.

## 3. Actual time-independent request actuator

Let a_i be a local physical request register. The following is a fixed, request-controlled Hamiltonian, not an external switching waveform:

    H_i=Omega P_(a_i=1) tensor
             [S_i tensor |e><0|+S_i tensor |0><e|],
    J_done,i=sqrt(kappa) I_(Q_i B_i) tensor |1><e|.

The input register and routing clock may be grouped in that resource cell or connected by a declared local classical input coupler. Under G,

    G^* H_i G=I_(Q_i B_i) tensor Omega P_(a_i=1)(|e><0|+h.c.),
    G^* J_done,i G=I_(Q_i B_i) tensor sqrt(kappa)|1><e|.

Thus the physical H really moves the unknown state by SWAP, while the actual resolved terminal is CLOCK-ONLY because e and 1 have the same frame. DONE=1 is reached nominally only through this terminal. Absent perturbations, it is absorbing. Turning the request off during a coherent 0/e excursion may leave a partial route, but never damages the canonical code: the e part can retire and the 0 part can wait indefinitely. Reassertion resumes. Premature or repeated requests alter physical location, not the logical instruction.

Request generation/truth is NOT assumed correct. Arbitrary nominal controller operations on request/spare factors, with the declared frame-covariant actuation, act as canonical DATA identity. Consequently the SAME native memory potential and logical module remain valid through arbitrary asynchronous/coherent request histories, under the same bounded local perturbations. This protects quantum waiting; it does not prove the controller intended a particular circuit stage to execute.

## 4. Vacant-bank reset is safe even on coherent phases

For each clock c and spare basis b, define a SEPARATE physical onsite jump

    K_(c,b)=sqrt(mu) G_i[ I_Q tensor |0><b|_B tensor |c><c| ]G_i^*.

At c=0 this resets physical B. At c=e or 1 it resets physical Q. Every jump separately satisfies

    G_i^* K_(c,b) G_i=I_Q tensor |0><b|_B tensor sqrt(mu)|c><c|.

It can dephase the program clock, but it NEVER acts on the canonical protected factor. This remains exact for a joint Q/spare/clock/reference state with coherences. The complete source effects sum to mu I; all losses are included. No coherent merging of source-clock labels is needed, and no arbitrary physical DATA reset is disguised as an auxiliary eraser.

On the physical DONE sector, every further CPTP operation on the old Q bank alone is an operation on canonical spare. It cannot alter the later protected subsystem/reference marginal. This is a genuine per-column consumed-source firewall, as long as DONE remains the actual routing phase. An old module acting also on unfinished columns, or changing routing labels, is not covered by that statement.

Phase-resolved resets add real clock dephasing. They must be included in the finite service calculation rather than dropped as harmless for timing.

## 5. Actual finite service, with dephasing retained

On an interval where the requested level is enabled, the 0/e block has H=Omega X, terminal e->1 rate kappa, and dephasing rate mu from section 4. Put B_clk=I-|1><1| and extend by zero on 1 the positive matrix

    R=[[2/kappa+(kappa+2mu)/(4Omega^2), -i/(2Omega)],
       [i/(2Omega),                         2/kappa]].

The COMPLETE actual adjoint satisfies L_clk^*R=-B_clk. Let Rmax/min be its two positive eigenvalues. Then A=R/Rmax obeys a B_clk<=A<=B_clk and L^*A<=-rA with a=Rmin/Rmax, r=1/Rmax. This includes arbitrary spare states and common-bath correlations in the nominal clock marginal. It is not an atomic rate approximation or an instantaneous SWAP.

Across independent resource-cell nominal clock channels, the standard product hierarchy gives an exponentially small unfinished fraction after a fixed sufficiently long enabled dwell, under bounded-body continuous perturbations and a legitimate held-target/input model. A finite noisy request-delivery/enable interval can instead be included in a finite forward support expansion; an unbounded unproved delivery time cannot.

This service statement does NOT supply a reliable persistent request field or a global block-DONE detector. A local DONE state says that THIS column's canonical protected factor is on B. It does not assert that most other columns have completed.

## 6. Why a pulse-triggered finite clock is NOT a persistent recipient

Here is a decisive allowed-noise counterexample to the naive autonomy upgrade. Suppose the request pulse has ended; its local stored state is now inactive, and the router is in DONE=1. At rate eta let one bounded onsite noise channel reset the ENTIRE finite request/router state to the initial inactive/0 state. This channel is allowed by the fixed-body joint cb budget (up to a fixed rate normalization). It need not touch DATA.

Once reset, that column has no enabled forward drive and no path back to DONE. Its mode defect is permanent. For independent such admissible reset noise, the expected fraction of unarmed columns at time t is exactly

    p_lost(t)=1-exp(-eta t).

Thus after time O(1/eta) a macroscopic fraction is no longer in the B frame. The physical vacant-bank resets can then clear B at those columns. The covariant native memory can still protect the canonical logical state, redistributing it into Q, but the FIXED-bank B readiness premise fails. An exponentially long ordinary B-output guarantee cannot be inferred from canonical quantum protection.

Adding finitely many unprotected local mode bits does not repair this under the admitted noise model: one fixed-body reset of the entire grouped cell can erase them together. Calling DONE irreversible only describes its NOMINAL transition graph, not robustness to local replacement noise. A hardwired first-request latch is not an immutable classical fact.

Actual repairs require an additional mechanism:
- a persistent refreshed target source, with its delivery/protection proved;
- a distributed protected mode/epoch encoding with an actual causal interface;
- or an unconditional B attractor, which permits pre-routing and therefore is not strict no-transfer-before-request semantics.

The last option is quantum-safe for already-present encoded Q, but for a newly arriving circuit input the producer must write the covariantly selected port. Merely pre-routing blanks and later writing bare Q loses the input. None of these repairs is silently supplied here.

## 7. What can feed an asynchronous compiler now

The exact local instrument is useful: unknown encoded Q can remain protected while its columns move asynchronously into arbitrary spare banks; actual same-frame DONE resets and vacant-bank resets create no logical seam; no all-controller-idle barrier is required. Its grouped two-site/onsite-reset structure remains compatible with the native cavity hardware class.

The companion `ACTUAL_BUSY_HORIZON_AND_JOINT_CUT.md` supplies a candidate horizon/retained-controller-instrument comparison, avoiding conditioning a pointwise live-BUSY tail on a correlated trigger. It does not repair the lost-mode counterexample or make a request truthful. A fixed ordinary B recovery additionally needs a demonstrated small non-B fraction at the actual access instrument; a general consumer needs a valid logical causal order and a fault-tolerant gate/interface. These are different obligations.

A supposedly complete autonomous handoff that assumes an immutable DONE, a hidden global all-ready test, a prepared gate state, or an encoded-input producer that magically follows a changed port has supplied the hard operation as a premise. This note deliberately stops before that inference. Existing continuous port/memory theorems and the broader asynchronous-QCA work remain separate.
