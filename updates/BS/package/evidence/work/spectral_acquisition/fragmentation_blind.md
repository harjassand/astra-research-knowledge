# Fragmentation acquisition: a visibility obstruction and two finite-time repairs

Status: internally derived mathematical results, 2026-10-10. One subagent independently checked the boundary expansion and exact two-time identifiability result. No external proof review, formal verification, experimental validation, or historical-priority claim. This is useful restricted progress, not a historic breakthrough.

## Source and observation contract

Pinned repository: `harjassand/astra-research-knowledge`, commit `8aed7fd74eb14622ed5a0a3635a799374296e32a`.

Read entrypoint `00_START_HERE.txt`, `AGENTS.md`, current notice `frontier/cards/N528-no-sc-positive-noisy-fragmentation-inverse.json`, and originals:

- `updates/BQ/package/supplied/fragmentation_no_SC_positive_extension_2026-10-09/NO_SC_NOISY_RECOVERY.md`.
- `updates/BQ/package/supplied/fragmentation_no_SC_positive_extension_2026-10-09/FOCUSED_PROOF_PRIOR_AUDIT.md`.

The source explicitly assumes known positive alpha and gamma. Its noisy inverse estimates the increment density k on (0,L], using intact-atom counts, calibrated bins, and one aggregated tail category. It allows bounded BV k with k(0+)>0. Its reported O(N^(-1/3)) risk is conditional on the rate parameters and independent calibrated mass-tag acquisition; it does not identify the rates or claim an experimental observation model. The current repository notice is `source_derived_unreviewed`.

Here S starts at zero, has positive iid increments with density k, and jumps from s at rate alpha exp(-gamma s). Let P_t denote its law, f_t its positive-half-line density, a=alpha t, and c_a=a exp(-a). Time and log-size coordinates are assumed calibrated. No unknown detector weighting or blur is silently admitted.

## 1. Exact obstruction: multiple times do not repair invisible post-break dynamics

**Theorem 1.** Fix L>0. If K((0,L])=0, observing the entire coarsened path

    Z_t = S_t if S_t <= L, and Z_t = tail otherwise,

for all t>=0 contains no information about gamma. Its law is an intact state at zero until an Exp(alpha) time, followed permanently by the tail state. This holds for every gamma>0 and for bounded smooth increment densities supported in (L+1,L+2).

**Proof.** The first waiting time has rate alpha, independent of gamma. The first positive increment exceeds L almost surely. Positivity of all subsequent increments makes the tail absorbing for the observation. Thus all observed randomness consists of that first waiting time. QED.

The conclusion is stronger than a one-endpoint alias: no finite or continuous temporal sampling of the same coarse state repairs it. Full untruncated sizes, a measured tail shape, or a different initial-size intervention would change the interface.

**Quantitative corollary.** Put

    k_epsilon(s) = (epsilon/L) 1_(0,L)(s)
                   +(1-epsilon) 1_(L+1,L+2)(s).

For fixed L this family has uniformly bounded density and BV norm, and every epsilon>0 gives a positive boundary trace b=epsilon/L. For any gamma_0 != gamma_1, couple their first jump time and first increment. Unless that increment belongs to (0,L], their entire coarse paths coincide. Therefore, with TV defined as sup_A |P(A)-Q(A)|,

    TV(path law at gamma_0, path law at gamma_1) <= epsilon.

For N independent parents/tags, TV of the complete observations is at most N epsilon, by product coupling. For every estimator of gamma,

    max_j E_j |gamma_hat-gamma_j|
      >= |gamma_1-gamma_0| (1-N epsilon)/4.

Proof of the last display: turn the estimate into the nearest-of-two test. A wrong test incurs absolute error at least half the parameter separation; the minimum sum of testing errors equals 1-TV. This gives the stated maximum-risk lower bound.

Taking epsilon=1/(4N) leaves a lower bound 3|gamma_1-gamma_0|/16. Thus even qualitative positivity k(0+)>0 does not permit uniform consistent rate estimation on the bounded-BV class. A quantitative visibility/information assumption is indispensable.

The obstruction is not inherently an unphysical arbitrary-K phenomenon. Choose B large enough that 1/B<exp(-L), and a smooth symmetric random partition of unity supported near the equal B-way split, with every daughter fraction below exp(-L). Its mass-tag K has a smooth density supported beyond L. Mix this partition law with probability epsilon of a uniform binary split. The mixed mass-tag density has trace b=2 epsilon and fixed bounded-BV envelopes, while visible post-break dynamics occur with probability at most epsilon. The same coupling applies. This physical version assumes the observation retains tail mass, not the number or sizes of individual subthreshold fragments.

## 2. Two times identify gamma when the near-parent trace is positive

**Theorem 2.** Suppose k is bounded by M on (0,s0), with finite right trace b=k(0+)>0. For every fixed a>0,

    F_a(s) := f_(a/alpha)(s)/(a exp(-a))
            = k(s) + (a/2)[gamma s k(s)+(k*k)(s)] + R_a(s),
    |R_a(s)| <= C_a s^2,                     0<s<=s0, a.e.

One valid explicit constant, for gamma>0, is

    C_a = M gamma^2 [a/4 + a^2 exp(a gamma s0)/6]
          +(a/2)(1+a) gamma M^2 exp((1+a)gamma s0)
          +exp(a) a^2 M^3 exp(a M s0)/12.

Consequently, for distinct positive a_1,a_2,

    b = ess-lim_(s down 0) F_a(s),
    D = ess-lim_(s down 0) [F_(a_2)(s)-F_(a_1)(s)]/s
      = ((a_2-a_1)/2) b(gamma+b),
    gamma = 2D/[(a_2-a_1)b]-b.

The intact atom identifies alpha=-log(P_t({0}))/t. Hence two exact positive-time endpoint laws identify alpha and gamma in this class. The formulas do not estimate or assume the derivative of k. Density limits can be interpreted as essential limits, avoiding arbitrary choices of density representatives.

**Proof.** Decompose the endpoint density by jump count.

For exactly one jump, the normalized contribution is

    k(s) integral_0^1 exp(a(1-exp(-gamma s))u) du.

Writing z=a(1-exp(-gamma s)), use |z-a gamma s|<=a gamma^2 s^2/2 and |integral_0^1 exp(zu)du-1-z/2|<=z^2 exp(z)/6. This proves the first term of the remainder bound.

For two jumps let x be the intermediate position and u<v the two jump times. Relative to the zero-position path coefficient exp(-a)a^2/2, the integrand ratio has log

    E=-gamma x+alpha(1-exp(-gamma x))(v-u)
                    +alpha(1-exp(-gamma s))(t-v).

For 0<=x<=s, |E|<=(1+a)gamma s, hence |exp(E)-1|<=(1+a)gamma s exp((1+a)gamma s0). The normalized two-jump contribution is therefore (a/2)(k*k)(s), with error bounded by the second term of C_a times s^2, since (k*k)(s)<=M^2 s.

For r>=3, the time-integrated path coefficient is at most a^r/r!, while k^{*r}(s)<=M^r s^{r-1}/(r-1)!. Summing and using r!(r-1)!>=12(r-3)! gives the third term of C_a times s^2.

The normalized one-jump term tends to b; all other terms vanish at zero. Also (k*k)(s)/s tends to b^2 by bounded convergence after the substitution x=su. Subtract the expansions at the two times; the unknown k(s) cancels exactly. Division by s and passage to the limit give D and the displayed inversion formula. QED.

BV guarantees a right trace but supplies no quantitative trace-convergence modulus by itself. The result does not contradict Theorem 1, because b>0 excludes its exact invisible class; the quantitative corollary explains why small b makes the repair badly conditioned.

## 3. A finite-sample acquisition method and its cost

Impose quantitative assumptions b>=b0>0 and |k(s)-b|<=H s on (0,s0), with fixed compact positive bounds on alpha,gamma and fixed distinct positive times. Take independent endpoint cohorts at t_1,t_2. For 0<h<=s0 define

    C_i(h) = P(0<S_(t_i)<=h)/c_(a_i),
    b_hat = C_hat_1(h)/h,
    D_hat = 4[C_hat_2(h)-C_hat_1(h)]/[(a_2-a_1)h^2],
    gamma_hat = D_hat/b_hat-b_hat.

Clip the denominator below at b0/2 for a globally defined estimator; one may also clip gamma to its assumed compact range. Here C_hat_i is the empirical bin frequency divided by c_(a_i). This uses a single near-parent bin per time, not numerical differentiation of a fitted density.

Let J(h)=gamma integral_0^h s k(s)ds + integral_0^h(k*k)(s)ds. Integration of Theorem 2 gives

    C_i(h)=integral_0^h k(s)ds +(a_i/2)J(h)+r_i(h),
    |r_i(h)|<=C_(a_i) h^3/3.

The Lipschitz condition implies

    |J(h)-b(gamma+b)h^2/2|
      <= H(gamma+b)h^3/3+H^2 h^4/24.

Therefore the deterministic bias of D_hat relative to b(gamma+b) is at most

    [2H(gamma+b)/3 + 4(C_(a_1)+C_(a_2))/(3|a_2-a_1|)]h
       +H^2 h^2/12,

and the bias of b_hat relative to b is at most

    [H/2+a_1(gamma M+M^2)/4]h+C_(a_1)h^2/3.

For an explicit sampling bound, put B_i=a_i M exp(a_i M s0). The path series gives f_(t_i)(s)<=B_i on (0,s0), so the bin probability is at most B_i h. With z=log(4/delta), Bernstein's inequality gives simultaneously, with probability at least 1-delta,

    |C_hat_i-C_i| <= E_i
      := [sqrt(2 B_i h z/N_i)+2z/(3N_i)]/c_(a_i).

Thus add E_1/h to the b error, and 4(E_1+E_2)/(|a_2-a_1|h^2) to the D error. On the event |b_hat-b|<=b0/2,

    |gamma_hat-gamma|
      <= 2|D_hat-b(gamma+b)|/b0
         +[1+2(gamma+b)/b0]|b_hat-b|.

For N_i of order N and fixed parameters this yields

    |gamma_hat-gamma|
      = O(h + sqrt(log(1/delta)/(N h^3))
               + log(1/delta)/(N h^2)).

Taking h of order (log(1/delta)/N)^(1/5) gives an O((log(1/delta)/N)^(1/5)) high-probability rate. This is an upper bound only; no matching minimax claim is made. At fixed confidence, accuracy epsilon costs O(epsilon^(-5)) independent observations and size resolution h=O(epsilon), with constants worsening as b0 or |a_2-a_1| shrink or c_(a_i) becomes small.

If alpha is unknown, estimate it from an intact-atom cohort. For survival bounded away from zero and one, its error is O(N0^(-1/2)). Perturbing the normalizing coefficients and a_i in the contrast adds O(|alpha_hat-alpha|/h). Taking N0 of order N and h=N^(-1/5) makes this O(N^(-3/10)), smaller than the leading N^(-1/5) rate. A union bound accommodates use of the same endpoint cohorts, though independent calibration simplifies the proof.

Computational cost of the rate-acquisition statistic is linear in observed endpoints and constant storage after streaming bin counts. Combining this rate estimate with N528's supplied-rate inverse would add rate error through its explicit sensitivity term. The resulting available bound is generally O(N^(-1/5)), not O(N^(-1/3)); the acquisition cost dominates. This composition remains conditional on correctness of the source inverse and on its numerical defect/precision policy.

## 4. A stronger intervention: two initial sizes acquire the rates parametrically

If a laboratory can prepare two known monodisperse initial sizes x_1 != x_2 under the same physical rate law B(x)=alpha x^gamma, the intact probabilities obey

    p_j = exp(-alpha x_j^gamma T_j),
    lambda_j = -log(p_j)/T_j,
    gamma = [log(lambda_2)-log(lambda_1)]/log(x_2/x_1),
    alpha = lambda_1/x_1^gamma.

This requires no daughter-kernel information, boundary trace, or descendant independence. Each initial parent's intact indicator is Bernoulli. With probabilities bounded away from zero and one and fixed log-size separation, Hoeffding plus the displayed smooth transformation yields O(n^(-1/2)) rate-parameter error. For example, |p_hat-p|<=sqrt(log(4/delta)/(2n)) simultaneously. The derivative of log(-log p) is 1/(p log p), making the conditioning explicit. A small |log(x_2/x_1)| amplifies exponent error.

This is elementary survival calibration, not an invented fundamental method. It demonstrates that changing the experiment can remove the parameter confounding more efficiently than extracting tiny boundary contrasts from a fixed initial size. Preparation error, uncertain size calibration, unresolved intact particles, and detector drift must be budgeted; none has been solved here. If preparation is feasible at acceptable cost, O(epsilon^(-2)) calibration samples preserve the source kernel estimator's O(epsilon^(-3)) nominal sampling scaling.

## 5. Correlated descendants: what N actually counts

**Proposition.** Suppose N independent mass-conserving fragmentation trees start with mass one. At time T tree i has descendant masses X_(ij), summing to one. Measure the mass-weighted histogram

    H_(i,n) = sum_j X_(ij) 1_{-log X_(ij) in bin n},
    Y_n = (1/N) sum_i H_(i,n).

Then E H_(i,n)=p_n, the mass-tag endpoint probability, and

    E sum_(n<=m) |Y_n-p_n| <= sqrt(m/N).

**Proof.** Conditional on a realized tree, a uniformly selected initial mass point ends in descendant j with probability X_(ij), giving the expectation identity. Since 0<=H_(i,n)<=1, Var(H_(i,n))<=p_n. Independence across initial trees gives Var(Y_n)<=p_n/N. Sum Cauchy-Schwarz bounds and use sum_(n<=m)p_n<=1. QED.

This replaces the iid-tag histogram bound without pretending descendants are independent. Ancestor identities need not be recorded if every initial parent has the same known mass and aggregate mass is calibrated: summing the hidden H_i produces the same Y. N is the number of independent initial parents, not the final fragment count. Near-parent single-bin statistics also satisfy the needed Bernstein bound because each H_i is bounded by one.

Acquisition cost is not N scalar measurements. With at most B daughters per split and rates bounded by alpha (unit initial mass), the expected number of extant descendants per parent is at most exp(alpha(B-1)T), by a dominating branching process. Complete size readout can therefore cost up to N exp(alpha(B-1)T) in expectation. Direct independent mass tagging, complete weighted fragment readout, and unbiased subsampling are different experimental interfaces. An uncalibrated truncated number histogram does not satisfy this proposition.

## 6. Prior art and honest consequence

Primary sources checked live:

- Doumic, Escobedo and Tournus (2024), *An inverse problem: recovering the fragmentation kernel from the short-time behaviour of the fragmentation equation*, Annales Henri Lebesgue 7, 621-671, DOI 10.5802/ahl.207: https://www.numdam.org/item/10.5802/ahl.207.pdf . Journal pp. 625-628 explicitly assume the rate B known and give short-time kernel reconstruction, stability for initial spread/noise, and a Mellin approximation. This is a direct comparator, with broader initial-data treatment than the present exact boundary formulas.
- Doumic, Escobedo and Tournus (2018), *Estimating the division rate and kernel in the fragmentation equation*, Ann. IHP C 35, 1847-1884, DOI 10.1016/j.anihpc.2018.03.004: https://www.numdam.org/item/10.1016/j.anihpc.2018.03.004.pdf . It establishes uniqueness of the rate parameters and kernel from the long-time self-similar profile under its assumptions, with a Mellin representation. Thus unknown-rate identification is not new in general; a possible contribution here is specifically the two finite-time boundary cancellation and its explicit acquisition accounting.

The strongest useful principle is an experiment-design distinction: an inverse may be injective and stable with supplied rates while the experiment contains arbitrarily little information about those rates. A positive boundary trace alone does not fix this uniformly. Quantitatively visible near-parent mass supports a two-time acquisition route; a controlled change of initial scale can be much cheaper.

The consequential unresolved obstacle is an experimentally realizable, quantitatively calibrated observation/preparation protocol that estimates a nonparametric daughter law and its rates with favorable total cost despite initial spread, unknown detection bias/blur, and rare visible post-break events. No result here establishes that protocol or a transformative new general capability.

## 7. Numerical identity checks, not statistical benchmarks

For the exact solvable case k(s)=beta exp(-beta s), gamma=beta, the endpoint density is

    f_t(s)=a beta exp(-beta s) exp(-a exp(-beta s)),

with atom exp(-a). Direct differentiation verifies the forward equation, and direct integration verifies total mass one. Thus

    C_i(h)=expm1(a_i*(1-exp(-beta h)))/a_i.

For beta=gamma=1.3, a_1=0.5, a_2=1.5, the deterministic cumulative-bin estimator produced:

| h | b_hat | gamma_hat | absolute gamma error |
|---:|---:|---:|---:|
| 0.10000 | 1.256963974 | 1.309629255 | 0.009629255 |
| 0.05000 | 1.278662601 | 1.305912236 | 0.005912236 |
| 0.02500 | 1.289382361 | 1.303236585 | 0.003236585 |
| 0.01250 | 1.294704707 | 1.301689125 | 0.001689125 |
| 0.00625 | 1.297355832 | 1.300862357 | 0.000862357 |

Reproduce using standard-library Python:

```python
import math
beta, a1, a2 = 1.3, 0.5, 1.5
for h in (0.1, 0.05, 0.025, 0.0125, 0.00625):
    C1 = math.expm1(a1*(-math.expm1(-beta*h)))/a1
    C2 = math.expm1(a2*(-math.expm1(-beta*h)))/a2
    bhat = C1/h
    Dhat = 4*(C2-C1)/((a2-a1)*h*h)
    ghat = Dhat/bhat-bhat
    print(h, bhat, ghat, abs(ghat-beta))
```

A second diagnostic separated beta=1.3 from gamma=0.7. It integrated the one-, two-, and three-jump contributions using 12-node Gauss-Legendre quadrature on increment simplices and positive 80-term uniformization of the associated at-most-four-state pure-birth chains. At s=(0.08,0.04,0.02,0.01,0.005), substituting the pointwise contrast and b_hat=F_(a_1)(s) gave gamma estimates (0.788215389,0.744855304,0.722614036,0.711353537,0.705688388). The omitted density terms are O(s^3), so their contribution to the contrast is O(s^2). These are finite diagnostic checks of factors and signs, not a measured statistical risk, minimax result, or experimental demonstration.
