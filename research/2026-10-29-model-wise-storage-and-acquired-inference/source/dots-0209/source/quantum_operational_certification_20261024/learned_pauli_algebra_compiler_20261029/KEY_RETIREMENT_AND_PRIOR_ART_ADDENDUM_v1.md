# Key-retirement clarification and nearest prior-art boundary
2026-10-29. Addendum; does not alter frozen governing proofs.

## Key isolation is permanent for the assessed execution
For PRIVATE_PAD_PAYLOAD_INSTRUMENT_v1.md, fresh private pad keys must remain inaccessible to the source throughout every later interaction, not merely during their own source call. They are retired after trusted inverse-pad control and excluded from all later source-visible records. If a source swaps an initially unprotected physical payload qubit into its memory, it may hold the encrypted payload K|psi>. Later revealing K would give it information not represented by the averaged key-retired instrument. Thus permanent key isolation/retirement and no later control side channel are part of the theorem interface. The single-call averaged formula is insufficient to justify composition if later operations depend on leaked keys. No joint-distance claim including retained key records is made.

## Direct prior-art comparator
Silva, Magesan, Kribs, Emerson, “Scalable protocol for identification of correctable codes,” Phys.Rev.A78,012347(2008), arXiv0710.1900. Full primary manuscript inspected2026-10-29:
https://www.math.uwaterloo.ca/~jemerson/papers/SilvaEtAlPhysRevA08.pdf

SectionII proves exact-correctability transfer from a twirled channel to its original channel. SectionsIII/VI use permutation-invariant Pauli characterization and Pauli commutation structure to find Clifford encodings without dense operator matrices. This is a direct antecedent to task-specific partial-noise acquisition and algebraic code discovery. Consequently those broad ideas are not claimed new here. The current load-bearing bridge instead concerns actual retained-memory instruments, private roles, finite innovation accounting, and an explicitly controlled direct-payload/outer-code composition. Whether that full combination is historically novel remains unreviewed. Known ingredients must not be relabelled as a foundational discovery merely because a finite implementation was written.
