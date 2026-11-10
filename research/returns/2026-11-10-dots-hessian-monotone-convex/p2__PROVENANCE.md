# Provenance and limits

Date: 9 November 2026.

- Reviewed theorem source: SHA256 70867bc2137841c0005f8876d073f1396149dbe09fc7ddd0a3619c143d86afaa.
- Complete independent review: SHA256 40ae6feedb4dc44e53db696b0417843f324aed5665519720f1fe534cedc89381.
- Corrected independent exact checker, copied without changes into this packet: SHA256 8af615d47b1b29c20375f2e3652c4efb80e0d277215e018ddb5b680208d607b1.
- First checker source: SHA256 729f9062315bc06ed381aa2f7532ffdee4048f5307ac4506ad3db2a856a871fa. It reached final JSON output, which rejected SymPy BooleanTrue values. The corrected source changes only their serialization to Python bool; it does not change mathematical tests. Both original source and failure output remain preserved in the research record.

THEOREM_AND_PROOF.md is a standalone reader edition of the reviewed theorem. It supplies the original J_1 normalization explicitly, expands the first two principal-minor proof, and includes the complete coarse-reserve bound instead of referring to the earlier diagonal special case. These additions are exactly the independently reconstructed arguments in the review. No theorem assumption, coefficient, translator, Gram matrix, numerical constant or conclusion was changed.

INDEPENDENT_REVIEW.md retains the entire mathematical analysis and verdict. Coordination details were removed and checker filenames were made local to this packet. This editorial preparation is not presented as another independent review.

The successful exact receipt reports 1.092180251 seconds, Python 3.12.14 and SymPy 1.14.0. This is a reproduction cost, not a performance or hardware claim. The algebraic identities and analytic PSD arguments, not numerical examples, support the theorem.

No claim of historical novelty is made. The result is a direct certificate for this original anisotropic quartic and this adapted scalar-potential class. It is not full J_r quasiconvexity, an arbitrary-vector-field theorem, or an all-r result. The earlier fixed-contact theorem and its packet remain unchanged.
