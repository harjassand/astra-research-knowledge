# Atomic-herald first-return test: proof and limits

This is a conditional strengthening of the fixed-start source-clock IFT test
in `SOURCE_CLOCK_IFT_TEST.md`. It removes stationary initialization for the
driven excursions only if a nondisturbing binary herald identifies exactly
one microscopic state. The herald and the startup wait are operational
assumptions, not consequences of scalar-work observation.

## First-return identity

Assume a finite, irreducible CTMC under the source-clock family, with a
predeclared repeated closed protocol of period \(\tau\). At phase zero its
stationary law \(\pi=\pi_{E(0)}\) is strictly positive. Define the one-cycle
tilted kernel in column convention by
\[
M_{ij}=\mathbb E_j\!\left[e^{-\beta W_{\rm cyc}}
                     \mathbf 1_{\{X_\tau=i\}}\right].
\]
The fixed-start FK identity gives \(M\pi=\pi\). Since the finite CTMC is
irreducible and the exponential weight is positive, \(M\) is strictly
positive. Hence
\[
R_{ij}=M_{ij}\frac{\pi_j}{\pi_i}
\]
is a positive row-stochastic matrix:
\(\sum_jR_{ij}=(M\pi)_i/\pi_i=1\). Its finite chain is recurrent.

Let a herald report exactly \(X_0=A\), a single full microscopic state, at
phase zero. Run the repeated protocol and set
\[
K=\inf\{k\ge1:X_{k\tau}=A\}.
\]
For a specific first-return boundary loop
\(\gamma=(i_0=A,i_1,\ldots,i_{k-1},i_k=A)\), with no interior A, the
work-weighted forward path mass is
\[
m(\gamma)=\prod_{r=0}^{k-1}M_{i_{r+1},i_r}.
\]
The reversed loop is a first-return path for row chain \(R\) starting at A,
and its probability is
\[
\prod_{r=0}^{k-1}R_{i_{r+1},i_r}
=\left(\prod_{r=0}^{k-1}M_{i_{r+1},i_r}\right)
  \frac{\pi_{i_0}}{\pi_{i_k}}
=m(\gamma),
\]
because the \(\pi\)-ratios telescope and both endpoints equal A. Reversal is
a bijection on these first-return loops. Summing the row-R first-return
probabilities, which equal one, proves
\[
\boxed{\mathbb E_A[e^{-\beta W_{K\tau}}]=1.}
\]
No value of \(\pi\) is needed by the experiment or test. It appears only in
the proof. The original time-inhomogeneous CTMC has the strong Markov property
at the discrete period-boundary return time; each successful excursion starts
again in the same state A and at the same drive phase. The identity is for
first returns of the boundary skeleton, not the first continuous-time visit
to A inside a cycle.

## Timeout and anytime test across excursions

For a fixed cap \(K_{\max}\), define
\[
Z=\mathbf 1_{\{K\le K_{\max}\}}e^{-\beta W_{K\tau}},
\]
with \(Z=0\) on timeout. It is a partial sum of the nonnegative first-return
loop masses, so \(\mathbb E_A Z\le1\). For any predeclared
\(0\le\lambda\le1\), \(F=1-\lambda+\lambda Z\) is nonnegative and has
conditional expectation at most one. After each excursion, the strong Markov
property gives the same conditional bound given the past. Therefore
\[
S_n=\prod_{m=1}^n(1-\lambda+\lambda Z_m)
\]
is a nonnegative supermartingale under the source-clock null, and
\(\Pr(\sup_n S_n\ge1/\alpha)\le\alpha\). This anytime guarantee is across
excursion index, not across cycles within an excursion. It uses the exact
scalar work for successful excursions. With noisy readouts, let \(\hat W_m\)
be the randomized paired-phase estimate over the \(K_m\le K_{\max}\) cycles
of successful excursion \(m\). For a prechosen summable error allocation,
for example \(\alpha_m=\alpha_{\rm read}\,6/(\pi^2m^2)\), define
\[
r_m=B\sqrt{2K_m\log(1/\alpha_m)},\qquad
U_m=\hat W_m+r_m+K_mV_hb_{\rm ph},\qquad
\underline Z_m=e^{-\beta U_m}.
\]
Conditional on the full physical path of that excursion,
\(\Pr(W_m>U_m)\le\alpha_m\), so \(\underline Z_m\le e^{-\beta W_m}\)
except on an event of probability at most \(\alpha_m\). Set
\(\underline Z_m=0\) for timeouts. On the event that every allocated work
bound is valid, every observed factor
\(1-\lambda+\lambda\underline Z_m\) is no larger than its exact-work
counterpart. A union bound therefore gives the noisy-readout anytime level
\(\alpha_{\rm test}+\sum_m\alpha_m\), where \(\alpha_{\rm test}\) is the
Ville threshold for the exact-work supermartingale. This uses \(2K_m\)
scalar readouts on each successful excursion; never exponentiate an unbiased
work estimate and assume its mean is preserved. A false-positive herald needs
its own bound/budget; the proof assumes the binary A label is exact. A missed
A hit only delays triggering if the detector is nondisturbing, but adds
waiting time and fuel consumption.

If starting from an arbitrary distribution, hold \(E=E(0)\) until the exact
herald reports A at a period boundary; start the first drive cycle there.
This uses no energetic reset, but the trigger supplies microscopic state
information. After a timeout, stop the driven attempt at its closed-protocol
boundary, hold \(E=E(0)\), and wait until A appears at a period boundary before
starting the next attempt. Alternatively, continue the drive while waiting,
but ledger all such cycles separately. In either design, every waiting time,
chemical turnover, detector/readout, and controller resource is paid and
recorded. Holding E constant contributes zero field-port parameter work but
can still consume chemical fuel. Omitted waiting or timeout-cycle work is not
part of the e-process and must not be counted as net output. If A is not
reached, the test simply produces no further excursions. Irreducibility
ensures eventual boundary hits under the ideal finite CTMC, but supplies no
useful deadline unless a hitting-time bound is separately available.

## Why an atomic state matters

If the herald reports a block \(B\) of hidden states instead of one state,
the forward loop can start at \(i\in B\) and return at a different
\(j\in B\). Reversal then leaves the factor \(\pi_j/\pi_i\), which does
not telescope to one. A block version can hold if the microscopic entrance
law is exactly \(\pi\) conditioned on B, since then the factors cancel after
averaging; a herald alone does not establish that law.

For example, the algebraic conditions \(M\pi=\pi\) and positivity alone do
not make a block return expectation equal to one. With
\[
\pi=(1/3,2/3)^T,\qquad
M=\begin{pmatrix}1/2&1/4\\3/10&17/20\end{pmatrix},
\]
one has \(M\pi=\pi\) but the column sums are \(4/5\) and \(11/10\).
For a herald that only says “state lies in the whole two-state block,” the
first-return time is one cycle and the tilted expectation depends on the
unobserved entry state. This matrix illustrates the algebraic gap; it is not
claimed as a specific CTMC realization. A source-clock CTMC also exhibits
generic non-unit column sums under nontrivial driving: for small
\(h(t)=\varepsilon g(t)\), \(g(0)=g(\tau)=0\), the first variation of its
column-sum row is
\[
\left.\frac{d}{d\varepsilon}\mathbf1^TM_\varepsilon\right|_{0}
=-\beta\int_0^\tau g(t)f^TQ_0e^{Q_0t}\,dt,
\]
which is nonzero for generic \(g\) when \(f\) is nonconstant. Thus a
coarse herald does not get the atomic identity for free.

## Operational boundary

The herald must identify one microscopic state of the complete Markov model,
without disturbing transitions or the work path; false positives must be
bounded and paid separately, and detector disturbance must be ruled out or
included in the model. Missed hits delay triggering. If unobserved memory variables mean
“A” is not a complete Markov state, the strong-Markov restart argument fails.
Waiting at \(E(0)\) until A is observed avoids an energetic reset and can be
started from any initial distribution, but the trigger supplies state
information and potentially feedback/control work. Its detector, logic,
waiting time, and fuel costs require calibration. This is a strong structural
interface assumption, not ordinary scalar \(f\) readout.

The test can reject the source-clock work-fluctuation null; it does not certify
negative mean work, net output, or useful operation. The e-process only uses
selected A-to-A excursions. All elapsed time, holding/driven waiting, field
work outside those excursions, chemical consumption, and measurement costs
must remain visible in a separate performance ledger.
