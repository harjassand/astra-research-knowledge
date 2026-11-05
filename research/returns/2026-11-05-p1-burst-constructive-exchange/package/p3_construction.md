# P3 constructive exchange: an immutable-schedule burst compiler

Date: 5 November 2026. Independent P3 construction for the root researcher.

## Status and main result

The decisive semantic ingredient used here is **one normalizing refresh round before the logical update round**. Arbitrary-input normalization and doubled error correction are existing fault-tolerance machinery; the closest published comparison is Balasubramanian–Davydova–Lake, Quantum 10, 2125 (2026), Section 2 and Appendices B/C. It upgrades the familiar five-spatial-copy / three-temporal-pass routine from a theorem for globally nice noise to an arbitrary-fault-field coarse simulation with bounded propagation of bad regions. The proof below is explicit. The finite checker verifies 491,520 active-pass adversarial cases and 640 vote/boundary cases for the single-bit semantic core; it does not implement the complete hierarchy or a physical apparatus.

Together with geometric padding and Poisson localization, the construction supplies the positive theorem for the **strict Pareto** question under P3's stated immutable gate/schedule abstraction. The final version incorporates the independent audit of circuit substitution, prewarming, synchronization and level conversion in `p3_independent_audit.md` and `p3_compiler_lemma.md`. It does not claim the general finite-(d+1)-moment endpoint, autonomous self-fabrication, practical hardware, or new priority over all fault-tolerance literature. Unlike the original P3 recurrence, a concrete semantic gadget and an arbitrary-E projection are supplied.

The source comparison is essential: Gacs's sparse-error correction machinery supplies the five-copy / three-pass idea. His lecture explicitly warns that a global 1-sparse theorem alone is not an arbitrary-error amplifier. The normalization-then-gate routine below addresses that missing interface when the schedule and addressing are immutable. It avoids claiming that the unmodified nice-fault theorem already proves the result.

## 1. Declared local circuit model

Use a finite line of one-bit registers embedded in R^d, with a fixed finite set of nearest-neighbor Boolean gates (COPY, reset, and a universal two-input Boolean basis suffice), bounded degree, fixed microscopic update rate, and fixed information speed. Gate laws and the time-dependent input-independent schedule are supplied as immutable primitives, exactly as allowed in P3's final refinement. Every register, including message, workspace and holding registers, is corruptible.

One may first describe the routine with a fixed number of tracks per line site. Replace tracks by separate neighboring one-bit sites and implement each fixed-size track permutation or Boolean operation by a constant-depth nearest-neighbor circuit. The number of tracks and the conversion factor are constants independent of the geometric padding B and hierarchy level. This is a physical layout change, not an unbounded local alphabet. The recursively compiled object is always a circuit on one-bit sites; it includes every workspace site and is therefore closed under the same substitution.

During this flattening, Info can move only inside its constant-size microcell, and is restored after each simulated multitrack tick. Long routes transport message copies, never the protected Info positions themselves. A raw fault island consequently enlarges by only a fixed spatial/time guard. Increase w and the idle gaps by that guard before choosing B. This prevents a moving track implementation from silently invalidating the five-spaced-copy argument.

All large constants are family constants fixed after d, alpha, accuracy and the gate set are fixed. No gate receives an arbitrarily distant input in one tick. An instruction schedule is charged by its uniform compilation and circuit-size cost; its reliability remains a premise of the model rather than a hardware theorem.

## 2. A concrete local semantic gadget

### 2.1 Five-copy encoding and regular states

A macrocell stores one bit in five Info positions separated along the line by D. Choose D greater than the spatial width w of an allowed fault island. Call a five-bit Info word **regular** if at least four copies agree. Its logical value is their majority. Other registers can be arbitrary at the macrostep boundary.

A nice fault island is an arbitrary set of register corruptions contained in one spatial interval of width at most w and one time interval of width at most w. Its values may be adversarial and may depend on the stored input. The fault island can affect at most one Info position in each input macrocell. It can corrupt every track/register at that physical location.

### 2.2 One three-pass round

Keep Info fixed throughout the round, except for physical faults. For i=1,2,3:

1. Reset the temporary message/work registers by the scheduled local reset gates.
2. Copy each of the five Info values into a separate message lane; transport them by nearest-neighbor COPY/SWAP gates to the computation site. For a fixed-fanin logical gate, do this for each input macrocell in its fixed neighborhood.
3. Decode each input by majority of its five values; apply the specified Boolean gate f.
4. Broadcast the result by local gates to five separated positions in a fresh Hold_i track.

Use idle gaps longer than w between active passes and between successive rounds. Finally set each output Info position to the local majority of its three Hold values. The Hold tracks remain untouched except by physical faults and their prescribed writes. Since the number of inputs, lanes and stages is fixed, a pass requires at most cB local ticks on a macrocell of length B, for a constant c independent of B.

The model does not need protected mutable counters. The known location and time of each gate are supplied by the immutable layout/schedule.

### 2.3 Regular-input correctness of one round

Assume each input Info word is regular, representing its intended bit. Before the new fault there is at most one incorrect replica per input. The fault changes at most one additional Info position per input. Consequently every clean pass sees at most two incorrect copies among five and decodes the intended bit.

The temporal gaps imply that a single island can intersect at most one active pass. It can therefore spoil at most one whole Hold word through computation/transport. It can also alter all retained Hold tracks at the one output position in its spatial interval. At every other output position the other two Hold values are correct, so the final majority is correct. Output Info is regular and represents f of the intended inputs.

This includes persistent damage to Info and workspace: Info damage is bounded spatially; workspace is reset before each pass; globally propagated work damage is confined to one temporal pass.

### 2.4 Why one round is insufficient for arbitrary input

If an incoming five-copy word is not regular, one spatial fault can change its majority between clean temporal passes. The clean passes can then disagree, and the globally spoiled pass can decide a different output at different replica sites. Thus a nice-noise theorem with regular input is not yet an arbitrary-E amplifier. This is the issue the additional normalization handles.

### 2.5 One normalization followed by the logical round

Prepend **one** identity/majority normalizing round, then execute the logical-gate round. Separate all active stages by gaps longer than w. For one island in the whole macrostep:

* If it intersects normalization, the logical round is clean. It sees fixed, possibly arbitrary Info words and computes the same f of their majority-decoded values in every pass. Its output is a perfect repetition word.
* If it intersects the logical round, normalization was clean and produced perfect repetition inputs. The regular-input correctness argument applies.
* If it intersects a gap or final commit, it alters at most one replica per involved input/output block.

The complete macrostep therefore has:

**R — regularization.** Arbitrary incoming Info/work/holding states give regular output Info under a nice macrostep.

**C — semantic correctness.** Regular input Info gives the intended logical output, with regular output Info, under a nice macrostep.

Both properties hold for every Boolean input assignment and arbitrary fault values. Normalize all input macrocells synchronously, then hold their Info fixed throughout the three logical passes. All output commits are synchronized. The earlier two-normalization version is a valid redundant variant; it is preserved in the separate three-round checker. The reduction to one normalization was supplied by the independent P1 audit.

### 2.6 Exact finite check

`p3_gadget_check.py` enumerates all 32 incoming five-bit words, every one of six active-pass positions in the two rounds, each of five spatial replica positions, both new Info values, all eight assignments to retained Holds at that position, and every arbitrary five-bit spoiled Hold word. All 491,520 cases give regular final output; all 184,320 cases with regular input preserve the input value. A further 640 vote/boundary cases pass. This is an exact integer verification of the semantic invariant. It does not verify the complete layout or hierarchy by simulation.

## 3. Arbitrary-E projection: the missing amplifier interface

Let W(i,t) be the fixed spacetime region used by output macrocell i during macrostep t, including its normalized input macrocells, message routes, both rounds and idle gaps. Its spatial width is at most aB and duration at most U, with fixed a and U<=c_0 B before optional padding. Let

    Bad(i,t) = {the faults in W(i,t) cannot be enclosed in one w-by-w island}.

Decode the actual Info at every macro-boundary by majority, obtaining Y_t(i), even when an encoding is irregular. Let I_t(i) flag an irregular Info word.

Property R gives, without any assumption on incoming state,

    I_(t+1)(i) <= 1_Bad(i,t).

Property C gives

    Y_(t+1)(i) = f_(i,t)(Y_t of its input neighbors)

unless Bad(i,t) occurs or an input encoding is irregular. Consequently, for regular initial encoding, the induced coarse fault field is contained in

    E' subset Bad union ForwardNeighbor(Bad).

ForwardNeighbor advances time by one macrostep and expands space only by the fixed input-neighborhood range. This is a deterministic statement for **every** raw fault field E. It is not an argument assuming a globally nice trajectory. A bad region can leave arbitrary encoding, but the next nice macrostep normalizes it; it cannot generate indefinitely propagating unencoded control state.

Since the compiled circuit includes all its workspace sites as ordinary one-bit registers and never uses mutable addresses to choose a gate, this projection can be iterated. At level k, take the actual decoded bit trajectory as the input trajectory to the next projection, and the monotone support envelope E_k as its fault set. Values at E_k are unrestricted. Thus physical faults induce an ordinary adversarial register-error process at each higher scale.

Boundary initialization contributes its explicit set of irregular input cells if any. Commissioning and the level conversions below arrange regular encoded inputs; their failures are included as separate charged events. For input-independent blank workspace, reset/preparation circuits are counted, rather than assuming that arbitrary preexisting values equal zero.

The global rounds are synchronized across all spatial colors: finish one full pass for every color, then take its idle gap, then start the next pass. This ensures a time-bounded island cannot corrupt different numbered passes merely because two neighboring gates were assigned different colors.

All logical output commits are simultaneous. No output Info is overwritten after one color while another color is still reading old Info. Colors schedule transport and computation into separate Hold tracks; final pointwise majority is a global barrier. Normalization commits are likewise synchronized.

Bad windows and their projections are proof objects. The circuit receives no fault flags. Corruption values may be globally correlated and input-dependent; the support envelope depends only on burst geometry and the semantic guarantee holds for every assignment of values.

## 4. Bounded local state and geometry under iteration

The track description is only a finite circuit-design convenience. Flatten it once into a constant-size group of binary sites. A single multitrack tick is a fixed finite collection of local Boolean operations/permutations; a constant coloring and nearest-neighbor swap network executes it in a fixed number of physical ticks. This factor is independent of B and k.

Now apply the gadget compiler to the flattened binary circuit, not to an ever-growing symbol alphabet. Every logical bit site, including every workspace bit of the previous level, is replaced by one length-B binary macrocell. The input circuit's gate set remains the fixed Boolean basis after every substitution. This gives

    L_k = B^k,       tau_k = U^k,

with one-bit local state, fixed range/degree/density and a fixed U/B lower bound determined by the local implementation. Choose integers B,U with U>=c_0 B and define z=log(U)/log(B)>1. For any desired nonempty subinterval of (1,alpha-d), sufficiently large B permits such an integer U with z in that subinterval. Extra time is supplied by scheduled waiting/refresh identities. All waiting registers remain inside the encoded circuit and the fault model.

The footprint needed to determine a level-k induced fault is contained in a spatial interval of width C_x L_k and a time interval of width C_t tau_k. The constants stay bounded: new dependencies add a fixed parent footprint plus a previous-level footprint, producing geometric sums in 1/B and 1/U. Choose w larger than the resulting support constants and choose B larger again. No footprint grows like kL_k.

Precisely, including previous-period/neighbor guards in constants a,b, raw spatial and temporal half-widths satisfy rho_(k+1)<=a L_(k+1)+rho_k and eta_(k+1)<=b tau_(k+1)+eta_k. Hence rho_k/L_k<=a/(1-1/B)+rho_0 and eta_k/tau_k<=b/(1-1/U)+eta_0. Choose w larger than twice these constants plus the short-burst spatial guard. Geometry constants a,b do not depend on w; choose B sufficiently large after fixing w so that all idle gaps fit.

## 5. Poisson renormalization with genuine independence

Let the physical radius law be Pareto P(R>r)=r^(-alpha), r>=1, alpha>d, and intensity lambda. For a line embedded in R^d, integrate transverse burst centers. The exact induced marked intensity on the line is

    lambda (2R)^(d-1) dx dt F(dR).

Thus the line sees a one-dimensional burst process with the radius law tilted by R^(d-1); for Pareto marks its effective tail exponent is alpha-d+1. It is not legitimate simply to use the unmodified one-dimensional radius law.

Let p_k bound the probability that a specified level-k coarse fault/support test occurs. Because a non-nice next-level window contains two coarse fault points separated by more than w in space or time, it contains two candidate level-k tests with sufficiently separated raw influence regions. There are at most a fixed C(B,U) candidate pairs. The previous-step/neighbor inflation in Section 3 only changes these fixed constants.

Exclude all physical bursts with radius at least cL_k that intersect the enlarged parent dependence region. Their mean count is at most

    D lambda tau_(k+1) L_(k+1)^(d-alpha)
       = D lambda theta^(k+1),
    theta = U B^(d-alpha).

For example, on the line this follows by integrating

    lambda tau_(k+1) E[(A L_(k+1)+2R)(2R)^(d-1) 1_(R>=cL_k)],

which has the stated scale for alpha>d. A more conservative enclosing d-dimensional cube gives the same exponent. The constants include B, c, the support enlargement and the finite-radius discretization guard.

After this exclusion, the two sufficiently separated child tests depend on disjoint regions of the marked Poisson process. Temporal separation works because the physical bursts are instantaneous; spatial separation works after enlarging each child region by the cutoff radius. The restricted small-radius Poisson fields are independent. Their bad-test probabilities are no greater than p_k, since the support construction is monotone in the raw fault set. Large- and small-radius Poisson processes are independent thinnings.

Therefore the actual bound is

    p_(k+1) <= C p_k^2 + D lambda theta^(k+1).

This square comes from separated Poisson influence sets, not from two marginal error estimates. The deterministic two-fault implication follows from the explicit R/C gadget and projection, rather than from independent isolated Toom repair cones.

A finite set fails to fit in one w-by-w rectangle precisely when two points differ by more than w in space or time. A parent window contains O(BU) candidate child points. Each child event depends on raw faults in its uniformly bounded footprint above; truncating radii below cL_k expands its Poisson influence set spatially by at most cL_k and not temporally. The chosen w makes these sets disjoint. C is a fixed multiple of (BU)^2, including the forward-neighbor union factor. Exclude large bursts over the enlarged parent dependence window, so an outside large burst cannot secretly couple the child tests. No conditioning on successful past computation is used.

The base bound is p_0<=C_0 lambda, using finite E[R^d]. If theta<1, choose A>=max(C_0,2D) and sufficiently small fixed lambda, for example lambda<=theta/(2CA). Induction gives

    p_k <= A lambda theta^k.

Choose the integer parameters so that z=log(U)/log(B) lies in (1,alpha-d); then theta=B^(z+d-alpha)<1 exactly. Such a z exists precisely for strict Pareto alpha>d+1.

## 6. Finite seed, growing encoding, and physical readout

The following conversions are ordinary finite circuits and are included in the failure budget. No special perfect level-conversion gate is assumed.

At level k, a fixed-size-in-k circuit of at most M(B) primitive child rectangles (a conservative bound M(B)=O(B^2) suffices) copies the current logical bit into the five Info positions of a new level-(k+1) macrocell, prepares its input-independent working registers and resets retired data. It uses local neighbor transfer and compiled identities while values wait. Its duration is O(B tau_k) and extent O(B L_k). Its failure is at most M(B)p_k by a union bound; no independence is needed here.

For this claim use the whole lower-level projected bit trajectory, including workspace, through the conversion. On the event of no induced coarse fault in the finite encoding circuit, its output is the exact desired higher-level code pattern in that projected trajectory. It therefore supplies regular initial Info for the next projection. Lower physical residues are not assumed absent: their later effects are already in the lower-level Bad/ForwardNeighbor support envelope. Pad stage boundaries to the applicable macroperiods and retain the preceding-period guard in every dependence box. If a conversion fails, charge that event; do not condition the Poisson square bound on successful history.

Conversely, a level-k circuit transports the five child logical copies of a level-(k+1) encoding to a local majority operation and retains its answer in one child encoding. This costs the same order and has the same failure bound. It is a charged local decoding path, not a global decoder. Further downward conversions eventually reach a fixed finite terminal circuit.

Choose a fixed starting level k_0, independent of the requested horizon T. Commission its input-dependent encoding using a finite local writing circuit. If a bare input is used, a conservative success event is that no burst intersects its finite commissioning spacetime region; its error contribution is at most C_prep lambda plus the writer's stated entry error. This is a fixed paid cost, not an assumption that enlarging the seed erases earlier exposure. All input-dependent copies after commissioning lie in the fixed radius r_0=O(L_(k_0)); outside initial data are input-independent.

Given T, choose K with tau_K>=T. Ascend through levels k_0,...,K, execute O(1) top-level holding steps as needed, and descend to the fixed terminal interface. The overall delivery time is O(tau_K)=O(T), with the constant depending on the fixed family. The readout delay can be O(T), and is explicitly part of the endpoint. This is not a fast local-query theorem.

The accumulated data error is bounded by

    delta_prep + 2 M(B) sum_(k>=k_0) p_k + C_hold p_K + delta_terminal
      <= delta_prep + 2 M(B) A lambda theta^(k_0)/(1-theta)
          + C_hold A lambda theta^K + delta_terminal.

The terminal detector/circuit has a fixed nonzero error floor included in delta_terminal. Small enough fixed lambda and a specified terminal error budget make the total at most 1/4 uniformly in T. The final local collection and every retained input-dependent register remain in the fault model until delivery.

Fresh input-independent hardware can be installed before the unknown input arrives; construction costs are charged. It does not contain a copy of the answer. Blank initialization/reset is a declared finite local operation; no protected external backup is used.

Prewarm a fresh adjacent destination while the source runs protected identities; reset never touches the retained source. The source/destination intervals across the ladder occupy a geometric sum O(L_K), and retired intervals can be reset and reused during descent. All scale changes occur at compatible child-macroperiod boundaries, with deterministic padding and the preceding-period fault guard retained. The supplement gives the staged-reset induction that handles arbitrary initial workspace without requiring every microscopic reset to succeed.

## 7. Resource consequence and comparison

For the one-dimensional layout in R^d,

    active register-line extent/cell count O(L_K) = O(T^(1/z)),
    delivery duration O(T),
    local work and spacetime O(L_K tau_K) = O(T^(1+1/z)).

An explicit schedule has O(L_K tau_K) local-gate instructions, each requiring O(log T) address/time bits; uniform generation has a proportional polynomial bit cost. A compact recursive description is also possible because the template is fixed. The active-register count is not asserted to include a separately engineered reliable schedule controller. Such a controller is part of the granted immutable scheduling premise; constructing a physical replacement could require additional hardware, time and energy. Per-site operating power gives the same spacetime scaling for the charged gate-operation energy, in addition to commissioning, reset and metrology costs. This is not a universal thermodynamic lower bound or a total physical-hardware optimum.

For any strict Pareto alpha>d+1, z can be chosen arbitrarily close to alpha-d from below, so the hardware exponent approaches 1/(alpha-d) from above. The fixed-device complete-cover obstruction has precisely that extent exponent. This supplies an asymptotic approach to the ceiling; it does not establish a sharp constant or the endpoint exponent with bounded overhead.

The mechanism is an actively corrected classical bit. It does not supply passive quantum storage, arbitrary quantum reference preservation, positive information density, or universal computation. The universal cone-erasure obstruction still applies to any later input-dependent computation, but those positive bridges need separate constructions.

The full strict Pareto classification would now pair the accepted negative result alpha<=d+1 with this immutable-schedule construction for alpha>d+1. It is stronger than a Poisson-hail workload conclusion because it supplies semantic storage, finite seed and local readout. Its scientific status depends on the explicit circuit/projection proof and the absence of a prior theorem already covering the same correlated-burst contract.

## 8. Stronger published comparator: Tsirelson and extended rectangles

Balasubramanian, Davydova and Lake, *A local automaton for the 2D toric code*, Quantum 10, 2125 (2026), Section 2, review and modify Tsirelson's hardwired one-dimensional classical automaton. Its immutable time-dependent instruction convention matches the schedule abstraction here. Appendix B gives EC A/EC B and the extended-rectangle argument for arbitrary incoming syndromes; Appendix C.1 explicitly mentions doubling EC as an alternative proof of EC A. Neither double normalization nor an arbitrary-input fault-tolerance compiler is claimed as generally new.

The unpadded classical construction has spatial factor 3 and time factor 6, hence z=log(6)/log(3)>1. A direct burst-moment transfer with those fixed factors would demand alpha>d+z. Concatenating that fixed template preserves z. The padded island-tolerant routine here permits an arbitrarily large B with active time at most c_0 B, so z can be chosen in (1,alpha-d) for every strict Pareto alpha>d+1.

The published probabilistic theorem uses p-bounded/local-stochastic noise. A single sufficiently large spatial burst corrupts a contiguous set of n sites with polynomially small probability in n, whereas p-boundedness requires an upper bound p^n. The original p-bounded threshold therefore cannot simply be applied to this physical field. The bridge supplied here is monotone arbitrary-field projection, separated short-radius Poisson influence tests, the additive large-radius term, and finite-seed growth with finite local delivery. This is a comparison of stated theorems, not an exhaustive historical novelty proof.

## 9. Primary source anchors

1. P. Gacs, *Reliable Computation with Cellular Automata*, JCSS 32 (1986), 15–78. Author PDF: https://www.cs.bu.edu/faculty/gacs/papers/GacsReliableCA86.pdf . Section 5, especially Theorem 4 and its proof, printed pp. 30–31 / PDF pp. 15–16, contains the five-spaced-copy and three-temporal-computation routine under correct Addr/Age. The present model supplies those by immutable gates/schedule. The source's later structure-restoration and self-simulation tasks are not assumed solved by the nice-fault lemma.

2. P. Gacs, *Reliably computing cellular automata*, 2012 lecture notes: https://cs-web.bu.edu/faculty/gacs/papers/Recife_2012_lect.pdf . Pages 56–59 give the program outline and Nice Faults lemma; pp. 64–66 discuss sparse correction and alphabet growth; p. 71 warns that the global sparse-noise theorem is not yet an arbitrary-error amplifier. The R/C projection and binary-circuit substitution above address those two issues for this fixed-schedule burst implementation. Generic normalization/exRec machinery is credited to the stronger published comparator below.

3. The original P3 governing return/report and uniform-horizon refinement are saved unchanged in `sources/`. The cone-loss lower theorem is accepted at its source scope, not re-proved here.

No claim is made that this construction has been physically built or that a numerical simulation validates the infinite-scale theorem. The exact checker is a finite audit of one newly supplied semantic bridge.

4. S. Balasubramanian, M. Davydova and E. Lake, *A local automaton for the 2D toric code*, Quantum 10, 2125 (2026), published final version: https://quantum-journal.org/papers/q-2026-06-02-2125/pdf/ . Section 2, Appendix B, Appendix C.1. This is stronger directly compatible fault-tolerance prior art than the Gacs lecture alone. Primary extraction: `sources/bdlake_2026_tsirelson_exrec.txt`.
