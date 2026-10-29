# Observable solver-gap bounds for actual-history guarded recovery
2026-10-29. New high-probability construction, independent review pending. This is NOT substitution of a realized gap sum into an expectation theorem.

## 0. Contract, filtration and fixed comparator
Use the accepted finite FTPL controller with d=35 features per star edge, m=n-1 edges, fixed rational probe probability p, public rational perturbation amplitude R>0 and midpoint count M. Write L=720. All source operations are fixed before the current private choices; actual product-probe feedback is candidate-independent. The complete neutral pre-role sampler schedule is required. A supplied fixed computation budget returns an actual rational quaternion and sound rounded-query lower bound on EVERY active round, never an action-dependent abort. This theorem does not build an engineering clock.

Use a two-stage pre-call filtration. First reveal only current NEUTRAL preflight success/count events, before revealing any accepted candidate/key/role indices. Their independence from accepted indices permits this equivalent ordering. Let H_(t-1) denote this pre-call filtration, including all actual earlier history and the declared causal source information needed to fix the current source map. It does not reveal current private actions, probe settings or role. If preflight aborts, that round is inactive and all its losses/feedback/gaps are0. The martingale proofs insert these preliminary count-only steps and use conditional expectation twice; they do not average an active loss against an unconditional probe rate diminished by a current abort. Current complete source memory may be correlated with the outer payload; the accepted orbit memory-effect identity supplies the needed correlated-input transfer. A fixed comparator tuple C* is chosen independently of the realized dataset. No hindsight comparator, counterfactual policy history or drifting-frame replacement is claimed.

After actual stopping, set all actual loss, feedback and gap variables to0 for analysis. No source calls, solver queries or imaginary observations occur. Potential increments then vanish. Hypothetical future independent role coins are used only for the existing finite-cap shortage coupling.

## 1. Always-valid bounded gap
For edge i let G_(i,t-1) be its accumulated feedback vector and Zhat its midpoint perturbation. Its quartic query is F(q)=(1/2)sum_j (G_j+Zhat_j)phi_j(q). Always retain a fixed rational unit-quaternion candidate and the trivial lower bound minus the coefficient-l1 norm. Any improved lower bound must be sound, and is replaced by its maximum with that trivial lower bound. Let e_it>=0 be the actual candidate value minus this retained lower bound.

Since ||g_it||1<=L/p on a probe and0 otherwise, and ||Zhat||1<=dR,

 e_it <= ||G_(i,t-1)||1+dR <= (T-1)L/p+dR =: B.       (1)

This is a public deterministic bound for the whole declared horizon. It does not assume successful optimization. Define e_t=sum_i e_it in[0,mB], mu_t=E[e_t|H_(t-1)], and Eobs=sum_t e_t. These gaps and their sum are acquired solver certificates, not physical logical-loss measurements.

## 2. Observable predictable-gap bound
Put c=1-exp(-1). For0<=e<=mB, convexity gives exp(-e/(mB))<=1-c e/(mB). Thus

 exp{sum_(r<=t) [c mu_r-e_r]/(mB)}

is a nonnegative supermartingale starting at1. Markov's inequality at the declared horizon yields, with probability>=1-delta_e,

 sum_t mu_t <= U_e := [Eobs+mB ln(1/delta_e)]/c.       (2)

The convenient entirely conservative form is U_e<=Ubar_e:=2Eobs+2mB ell_e when ell_e>=ln(1/delta_e), since c>1/2. One may therefore use Ubar_e instead of U_e. This controls the sum of conditional means on the ACTUAL stopped history, not a counterfactual uncapped solver. It is not an unconditional estimate of E[Eobs] obtained by plugging in one sample.

## 3. New high-probability true-loss regret
Let x_it be the returned feature action, x_i* the fixed comparator feature, xbar_it=E[x_it|H_(t-1)], and a_it=grad Phi(G_(i,t-1)), where Phi is the accepted continuous-box-smoothed minimum. Let z_it=E[g_it|H_(t-1)]. The actual true current loss difference is

 r_it=delta_it(C_it)-delta_it(C_i*)=z_it dot(x_it-x_i*).

The equality uses the unbiased shared product-probe feedback; the action-independent loss constant cancels. Each delta lies in[0,2]. Conditional current feedback independence is essential here.

The accepted variable-gap finite-difference argument gives, on active rounds,

 ||xbar_it-a_it||infinity <= min(1,sqrt((E[e_it|H]+dR/M)/R)).

On inactive rounds z_it=0, so no hypothetical approximate-oracle output is required. Define the centered martingale increment

 Y_t=sum_i {r_it - g_it dot(a_it-x_i*) - z_it dot(xbar_it-a_it)}.

It has conditional mean0. The sum of true action losses has conditional range length at most2m; the feedback term has range length at most2mL/p. Therefore Y_t has conditional range length at most2m(1+L/p), irrespective of correlations across edges. Conditional Hoeffding gives, with probability>=1-delta_m,

 sum_t Y_t <= m(1+L/p)sqrt(2T ln(1/delta_m)).          (3)

For completeness, the conditional Hoeffding lemma follows by twice differentiating the centered log-mgf: its second derivative is a tilted variance bounded by one quarter of the squared range. Integrating from0 twice gives lambda² range²/8, and exponential Markov gives(3). No independent quantum outcomes are assumed.

The potential step is PATHWISE in the observed feedback:

 sum_(t,i) g_it dot(a_it-x_i*)
 <= mdR/4 + (1/(4R))sum_(t,i)||g_it||1².

Let Vobs denote this observed sum of squared norms. Combining the pathwise potential, (2), (3), and Cauchy over all mT bias terms proves, with probability>=1-delta_e-delta_m,

 sum_(t,i)delta_it(C_it)
 <= Gamma_path + Hobs,                                (4)

 Gamma_path=sum_(t,i)delta_it(C_i*),
 Hobs=mdR/4+Vobs/(4R)
      +L sqrt[(mT/R)U_e +m²dT²/M]
      +m(1+L/p)sqrt[2T ln(1/delta_m)].

Replacing U_e by Ubar_e is valid. Every other quantity in Hobs is an actual certificate/feedback counter or declared public parameter. Equation(4), not an expectation substitution, is the new high-probability actual-loss statement. It is for each fixed comparator, not simultaneously for a retrospectively chosen one.

For exact fixed hidden joint symmetry, Gamma_path=0 on every actual history. For approximate symmetry one needs a PATHWISE budget Gamma_path<=Gamma_bar, or a separately justified high-probability bound. If only E Gamma_path<=gamma_bar is known, Markov supplies Gamma_path<=gamma_bar/delta_G with an additional delta_G failure allowance; do not silently treat an expectation as a pathwise promise.

## 4. Validation martingale and an honest observable readiness event
Let F_t be the actual indicator of validation failure on round t. Reveal the fresh candidate tuple at an intermediate proof filtration, but not its independent matching/permutation/probe/role keys. The neutral prefetch schedule permits this conceptual reordering because key laws and cap ranges are candidate-independent. The current matching inequality and source-memory marginal closure give

 q_t:=E[F_t | H_(t-1), current candidates] <= a alpha_n sum_i delta_it(C_it),
 alpha_n=2^n/Catalan(n/2), validation probability a.

The binary-outcome martingale has range1 per round. Hence with probability>=1-delta_v,

 F:=sum_t F_t <= a alpha_n sum_(t,i)delta_it(C_it)
                       +sqrt[(T/2)ln(1/delta_v)].       (5)

This remains valid for retained quantum memory, correlated outer payload and adaptive histories. It does not require conditioning on a latent Pauli fault label. On stopped rounds both sides' new increments are0.

Declare a nonnegative fixed/pathwise comparator budget Gamma_bar and compute the OBSERVABLE inequality

 a alpha_n (Gamma_bar+Hobs)+sqrt[(T/2)ln(1/delta_v)] < b+1.    (CERT)

Use conservative rational upper bounds when evaluating it. Define the event Cert to mean this inequality passes, a verified outer code was actually deployed, and no non-source resource/sampler abort occurred. This is a diagnostic event under the UNMODIFIED guard, not a new postselection rule or change to the accepted output instrument.

If J<=sT/2, the usual hypothetical independent role coins have service-shortage probability at most exp(-sT/8). On the simultaneous good events (4),(5), a run satisfying Cert cannot have stopped on b+1 failures; if it also has enough service coins, it must accept by the cap. Consequently

 Pr[reject AND Cert] <= delta_e+delta_m+delta_v+delta_G+exp(-sT/8).  (6)

Here delta_G=0 for a deterministic pathwise comparator budget. The same statement gives

 Pr[accept] >= Pr[Cert] - [delta_e+delta_m+delta_v+delta_G+exp(-sT/8)].

If Cert is defined WITHOUT excluding code/sampler abort, add their separate failure budgets. A lower bound on Pr[Cert] is still required for an unconditional high-yield conclusion. One observed certificate does NOT establish that probability. There is also no claim Pr[reject|Cert]<=the RHS without division by a justified positive Pr[Cert]. The original model-free accepted-map soundness remains its original UNCONDITIONED accepted-branch claim; postselecting that branch on a newly exposed diagnostic requires separate analysis.

## 5. Finite arithmetic and asymptotic interpretation
All certificates e_it and feedback vectors are rational. Choose delta_e,delta_m,delta_v as declared dyadic budgets. For delta=2^-k, the integer k conservatively bounds ln(1/delta). Use Ubar_e and an integer/dyadic rational upper square root, obtained by exact squared comparison, for each displayed radical. Thus (CERT) has a finite exact implementation without an irrational probability or square-root oracle. These are classical diagnostic costs, not an engineered hardware scheduler.

For fixed n,p, R proportional to sqrtT and M>=140T², Vobs<=m T L²/p² gives an O(sqrtT) potential/stability term. The loss martingale is O(sqrt(T log(1/delta_m))). If Eobs=o(TR) and log(1/delta_e)=o(R), the new gap term is o(T), because B=O(T) and its extra uncertainty contribution is O(T^(3/4)sqrt(log(1/delta_e))). Polynomially small fixed-confidence budgets satisfy that scaling. In the fixed-four-spin concatenated compiler, b grows linearly in T. Hence sufficiently small OBSERVED gap budgets can eventually make (CERT) pass, but this theorem alone does not make those budgets likely for a particular solver.

The result moves the unresolved obligation from an unobserved expected solver gap to a computable observed diagnostic with a joint false-certificate bound. It does NOT prove every structured query is easy, an empirical conditional-error claim, a practical timing advantage, or an advantage over an equally informed adaptive full-path controller. The current loss surrogate can still be conservative relative to actual logical fidelity.

## Dependencies
Accepted finite FTPL theorem; accepted variable-gap fixed-clock theorem; exact product-probe loss identity; full-P Poincare/orbit memory-effect transfer; matching witness; neutral all-key sampler scheduling; actual arbitrary-error outer compiler and finite guard. Earlier sources are unchanged. New load-bearing parts are the observable supermartingale, true-loss martingale composition and joint-event certificate interpretation.
