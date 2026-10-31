# Direct immigration-death bridge by marked-Poisson thinning

31 October 2026. Unreviewed constructive source lemma for the bosonic compiler. This is ordinary marked-Poisson reasoning used to acquire an explicit coherent source, not a novelty claim. It replaces recursive bridge-CDF inversion; that earlier route remains valid at its separately priced scope.

## 1. Exact endpoint-conditioned law

Consider immigration rate nu>0, death rate delta>0 per particle, initial count n, final count m, and duration t>0. Write

    p=exp(-delta*t), beta=nu*(1-p)/delta.

Initial particles survive independently with probability p. Immigrants alive at t form an independent Poisson population of mean beta. Hence the number A of initial survivors, conditional on final m, has probabilities proportional to

    w_a=Binomial(n,a;p)*Poisson(beta,m-a),
    0<=a<=min(n,m).

After sampling A, independently generate:

1. n-A initial-particle death times, each exponential of rate delta conditioned to lie in[0,t].
2. m-A surviving-immigrant arrival times t-D, where D has that same truncated-exponential law. These immigrants have no death before t.
3. A FRESH independent Poisson(nu*t) count C of candidate immigrants. Their birth times are iid uniform on[0,t], and their lifetimes iid Exp(delta). Keep exactly the candidates whose birth plus lifetime is <=t, with both their birth and death events. Discard the others completely.

Sort these events chronologically, retaining their birth/death types. No particle labels are needed to recover the occupation path.

Proof: initial lifetimes are independent exponentials. The stationary marked arrival Poisson process splits independently into the region of immigrants alive at t and the region dead before t. The former has mean beta, and conditional on its population its arrival ages have density delta exp(-delta*u)/(1-p), 0<=u<=t. The latter has intensity nu ds*delta exp(-delta*ell)dell on s+ell<=t. Step3 is precisely independent thinning to that region. It is independent of both initial survivors and the independently generated alive-immigrant population. Thus conditioning the endpoint affects only A and the surviving population, not the dead-immigrant process.

The candidate process in step3 is NOT used to generate the conditioned surviving immigrants. Its rejected candidates are fictitious discarded work. Reusing those candidates as the actual alive population would change the law.

The construction produces the exact immigration-death bridge. In particular, type probabilities after sorting are the correct conditional birth/death probabilities without explicitly dividing by a continuation probability after each event. Occupation never becomes negative because every dead immigrant's death follows its own birth and there are only n-A initial deaths.

Boundary branches: at t=0 the kernel is identity (n=m gives the empty path; n!=m has zero weight). The compiler removes exactly zero-coupling modes initialized in vacuum. If the source is reused at nu=0 with excited input, use the pure-death branch: m<=n, exactly n-m iid truncated-exponential death times, and no immigrants; m>n has zero weight. At delta=0 the abstract pure-birth bridge, when m>=n, has exactly m-n uniform arrival times and no deaths; m<n has zero weight. These branches are not evaluated by logs of zero. The retained compiler modes and nontrivial time queries have strictly positive nu,delta,t.

## 2. No rare-endpoint arithmetic denominator

The relative weights have an especially stable form:

    w_a/w_0=binom(n,a)*(m!/(m-a)!)*exp(a*z),
    z=log p-log(1-p)-log beta.

The a=0 relative weight is1. Compute their logarithms, subtract their maximum, exponentiate nonpositive differences, and normalize a finite list. No tiny endpoint probability is divided by. Factorials involve only integers<=max(n,m). The numerical normalizer after maximum subtraction is at least1.

Use log p=-delta*t directly and log(1-p)=log(-expm1(-delta*t)). For small delta*t, stable series or log-exprel formulas avoid cancellation. Since beta=nu*t*(1-exp(-x))/x with x=delta*t, its logarithm is computable with precision polynomial in input bit lengths and log(1/t). Large negative log weights can be discarded at an absolute-error budget. No positive exp(delta*t) intermediate is formed.

A useful sensitivity check is

    dz/dt=-delta-2delta*p/(1-p),
    |dz/dt|<=delta+2/t.

The finite softmax therefore has TV derivative at most a conservative max(n,m)*(delta+2/t). This is not needed recursively: all draws use the same fixed input duration, with no updated-duration chain.

## 3. Endpoint-independent event cap

Conditioned on n,m,A, the total retained event count is

    V=(n-A)+(m-A)+2*C_kept <= n+m+2*C,
    C~Poisson(nu*t).

For r independent mode bridges with endpoints<=L, candidate counts sum to Poisson(U), U=t*sum_i nu_i. Thus

    V_total<=2rL+2 Poisson(U),

with NO endpoint-probability divisor. Choose

    H=ceil(U_max*(e-1)+log(100/eta))+1,
    K=2rL+2H.

Exponential Markov gives candidate-count overflow probability below eta/100 uniformly in every endpoint pair and allowed duration. For the bosonic windows nu_i=Gamma_i/2 and t<=1/[16r Gamma(L+1)], one may take U_max<=1/[32r(L+1)]. Counts are particularly small, but the deterministic cap is paid.

Sample each candidate count by a finite Poisson CDF scan through the remaining H budget; all remaining probability goes to overflow. Mean nu_i*t is bounded by U_max, so no large-mean sampler or rejection oracle is needed. Uniform count words, scans and unused event slots are padded reversibly. On overflow SELECT has zero good block.

A path leaving the physical Fock cube is also assigned zero immediately in the operator word. It is NOT resampled or renormalized. This keeps the untruncated positive kernel as a majorant and returns exactly the truncated Dyson sum.

## 4. Tie and boundary exclusions without rare conditioning

The truncated-exponential density is at most

    delta/(1-exp(-delta*t)) <= delta+1/t.

Surviving-immigrant birth times have the same density bound. Candidate birth times have density1/t. Candidate death times, prior to retention, have density at most1/t by convolution. A candidate's own birth/death separation is its exponential lifetime, with density at most delta. Different particles' times are independent conditional on their counts and A; mixtures over A preserve all uniform bounds.

Conditional on total candidate count<=H, there are at most K retained or candidate event times that matter. Union bounds therefore give

    Pr(any relevant boundary/tie or retention ambiguity within zeta)
       <= C*(K+1)^2*(1+delta_max+1/t0)*zeta

for all t>=t0. Retention ambiguity means candidate death near t. Cross-mode pairs are included. Same-candidate birth/death pairs use the lifetime bound rather than a false independence claim. There is no division by endpoint probability, since the draws already realize the conditional law directly.

Choose zeta<=min(t0/10,eta/[100(K+1)^2(1+delta_max+1/t0)]) with a sufficiently conservative fixed constant. Endpoint events and the cutoff-crossing flag are stable under time rounding on the retained set. Exact coincidences have zero reference probability.

## 5. Direct finite-bit draws and their coupling

The truncated-exponential quantile is

    D(u;t)=-log(1-u(1-exp(-delta*t)))/delta.

For the SAME uniform u, its duration derivative is

    partial_t D = u exp(-delta*t)/(1-u+u exp(-delta*t)) in[0,1].

Thus both D(u;t) and t-D(u;t) are1-Lipschitz in duration. Its uniform derivative on u<=1-sigma is at most t/sigma. Draw a finite uniform word and evaluate log/expm1 with absolute error allocated to the time grid. Removing uniform tails of total probability eta/poly(K) gives the stated derivative bounds at logarithmic bit cost. Zero or extremely small x is handled by stable series, not division of two inaccurate small numbers.

For candidate lifetimes draw a uniform V and use ell=-log(V)/delta. Exclude V below sigma with its probability charged. To avoid generating a very large lifetime, first test V>=exp[-delta*(t-birth)]. If not, discard that candidate. If retained, compute ell<=t. The test uses an independent V, so uniform strips around its computed threshold cost their width even though the threshold depends on the birth word. Arithmetic error in the retention test and its uniform word is budgeted by this strip. The final comparison birth+ell<=t is stable off the global boundary cut.

All categorical/CDF probability lists are certified, clipped to valid nonnegative masses and normalized. Absolute list error controls TV; finite uniform discretization costs only the sum of threshold widths. No union over all possible quantum endpoint/time inputs is needed: the error bound is uniform for EACH fixed input, hence controls the block diagonal source routine on their superposition.

If two durations differ, candidate Poisson counts couple with TV<=nu*|Delta t|; posterior A has the bound in Section2. Conditional on equal counts, initial/surviving times change by at most |Delta t|, candidate births likewise, and acceptance changes only near its priced boundary. This supplies an explicit duration-stability check, but there is no recursive duration denominator to amplify.

## 6. Coherent source and selected words

Use a product of finite uniform WORD registers; compute the categorical survivor count, candidate counts, times, event types and sort permutation reversibly. Every register and loop has a polynomial cap in r,L,log(1/eta), input lengths and log(1/t0). Both row and column preparations use the IDENTICAL endpoint-conditioned routine and seed labels. SELECT preserves those labels, applies the chronological system operator word and known number phase, and is zero on overflow or cutoff-crossing flags. Unpreparing inner work takes the arithmetic operator average. It does not measure the physical reservoir or system.

For occupation path n_i(s), the number phase is

    exp[-i sum_i Omega_i integral_0^t n_i(s) ds].

It can be computed from endpoint and event data:

    integral n_i(s) ds = n_final,i*t - sum_(events j of i) sign_j*time_j.

A time rounding h changes this phase argument by at most O(K*Omega_max*h), plus the separate external-duration error. A conservative O((K+1)^2 h) factor can also be used. This must be charged alongside the system-H0 interval errors. Large known frequencies require phase arithmetic bits logarithmic in magnitude and target error, not a loop of Omega*t rotations. This is explicit number-phase evaluation, not generic Hamiltonian fast-forwarding.

This source lemma does not by itself supply local row/column normalization, the complete first-event isometry, or the global physical-time comparison. Those remain in the separate compiler assembly.

## 7. Equivalent dead-immigrant source

An alternative exact source draws D~Poisson(nu*t-beta) dead immigrants. Their lifetime density is proportional (t-ell)delta exp(-delta*ell) on[0,t]. A truncated-exponential proposal accepted with probability1-ell/t has mean acceptance at least1/2, since the decreasing proposal density has mean at most t/2. Given ell, draw birth uniformly in[0,t-ell]. This is also a sound constant-acceptance construction when its rejection cap and arithmetic are charged. The thinning construction above avoids subtracting nu*t-beta and uses no rejection loop, while preserving the same endpoint-independent cap order. Neither representation is claimed new.
