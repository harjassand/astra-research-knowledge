# Preserved failed check and scope correction

1. orbit_frame_check_v1.py correctly constructed the Parseval frame, but its independent FULL Hom target used only the central transposition sum. At k6, distinct low/high-defect shapes can have equal content sums, causing the comparison assertion to fail. This was a defect in the independent-target construction, not a repaired scientific frame. v1 remains preserved. v2 uses full joint Jucys–Murphy decomposition for the target and all five fixtures pass. The actual general projector algorithm already requires full joint decomposition.
2. OPERATIONAL_SCOPE_ADDENDUM_v2.md records the separate N=0 selected-image case. Having nonzero H-seeds alone does not guarantee a nonempty selected reference. The decoder still has a total fallback.
