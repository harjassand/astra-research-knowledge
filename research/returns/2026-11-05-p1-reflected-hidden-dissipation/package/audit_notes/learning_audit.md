# Reflection-defect dissipation: mathematical and finite-data audit

Prepared independently by the learning/audit branch for integration into the main research record. This note supplies proofs and resource accounting, not a claim of literature priority.

## 1. Model and notation

Let `X_s` be a stationary, irreducible finite-state continuous-time Markov chain with generator `Q`, stationary distribution `pi`, and all microscopic states even under physical time reversal. The number of microscopic states is arbitrary and need not be known. Assume bidirectional rates on every occupied edge when finite entropy production is desired. Define the stationary reversed generator by

`q*_ij = pi_j q_ji / pi_i`.

Its dimensionless entropy-production rate is

`sigma = sum_{i != j} pi_i q_ij log(q_ij / q*_ij)`.

Multiplication by Boltzmann's constant converts this to entropy per unit time under the stochastic-thermodynamic interpretation. The all-even-state assumption is essential: equilibrium dynamics with odd momentum/velocity variables need not satisfy the ordinary reflection constraints below.

Observe only `Y_s=f(X_s)` in a finite alphabet. Fix a half-window length `t>0` and any finite selection of observation times in `[0,t]`. Let `B` be the resulting future word, and let `A` be the reflected past word sampled at the matching negative times, ordered from the midpoint outward. The shared midpoint observation may be included in both words. Let the word alphabet have size `k` and define

`M_ab = P(A=a, B=b)`.

All probability statements in Sections 2--5 concern the stationary distribution. Section 6 accounts for obtaining the statistics from one trajectory without free equilibrium preparation.

For each midpoint microstate `i`, let `u_i` be the future-word distribution under `Q`, and `v_i` the future-word distribution under `Q*`, both started at `i`. By the Markov property and stationarity,

`M = sum_i pi_i v_i u_i^T`.

Define

`c_i=(u_i+v_i)/2`, `d_i=(u_i-v_i)/2`,

`S=(M+M^T)/2`, `r=S 1`, and `A0=S-r r^T`.

The name `A0` here denotes a centered reflection matrix, not a dynamical generator. Both `u_i` and `v_i` are probability vectors; therefore `c_i` is a probability vector and `1^T d_i=0`.

## 2. Exact positive-minus-positive representation

**Theorem 1.** The centered and uncentered reflection matrices satisfy

`S=C-Z`,

where

`C=sum_i pi_i c_i c_i^T` is completely positive,

`Z=sum_i pi_i d_i d_i^T` is positive semidefinite, and `Z 1=0`.

Moreover,

`A0 = Cov_pi(c_i) - Z`.

**Proof.** Expanding `c_i c_i^T-d_i d_i^T` gives `(u_i v_i^T+v_i u_i^T)/2`. Averaging proves the first identity. Nonnegativity of `c_i` proves complete positivity. The remaining claims follow from `sum_i pi_i c_i=r` and `1^T d_i=0`.

At equilibrium, `Q=Q*`, so `u_i=v_i`, `Z=0`, and the entire reflection matrix is completely positive. Thus every negative reflected covariance measures a contrast between conditional future laws under the two microscopic directions of time. It can remain visible even when the observed process itself has a time-symmetric path law.

Complete positivity here means a finite sum of outer products of entrywise nonnegative real vectors. It does not refer to complete positivity of quantum channels.

## 3. Entropy controls the negative component

Put `h_i=TV(u_i,v_i)`, where total variation is half the L1 distance. Since `d_i` has zero sum,

`||d_i||_2^2 <= ||d_i||_1^2/2 = h_i^2/2`.

Pinsker's inequality gives `h_i^2 <= KL(u_i||v_i)/2`. Data processing from the complete half-path to the observation word and the stationary CTMC path-entropy identity give

`sum_i pi_i KL(u_i||v_i) <= t sigma`,

and the same bound with `u_i,v_i` exchanged. Consequently

`tr Z <= t sigma/4`.

**Theorem 2, spectral form.** Let `nu=tr((A0)_-)`, the sum of the magnitudes of all negative eigenvalues of `A0`. Then

`sigma >= 4 nu/t`.

In total-window notation `T=2t`, this is `sigma >= 8 nu/T`.

**Proof.** Since `A0+Z` is positive semidefinite, the negative spectral projector `P_-` satisfies

`nu=-tr(P_- A0) <= tr(P_- Z) <= tr Z <= t sigma/4`.

There is also an exact convex interpretation. The minimum of `tr E` over matrices satisfying `E>=0`, `E 1=0`, and `S+E>=0` is `nu`. Indeed, `S+E>=0` and `(S+E)1=r`, `1^T(S+E)1=1` imply `S+E-r r^T>=0` by the matrix Cauchy--Schwarz inequality; conversely that centered positivity implies `S+E>=0`. Thus this is precisely the minimum-trace positive correction of `A0`, attained at `E=(A0)_-`, which annihilates `1` because `A0 1=0`.

Keeping the stronger constraint `S+E` completely positive defines a potentially stronger quantity

`kappa_CP = inf {tr E : E>=0, E1=0, S+E in CP_k}`,

with `nu <= kappa_CP <= tr Z`. Hence `sigma>=4 kappa_CP/t`. Replacing CP by positive semidefinite plus entrywise nonnegative gives an intermediate tractable relaxation. CP membership is not generally tractable, and none of these necessary constraints proves that a candidate table has a reversible CTMC realization.

### Nonlinear strengthening

For any two probability laws with total variation `h`, binary coarse-graining on the set where the first density exceeds the second yields

`[KL(u||v)+KL(v||u)]/2 >= 2 h atanh(h)`.

To verify the constant directly, the binary probabilities have the form `p=q+h`; minimizing the binary Jeffreys divergence over `q` gives `q=(1-h)/2`, `p=(1+h)/2`. The half-Jeffreys divergence there is `2h atanh(h)`.

The function `f(s)=sqrt(s) atanh(sqrt(s))`, `0<=s<1`, is increasing and convex: its power series is `sum_{n>=1} s^n/(2n-1)`. Therefore

`t sigma >= 2 sum_i pi_i f(h_i^2) >= 2 f(sum_i pi_i h_i^2)`.

Since `sum_i pi_i h_i^2>=2 tr Z>=2nu`,

**Theorem 3.**

`sigma >= (2/t) sqrt(2nu) atanh(sqrt(2nu))`.

The same formula is valid with `nu` replaced by `kappa_CP`. All these quantities lie in `[0,1/2]`; the endpoint `1/2` forces infinite entropy under the declared model. Near zero, the nonlinear formula reduces to `4nu/t`.

The coefficients in the information inequalities are sharp individually. This audit does not prove attainability of the overall bound by finite CTMCs for every observed word table.

## 4. Scalar witnesses and observed midpoint sectors

Let `F` be any real function on words with range width `R=max F-min F`. Write `a_i=E_{u_i}F`, `b_i=E_{v_i}F`, and `d^F_i=(a_i-b_i)/2`. The reflected moment obeys

`E[F(A)F(B)] = E[((a_i+b_i)/2)^2] - E[(d^F_i)^2]`.

The same argument works after subtracting the constant `(E F(A)+E F(B))/2`, which removes the positive mean contribution and can strengthen the witness. A negative reflected moment or centered reflected moment `-gamma<0` implies

`gamma <= E[(d^F_i)^2] <= (R^2/4) E[h_i^2]`.

Thus

`sigma >= (2/t) sqrt(4gamma/R^2) atanh(sqrt(4gamma/R^2)) >= 8gamma/(t R^2)`.

For `F` in `[-1,1]`, `R=2`, the simple bound is `sigma>=2gamma/t`, or `4gamma/T` for `T=2t`.

If an actually observed midpoint event restricts the witness to a sector of stationary mass `p`, and the conditional contrast vanishes outside that sector, conditional Jensen improves this to

`sigma >= (2p/t) sqrt(eta) atanh(sqrt(eta))`,

`eta=4gamma/(p R^2)`.

Here `gamma` is the unconditional negative moment including the sector indicator. Disjoint observed sectors can be combined by summing their conditional entropy lower bounds. If `p` is estimated from data, an upper confidence bound on `p` gives a conservative substitution: for fixed `gamma`, `p f(4gamma/(pR^2))` decreases with `p` on its feasible domain. Taking `p=1` always recovers the ungated bound. Conditional or sector selection must be fixed before held-out validation, or covered by a simultaneous confidence procedure.

## 5. A stronger tractable representation by vector embeddings

The one-hot spectral result depends on the chosen word coordinates. A bounded-diameter embedding removes that arbitrary geometry and yields a useful SDP.

Define

`Gamma(M)=max_H -tr(H A0)`

subject to

`H>=0`, `H1=0`, and `Haa+Hbb-2Hab<=1` for every word pair `a,b`.

Such an `H` is the Gram matrix of vectors `g(a)` in a Euclidean space with pairwise distance at most one. The centering condition fixes an irrelevant common translation. The maximizer can have dimension at most `k`.

Let `c^g_i=(E_{u_i}g+E_{v_i}g)/2` and `d^g_i=(E_{u_i}g-E_{v_i}g)/2`. The exact matrix identity becomes

`G A0 G^T = Cov(c^g_i)-E[d^g_i(d^g_i)^T]`.

For any diameter-one embedding, maximal coupling gives

`||d^g_i|| <= h_i/2`.

Consequently

`Gamma <= E[h_i^2]/4 <= 1/4`,

and the same entropy argument proves

`sigma >= (2/t) sqrt(4Gamma) atanh(sqrt(4Gamma)) >= 8Gamma/t`.

In total-window notation this is `sigma >= (4/T) sqrt(4Gamma) atanh(sqrt(4Gamma)) >=16Gamma/T`.

This SDP dominates the spectral bound: `H=P_-/2` is feasible because every `e_a-e_b` has squared norm two, and gives objective `nu/2`. The family is monotone under refinement of the observed words at fixed window length: any coarse embedding can be lifted to the finer word alphabet, preserving its diameter and objective. Changing the window length also changes the prefactor and does not automatically give rate monotonicity.

This is an ordinary semidefinite program with `k(k+1)/2` real matrix variables and `O(k^2)` distance constraints. Its dependence is on observed word count, not hidden-state count. For alphabet size `q` and `m` observations per half-window, `k` can be as large as `q^m`; the method does not eliminate that word-complexity cost.

## 6. A finite-data protocol on one physical trajectory

### Assumption that pays for dependence and preparation

Assume a known uniform mixing envelope for the actual microscopic chain:

`alpha(s)=sup_x TV(P_s(x, .),pi) <= C exp(-s/tau)`.

The constants are part of the experimental guarantee. They are not obtained for free from the observed record. They can be much worse than the visible correlation time and can depend badly on hidden metastable states.

After any training phase, freeze the word map, window length, and witness. Wait a gap `g` before the first validation window and between successive validation windows. The first gap pays for equilibrium preparation from an arbitrary unknown starting state; no exact stationary reset is presumed. Conditional on every previous validation history, the next window's starting state is within `alpha(g)` of `pi`. Sequential maximal coupling therefore couples `N` validation windows to iid stationary windows independent of the training phase with total failure probability at most `N alpha(g)`.

Choose

`g=tau log(4 C N/delta)`

(or zero if the upper expression is negative). Then the total coupling failure is at most `delta/4`.

### Direct scalar validation

For a frozen uncentered scalar witness `F` in `[-1,1]`, record

`H_j=F(A_j)F(B_j)` in `[-1,1]`.

Let `bar H` be the sample mean and

`r_N=sqrt(2 log(4/delta)/N)`.

Hoeffding plus the coupling gives, with probability at least `1-delta/2`,

`E_pi H <= bar H+r_N`.

Thus the lower confidence value

`gamma_L=max(0,-bar H-r_N)`

may be substituted into the scalar entropy formula. A true negative gap `gamma` is resolved with margin `gamma/2` once

`N >= 8 gamma^(-2) log(4/delta)`.

This is a sufficient sample cost. It is not a claim that separating every window by such a gap is optimal.

The physical elapsed time, excluding training, is at most `N(2t+g)`. If each half-word uses `m` observation times, the number of observation readings is at most `2mN`, or fewer if shared midpoints are reused. The budget includes the first preparation gap and every decorrelation gap. Readout accuracy and timing resolution remain separate experimental requirements.

### Validating the centered vector SDP without estimating the full table

After learning a diameter-one embedding `g` on the training data, use `n` pairs of validation windows. For one pair write `x=g(A)`, `y=g(B)`, `x'=g(A')`, `y'=g(B')`, and set

`Zpair = (x.y+x'.y')/2 - (x+y).(x'+y')/4`.

For independent windows, `E Zpair=tr(G A0 G^T)`. Setting `c=(x+y)/2`, `d=(x-y)/2` and similarly for the second window gives the useful identity

`Zpair=||c-c'||^2/2-(||d||^2+||d'||^2)/2`.

Diameter one implies `Zpair in [-1/4,1/2]`, a range width of `3/4`. Therefore a one-sided confidence radius is

`r_n=(3/4) sqrt(log(4/delta)/(2n))`.

Use gaps with `2n alpha(g)<=delta/4`; then, with the same confidence accounting,

`Gamma_L=max(0,-mean(Zpair)-r_n)`

is a valid witnessed lower bound on `Gamma(M)`, and may be substituted into its nonlinear entropy formula. Discovery of the embedding can be expensive, but validation of a fixed embedding has no exponential word-table sample factor. No independence is required within a validation window; only the paid gaps between windows provide the iid coupling.

### Why an unknown mixing time cannot simply be omitted

There is no uniform finite record length for estimating stationary word probabilities over all finite irreducible CTMCs of unknown dimension and unknown rates. Even a two-state chain with switching rate tending to zero produces an almost constant finite record. Hidden regimes with arbitrarily slow switching also prevent uniform power against alternatives whose nonequilibrium behavior occurs in an unvisited regime. These examples rule out a distribution-free acquisition-rate claim. They do not prove that every conceivable finite-data test of reversibility is impossible without mixing assumptions.

## 7. Independent fixed-lag triple lower bound

For the proposed four-state example, take the supplied exact triple law on `a,b,c in {-1,+1}`:

`P_epsilon(a,b,c)=1/8 [1+r(ab+bc)+r^2 ac+m abc]`,

where `m=r^2(epsilon t)^2` and `0<r<1` is fixed at the chosen lag. At `epsilon=0`,

`P_0(a,b,c)=1/8(1+r ab)(1+r bc)`,

the stationary binary telegraph triple law. The underlying model must ensure positivity; alternatively it suffices here to restrict `|m|<(1-r)^2`.

Since `P_epsilon-P_0=m abc/8`, direct summation gives the exact identity

`chi^2(P_epsilon || P_0)=m^2/(1-r^2)^2`.

To check it, change variables to `s=ab`, `z=bc`, and the remaining free sign. The sum over that sign contributes two and the two geometric factors each sum to `2/(1-r^2)`.

For `n` independent triples, KL tensorizes and `KL<=chi^2` gives

`KL(P_epsilon^n || P_0^n)<=n m^2/(1-r^2)^2`.

Any test with type-I and type-II errors at most `delta<1/2` must therefore satisfy, by binary data processing,

`n >= [(1-r^2)^2/m^2] (1-2delta) log((1-delta)/delta)`.

At a fixed nonzero lag this is `Omega(epsilon^(-4) log(1/delta))`. A held-out bounded witness with gap proportional to `epsilon^2` attains the same power of `epsilon` through Hoeffding. This is a matching exponent for independent fixed-lag triple tests only. It is not a lower bound for every method that receives the complete continuously observed trajectory, for adaptive lag selection, or for interventions into the apparatus.

## 8. Novelty and scope audit

Classical reflection positivity of stationary reversible Markov processes is established prior machinery. A relevant primary reference is P. E. T. Jorgensen, K.-H. Neeb, and G. Olafsson, *Reflection Positive Stochastic Processes Indexed by Lie Groups*, SIGMA 12 (2016), 058, DOI 10.3842/SIGMA.2016.058.

Inferring positive entropy production from time-symmetric observations is also established. Skinner and Dunkel, *Improved bounds on entropy production in living systems*, PNAS 118 (2021), e2024300118, explicitly provide optimal bounds for specified multistep statistics and time-symmetric coarse observations. Their four-state clock discussion and direction-switching biased random walk are especially relevant comparators. The full article is available at https://pmc.ncbi.nlm.nih.gov/articles/PMC8106300/ .

Time-symmetric correlation-time inference is another comparator: Dechant and collaborators, *Thermodynamic Bounds on Correlation Times*, Physical Review Letters 131 (2023), 167101. Do not describe the present result as the first time-symmetric dissipation witness.

Targeted searches did not locate the exact centered reflection-defect/CP correction bound, its nonlinear form, or the bounded-diameter SDP above. That is not proof of priority. The defensible candidate contribution is the explicitly proved combination: an unknown-hidden-dimension representation, a convex observable calculation, and a paid finite-data route. Its novelty should remain qualified until a broader expert literature review.

No claim is made that the bounds are optimal over all hidden models, that every nonreversible observation must violate them, that CP reflection constraints are complete for finite reversible CTMC realization, that hidden odd variables are covered, or that the result alone constitutes a civilization-changing discovery.

## 9. Computational algebra check

A separate numerical check used 400 random finite generators of dimensions 3, 4, 5, and 7, with five half-window lengths for each. It verified the exact identity `S=C-Z`, the inequality `tr Z<=t sigma/4`, and `nu<=tr Z` within floating-point tolerance. This check supports algebraic implementation only; the proofs above establish the result, and the random examples do not establish tightness.

## Appendix A. Calibrated independent readout errors

Suppose the physical observable is binary, `Y in {-1,+1}`, and each distinct observation is independently flipped with known probability `eta<1/2`, independently of the microscopic dynamics. Set `rho=1-2eta>0` and write the recorded value as `Z=Y B_flip`, with `E[B_flip]=rho`. Thus `E[Z/rho | Y]=Y`.

For the gated triple witness

`H=(1-Y_0)/2 (Y_-+c)(Y_++c)`,

the corrected statistic

`H_tilde=(1-Z_0/rho)/2 (Z_-/rho+c)(Z_+/rho+c)`

is exactly unbiased conditional on the underlying ideal triple. This follows by multiplying the three independent conditional expectations. In particular `E H_tilde=E H`, so a confidence bound for its mean feeds into the same ideal population dissipation theorem.

The exact finite range is obtained from the eight possible recorded triples. More compactly, put `a=1/rho` and form the six numbers

`{(1+a)/2,(1-a)/2} times {(c+a)^2,(c-a)^2,c^2-a^2}`.

Let `L` and `U` be their minimum and maximum. For `N` independent or successfully coupled validation windows, replace the scalar confidence radius by

`r_N=(U-L) sqrt(log(4/delta)/(2N))`.

Then `gamma_L=max(0,-mean(H_tilde)-r_N)` is a valid negative-moment lower confidence value, with the same coupling-failure accounting as Section 6. For fixed `c`, `U-L=O(rho^(-3))`, hence resolving a gap `gamma` costs

`N=O(rho^(-6) gamma^(-2) log(1/delta))`.

Therefore a fixed nonzero readout error rate is tolerated whenever its calibrated `rho` is bounded away from zero; the error rate need not shrink with the requested sample precision. This is an explicitly paid statistical overhead, not error cancellation without cost.

The assumptions exclude readout-induced disturbance, temporally correlated flips, unknown drift of the flip rate, and unknown outcome-dependent readout errors. If `rho` is only estimated, its confidence interval and the resulting correction bias must be included. Obtaining calibration from known input labels is an additional experimental operation; it is not supplied by the observation record automatically. At `rho=0`, the readout contains no information about `Y` and the correction is impossible.

The inverse-corrected central factor can be negative. Consequently the elementary nonnegative-weight null-test proof in Appendix B must not simply be applied to the corrected statistic without a separate argument. The mixing-based held-out guarantee above remains valid.

## Appendix B. Stationary equilibrium null test without a mixing assumption

This independently audits the physics branch's no-mixing result. It is a hypothesis-test guarantee for equilibrium, not concentration of an arbitrary nonequilibrium stationary mean.

Assume the hidden chain is stationary and reversible. Let `P=P_t` be its transition operator over time `t`, self-adjoint on `L2(pi)`. Choose fixed functions `g` and `w` of the observed state, with `w>=0`, and let

`B=||w||_infinity ||g||_infinity^2`.

Record consecutive blocks of duration `2t`, sharing their endpoint observations, and define

`Z_r=w(Y_{(2r-1)t}) g(Y_{(2r-2)t}) g(Y_{2rt})`.

For `theta>=0`, define the tilted two-step kernel on microscopic endpoint states by

`K_theta(x,z)=sum_y P(x,y)P(y,z) exp[-theta w(f(y))g(f(x))g(f(z))]`.

Detailed balance shows that `K_theta` is self-adjoint on `L2(pi)`. Its entries are nonnegative. It need not be positive semidefinite, an important distinction.

Expand the exponential in its absolutely convergent power series. The coefficient of `(-theta)^j/j!` is

`A_j=D_{g^j} P D_{w^j} P D_{g^j}`,

where `D` denotes diagonal multiplication after composing with `f`. Each `A_j` is positive semidefinite, because `P` is self-adjoint and `w^j>=0`. Also `||A_j||<=B^j`.

Dropping the negative odd terms in quadratic-form order yields

`lambda_max(K_theta)<=sum_{j even} (theta B)^j/j!=cosh(theta B)`.

Nonnegative entries supply the other half of the operator-norm argument: by Perron--Frobenius, the spectral radius of this self-adjoint nonnegative kernel is its largest eigenvalue. Thus even if negative eigenvalues occur,

`||K_theta||=lambda_max(K_theta)<=cosh(theta B)`.

For a stationary start, the exact moment-generating function is

`E_pi exp[-theta sum_{r=1}^n Z_r] = <1,K_theta^n 1>_pi <= cosh(theta B)^n`.

Using `log cosh u<=u^2/2` and optimizing the Chernoff parameter proves

`P_pi[(1/n) sum_r Z_r <= -gamma] <= exp[-n gamma^2/(2B^2)]`.

No spectral gap or mixing time enters. For example, observing a negative average of magnitude at least

`B sqrt(2 log(1/delta)/n)`

rejects the stationary reversible all-even null with type-I error at most `delta`, even with the stated shared-boundary dependence.

### Scope of this null test

1. The start is stationary. For an arbitrary initial preparation, Section 6's paid mixing route remains valid. Apparent stationarity of a short observed record is not a substitute for that assumption.
2. The witness is fixed independently of the validation data. Learning a witness on an earlier portion of the same dependent path and then invoking this bound conditionally is not automatically valid. A finite predeclared witness family may instead be protected by a union bound, or a genuine separation/independence argument must be supplied.
3. The theorem controls a false declaration of nonequilibrium. It does not make the empirical negative average a high-confidence estimate of its nonequilibrium stationary expectation. Substituting the raw empirical gap into the population numerical entropy bound without the corresponding concentration argument is not justified.
4. The physical all-even time-reversal assumption and the observation model remain in force.

The tilted-kernel proof remains valid for a reversible discrete-time transition operator with the same two-step block construction; positivity of `P` as an operator is not needed because every coefficient contains the factorization `P D_{w^j} P`.
