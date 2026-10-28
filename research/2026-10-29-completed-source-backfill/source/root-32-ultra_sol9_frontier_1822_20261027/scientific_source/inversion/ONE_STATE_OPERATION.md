# Four scalar settings witness a nonreversible return revival

This is the smallest constructed acquisition operation in this worker. It is
a conditional physical measurement design with a complete derivation and
synthetic records. It is not a new claim that reversible Markov return
probabilities are completely monotone. Historical novelty of this loss-pulse
design, physical access and practical advantage remain UNKNOWN.

## Contract

An unknown finite, time-homogeneous, conservative classical CTMC has column
generator Q and transition matrix P(t)=exp(tQ). It is prepared repeatedly in
one fixed unknown p. Only one *resolved kinetic state* i is addressable, with
p_i>0. An early pulse deletes an unknown fixed fraction aE>0 of that state;
a late pulse deletes an unknown fixed fraction aL>0. They may differ. The
pulses do not change the law of surviving trajectories or touch other states.
At each endpoint, one aggregate detector counts all surviving states with
fixed unknown affine law y=beta+gamma*1^T x, gamma>0. All other states,
their count, rates and connectivity can be inaccessible.

The operation chooses two delays t2>t1. At each delay measure just two
conditions: late pulse alone, and early+late pulses. Thus there are four
settings, one state-selective loss label, and no supplied state populations,
pulse efficiencies, microscopic generator, stationary preparation or detector
gain/offset. Time homogeneity, conservation, state resolution and the pulse/
detector premises are real physical acquisitions, not inferred from four means.

## Construction

With E_i=e_i e_i^T, R_E=I-aE E_i and R_L=I-aL E_i,

    y_late(t)=beta+gamma*1^T R_L P(t)p,
    y_both(t)=beta+gamma*1^T R_L P(t)R_E p.

Conservation 1^T P(t)=1^T gives

    y_both(t)-y_late(t)
       = -gamma*aE*p_i + gamma*aE*aL*p_i*P_ii(t).

Therefore the directly measured difference-in-differences is

    D=[y_both(t2)-y_late(t2)]-[y_both(t1)-y_late(t1)]
      = gamma*aE*aL*p_i*[P_ii(t2)-P_ii(t1)].               (1)

Every unknown nuisance factor on the right is positive and time independent.
The sign of a return revival is acquired without calibrating any of them.

## Reversible null theorem

If Q is reversible with positive measure pi, let

    S=diag(pi)^(-1/2) Q diag(pi)^(1/2).

Detailed balance makes S real symmetric and negative semidefinite. Its
orthonormal eigenvectors v_l and nonnegative decay rates lambda_l give

    P_ii(t)=[exp(tS)]_ii=sum_l v_l(i)^2 exp(-lambda_l*t).    (2)

Thus P_ii is completely monotone, in particular nonincreasing. Equation (1)
proves D<=0 for every reversible fixed generator, independent of the initial
preparation. A certified D>0 therefore rejects that model class. It does not
establish a complete state reconstruction, entropy-production rate, an energy
source, or irreversibility in a model whose classical CTMC premise was not
acquired. Coherent quantum oscillations, non-Markovian memory or an externally
time-varying generator can also violate the classical reversible null.

Failure to find a revival does not certify reversibility: many irreversible
generators have monotone returns at the selected state or over the selected
time range. No universal search horizon or minimum revival is promised.

## Exact finite-confidence sign

Take m independent [0,1] readouts at each of the four settings. Dhat is a
signed sum of four sample means. Apply Hoeffding directly to the 4m independent
bounded signed observations: sum of squared range widths is 4/m. Hence

    Pr(Dhat-D>=d) <= exp(-m*d^2/2).                        (3)

This direct contrast bound avoids incorrectly assuming independent derived
contrasts or paying an unnecessary four-mean union bound. With m=100,000 and
d=1/100, the error is <=exp(-5)<1/100. The latter inequality can be checked
with exact rational arithmetic by a positive Taylor lower bound for exp(5).
If Dhat>1/100, its rational difference from 1/100 is a strictly positive
99%-confidence lower bound for D under the interface and IID premises.
This is a theorem about actual independent bounded observations; a finite-bit
synthetic RNG is not itself asserted to realize exact IID sampling.

If each setting has an independently acquired systematic mean-error bound
zeta, replace d by d+4zeta in the sign comparison. Different preparations,
pulse efficiencies or detector gains across delays do not cancel without such
a bound. Settings should be interleaved to measure drift, but interleaving
alone is not proof of stability.

The demonstrated design has 400,000 fresh preparations, 400,000 terminal
readouts, and 600,000 elementary loss pulses (one or two per setting), plus
physical reset, selective-pulse, timing, energy and detector costs. Simulating
the binomial counts is not performing those physical acquisitions.

## Construction example

The code declares an eight-state ring with clockwise rate 1 and reverse rate
0.05. Only state 0 is selectively addressable; the other seven states remain
unobserved. At t1=4 and t2=8, P_00 rises from approximately 0.056248 to
0.138133. The initial distribution is deliberately nonstationary, with p_0=0.4.
Unknown early/late pulse efficiencies and detector parameters are supplied
only to generate synthetic observations, then canceled by (1). See the saved
one_state_record.json for all inputs, raw integer counts and exact sign.

## Strong ordinary comparator

An equally informed ordinary analysis gets all four Bernoulli records and the
same null D<=0. Binomial likelihood under that *linear* constraint is convex;
the implementation fits it directly and reports numerical convergence and an
asymptotic likelihood-ratio statistic. A standard delta-method interval uses
the same four-means variance. The exact contrast estimator is ordinary and
neither method is denied any information. This worker claims no statistical
or computational advantage over those analyses. The constructed object is
the finite loss-only acquisition interface and its nuisance cancellation.

## Essential boundaries and repair

- **Natural population loss.** For substochastic P, the term
  -gamma*aE*p_i*1^T P(t)e_i depends on t and can fake a revival. If conservation
  is not acquired, measure baseline and early-only at *each* delay as well.
  The resulting eight-setting inclusion-exclusion recovers
  C(t)=gamma*aE*aL*p_i*P_ii(t). For a reversible generator plus arbitrary
  diagonal killing, the symmetric semigroup proof (2) still gives monotonicity.
  The four-setting shortcut is not valid merely because loss seems small.

- **Unresolved states.** A macrostate pulse is covered under acquired lumpability,
  or under the alternative stationary-preparation contract. With arbitrary
  hidden substates and transient preparation the theorem fails. The code
  preserves a reversible symmetric three-state chain with fast 1<->2 and slow
  0<->1 exchange, group {0,1}, and preparation concentrated at state 1. Its
  group return falls then rises while microscopic detailed balance holds.
  The six-state exact false-cycle ratio16/5 in CYCLE_OPERATION.md is a second
  sharp version of the same boundary.

- **Stationary macrostate variant.** If p=pi is a stationary preparation and Q
  is reversible under the null, any group indicator f has
  f^T exp(tQ)diag(pi)f as a positive mixture of decaying exponentials. Thus the
  eight-setting contrast also supports arbitrary uniform-depletion groups
  under this different, explicitly acquired preparation contract. A known
  total-variation error delta in stationary preparation perturbs each such
  correlation by at most gamma*aE*aL*delta. Acquiring that stationarity bound
  can require substantial mixing time and is not supplied by this operation.

- **Detector/control errors.** State-dependent detection, nonlinear saturation,
  off-target loss, pulse-induced transitions and survivor-law changes are
  outside the exact theorem; acquired deterministic mean-error bounds can be
  charged through zeta. A mathematical label for a level is not proof of
  physical kinetic-state resolution, particularly for unresolved magnetic,
  vibrational, velocity or environmental substates.

## Prior credit and next physical gate

State-selective removal to acquire temporal correlations predates this work
(Robens et al., Phys. Rev. X 5, 011003, 2015,
https://doi.org/10.1103/PhysRevX.5.011003). Reversibility/correlation asymmetry
is established theory (Ohga, Ito and Kolchinsky, Phys. Rev. Lett. 131, 077101,
2023, https://doi.org/10.1103/PhysRevLett.131.077101). State-selective depletion
of cold-molecule populations is an existing physical building block (Schenk,
MPQ317, 2007, https://www.mpq.mpg.de/7062849/MPQ317.pdf). None supplies the
entire interface or novelty conclusion for this construction. In particular,
the molecular report does not acquire single-kinetic-state resolution,
uniform detection and survivor-law preservation for our operation.

The next acquisition is one consequential classical system with a calibrated
bound on pulse selectivity/duration, equal-weight affine total counting, fixed
survivor dynamics and preparation repeatability, plus the same-record ordinary
analysis. This worker did not perform that acquisition, run a physical
experiment, or establish a practical advantage or foundational breakthrough.

For the affine eight-setting variant, equal state weights are in fact
unnecessary. If the detector is beta+w^T x with fixed unknown w and w_i>0,
the same inclusion-exclusion yields C(t)=w_i*aE*aL*p_i*P_ii(t). This follows
from w^T E_i=w_i e_i^T and retains the monotonicity theorem. It tolerates
unknown weights on all other states and reversible diagonal killing. This
does not justify the four-setting shortcut with such a weighted detector,
because its canceled total-survival term would no longer be conserved.

## Final constructed repair: unknown strictly increasing detector

Affine calibration can be removed for a useful sufficient ordering pattern.
Keep all other four-setting premises, but replace the detector by an arbitrary
fixed strictly increasing function h of *total surviving population*. Denote
the four underlying populations by s_late(t) and s_both(t). If the measurements
certify both

    y_both(t2)>y_both(t1),
    y_late(t1)>y_late(t2),                                 (4)

strict monotonicity implies the same two population inequalities. Consequently

    [s_both(t2)-s_both(t1)]-[s_late(t2)-s_late(t1)]>0.

The population version of (1) forces a return revival. Thus (4) rejects the
same reversible fixed classical CTMC class without knowing detector gain,
offset, curvature, saturation law, p_i or either pulse efficiency. This is an
ordinal sufficient test, not a quantitative population-return bound. It can
fail where the affine cardinal contrast succeeds. It still needs equal-weight
total counting, conservation and a detector that is the same across settings.
The eight-setting nonconservative repair above uses affine inclusion-exclusion
and does not automatically extend to an arbitrary monotone detector.

For two independent m-trial bounded means, the one-sided difference error
bound is exp(-m*d^2). With m=100,000 and d=3/400, the two positive empirical
differences minus d hold simultaneously except with probability at most
2*exp(-45/8)<1/100. The code verifies the last bound using positive rational
Taylor terms, and verifies both sign margins with exact integer-count
arithmetic. An acquired per-setting mean bias zeta subtracts 2zeta from each
margin. No finite-bit sampler is claimed to prove its own IID contract.

The constructed example uses 32 states on a directed ring. State 0 exits at
rate 1; the 31 inaccessible intermediate states exit at rate 31/5. This creates
a delayed return wave. Only label0 is controllable, and the detector used to
generate the scalar records is the nonlinear law h(s)=1/100+49*s^2/50. The
estimator is not supplied that law. At the predeclared delays 3 and 6,
P_00 rises from approximately 0.0505184 to 0.2607253.

An exact stationary vector is pi_0=1/6 and pi_j=5/186 for j>0. The declared
nonstationary preparation is p_0=8/31, p_j=23/961. It is selected from the
declared model to balance the two population margins: with aE=17/20,
p=(1-theta)pi+theta*e0, theta=17/155=aE*p_0/2. Hence late survival decreases
and both-pulse survival increases by the same positive amount. This is a
provided synthetic preparation, not an acquired means to prepare that physical
distribution. A real unknown specimen need not show this crossed ordering;
finding lags/preparations would incur additional acquisition and testing costs.

An independent exact-rational uniformization calculation with a positive
exponential-series tail bound certifies that model return rise exceeds
0.2102068365. The model's two ideal detector-order margins exceed 0.0346129206
and 0.0269414577, and its floating forward means differ from the exact model
by at most 5.081e-15. The rational intervals and tails are preserved in
outputs/uniformization_certificate.json; this is model verification only.

The same 400,000 preparations/readouts and 600,000 elementary pulses suffice
for the saved synthetic record. The matched ordinary analysis gets exactly
these four records. Under the enlarged ordinal null, at least one of the two
ordering inequalities is nonpositive. The null is therefore the union of two
halfspaces. Its binomial maximum likelihood fit is the better of the two
ordinary pooled-mean fits; both are implemented. This is a standard
intersection-union comparison, not a claimed new statistical test. The
ordinary analysis also rejects; there is no superiority claim.

The practical gate is now a known direction of monotonic response to *total*
surviving population rather than full affine calibration. All other physical
gates remain. Return monotonicity itself is prior art: Chen Yong, "On the
Monotonicity of Autocorrelation Function for Finite State Markov Processes,"
Acta Scientiarum Naturalium Universitatis Pekinensis45(1),11 (2009),
https://xbna.pku.edu.cn/EN/Y2009/V45/I1/11. The current Astra records N507,
N508 and N588 also contain stronger reversible-process mathematics; this
worker does not replace or rebrand those results.
