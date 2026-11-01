Unfrozen intermediate fixed-point implementation. Unit checks passed, first3cases
completed. The513D computation was interrupted at21:05UTC with exit130 before a
certificate; no false result or claimed budget failure. Exact division/remainder
by2^P in fixed-point products was replaced by mathematically identical shifts/masks.
A measured20000-product microcheck atP2688 was0.306s fordivmod versus0.098s forshift;
this is an arithmetic diagnostic, not an end-to-end comparison. All final outputs
and receiving tests are regenerated below. Earlier accepted sources unchanged.
