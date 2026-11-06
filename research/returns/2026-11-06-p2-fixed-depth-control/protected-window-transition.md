# Growing-depth failure and the protected transition still missing

The fixed-depth conjugation in the [complete P2 return](P2_FIXED_DEPTH_CONTROL_20261106_RETURN.txt) cannot simply be applied to a growing universal computation.

Take the nearest-neighbour CNOT chain `C=C_m…C_1`, `C_j=CNOT_(j−1→j)`. One old flag controls an initial `X₀`, while later CNOT flags are already set. Then `W(0)=C`, `W(1)=CX₀`, so repairing the flag requires `W(1)W(0)†=CX₀C†=X₀X₁…X_m`. As an atomic attempt attached to the old flag it has unbounded range. A local control fault at a final controlled`Z_m` similarly produces `C†Z_m C=Z₀Z₁…Z_m` in the frame description. Constant support/source enlargement is lost when depth grows.

These are explicit failures of **whole-computation conjugation**, not a general autonomous-computation impossibility. Local communication and protected intermediate operations may still implement what is required, but must be constructed and charged. A fixed frame also obeys `W(p_m)W(p_0)†=I` on every closed controller walk. Cycling the same flags therefore cannot accumulate computation by this mechanism: the cancellation that makes repair safe cancels closed-cycle work. A protected frame change, another protected data operation or a different representation is required.

Simply dividing a circuit into fixed-depth windows leaves a substantive physical obligation. The device must preserve completed logical action while clearing/reusing old flags; an uncompensated reset is not the safe repair map. If the window is complete, leaving data untouched during a frame change can retain the intended gate; if only partial, it retains a partial gate. Resetting flags at different times also changes the intermediate code seen by recovery. A completion bit alone proves neither safe reset nor ongoing recovery.

The missing operation must therefore:

- Physically transition between protected quantum frames while retaining the unknown reference-entangled state.
- Contain damaged-controller effects during waiting and repair, with recovery valid through intermediate states.
- Finish under a good event defined from the actual burst source and primitive attempts, with progress and all installed exposure/costs paid.

The source explicitly does not provide that operation, the initial unknown-input acquisition/encoding, scalable autonomous memory/controller progress, or protected measurement and an installed classical receiver. Its earlier exact support-wise CPTP/history transfer can transport a valid certificate; it does not construct the certificate, correctness event or progress. The projective/sharp output criterion and general-POVM counterexample retain their original conditions.

Dünnweber–Styliaris–Trivedi's cited continuous-time development and Gács's detailed classical consistency/healing machinery do not close these quantum physical side effects merely by citation. Capital adds no synchronizer, assumed valid interleaving, finite-test-to-threshold inference or stronger passive-memory claim.

Finite examples in the return check channel algebra and CNOT-chain/Pareto arithmetic. They do not establish protected idles throughout arbitrary controller repair or close the global north-star theorem. No code replay, external source acquisition, new review or processor build was performed for this publication.
