# Finite photon readout, mean reference and cycle-affinity confidence

27 October2026. This is a positive conditional acquisition/inference operation. It does not claim that a real instrument has supplied the contracts below. The source-affinity theorem is in `SPECTRAL_AFFINITY_THEOREM.md` and has received a completed independent root mathematical review. This note supplies the distinct photon/statistical bridge.

## Physical/record operation

The source is the stationary finite-state, all-even, bidirectional irreducible Markov system of the theorem. Its nonnegative instantaneous emission intensities are arbitrary unknown state functions f_i(X_t). A common passive readout shutter w(t)>=0 gates the emitted signal **before** the separate unknown temporal responses. The shutter must not perturb the source dynamics. This is an acquisition promise, not a conclusion from detecting photons.

Conditional on the whole source path, channel i is an independent Poisson counting process with intensity

`lambda_i(t|X)=b_i(t)+[h_i*(w f_i(X))](t)`.

Here h_i is a fixed nonnegative causal response/delay kernel of finite total gain eta_i. In this note **b_i(t) is a deterministic intensity waveform**, repeated identically between on/dark conditions; the resulting background Poisson processes are independent between channels and independent of X. Random background intensity paths are not included in the displayed covariance equality: they would contribute an additional diagonal intensity-variance term and need conditioning/pathwise ceilings. An ideal passive detector has eta_i<=1; another known gain upper bound may be used instead. Detector dead time, saturation, feedback, source-dependent backgrounds and correlated read noise are not granted this conditional Poisson/linear-mean model.

Capture the complete response with zero prior source memory, or charge an acquired initial/tail error. For a hard response support [0,L], a source gate supported in [0,T] requires output acquisition through T+L. A long finite capture is not exact for an unspecified infinite tail.

At analysis frequency v define the physical gated Fourier integral `Z_i=integral w(t)f_i(X_t)exp(i v t)dt` and the measured event phasor `Y_i=sum_events exp(i v t_event)`. Conditional Poisson integration gives

`E[Y_i|X]=H_i(v) Z_i+B_i(v)`,

`Cov(Y)=diag(H) Cov(Z) diag(H)^dagger+diag(E total_count_i)`.

The diagonal term is real nonnegative even though photon paths are non-Gaussian. Thus the uniform Markov spectral cone survives. A full detector-noise reversal law is unnecessary for this covariance/affinity operation. Conversely arbitrary real correlated noise added after distinct unknown filters cannot be pulled back as real noise and is outside the promise. Shared real noise **before** the filters is a different case.

## The gate gives an ordinary phase reference

Let mu_i=E f_i(X)>0, and let W(v)=integral w(t)exp(i v t)dt. Interleave dark records using the same output observation interval and an input shutter identically zero. Their mean background is the same B_i. Therefore

`m_i:=E[Y_i,on]-E[Y_i,dark]=mu_i H_i(v) W(v)`.

Unknown source brightness cancels from phase calibration: `arg(m_i)-arg(m_j)=arg(H_i)-arg(H_j)`. The common W phase cancels. When DC quantities are also estimated, `(m_i(v)/m_i(0))*(W(0)/W(v))=H_i(v)/H_i(0)` identifies the normalized transfer response. These are ordinary mean-response/lock-in calibration facts; the gate does not leave its available calibration information hidden from a comparator.

Nonzero W, nonzero source means and adequate phase precision are essential. A rectangular long gate at fixed v has bounded Fourier mean and sinc zeros; exact normalization is not free acquisition. The executed calculation uses two common short nonnegative windows separated by a quarter analysis period, making W nonzero. A properly paid modulated calibration window is another ordinary option. Different per-channel windows cannot be silently substituted for this common gate.

For two channels, let C=Cov(Y), or any positive real diagonal rescaling and common multiple of it. Then

`P=C12*conj(m1)*m2`

has imaginary part equal to `|m1 m2| Im(C12 exp[-i arg(H1)+i arg(H2)])`. The mean-referenced imaginary coherence

`q=|Im P|/[|m1 m2| sqrt(C11 C22)]`

is no larger than the canonical imaginary radius r of the actual phase-corrected covariance. The source theorem gives

**`Amax >= 2pi*q/sqrt(1-q^2)`**.

This two-channel operation uses first moments supplied by the actual gate. The strongest ordinary method receives those same means and can exploit the same calibration. It is not a statistical superiority claim for blind three-channel closure. The physical target is **maximum microscopic cycle affinity**, not entropy production per unit time.

## Centering and an eight-component data block

Use two independent bright records a,b and one independent dark record d per statistical block. Define

`D_i=Y_i^a-Y_i^b`,

`M_i=(Y_i^a+Y_i^b)/2-Y_i^d`,

`W_ij=D_i D_j*`.

Then E M_i=m_i and E W_ij=2Cov(Y)_ij. No population mean or source label is supplied to the covariance estimator. Mean and covariance estimators share data; they need not be independent after a simultaneous confidence construction. For two channels the real coordinates are Re/Im M1,M2 (four), W11,W22 (two), and Re/Im W12 (two): J=8, not nine or twelve.

## Known photon envelopes, not observed maxima

Acquire upper bounds Lambda_i,on and Lambda_i,dark on each record's **conditional total photon mean**. For example, a known intensity ceiling F_i, gain ceiling G_i, gate area integral w, and background ceiling give

`Lambda_i,on <= F_i G_i integral w + integral b_i`,

with the appropriate finite output interval for background counts. These ceilings are external inputs, not maxima inferred from the same finite record. Conditional independence implies that each block's total count P_i=N_i^a+N_i^b+N_i^d can be coupled below independent Poisson dominators Q_i of mean

`ell_i=2Lambda_i,on+Lambda_i,dark`.

The construction is valid even though source intensity fluctuations correlate channels: conditional on all source paths, add independent Poisson counts to bring each conditional mean up to the fixed ell_i. The resulting joint dominator law is a product with no dependence on those source paths.

Choose integer cutoffs K_i **before calibration data**, and zero the entire block's feature matrix/means if any P_i>K_i. This is a statistical estimator, not physical detector saturation. Dividing M_i by K_i and W_ij by K_i K_j makes mean and off-diagonal real/imaginary coordinates lie in [-1,1], and diagonal coordinates in [0,1]. Clipping can change physical asymmetry; the following tail bias explicitly restores the **unclipped** target. The clipped covariance is not simply declared to obey the physical cone.

Write `Q_i~Pois(ell_i)` and define

`p0_i=Pr(Q_i>K_i)`,

`p1_i=ell_i Pr(Q_i>=K_i)`,

`p2_i=ell_i^2 Pr(Q_i>=K_i-1)+ell_i Pr(Q_i>=K_i)`.

Union bounds and Poisson factorial moments give the complex mean bias bound

`tM_i=[p1_i+ell_i sum_(k!=i) p0_k]/K_i`,

the diagonal covariance bias bound

`tC_ii=[p2_i+(ell_i^2+ell_i)sum_(k!=i)p0_k]/K_i^2`,

and for i!=j the off-diagonal complex bias bound

`tC_ij=[p1_i ell_j+ell_i p1_j+ell_i ell_j sum_(k!=i,j)p0_k]/(K_i K_j)`.

All are upper bounds; overlaps are not subtracted. No independence of the actual source-controlled counts is used beyond the justified dominator coupling.

The planning code bounds a Poisson tail without floating exp: for rational ell and k>ell,

`Pr(Pois(ell)>=k) <= [ell^k/k!]/[(1-ell/(k+1))*sum_(j=0)^J ell^j/j!]`.

This uses a finite Taylor lower bound on exp(ell) and a geometric upper bound for the remaining tail. The computed count-tail bounds are exact rational numbers. Choosing the cutoff from these known inputs does not use hidden source-state information.

## Simultaneous finite confidence

For **N>=2** independent clipped blocks, let theta_hat_j and s_j^2 be each coordinate's empirical mean and unbiased sample variance, and R_j its range length (2 or1 above). The established Maurer–Pontil2009 Theorem4, applied to both signs and unioned over J=8 coordinates, gives the radius

`e_j=sqrt[2 s_j^2 log(4J/alpha_stat)/N]+7 R_j log(4J/alpha_stat)/[3(N-1)]`.

With probability at least 1-alpha_stat all coordinates are covered simultaneously. The variance is data-derived. The private population model in the resource calculation is not an inference input.

For a complex mean, combine its two statistical radii as `sqrt(e_Re^2+e_Im^2)` and add tM_i. For C12 do the same and add tC_12. For diagonal Cii use upper bound `C_hat_ii+e_ii+tC_ii`. Unknown source/photon-count means have not been plugged in as if measured.

If timestamps/phasor arithmetic add an acquired per-photon error eta, use coded phasors of modulus<=1. On retained blocks the normalized mean feature error is <=eta, and covariance feature error <=2eta, by the product difference identity and count bounds. Add these to the respective bias radii. Unqualified clock errors, record-dependent gains or gate mismatch are not assigned eta=0 for free. Outward-rounded arithmetic is needed for a machine-certified numerical certificate; the present resource script is explicitly numerical planning, not such a certificate.

For the alternative ordinary median-of-means compiler, the acquired count ceilings also give finite fourth-moment bounds. It avoids truncation bias but may be much more conservative when it uses only worst-case intensity caps. It is an established comparator, not a new bound. The strongest ordinary implementation may use the same clipped empirical-Bernstein scheme as this protocol; there is no algorithmic resource separation claimed.

## Confidence disks to an affinity certificate

Let a=C_hat12, b=conj(m_hat1), c=m_hat2, with complex error radii e_a,e_b,e_c. Let u_a=|a| etc, using certified upper magnitudes in an exact implementation. Set

`Eprod=(u_a+e_a)(u_b+e_b)(u_c+e_c)-u_a u_b u_c`,

`L=max(0,|Im(abc)|-Eprod)`.

Let d_i be the diagonal upper confidence bounds. If the mean/variance guards are valid, the sufficient radius lower bound is

`q_lower=L/[(u_b+e_b)(u_c+e_c)sqrt(d_1 d_2)]`.

The three-factor error bound includes all covariance/mean dependencies through simultaneous disks. It is not a product of independent marginal confidence claims. Then return `2pi*q_lower/sqrt(1-q_lower^2)`. Zero-containing mean disks or nonpositive variances give UNKNOWN/no positive certificate. A computed lower radius>=1 indicates an inconsistent moment/PSD set, not permission to clip it to a spectacular finite bound. Positive real channel normalizations and the common factor2 in E DD^dagger do not change the operation.

## Tail, preparation and total acquisition bills

Hard support and a cleared detector permit exact complete capture. With an acquired response-tail mass bound zeta_i(L), full source photons missed after T+L have mean at most `F_i integral(w) zeta_i(L)` per bright record. A union budget for all records can make the probability of **any** missed source photon <=alpha_capture. Initial residual detector memory requires its own dark-washout bound or an explicit reset. These are not inferred from the apparent absence of late counts.

True independent stationary trials may be supplied by a qualified preparation operation, with its cost. Alternatively a separately acquired stationary absolute-regularity envelope beta(R) permits gaps R between bright source windows; coupling to IID blocks costs at most the sum of the beta gaps. An initial-state convergence envelope prices stationary preparation. Finite irreducibility alone does not acquire either envelope, and no microscopic state label or free rare reset is substituted for them.

In the executed planning choice, alpha_stat=.01, total source coupling failure=.005, and initial stationary-preparation failure=.005. With exact hard-support/unit-latency readout and no other errors this gives **98% confidence**, not99%. The separate beta=.1 variance event is used only for the power/resource calculation and is not another confidence-coverage input. A general implementation adds actual tail/readout/setup failure budgets too.

## What was actually computed

`cox_acquisition_planning.py` reuses the accepted four-state rare-cycle family solely as a declared population model. Two common shutter windows have width .01, separation .18, and carrier v=pi/(2*.18). Maximum brightness gives20 expected photons per open window at a maximally bright state. These quantities are model source-time units and photon numbers, not acquired hardware specifications.

The script integrates the exact state-resolved Feynman–Kac moment hierarchy through order4. An independent analytic two-window covariance formula checks it. It generates **no random records**. Exact rational Poisson tails set cutoff144 from the maximum block mean80. Population moments only bound the power of a data-variance-based confidence algorithm; they are not fed into a purported observed-data confidence statement.

Planning assumes unknown pure channel latencies within .12, unit efficiency and zero dark background. General attenuating H can leave the theorem valid but remove the .05 floor altogether; no uniform power over unknown gain/efficiency is asserted. Dark readout can occupy a paid source mixing gap when the schedule is long enough; it is still acquired, counted and subjected to its required moment/noise contract.

Numeric planning gives approximately1.37M blocks at active fraction .5,4.68M at .1, and44.2M at .01 for the displayed .05 floor. This requires2N bright plus N dark records, about55M,200M and2.09B model source-time units, respectively, and roughly24–37M signal photons. The constant point-information floor does not remove rare-activity acquisition. The worst-cap MOM calculation is more conservative and has a stronger power receipt in the present code; it is not presented as a matched-power algorithmic speedup. The strongest ordinary comparator may choose empirical Bernstein too.

These are **numerical population-power/resource diagnostics**, not rigorously rounded power certificates, simulated experimental success, physical timings or acquired-data inference. No max-cycle-affinity estimate has been certified from real photons. The finite readout/centering/mean-calibration/tail/confidence mathematics is the positive operation; actual device linearity, common gating, response support/tails, source stationarity/mixing and practical advantage remain unacquired.
