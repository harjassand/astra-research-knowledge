# Independent actual-binding and whole ideal-sampler receipt

1 November2026. **Qualified PASS for a constructive ideal commuting-Gibbs syndrome sampler for the actual recursive family, with a matched supplied/computably fixed decoder.** This is not a noisy physical loader or a sampler for generic noncommuting interacting equilibrium.

Frozen audited files:
- `recursive_initialization/actual_decoder_binding.md`: SHA256 `61a0a149960cfe21beb30d0d4a91f2553932227675e6dbb26514c5501cdbf685`.
- `ROOT_RECURSIVE_THERMAL_SAMPLER_JOIN.md`: `a28c7243fd3136019e4df64e7ffaa7da1912573e43e6587412c3c157fc7e3879`.
- Governing abstract root: `3a724349a408548f8d86b012c05638109c27a5613a16674648e8b775fc4cf81c`, received in `ABSTRACT_TRACE_POLYMER_RECEIPT.md`.

Personally checked the governing source text `producer-workspace/source.txt`, Sections4–5: Lemmas4.8/4.12, Corollaries4.9/4.13, RZ parity reduction, RX endpoint duplication, recursive correction identity, and especially the modified level2 decoder in Section5.1.1. No introductory unrestricted confinement claim is used.

## 1. Actual validity recognizer

RX X-gadget syndrome restriction of a globally valid input is in the local image. The source's local correction exists with the stated outgoing-weight bound; the fixed table can choose zero on zero input. After this cleanup, the proof-only H1(Yx)=0 error cleaning establishes that every Q restriction is in its local image. The actual algorithm does not pretend to know or compute the unknown error. Lemma4.12 supplies the Q correction and its endpoint bound. Both intermediate syndrome weights are nonincreasing. A valid residual has only duplicated Z endpoint coordinates, so the parent syndrome weight is half the residual weight.

For RZ, parity on each connected local graph is precisely the quotient by local boundaries. Moving the input to its fixed parity anchor has an explicit local correction and a nonincreasing parent syndrome. These are the actual source maps, not an arbitrary coarse energy model.

On arbitrary inputs, the image tests, duplicate-endpoint checks and coordinatewise one-step reconstruction flags suffice. If all flags vanish and the terminal image test accepts, repeated substitution of checked identities and the actual chain-map relation produces a fine correction with boundary equal to the original input. Hence acceptance implies global image membership, including all redundant-check constraints. Conversely valid inputs pass by the source theorems. No global metacheck oracle is hidden.

The terminal object MUST be the whole fixed level2 block and its SAME Section5.1.1 decoder. The binding correctly retains it instead of silently reverting to a five-qubit seed lookup. Its O(ell^4) input and potentially exponential fixed-parameter table are charged to the constants. Fixed local choices must be supplied, or computed by the declared finite admissible search, with the same choices defining the logical frame. This is not a compilation theorem for an inaccessible/noncomputable decoder oracle.

**Totalization convention:** on a failed local membership/endpoint/terminal test, retain the reject flag and set unspecified correction/coarse outputs deterministically, for example to zero. The frozen text's “reject; otherwise choose” needs this interpretation to define a total fixed DAG. It has no effect on accepted executions, the sampler, or their activity bound.

## 2. Linear active size and O(n) host

At fixed ell, bounded incidence gives fixed-size local tables, updates and identity stencils. Tables can be used as macro-gates; no arbitrary Boolean compilation is assumed to preserve zero behavior. Every gate has all-zero output on all-zero input under the specified normalization.

For each valid level, RX uses at most three syndrome stages of weight no greater than the incoming weight. Every active local solve has a nonzero local input; every nonzero correction bit comes from such a solve; each emitted bit has fixed fanout. Active update/validation gates, including cancellation gates, can therefore be charged to these stage inputs with a sufficiently large fixed S. The terminal macro-gate is included in S. Alternating factor1 and factor1/2 reductions imply sum_i|sigma_i|<=4|sigma_top|. Hence12S|sigma_top| is a safe uniform bound after absorbing the finite local bookkeeping into S.

The full downward physical representative is correctly excluded from this trace. Expanding its high-level corrections during trace construction could violate the linear energy-size relation. It is reconstructed separately after sampling, at polynomial charged cost.

Every qubit has both check types. Thus each replacement has at least(ell+1) old-qubit block vertices and n_(i+1)>=(ell+1)n_i>=4n_i. All check/gate counts per level are O(n_i), and their geometric sum is O(n_top). The typed stencil graph has bounded degree and a finite label alphabet, with constants depending on fixed ell and the fixed terminal block. Therefore the actual construction meets the abstract host and active-size premises, not merely a generic polynomial decoder runtime bound.

## 3. Exact local trace recognition

The local membership promise is valid with the following exactness conditions, agreed as implementation clarifications:
- a listed gate is marked iff at least one input is nonzero;
- listed nonzero top inputs are exactly the selected top syndrome support;
- every listed gate includes its COMPLETE input/output stencil, with consistent values and its exact deterministic truth table;
- every nonzero wire includes all required active fanout gates and its producer unless it is a top input;
- unlisted boundary values are zero and no extraneous marked objects are admitted;
- all rejecting flags are zero and the marked component is connected.

If internal wire objects are separately represented, mark each iff its value is nonzero; equivalently insert zero-preserving identity objects. Their bounded incidence and number are absorbed into S. Recording internal wires only as gate-stencil values is another valid canonical convention. Optional zero-wire/gate decorations would destroy uniqueness and are NOT allowed.

Under these checks, any hypothetical missing active external gate has a first nonzero incoming boundary wire, contradicting complete fanout/zero boundary. Thus unlisted gates evaluate to zero, and the candidate is its exact isolated replay. Bounded stencils/fanout make recognition polynomial in candidate size using preprocessed local incidence/table access, rather than an O(n) global image query. Identifier bit lengths/random-access preprocessing must still be charged. Full replay is a correct polynomial fallback.

## 4. Exact Gibbs gas and established sampling consumer

The received abstract component theorem now applies to this actual validator. It gives a bijection between valid syndromes and compatible connected exact traces. Top input supports are disjoint and additive energy factors exactly. Equal dimensions of valid stabilizer eigenspaces remove any error-representative multiplicity. CSS syndrome spaces factor because the X and Z parity-check images can be realized independently by a Pauli product; their energies factor as well. Allocate sampling errors between the two sectors.

With A=12S, activity is bounded by exp[-beta J_min m/A]. At sufficiently low fixed temperature, both the elementary weighted mixing condition and the stronger exponential sampling criterion hold. The threshold may be far below any practically useful temperature because A and label/degree constants are enormous. It is still fixed independently of n.

Primary comparator checked directly: [Chen–Galanis–Goldberg–Perkins–Stewart–Vigoda, arXiv:1901.06653v6](https://arxiv.org/html/1901.06653v6), Definitions1,3,4 and Theorem5. Exact traces are connected labeled subsets of the stencil-overlap host; compatibility is distance at least2. Their local membership and weight routines meet the theorem's mathematical computational contract after fixed-parameter preprocessing. Its near-linear sampling bound is in that model; encoded coefficient precision, identifiers, table construction and random-bit costs are not erased by quoting it. No new general polymer-sampling theorem is claimed.

The root's explicit logarithmic dictionary plus birth–death coupling remains a self-contained polynomial-in-n/epsilon fallback. Its Poisson cap is valid by the stated exponential-moment estimate. Truncation, mixing, cap, approximate weights, transition probabilities and Poisson sampling must each receive error budget. No exact-real oracle or unlimited runtime is required. This fallback suffices even if one declines a stronger near-linear implementation claim.

## 5. Quantum preparation channel and limits

For a supplied encoded input, including an arbitrary reference, the matched representative E_D(sigma) maps to rho_LR tensor the pure syndrome label in THAT decoder frame. The product order/phases must match the fixed decoder; irrelevant sectorwise global phases do not change the channel. Orthogonal syndrome blocks make the output trace-norm difference exactly the l1 difference of sampled syndrome probabilities, hence at most2epsilon. There is no reference-dimension loss.

Hierarchical physical correction reconstruction has polynomial classical cost at fixed ell, but is outside the activity trace. Applying its final Pauli string is an ideal operation with separately charged routing/addressing/duration. A ground-state encoder is still needed if no encoded input is supplied. Fixed-rate noisy output errors are not cured by a classical syndrome-sampling theorem.

This closes the constructive IDEAL thermal-syndrome preparation obstruction for the known commuting family. It neither establishes passive local thermal mixing nor prepares the actual joint Gibbs state after generic noncommuting perturbations or inaccessible-bath coupling. It provides no constant-noise write/read threshold, return-to-equilibrium bound, or superiority over an actively protected comparator with the same control resources.

## 6. Actual finite diagnostic

Independently reran `actual_rx_recognizer_fixture.py`, suppressing only its final stored-result write. It passed all4096 syndrome inputs:2048 accepted,2048 rejected; local flags exactly matched the global binary image;2071 accepting component replays were exact;24 inputs had genuine two-component decompositions. The host had135 objects and maximum degree26; observed trace/weight ratio was51.

This fixture is one RX step of the19-qubit Bell-square construction at ell3. It is NOT the actual family's modified whole-level2 terminal block and is not a multilevel performance experiment. The all-level acceptance above rests on the source-matched proof, not extrapolation from this fixture.

No substantive formal gap found, subject to the stated total-table/exact-marking/encoded-computation conventions. The ideal commuting whole join is accepted; physical and generic-V loading boundaries remain open.
