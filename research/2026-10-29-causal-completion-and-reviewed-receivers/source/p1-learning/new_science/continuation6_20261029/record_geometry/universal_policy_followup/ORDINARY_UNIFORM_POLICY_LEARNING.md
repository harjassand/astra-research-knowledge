# A constructive conventional receiver for all fixed-context policies

Date: 2026-10-29. Existing Astra P1 / record_geometry role.

The generic route here is established; see `PREDECESSOR_AUDIT.md`. This note makes one conventional finite-data receiver explicit, including target action probabilities equal to zero. Its continuous-class confidence statement is slightly broader than needed for the root's finite-grid policy-selection theorem. It is not a claim of a new physical principle.

## 1. Actual interface

An episode contains `H >= 1` action selections from an actual menu of `A >= 2` actions. A fixed supplied causal function of the recorded past provides the current context in `{1,...,S}`. Targets are all policies `q` with one probability row `q_c` per context and independent fresh action sampling at each visit.

The plant can have arbitrary hidden state and causal memory. Its initial law and its conditional physical kernel given the preceding history and actual action are common to all controllers. The comparison concerns the declared physical record; private selector keys are marginalized. Action timing must satisfy this same common-kernel interface.

The bank consists of `N` independent actual episodes from one warranted initial law. A conditional theorem holds after an old record when the same independence and deployment-start premises hold conditional on that record. Arbitrary repetition on one specimen does not supply this premise.

There are `J` tasks `R_j` fixed before acquisition, each recorded and valued in `[0,1]`. An arbitrary new function of the realized bank is not covered.

## 2. Universal behavior and change of measure

Reset the classical selector counts at each episode and select action `a` in context `c` with probability

\[
\beta_t(a\mid h_t)=\frac{n_{ca}+1/2}{n_c+A/2}.
\tag{1}
\]

For an episode `omega`, its marginal selector factor is

\[
Q_\beta(\omega)=\prod_c
\frac{\Gamma(A/2)}{\Gamma(n_c+A/2)}
\prod_a\frac{\Gamma(n_{ca}+1/2)}{\Gamma(1/2)}.
\tag{2}
\]

The chronological common plant factors cancel, giving

\[
\rho_q(\omega)=\frac{dP_q}{dP_\beta}(\omega)
=\frac{\prod_{c,a}q_{ca}^{n_{ca}}}{Q_\beta(\omega)}.
\tag{3}
\]

Use `0^0 = 1`. Counts suffice to compute the ratio, even when the physical dynamics are not exchangeable. Equation (3) can hold on a full latent plant-path extension, although only recorded task functions can be evaluated from the bank.

The Cover–Ordentlich individual-sequence bound gives

\[
0\le\rho_q(\omega)\le B,
\qquad B=2^S(1+H/S)^{S(A-1)/2}.
\tag{4}
\]

It follows by multiplying the context bounds `2(n_c+1)^((A-1)/2)` and using AM–GM. A smaller observed ceiling on sampled paths alone does not supply a smaller unseen-path ceiling.

Set

\[
\widehat V_j(q)=N^{-1}\sum_i\rho_q(\omega_i)R_j(\omega_i),
\qquad V_j(q)=E_qR_j.
\tag{5}
\]

For fixed `q,j`, summands lie in `[0,B]` and have second moment at most `B`, since `rho_q^2 R_j^2 <= B rho_q R_j^2`. Therefore a finite set `Gamma` of policies has, with probability at least `1-delta`, simultaneous error at most

\[
e_N=\sqrt{\frac{2B\ell}{N}}+\frac{2B\ell}{3N},
\qquad \ell=\log\frac{2J|\Gamma|}{\delta}.
\tag{6}
\]

This is Bernstein and a union bound. The sample requirement is linear in the domination ceiling, rather than the quadratic dependence from a range-only Hoeffding bound.

## 3. A grid giving uniform confidence on the entire continuous class

Take an integer `M > A`. In one row let `G_M` contain every vector `k/s`, where `k` has `A` nonnegative integer entries, `s = sum_a k_a`, and `M-A <= s <= M+A`. Put `Gamma_M = G_M^S`. Then

\[
|\Gamma_M|\le
\left[(2A+1)\binom{M+2A-1}{A-1}\right]^S.
\tag{7}
\]

For any `q`, normalize the componentwise floors of `M q_c` to obtain `q_c^-`, and normalize the ceilings to obtain `q_c^+`. The normalizers are positive. Both resulting policies belong to `Gamma_M`, and componentwise

\[
(1-A/M)q_{ca}^-\le q_{ca}\le(1+A/M)q_{ca}^+.
\tag{8}
\]

Multiplication along any `H`-stage history and nonnegativity of the tasks yield the deterministic empirical bracketing

\[
b\widehat V_j(q^-)\le\widehat V_j(q)\le a\widehat V_j(q^+),
\quad b=(1-A/M)^H,\quad a=(1+A/M)^H.
\tag{9}
\]

This does not require a positive lower bound on target action probabilities.

Flooring or ceiling and then normalizing changes a row by at most `2A/M` in `L1`. Thus its TV change is at most `A/M`. Couple actions maximally while histories agree, and use the same physical transition on matching histories/actions. The probability of any action mismatch is at most

\[
\alpha=HA/M.
\tag{10}
\]

Consequently `|V_j(q)-V_j(q^+)| <= alpha` and the same holds for `q^-`, without a Markov assumption on the plant.

Apply (6) on `Gamma_M`. If `alpha <= 1/4`, its simultaneous event implies

\[
\boxed{\sup_q\max_j|\widehat V_j(q)-V_j(q)|
\le3\alpha+2e_N=:E_N.}
\tag{11}
\]

For completeness, `a <= exp(alpha) <= 1/(1-alpha)`, so the upper error in (9) is at most

\[
(a-1)+a\alpha+a e_N
\le\frac{2\alpha+e_N}{1-\alpha}
\le3\alpha+2e_N.
\]

Bernoulli's inequality gives `b >= 1-alpha`; the lower error is at most `2alpha+e_N`. These inequalities prove (11) for every target, including all simplex faces.

## 4. Useful intervention selected after acquisition

A data-selected policy `qhat` within optimization error `zeta` of maximizing `Vhat_j` satisfies, on the same event,

\[
V_j(\widehat q)\ge\sup_qV_j(q)-2E_N-\zeta.
\tag{12}
\]

For any baseline `q_0`, it also has the actual-value improvement certificate

\[
V_j(\widehat q)-V_j(q_0)
\ge\widehat V_j(\widehat q)-\widehat V_j(q_0)-2E_N.
\tag{13}
\]

The complete selected policy may be untested. The theorem still uses the actual operation menu and the stipulated deployment start. It concerns a simultaneous frequentist event, not posterior confidence for every realized bank.

Taking `M` of order `HA/epsilon` gives the conventional sufficient episode scaling

\[
N=O_{A,S}\!\left(
\frac{H^{S(A-1)/2}}{\epsilon^2}
\left[S(A-1)\log\frac{H}{\epsilon}+\log\frac{J}{\delta}\right]
\right).
\tag{14}
\]

The native-call count is `NH`. Actual preparation and instrumentation costs are additional. Optimization of the empirical polynomial over the row simplices is not guaranteed efficient by the statistical proof.

## 5. A stronger deterministic-policy comparator

For deterministic maps `f: {1,...,S} -> {1,...,A}`, sample `f` uniformly at episode start. Equivalently, select a uniform action on first visiting a context and store it for later visits. The marginal physical-path mixture obeys

\[
P_f\le A^S P_{\rm atom},
\tag{15}
\]

independently of horizon. A finite policy library of size `L` similarly admits domination `L` by its uniform mixture.

A half-atomic/half-KT episode mixture gives domination `2A^S` for deterministic targets and `2B` for all randomized targets. Its marginal likelihood is used when computing weights; it does not identify its private branch key with a target's key. Randomized fixed-context policies may outperform all deterministic members, so the deterministic comparator does not replace the full theorem.

## 6. Actual selection and sensing costs

The KT probabilities are rational. Fair-bit rejection implements them exactly with finite expected bit use but potentially unbounded selector time. That time must satisfy the physical common-kernel premise. For a selected policy rounded to an executable one with per-context TV error `xi`, the same coupling as (10) adds at most `H xi` to bounded-task value error.

This receiver learns task values without reconstructing the hidden dynamics. It does not manufacture independent starts, precise sensors, faithful actuators or a common action clock. The companion `PHYSICAL_INTERFACE_FAILURES.md` supplies exact failures of stronger statements. No apparatus data, practical advantage, new generic mechanism or resolved priority is claimed.
