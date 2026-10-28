## The continuation establishes a stronger measurement interface

**A reciprocal single-feed receiver, combined with a local coherent reference, can recover matched target power directly from three passive target-load states and twelve scalar power readings.** The recovery has a uniform linear bounded-error modulus, including at zero target strength and when the feedback pole cannot be resolved separately.

This removes two substantial restrictions: complete collection of returned power, and phase-circle actuation at the hidden target. It also changes the information acquired by the instrument, which is why it can improve on the original interface’s square-root precision modulus without contradicting that theorem.

I completed the proofs, exact arithmetic implementations, full control emulations, calibration extension, retained failure examples, and scoped reviews. The complete reproduction passed all nine check groups.

**Saved deliverables:**

- [Astra_P1_Reciprocal_Receiver_Continuation.zip](https://chatgpt.com/library?file_id=libfile_f116706293d08191b387e8239bbe5452&account_id=personal) — the complete continuation, original sources and report, proofs, code, raw transcripts, results, reviews, and reproduction instructions.
- README.md[README.md](unacquired-archive/continuation/README.md) — the research report and evidence map.

This is a mathematical construction and executable research result under explicit measurement and actuation conditions. No hardware calibration or execution of the protocol is claimed.

## 1. The physical opening: collect through the reciprocal launcher

Keep the original passive reciprocal source:

\[
S=
\begin{pmatrix}
S_0&t\\
t^T&s
\end{pmatrix},
\qquad S^*S\preceq I,
\]

with accessible return matrix under target reflection \(z\),

\[
T_z=S_0+\frac{z}{1-sz}tt^T.
\]

Write

\[
G=\overline t\,t^T,\qquad
p(u)=u^*Gu=|t^Tu|^2,\qquad
\tau=\operatorname{tr}G.
\]

Here \(p(u)\) is matched-target power for the prepared input.

A reciprocal launcher has forward transfer \(U\) and reverse transfer \(U^T\). Driving one feed prepares \(u=Ue_1\). If the other feeds are matched, the return at that **same feed** is

\[
h_z(u)=u^TT_zu
      =h_0(u)+\frac{z}{1-sz}a(u),
\]

where

\[
a(u)=(t^Tu)^2,
\qquad
\boxed{|a(u)|=p(u).}
\]

The transpose is the decisive physical feature. A generic fixed receiver projection does not have this identity and can be blind. The construction uses the reciprocal return of the mode actually launched; other return modes are terminated.

There is a useful extension beyond an ideal reflectionless launcher. Any **fixed passive reciprocal front end**, with one upstream source/return feed, one target port, and other external ports matched, reduces to a reciprocal two-port. Its target-load residue remains the square of its feed-to-target amplitude. Thus per-configuration target-power metrology can tolerate reciprocal insertion loss and internal reflections.

The control theorem has an additional requirement: the commands must act through a fixed calibrated linear input map. Arbitrary command-dependent reflections can change the effective source and do not automatically preserve one fixed target Gram.

The resulting acquisition choices are:

| Interface | Target settings | Raw powers per input | Acquired observable |
|---|---|---:|---|
| Original calibrated total-return collection | Two five-phase circles and shared matched baseline | 11 | \((\operatorname{tr}G)p(u)\) |
| Reciprocal single-feed receiver, without reference | Same two circles and baseline | 11 | \(p(u)^2\) |
| Reciprocal single-feed receiver with local reference | \(0,+r,-r\), four local reference phases each | 12 | \(p(u)\) |

The middle construction removes full output collection but retains square-root sensitivity. The third construction supplies the stronger observable.

The physical construction and its qualifications are recorded in CALIBRATION_AND_FAILURES.md[CALIBRATION_AND_FAILURES.md](originals/CALIBRATION_AND_FAILURES.md).

## 2. Direct target-power recovery without resolving the pole

### Acquire three complex returns using power detectors

Use target states

\[
z\in\{0,+r,-r\},\qquad 0<r<1.
\]

A passive half-power combiner mixes the return with a reference of amplitude \(R>0\):

\[
I_\theta(z,u)=\frac12\left|h_z(u)+Re^{i\theta}\right|^2.
\]

Four local reference phases acquire the complex return:

\[
\widehat h_z=
\frac{
(\widehat I_0-\widehat I_\pi)
+i(\widehat I_{\pi/2}-\widehat I_{3\pi/2})
}{2R}.
\]

If each physical power reading has simultaneous absolute error at most \(\eta\), then

\[
|\widehat h_z-h_z|
\le \frac{\sqrt2\,\eta}{R}.
\]

This costs twelve raw detector readings for the three target states. Reference energy, combiner loss, detector dynamic range, and phase stability remain resources.

### Eliminate the nuisance pole stably

Define

\[
c=\frac{h_r-h_{-r}}{2r}
  =\frac{a}{1-r^2s^2},
\]

\[
d=\frac{h_r+h_{-r}-2h_0}{2r}
  =rs\,c.
\]

Every physical pair satisfies

\[
|d|\le r|c|.
\]

On that set, define

\[
\Psi(c,d)=c-\frac{d^2}{c},
\qquad
\Psi(0,0)=0.
\]

Then \(\Psi(c,d)=a\), so \(p=|\Psi(c,d)|\).

Although the expression contains division by \(c\), its physical restriction is uniformly stable. For two feasible pairs, putting \(k=d/c\) and \(k'=d'/c'\) gives the exact identity

\[
\Delta\Psi
=(1+kk')\Delta c-(k+k')\Delta d.
\]

Since \(|k|,|k'|\le r\),

\[
|\Delta\Psi|
\le (1+r^2)|\Delta c|+2r|\Delta d|.
\]

This continues to zero signal. Accurate separate estimation of \(s\) is unnecessary.

The executable decoder keeps the noisy \(c\) and clips the noisy \(d\) radially into \(|d|\le r|c|\). If each acquired field has error at most \(\epsilon_h\), the resulting target-power estimate obeys

\[
\boxed{
|\widehat p-p|
\le K_r\epsilon_h,
\qquad
K_r=\frac1r+3r+8.
}
\]

At \(r=1/2\),

\[
K_r=\frac{23}{2},
\qquad
|\widehat p-p|
\le \frac{23}{\sqrt2\,R}\eta
\]

for detector error alone. Other acquisition errors must be included in the field budget.

The implementation uses inward dyadic clipping and outward rational magnitude bounds. A review also caught a potential proof trap: the complex feasible set is nonconvex, so a nearest projection cannot simply be declared nonexpansive. The saved proof uses the explicit clip and its own error bound.

The complete derivation is in COHERENT_THREE_LOAD_OBSERVABLE.md[COHERENT_THREE_LOAD_OBSERVABLE.md](originals/COHERENT_THREE_LOAD_OBSERVABLE.md).

### Why the original lower bound survives

For a dark-background family, target coupling produces a return field proportional to target power. Squaring that field produces an intensity proportional to target power squared. The reference supplies a measured interference term that is linear in the return field.

That is additional acquired information. The original uniform square-root lower bound remains a correct statement about its original measurement interface.

I also saved a matching **linear bounded-error exponent** for the new interface when reference amplitude is bounded. A zero source and a sufficiently weak reciprocal source have raw reference-intensity transcripts within the allowed error while their target Grams differ linearly in that error. This establishes sharpness of the precision exponent, without claiming optimal dimension constants or a photon lower bound.

## 3. Calibration was treated as part of the construction

### The target tag has an explicit realization

At a real reference impedance \(Z_0\),

\[
z=\frac{Z-Z_0}{Z+Z_0}.
\]

For \(r=1/2\), the three states are the positive resistances

\[
Z_0,\qquad 3Z_0,\qquad Z_0/3.
\]

This replaces remote phase-circle control with switching among three passive terminations. The assembled switch, leads, and terminations must be characterized at the target reference plane, either before embedding or through a genuine calibration connection. Component labels and DC resistance tolerances do not establish the required RF reflection coefficients.

The local receiver can be calibrated with reference-only readings, a power standard, and known test fields in two independent quadratures. The proof retains uncertainty in that calibration and requires a warranted stability allowance. A finite calibration fit does not establish unrestricted future stationarity.

Existing calibration software provides implementation support: scikit-rf implements calibration from measured standards and their known responses. It does not by itself supply adversarial uncertainty bounds for the assembled apparatus. [scikit-rf Documentation](https://scikit-rf.readthedocs.io/en/latest/tutorials/Calibration.html?utm_source=chatgpt.com)

No such physical calibration was performed here. The result supplies a construction for an instrumented target; it does not infer calibrated access to an existing uninstrumented hidden target.

### Shared calibration errors give a substantially better weak-target bound

A major extension emerged while checking the practical error budget. Treating every reference error as independent can charge the entire bright background against a weak target. That loses information about errors that remain common across the three load states.

The stronger receiver model is

\[
x_\ell=
\alpha h_{\zeta_\ell}
+\beta\overline{h_{\zeta_\ell}}
+b+e_\ell.
\]

Here:

- \(\alpha\) is a common complex gain;
- \(\beta\) is common quadrature leakage;
- \(b\) is a common offset;
- \(e_\ell\) contains readout error and all unshared drift.

Four fixed imperfect reference phasors produce precisely this form. The common offset cancels in the contrasts, and an unknown common phase does not change the recovered residue magnitude.

Suppose actual loads satisfy

\[
|\zeta_\ell-z_\ell|\le d_z,
\qquad
|\zeta_\ell|,|z_\ell|\le r_{\max}<1.
\]

Exact subtraction gives

\[
|h_\zeta-h_z|
\le p\,\lambda,
\qquad
\lambda=\frac{d_z}{(1-r_{\max})^2}.
\]

The background \(h_0\) is absent. Load uncertainty enters proportionally to the target signal.

With acquired bounds

\[
g_L\le|\alpha|\le g_U,\qquad |\beta|\le b_{\max},
\]

the clipped estimate \(\widetilde p\) obeys

\[
|\widetilde p-q|\le B+\Theta q,
\qquad q=|\alpha|p,
\]

where

\[
B=K_r\epsilon+\text{certified numerical allowance},
\]

\[
\Theta=
K_r\lambda\left(1+\frac{b_{\max}}{g_L}\right)
+\frac{1+7r^2}{1-r^2}\frac{b_{\max}}{g_L}.
\]

For \(\Theta<1\) and \(g_L>0\), this yields the acquired interval

\[
\boxed{
p\in
\left[
\frac{(\widetilde p-B)_+}{(1+\Theta)g_U},
\frac{\widetilde p+B}{(1-\Theta)g_L}
\right]\cap[0,1].
}
\]

For the tested scalar-gain case,

\[
r=\tfrac12,\quad
r_{\max}=0.51,\quad
d_z=0.001,\quad
[g_L,g_U]=[0.99,1.01],
\]

and \(\beta=0\),

\[
\Theta=\frac{115}{2401}\approx0.04790.
\]

Thus one-percent common gain uncertainty and a \(0.001\) load-reflection tolerance produce a finite **relative** calibration width. They do not automatically impose a background-sized absolute error floor.

Unshared drift still has to resolve the target signal. That requirement is essential: exact counterexamples show that unrestricted load-dependent reference phase can counterfeit a target.

The full result, including fixed I/Q imbalance and the correction from matched-target power to power absorbed in an imperfect final load, is in SHARED_CALIBRATION.md[SHARED_CALIBRATION.md](originals/SHARED_CALIBRATION.md).

## 4. Whole-Gram recovery and complete control

The new scalar oracle supports a uniform all-input reconstruction theorem.

Assume each acquired \(p(u)\) has simultaneous error at most \(\delta\). Acquire the \(n\) diagonal entries, select the largest acquired diagonal \(D\), and proceed as follows:

- If \(D\le4\delta\), return \(\widehat G=0\). Then \(\|G\|\le5n\delta\).
- Otherwise, use two quadrature queries per remaining coordinate to recover the selected column \(q=Ge_k\), and return \(\widehat q\widehat q^*/D\).

With

\[
e=\sqrt{8n-7}\,\delta,
\qquad
T_U=\sum_j(\widehat d_j+\delta),
\]

the nonzero branch has the acquired certificate

\[
\|\widehat G-G\|
\le
\frac{2\sqrt{(D+\delta)T_U}\,e+e^2}{D}
+\frac{T_U\delta}{D}
<11n\delta.
\]

Therefore

\[
\boxed{\|\widehat G-G\|\le11n\delta}
\]

uniformly, including a zero or unresolved source.

The schedule uses \(3n-2\) target-power queries, hence \(36n-24\) raw reference powers, with twelve additional readings for optional final verification. Its executable evidence is a 144-case exact oracle-level test using positive LDL pivots to certify the operator inequalities. Physical approximation of the ideal quadrature commands remains a charged error.

The complete control executions below use the conventional sequential two-mode controller, with separate acquired trace certification and final verification:

\[
n+4(n-1)+1=5n-3
\]

target-power queries, or

\[
60n-48\quad\text{readings plus twelve verification readings}.
\]

That is 444 readings for eight inputs and 144 for three inputs. Numerical eigensolvers only propose commands; rational checks certify their norm, optimization gap, preparation loss, and resulting control bound.

The reconstruction proof is in ALL_INPUT_GRAM.md[ALL_INPUT_GRAM.md](originals/ALL_INPUT_GRAM.md).

## 5. What the executed evidence supports

The following are **certified lower bounds on the fraction of the matched-target optimum**, rounded down. Errors are declared normalized absolute detector-power errors. The results concern the numerical sources and their synthetic acquisition conditions.

| Source and calibration conditions | Raw error \(\eta\) | Readings, including verification | Certified optimum fraction |
|---|---:|---:|---:|
| Eight-input rational source 120, ideal calibration | \(10^{-9}\) | 444 | 99.9999% |
| Same source, ideal calibration | \(10^{-5}\) | 444 | 99.3787% |
| Weak eight-input source 126, ideal calibration | \(10^{-9}\) | 444 | 99.9987% |
| Same weak source, ideal calibration | \(10^{-5}\) | 444 | 88.4580% |
| Intrinsically blind four-input source, new reference interface | \(10^{-9}\) | 204 | 99.9999% |
| IEEE-derived 30 GHz model, ideal calibration | \(10^{-7}\) | 144 | 92.3630% |
| Same IEEE-derived model, ideal calibration | \(10^{-10}\) | 144 | 99.9919% |
| IEEE-derived model, gain \([0.99,1.01]\) and load tolerance \(0.001\) throughout | \(10^{-7}\) | 144 | **82.2670%** |
| Weak source 126, same coarse calibration throughout | \(10^{-7}\) | 444 | **88.9459%** |
| Zero target and unresolved weak target, separate cases | \(10^{-9}\) | 204 each | 0% |

The coarse-calibration rows are complete acquisitions and controls with those tolerances applied throughout. They are not merely final verifications of commands selected with better calibration.

For the coarse-calibration IEEE run, the acquired delivered-power interval is

\[
[\,7.729163386366539\times10^{-5},
\;9.023751065532179\times10^{-5}\,].
\]

Its positive optimum-fraction certificate comes from acquired trace and final-power intervals. Its accumulated-regret certificate gives a zero fraction; that weaker result is retained in the saved output. Diagnostic source truth is not substituted for the acquired certificate.

The IEEE numerical model was used through the original loader without symmetrization, rescaling, projection, or interpolation. Its existing numerical reciprocity and passivity checks pass. **The underlying IEEE measurements are real source data; these runs are offline emulations of the unchanged numerical model.** They do not certify unknown device/model-fit uncertainty or demonstrate the load protocol on that device.

The evidence also includes:

- Replay of the original finite first-harmonic checks, with their floating-point scope stated.
- Separate exact rational identity checks.
- 303 exact algebra/clipping cases and sixteen complete scalar queries.
- Ten complete coherent control runs.
- Two complete controls with coarse shared calibration.
- Supplementary fixed I/Q imbalance and common-offset verification.
- Three finite-command control runs.
- Zero, unresolved, blind, and calibration-failure cases retained alongside successes.

Results and exact endpoints are saved in coherent_complete_control_results.json[coherent_complete_control_results.json](unacquired-archive/continuation/mechanisms/coherent_complete_control_results.json) and shared_calibration_full_control_results.json[shared_calibration_full_control_results.json](unacquired-archive/continuation/access/shared_calibration_full_control_results.json).

## 6. Important failures remain explicit

### Unknown target-load scale is an exact ambiguity

The transformation

\[
t'=ct,\qquad s'=c^2s,\qquad z'=z/c^2
\]

preserves every accessible complex response while multiplying matched-target power by \(c^2\), whenever both constructions remain passive.

An exact rational witness uses coupling \(1/4\) with loads \(z\), versus coupling \(1/2\) with loads \(z/4\). Their returns coincide, while matched-target powers are \(1/16\) and \(1/4\).

A known matched state alone does not remove this ambiguity. The coherent receiver cannot provide free target-load calibration.

### One nonzero known load is insufficient in general

The saved passive two-ports

\[
S_1=
\begin{pmatrix}0&1/4\\1/4&0\end{pmatrix},
\qquad
S_2=
\begin{pmatrix}0&1/5\\1/5&18/25\end{pmatrix}
\]

have identical complex returns at \(z=0\) and \(z=1/2\), but target powers \(1/16\) and \(1/25\). The state \(z=-1/2\) distinguishes them.

This supports retaining both nonzero load states in the general unknown-background construction.

### Reference commonality must be warranted

A target-free return with load-dependent reference phase can produce exactly the twelve powers expected from a passive nonzero target. A successful fit to the three-load model therefore cannot establish unrestricted phase stability.

A separate load-dependent gain example defeats the shared-calibration decoder. Its additional reference sums can expose that particular amplitude error, so the report does not mislabel it as full-transcript indistinguishability.

### Reciprocity and dynamics remain physical obligations

With distinct forward and return couplings, a scaling ambiguity preserves the return product while changing delivered power. The interpretation \(p=|a|\) needs reciprocity in compatible power-normalized ports.

Likewise, quiet accessible power does not establish that hidden energy has decayed. A stationary scattering matrix supplies no generic settling time.

These failures and the bounded-reference precision lower bound are preserved in NEW_LIMITS.md[NEW_LIMITS.md](originals/NEW_LIMITS.md).

## 7. Finite commands, time, and photons are charged

The finite-command implementation rounds coordinates and then applies a common inward attenuation. It verifies subunit norm exactly and charges

\[
2\|u_{\mathrm{actual}}-u_{\mathrm{proposed}}\|
\]

as a target-power preparation loss.

The correct resource description is **\(b\)-bit coordinate quantization plus a common \(b\)-bit attenuation setting**. Multiplying the two can require \(2b\) fractional bits, and the acquisition mixtures can require another bit. The report incorporates that review correction.

Fresh eight-input weak-source runs at \(\eta=10^{-7}\) certify 98.4624%, 99.8710%, and 99.8713% for \(b=12,24,40\), respectively, each using 444 readings.

For timing, the original finite-memory argument supplies an \(L^2\) bound over a certified flush block \(T\). It does not imply an arbitrary short-window pointwise bound. For a detector integration window \(W\), the continuation uses

\[
d_{\mathrm{window}}\le\sqrt{T/W}\,d_j.
\]

The simpler bound applies to complete \(T\) windows or integer multiples. The required \(T\) must include added receiver-path and relevant load delays.

For the explicit eight-input schedule at \(\eta=10^{-7}\), the conservative reset, settling, and integration ledger is \(2590T\), plus actuator latencies. No duration in seconds is inferred from the stationary backplane data.

Reference photons, signal photons during settling, combining loss, calibration exposures, switching, and reset illumination are separately charged. A conditional Poisson concentration calculation supplies a sufficient exposure for a simultaneous error budget, but **neither the old square-root nor the new linear bounded-error modulus is a photon lower bound**. In the dark family, direct counting and coherent-reference detection can both require order \(p^{-2}\) photons for fixed relative target-power precision. Universal photon superiority is not established.

## 8. Prior work, Astra reuse, and preservation of the original result

Three-load coherent hidden-port estimation is established prior work. In particular, *Virtual VNA* already uses known distinct target loads and coherent accessible measurements for hidden-port scattering recovery, and discusses the calibration problems caused by switches and connecting structures. I used that work to check the construction and its scope; this continuation makes no literature-wide priority claim. [arxiv.org](https://arxiv.org/html/2403.08074v3?utm_source=chatgpt.com)

Reciprocal programmable linear optics and calibrated switched-load backscatter also have existing physical precedents in Miller’s universal linear optical component work and NIST’s reference-modulation work. They support the choice of building blocks without validating the assembled tolerances assumed in these emulations. [ee.stanford.edu](https://ee.stanford.edu/~dabm/430.html?utm_source=chatgpt.com)

The contribution developed within this P1 continuation is the scalar target-power residue, its uniform bounded-error recovery, the shared-calibration interval, the all-input Gram theorem, and the finite certified control execution.

I read the selected current Astra material at commit `b2adf267d6341d66a643102658fbadeb01518301`. N997/N996 informed the acquired-interface distinctions; their full-vector and transpose operations were not assumed for intensity data. N1050 informed the instrument-gauge check. N1061 informed the same-loop reciprocity and hidden-settling obligations. Their different models and query counts were not imported as wave-power theorems.

All **111 original source files**, the supplied archive, and the completed report still match their recorded hashes. The original eleven-reading observable, \(55n-44\) plus eleven control count, both physical first-harmonic normalization roots, square-root bounded-error theorem, and unchanged OpenWFS comparator are preserved. The reported **407 versus 539** remains one matched eight-input instance, with no universal superiority claim.

The scoped reviews checked the arguments used here and resolved the timing, projection, finite-precision, and test-description issues described above. They are not an independent whole-proof audit of the original archive.

The completed package can be reproduced with:

```bash
python continuation/run_reproduce.py
```

Its next physical requirement is experimentally warranted tag calibration, shared receiver stability, and a settling envelope for an assembled instrument. The present work specifies what those measurements must establish and how their residual uncertainty enters the certificate. No equipment operation, purchase, outreach, P1 role replacement, or additional Pro experiment was performed.