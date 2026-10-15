# Sharp-negative margin: independent partial progress

The unrestricted all-affine fourth-order margin is **UNRESOLVED**. No exact
zero-margin sequence was found. External correctness and priority remain
UNKNOWN. The source pin is b32943eeb62d0d79929a9e572a344219a785ebf9.

The complete construction and proof state is PROOFS.md. New usable results:

1. Triangular periodic gradients with one target component depending on
   one coordinate admit the all-affine margin r/[64(r+2)]>1/64. This permits
   rank-two gradients and is independent of cell aspect ratio. A splitting
   tree of depth N has margin α/(3N³); no claim uniform in N follows.
2. For q=[[p,b],[c,z]], set S=(r+1)p+z,
   m=∫[S²+r(r+2)c²/3], n=||p||4+||c||4+||z||4. The contact cubic obeys
   |∫DJ(q):I|≤C_r sqrt(m)||q||4 n. The proof uses mixed-Hessian
   interpolation ||fxy||_(8/3)²≤C||fxx||2||fyy||4 after an elliptic
   right inverse removes S.
3. Consequently, on a fixed rectangular torus or fixed bounded support,
   ||q_n||4=1 and uniform integrability of |q_n|⁴ imply
   liminf Gap_(t_nI)(φ_n)≥α for |t_n|→∞. Growing exact contact-ray escape
   therefore requires loss of fourth-power uniform integrability.
4. The unique scalar homogeneous quadratic observable whose two derivatives
   lie in the constant reduced-row span is positive definite:
   Q=v-(2r+1)u/3-(10r+8)j/(3r). Its gradient is controlled by the corrected
   density. Four additional directional metric flux identities and strict
   metric-cone separation are saved. These do not supply the target.

Decisive countermodels and limits are explicit. A rotating rank-one
periodic gradient has spatially constant Q at every heat time but positive
fourth energy, so scalar Q alone cannot prove coercivity. Exact concentration
scaling φ_a(x)=a^(-1)φ(a²(x-x0)), B_a=aB preserves both Gap and ∫|Dφ|⁴,
embedding the fixed-background problem into growing backgrounds without
uniform integrability. A fixed-profile anisotropic shear blowup retains
α b⁴ plus a square after its determinant null term is removed.

The analytic auditor independently supports only the triangular theorem,
the cubic estimate and the stated uniform-integrability theorem. A real
R² lemma defect was repaired: D²f∈L4 is required to exclude f=xy. This
stronger hypothesis is already supplied by the cubic proof. The repair and
attribution are preserved in PROOFS.md; exact checks do not adjudicate
analytic proofs. Other sections remain construction results.

The exact executable is check_exact.py. Its output EXACT_CHECKS.json verifies
the quadratic identities, restriction ranks and branch-nonzero minors,
positive-definiteness gap, metric null gaps, cubic expansion, concentration
exponent and soft-shear Laurent coefficient. PROVENANCE.json records the
read-only source hashes and the audit repair. No W/source/Git write was made
by this worker.

Remaining gates: concentrated profiles, affine directions approaching
contact with transverse offsets, and genuinely two-dimensional infinite
hierarchy. No sharp-J storage transfer is authorized by these partial bounds.
