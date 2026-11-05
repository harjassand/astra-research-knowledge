# Finite positive fitting of a passive memory kernel

## Result and scope

This note closes the mathematical interface from finitely many certified, finite-precision kernel reports to an encoded positive exponential model with a finite-horizon \(L^1\) certificate. It does not assume a known number of hidden modes, a positive spectral gap, or an upper relaxation-rate bound. It does not assume that a physical apparatus already supplies kernel reports: the actual-control protocol must establish the report intervals used below.

Positive exponential approximation and its logarithmic-squared mode scaling have strong prior results. The construction here makes a robust nodal certificate, a positive linear feasibility problem, sparse extraction, and finite coefficient errors explicit. No historical novelty is claimed for those ingredients or their combination.

Let

\[
K(t)=\int_{[0,\infty)}e^{-\lambda t}\,d\nu(\lambda),\qquad
\nu\ge0,\quad \nu([0,\infty))\le B.
\]

The positive rational numbers \(B,T,\zeta\) are supplied bounds and specifications. If \(B=0\), \(T=0\), or \(\zeta\ge BT\), the zero model settles the nontrivial part of the task. Otherwise normalize

\[
s=t/T,\quad k(s)=K(Ts)/B,\quad \epsilon=\zeta/(BT)\in(0,1).
\]

Thus \(k\) is the Laplace transform of a nonnegative measure of mass at most one. A normalized model \(\widehat k\) gives

\[
\widehat K(t)=B\widehat k(t/T),\qquad
\|K-\widehat K\|_{L^1(0,T)}
=BT\|k-\widehat k\|_{L^1(0,1)}.
\]

The mass bound is an actual prior requirement. Without a finite known bound, modes \(A e^{-\lambda t}\) with \(A\) proportional to \(\lambda\) can have substantial integrated response while being arbitrarily small at every fixed positive sample time.

## 1. A finite plan

Choose

\[
a=\epsilon/8,\quad
J=\lceil\log_2(1/a)\rceil,\quad
n=\lceil\log_2(128/\epsilon)\rceil,\quad
M=Jn,
\]

\[
L=\lceil\sqrt{2n-1}\rceil,\qquad
\delta=\frac{\epsilon}{16L}.
\]

For \(j=0,\ldots,J-1\), let

\[
I_j=[a_j,b_j],\qquad a_j=2^j a,\quad b_j=\min(2a_j,1).
\]

In each interval use the affine images of the \(n\) roots of \(T_n\), the Chebyshev polynomial of the first kind. Denote these ideal sample times \(s_{j\ell}\). Replace them by rational times \(\widetilde s_{j\ell}\in I_j\) satisfying

\[
|\widetilde s_{j\ell}-s_{j\ell}|\le(\delta/2)a_j.
\tag{1}
\]

These are executable times. For example, isolate the \(n\) polynomial roots using rational Sturm intervals, round their midpoints to a dyadic grid, and verify the intervals and rounding inequalities. No exact trigonometric clock is needed.

The physical acquisition module must return rational reports \(y_i\) on one event \(\mathcal E\) such that

\[
|y_i-k(\widetilde s_i)|\le\delta,\qquad i=1,\ldots,M.
\tag{2}
\]

Any sensor, finite bin, finite ramp, imperfect tracking, digitization, and stochastic error must already be included in this allowance. Statistical dependence between reports does not enter the deterministic fitting proof. It matters when proving the event \(\mathcal E\).

In physical units, the report tolerance is \(B\delta\), the first admitted time is \(Ta=\zeta/(8B)\), and the timing tolerance in interval \(j\) is \(T\delta a_j/2\). The number \(M=O(\log^2(1/\epsilon))\) counts distinct evaluation times, not experiments, repetitions, physical duration, or sensor samples.

## 2. Deterministic certificate from sampled discrepancies

**Lemma.** Suppose \(k_1,k_2\) are positive-mixture kernels of mass at most one. At the rational sample times above suppose

\[
|k_1(\widetilde s_i)-k_2(\widetilde s_i)|\le q.
\]

Then

\[
\|k_1-k_2\|_{L^1(0,1)}
\le a+16\,2^{-n}+L(q+\delta).
\tag{3}
\]

Here \(\delta\) is the timing contribution from (1); with exact ideal samples it is omitted. More generally, individual sample error bounds can replace \(q\), and interval lengths can be retained rather than bounded by one.

### Analytic control independent of the spectrum

For \(\operatorname{Re}z>0\),

\[
|k_r(z)|\le1,\qquad |k_1(z)-k_2(z)|\le2.
\]

Analyticity follows from dominated differentiation on every compact subset of that half-plane. Although the support of the measure can be unbounded, \(\lambda^m e^{-\lambda c}\) is bounded for each \(c>0\).

Map \([-1,1]\) affinely to an interval \([a_j,b_j]\) with \(b_j\le2a_j\). The Bernstein ellipse with parameter \(2\) remains in the open right half-plane. Its leftmost real point is

\[
\frac{a_j+b_j}{2}
-\frac{5}{4}\frac{b_j-a_j}{2}
=\frac{9a_j-b_j}{8}
\ge\frac{7a_j}{8}>0.
\]

Thus the difference \(F=k_1-k_2\), after this affine map, is analytic and bounded by two on that ellipse.

### Interpolation remainder

Write its Chebyshev expansion \(F(x)=\sum_{m\ge0}c_mT_m(x)\). The elementary contour bound gives

\[
|c_m|\le4\,2^{-m}.
\]

At the \(n\) roots of \(T_n\), the interpolant of \(T_m\) is a signed Chebyshev polynomial of degree below \(n\), or zero, by cosine aliasing. Its supremum norm is at most one. Therefore

\[
\|F-\mathcal I_nF\|_\infty
\le 2\sum_{m=n}^\infty|c_m|
\le16\,2^{-n}.
\tag{4}
\]

### An elementary sample-amplification bound

The cardinal functions at Chebyshev roots have the discrete cosine representation

\[
\ell_j(x)=\frac1n\left(1+
2\sum_{m=1}^{n-1}T_m(x)\cos(m\theta_j)\right).
\]

Discrete orthogonality gives

\[
\sum_{j=1}^{n}\ell_j(x)^2
=\frac1n\left(1+2\sum_{m=1}^{n-1}T_m(x)^2\right)
\le\frac{2n-1}{n}.
\]

Hence

\[
\sum_j|\ell_j(x)|\le\sqrt{2n-1}\le L.
\tag{5}
\]

This intentionally uses an elementary, slightly loose bound. The usual logarithmic Lebesgue bound can improve the tolerances and dictionary size without changing the sample-count conclusion.

### Finite timing

For any positive mixture of mass at most one,

\[
|k_r'(s)|\le \sup_{\lambda\ge0}\lambda e^{-\lambda s}
=\frac1{es}.
\]

Both ideal and rational nodes are inside \(I_j\), so (1) changes either kernel's value by at most \(\delta/(2e)\). Their difference changes by at most \(\delta/e\le\delta\).

On the omitted initial interval, both kernels lie in \([0,1]\), giving \(|F|\le1\) and integrated error at most \(a\). Apply (4) and (5) on the remaining intervals and sum their lengths, which total less than one. This proves (3).

### A directly usable output check

For any positive finite model of mass at most one, let sound exponential interval arithmetic establish

\[
|\widehat k(\widetilde s_i)-y_i|\le r
\quad\text{for every }i.
\]

On \(\mathcal E\), equation (3) gives the exact certificate

\[
\boxed{\quad
\|k-\widehat k\|_1
\le a+16\,2^{-n}+L(r+2\delta).
\quad}
\tag{6}
\]

One \(\delta\) comes from acquisition and one from timing. This is the verifier implemented in the accompanying program. Its validity does not depend on how the model was proposed.

## 3. An explicit finite positive dictionary

Set

\[
\mu_0=\delta/4,\quad
H=\lceil4/\delta\rceil,\quad
C=\lceil\log_2(4/\delta)\rceil,
\]

and let \(R\) be the least nonnegative integer with

\[
\mu_0 2^R\ge C/a.
\]

Use the rational pole set

\[
\mathcal P=\{0\}\cup
\left\{\mu_0 2^j(1+\ell/H):
0\le j<R,\ 0\le\ell<H\right\}
\cup\{\mu_0 2^R\}.
\tag{7}
\]

There are \(N=RH+2\) entries. A measure on arbitrary hidden rates admits a grid witness \(\sum_{\mu\in\mathcal P}w_\mu e^{-\mu s}\), with \(w_\mu\ge0\) and total weight at most one, whose discrepancy is at most \(\delta/4\) at every \(s\in[a,1]\).

**Proof.** Map every hidden rate below \(\mu_0\) to zero. The per-unit-mass error is at most \(\mu_0s\le\delta/4\). Map intermediate rates down to the nearest grid pole \(q\). Consecutive positive poles have ratio at most \(1+1/H\), so

\[
0\le e^{-qs}-e^{-\mu s}
\le(\mu-q)s e^{-qs}
\le\frac1H(qs)e^{-qs}
\le\frac1{eH}\le\delta/4.
\]

Discard rates at least \(\mu_02^R\). For \(s\ge a\), their per-unit-mass signal is at most \(e^{-C}\le2^{-C}\le\delta/4\). Each hidden rate incurs error at most \(\delta/4\); integrating against total mass at most one proves the claim. This is a feasibility proof, not a procedure requiring the hidden measure.

Including zero is essential to the admitted class. No waiting time or spectral gap is used. Very fast rates are discarded only after paying the full initial-interval error in the certificate.

## 4. Rational LP, sparse extraction, and output bits

Let \(A_{i\mu}=e^{-\mu\widetilde s_i}\). Compute rational entries \(\bar A_{i\mu}\) satisfying

\[
|\bar A_{i\mu}-A_{i\mu}|\le\delta/4,
\qquad 0\le\bar A_{i\mu}\le1.
\tag{8}
\]

A fixed dyadic denominator with \(b_A=\lceil\log_2(8/\delta)\rceil\) bits suffices. Certified exponential intervals followed by downward rounding produce (8).

Solve the rational linear feasibility problem

\[
w\ge0,\qquad \mathbf1^\top w\le1,\qquad
|\bar Aw-y|\le2\delta\,\mathbf1.
\tag{9}
\]

It is feasible on \(\mathcal E\): the grid witness differs from the true samples by \(\delta/4\), coefficient approximation contributes at most \(\delta/4\), and acquisition contributes at most \(\delta\), totaling \(3\delta/2\).

To extract a sparse model, preserve the \(M\) values \(\bar Aw\) and the total mass. Conic Caratheodory elimination in dimension \(M+1\) leaves at most \(M+1\) nonzero entries. Explicitly, whenever there are more, take a rational null vector \(v\) of the active columns of

\[
\begin{bmatrix}\bar A\\\mathbf1^\top\end{bmatrix}.
\]

The mass row forces any nonzero \(v\) to have both signs. Replace

\[
w\leftarrow w-\theta v,\qquad
\theta=\min_{v_j>0}w_j/v_j.
\]

All weights remain nonnegative, one disappears, and the preserved quantities are unchanged. This terminates after at most \(N-(M+1)\) eliminations.

Exact rational LP weights can have larger denominators than desired for storage. Round each retained weight downward to a dyadic grid with

\[
b_w=\left\lceil
\log_2\frac{8(M+1)}{\delta}
\right\rceil.
\tag{10}
\]

The total lost mass is at most \(\delta/8\), so predictions change by at most \(\delta/8\) everywhere. Positivity and the mass bound remain valid. The output-report discrepancy is at most

\[
r\le 2\delta+\delta/4+\delta/8=19\delta/8.
\]

Substituting into (6),

\[
\|k-\widehat k\|_1
\le\frac{\epsilon}{8}+\frac{\epsilon}{8}
+\frac{35L\delta}{8}
=\frac{67}{128}\epsilon<\epsilon.
\tag{11}
\]

The spare constant is deliberate; it permits straightforward outward numerical bounds. Multiplication by \(BT\) proves the requested physical \(\zeta\) guarantee.

### Computing exponentials without a hidden fast-rate cost

For nonnegative rational \(x\), a rational enclosure of \(e^{-x}\) to \(b\) bits can be computed as follows. If \(x\ge b+2\), use \([0,2^{-(b+2)}]\), since \(e>2\). Otherwise reduce \(x\) by a power of two until it lies in \([0,1]\), enclose the exponential by consecutive alternating Taylor partial sums, and square the nonnegative endpoints repeatedly. A starting enclosure narrower by the number of squarings compensates for their error amplification. All steps use finite rational arithmetic. The accompanying verifier implements this procedure.

### A guaranteed finite fallback, without assuming numerical LP success

The delivered program also implements a slower, completely finite alternative. Set \(D=2^{b_w}\), with \(b_w\) from (10). Enumerate every support of size at most \(M+1\) in the pole dictionary, and all positive integer weight vectors on that support with total at most \(D\); divide the weights by \(D\). Check every candidate with exact exponential intervals and equation (6).

The grid witness can be compressed in the coordinates of the exact sample values and mass, leaving at most \(M+1\) real weights. Rounding those weights downward to the denominator \(D\) loses at most \(\delta/8\). Consequently this enumeration contains a candidate with true report discrepancy at most \(11\delta/8\). Exponential enclosure widths at most \(\delta/128\) leave strict slack below the verifier threshold \(19\delta/8\). Thus the search terminates with a valid output on every admitted dataset.

There are at most

\[
\sum_{r=0}^{M+1}\binom Nr\binom Dr
\le (M+2)[N(D+1)]^{M+1}
=\exp(O(\ell^3))
\]

candidates, with each candidate requiring polynomially many finite rational operations. This is a concrete worst-case cost, not a practical efficiency claim. The implementation tries the fast LP proposal first and invokes this search only if the proposal or exact verification fails. A standard exact rational LP solver can replace the exhaustive fallback and recover polynomial time in the explicit dictionary input size.

## 5. Resource ledger

Write \(\ell=1+\log(1/\epsilon)\), and let \(L_0\) denote the binary length of the supplied rational scales and reports beyond the accuracy-dependent precision.

| Resource | Bound or obligation |
|---|---|
| Time intervals | \(J=O(\ell)\) |
| Distinct kernel report times | \(M=Jn=O(\ell^2)\) |
| Report precision | \(\delta=\Theta(\epsilon/\sqrt{\ell})\); \(O(\ell)\) accuracy bits |
| Earliest physical report | \(\zeta/(8B)\) |
| Earliest timing allowance | order \(T\epsilon^2/\sqrt{\ell}\), with the displayed constants |
| Dictionary size | \(N=O(\epsilon^{-1}\ell^{3/2})\) |
| Largest physical retained pole | \(O((B/\zeta)\log(1/\epsilon))\) |
| Smallest positive physical grid pole | \(\delta/(4T)\); zero is also present |
| Coefficient matrix | \(MN\) entries of \(O(\ell)\) accuracy bits |
| Exact fit computation | rational LP of this explicit size; polynomial in its binary input length using standard rational LP algorithms |
| Delivered executable's guaranteed fallback | at most \((M+2)[N(D+1)]^{M+1}=\exp(O(\ell^3))\) candidates; \(D=2^{b_w}\) |
| Final modes | at most \(M+1=O(\ell^2)\) |
| Final encoded model | \(O(M(L_0+\log((M+1)/\delta)))=O(L_0\ell^2+\ell^3)\) bits |
| Runtime model state | one variable per retained mode, plus the observed coordinate |
| Physical repetitions, force, slew, bins, duration | supplied by the actual acquisition construction; absent from the nodal-fit theorem |

The small final model does not imply a small fitting workspace or a small experiment budget. In particular the explicit dictionary is polynomial, not polylogarithmic, in inverse accuracy. If individual reported values require averaging noise, those repetitions are additional to \(M\).

The pole formula (7) uses within-octave rational grids rather than powers of a rational number close to one; this prevents pole denominators from accumulating \(N\) factors. Pole encoding length is \(O(L_0+\ell)\).

## 6. Executed certificate and its exact scope

The executable file is \`passive_certified_fit.py\`. It constructs rational sample times from exact polynomial root enclosures, forms a positive dictionary, proposes a fit using HiGHS, rounds weights to dyadics, and issues a certificate only after exact rational exponential-enclosure checks pass.

The numerical solver is a proposal mechanism. The script does not identify floating-point HiGHS with a universally successful exact LP algorithm. Failed proposal or verification invokes the finite fallback proved above. This closes executable termination on admitted reports at the stated, potentially enormous, fallback cost. It does not establish polynomial worst-case runtime for this particular implementation.

The run uses \(\epsilon=1/4\), \(M=45\) samples and \(N=24{,}322\) dictionary poles. Its bounded synthetic reporting errors are independently verified from the microscopic fixture, then only the rational reports are passed to the learner. The learner receives no hidden modes.

| Synthetic fixture | Retained modes | Certified \(L^1\) bound | Numerical diagnostic \(L^1\) |
|---|---:|---:|---:|
| Zero, \(10^{-9}\), moderate, and \(10^9\) rates | 4 | 0.121397 | 0.003284 |
| Thirteen decades of hidden rates | 5 | 0.121748 | 0.003638 |
| Twelve nearly coinciding hidden rates | 3 | 0.121930 | 0.002772 |

The certificate follows from finite reports, positivity, exact interval checks, and the theorem. The diagnostic quadrature is not used in its proof. The run is not a physical acquisition experiment. A separate exact audit exercises sparse extraction on five positive modes and confirms preserved sampled moments and mass. A second audit forces the finite fallback on a constant-kernel fixture and verifies a one-mode output.

## 7. Join to nonlinear prediction

The accepted passive-memory theorem in \`../PASSIVE_MEMORY_ACCEPTED_SOURCE.md\` supplies, for the same initial observed coordinate,

\[
\|x-\widehat x\|_{L^2(0,T)}\le R/\mu,\qquad
\sup_{t\le T}|x(t)-\widehat x(t)|\le R/\sqrt{2\mu},
\]

with

\[
R=\zeta\|\dot{\widehat x}\|_{L^2(0,T)}
+\|\rho\|_{L^2(0,T)}.
\]

The endpoint theorem applies on every prefix and the prefix residual norms are bounded by the full-horizon norm, giving the displayed supremum bound. The residual \(\rho\) must include initial hidden-force mismatch, actual forcing mismatch, and numerical equation residual. The kernel certificate alone does not establish those terms.

Finite positive mixtures have the familiar realization

\[
\dot z_j=-\lambda_j z_j+\dot{\widehat x},\qquad
\dot{\widehat x}+V'(\widehat x)+\sum_jw_j z_j
=f+\widehat g.
\]

Initialization is not silently set to zero. The root construction's later-time force measurement addresses the old offset separately: for a signed initial-force measure of total variation at most \(G\), its derivative obeys \(|g'(t)|\le G/(et)\). A finite late bin therefore supports a finite future constant approximation without erasing zero-rate modes. The actual hold/tracking, bin, sensor, and earlier-control contributions still have to be paid in that module.

The numerical execution also needs an executable, enclosed evaluation interface for \(V'\) and the forcing, with the relevant regularity bounds. Strong convexity by itself does not provide an algorithm for an arbitrary function. The model's small dimension does not make this interface free.

A single good calibration event supports every later admitted prescribed forcing to which the residual theorem is applied. If a controller receives the model's own trajectory rather than the physical trajectory, the two forcings can differ. Arbitrary discontinuous closed-loop feedback does not follow from this deterministic trajectory bound; its discrepancy must be controlled separately.

## 8. Boundary of the claim

The construction certifies an integrated finite-horizon kernel and resulting deterministic trajectory residual. It does not identify the microscopic measure, recover its order or rates, certify \(K(0)\), control derivatives at zero, make a uniform infinite-horizon claim, simulate thermal path laws, or establish a hardware implementation.

All of those distinctions matter. A very fast mode can be invisible at the samples and still alter \(K(0)\). A zero-rate mode remains in the admitted class and can carry a persistent old force. A large future velocity norm can make the trajectory error allowance large even for a small kernel \(L^1\) error.

