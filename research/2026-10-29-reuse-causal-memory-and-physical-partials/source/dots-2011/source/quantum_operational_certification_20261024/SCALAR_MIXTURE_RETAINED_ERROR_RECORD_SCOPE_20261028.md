# Retained-error-record scope clarification (sources preserved)

28 October 2026. This note does NOT amend the bytes or receipts of the received sources. It makes their exact map assumptions explicit and separates subsequent broader constructions.

The received `ordinary_label_aware_syndrome_memory_acquisition_20261028.md` Part A (source `7ee3c5a23d42ce3d45e00514536ede77cf935ebc17086d1a18b45c9ef29871f0`) defines exactly

    F_f=sum_a w_f(p_a) K_a.

The SAME retained-memory CP map K_a occurs for every subsequently sampled physical bit pattern f in branch a. K_a can have arbitrary coherent memory and depend on prior history. It does NOT include an additional f-dependent retained state update or an appended which-error tag after sampling. A fresh error-sampling environment can be discarded; if that environment becomes future-accessible source memory, this narrower scalar-mixture equality must be checked again. The exact identity is a real physical restriction, not a generic consequence of conditional scalar error probabilities.

Its Part B and the received known-code label lift permit general CP pattern maps F_f but impose CP-positive signed coordinate maps H_i. Fully error-resolved outgoing memory generally violates that stronger CP positivity even when its signed input effect is positive. Those received proofs and their exact premises remain sound; an error-tagged source must not be silently placed inside them merely because its marginal bit-error probability is below 1/2.

Likewise the native inequality sum_bad F_f<=_CP r sum_all F_f follows from a branchwise scalar probability bound only when the same retained K_a multiplies all error probabilities. If F_I(omega)=(1-p)omega tensor |0><0| and F_X(omega)=p omega tensor |1><1|, then the bad effect is pI but the difference r T-F_X has a negative flag block at r=p<1. The corresponding good-minus-(1-p)TOTAL witness is -p(1-p), or -3/16 at p=1/4.

Two separate newer mechanisms address the wider error-tagged setting:

* `ordinary_physical_port_effect_bias_acquisition_20261028.md` audits the SAME finite physical-port calibration algorithm under positive signed INPUT EFFECTS. With trivial emitted gauge, the reduced conditional mean only depends on Tr H_i(omega), so full H_i CP positivity is unnecessary. Consult its own receiving status.
* `common_clean_subchannel_memory_bound_20261028.md` compares service processes through their common all-good CP subchannel under uniform BAD EFFECT bounds, rather than falsely claiming CP domination by id tensor TOTAL. Consult its own receiving status.

The narrow CP-domination identity-module and the broader common-subchannel process bound are different mathematical statements. Their identical-looking scalar process allowances do not make the stronger map-order assertion valid in the broader class. Generic physical implementation discrepancies are additionally paid in complete norm and need not preserve either nominal exact-control CP identity.
