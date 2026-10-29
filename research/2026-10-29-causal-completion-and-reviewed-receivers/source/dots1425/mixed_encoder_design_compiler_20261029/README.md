# Finite common-design compiler
Current preferred proof: BOX_MULLER_FINITE_COMPILER_DRAFT.md, with PADDING_AND_SCHUR_DEPENDENCY.md and FINITE_SCALAR_ARITHMETIC_ADDENDUM.md. Their separate hash manifests are immutable inputs to receiving review. Consult producer-workspace/box_muller_design_compiler_audit_20261029 for actual acceptance status; this README itself is not a review receipt.

The proof implements the established BHH common-design construction with finite scalar randomness/arithmetic, replacing the earlier fixed-d GT uniform-state enumeration by one highest-weight state plus common twirling. It retains full quantum storage/control costs and huge theorem constants. check_box_muller.py/json are coupled high-precision diagnostics and exact parameter checks, not a certified interval implementation or full decoder run.

PRIMARY_TRANSFER_DRAFT.md is the earlier source/obligation note. FINITE_HAAR4_COMPILER_DRAFT.md is a slower rational Gaussian-grid fallback proposal, superseded as the preferred route and not separately received. Neither should override the Box–Muller governing contract or be mistaken for the current accepted scope.
