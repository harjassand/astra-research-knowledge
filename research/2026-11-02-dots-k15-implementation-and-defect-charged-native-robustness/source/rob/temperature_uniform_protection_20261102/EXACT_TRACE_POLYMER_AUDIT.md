# Independent audit: exact canonical trace polymers

2026-11-02. Reviewer: `producer-workspace/audit_exact_trace_polymer_gas`.

## Decisive finding

**PASS for the explicitly strengthened representation `T_plus` below, using the specified fixed-input-seeded, all-branch decoder implementation. NOT a claim already proved by the older removable-witness theorem.**

The earlier construction establishes validity of whole trace restrictions and retained decoder histories. Its generic F1–F4 statement deliberately does not establish an insertion theorem. Moreover, a union of activated stencils need not be induced in its ambient graph, so its distinct components need not satisfy the proposed “no ambient edge” compatibility. Those two distinctions must remain visible.

The root has now explicitly adopted this new representation convention, without changing the decoder:

    V(s) = the charged, typed, labeled vertex set of its old full trace T(s),
    T_plus(s) = G[V(s)].

Add EVERY ambient edge with BOTH endpoints already in `V(s)`. Add no vertex, do not activate any zero gate, and do not recompute any sheet choice after completing these edges. A polymer is a nonempty connected **canonical labeled** `T_plus(tau)`, for a valid nonzero syndrome `tau`. Two polymers are compatible precisely when their vertex sets are disjoint and have no ambient edge between them.

For this convention and the concrete union-seeded implementation, I prove below:

1. Every component `C` of `T_plus(s)` has valid physical leaf syndrome `tau_C` and **exactly** `T_plus(tau_C)=C`, including ghost vertices and canonical labels.
2. Every compatible collection assembles exactly:

       T_plus(XOR_i tau_i) = disjoint union_i T_plus(tau_i).

3. Therefore the connected canonical traces give an exact bijection for ALL valid syndromes, not merely an injection on witness events.

The completion preserves the already earned linear charge, degree and entropy bounds. It does not by itself prove factorization for a perturbed/noncommuting Gibbs state.

## 1. Files and scope reviewed

Primary original documents:

- `explicit_memory_witness_20261102/ROOT_FULL_TRACE_JOIN_ADDENDUM.md`, SHA-256 `8274c662e5dab4c5366519bde7953ad8251fabc494c11f74910218d6c499ade2`.
- `explicit_memory_witness_20261102/ROOT_SMALL_SCALE_MEMORY_JOIN.md`, SHA-256 `1f92644f6e97f8261690bf8fbf08758b8b491181541ebc09e5ba9fb7e4c1ea95`.
- `component_decoder_threshold_20261102/FULL_TRACE_REMOVABLE_EXTENSION.md`, SHA-256 `6e1fec2cebdfa4bc70f0c74596be94e9afce6aff72e93a1288aacee1a143288e`.
- `component_decoder_threshold_20261102/PACKET_CHARGE_EXTENSION.md`, SHA-256 `e862fcad8e25bc456311931982f01a3dc94c94b8697534a66665905240613d93`.
- `local_duality_transfer_20261102/REMOVABLE_TRACE_EXTENSION.md`, SHA-256 `aa4c5b287f179b8371d14b1d4ef978c4d34e24548e03c7a56665cead7fd8df2f`.

Also inspected the component theorem, its full-trace and joined independent audits, the actual-family binding supplement in `FRESH_WHOLE_FAMILY_AUDIT.md`, the packet ownership contract, and the new constructor's `EXACT_TRACE_POLYMER_REASSEMBLY.md`.

This audit takes the previously admitted actual-family maps, common lifts, local identities, and charged shape bounds as its input. It is not a new executable all-recursion coordinate verification. The new mathematical issue is exact trace replay and reverse assembly.

## 2. Why the old conclusion was insufficient on its own

Deletion closure only addresses collections of components already observed together in ONE run. It need not characterize which independently observed components can coexist after insertion. The old theorem explicitly warns about this and only consumes the valid-removal injection in its probability proof.

There is also a distinct graph-convention issue. A bounded-degree ambient graph may contain a possible edge which is absent from the presently activated-stencil union. Then different components of that union may be adjacent in the ambient graph. The proposed no-ambient-edge compatibility would reject a collection that actually occurs.

A small example shows this is a real logical gap, not an implication of deletion closure. Let every binary syndrome on coordinates `a,b,c` be valid, and correct it by the identity boundary map, with zero coarse output. Use fixed connected seed stencils

    S_a: a--A--x,
    S_b: b--B--y,
    S_c: c--C--x--y.

Here `A,B,C` are correction ports and `x,y` are bounded zero halo/connector ports. Let `G` be the union of all possible stencils. All decisions may be trivial; all correction rows and packet blocks are local, zero preservation and contraction hold, and deletion exactly preserves the surviving trace. But `T(a+b)=S_a union S_b` has two components while `G` has edge `x--y`, supplied by `S_c`. Thus those two components are incompatible under the proposed rule. This example shows what the *written abstract interfaces* fail to imply; it is not a claim that the particular family must instantiate these exact ports.

The induced-edge completion repairs this issue without a new physical interaction or an uncharged closure. It merges existing trace components only. In particular, it is not “complete a component of the entire ambient graph.”

## 3. The additional insertion premise actually used

The positive result uses the literal implementation specified in the root join and actual-family supplement, not the most general alternative permitted by abstract F1:

- Before choosing sheets, a layer's active component geometry comes from fixed bounded stencils seeded by occupied input packet blocks. It includes both branches' potential correction/output supports and every possible collision/ownership connection.
- Whole input packets are retained. All possible contributors to an output packet are connected before choosing the branch. The packet charge is only a deterministic finite lookup on that unchanged whole state.
- Each original decoder component makes its own deterministic choice from its labeled inputs. There is no component enumeration dependency, off-component control, or unrecorded global state.
- Extra recorded actual residual rows are activated from nonzero operands, and their complete fixed operand stencils are recorded. Incidental zeros do not seed further rows or layers.
- Every trace vertex belongs to a charged seeded stencil connected to its seed/ancestry; there are no unowned free ghost components.
- The physical linear prepass activates a row gate when ANY occupied physical input contributes to it, even if its XOR output is zero.
- A single common finite terminal bag is present exactly when terminal input is nonzero, and the terminal decoder sends zero to zero.

These rules exclude an assembly predicate which activates a new, previously unrecorded bridge only when two or more independent components are simultaneously present. `T_plus` alone would NOT repair such a predicate: it adds edges only, never missing vertices. Both-branch map footprints and all potential ownership/collision stencils are the reason this predicate is excluded here.

Typed coordinate ports are distinct even if geometrically colocated, unless the fixed graph explicitly identifies/connects them. Canonical labels include occupied versus zero values and each original component's branch flag. The new trace-component grouping does NOT authorize replacing several old flags with one new minimum choice.

## 4. Forward restriction gives exact replay, not only validity

Fix valid `s` and a component `C` of `T_plus(s)`. Since old trace edges are ambient edges, `C` is a union of whole components of `T(s)`. Restricting the original local residual identities keeps every nonzero operand of a row or none. Whole packet ownership is preserved. The terminal restriction is the complete old terminal input/correction or zero. Telescoping therefore gives a filling of the restricted physical leaf syndrome `tau_C`, BEFORE invoking a decoder on it. In particular `tau_C` is valid.

Delete all other original full-trace components. F1 and the literal union-seeded layer rule leave the retained input component states, flags, corrections, and coarse outputs unchanged, layer by layer. At the terminal, the input is unchanged or zero, so the recorded correction agrees as well.

One must additionally check the ghost vertices to obtain equality of traces rather than only equality of computed nonzero variables. That check succeeds here:

- A fixed input-seeded stencil intersecting `C` has its connected occupied seed in `C`, so it remains seeded in the replay.
- A row seeded by a retained nonzero operand is recorded again with the same complete stencil. If a recorded row/stencil is retained, its nonzero or component owner is in that same original trace component; it cannot be secretly owned only by a discarded component.
- A potential zero stencil recorded on behalf of a component is retained because that whole component and its same labeled input are retained.
- The full terminal bag is retained exactly when its retained terminal input is nonzero.

Hence no vertex of `C` loses its last seed, and no new stencil appears. The “remove any now-unseeded incidental zeros” caveat in the generic deletion statement causes no loss inside a selected complete component with this connected seed ownership.

Thus the replayed old vertex set is exactly `V(s) intersect C`, with the same labels. Completing ambient edges gives

    T_plus(tau_C)=G[V(s) intersect C]=C.

Each `C` contains a nonzero physical leaf: ancestry/zero preservation excludes a nonempty charged component without an occupied ancestor (the physical kernel-only prepass case has physical leaves even if no dual output). Distinct `C` have disjoint leaves, and those leaves exhaust `s`. Because `T_plus(s)` is induced, its different components have no ambient edges between them. They are compatible polymers.

## 5. Reverse assembly: no new vertices, decisions, or cancellations

Take a finite compatible collection `W_i=T_plus(tau_i)` of canonical connected polymers. The physical occupied leaf supports are disjoint, since a common occupied input coordinate would be a common trace vertex. Set `s=XOR_i tau_i`; its physical support is their disjoint union. Since valid syndromes are a linear coboundary space, `s` is valid.

### 5.1 Physical duality prepass, when present

For a fixed row of `F^2`, every polymer containing any occupied contributor already contains that row's active gate, regardless of the XOR value. Two polymers contributing to the same row would share its gate and hence be incompatible. Consequently all occupied contributors to a row belong to at most one polymer. The union prepass has exactly the union of the standalone gates and occupied wires; its row outputs have the same values as before, with no cross-polymer cancellation. The initial dual syndrome is the disjoint union of the standalone dual syndromes.

A zero-output prepass component remains present with all its physical leaves and cancellation gates. It is not discarded for having no dual output. Optional fixed `H^2` stencils obey the same seed-union rule. The fully lifted `G` postpass is NOT introduced into the trace; its linear correction may overlap algebraically without causing trace activation.

### 5.2 Packet layers and component decisions

Inductively suppose a layer's input is the disjoint union of the standalone layer inputs. Two polymers cannot contribute different portions of one packet block: each standalone occupied packet records the complete block, so their charged vertex sets would overlap. Each retained packet therefore has exactly its standalone state, not merely the same total charge.

The active pre-choice stencils on the union input are exactly the union of the standalone fixed stencils. No two different polymers' stencils can meet or acquire a dependency edge: meeting is overlap, and a fixed cross edge would be ambient adjacency, both excluded by compatibility. Therefore each original layer decoder component is exactly an old standalone component. Its component-local deterministic choice and computed correction/output values are unchanged. This argument applies to the ORIGINAL decoder components, not the possibly larger `T_plus` components.

The potential supports of BOTH branches were recorded before choosing. If two different polymers could contribute to the same correction coordinate, output coordinate, or output packet, their potential stencils would share the corresponding coordinate/owner port or be joined by its fixed dependency connection. Compatibility excludes this. Therefore the recombined actual outputs/corrections have no new cross-polymer cancellation; the next-layer nonzero input remains exactly the union of the standalone inputs.

The finite-state packet charge and matching lookup are not hidden nonlinear assembly gates. They are evaluated on unchanged whole packet/component inputs. Their outputs and their resulting minimum-sheet choice are therefore identical.

### 5.3 Residual rows and zero activation

A residual row becomes active only because some actual operand is nonzero (or because it was already included as a charged component's fixed potential stencil). In the union run that operand belongs to a standalone run and has the same value there, so the row's complete stencil was already present. A new row cannot be created solely by placing old zero halo ports together. Every old active row remains active because cross-polymer nonzero cancellation at its variable ports was excluded above. Thus residual bookkeeping creates no new vertex and removes no old one.

The same reasoning handles all bounded auxiliary/comparison residual identities actually recorded in the construction. It would fail for an extra unrecorded conjunction-based gate, which is why the literal seed rule is essential.

### 5.4 Terminal action

At most one standalone polymer has nonzero terminal input: two would both contain the same finite terminal bag and hence overlap. The union terminal decoder therefore sees the unchanged standalone terminal input, or zero. Its action is exactly the recorded action. Several originally separate layer components may reach that one bag, but they are already one full-trace polymer; their original component flags are not changed.

Induction proves equality of all old charged vertex sets and labels:

    V(s)=disjoint union_i V(tau_i).

Completing ambient edges adds no cross edge by compatibility. Therefore

    T_plus(s)=disjoint union_i W_i.

This is the required reverse assembly theorem.

## 6. Bijection, exact classical gas, and quantitative inheritance

Define `P` to be the nonempty canonical connected `T_plus(tau)` over valid `tau`. Polymers are labeled records, not unlabelled geometric sets: different occupied packet patterns may have the same geometric halo and must not be conflated.

The forward map sends any valid syndrome to the components of its unique canonical `T_plus` trace. The reverse map takes the disjoint XOR of polymer leaf syndromes. Sections 4–5 make these mutually inverse. The empty collection corresponds to zero syndrome. This establishes an exact canonical representation on the full valid syndrome space.

For equal-multiplicity stabilizer syndrome sectors with additive excitation energy

    E(s)=sum_j epsilon_j s_j,

one consequently has, after dropping the common vacuum-energy/sector-multiplicity factor,

    Z_syndrome = sum_{compatible Gamma} product_(W in Gamma) z(W),
    z(W)=exp[-beta sum_(j in supp(tau_W)) epsilon_j].

A valid-removal ratio alone, or a general positive syndrome weight satisfying it, does NOT imply these factorized activities. The exact gas formula here uses the additive commuting reference energy and equal sector multiplicity. Exact combinatorial encoding still exists for other weights, but their gas weight can contain interactions.

`T_plus` adds no vertices; its components are unions of old complete components. The old selected-union charge recurrence therefore gives `|V(W)|<=C |tau_W|`. Its degree is the same bounded ambient degree. Finite labels and rooted connected-animal counting give at most `A^m` polymers of mass `m` through a fixed vertex, with no free scale/depth labels. A polymer is incompatible only through its own vertices or their at most boundedly many ambient neighbors, so the number of relevant incompatibility anchors is at most `C' m`.

For `epsilon_j>=epsilon_min>0` and a fixed `a>0`, the usual KP bound follows once

    C' sum_(k>=1) A^k exp[-(beta epsilon_min-a)k] <= a.

The exact gas therefore supplies legitimate low-activity connected/Ursell estimates for the commuting reference. Source-observable dependence regions and their anchor incidence still have to be included when applying those estimates.

## 7. Boundaries of this sign-off

- The NEW induced-edge completion must be declared. Do not retroactively say the removal-only package had already established this gas.
- Do not broaden the insertion theorem to arbitrary F1–F4 decoders with component-dependent unrecorded activation. Its proof uses the concrete fixed-seed/all-potential-stencil rule.
- Do not choose one new branch for a merged `T_plus` component. This is a representation grouping only; all old per-layer choices are replayed.
- Cancelled prepass gates and complete owner/operand stencils are essential. Discarding them destroys the reverse argument and may also destroy validity of restriction.
- No expansion of the finest-level `G` image or other fully lifted correction support is justified by this trace-size proof. Those are handled algebraically/separately.
- The graph is a space–scale graph. This result does not, without an additional support analysis, assert exponential clustering in physical Euclidean distance.
- Annealed noncommuting source bounds, temperature-uniform coefficient control, bath-volume uniformity, and the perturbed denominator remain separate claims. Exact static combinatorics removes one obstacle but does not supply those analytic estimates.

**Final audit verdict:** the requested exact canonical polymer gas is rigorously available for the commuting syndrome reference after the root's explicitly adopted `T_plus` convention, with the declared union-seeded implementation and no new decoder decisions. The older injection argument alone would not have earned it.
