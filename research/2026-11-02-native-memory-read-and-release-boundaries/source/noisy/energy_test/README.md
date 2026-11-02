# Preparation-energy physical-resource test

**Result:** a constructive driven, exactly reference-charge-conserving attack, not just a failed robustness bound.

Read `CONSTRUCTIVE_ATTACK.md` for the complete protocol and caveats. `check_buffer.py` / `check_buffer.txt` independently check the equal-rate virtual-source inversion and finite-size invariant battery distribution.

Core chain: independent Pauli noise creates an inverted *virtual* transition → polynomial supply of fresh mixed bath groups pumps an O(log n) unary work buffer → a one-bit reversible flag enables each energy-resolved code Pauli exactly once → a known logical-Pauli path succeeds with probability 1−o(1), conditioned on a polynomial-probability thermal workspace branch. This yields unconditional decoded logical error n^−O(1) in polynomial time.

No extensive clean battery, clean entropy sink, postselection, energy-injecting control, or global thermal permutation is assumed. Initial bath size, spent bath, routing carriers, bounded-strength pulses, and routing time are polynomial. Time-dependent scheduling is explicitly used; no autonomous extension is claimed.

Remaining checks against the parent theorem: actual CSS energy commensurability; contact-port geometry; exact bath/control quantifiers; operational decoder covariance; any preassigned strict gap/body caps. A statement covering the explicitly constructed species and energy-resolved primitives cannot retain stretched-exponentially small worst-case failure after this preparation noise.

**Stronger addendum:** `FIXED_GAP_FIXED_BODY_SOURCE.md` proves the fixed-gap set {0,Δ,2Δ} suffices for every fixed common bath flip rate q>0. A composite virtual source is compiled into four-body-or-smaller exact-K gates using reusable zero-energy predicate scratch. This removes q-dependent native-arity and high-onsite-gap caveats. `check_fixed_gap.py` verifies the inversion numerically and exhaustively verifies the m=2 compiled swap truth table.
