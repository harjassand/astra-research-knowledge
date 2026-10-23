# Independent check of the binary-port finite-cycle certificate

**Verdict: the sign certificate passes.** The interval enclosure proves the stipulated model's exact periodic **work on** is negative, hence the field controller receives positive work. I found no mathematical sign gap in the contraction, residual, rate-derivative, normalization, or work-integral steps.

Audited inputs:

- `work/opportunity_kinetics/lead/binary_port_finite_cycle.py`, SHA-256 `011bc3fc0167304172bbd34d5f031cea788a5e432d47f9956e9f0ba0c448f9eb`.
- `work/opportunity_kinetics/lead/binary_cycle_certified.json`, SHA-256 `a61d2b75d3f1491a377c395f6d61274383f320e9b16a2c0095a3c63d9eb60c34`.

The independent interval recomputation is executable as [binary_certificate_independent_audit.py](binary_certificate_independent_audit.py). It reconstructs the proposed nodes, then separately recomputes interval residuals, rate-derivative bounds, the contraction estimate, and the exact piecewise-linear work integral; it does not call the source's `interval_certificate` routine.

## Proof checks

The geometric model has `f=(1,0,0)`, maximum baseline exit rate (D_0=26/25=1.04), minimum baseline off-diagonal rate (m_0=1/1000), and (|f_i-f_j|\le1). For amplitude (A=0.3), every off-diagonal rate is at least (m=m_0e^{-A/2}), while the exit rate is at most (D_0e^{A/2}). The independent interval run gives

\[
3m\ge0.00258212392927517,
\quad D_{\max}\le1.04e^{0.15},
\quad \|\dot Q\|_1\le D_{\max} A\nu,
\quad \|\ddot Q\|_1\le D_{\max}\nu^2(A+A^2/2).
\]

At ν=0.01 the last two upper bounds are (0.00362492283731225) and (0.000041686612629091). These follow by differentiating (q_{ji}=q^0_{ji}e^{h(f_j-f_i)/2}) and using the column-induced matrix 1-norm: a generator column contributes twice its total outgoing-rate derivative. The time-varying CTMC is contractive on zero-sum vectors at rate (3m), by splitting off the complete-graph generator with every directed off-diagonal rate (m).

For each periodic linear segment (\tilde p), define (r=\dot{\tilde p}-Q\tilde p). The audit checks the Taylor estimate

\[
\|r(t)\|_1\le \|r(t_m)\|_1+\delta\|\dot r(t_m)\|_1
+\frac{\delta^2}{2}\bigl(\|\ddot Q\|_1+2\|\dot Q\|_1\|\dot{\tilde p}\|_1\bigr),
\qquad \delta=\Delta t/2.
\]

Here Δt is the **time** interval; the phase half-width is νΔt/2. The independently recomputed maxima match the certificate to its displayed precision: midpoint residual (2.769324284532664\times10^{-9}), midpoint residual-derivative (4.590655234565644\times10^{-6}), slope norm (4.479991875832982\times10^{-4}), and global residual (2.100383732795999\times10^{-7}). Periodic normalized exact probability (p) and (\tilde p) differ by at most (r_{\max}/(3m)\le8.134325812107\times10^{-5}) in (\ell_1).

For node construction, the first two stored binary64 coordinates are interpreted as exact dyadic rationals and the third is defined as the exact complement (1-p_0-p_1). Thus every proposed node is exactly normalized and periodic; all endpoints are positive, and linear interpolation preserves positivity. The independent checker verifies this complement construction at every node.

The work integral is also correct. With (h=A\cos(\nu t)), (\dot W_{\rm on}=-\dot h\,p_0). On a segment of time half-width δ, midpoint phase θ, and linear slope (s_0=\dot{\tilde p}_0), its exact contribution is

\[
2A\left[\bar p_0\sin\theta\sin(\nu\delta)
+s_0\cos\theta\left(\frac{\sin(\nu\delta)}{\nu}-\delta\cos(\nu\delta)\right)\right].
\]

This confirms the source's use of `half=dt/2` in time units and `sinhalf=sin(nu*half)`. The independent sum gives the same profile-work interval, 
\([-0.000746268657873633,-0.000746268657873632]\). Since (\|f\|_\infty=1) and (\int_0^T|\dot h|dt=4A), the work error is at most (4A r_{\max}/(3m)\le0.000097611909745274). Therefore

\[
W_{\rm on}\in[-0.000843880567619,-0.000648656748128]<0.
\]

The certificate establishes positive work delivered to the controller, not positive work on the system. It charges chemical work separately and scopes out any kinetic-barrier actuator cost.

## Reproducibility limitation

The JSON stores the interval summary but not the 8193 exact dyadic node pairs or their hash. My audit deterministically reconstructed those nodes with the pinned script's RK4 candidate generator and independently checked the interval proof. A detached verifier would need either the same generator/version or a future certificate that includes the exact node payload and hash; this is a packaging gap, not a defect in the verified inequality for the reconstructed candidate.
