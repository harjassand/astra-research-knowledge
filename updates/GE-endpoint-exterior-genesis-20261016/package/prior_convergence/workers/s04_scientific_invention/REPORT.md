# Frontier B investigation: loss-echo tomography of hidden kinetics

**Decision (2026-10-16):** A precise, internally proved structural-identification operation was found. It does **not** yet establish a new scientific capability. The algebraic core is close to established bilinear/switched-system realization, a closely related ion-trap experiment already extracts two-isomer rates using stronger spectroscopy, and the required continuous state-dependent loss field and useful finite-noise precision have not been demonstrated. Status: **internal theorem and exact replay; novelty unproved; physical acquisition unproved; consequential capability NOT ACHIEVED.**

## Chosen operation and the unavailable measurement

A conservative hidden kinetic network can be invisible to total-population measurement. Let \(x(t)\in\mathbb R^n\) be state populations, \(A\) an unknown continuous-time Markov generator in the **column** convention (nonnegative off-diagonal entries, \(\mathbf1^TA=0\)), and \(b\) a nonzero normalized initial distribution. Without perturbation, the sole output \(y(t)=\mathbf1^T e^{At}b=1\) carries no information about internal rates.

The proposed physical operation turns on a *single* fixed field that removes surviving material at unknown, state-dependent effective rates \(D=\operatorname{diag}(d_1,\ldots,d_n)\), and then turns it off. When on, the generator is \(M=A-D\); when off, it is \(A\). The only readout is the fraction surviving, \(\mathbf1^Tx\). This does not assume an ability to address each hidden state, measure its population, or know any \(d_i\). It does require a genuinely controlled loss field whose action is diagonal and constant during an assay. The \(d_i\) are **effective loss rates at that setting**; absolute optical cross sections would additionally require calibrated field intensity.

One on interval followed by darkness is insufficient in general: after the field turns off, the output remains \(\mathbf1^T e^{M t}b\) by conservation. A second on interval reads the hidden redistribution that happened during the dark period. The measured two-pulse response is

\[
Y(t_1,\tau,t_2)=\mathbf1^T e^{M t_2}e^{A\tau}e^{M t_1}b.
\]

This is a loss-based pump/dark/probe experiment, with the *same fixed* loss setting for pump and probe and only aggregate survival measured. If an instrument could produce its assumed field without changing \(A\), it would make hidden rate estimation possible in a class where the unperturbed total count is exactly flat. That is a mathematical capability conditional on the instrument, not evidence that such an instrument was built or that the rate estimation beats existing methods.

## Exact finite-moment theorem

Assume \((M,b,\mathbf1^T)\) is a minimal ordinary linear realization, meaning

\[
C=[b,Mb,\ldots,M^{n-1}b],\qquad
O=\begin{bmatrix}\mathbf1^T\\\mathbf1^TM\\\vdots\\\mathbf1^TM^{n-1}\end{bmatrix}
\]

are both nonsingular. Assume the effective loss rates \(d_i\) are pairwise distinct and the state model really is a conservative \(A\) plus diagonal loss. Then all parameters \((A,D,b)\) are exactly identifiable from the one-pulse curve \(\mathbf1^T e^{Mt}b\) and the two-pulse response \(Y(t_1,\tau,t_2)\), **up to permutation of hidden state labels**. No separate loss-rate calibration and no pure-state preparation are needed within this ideal theorem. If \(n\) is not supplied, exact one-pulse data reveal it as the Hankel rank under the same minimality assumption.

The finite algebraic data needed are derivatives of total order at most \(2n-1\):

\[
H_{ij}=\mathbf1^TM^{i+j}b,\quad
H^M_{ij}=\mathbf1^TM^{i+j+1}b,\quad
K_{ij}=\mathbf1^TM^i A M^j b,
\qquad 0\le i,j<n.
\]

The first two matrices come from one-pulse time derivatives. The third is the \(\partial_{t_2}^i\partial_\tau\partial_{t_1}^j\) derivative of \(Y\) at zero durations. Since \(H=OC\), \(H^M=OMC\), and \(K=OAC\),

\[
\widehat M=H^{-1}H^M=C^{-1}MC,\qquad
\widehat A=H^{-1}K=C^{-1}AC,\qquad
\widehat D=\widehat A-\widehat M=C^{-1}DC.
\]

Likewise \(\widehat b=H^{-1}(\mathbf1^TM^i b)_{i=0}^{n-1}=C^{-1}b\) and \(\widehat c=\mathbf1^TC\). Distinct eigenvalues of \(\widehat D\) yield its physical state axes. Each eigenvector has a unique scaling for which \(\widehat c\) evaluates to one, because in physical coordinates \(\mathbf1^Te_i=1\). The only residual freedom is eigenvector ordering, i.e. state permutation. This also proves uniqueness against any competing \(n\)-state model satisfying the assumptions. If a competing model has a different minimal dimension, its one-pulse Hankel rank differs.

The theorem is sharp about some assumptions. Uniform loss \(D=dI\) gives \(y(t)=e^{-dt}\) under any on/off schedule, independent of \(A\). Repeated or nearly repeated \(d_i\) lose or badly condition state labels. Failure of \(C\) or \(O\) loses reachable or observable modes. The theorem does not map recovered mathematical states to chemical structures; independent spectroscopy or chemistry is needed for that interpretation.

### Finite-time version without derivative estimation

There is an exact grid-sampling variant. Choose on-grid step \(h>0\), one fixed dark interval \(\ell>0\), and write \(P=e^{Mh}\), \(Q=e^{A\ell}\). Measure the one-pulse probabilities \(v_k=\mathbf1^TP^kb\) at \(k=1,\ldots,2n-1\), with \(v_0=1\) known. Also measure \(w_{ij}=\mathbf1^TP^iQP^jb\) for \(0\le i,j<n\); its \(i=0\) row equals \(v_j\) by conservation, leaving \(n(n-1)\) genuinely new two-pulse settings. Form \(H_{ij}=v_{i+j}\), \(H^P_{ij}=v_{i+j+1}\), and \(K^Q_{ij}=w_{ij}\). If the sampled \((P,b,\mathbf1^T)\) is minimal, then \(H^{-1}H^P=C_P^{-1}PC_P\) and \(H^{-1}K^Q=C_P^{-1}QC_P\), where \(C_P=[b,Pb,\ldots,P^{n-1}b]\). If every eigenvalue of \(M\) lies in \(|\operatorname{Im}\lambda|<\pi/h\) and every eigenvalue of \(A\) lies in \(|\operatorname{Im}\lambda|<\pi/\ell\), principal matrix logarithms recover \(M\) and \(A\) in that same basis, followed by \(D=A-M\) and the same eigenvector normalization. These nonaliasing bounds are substantive prior rate/timing information, and an unfortunate sample grid can make \(H\) singular or badly conditioned even when the continuous-time model is minimal.

The total number of nonduplicate nonzero-time scalar probabilities is \((2n-1)+n(n-1)=n^2+n-1\), matching the free-parameter count of a fully connected \(A\), diagonal \(D\), and unknown normalized \(b\). This equality is a noiseless algebraic count, **not** an efficiency or sample-complexity claim. In the three-state fixture, [`two_pulse_finite_time_replay.py`](two_pulse_finite_time_replay.py) uses \(h=\ell=0.2\) and exactly 5 one-pulse plus 6 new two-pulse settings; it reconstructs \(A,D,b\) to \(2.5\times10^{-12}\) numerical absolute error, while \(\kappa(H)\approx1.21\times10^4\), already warning of severe noise amplification.

The warning becomes decisive for this *minimal grid* under counting noise. With unknown \(b=(0.5,0.3,0.2)\), the same \(A,D\), and 11 log-rate/log-loss/logit coordinates, [`two_pulse_minimal_fisher.py`](two_pulse_minimal_fisher.py) gives a smallest per-setting Bernoulli-weighted singular sensitivity of \(1.94\times10^{-7}\) and condition \(7.39\times10^6\). The local Cramér–Rao calculation would require about \(2.65\times10^{15}\) independent outcomes **per setting** for 0.1 one-sigma precision along its weakest parameter combination. This is one synthetic, deliberately compact design, not a universal lower bound or a statement about an optimized rich time grid. It rules out promoting the exact parameter-count match into a practical efficiency claim.

A broader but still unoptimized 180-schedule grid does not rescue this fixture in the same local-count model. [`two_pulse_rich_fisher.py`](two_pulse_rich_fisher.py) gives minimum weighted sensitivity \(4.71\times10^{-5}\) for \(D=(2,3,5)\), implying about \(4.50\times10^{10}\) independent outcomes per setting for 0.1 local one-sigma precision along the weakest direction. A more separated synthetic field \(D=(0.2,3,15)\) with correspondingly shorter on-times raises that sensitivity to \(7.82\times10^{-4}\), but still implies about \(1.64\times10^8\) outcomes per setting. These numbers are local Cramér–Rao calculations for two fixed designs, not universal impossibility claims; another field, topology, prior constraint, or optimized design may change them. They do show that an exact observable-rank theorem is far from useful all-rate precision in these examples.

If one **supplies a pure initial state** and the strongly separated field \(D=(0.2,3,15)\), the same script gives weighted sensitivity \(0.0140\), corresponding to about \(5.08\times10^5\) outcomes per setting for 0.1 local precision in its weakest direction. That substantial improvement depends on an independently acquired preparation capability and still totals roughly 91 million independent outcomes over 180 settings. It cannot be attributed to the total-survival readout alone.

### Sharp single-pulse failure

For \(n=2\), start in state 1, take \(A=\begin{psmallmatrix}-a&r\\a&-r\end{psmallmatrix}\), \(D=\operatorname{diag}(d_1,d_2)\), and fixed on amplitude one. Both positive models

\[
(a,r,d_1,d_2)=(2,1,2,3)\quad\text{and}\quad(1,1,2,4)
\]

have the **same entire** one-pulse Laplace response \(\mathbf1^T(sI-M)^{-1}e_1=(s+6)/(s^2+8s+14)\), although their internal rates differ. Their two-pulse mixed derivative \(\mathbf1^TMAMe_1\) is respectively 10 and 8. Thus the dark interval plus second loss interval adds a genuine discriminator at one fixed field setting. This does not imply that two pulses are superior to every other experiment: with two *known relative* field amplitudes, the two-state constant-dose rational functions already identify the four parameters algebraically.

Specifically, with a calibrated relative dose \(u\), the two-state constant-dose transform is
\[
Y_u(s)=\frac{s+q+u d_2}{s^2+s[q+u(d_1+d_2)]+u(a d_2+r d_1)+u^2d_1d_2},\qquad q=a+r.
\]
If \(N_u\) is its numerator constant and \(B_u,C_u\) are its denominator's linear and constant coefficients, then \(d_1=(B_u-N_u)/u\), \(d_2=(N_{u_2}-N_{u_1})/(u_2-u_1)\), \(q=N_u-ud_2\), \(m=(C_u-u^2d_1d_2)/u\), \(a=(m-qd_1)/(d_2-d_1)\), and \(r=q-a\). These formulas require \(d_1\ne d_2\) and a minimal two-state transfer; they demonstrate the strongest simple alternative when dose calibration is available.

### Broader all-sequence result

Even when the ordinary triple \((M,b,\mathbf1^T)\) is nonminimal, if \(D\) has distinct entries and every state is reachable in the directed graph of \(A\) from the support of \(b\), arbitrary on/off pulse sequences identify \((A,D,b)\) up to permutation in the ideal all-data limit. Derivatives in segment durations give all word moments \(\mathbf1^T W(A,D)b\). Rows \(\mathbf1^TD^k\), \(0\le k<n\), span the dual space by the Vandermonde determinant. Polynomial spectral projectors in \(D\) isolate vertices; products along graph paths span all state vectors from \(b\). Minimal bilinear realization then determines \(A,D,b,c\) up to similarity. Because both \(D\) matrices are simple diagonal and both output rows are \(\mathbf1^T\), that similarity must be a permutation. Words through length \(2n-1\) suffice for a full rank selected Hankel construction. This is a structured application of known bilinear realization theory, **not** an independent novelty claim.

## Exact and finite-noise tests

- [`two_pulse_echo_replay.py`](two_pulse_echo_replay.py) exactly verifies the two-state one-pulse collision and its two-pulse separation, and reconstructs a fully connected three-state fixture from the \(H,H^M,K\) matrices. It reports \(\det H=-375\) and recovers \(A=[[-3,1,2],[2,-5,1],[1,4,-3]]\), \(D=\operatorname{diag}(2,3,5)\), and \(b=e_1\). This is symbolic replay, not a physical assay.
- [`one_field_word_replay.py`](one_field_word_replay.py) verifies the broader finite-word realization for the same three-state fixture; the selected word Hankel has rank 3, determinant 24, and maximum required word length 5.
- [`one_field_replay.py`](one_field_replay.py) checks the exact two-state constant-dose transfer formula and a nonzero nine-point Jacobian determinant for a three-state finite constant-dose design. The latter proves local identifiability at that fixture, **not** global identifiability or practical estimation.
- [`two_pulse_fisher.py`](two_pulse_fisher.py) audits a two-state Bernoulli-survival design using log-parameter sensitivities. Twenty one-pulse settings have a numerical null singular value \(1.75\times10^{-11}\), consistent with the exact ambiguity. Sixty-four two-pulse settings have singular values approximately \((4.117,0.728,0.0750,0.0150)\), condition 274. With 10,000 *independent survivors/trials per setting*, the local Cramér–Rao lower-bound one-sigma fractional errors are about 24%, 62%, 2.1%, and 11% for \((a,r,d_1,d_2)\). This is a best-case local lower bound under an ideal Bernoulli model, not achieved error or a universal sample complexity. It already signals costly precision.

The highest derivative order grows linearly as \(2n-1\), but estimating high derivatives from finite time points can amplify shot noise much more severely; the exact moment count is not a practical acquisition bound. The two-pulse test uses 64 schedules, so its quoted 10,000 trials per schedule imply 640,000 independent survival outcomes; actual ion-trap shots may contain multiple correlated ions and need their own count-noise calibration. Timing, detector normalization, field stability, residual background loss, sample reset, and pulse-induced changes in \(A\) all enter the real cost.

There is also a simple **contrast lower-bound scaling**. Write \(D=dI+\varepsilon E\), with fixed bounded \(E\), and consider any fixed finite pulse schedule and finite time horizon. At \(\varepsilon=0\), its survival probability is \(e^{-dT_{\rm on}}\) regardless of \(A\). Matrix exponentials are analytic in \(\varepsilon\), so every sensitivity \(\partial y/\partial A_{ij}\) is \(O(\varepsilon)\). If the survival probability stays away from 0 and 1, the per-independent-trial Bernoulli Fisher information in an internal-rate direction is at most \(O(\varepsilon^2)\). Thus any fixed-precision rate estimate from such schedules requires at least order \(\varepsilon^{-2}\) independent outcomes as the state-dependent loss contrast vanishes, even before other noise and nuisance parameters. This is a local information bound, not a universal tight sample-complexity theorem.

## Other initial mechanisms and why they lost

1. **Thermal edge-perturbation tomography.** For a heat/network operator \(L\), adding one calibrated shunt \(qvv^T\) changes \(G=L^{-1}\) by Sherman–Morrison:
   \(G_q=G-qGvv^TG/(1+qv^TGv)\). A scalar one-port readout \(h^TG_qh\) exposes \((h^TGv)^2\) and \(v^TGv\), not the signed interior Green function or unique topology. One would need many independently placeable shunts and boundary sensors, which are themselves a major acquired interface. The rank-one identity is standard; I did not promote this branch.
2. **One sink per hidden state, two doses each.** This stronger-control branch yields an exact compact reconstruction theorem, implemented in [`selective_sink_replay.py`](selective_sink_replay.py). For sink \(u k_i e_ie_i^T\), unknown \(k_i>0\), and absorption-time Laplace transform \(\phi_{i,u}(s)\), two known relative doses recover \(F_i(s)=k_i e_i^T(sI-A)^{-1}b\) by
   \[
   F_i(s)=\frac{(u_2-u_1)\phi_{i,u_1}(s)\phi_{i,u_2}(s)}{u_1u_2[\phi_{i,u_2}(s)-\phi_{i,u_1}(s)]}.
   \]
   At \(n\) distinct positive frequencies, full Krylov rank makes \(F\) invertible. Conservation solves \(F^T(1/k_i)_i=(1/s_j)_j\); the resolvent columns then yield \(A\). This requires **n separately addressable sinks** and a known dose ratio, essentially the missing state-selective interface. In a 3-state Gaussian approximation to 18 matched Laplace means, algebraic inversion was unstable and a positive-rate joint fit to the *same observations* was substantially better: at one million independent absorption times per assay, median relative \(A\) error 0.963 versus 0.033 on the stress fixture, and 0.059 versus 0.012 on a better-spaced fixture (12 seeded replicates each). The fit is a competent fixed-start benchmark, not a proven optimum. Logs: [`conditioning_stress.txt`](conditioning_stress.txt), [`conditioning_separated.txt`](conditioning_separated.txt), script [`conditioning_probe.py`](conditioning_probe.py). This branch therefore neither removes the difficult physical interface nor beats same-data inference.

## Closest predecessors and priority boundary

- **Sontag, Wang, and Megretski, *Input Classes for Identification of Bilinear Systems* (2006 preprint; 2009 IEEE TAC).** Their initialized type-II model is exactly the ambient form \(\dot x=(A+uN)x,\ x(0)=b,\ y=cx\). They state equivalence via all noncommutative word moments and the minimal-realization similarity theorem. They also prove generic fixed-amplitude pulse-family sufficiency and generic constant-input insufficiency. [Primary preprint](https://arxiv.org/html/math/0610633v1), [journal PDF](https://www.sontaglab.org/FTPDIR/sontag_wang_megretski_inputs_tac_54_195_207.pdf). Our conservation restriction \(cA=0\) is nongeneric: a single pulse followed by darkness has no further output change, so their generic positive result must not be imported unchanged. Our two-pulse \(H^{-1}K\) derivation is a specialized classical realization argument, not a new foundational identification principle.
- **Juang, *Continuous-Time Bilinear System Identification* (NASA technical memorandum, 2003)** uses pulse responses of distinct durations and a free-decay Hankel matrix to recover bilinear dynamics. [Primary full memorandum](https://ntrs.nasa.gov/api/citations/20040000390/downloads/20040000390.pdf). In the present conservation setting its free-decay signal is constant, so that particular rank-\(n\) Hankel step collapses; the second loss interval restores an observable output. **Juang and Lee, *Continuous-time bilinear system identification using single experiment with multiple pulses* (2012)** explicitly uses multiple pulses interleaved with free decay. [Primary publisher abstract](https://link.springer.com/article/10.1007/s11071-011-0323-9). These are strong priority warnings for the two-pulse protocol; I did not establish that the exact conservative/diagonal/single-aggregate theorem is absent from them.
- **Sattar et al., *Finite Sample Identification of Partially Observed Bilinear Dynamical Systems* (2025)** provide a noisy-data bilinear realization algorithm and bounds under stability assumptions. [Primary PMLR article](https://proceedings.mlr.press/v283/sattar25a.html). Their finite-sample theory is an incumbent to compare before any efficiency claim.
- **Gross and Blüthgen, *Identifiability and experimental design in perturbation studies* (2020)** analyze which network parameters can be learned under perturbations; their steady-state/multichannel setting differs, but the experimental-design framing and structural-versus-practical gap are directly relevant. [Primary article](https://academic.oup.com/bioinformatics/article/36/Supplement_1/i482/5870467).
- **Harville et al., *Cryogenic Ion Kinetics and Thermodynamics in a Temperature Controlled, Radiofrequency Ion Trap* (2025)** is the closest acquired physical platform found. They selectively bleach one of two tag isomers with a 5 ns IR pulse, measure time-resolved isomer-specific probe intensities, use conservation to calibrate relative optical cross sections, and infer forward/reverse interconversion rates. They report recovery time constants near 48–49 µs and a gas density that drifts with extraction delay. [Primary author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC12525174/). This is strong evidence that state-specific loss and total parent-ion counting are real, but also that a stronger readout already solves this two-isomer case. Their nanosecond bleach plus later state-selective probe is **not** the assumed continuous on/off diagonal hazard with unchanged stationary \(A\). It cannot be cited as a validation of this operation.
- **Offenberg et al., *Measurement of small photodestruction rates of cold, charged biomolecules in an ion trap* (2008/2009)** independently demonstrates a continuous-wave UV photodestruction field in an ion trap, intensity-linear rates, and parent-ion loss measurement. [Primary preprint](https://arxiv.org/abs/0810.5097). Its measured rates below 0.05 s\(^{-1}\) are from a different molecule and regime, versus the roughly 20,000 s\(^{-1}\) recovery scale in the Harville system; combining these two component demonstrations into a single useful loss-echo experiment remains unproven. The numerical rate contrast is an illustration of that cross-platform gap, not a physical limit.

## First credible application chain and decisive gates

The most plausible conditional use is a trapped-ion or other isolated-isomer experiment in which multiple hidden conformers interconvert, a single fixed optical band removes them with distinct hazards, and only total surviving parent count is available. One would first establish the unchanged-\(A\) diagonal-loss law by independently measuring dose linearity and on/off switching, verify stable initial preparation or jointly fit unknown \(b\), collect one- and two-pulse total-survival curves over on/dark times comparable to exchange rates, fit \(A,D,b\) jointly under counting noise, and then predict held-out pulse schedules. Independent isomer-resolved spectroscopy on the **same samples** would be needed to validate the recovered state interpretation. The exact Hankel inversion is a structural witness and initialization, not the final noisy estimator.

The decisive physical discriminator is a held-out two-pulse survival curve that separates two models indistinguishable under every feasible one-pulse schedule, with enough count precision to reject the wrong model and with an independently verified unchanged kinetic generator during illumination. The decisive practical comparison is a joint likelihood or Bayesian fit of the **same raw two-pulse counts**, plus any stronger incumbent that already measures state-resolved probes, including the cited ion-trap procedure. If direct spectroscopy is available at comparable cost, this proposal has no established advantage. If a field changes interconversion rates, populates excited states, causes non-diagonal transitions, or has identical effective hazards across states, the theorem's model or identifiability condition fails.

**Remaining claims:** exact reconstruction under stated algebraic assumptions is proved and symbolically replayed. No physical dataset, independent physical validation, novelty proof, competitive error bound, demonstrated time/energy/preparation budget, or consequential new discovery exists here. The honest promotion status remains **NOT ACHIEVED**.
