# Independent audit: physical-flat mixed-reset Helstrom capability

**PASS**, 2026-10-26. Governing `physical_flat_mixed_reset_helstrom_capability.md`, Sections 1–5. Checked the actual noncommuting positive-mixture dependency `white_noise_stability_operator_bath_lifting_theorem.md`, rather than assuming scalar diagonalization.

## Exact source measure, including singular endpoints

The operator-bath lift applies with base A0=Phi3, bath coefficient C=X=p sigma, and baseline B=Y=q eta/9. It gives an EXACT identity Delta=integral h(s)dmu(s), not only a bound. Its alternate deficit convention f(A)+f(EA)-2f(NA) agrees with the normalized/unscaled-WH convention used here. The lift's spectral counting equality follows from congruence: the number of eigenvalues of C^(1/2)(B+uI)^(-1)C^(1/2) above z is the number of positive eigenvalues of C/z-B-uI. Integrating in u gives Tr(C/z-B)_+. Thus the source-derived measure is legitimate for noncommuting and singular baths; it does not describe one simultaneously realizable classical experiment.

Extend Q(t)=Tr(tX-Y)_+ by zero to t<0. Its distributional second derivative is a positive measure on [0,infinity), with atom Q'(0+) at zero. Convexity and Q(t)/t ->TrX give total mass p. Integrating twice yields Q(t)=integral(t-s)_+dmu(s). The lift's integration-by-parts boundaries are received by h(infinity)=0 and h(0)=Delta(Phi3)=0, with the zero atom still retained for the mass identity.

The note correctly uses a first-moment INEQUALITY, not an unjustified equality: tp-Q(t)=integral min(t,s)dmu(s)<=TrY. Monotone convergence gives integral s dmu<=q/9, hence integral(1+9s)dmu<=1. Missing Y-only support contributes no finite-slope mass and need not saturate this bound.

The Helstrom identity is exact: e=p-Tr(X-9Y)_+=p-9Q(1/9)=integral min(1,9s)dmu(s). Zero atoms contribute zero to both h and the error; p=0 gives the zero measure, while q=0 gives p times the atom at zero. All pure, orthogonal-support and singular cases are therefore received without inverse eigenvalues.

## Scalar payment and Cauchy-Schwarz

The actual scalar curve h(s)=Delta(Phi3+sI9) equals the displayed four-term entropy expression. Differentiating D(x,s) in x gives log[(x+s)(x+9s)/(x+3s)^2], and D(0,s)=0. Thus its integral from x=0 to1 is exactly (6). The bound log(1+u)>=u/(1+u), followed by (x+s)(x+9s)<=(1+s)(1+9s), yields h(s)>=2s/[(1+s)(1+9s)].

For s<=1/9, the ratio to min(1,9s)^2/(1+9s) is 2/[81s(1+s)], minimized at s=1/9 with value1/5. For s>=1/9 it is 2s/(1+s), likewise minimized there with value1/5. The zero endpoint is continuous. Weighted Cauchy-Schwarz using the received moment bound therefore gives e^2<=5Delta, with no dimension factor.

## Actual output instrument and access

The logical Helstrom effect is an actual measurement on the accessible output logical system. With alpha=pTr((I-M)sigma), beta=qTr(M eta), the postmeasurement/discarded-logical qutrit maps are exactly (p-alpha)id+beta R0 and alpha id+(q-beta)R0. Noncommutativity of sigma,eta causes no change to these scalar Born coefficients. The full original channel—not a hidden success/reset label—is measured.

The two map errors are opposites, so their classical direct sum has diamond norm exactly twice ||beta R0-alpha id||_diamond, bounded by2(alpha+beta)=2e. This includes arbitrary input ancillas. If desired, reset preparation on the failure output is an additional common CPTP postprocessing and cannot worsen this bound. For p>e the actual success probability is at least p-e; normalized successful outputs obey the stated2e/(p-e) trace bound. An output isometry V is inverted on its range and completed trace preservingly elsewhere. The construction requires the discrimination data, not only the entropy value.

## Sharp exponent, even for arbitrary output decoders

For sigma=eta=1, the channel is qutrit depolarization. Around p=0 its Choi/source perturbation has squared Hilbert-Schmidt norm8p^2/9, while its WH output perturbation has2p^2/9. The entropy Hessian at I9/9 is9 times identity, giving Delta=2p^2+O(p^3).

The Haar identity integral P_psi tensor P_bar(psi)=(I9+3Phi3)/12 gives a separable Choi state at p=1/4; convex interpolation with I9/9 covers0<=p<=1/4. Any reference-only output instrument preserves separability of its possibly subnormalized success block C_s. The witness W=I9/3-Phi3 has nonnegative expectation on such blocks, expectation -2p/3 on pPhi3, and operator norm2/3. Trace duality yields ||C_s-pPhi3||_1>=p. A maximally entangled input and success-block selection give the same lower bound for the full instrument diamond error. Therefore no exponent above1/2 can hold with the specified actual target success probability p, even for arbitrary physical-output decoders. Constants are not claimed optimal.

## Scope and replay

The value class was already covered by the operator-bath theorem; the new result is the dimension-free Bayes-error and actual heralded-instrument capability. It does not imply that unmeasured logical states become orthogonal at this rate, or cover arbitrary physically nonflat mixed reset states. No hidden Kraus label or measurement-cost claim is introduced.

Replayed the author's checker from the quantum-folder working directory:120 complex cases PASS, plus the depolarizing small-p asymptotic tending to coefficient2. Analytic measure and instrument receiving above are controlling evidence.

## Later fixed-success sharpness refinement

Also PASS: take fixed p=q=1/2, sigma_r=diag(1-r,r), eta=diag(0,1). The actual accessible logical direct sum has a reversible block of mass p(1-r) and a depolarizing block of mass q+pr with success fraction pr/(q+pr). Homogeneous additivity gives Delta=2p^2r^2/q+O(r^3), while the logical Bayes error is exactly pr for small r.

The second block is entanglement breaking for sufficiently small r. Under ANY output success decoder its contribution has nonnegative expectation against W=I9/3-Phi3. The first block's successful Choi contribution has trace at most p(1-r), hence W expectation at least -(2/3)p(1-r). Linearity applies even if the decoder does not explicitly measure the logical block. Comparison with target pPhi3 therefore leaves a witness gap >=2pr/3, giving successful-block trace distance and full instrument diamond distance >=pr. This proves square-root exponent sharpness while keeping the target success probability fixed away from zero; the lower bound is not merely a vanishing-success artifact.
