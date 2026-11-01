# Finite acquired reference rate and uniform passage-time CDF accuracy

Status: new candidate consumer corollary, independently unreceived. It uses the
separately frozen root theorem `RESOLVENT_TO_SURVIVAL_ROOT_CANDIDATE.md`, SHA
2414f104c0b74b59796af2f24c9a93ac5300a1a6eee7bd1137e0adef1dbfee67,
and the actual constant-SPD quartic model/EXACT FULL Gibbs|A initialization of
the separately frozen MFPT receiver. Neither earlier freeze is changed.

## 1. Receiving the abstract spectral theorem from actual finite intervals

The root proof shows for the actual killed diffusion, equilibrium committor h
(which need NOT be computed), source-current bound B_A, mass M and slab mass S,

    sup_t |P_A(tau_B>t)-exp(-k0 t)| <= epsilon+d_init,
    k0=1/(beta M R), rho=S/M,
    epsilon=(1+rho)^2 B_A/(beta M^2 R)-1,
    d_init=rho+sqrt(rho(1+rho)).                          (1)

Its inverse quantities are finite zero-resolvent forms, not a presumed global
inverse. The current has already earned B_A and Q_S<=rho^2 B_A. The scalar trial
has earned capacity<=1/(beta R). No angular mixing, computed committor, spectral
gap or actual projected Markov law is a receiving premise.

Let the MFPT engine re-acquire exact outward Mlo<=M<=Mhi, Rlo<=R<=Rhi,
r>=rho and T_hi>=(1+rho)B_A/M, with T_lo=beta Mlo Rlo>0. Its ratio is T_hi/T_lo.
Then monotonicity gives a finite explicit bound

    e=(1+r)T_hi/T_lo-1 >= epsilon,
    d=e+r+sqrt_upper(r(1+r)),
    k_lo=1/(beta Mhi Rhi), k_hi=1/(beta Mlo Rlo).          (2)

Every positive root is enclosed upward by exact integer arithmetic. The new
law cannot simply be copied from an old MFPT certificate: its spectral/source
hypotheses, additional root, original external KS tolerance and actual model
must be received, and all numerical work repeated or source-bound.

## 2. A single acquired exponential reference, not an unknown exact rate

Choose the exact rational arithmetic midpoint k_star=(k_lo+k_hi)/2. For positive
a,b and t>=0, the mean-value theorem and sup_t t exp(-ct)=1/(e c) give

    |exp(-at)-exp(-bt)| <= |a-b|/[e min(a,b)].

For b=k0 in[k_lo,k_hi] and a=k_star, the maximum relative quotient is at most
(k_hi/k_lo-1)/2. Since euler's number e>8/3,

    sup_t |exp(-k_star t)-exp(-k0 t)|
      <= (3/16)(k_hi/k_lo-1).                            (3)

Here the letter e in(2) is a spectral error, not Euler's number. Combining gives

    delta=e+r+sqrt_upper(r(1+r))
              +(3/16)(k_hi/k_lo-1),
    sup_(t>=0) |P_A(tau_B<=t)-(1-exp(-k_star t))|<=delta. (4)

Thus a requested Kolmogorov error is checked by ONE exact rational inequality.
This is an all-time absolute probability bound. Uniform accuracy of this CDF
does NOT imply a small relative error in tiny tail probabilities or unbounded
moments. The separate mean certificate remains separate and is not re-proved
by integrating a constant CDF error over an infinite horizon.

For a finite rational query t>=0, receive directed E_lo<=exp(-k_star t)<=E_hi.
Then the actual CDF lies in

    [max(0,1-E_hi-delta), min(1,1-E_lo+delta)].           (5)

At t=0 it is exactly zero, since initialization is inside A, separated from B,
and paths are continuous. Optional external absolute interval-width requests
must be checked after outward exponential error and truncation. Rarity-relative
accuracy is not promised. Exponential arithmetic and query counts are paid.

## 3. Why the all-time conclusion is compatible with zero spectral gap

The root spectral lemma controls the spectral measure of one committor vector,
not the full spectrum. It uses E X<=1 and E(1/X)<=1+epsilon, which are earned by
current and trial energies. Small positive spectral weight may lie arbitrarily
near zero. Scalar far-tail cutoffs already show the killed gap is zero in this
model; no isolated smallest eigenvalue or exact quasistationary exponential law
is inferred. A uniformly small absolute error can coexist with heavier extreme
tails. A restricted mean alone would not suffice; both energy directions and
the full A-versus-committor initialization comparison matter.

## 4. Scope and actual cost

The raw model is the complete ordinary constant-isotropic/diagonal mobility
and positive homogeneous quartic program. Exact full Gibbs|A is required; the
old engineered lift's fixed-ray preparation does NOT transfer. The theorem is
a mathematical predictive operation, not an empirical parameter or preparation
certificate. For the bounded CDF observable, an independently earned total-
variation preparation error can be added; it still would not certify the mean.

The wrapper must call the unchanged source-pinned MFPT engine, acquire its full
raw/coercivity/mobility and scalar/tail certificates, compute one extra outward
root and exact rate/error constants, then evaluate optional rational-time
queries with the previously reviewed directed exponential primitive. Additional
exp products consume the REMAINING original operation budget, not a fresh
uncharged one. All query/task types, bits, counts and arithmetic limits are
validated. Verifier recomputation binds every proof-bearing field to the
external original model/task; timing and work counters are diagnostics only.
