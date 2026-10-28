# Independent internal review of the certified continuum two-kick benchmark

**Reviewer:** producer-workspace/knowledge_and_comparator  
**Review completed:** 2026-10-28  
**Disposition:** pass for the specified mathematical benchmark, after two small source corrections. No unresolved mathematical or scalar-arithmetic defect was found in the reviewed version. This is an actual independent internal review of source, derivations and executed checks, not external peer review or a general verification of the Python interval class.

## 1. Exactly what was reviewed

The source is ../code/certified_continuum_kicks.py, SHA-256:

    e38d736042d0ac78e2bfaaba416fb43febd4ab0bce476e0a5113b49132643f43

The completed numerical receipt is ../data/certified_continuum_kicks.json, SHA-256:

    0d9f561dddf86014817dee2d42d43dd79d65af573855b18f567ce640c2d05a15

The receipt's embedded source hash agrees with the source. Both files were unchanged during the independent audit replay. The owner explicitly identified this source as stable before the final hash pin.

The model is a vacuum bosonic continuum with dimensionless positive-frequency density

\[
\rho(\omega)=\frac{21}{10}e^{-\omega},\qquad \omega\geq0,
\]

and two specified interaction-picture kicks,

\[
U=U_2U_1,\qquad
U_1=e^{-i(1/2)X\sin\Phi(f_0)},\qquad
U_2=e^{-i(3/4)Z\sin\Phi(f_{3/5})}.
\]

Here \(\Phi(f)=a^\dagger(f)+a(f)\), with the convention
\(\langle f_0,f_t\rangle=\int_0^\infty\rho(\omega)e^{i\omega t}\,d\omega\).
The source input dimension is two. The detector is an ideal threshold instrument after a passive linear splitter, with one-particle collected-port effects \(E_1=(3/5)I\), \(E_2=(1/4)I\), and uncollected effect \(E_0=(3/20)I\).

This review does not extend the old baseline circuit representation certificate to the new model. It does not certify a finite-duration P2 waveform, a physical notch, a collected microwave port, source preparation, device loss, reset, repeated rounds, or a computing workload. The numerical bounds here concern approximation of the specified retained unitary and its specified ideal detector instrument.

## 2. Corrections requested and applied during this review

1. The original packet expression used \((-1)^{n+m}\) as Python exponentiation of integer -1 by the possibly negative integer n+m. Negative integer exponents produce a float in Python. Those particular floats were exactly \(+1\) or \(-1\), and the subsequent conversion to Fraction was exact, so this was not a discovered numerical error in the prior bound. The owner replaced the expression with integer parity, making the claimed exact integer coefficient arithmetic literal.

2. The event-interval helper previously clipped both raw interval endpoints at zero without first checking a negative upper endpoint. Since the underlying event effect is positive, an upper endpoint below zero would indicate an invalid enclosure or a model/arithmetic failure. The owner added an assertion that the upper endpoint is nonnegative before clipping. No supplied interval triggered this assertion; all reported bounds were unchanged.

No other correction was required for the reviewed benchmark. These changes are included in the pinned source above.

## 3. Analytic coefficient and operator bounds

For a Pauli involution \(P\), the Jacobi–Anger expansion gives

\[
e^{-i\theta P\sin\Phi(f)}
  =\sum_{n\in\mathbb Z}(-1)^n J_n(\theta)P^nD(inf).
\]

Every \(P^nD(inf)\) has operator norm one. Consequently an absolute coefficient-tail bound is an operator-norm bound, with no vacuum, low-energy, Fock, or reference restriction.

The code keeps \(-8\leq n\leq8\) per kick. Each retained \(J_n(\theta)\) is represented by the midpoint of an alternating-series enclosure using 22 terms and the next term. The absolute term ratio is bounded above by \(\theta^2/4<1\), including the \(n=0\) case, so the alternating enclosure is valid for both specified areas. Negative orders use \(J_{-n}(\theta)=(-1)^nJ_n(\theta)\). The midpoint radius is propagated in the coefficient \(\ell^1\) error.

For \(n\geq K+1\),

\[
|J_n(\theta)|
\leq
\frac{(\theta/2)^n}{n!}\frac1{1-a},
\qquad
a=\frac{\theta^2}{4(K+2)}<1.
\]

This follows by bounding the absolute power series geometrically after dropping an additional \(1/k!\) suppression. The ratios of consecutive leading factors are at most \(q=\theta/[2(K+2)]<1\). Both positive and negative tails are therefore bounded by exactly the rational expression used in the code:

\[
\sum_{|n|>K}|J_n(\theta)|
\leq
\frac{2(\theta/2)^{K+1}}{(K+1)!}
\frac1{1-a}\frac1{1-q}.
\]

Let \(P_j\) be the resulting bounded operator polynomial, and let
\(\|P_j-U_j\|\leq\delta_j\). The audited composition bound is

\[
\|P_2P_1-U_2U_1\|
\leq \delta_2(1+\delta_1)+\delta_1
=(1+\delta_1)(1+\delta_2)-1
=:\epsilon.
\]

The receipt encloses

\[
\begin{aligned}
\delta_1&\simeq 2.1699277983126690\times10^{-11},\\
\delta_2&\simeq 8.5172275243642020\times10^{-10},\\
\epsilon&\simeq 8.734220304380287\times10^{-10}.
\end{aligned}
\]

All these coefficient calculations and comparisons are exact rational arithmetic before outward conversion for display.

### Complete-channel meaning of the \(2\epsilon\) bound

Let \(V\) be the exact source-to-source-plus-bath isometry obtained by appending the vacuum and applying \(U\), and let \(A\) be the analogous polynomial map. Then \(\|A-V\|\leq\epsilon<1\). All singular values of \(A\) lie in \([1-\epsilon,1+\epsilon]\), so

\[
W=A(A^\dagger A)^{-1/2}
\]

exists as an isometry and satisfies \(\|W-A\|\leq\epsilon\). It follows that \(\|W-V\|\leq2\epsilon\). For the exact and polar isometries, their complete output channels obey

\[
\frac12\|\mathcal W-\mathcal V\|_\diamond
\leq\|W-V\|
\leq2\epsilon.
\]

This bound is uniform over all source inputs and entangled reference systems. Applying a common detector channel, retaining its classical records, and tracing other outputs cannot increase it. The audited rational value satisfies

\[
2\epsilon
<
1.747\times10^{-9}.
\]

The final decimal enclosure is

\[
[1.74684406087605731641352644527525299586098243323,\,
  1.74684406087605731641352644527525299586098243324]\times10^{-9}.
\]

The finite packet map \(A\) itself is not exactly normalized. The receipt's raw Gram diagonal is approximately \(1+1.98248\times10^{-19}\). Thus this channel statement uses the explicit mathematical polar construction; it is not a claim that the unnormalized raw packet map is already trace preserving. The code does not serialize a separately polar-normalized Choi matrix.

## 4. Packet phases and detector effects

The continuum overlap is evaluated analytically:

\[
C=\langle f_0,f_{3/5}\rangle
=\frac{21/10}{1-i\,3/5}.
\]

Writing \(C=C_R+iC_I\), the packet amplitudes are
\(\alpha_{nm}=i(nf_0+mf_{3/5})\). The Weyl product in the correct time order gives

\[
D(imf_{3/5})D(inf_0)
=e^{i nm C_I}D(\alpha_{nm}).
\]

The packet source factor is \(Z^mX^n\), including the integer parity sign from the two Bessel expansions. The reviewed code has this matrix order and this phase sign. Its norm and cross-overlap are

\[
\begin{aligned}
\|\alpha_{nm}\|^2
&=\tfrac{21}{10}(n^2+m^2)+2C_Rnm,\\
\operatorname{Im}\langle\alpha_{nm},\alpha_{n'm'}\rangle
&=C_I(nm'-mn').
\end{aligned}
\]

For the no-click effect \(\Gamma(zI)\), the normalized coherent-state matrix element is

\[
\langle\alpha_p|\Gamma(zI)|\alpha_q\rangle
=
\exp\!\left[-\tfrac12\|\alpha_p\|^2
            -\tfrac12\|\alpha_q\|^2
            +z\langle\alpha_p,\alpha_q\rangle\right].
\]

The code adds the packet Weyl phase difference to the imaginary part of this kernel, with the correct index orientation. The four contractions are \(z=1,2/5,3/4,3/20\): all outputs, no click in port 1, no click in port 2, and no click in either port. Inclusion–exclusion then produces neither, only 1, only 2, and both. The shared emitted field is retained throughout; independent click probabilities are not substituted.

The paired Hermitian accumulation stores
\([Q_{00},Q_{11},\operatorname{Re}Q_{01},\operatorname{Im}Q_{01}]\).
For \(|+i\rangle=(|0\rangle+i|1\rangle)/\sqrt2\),

\[
\langle+i|Q|+i\rangle
=\tfrac12(Q_{00}+Q_{11}-2\operatorname{Im}Q_{01}),
\]

which agrees with the implemented sign. The independent Fock calculation is sensitive to both the Weyl phase and this input convention.

### Why the reported probabilities apply to the exact model

The reported event intervals are transferred directly from the unnormalized candidate \(A\), not from an uncomputed polar event table. For any event effect \(0\leq\Pi\leq I\) and normalized input \(\psi\),

\[
\left|
\|\sqrt\Pi\,V\psi\|-\|\sqrt\Pi\,A\psi\|
\right|\leq\epsilon.
\]

Hence a valid interval for the candidate event probability \(p\) yields the exact-model enclosure

\[
\left[
\max(0,\sqrt p-\epsilon)^2,\,
\min(1,(\sqrt p+\epsilon)^2)
\right],
\]

with the lower and upper endpoints evaluated in the appropriate directions. Clipping a slightly negative interval lower endpoint to zero is justified by positivity of the underlying event effect. The new upper-endpoint assertion catches an impossible negative enclosure.

## 5. Scalar-arithmetic review

The following checks concern the pinned source at its stated parameters.

- Fraction construction, factorials, Bessel centers, tails, continuum norms, phases and coefficient products are exact. All packet Pauli entries are integers after the correction. Remaining powers of \((-1)\) have nonnegative integer exponents.
- The rational Machin formula uses \(16\arctan(1/5)-4\arctan(1/239)\), with alternating remainder brackets and the correct signs when combining interval endpoints.
- Trigonometric range reduction chooses an integer using exact rational arithmetic. It does not require the midpoint approximation to choose the mathematically nearest integer: the code separately checks that the resulting remainder enclosure lies in \([-1,1]\), and the quadrant identity is valid for every integer.
- Cosine degree 38 and sine degree 39 have the stated uniform remainders \(1/40!\) and \(1/41!\) on that interval. All Horner operations are outward. Interval squaring across zero can overestimate the range but cannot exclude the true square.
- Fraction-to-Decimal division, interval addition and each possible product endpoint use explicit floor/ceiling contexts. Negation uses the context-independent copy-negate method.
- Decimal exponential and square root are correctly rounded nearest operations; bracketing with adjacent representable values encloses the exact endpoint functions. These monotone functions then enclose the original interval. The observed exponential arguments range from \(-79296/85\) to zero, far inside the configured exponent range.
- Final square-root subtraction, addition, squaring and endpoint clipping have the correct outward directions.
- Runtime fields and the printed float summary do not enter any asserted mathematical bound. The receipt preserves exact numerators, denominators and outward decimal endpoints.
- Changing the ambient Decimal precision to 180 for the independent audit did not alter any replayed root interval string, corroborating that the audited path consistently uses its explicit contexts.

This is a review of the exercised finite parameter domain. It does not assert that the small interval class handles arbitrary NaNs, infinities, user-supplied invalid intervals, or exponential underflow correctly.

## 6. Executed independent checks

The reproducible audit harness is certified_kick_audit.py; its receipt is certified_kick_audit.json.

It performed the following checks successfully:

| Check | Result |
|---|---|
| Embedded source hash vs source bytes | Exact match |
| Exact rational \(\epsilon<1\) and \(2\epsilon<1.747\times10^{-9}\) | Pass |
| All retained Bessel enclosures, with a separate 180-digit series | Pass, 34 coefficients |
| Tail comparison to a separate 100-term numerical sum | Pass; diagnostic only |
| Machin rational \(\pi\) enclosure vs independent Gauss–Legendre iteration | Pass |
| All distinct phase kernels vs direct original-argument Taylor series | Pass, 3,539 arguments |
| All distinct exponential kernels vs 180-digit Decimal exponential | Pass, 18,230 arguments |
| Root raw Gram and all four raw effects replay | Exact string match |
| All sixteen final probability intervals replay | Exact string match |
| Independent finite-Fock probabilities inside exact-model intervals | All sixteen enclosed |

The scalar checks support the analytic arithmetic review. They are not substituted for its remainder and directed-rounding proofs. The exponential diagnostic uses the same Decimal library at a much higher precision; the trigonometric diagnostic uses a separate direct Taylor evaluation with no shared range reduction.

### Independent oscillator calculation

independent_kick_fock_check.py constructs two oscillator modes realizing the exact Gram matrix of the two sampled continuum vectors. Writing the scalar variance as \(v=21/10\), these vectors are

\[
f_0=(\sqrt v,0),\qquad
f_{3/5}=\left(C/\sqrt v,\sqrt{v-|C|^2/v}\right).
\]

For these two instantaneous kicks, this finite one-particle span is exact. The check then uses quadrature diagonalization and direct trigonometric matrix functions, without the root Bessel coefficients, Weyl packet sum, or interval code. Oscillator Fock truncation is the approximation being varied.

| Per-mode Fock cutoff | Maximum probability change from preceding cutoff |
|---:|---:|
| 48 | Initial run |
| 80 | \(5.063841013175363\times10^{-10}\) |
| 120 | \(2.1760371282653068\times10^{-14}\) |
| 160 | \(3.68594044175552\times10^{-14}\) |

The cutoff-160 isometry defect was \(2.591047889277696\times10^{-14}\). All sixteen cutoff-160 event values lie inside the certified continuum intervals. For example, the neither-click probability is approximately \(0.69522963554716\) on \(|0\rangle\) and \(0.57227918524756\) on \(|+i\rangle\); both-click probabilities are approximately \(0.10326871807173\) and \(0.14506968534048\), respectively.

This is an independent convergence and sign/order diagnostic. There is no rigorous Fock-tail claim attached to this separate computation. The continuum certificate rests on the exact operator-polynomial tail and interval evaluation above.

## 7. Review evidence and reproducibility

Run from the saved package:

    python knowledge_and_comparator/independent_kick_fock_check.py
    python knowledge_and_comparator/certified_kick_audit.py

The second script reads the root receipt, replays the interval computation without replacing it, and checks hashes before and after its run. Re-executing the first script changes its runtime-bearing receipt hash; the second script records the then-current hash.

Additional pinned files at this review boundary:

| File | SHA-256 |
|---|---|
| certified_kick_audit.py | b25cd59cb5f691502b5f39574cca1fdd32207bbf03a92cf269e18eb7a62694f9 |
| certified_kick_audit.json | 6f4d3433d6cd78efbc4343e576f4c12f25f319f7cd7aa4a90f30bb6f46fef0b9 |
| independent_kick_fock_check.py | 4c14219b4377b698db3a2c700641ee7a54e285dfccf3305fb5b04f469df478da |
| independent_kick_fock_check.json | 3f628f4d0ae9a15f7a14a9e6d672e6f1e8deae07afb059447615dcc14b36d180 |

The reviewed result is a useful bounded nonlinear continuum instrument benchmark: a reference-uniform operator approximation and complete ideal detector-record construction, with explicit scalar arithmetic enclosures. Its small number is a retained-dynamics approximation bound for this stipulated benchmark. It supplies no device error rate, gate fidelity under P2 operating conditions, or total workload guarantee.

