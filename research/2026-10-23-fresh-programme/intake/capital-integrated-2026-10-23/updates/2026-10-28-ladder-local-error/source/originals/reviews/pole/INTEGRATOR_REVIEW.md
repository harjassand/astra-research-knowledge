# Warm review of the C86 integration return

## Prior exposure and scope

This is **not a blind or fresh independent review**. Before opening C86, I had
read the governing ladder packet, S62's source-density proof and code, the
full C16 and C51 constructions and code, and their associated results. I had
replayed C51's supplied contour check, the S62 checks, and the C16 interval
certificate, and had constructed a separate finite Fock diagnostic. My prior
review and its replay files are in the same `trial_coord_review` directory.
In that earlier material C51's result file exposed a `c74` source path; C86
also explicitly identifies the integrated specialist as `c74`. I did not
infer a model or policy assignment. The only newly opened source for this
turn was the complete eight-file C86 frozen return, including its manifest.
All seven manifest entries match the bytes and SHA-256 hashes of the copies.
The frozen source files were not edited.

## Verdict

**The integration adds a valid exact local derivation and useful diagnostic
checks, but identifies no load-bearing defect in the specialist handoff and
does not establish a new pole theorem.** This agrees with C86's explicit
provenance statement: the specialist had already established the qualitative
target, subject to its stated S62 density input. Its new formulas are
consequences of that handoff's isolated, transpose-symmetric simple
eigenprojection, odd-sector inverse, and parity, rather than a missing
resonance hypothesis or repair. They add an alternative local response
representation and a more explicit cancellation algebra.

## Targeted mathematical check

1. Let `P0=psi_theta B(psi_theta,.)`, `Q0=1-P0`, and `f=V psi_theta`.
   From the specialist's simple Riesz eigenprojection and odd invertibility,
   `B(psi_theta,psi_theta)=1`, `P0` is bounded and transpose symmetric,
   `f` is odd with `Q0 f=f`, and the complementary restriction of
   `H_theta-E` is invertible. In a possibly smaller local `(eta,z)`
   neighborhood, `D_eta(z)=Q0(H_theta+eta V-z)Q0` remains invertible.
2. Relative to `span(psi_theta) + ran(Q0)`, the full operator has block
   matrix `[[E-z, eta f^T],[eta f,D_eta(z)]]`: parity makes the diagonal
   matrix element of V vanish. Its exact Schur complement is therefore
   `F=E-z-eta^2 B(f,D_eta(z)^(-1)f)`. It retains all powers of eta in the
   complementary inverse. The local zero is equivalent to the full
   eigenvalue and satisfies `F_z(0,E)=-1`. This is a distinct equation from
   replacing `D_eta` by the unperturbed odd inverse; the latter only gives
   the quadratic coefficient. No finite-rank assumption on V is needed.
3. Block inversion gives `G_psi=1/F` and, with `a_p=B(psi_theta,p)` and
   `p_Q=Q0 p`,

   `G_p=B(p_Q,D_eta^(-1)p_Q) + [a_p-eta B(f,D_eta^(-1)p_Q)]^2/F`.

   Transpose-bilinear symmetry is essential. At zero, `a_p^2=Z_p>0`, so
   the specialist's visibility follows locally. At a nonzero-eta pole the
   coefficient of `1/(lambda-z)` also includes `-1/F_z(eta,lambda)`; C86
   correctly calls the displayed squared factor a numerator, not the entire
   residue. Parity conjugates `D_eta` to `D_-eta` and sends `f` to `-f`, so
   F and the uniquely selected branch are even.
4. In the hypothetical mixed-atom coincidence, write `d=a-z`,
   `R=Pi/d+R0`, `v=Pi q`, `g=R0 q`, `m0=q^T R0 q`, and
   `b=q^T Pi q>0`. The rank-one symmetric projection gives `v v^T=b Pi`.
   Direct expansion yields exactly

   `R-Rq(q^T Rq)^(-1)q^T R = R0 + (m0 Pi-v g^T-g v^T-d g g^T)/(b+d m0)`.

   The denominator is nonzero in a sufficiently small neighborhood of
   `d=0`, so the displayed compressed inverse is holomorphic there and the
   inverse identities extend. This verifies C86's expanded formula and is
   the explicit algebra behind the cancellation already stated by C51.
   The C16 interval certificate separately shows this coincidence does not
   occur at the fixed `g=1/5`; the specialist argument did not need that
   numerical separation.

## Numerical evidence, including failures

I inspected all three C86 numerical output files and both scripts; I did not
rerun the computationally heavy integration since no concern required it.
The integrator's physical L/R-basis Fock construction removes the two
forbidden states, uses the actual diagonal detuning, and applies a complex
orthogonal transpose-bilinear basis change. The previously supplied contour
script in C86 has the same hash as the C51 contour script I replayed before
this turn. The 20-node results report a two-constraint inverse discrepancy of
`2.075e-13`, absolute dressed and bare response discrepancies of
`1.303e-10` and `1.254e-10`, and `Im s=6.6838746e-8`. These numbers check
finite discretizations and algebra, not an interval or existence theorem.

The saved coarse failures matter:

* At 8 nodes and theta `0.25`, the unperturbed imaginary energy is
  `+7.26079e-7` and the source coefficient has **wrong-sign**
  `Im s=-2.23502e-6`.
* At 12 nodes and theta `0.25`, `Im s=+4.69035e-8`, about 30% below the
  much better 96–160-node diagnostic near `6.6837594e-8`.
* The separately preserved initial 12-node, theta `0.4` run has another
  **wrong-sign** `Im s=-5.44189e-8`, with unperturbed imaginary energy
  `-6.79173e-9`. This case is retained in
  `integration_check_low_order_results.json`; it is not in the final
  8/12/20-node theta-0.25 sweep.

The coarse results do not refute the analytic operator proof, and the
20-node agreement does not certify a coefficient, detuning interval, or
finite-eta width. The local positive eta radius and remainder constants
are defined through unevaluated resolvent bounds. Lifetime, time-domain
decay, device performance, and scientific novelty remain separate claims.

Replay copies are in `trial_coord_review/C86/`; no C86 frozen sources were
changed. A convenience parser initially assumed that the older low-order
JSON contained response-error fields and failed with a `KeyError`; I then
read that file directly. This parser failure is not a numerical experiment.
