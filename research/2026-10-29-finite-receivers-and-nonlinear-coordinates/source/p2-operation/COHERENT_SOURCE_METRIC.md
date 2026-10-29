# Exact source-only norm for the coherent-memory example

Author `/root`. This follow-up is separate from the pinned memory-fault theorem; its independent review is recorded with the coherent-memory extension.

Use the Bell-eraser model in `reviews/memory_faults/COHERENT_RECORD_EXTENSION.md`, with E=exp(-i theta Q), Q=Z_1, c=4/5 and s=3/5. After Bell feedback the actual instrument is the common Bell receiver following exp(-i theta Z_x tensor Q); its baseline follows exp(-i theta I tensor Q). Trace every receiver output and record. The resulting maps take the joint source/environment input to the source. No field-independent source channel is assumed.

Write a joint density operator in source-x blocks rho_ab, with source z and arbitrary references included inside each block. Diagonal output blocks equal the baseline. The off-diagonal difference is

\[
A=\operatorname{Tr}_E[(e^{-2i\theta Q}-I)\rho_{01}].
\]

Trace-norm duality, including any reference extension, gives

\[
\|A\|_1\leq\|e^{-2i\theta Q}-I\|\|\rho_{01}\|_1
\leq2\sin\theta\sqrt{\operatorname{Tr}\rho_{00}\operatorname{Tr}\rho_{11}}
\leq\sin\theta.
\]

The dual operator is a tensor product of a reference contraction and the field operator, so arbitrary references do not change this bound. The source difference has Hermitian blocks [[0,A],[A*,0]], whose half trace norm is ||A||_1. This proves the universal source-only upper bound sin(theta) for arbitrary initial correlations.

A Q eigenstate and source x in |+> give the source rotation diag(e^-i theta,e^i theta), saturating the bound. Thus the exact universal source-only half-diamond distance from the receiver-traced common-input baseline is 3/5. It is the norm of a map on the joint input, not one source channel for all field states.

The separately proved complete-record distance in the same model is 24/25. These are exact norms for different output interfaces. The false classical Pauli replacement predicts 9/25. Additional acquired corrective controls could change these prescribed-protocol performances.
