# Broadcast programming of reciprocal bistable material cells

An explicit reciprocal energy network can write every `N`-bit stationary output pattern using a fixed scalar control alphabet, constant deterministic switching margins, `5N+2` cells, and at most `3N+8` commands including reset. The construction includes the reciprocal back-action of the write gate and its reset layer; it does not assume a one-way local signal.

This is an internally constructed mathematical operation. **A new civilization-scale capability and a practical advantage remain NOT_ACHIEVED.** One-drive mechanical and magnetic shift registers are strong established prior operations. The present result gives a particular all-`N` energy construction with explicit reset and margins; it does not establish a new generic memory capability or acquire its broadcast hardware.

## The consequential question and the constructive result

The independently locked question was whether a material could be programmed through one global scalar input without individually addressed cells, an increasing number of clock phases, or increasingly fine coercivity thresholds. The intended consequence was an interface for programmable spatial material states with few external controls. The seed was locked before the new literature and sibling recon in [SEED_LOCK.json](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/SEED_LOCK.json).

The construction has three local components: an antiferromagnetic-like track that moves a domain wall, stationary memories written only beside that wall, and an auxiliary bias layer that prepares and resets the track. A simple domain-wall counter alone failed the reset requirement: it grows its preferred phase but does not automatically recreate the higher-energy starting pattern. The auxiliary layer fixes this specific failure by preparing the track with one staggered preference and then reversing that preference before writing.

The exact energy is

\[
E=\sum_i c_i(1-x_i^2)/2-H\sum_i g_ix_i-\sum_i b_ix_i-\sum_{i<j}J_{ij}x_ix_j,
\quad x_i\in[-1,1],\quad J_{ij}=J_{ji}.
\]

Each coordinate has finite onsite curvature and two mechanical stops. Its stability margin at endpoint `s_i` is

\[
c_i+s_i(g_iH+b_i+\sum_jJ_{ij}s_j).
\]

The track uses `c=10`, field gain one, and nearest-neighbor coupling `-10`. Each track cell couples reciprocally to an auxiliary with `c=40`, gain two, and coupling of alternating sign and magnitude four. Each output memory has `c=13`, gain one, and couplings `+1` to an adjacent pair of track cells. There are only two fixed boundary references. All coefficients and the nine commanded levels are independent of array size.

During programming, a global `+10` pulse advances the track to a `++` wall beside one memory. That memory sees a field offset of two, so an optional global `+12` overshoot writes it; all other unwritten memories remain below threshold. A global `-10` pulse then advances the wall and removes the local write permission. Previously written outputs hold their signs. The setup and global reset sequence are explicit, rather than supplied by manual local setting.

The [complete proof](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/PROOF.md) gives the energy, all coefficients, reset, spatial induction, wrong-write inequalities, deterministic perturbation bound, and full ideal-cycle work. The maximum graph degree is four and weighted degree is 25. All non-switching coordinates retain margin at least two at intended critical events; every pulse endpoint has margin at least one. Intended simultaneous switching groups have no mutual coupling, and the inequalities cover their entire continuous transition box. Thus their order cannot corrupt the operation.

![Reciprocal architecture, exact example, and source-work cost](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/broadcast_construction.png)

## A real same-input comparison and strong incumbents

There is a strict restricted comparison against **independent** hysterons. With a fixed alphabet of `K` scalar levels, upper and lower thresholds can occupy only finitely many response bins, at most `(K+1)(K+2)/2`. Cells in the same bin class, starting from a common reset state, have identical responses to every input word. Such an array cannot write every word on arbitrarily many independently specified output bits. The construction uses interactions to store the address state locally and bypasses that independent-array limitation without shrinking a threshold margin.

This does not establish superiority over interacting memories. Their prior capability is directly relevant:

| Ordinary operation | Actual source scope | Consequence for this candidate |
|---|---|---|
| McClelland and Atmaja, 2006 electromechanical shift registers | Single-electrode actuation of interacting bistable levers; a working laboratory-scale model and modeled submicron designs; a broadcasting write/shift scheme and initialization discussed | Broad one-input mechanical nonvolatile writing is prior art, not a new capability supplied here |
| Mansell et al., 2017 magnetic shift register | Demonstrated 16 discrete elements under a symmetric scalar magnetic field, including field-coupled data injection | A scalar field and serial commands are not by themselves a novel operation; their spatial material implementation is a strong incumbent |
| Mei and Chen, 2023 mechanical in-memory computing | Experimental buckled-beam memories, shift-register interaction, and computing structures driven by force clocks | Mechanical memory and serial-to-parallel state transfer are established; the exact control and data ports must be compared |
| Paulsen, 2026 interacting mechanical hysterons | Springs and rotors with tunable interaction signs, including a global-drive antiferromagnetic domain-wall counter | The counter primitive and its physical platform are established; the present contribution is the specific energy-level write/reset composition, with priority unknown |

These are independently published earlier operations, not hypothetical ordinary researchers being allowed to copy a newly supplied proof. Their existence defeats an inflated generic claim while leaving the exact construction's historical priority unresolved.

The strongest 2006 source explicitly describes distinguishing broadcast write pulses from shift pulses through a special first element. The retrieved material does not supply a matched energy, tolerance, and loading dataset for a quantitative comparison with this construction. No numerical advantage over it is inferred. [IBM primary publication page](https://research.ibm.com/publications/molded-electromechanical-shift-register-memories), [authors' AVS 2006 abstract](https://www.avsconferences.org/AVS2006/Sessions/Schedule/14459).

The 2017 paper establishes its measured shift operation and also reports lithographic variation as a limit to longer chains. The exact constant-margin model here does not eliminate actual fabrication variation or supply a fabricated improvement. [Mansell et al., Nanotechnology 28, 385201](https://doi.org/10.1088/1361-6528/aa7f63).

The mechanical computing and domain-wall components are credited to their original authors. [Mei and Chen, Nature Communications 14, 5204](https://doi.org/10.1038/s41467-023-40989-1), [Paulsen, Nature Communications 17, 2799](https://doi.org/10.1038/s41467-026-70913-2).

## Full costs expose the remaining gap

Let `p_old` and `p_new` count ones in the old and new words. The exact quasistatic hard-stop model gives

\[
\#\text{flips}=10N+4+p_{old}+p_{new},
\]

\[
W_{net}=452N+200+26(p_{old}+p_{new})
\]

in normalized energy units. All completed words at `H=0` have equal energy. This full rewrite cost includes reset of the old word, temporary writing and clearing of every memory, and reset/arming of the auxiliary layer. It assumes ideal recovery of source work returned by the device.

Without recovery, the positive part of work in this specified unbalanced source convention can be quadratic:

\[
W_+(0^N\to1^N)=88N^2+856N+348,
\qquad W_+(1^N\to0^N)=60N^2+850N+348.
\]

These are actual computed and analytically counted costs for the declared source convention, not measured actuator energy. Source balancing or a different energy-storage circuit changes the positive-part bookkeeping and must be supplied physically. Linear ideal net hysteresis does not establish linear wall-plug work.

The uniform scalar field is another supplied input. As one concrete mechanical-bus check, suppose an end-driven elastic rod carries `N` stations at pitch `ell`, each with a possible force load `f`. Its worst end-to-end sag is

\[
\Delta H=\frac{f\ell}{EA}\sum_{j=1}^N j
=\frac{f\ell N(N+1)}{2EA}.
\]

Keeping sag below a fixed fraction of the switching margin in that geometry requires axial rigidity `EA` proportional to `N^2`; with fixed material modulus and pitch, the bus volume can grow as `N^3`. This is a conditional example, not a lower bound on every broadcast geometry. It prevents a uniform mathematical `H` from silently becoming a free mechanical input. A different field, distributed drive, folded layout, balancing scheme, or hierarchical bus needs its own cost and interface.

The physical realization also needs stable finite wells, damping, actuator force and rate limits, spatially resolved output under useful service load, manufacturing tolerance, and a readout contract. None was acquired or experimentally measured. Interactions and negative local stiffness are represented by an explicit passive energy decomposition, but that is not a manufactured linkage with a measured constitutive law.

## Finite compliance and thermal fidelity

The root constructed a companion finite-compliance continuation after reading the energy and local certificates. It adds finite quartic wall potentials and ten event holds, giving nineteen fixed field levels and a bounded-time overdamped gradient realization. Its arithmetic and local inequalities were checked independently in this context. [Finite-compliance construction](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/parent/SOFT_STOP_EMBEDDING.md).

This closes the reliance on perfectly rigid stops at that deterministic model scope. It does not acquire a material or broadcast bus. Its holds and finite movement of other coordinates change the work. The hard-stop work formulas above do not transfer to it; finite-rate compliance losses over `N` cells and `O(N)` clocks can be quadratic. Increasing clock duration can trade energy loss against time, which is also a charged resource.

Constant deterministic force margins are distinct from whole-array thermal reliability. Under a separately justified activated-escape bound `p <= A exp(-DeltaE/kBT)` for each of `M` opportunities, the union bound requires

\[
\Delta E\ge k_BT\log(AM/\epsilon)
\]

to obtain whole-operation failure at most `epsilon`. For `M` proportional to `N^2`, this sufficient bound needs logarithmic barrier growth. Neither the attempt factor nor the minimum collective escape barrier was acquired. A single-coordinate barrier must not be substituted for the coupled escape path. No finite-temperature global-success guarantee is claimed.

## Verification and provenance

The exact rational event solver in [network.py](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/network.py) records reciprocal energy drops and work balance. [check_construction.py](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/check_construction.py) completed:

- all 126 target words for `N=1,...,6`;
- 252 old-word/new-word/order cases for `N<=3`, using three relaxation orders;
- 154 local certificates including the full continuous box of intended coordinates;
- resource traces through `N=32`.

All tests passed. All 252 stored canonical rewrite work balances equal the analytical formula, including the deliberately retained `1e-9` event overshoot. [CHECKS.json](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/CHECKS.json), [RESULT.json](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/RESULT.json), [example 10110](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/alternative/fresh_capability_question_20261027/broadcast_bistable_programming_20261027/EXAMPLE_10110.json). The general result follows from the proof's local inequalities and induction; finite tests alone would not establish it.

Task-first Astra intake was pinned at `f9558b967f5014eced96f229cf89cc4aa7f3490b`. It read the start file, selected mechanics/control and retained-writing topic routes, and packet `N821`. That packet concerns phase-selective crystal rewriting, not the present state-programming operation; it supplied no scientific premise. No whole archive or active sibling result was read before seed lock. The physical spring/rotor and shift-register comparisons came from primary author/publisher sources.

The IBM full paper was not accessible through the available public page tool; its author-hosted publication abstract and authored conference abstract were read. The IOP PDF request returned a non-PDF response; primary abstract and publisher-indexed full-text passages were read instead. These access limits are preserved in the source ledger. Firecrawl was not retried.

## Endpoint

The locked question has a constructive answer **inside the declared energy model**, including reset, reciprocity, and constant deterministic margins for every `N`. The parent continuation supplies a finite-compliance model version. The result does not establish that humanity lacked single-drive material memory, that this particular composition is historically new, or that a useful loaded device is better than ordinary mechanical, electromechanical, or magnetic memory. The civilization-level mission remains **NOT_ACHIEVED** at this endpoint.
