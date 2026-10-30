# Full-Hilbert no-creation theorem for repaired multi-lock history defects
Date: 2026-10-29. Uses exactly REPAIRED_GENERATOR.md. Not a data-fault threshold.

## Definition
Fix a simultaneous hub-phase/lock-label configuration c. Let chi_h(c) be its owner-h clock consistency predicate; chi_h=0 for abort labels. Let Pi_h^0=I_data⊗|0><0|_(W_h), and V_(h,t)=U_(h,t)...U_(h,1). Define the clean projector on that clock block by

P_h(c)=0 if chi_h(c)=0;
P_h(c)=Pi_h^0 in A or Q phases;
P_h(c)=V_(h,t) Pi_h^0 V_(h,t)† in G_t.

Define B_h as the direct sum over all clock configurations of I−P_h(c). These are bounded-support projectors on hub h and its fixed resource neighborhood. They are defined on the ENTIRE physical Hilbert space, not just legal trajectories. 'Good' means consistency with an arbitrary underlying data state and clean workspace history; it does NOT mean that underlying data state is logically correct.

## 1. The B_h commute
Work blockwise in c. If h is clock-inconsistent, B_h=I. Otherwise an A/Q projector acts only on its private workspace. If both h and k are consistent G-phase hubs, every resource in each support must carry its exact owner tag. Their supports cannot overlap, since one lock cannot carry both tags. Thus their data/workspace projectors have disjoint support. This proves pairwise commutation for arbitrary configurations and arbitrary coherent data/workspace states.

Private hub workspaces are NOT data resources available to other hubs. This architectural assumption is essential to the argument and is explicit in the generator.

## 2. Every Hamiltonian term commutes with every B_h
For an edge of the clock transition graph with payload unitary U, the precise block condition is P_h(c') U=U P_h(c).

Acquisition/unacquisition changes an exactly free lock to/from its exact owner tag and changes the matching prefix count. The owner's consistency truth value is identical on both ends; A-phase history is the same workspace-zero projector. For another owner k, both lock labels are non-k labels. Its consistency and workspace/history conditions are unchanged, or its required k tag makes both blocks inconsistent. Therefore all P_k intertwine.

A gate of owner h preserves its clock-consistency truth value. On consistent blocks it maps the prefix history projector by U; on inconsistent blocks P_h=0 on both ends. For another consistent executing owner k, if the target is in R_k, k requires tag o_k while the physical h-gate requires o_h, so the entire gate block vanishes there. Otherwise the payload gate is disjoint from k's workspace/data support. A/Q projectors of k use only private W_k. **This is exactly where the ownership projector on every gate is required.** Omitting it invalidates the theorem.

Verification adds/removes a condition that is known true on its transition edge; Q history projectors are unchanged. Cleanup o_h↔z_h operates only where h does not claim that resource: both labels are inconsistent in an unexpected/verified-prefix position, or both permitted in an unverified Q suffix. Thus its owner's consistency is unchanged, and all other owners see two equally non-own labels.

Abort coupling has an inconsistent original phase on one side and an abort label on the other, so P_h=0 on both sides. It changes no resource tag or payload, and acts only on private W_h, trivially on that workspace; other owners' projectors commute.

Finally, position/lock-label monitor couplings are block-diagonal and workspace-blind, hence commute with every B_h. These facts prove [H,B_h]=0 and [H,product_(h∈S)B_h]=0 for every finite S.

## 3. Resets cannot create any owner defect, including joint products
Every label-resolved physical reset maps the good subspace of each owner into that owner's good subspace (or annihilates that source branch):
- terminal/abort reset sets its private workspace to0 and enters Q0, which is clock-consistent for any remaining lock configuration;
- Qk→A0 preserves the predicate 'no own o/z anywhere'; if that predicate fails, the owner was already inconsistent;
- lock z_h→f can only remove a clock inconsistency of h or leave it unchanged. It cannot turn a consistent required-owned position into a missing one, because z_h was already not the required o_h;
- A/Q workspace refresh resets exactly the projector whose complement is the good-clock history defect;
- other owners cannot have their data/workspaces altered by these resets, and their clock predicates are unchanged under another owner's cleanup label→free.

Formally, for each reset channel J from clock block c to c',
B_h(c') J P_h(c)=0.
Because the B commute, for B_S=product_(h∈S)B_h this gives
B_S(c') J (I−B_S(c))=0.
For the declared complete instruments, the summed J†J is scalar on the relevant workspace (and clock-diagonal), so it commutes with B_S. Thus each reset generator obeys D_reset*(B_S)≤0. Terminal syndrome rates must be uniform, and syndrome channels must remain separately resolved, as specified; replacing them by one coherent sum or arbitrary unequal losses would not be the same theorem.

Combining with the Hamiltonian result gives the full-Hilbert operator inequality

L_clean*(B_S)≤0  for every finite owner set S.

Hence T_t*(B_S)≤B_S for all t≥0. This is exact no-creation, including coherent superpositions between clock sectors and reference entanglement.

## 4. Finite-rate healing paths
A clock-inconsistent ordinary phase has at least one definite violated local test after the finite-rate clock monitor's projection. Its path is phase→distinct abort R_(p,j)→Q0; an initial abort needs only its reset.

A clock-consistent dirty A/Q phase is a nonzero-workspace state and can refresh directly. A clock-consistent dirty G_t has all resources already owned. Reversing its t gates maps its dirty-history projector exactly to the nonzero-workspace projector at A_k. Refresh then removes it. No resource acquisition, neighboring progress, or rollback wait chain is needed for this defect-healing path. The maximum number of selected steps is max(2,L+1).

The finite-rate, label-resolved reset-monitor proof supplied by the scheduling worker turns these paths into a volume-independent operator contraction T_T*(B_h)≤(1−c)B_h for fixed T,c>0. This step relies on its explicit monitor/no-jump assumptions and is documented separately, rather than inferred from graph reachability alone. It yields exponential decay of bad-weight/test probability, not automatically a classical first-healing-time process for unmeasured coherent evolution.

## 5. Regression evidence
- `check_all_clock_flags.py`: all22,680 arbitrary clock states for two overlapping supports,141,561 directed transitions; all Hamiltonian edges preserve both Boolean owner flags, all resets only decrease them.
- `check_quantum_history_flags.py`: non-permutation Hadamard prefixes plus an overlapping reset+X recovery. All clock states reduce to14 history-projector block types. It checks51 Hamiltonian intertwining types and162 joint-reset range inclusions, using exact dyadic matrix equality. No floating eigenvalue tolerance is used for these identities.

These are regression instances accompanying the general blockwise proof, not claims of experimental realization or a scalable quantum memory.

## Remaining distinction
A reset can clear B_h while leaving errors on its owned data. Thus sparse/healing history defects are a controller-integrity theorem, not a proof that data faults are sparse, that encoded memory survives, or that bare physical data has a desired graph-state syndrome distribution. The multi-gate prefix dressing generally changes bare observables. A data fault-path contract and output/drain/decoding interface remain separate obligations.
