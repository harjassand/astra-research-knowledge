# Controlling source-branch qualification

31 October 2026. This addendum corrects the wording of Section 1 of `FINITE_RATE_COHERENT_ERASER_CANDIDATE.md`; its frozen bytes are preserved for audit continuity.

The sentence “Its source marginal is the ordinary driven damped qubit; downstream coupling does not change it” is to be read instead as:

> The upstream **joint source–data marginal** evolves under its own source–data generator, unaffected by the downstream cascaded cavity. **Conditioned on a fixed data-Z eigenbranch**, its source state is the ordinary driven damped qubit with the corresponding sign of the drive. For a general data superposition, the unconditional source marginal is not, in general, a single driven-qubit state: it is a mixture of the two opposite-drive branch marginals.

All p, y, s, beta, D and incoherent-photon quantities in Section 3 refer to the explicitly fixed Z_d=+1 branch. Its opposite branch follows by the exact source-Z / field-parity symmetry stated there. In particular, the branch field mean is not to be replaced by the unconditional source mean for a superposed data input. The common-branch initialized-isometry argument, exact coherent projection, variance bound, and source excitation envelope remain as stated. No numerical certificate or code changes are required by this wording correction.

The previous 13-file candidate manifest, SHA256 `2e40e9b9f7c27eadbeb2c5d8d5953a260ccb8e13d642151f2e7f9f75b0198fbe`, is retained as `MANIFEST_PRE_BRANCH_QUALIFICATION.json`. The current manifest adds this controlling qualification, binds that prior manifest, and verifies every previously bound file is byte-for-byte unchanged.
