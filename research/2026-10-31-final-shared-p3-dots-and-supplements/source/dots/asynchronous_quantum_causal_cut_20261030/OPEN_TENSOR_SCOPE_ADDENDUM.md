# Scope precision for the independently reviewed open-tensor lemma

2026-10-30. This does not mutate OPEN_TENSOR_CORRECTNESS_V1.md, whose reviewed SHA256 begins 598e20f6.

The full amplitude premise must cover the ENTIRE local hole space, including every input/output, dilation, measurement-record and classical-control port needed to span each rectangular hole, and every allowed syndrome/ancillary input. Data-only fault correctness or fixed-ancilla marginal correctness is insufficient.

The receiver derivation from extremality is safest for a logical UNITARY target and independent syndrome processing. For a genuinely nonunitary logical target, merely selecting a Stinespring dilation does not prove the common-isometry identity (2.1). Such an identity must be independently earned for the actual retained interface, including its intended logical outcome registers. The abstract tensor lemma remains valid whenever that stronger premise is proved.

The [[5,1,3]] diagnostic verifies an ideal recovery-cut factorization, not a native fault-tolerant gadget.

Independent review: producer-workspace/INDEPENDENT_REVIEW.md, SHA256 4639f780239e8865b48e2c6853d45b6cb5601f60950ab02d5832617914506168. Its scoped PASS includes the same qualifications and makes no architecture promotion.
