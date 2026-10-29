# A multiscale certificate for residual energy using returned physical trials

29 October2026. Complementary construction within continuing Astra P1. This
uses a STRONGER actual acquisition operation than one- or two-call independent
ensemble loops. The statistical ingredients are standard concentration and
multiscale tail integration; related coin-mixture literature is listed below.
No novelty of adaptive coin sampling, apparatus operation or practical speedup
is claimed.

## 1. Warranted physical experiment

Freeze a chosen macro operation and a reference probability c in[0,1] before
validation (or condition on independent training data). A specimen has hidden
H~nu. On that SAME specimen, an actual visible-return protocol permits repeated
trials X_1,...,X_m which, conditional on H=h, are independent Bernoulli(p(h)).
The return operation brings the visible state to the specified input label
while leaving H unchanged. It includes all bath memory required for the
conditional Markov law. This is an actual repeated experiment, not a copied
hidden state or a hypothetical pair of continuations.

Independent specimens genuinely sample nu. Source preparation, every trial,
return calls, sensing, clocks, switching, randomizers and disposal of private
keys remain paid. A return-time or success filter cannot silently discard
specimens, since that would change nu. If return has random duration, its
actual expected/tail cost is an additional resource bound. One returned coin
sample is not automatically one native call.

Goal: certify

    V=E_nu[(p(H)-c)^2] <= v,

where 0<v<=1, with false-certification probability at most delta. The theorem
supplies a valid upper confidence bound for ALL mixing distributions and
accepts with probability at least1-delta whenever V<=v/64. No smoothness,
finite hidden rank, number of disorder values, tail gap or parametric p(h)
model is assumed. The broad indifference region is explicit.

## 2. Nonadaptive multiscale schedule

Let

    L=ceil(log2(8/v)),       t_l=2^(-l), l=1,...,L,
    beta=v/64,             s>=log(2/delta),
    b>=log(128/v),         a=v/(128s),
    n_l=ceil(t_l/a),
    m_l=ceil(8b/t_l).

One may take equality in s,b. For exact integer scheduling the executable
uses s=ceil(log2(2/delta)) and b=ceil(log2(128/v)), which are conservative
upper bounds on the natural logarithms.

At level l draw n_l fresh independent specimens. On each obtain m_l returned
trials. Flag the specimen if

    |sample_mean-c| > 3sqrt(t_l)/4.

Let hat d_l be its flagged fraction and form the weighted statistic

    Q=sum_l t_l hat d_l.

Output the upper confidence bound

    U=min{1, t_L + (2Q+v/16)/(1-beta)}.                 (1)

Certify only when U<=v. The schedule is deliberately simple and does not need
adaptive stopping; an adaptive algorithm may improve constants, but is not
needed for the claimed exponent. Replacing the declared schedule by arbitrary
data-dependent selection needs its own confidence argument.

## 3. Soundness proof

Put theta(h)=p(h)-c. Let d_l be the true probability of flagging a random
specimen at scale l, including native coin noise.

If |theta|>sqrt(t_l), failure to flag requires sample error at least
sqrt(t_l)/4. If |theta|<=sqrt(t_l)/2, flagging requires the same error.
Hoeffding and the chosen m_l give, respectively,

    d_l >=(1-beta) Pr(theta^2>t_l),
    d_l <=Pr(theta^2>t_l/4)+beta.                        (2)

These are expectation statements. There is NO union bound over all specimens'
classification errors; a few false flags are permitted and charged.

For every theta in[-1,1], dyadic tail integration gives

    theta^2 <=t_L+sum_l t_l 1_{theta^2>t_l}.

Therefore, writing S=sum_l t_l d_l,

    V<=t_L+S/(1-beta).                                 (3)

To estimate S, treat Q as a sum of independent Bernoulli flags with individual
weights a_i=t_l/n_l<=a. For any real lambda, convexity on[0,1] yields

    log E exp(lambda Q/a)
       <=(S/a)(exp(lambda)-1).

For negative lambda the same inequality holds. Consequently the usual
multiplicative Poisson/Chernoff bounds give, simultaneously with probability
at least1-delta,

    S<=2Q+8as=2Q+v/16,
    Q<=2S+8as=2S+v/16.                                (4)

For the lower-tail assertion, S>2Q+8as implies Q<S/2 and S>8as; the standard
bound exp(-S/(8a)) is then at most exp(-s). For the upper-tail assertion,
use lambda=log2 and threshold2S+8as, obtaining an even stronger bound than
exp(-s). The two failure probabilities sum to delta. Pooling these weighted
flags is why there is no additional confidence union bound over L scales.

Combining(3) and(4) proves V<=U with probability at least1-delta, for every nu
and p. This is a genuine upper certificate, not only rejection of an exact
null hypothesis. The constant1 cap uses V<=1.

## 4. Near-null completeness

For every theta,

    sum_l t_l 1_{theta^2>t_l/4} <=8 theta^2.

Thus S<=8V+beta, because sum_l t_l<1. On event(4),

    U<=t_L+[32V+4beta+3v/16]/(1-beta).

If V<=v/64, t_L<=v/8 and beta=v/64, this is at most

    v/8+(3v/4)/(1-v/64)
      <=v(1/8+16/21) <v.

Hence a near-null source with V<=v/64 passes with probability at least1-delta.
The factor64 is a conservative proved separation, not an optimal constant.
A source in the middle region can pass or fail; every pass still has the
sound upper-certificate interpretation.

## 5. Complete resources

The number of independent specimens D obeys

    D=sum_l n_l <=128s/v+L.

The total number N of returned Bernoulli trials satisfies

    N=sum_l n_l m_l
      <=[1024 L s b+128s+256b]/v+L.    (5)

Proof: expand each product of ceilings as
(t_l/a+1)(8b/t_l+1), sum, use sum_l t_l<1 and
sum_l1/t_l=2^(L+1)-2<32/v.
Thus

    D=O(v^-1 log(1/delta)+log(1/v)),
    N=O(v^-1 log^2(1/v) log(1/delta)).                  (6)

Add every actual return operation and independent source-preparation cost.
If each returned trial costs at most C native calls, the native-call bound is
C*N, not N. With random return cost, use a separately warranted expected or
high-probability bound. Large hidden-dependent return costs can destroy an
otherwise favorable statistical scaling.

The constants in(5) are very conservative and can make this theorem worse
than a two-call estimator at moderate v. No practical improvement is inferred
from the exponent. A prescribed budget should use the actual schedule and
explicit counts before any claimed comparison.

## 6. Lower bounds and the change of acquisition interface

The power1/v is necessary up to logarithms for a uniformly sound near-null
certificate with nontrivial null acceptance. These elementary lower bounds
are not claimed new.

### Independent specimens are necessary

Take c=1/2. The null has p(H)=1/2 everywhere. An alternative has p=1/2 on
mass1-rho and p=1/2 +/-1/4 on massrho/2 each, where rho=32v (v<=1/32).
Then V=rho/16=2v while the overall mean remains c. Until a defective specimen
is drawn, all observations can be coupled exactly to the null, regardless of
how deeply or adaptively the previously drawn specimens are sampled. If at
most D specimens are used, the no-defect probability is(1-rho)^D. Null
acceptance>=1-delta and alternative acceptance<=delta require

    (1-rho)^D<=2delta,

hence D=Omega(v^-1 log(1/delta)) for a deterministic specimen cap. At constant
error the analogous expected-number bound is Omega(1/v), by the same coupling
and an encounter-probability bound. Many repeats of a few specimens do not
pay for rare undiscovered hidden responses.

### Native trials are necessary

An alternative with p=1/2 +/-sqrt(2v), equal mixing weights, also has mean c
and V=2v. For v sufficiently small every adaptively selected next Bernoulli
conditional mean lies within sqrt(2v) of1/2. Its conditional KL to a fair
coin is at most a constant times v. By the KL chain rule, any complete
transcript has KL at most O(v E[N]). Data processing to a decision with
error<=delta therefore requires N=Omega(v^-1 log(1/delta)). This applies to
fully adaptive choices of specimens and repeat counts under standard stopped
experiment conditions. It does not claim the logarithmic factors in(6) are
optimal.

### Why two-flip batches retain the old barrier

At c=1/2, compare the null to p=1/2 +/-sqrt(2v) with equal signs. Two
outcomes from one specimen have probabilities1/4+2v for00 and11, and
1/4-2v for01 and10. Their chi-square divergence from the four uniform null
outcomes is64v^2; KL is no greater. Any protocol restricted to independent
complete two-flip batches therefore requires Omega(v^-2 log(1/delta))
batches to distinguish this V=2v alternative from zero. This is the strict
alternative required for the claimed soundness threshold.

One observation per independent specimen has EXACTLY the same Bernoulli(c)
law under the mean-matched alternatives and can never detect V. The improved
certificate uses a real resource that the one/two-call-only acquisition
interface does not provide: arbitrarily many returned trials of the SAME
persistent hidden specimen.

## 7. Receiving consequence and records

For frozen disorder, if the deployed H marginal has density<=B relative to nu
conditional on the configuration/calibration data, a validated bound V<=U
controls the corresponding contribution to the root's full adaptive-record
KL bound. Repeat for each finite macro/input/outcome quantity, or allocate a
joint confidence budget; direct vector-outcome versions are possible but not
proved here. A known positive reference transition floor remains necessary
for the stated chi-square receiving conversion.

The validation must concern the ACTUAL deployed macro instrument. Retaining
its primitive selector can invalidate hidden-response cancellation even if
the averaged Bernoulli p(h) is constant. Arbitrary retained old Z is allowed
in the static-H receiving theorem, but selection/calibration dependence needs
the conditional deployment-density premise established in continuation1.
Independent validation does not by itself make deployment independent of the
training/validation data when the same specimen is reused.

The source H is not copied or equilibrated by a returned trial. The observation
can reveal H; that is useful during calibration and must be included in its
record/cost. The statistical proof only needs conditional independent native
outcomes and truly independent draws of new H at specimen boundaries.

## 8. Close primary predecessors

* Jasper C.H. Lee and Paul Valiant, *Uncertainty about Uncertainty: Optimal
  Adaptive Algorithms for Estimating Mixtures of Unknown Coins*, SODA2021,
  https://arxiv.org/abs/1904.09228 ; full v3 inspected at
  https://arxiv.org/html/1904.09228v3 . They explicitly distinguish within-coin
  from cross-coin adaptivity, estimate population fractions under a bias gap,
  and prove matching fully adaptive lower bounds for their task. This is
  serious reusable statistical machinery; the present squared-residual target
  lacks their global positive/negative gap.
* Kevin Jamieson, Daniel Haas and Ben Recht, *On the Detection of Mixture
  Distributions with Applications to the Most Biased Coin Problem*2016,
  https://arxiv.org/abs/1603.08037 . Their breadth/depth tradeoff concerns rare
  versus weak alternative coins and gives adaptive methods and lower bounds.
* Arpit Agarwal, Shivani Agarwal, Sepehr Assadi and Sanjeev Khanna, *Learning
  with Limited Rounds of Adaptivity: Coin Tossing, Multi-Armed Bandits, and
  Ranking from Pairwise Comparisons*, COLT2017,
  https://proceedings.mlr.press/v65/agarwal17c.html . Studies query complexity
  versus rounds of adaptivity for finding biased coins.

This note does not establish a new optimal coin-mixture tester. Its scientific
role is to make explicit how physically returned persistent-disorder trials
can turn the squared-residual acquisition barrier into a different, paid
statistical experiment, usable by conventional inference methods.
