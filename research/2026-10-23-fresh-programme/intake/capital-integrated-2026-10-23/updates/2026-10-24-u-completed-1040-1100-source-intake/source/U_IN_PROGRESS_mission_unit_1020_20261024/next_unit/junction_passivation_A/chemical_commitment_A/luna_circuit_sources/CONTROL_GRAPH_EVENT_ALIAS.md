# Control-graph check: donor unloading aliases transfer completion

**Result.** At the DNA-domain/control-graph level specified by Bath and Turberfield, hydrolysis followed by binding of the same downstream adaptor reaches the same “donor 3′-OH + next adaptor bound” state as successful transfer. The blocker/primer actuator therefore records donor unloading, not whether the growing chain was transferred onto the intended building block.

The counteredge is literal in the proposed chemistry:

```text
Transfer:  D–O–C(O)–P + H2N–B–C(O)–O–A  → D–OH + P–C(O)–NH–B–C(O)–O–A
Hydrolysis: D–O–C(O)–P + H2O            → D–OH + P–C(O)–OH
           H2N–B–C(O)–O–A remains available
```

After the *same* adaptor `A` occupies the next instruction in either branch, `D` has the same 3′-OH primer, and the same adaptor/blocker competition domains are present. The proposed sequence—expose the primer, extend with strand-displacing polymerase, remove the blocker, expose the next instruction—can therefore proceed along the same DNA control edges in the hydrolysis branch. No DNA-level edge in this mechanism checks the new `P–B` bond.

This is a graph-level alias, not a claim of identical microscopic states or rates. The transferred polymer changes the payload on `A`; it could alter binding, geometry, steric access, or enzyme kinetics. Such a payload-sensitive effect would be an additional discriminator and is unmeasured here. The cited source presents the transfer chemistry as future work; its Fig. 5 polymerase/blocker test uses a truncated downstream adaptor without the parallel-duplex domain, and does not demonstrate coupled transfer or product-order fidelity.

**Primary source:** Bath & Turberfield, “Mechanism for a molecular assembler of sequence-controlled polymers using parallel DNA and a DNA polymerase,” *Nanoscale Horizons* 11 (2026), 549–554, [DOI: 10.1039/D5NH00505A](https://doi.org/10.1039/D5NH00505A). The official RSC indexed main text describes a checkpoint based on the 3′-OH revealed after transfer, but also states that transfer chemistry remains future work and describes preliminary aminoacylation and use of adaptors as primers after hydrolysis.
