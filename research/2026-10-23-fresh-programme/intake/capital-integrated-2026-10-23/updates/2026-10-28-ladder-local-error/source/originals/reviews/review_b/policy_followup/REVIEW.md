# Warm source-informed follow-up review

**P84: ACCEPT** the exact fixed-\(g\) finite-positive response and the
independent strict lower bound \(\rho(E_p)>4\,10^{-16}\).

**P17: ACCEPT**, at its stated scope, the local second-sheet pole construction,
the ordered-limit \(g^8\) coefficient, the coherent two-control leading Gram
matrix and strict compensation residual, and the declared all-sector stability
box. This accepts a pole of a *continued physical local resolvent matrix
element*. It does not assert a nonreal pole of the actual physical-sheet
resolvent of a self-adjoint operator. The construction itself identifies the
local second sheet, so that distinction is a scope clarification rather than
a rejection of its intended claim.

Neither endpoint establishes a time-domain lifetime/gate theorem, finite-error
performance throughout its stability box, or a hardware/comparator advantage.
These verdicts do not rank the experimental source policies.

## P84: the new interval claim

The normalized source and odd compression agree with the already reviewed
governing construction. The numerical decimal remains ordinary quadrature.
The interval lower bound is a different claim, and it passes independently.

The root bracketing uses the signs of the continuum contributions correctly:
the plus continuum is positive and can be bounded by its mass divided by the
minimum positive spectral distances; the minus continuum is negative and its
magnitude has the analogous bound. Thus dropping the minus continuum gives
a valid upper bound at 5.9785, and dropping the plus continuum gives a valid
lower bound at 5.9787. Monotonicity then encloses the exact root. All squared
distances used to upper-bound \(L_+'+L_-'\) stay separated from zero.

The two chosen intervals lie strictly inside the moving shell for every
energy in that bracket. Interval evaluation of both real source ranges and
both positive densities is valid on the full rectangles in \((E,x)\).
If their masses are \(m_1,m_2\) and their source ranges are separated by
\(d>0\), minimizing over an arbitrary complex scattering constant gives
\[
\rho\ge N^2\frac{m_1m_2}{m_1+m_2}d^2.
\]
The right side increases with either positive mass. Consequently substituting
the individual mass lower bounds is justified; no scattering-constant
enclosure or continuum quadrature is needed.

`certify_positive.py` replayed unchanged from a copy. More decisively,
`rational_certificate.py` implements the certificate independently with exact
`Fraction` interval arithmetic, integer-square-root enclosures, and a rational
Machin/alternating-series enclosure of \(\pi\). It imports no endpoint code
and uses no floating-point interval library. Its exact predicates give
\[
\begin{aligned}
F(5.9785)&<-0.005244278049770154\ldots,\\
F(5.9787)&> 0.021199933262653301\ldots,\\
\rho(E_p)&>4.085313342901200935\ldots\,10^{-16}
           >4\,10^{-16}.
\end{aligned}
\]
Decimal strings in that independent output are display only; the comparisons
are exact rational predicates. This confirms the actual interval claim, not
merely the familiar analytic positivity argument. The broad lower bound does
not certify the decimal value \(2.12750672\,10^{-8}\).

P84's scalar boundary argument is also sound: endpoint densities have
integrable derivatives, the source is analytic on the band rectangle, and the
weighted sum convolutions are locally Lipschitz. The certified bracket
separates the nearby product atom from the shell. No omitted coincident-atom
case is needed at this certified fixed coupling. Its finite Fock replay has
maximum resolvent discrepancy \(7.55\,10^{-16}\), appropriately used only
as an algebra check.

## P17: continuation and the physical numerator

The crucial issue is whether a zero of the forbidden Green determinant gives
a pole that actually appears in a physical matrix element. Here it does.
For fixed sufficiently small nonzero \(g\), the detuned one-body memory
Green matrix is a finite inverse with the two explicit half-line Weyl
functions. Its two simple gap atoms and its band densities are analytic in
the detuning near zero. Symmetric tensor convolution gives all local
harmonic two-particle Green entries, including the forbidden matrix \(M\),
the physical bare-pair entry, and their cross entries.

Near \(\lambda\in(4,6)\), only the mixed-band density can be on shell.
The substitution \(x=4+(E-4)t\) extracts
\(\sqrt{t(1-t)}\); the remaining factors are analytic in \(E\) near fixed
\(\lambda\). Other channels are analytic there. Splitting a scalar Cauchy
integral into a neighborhood with this analytic density and its complement
constructs the local continuation with the usual spectral jump. This applies
to the numerator entries as well as to \(M\); it is not an assumed global
operator-norm continuation.

At zero detuning,
\[
M=\operatorname{diag}\big((L_++L_-)/2,K\big),\qquad
\partial_z\det M(\lambda,0)=\tfrac12(L_+'+L_-')K\ne0.
\]
The derivative is nonzero because the even derivative is positive and the
upper-rim \(K\) has strictly positive imaginary part. The analytic IFT
therefore supplies a unique local continued determinant zero. The exact
compression identity for the *physical* bare-pair matrix element is
\[
R_{pp}^{\rm hc}=R_{pp}^{0}-R_{pq}^{0}M^{-1}R_{qp}^{0}.
\]
At zero detuning its coupling to the vanishing even entry is
\((L_+-L_-)/2=L_+\ne0\), and its pole coefficient has magnitude
\(2L_+^2/(L_+'+L_-')=Z_p>0\). Analyticity preserves this nonzero numerator
for sufficiently small detuning. Thus the determinant zero is not a spurious
zero canceled from the continued physical pair resolvent.

Parity makes the local pole position even in detuning. The second-order
Feshbach coefficient has imaginary part
\(-\pi\langle\eta,\delta(H_{\rm odd}-\lambda)\eta\rangle\), with the
already constructed exact constrained source. The sign and normalization
therefore give \(-2\operatorname{Im}z=2\pi\delta^2S_g+O_g(\delta^4)\).
This is a valid fixed-\(g\) local analytic statement. Its window is limited
not only by the distance \(O(g^2)\) to threshold 6, but also by the nearby
harmonic mixed bound-atom pole at distance \(O(g^4)\). No uniform radius,
remainder, or exchange of small-error and small-\(g\) limits follows.

The code does not numerically locate a continued detuned pole. Acceptance of
that existence claim rests on the above analytic construction and nonzero
numerator, not on a finite-chain eigenvalue or a numerical linewidth fit.

## P17: asymptotics, compensation and stability

The load-bearing cancellations are correct. The atom parts of
\(J_+(E_+)+J_-(E_-)\) cancel at order \(g^{-2}\), leaving
\(-b/(3a)+O(g^2)\). With \(N=3ag^2+O(g^4)\), the memory source on the
mixed atom is \(-bg^2+O(g^4)\). Its atom dominates \(K\); off-shell
atom-band contributions are \(O(g^2)\), giving
\(\alpha_V=-bg^2+O(g^4)\). On the open shell the unconstrained source is
only \(O(g^4)\). The corrected amplitude is therefore \(bg^2+O(g^4)\),
not \(O(g^4)\). Complete endpoint densities scale as \(g^2\) each;
uniform off-memory denominators and bounded edge factors justify dominated
convergence on the moving shell. The elementary remaining integral is
\(16/(27\pi^2)\), giving \(64b^2/(27\pi)\) for the probability-width
coefficient.

The first-rung perturbation is an actual physical operator. The memory-row
equation gives bath-endpoint coordinate \((x-3)/c_\sigma\), and contracting
it in the dressed pair gives precisely the stated \(H_\sigma\) source.
The useful stable identity is
\(H_\sigma=c_\sigma m_{{\rm bath},\sigma}^{\rm phys}G_\sigma\).
It independently verifies its sign and avoids the subtract-one cancellation
in numerical evaluation. Its mixed-atom leading term cancels, whereas its
corrected shell amplitude is
\((3a/\sqrt2)m_1(x)g^2+O(g^4)\). Thus the cross coefficient comes from
coherent source amplitudes, as claimed.

Independent 55-digit quadrature in `extension_checks.py` gives
\[
M=\begin{pmatrix}
0.072228729993059564&0.076465509174826782\\
0.076465509174826782&0.081853568192768429
\end{pmatrix},
\]
\[
\epsilon_*/\delta=-0.934174414910629772,\quad
M_{11}-M_{12}^2/M_{22}=0.0007966076988223620874.
\]
The leading reduction is **90.6703890759**, and the determinant is positive,
\(6.52051825984\,10^{-5}\). Strict Cauchy–Schwarz applies because
\(1\) and the nonconstant \(m_1(x)\) are not proportional under the
positive shell weight. These two controls cannot cancel the leading shell
exactly. The independent complete finite-\(g\) calculation at \(g=.2\)
gives optimum \(-0.8711044516595\) and residual coefficient divided by
\(g^8\) of \(0.0008035703609541\). At \(g=.01\) the memory coefficient
divided by \(g^8\) is \(0.07217047264715\), approaching the proved limit.
All these digits are ordinary quadrature diagnostics.

New original-rail occupation-number checks at lengths 3, 5, 7 test both
physical source vectors pointwise and the *cross* resolvent matrix, rather
than only their separate norms. Maximum source discrepancy was
\(1.11\,10^{-14}\); maximum coherent matrix discrepancy was
\(2.30\,10^{-15}\). The frozen endpoint's eighteen diagonal Fock
comparisons also replayed, with maximum error \(1.09\,10^{-15}\).

The stability calculation passes. Eliminating the tails gives the stated
\(K_0\); the lower bound \(K_0\ge.4\) follows, for example, by the
diagonal-minus-off-diagonal bound. The memory block is at least 2.9 and
\(\|C\|^2\le.32\), so its Schur complement is at least 2.1. Zero-energy
tail elimination can be justified as a quadratic-form limit despite the
gapless lower rail, since its endpoint inverse-frequency form is finite.
Second quantization and hard-core compression preserve nonnegativity in
every fixed excitation sector. This stability box is not an admissible-error
box for the resonance Taylor approximation.

The formal plateau scalings and initial Markov bath-loss jump rate have the
correct factors. They remain formal plateau consequences: no controlled
survival-law remainder, loading/unloading error, two-cycle code-isometry
bound, joint \((g,\delta,\epsilon,\kappa,T)\) regime, actuator/noise
interface, or hardware advantage is acquired. In particular the 90.7 factor
is a leading ordered-limit coefficient ratio, not a certified finite-error
gate improvement. Direct memory retuning is correctly retained as the stronger
ordinary correction when available.

## Evidence and source exposure

All three Python scripts from each endpoint were read fully and replayed
from copies under `replay/`; all commands exited successfully. The P17 Fock
replay emitted the previously encountered macOS BLAS floating-flag warnings;
every recorded numerical field was separately checked finite. Summary and
independent evidence are in `evidence_summary.json`,
`rational_certificate.json`, and `extension_results.json`. Original manifested
files still match every frozen hash after the review.

This is explicitly a **warm** follow-up to my four-endpoint review. I read
P84 `RESULT.md`, `PROOF.md`, all three scripts, its certificate output and
manifest, then P17 `RESULT.md`, `CONSTRUCTION.md`, all three scripts and its
manifest, followed by the new replay results. P17's supplied prose exposes
choice/corpus context and named alternative opportunities; full blinding is
therefore not claimed. I did not access policy/model maps, root coordination
work, other reviewers, programme chats, memory, Dots, or the external papers
listed by the endpoint. Its mathematical argument was checked directly using
the supplied model. My own prior occupation-number helper was reused and is
explicitly imported by the independent extension script. No source mapping
was inferred, and no frozen endpoint was repaired.
