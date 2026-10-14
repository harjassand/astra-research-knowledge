# ASTRA — Isotope-coded temporal ancestry acquisition

Research note, 14 October 2026.

**Status:** conditional mathematical construction with synthetic verification. No experimental demonstration, external proof review, priority determination, or advantage over the strongest nonlinear isotope-transient protocol is claimed. The four-carbon examples are abstract ancestry laws, not fitted or independently validated catalytic mechanisms.

## 1. Scientific question and operational contract

For a product assembled from an even number n=2m of carbon atoms, let S_1 <= ... <= S_n be the times those atoms entered through a specified, controlled carbon-feed boundary. All product carbon must come from that labelled boundary, including any initial inventory whose preparation is charged. Entry time is not bond-formation time, surface residence time, or a spatial location.

The proposed operation acquires

    Q_n(r) = E exp[-2r L_n],
    L_n = sum_{j=1}^m (S_{2j} - S_{2j-1}).

L_n is the total length of the adjacent-pair matching of the ordered entry times. A common shift of all entry times leaves L_n unchanged. For n=2 it is the absolute entry-time difference. For n=4 it measures two paired gaps, not total age span.

The physical inputs are a controlled isotope-composition waveform at constant chemical feed, a stationary operating state, calibrated feed isotope purities, and calibrated product isotope-count fractions. No elementary reaction rates, microscopic states, internal trajectory samples, or full reaction-network reconstruction are supplied to the estimator.

The required assumptions are substantial:

1. Isotope composition does not change the unlabelled dynamics or the distribution of product ancestry.
2. Each entering molecule has one tracked carbon atom. Labels of distinct entering molecules are independent conditional on the prescribed isotope fraction and their entry times.
3. The ancestral carbon source is accounted for, without unlabelled cofeeds or an uncontrolled old inventory outside the error budget.
4. The product's full carbon isotope-count distribution is quantitatively measurable. Detector fragments must not silently replace whole-product carbon counts.
5. The ensemble of product histories is stationary during the acquisition, and the code has been applied throughout the relevant prehistory or an explicit startup error is carried.

An isotope-dependent change in chemistry breaks the genealogy interpretation even if total product yield is unchanged. Stable total yield alone cannot certify assumption 1.

## 2. Acquisition identity

Let sigma(t) be a stationary fair random telegraph process. Its sign flips at Poisson rate r. Set the feed heavy-isotope probability to

    p(t) = [1 + b + a sigma(t)] / 2,
    a = p_high - p_low > 0,
    b = p_high + p_low - 1.

For a carbon label X_i=+1 (heavy) or -1 (light), conditional independence gives

    E product_i [(X_i-b)/a] = E product_i sigma(S_i).

The product of an even number of telegraph signs depends only on the parity of Poisson flips in the disjoint intervals

    A = [S_1,S_2] union ... union [S_{n-1},S_n].

The total interval length is L_n. The elementary Poisson generating-function identity E[(-1)^N]=exp(-2 E N) therefore gives

    E product_i sigma(S_i) = exp(-2r L_n).

Averaging over the unknown ancestral histories proves the target identity.

Crucially, the estimator needs only K, the number of heavy carbon atoms in each product:

    W_n(K) = (1-b)^K (-1-b)^(n-K) / a^n,
    E W_n(K) = Q_n(r).

For symmetric purities b=0 and even n,

    W_n(K) = (-1)^K / a^n,
    Q_n(r) = a^(-n) sum_{k=0}^n (-1)^k P(K=k).

Thus n+1 isotope-count bins suffice. No position-resolved enumeration of 2^n labelling patterns is needed. This does not imply an unlimited high-order speedup: fixed imperfect purity amplifies shot noise as a^(-2n).

For arbitrary prescribed random codes the same reasoning yields

    E W_n(K) = E_history E_code product_i sigma(S_i).

Telegraph coding is one implementation with an especially simple interpretation and variance bound, not a claim that random switching is always optimal.

## 3. Uniform control-variance bound

This section bounds stochastic *code* noise, separately from preparation, chemical fluctuations, finite detection, and calibration.

Fix a particular ancestral pattern and its interval union A, consisting of at most m disjoint nondegenerate intervals. Write ell=|A|, H(s)=|A intersect (A+s)|, and delta(s)=ell-H(s). Let

    Z_A(t) = (-1)^(number of code flips in t+A).

Then

    E Z_A(t) = exp(-2r ell),
    Cov[Z_A(t),Z_A(t+s)]
       = exp[-4r delta(s)] - exp(-4r ell) >= 0.

The covariance vanishes when H(s)=0.

### Geometric lemma

For s>0,

    delta(s) >= min(s, ell/m).

Proof: project A onto the circle R/(s Z). On every nonempty finite fibre of A, the set difference A minus (A+s) has at least one point. Integrating over residues modulo s shows that delta(s) is at least the measure of this projection. If one component interval has length at least s, the projection is the whole circle. Otherwise the projection has measure at least the longest component length, which is at least ell/m. This proves the bound. Degenerate ell=0 gives deterministic Z_A and is handled separately.

The set of shifts having H(s)>0 is contained in A-A, a union of pairwise interval differences. The sum of their lengths is 2m ell. By symmetry, its measure on the positive half-line is at most m ell.

Consequently,

    integral_0^infinity Cov[Z_A(0),Z_A(s)] ds
      <= 1/(4r) + m ell exp(-4r ell/m)
      <= (1 + m^2/e)/(4r).

The variance of the time average over duration T is therefore at most

    Var[(1/T) integral_0^T Z_A(t) dt]
      <= (1 + m^2/e)/(2rT).

For an arbitrary stationary, code-independent mixture mu of ancestral patterns, apply Jensen's inequality to the centred time averages before averaging over the code. The same bound holds for the conditional-mean product signal. There is no bound on internal state-space size, common delay, or ancestral age span in this result.

### Finite product sampling

Under the additional idealization of N independent product draws conditional on the complete code, with times uniform over the observation interval and the stationary ancestry distribution, the law of total variance gives

    Var(Q_hat_n) <= (1 + m^2/e)/(2rT) + B_n^2/N,
    B_n = [(1+|b|)/a]^n.

For symmetric purity, the last term is a^(-2n)/N.

A constant-rate Poisson product stream with iid histories, conditional on N and the code, is one realization of this model. Real detector counts and real reaction events must not automatically be equated with independent product draws. Correlated chemistry, detector background, response-matrix inversion, and uncertain normalization require additional measured error terms.

The bound is a variance guarantee, not a Gaussian confidence interval. Chebyshev's inequality supplies a conservative confidence statement; independent repeat campaigns or a more detailed observation model may give sharper bounds.

### What the bound does not remove

The isotope code must cover the relevant ancestral history. A very old carbon inventory still entails startup/wash-in time. An ideal pure-heavy step after a pure-light steady preparation directly measures the probability of at least one pre-step carbon among a product's ancestors via the fraction of products not fully heavy. Imperfect purity requires a calibrated mixture inversion or a conservative bound, with its noise and conditioning charged.

The result concerns acquisition after valid preparation. It is not preparation-free inference of arbitrarily old hidden states. An unaccounted fraction eta of histories contributes at most 2 eta bias for ideal bounded parity. More general corrected readouts require the corresponding bounded-range factor.

## 4. Four-carbon separation from single-pulse data

Let tau>0 and define four product ages

    A_j = C + (j-1) tau + tau X_j, j=1,...,4,

where C>=0 is common to the four atoms. It can be any independent random delay, with the same law in both models.

In model E, X is uniform over the eight four-bit vectors of even parity. In model O it is uniform over the eight odd-parity vectors.

Every proper subset of up to three X coordinates has the same uniform law in the two models. Thus all corresponding labelled one-, two-, and three-atom age marginals coincide, even before forgetting atom positions.

A pure isotope step places a single boundary across the four ordered choice intervals. A single rectangular isotope pulse places two boundaries. At most one variable is nonconstant at each boundary. Therefore the complete isotope-count distribution at each output time depends on at most two X coordinates and is identical in E and O. This remains true for every pulse width and placement and after averaging over arbitrary common C. Imperfect but known inside/outside isotope probabilities do not change the argument, because the resulting count law is still a function of at most two varying X coordinates.

This is a statement about an *ideal two-level single rectangular pulse*, including arbitrary independent repetitions after matched preparation. It is not a statement about arbitrary pulse shapes, overlapping pulses, periodic modulation, or nonlinear frequency-response methods. Finite smooth ramps can distinguish the models and are not covered by this exact indistinguishability statement.

More generally, for a normalized deterministic isotope mean u(t) in [-1,1], the corrected parity contrast at output time t and common delay C is exactly

    Delta(t,C) = (1/8) product_{j=0}^3 [u(t-C-j tau)-u(t-C-(j+1) tau)].

This follows by expanding the even-minus-odd mixture. If u is Lipschitz with constant M, then |Delta(t,C)| <= (M tau)^4/8. A slow smooth transient can thus carry nonzero but fourth-order suppressed information. This bound applies to all methods using that waveform; it is not a way around input-bandwidth limitations.

For telegraph coding, x=exp(-2r tau) gives

    Q_E = (1+6x^2+x^4)/8,
    Q_O = (x+x^3)/2,
    Q_E-Q_O = (1-x)^4/8.

At r tau=2:

    Q_E = 0.12525161103782373,
    Q_O = 0.009160891550543754,
    difference = 0.11609071948727998.

This is an explicit positive information separation. It does not establish that these artificial histories describe a catalyst or that this statistic determines a unique chemical pathway.

## 5. Stronger competitors and the optimized code

### C2 construction is not a new capability over finite pulses

For two-carbon products, random independent-sign blocks of width h with a uniform random origin acquire

    Q_2(h) = E(1-|S_1-S_2|/h)_+.

However, inject a single pure-heavy rectangular isotope pulse of width h into an otherwise pure-light steady feed. If R is the constant total product flux and R_2(t) is the doubly-heavy product flux, then

    (1/R) integral_{-infinity}^infinity R_2(t) dt
      = E(h-|S_1-S_2|)_+ = h Q_2(h).

The equality follows from the overlap length of two shifted intervals. This is an exact comparator, not an asymptotic approximation. Coding is not inherently a new way to acquire this C2 functional. Full collection time, background, repeated pulse separation, and isotope dose determine the better protocol in practice.

### C4 example does not defeat optimized multipulse experiments

For the calibrated age grid above, choose a square-wave isotope code with

    sigma(t-tau) = -sigma(t).

Then for every output time and every common C, away from switching endpoints,

    product_j sigma(t-A_j) = (-1)^(X_1+X_2+X_3+X_4).

It follows that the corrected parity is +1 in E and -1 in O. The difference is 2 rather than the telegraph difference 0.11609 at r tau=2. The square wave also switches at rate 1/tau, compared with 2/tau for this telegraph setting, and both have mean heavy-feed fraction 1/2. Therefore random coding is not the strongest method on this known-scale synthetic benchmark.

Two appropriately placed finite heavy-isotope pulses generate the same alternating pattern over an aligned output window. If the common delay is known, this is another strong competitor. If it is unknown and broadly distributed, a continued square wave retains the delay-independent parity property after valid preparation.

Periodic isotope modulation and isotope frequency response are established experimental concepts. The candidate contribution is the exact nonlinear ancestry readout, the information-separation contract, and the acquisition bound. Its priority relative to the full nonlinear-transient literature remains unestablished.

## 6. Reproducible checks

The accompanying Python script exhaustively checks all 14 nonempty proper-coordinate marginals and all 32 binary input masks on the five possible age nodes. The E/O mass distributions coincide for 30 masks. Both alternating masks distinguish them. Every one of the 22 masks with at most two internal switches gives identical data.

It also simulates 100 independent complete telegraph-code campaigns. Within each campaign, 50,000 product samples per model share the same code, so finite-code randomness is not incorrectly replaced by independent label noise. Parameters are tau=1, r=2, T=2000, C=100, p_low=0.01, p_high=0.99. Simulated prehistory is 104 time units and is explicitly included in the cost report.

The corrected means are 0.1257168 (E) and 0.0092080 (O). Between-campaign standard deviations are 0.0069434 and 0.0094596. Standard errors of the 100-campaign means are 0.0006943 and 0.0009460. These are synthetic results and are not instrument-performance estimates.

For the covariance theorem, the script checks 1,000 random interval unions with 1-5 components, interval lengths from 0.01 to 100, gaps from 0.01 to 10,000, and telegraph rates from 0.01 to 100. It integrates the exact piecewise-exponential covariance. No violation is found; the largest observed integral/bound ratio is approximately 0.7311. Finite checks do not replace the proof or independent review.

## 7. Experimental application and acquisition ledger

A plausible first platform is isotope-transient methanol-to-hydrocarbons chemistry on H-ZSM-5, targeting an individually resolved four-carbon product. Published work already combines labelled methanol pulse sequences with mass spectrometry and chromatographic transient analysis. Adapting this to stationary constant-total-feed isotope coding, quantitative whole-product parity, and sufficiently fast measured inlet switching has not been demonstrated in this investigation.

A second motivation is joint carbon ancestry in CO2/CO electroreduction. Published OSRI experiments already investigate intermediary CO reservoirs. The C2 pulse equivalence above means that merely proposing the two-carbon transform does not establish an advantage there. Moreover, carbonate/bicarbonate exchange can delay gas-inlet isotope propagation. A boundary-defined ancestry observable must not be renamed a surface-residence or C-C-bond formation measurement.

Required accounting:

- Feed: actual p(t), mixing dead volume, transition shape, phase stability, isotope purity, chemical-feed constancy, and total labelled-carbon dose.
- Preparation: measured initial-carbon clearance or a quantitative remaining-history error; repeat preparations and discarded products count.
- Detection: response matrix for isotope count, background, natural-isotope corrections, product/fragment separation, recovery efficiency, drift, and effective covariance. N in the theorem is not raw ion count.
- Chemistry: isotope-dependent kinetics, stationary product selection, ageing/deactivation, and possible code-induced changes in hidden pathways.
- Control: total observation time and number of switches, not just number of measured products. Instantaneous Poisson switching is an idealization; finite transition duration must be calibrated or included in the actual code kernel.
- Computation: code generation/recording and calibration plus an n+1-bin weighted sum. Reaction-network inversion is not an input.
- Decision relevance: demonstrate that the acquired quantity separates physically competing mechanisms consistent with strong baseline data, and that the distinction matters to a catalyst-design or process-control decision.

The fair experimental comparison includes optimized single and multiple pulses, periodic modulation, nonlinear isotope-frequency analysis, and any relevant simultaneous spectroscopy, at matched isotope dose, catalyst time, preparation, detection precision, and prior calibration information. There is no certified dominance over this competitor set.

## 8. Scientific status and continuation criterion

The positive output is a physically specified way to turn multi-atom temporal ancestry into a pooled product statistic, with a rigorous acquisition identity and a proposed uniform variance theorem. It contains no free microscopic-information oracle.

The unresolved issue is not another algebraic rearrangement. It is whether a real, important catalytic ambiguity survives optimized existing transient measurements and is resolved by this acquisition at lower total cost or greater reliability. A same-platform benchmark that establishes that result is necessary before promoting this work to a new scientific capability. A laboratory design or technological improvement inferred solely from the synthetic E/O example would be unsupported.

## References and provenance

These references establish existing capabilities or close competitors, not the novelty of this note.

1. Louisia, S. et al. (2022). The presence and role of the intermediary CO reservoir in heterogeneous electroreduction of CO2. PNAS 119(18), e2201922119. DOI: 10.1073/pnas.2201922119. Full article and a figure page inspected.
2. Hartfelder, U., Szlachetko, J., Sa, J., van Bokhoven, J. A. (2012). Determination of catalytic reaction mechanisms by isotopic frequency response. Analyst 137, 5374-5381. DOI: 10.1039/c2an35903k. Bibliographic record and abstract located; full text was not successfully retrieved. This access limit prevents a conclusive priority comparison.
3. Liu, C., Uslamin, E. A., Pidko, E. A., Kapteijn, F. (2023). Revealing Main Reaction Paths to Olefins and Aromatics in Methanol-to-Hydrocarbons over H-ZSM-5 by Isotope Labeling. ACS Catalysis 13(8), 5205-5212. DOI: 10.1021/acscatal.3c00168. Author-institution abstract and methods synopsis inspected; no raw experimental data analysed.
4. Aleria, A. et al. (2026). Resolving the inverse problem in pulse response analysis of TAP reactors. arXiv:2607.04776v1. Preprint; describes model-free Y-procedure reconstruction and noise/regularization issues, with synthetic tests.
5. Jamil, S., Kapadia, R. (2026). Lie Generator Networks Extract EIS-Grade Battery Diagnostics from Pulse Relaxation Data. arXiv:2605.15351v1. Preprint considered during bottleneck screening, not independently validated here.
6. Seo, J. et al. (2024). Avoiding fusion plasma tearing instability with deep reinforcement learning. Nature 626, 746-751. DOI: 10.1038/s41586-024-07024-9. Existing capability considered during screening.

Astra repository orientation was inspected at revision ace0cfc4437fe91c20ccd24d69e0ee4bb335e871. Recent records were treated as unreviewed research navigation, not imported theorems. The OpenAI/math repository README was also inspected; no manuscript result from that repository is used as a proof premise here. No repository was modified.
