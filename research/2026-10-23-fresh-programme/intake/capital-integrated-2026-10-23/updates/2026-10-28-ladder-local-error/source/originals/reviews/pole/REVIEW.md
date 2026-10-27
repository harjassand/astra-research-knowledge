# Independent review of C16 and C51

Scope: the specified infinite ladder at `g=1/5`, the exact perturbation
`H_eta = H_0 + eta (n_L - n_R)` in the physical two-excitation space,
and local outgoing continuations of the declared pair responses. This is a
manual mathematical review with targeted replay, not a formal-verification
certificate. The source-density construction in S62 is an explicit input;
its normalization, positivity argument, and code were checked here too.

## Case-specific verdicts

* **C16:** The proof contains a substantive outgoing-pole construction, not
  merely an FGR calculation. Subject to the correction below, its bounded
  deformation, exclusion, exact compression, Riesz projection, visible simple
  pole, and even `O(eta^4)` expansion support the asserted local theorem. The
  executed rational interval certificate is load-bearing for its separations.
* **C51:** The proof also contains a substantive outgoing-pole construction.
  Its independent block-monotonicity argument establishes `E<6` and its
  treatment of a possible coincident mixed atom cancels the harmonic pole
  before the physical inverse is evaluated. Its matching argument covers both
  the bare pair and the original dressed-pair response. I found no substantive
  blocker in the local theorem at the declared scope.

These verdicts are based on the operator arguments, not on agreement between
the two files or on their floating-point root results. In both cases, the
conclusion concerns the specified local continuation of matrix elements;
there is no claim of a bounded continuation of the physical resolvent across
the spectrum on the original Hilbert space.

## Checks carrying the verdict

1. The sine-bath family has `phi_t(k)=k+t sin(k)` and uses the same analytic
   transformed form factor in both off-diagonal entries. It is bounded and
   holomorphic for `|t|<1`; for real `t` it is the stated unitary change of
   variables, fixing `LL`, `RR`, and `LR`. Second quantization and the
   two-forbidden-state compression give the full detuned hard-core model,
   with the physical perturbation norm one. No analytic continuation of an
   arbitrary `L^2` composition operator is needed. The transpose bilinear
   form, not a deformation-dependent Hermitian conjugate, is appropriate.
2. For the lowered contours, the bath energies have strictly negative
   imaginary part away from their endpoints. The deformed one-body Schur
   equation gives only the two displayed real candidates per channel; the
   physical square-root branch eliminates one each, leaving the two gap atoms.
   The bounded tensor-sum resolvent inclusion then excludes the pair energy
   from the deformed harmonic spectrum, apart from the mixed atom that C51
   explicitly handles. The mixed two-band endpoint at 6 must be excluded.
3. C16's exact interval computation establishes `5.9785 < E < 5.97865 < 6`
   and `5.97931529997724990766 < E_+ + E_- < 5.97931529997724990767`.
   Its integer-square-root enclosures, Machin pi bracket, interval Riemann
   cells, atom masses, and off-band resolvent interval denominators were
   inspected; the executed assertions reproduce the signs at both root
   brackets. These are interval claims; the decimal density is not.
4. In C51, at energy six the upper-channel bath blocks yield
   `L_+(6;kappa)=-1/(2 kappa s_b(kappa))` with a positive, nondecreasing
   `s_b`, and spectral reflection relates the lower channel to the upper.
   Hence unequal couplings `2/25 > 1/25` give `L_+(6)+L_-(6)>0`, and the
   strictly increasing root lies below six. If the mixed atom equals E, the
   rank-one principal part cancels completely in the exact odd compression;
   the removable singularity then gives the odd physical inverse. At the
   fixed g, C16's certificate additionally rules out that coincidence.
5. At eta zero, the even forbidden resolvent has a simple zero with derivative
   `D/2>0`, and the odd compressed inverse exists at E. The simple pole's
   residue is nonzero in `|LR>`; it is `2 L_+(E)^2 / D` or equivalently
   `-2 L_+(E)L_-(E)/D`. The transpose-normalized deformed pair has residue
   one in its own response. A fixed isolating contour, the Neumann bound and
   a rank-one Riesz projection produce the actual analytic eigenvalue branch;
   parity makes it even. The resolvent-defined positive radii and Cauchy
   remainder bounds are legitimate existence statements, with unevaluated
   constants.
6. Real-parameter unitarity followed by analytic continuation along the
   resolvent path matches the deformed response to the physical
   upper-half-plane germ. C51 applies this also to the analytically deformed
   pair vector. The odd source is the full dressed `V psi`, including the
   bosonic factor and both spectral atoms. The exact rank-one compression is
   `s(z)=(2/D)(F-J^2/M)`. Differentiating the actual simple eigenvalue gives
   `lambda_2=-s(E+i0)`; S62's nonconstant shell source proves
   `Im s(E+i0)=pi rho(E)>0`. Thus the sign and `O(eta^4)` are conclusions of
   the pole construction, not assumed golden-rule rules.

## Errors, qualifications, and remaining work

* **C16, PROOF.md lines 153–158:** the displayed derivative of
  `Re(c-cos(k-i t sin k))` has the wrong sign on its second term. The correct
  derivative is `sin(k) cosh(t sin(k)) - t cos(k)^2 sinh(t sin(k))`.
  For `0<t<1`, the inequality `tanh(u)<=u` proves it is at least
  `sin(k) cosh(t sin(k)) (1-t^2 cos(k)^2)>0`. Thus the claimed monotonicity
  is true, but the frozen displayed formula needs correction. As an independent
  point check at `k=pi/4,t=0.1`, the centered numerical derivative is
  `0.7053368041`, the correct formula `0.7053368039`, and the printed formula
  `0.7124137658`.
* C16 lines 443–446 should be read with the usual Schur-complement domain:
  the third eta bound makes the *harmonic* inverse exist throughout the disk,
  while equation (9) as an inverse identity requires its Schur matrix to be
  invertible; at the physical pole the identity is meromorphic. The later
  pole argument and C51's criterion make this restriction clear.
* Neither proof computes a positive numerical lower bound for its detuning
  radius, the norm constants, or a validated numerical error on the density.
  The reported contour roots are floating-point, seeded using the density and
  fixed pair energy, and are not proven to lie inside the qualitative eta
  radius. They are diagnostics only. No lifetime, time-domain survival law,
  physical realization, or practical advantage follows from this review.

## Independent executions and source exposure

All executions used copies below this review directory. Frozen proof and
script hashes in C16, C51 and S62 match their copied manifests; the replayed
C16 certificate output changes its recorded elapsed time in the copy only.

* `replay_c16_separation.log`: 1024-cell exact-rational interval replay,
  successful assertions, approximately 12.5 seconds.
* `replay_c16_contour.log`, `replay_c51_contour.log`: supplied floating-point
  contour implementations replayed. C51's five-node Fock inverse maximum
  difference was `5.68e-12`; its scalar continuation gave
  `s(E+i0) ~= 0.00707837231216 + 6.6837594e-8 i`.
* `replay_s62_high_precision.log` and `replay_s62_fock.log`: 30-digit
  floating-point recomputation gave `E ~= 5.9785793151665785452`,
  `rho ~= 2.12750672061584377e-8`; the finite local hard-core source/resolvent
  check differed by `1.91e-15`. These are not interval bounds.
* `independent_fock_check.py` and `independent_fock_check_n16.json` construct
  the two-boson matrix independently in L/R coordinates by an explicit
  Kronecker symmetrizer, then remove `LL` and `RR`. At 16 nodes per bath,
  the full inverse/Schur identity differed by `1.87e-14`, parity conjugation
  by `6.41e-14`, and eta/negative-eta selected eigenvalues by `3.05e-14`.
  Its direct transpose-bilinear second-order coefficient was approximately
  `-0.00707837233 - 6.6834e-8 i`; a conjugated pairing instead gave an
  imaginary part about `-0.002277`, illustrating the wrong continuation.
  This finite computation is a diagnostic, not the infinite-volume proof.

Blindness limitation: `C51/RESULT.md` itself contains a replay path ending in
`/c74/contour_check.py`, and `packet/SOURCE_SNAPSHOT.json` contains the
source identifier `P2_return_2241_20261026`. The supplied directory path also
contains the literal text `policy-terra`. No model or policy assignment for
either case was established or inferred from those strings. No memory,
programme chat, other reviewer, Dots, root working note, or admission folder
was accessed.
