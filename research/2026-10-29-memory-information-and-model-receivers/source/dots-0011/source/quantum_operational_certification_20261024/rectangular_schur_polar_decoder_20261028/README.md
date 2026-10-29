# Rectangular low-defect Schur polar decoder

28 October2026. Author construction awaiting independent review. Original earlier Astra and external sources unchanged.

The new bridge is explicit polynomial access to the FULL orthogonal reference-error frame for lambda=mu=(k/2,k/2), selected environmental sectors(k) and(k−2,2). Identity plus known transposition circuits span exactly this space; a polynomial-size Gram matrix has an explicit order-one nonzero eigenvalue. No Clebsch–Gordan oracle, dense exponential matrix, or unknown reference-channel simulator is supplied.

A bounded positive soft-polar polynomial gives total CPTP recovery with a fallback flag. It avoids a smallest-singular-value promise and retains a constant-factor mean Gram-defect bound. Code-isometry circuit access and any approximate-design moment-error guarantee are separate premises. The construction concerns a special finite-copy Schur regime, not general mixed-source coherent-information rates or arbitrary retained memory.

`GOVERNING_DECODER_v1.md` supplies representation, normalization, implementation and risk derivations. `rectangular_frame_check_v1.py` checks Young-orthogonal fixtures k4..16 and scalar filter inequalities. Its dense numerical random-code fixture is only a diagnostic, NOT the efficient code circuit or an executed QSVT circuit. Run with `OPENBLAS_NUM_THREADS=1 python rectangular_frame_check_v1.py`.

What remains: independent review; actual circuit synthesis/error budget; useful source probability/yield of the selected local/environmental sectors; extension to nonrectangular multiplicities or growing-defect environment sectors. Do not label this the full universal decoder. The central primary comparison is Rizzo et al., arXiv2609.38038v1; their open efficient polar-decoder question motivated this construction. Standard QSVT and conventional representation circuits are credited.
