# Review of the finite-scale corrector and pressure attack

Auditor, 7 November 2026. Reviewed constructor/FINITE_SCALE_CERTIFICATE_ATTACK.md first at SHA256 4daed6e4b7a1157fb38fbf3ff4382efc772c632201e5b64b7a42f5b0c708b758 and then the expanded/corrected version **42c53622d2c35a86d8acac1bc12a82bd6f31bcdb2e1269033dbc78067bf230a1**. Primary checks use the pinned Funaki–Gu–Wang 2404.12234v3, specifically (6.34)–(6.38), Proposition 6.7, Lemma 6.8/(6.70), Proposition 6.9, and (6.78)–(6.84). No main dossier or constructor file was edited.

## Verdict

**PASS for the one-dimensional scalar auxiliary operations, with the implementation/stopping qualifications below.** Shared seeds can produce one succinct deterministic local corrector with a simultaneous all-input approximation event; there is no exponential-input union-bound obstruction. The observed all-density residual test is valid. The revised canonical exterior correction is correct, and the canonical variance plus positive spectral/Feynman–Kac lift checks algebraically at its stated prescribed-coefficient scope.

This does **not** close a fully effective inhomogeneous finite-N weak-prediction theorem. Source/profile errors, the inhomogeneous corrected reference and the large-deviation/PDE cancellation remain to be assembled and bounded. The note accurately leaves this open. Neither a small corrector residual nor the pressure-input lemma alone certifies arbitrary finite-N prediction or new external forces.

## 1. Actual source construction and admissibility

The closed dual optimizer is generally not in F_0(Lambda^-); its whole Lambda^+ support and possible frozen-exterior dependence prohibit that shortcut. The corrected construction instead matches source (6.34)/(6.36): use open primal correctors on small cells, evaluate their density argument at the large interior's clamped empirical count, sum only sufficiently interior cells, and divide by the large volume.

In the source's scale indices, n=floor(m/(9d+3)) and cutoff epsilon=3^(-2dm/(9d+3)). In d=1, physical small side ell is Theta(b^(1/12)) and cutoff a is Theta(b^(-1/6)). Use the source's explicit integer count clamps M_*,M^* so the finite list of density values is unambiguous; rounding affects only the stated fixed-factor asymptotics. Source Proposition 6.7 already concerns this shrinking cutoff and gives uniform residual decay. It is not a fixed-cutoff theorem with an untracked a-dependent constant.

The Poisson solution for each small open cell is the correct variational f_p: G f_p=j_p and pi_b(ell+f_p) has the source's sign/normalization. Its persistent state is only the small interior. Thus the glued program depends only on the large interior, including the empirical-density index, and is an admissible density-free local function. In a residual test at external Bernoulli density rho, the program must still use its **internal empirical p**, never the external rho as an additional evaluation input. Otherwise it ceases to be one density-free F.

The checked scalar formula is one-dimensional. A general fixed-dimensional matrix/vector extension requires separate basis-direction and matrix confidence bookkeeping; it is not already proved merely by writing scalar c_(0,1).

## 2. Shared-seed finite program and all-input confidence

For each of Q_p polynomially many density values, fix M independent seed blocks. A call at input x resets each block to its stored initial seed position, performs the same prescribed capped finite-bit simulation rule, and averages its bounded scores. There must be no mutable global PRNG stream advancing across function calls. With this convention, repeated calls at the same input give exactly the same finite-precision value: one deterministic finite function is retained after acquisition.

For each fixed p,x, the M blocks are independent, even though values at different x share seeds. If the score bound is B_score=tau J, Hoeffding and a finite union bound give

M >= C B_score^2 e_f^(-2)[m_small log2+log(2Q_p/alpha)]

for simultaneous approximation of all Q_p times 2^m_small inputs, after allocating uniform bias separately. Evaluating or storing those inputs is unnecessary. Correlations across x do not invalidate this union bound.

The explicit open gap gives g^(-1)<=12ell^2/a^2=O(b^(1/2)) for the prescribed d=1 scales. Its truncation time is polynomial in b and log(1/e_f), including the log inverse product-weight term. Uniformization's proposal count is independent of the initial x, so a common hard cap yields an input-uniform finite seed length. Finite threshold error, random-time grid error, Poisson truncation and Poisson-count numerical sampling must all enter the uniform bias budget. The displayed H q_bits term is sufficient if q_bits accounts for all finite discrete choices, including the Poisson-count sampler; those initial-count CDF errors must not be silently omitted. Their additional polynomial count/log-precision cost is harmless.

The random-time representation f_p(x)=tau E_x j_p(X_S)+tail, S uniform on [0,tau], is valid. Locality allows j_p(x) to be computed by averaging the constant-sized ghost pattern relevant to each bond rather than enumerating the whole outside envelope. The program's fixed rounding, clipping, rate table and support must be retained along with its seeds.

Uniform sup error then controls the translated energy: only O(m) translates affect a specified bond, so |pi Gamma(F-Fhat)|<=C m e_F. With both function norms <=B_F, the energy perturbation is bounded by the stated polynomial expression C lambda m e_F(1+mB_F)+C lambda m^2e_F^2. This avoids demanding density differentiability from the sampled lookup program. It also handles adjacent empirical-count indices, provided the uniform approximation covers both.

Importantly, the direct residual certificate below is valid even if the uniform approximation event fails: Fhat is still a bounded admissible deterministic local function. The all-input approximation event is needed to prove efficient termination via the source construction, not to pretend every microscopic input has been explicitly tested.

## 3. All-density residual certificate and polynomial stopping

For frozen Fhat, Z_F=c_(0,1)[pi_(0,1)(ell+Gamma_F)]^2 is a nonnegative bounded finite-bit-local observable. Validation samples must be fresh conditional on the frozen program and rate table, or covered by a separately proved uniform validation bound. Sampling the construction data again without such an argument would invalidate a naive fixed-function confidence interval.

For a function of q Bernoulli bits, differentiating the product law coordinatewise gives |d E_rho Z/d rho|<=2q||Z||_infinity for all rho in [0,1]. Both constant configurations have exactly zero exchange score. Consequently the explicit endpoint cutoff a_R=e_R/(CqB_Z), a density mesh and bounded-score intervals certify an upper energy envelope on the entire unit interval. In its middle, the certified primal/dual interval gives a lower conductivity 2rho(1-rho)D_lower. The factors two and volume are correct: the translated score is already the conductivity energy, and F was volume-normalized during construction.

Relative rate uncertainty gives exactly

R_true(rho,Fhat)
 <=C_acquired(rho;Fhat)/(1-eta)-c_lower_acquired(rho)/(1+eta).

Positive consistent local-rate refinement and all associated confidence/bias budgets are required. A fixed physical systematic floor is not removed by more digital cell runs. The learned-table event, program-approximation event and fresh residual/coefficient validation events should be allocated over stages with a summable schedule such as 2^(-j^2), as in the dual compiler.

Polynomial stopping is justified by the actual source Proposition 6.7 and Lemma 6.8: exact source-glued functions have uniform residual <=C b^(-gamma), with fixed class parameters. Program approximation and validation errors can be kept below strict fractions of e_R using inverse-polynomial precisions and sample counts in b. The endpoint cutoff is inverse polynomial in the known program bound, so calling the density-interval compiler with that cutoff still has polynomial cost. These are conditional/high-probability complexity assertions; unknown convergence constants are not needed in the observed test. The same stage confidence-tail argument used for dual stopping supplies expected-cost control. A bare instruction to grow supports without these approximation and validation slacks would not by itself prove polynomial stopping.

## 4. Revised canonical exterior operation is valid

The original suspicion of r(F)-sized exterior dependence was incorrect. Source (6.78) defines

H_(L,zeta,F)=L_(Lambda_L,zeta) S_F,
S_F=sum_(x in Lambda_(L-r(F)-1))tau_x F,

and S_F is entirely supported inside the replacement block. Its exterior dependence after applying the generator comes only through the bare finite-range rates. In 1D the number of outside patterns is therefore 2^O(r), independent of r(F). Enumerating all block counts and these bare-rate boundary patterns is polynomial at fixed r. Typical-exterior sampling would still be an invalid replacement for the required supremum; the complete constant-range enumeration is the repair.

A_L has zero uniform-canonical mean, while B and H are generator images, so W=D(k/L)A_L-(B-H) is centered in each count/exterior fiber. Empty/full sectors vanish. Conditional uniform initialization and gap >=L^(-2) support a bounded random-time correlation estimator for V=<W,G^(-1)W>. A D interval perturbs W by <=e_D in 1D, and the stated resolvent/triangle bounds propagate both coefficient and microscopic rate errors conservatively. Positive empirical variance upper endpoints plus these errors yield a genuine uniform finite-block variance certificate.

For termination, **first obtain and freeze F with residual strictly below the intended canonical variance budget, then enlarge the replacement block**. Source (6.81)/(6.84) states

V/L=(1/2)R(k/L;F)+Q_L(F;k,zeta),

with Q_L bounded by C[L^(-gamma_2)+poly(r(F),||F||)/L] in 1D. Thus a sufficiently small fixed residual and fixed F give polynomial eventual smallness. Enlarging F's radius/norm arbitrarily at the same time as L, or retaining a residual floor larger than the target variance, would not justify stopping. No unknown source constant is needed to recognize the observed variance upper bound once obtained.

## 5. Positive pressure/Feynman–Kac lift: checked scope

For a positive reversible canonical G with gap g and centered multiplication W, set V=<W,G^(-1)W>, B=||W||_infinity. For unit f=a1+h and z=sqrt(<h,Gh>),

<f,(-G+sW)f><=-(1-|s|B/g)z^2+2|sa|sqrt(V)z.

Completing the square proves lambda_max(-G+sW)<=s^2V/(1-|s|B/g) when |s|B/g<1. There is no omitted first-order constant-mode term because W is centered on every fiber.

On a ring, each bond belongs to L-1 translated closed L-site blocks, so sum_x G_x=(L-1)G_N. For the stated potential (beta N/L)sum_x a_xW_x, the local tilt is s_x=beta a_x(L-1)/(NL). Conditional variational bounds then give pressure divided by N at most 2beta^2 A^2 V_max/L under beta A B/(Ng)<=1/2. Overlapping blocks need no independence. Prescribed time dependence is handled by the instantaneous operator-norm bound.

Entropy inequality relative to the stationary Bernoulli-1/2 path law costs at most H(mu_0|Bernoulli(1/2)^N)<=Nlog2, giving exactly

E integral_0^T (1/L)sum_x a_x(t)W_x(t)dt
 <=log2/beta+2beta A^2T V_max/L.

This controls a signed integrated expectation (and its negative), not automatically E of an absolute time integral or a path supremum. The prescribed a_x(t) restriction is essential. For example, on a symmetric two-state chain with W=+/-1, choosing the state-dependent multiplier a=W makes aW identically one; its spectral pressure is first order in s, contradicting a centered quadratic estimate. No feedback-control extension follows without a new argument.

## 6. Final status

The corrector program, observed all-density residual, uniform finite-block canonical variance and the stated pressure-input inequality are credible checked auxiliary operations at the explicit 1D local product-reversible assumptions. Their apparatus/model promises, conditional confidence and polynomial costs must remain attached. A complete finite-N profile/source/inhomogeneous-entropy theorem, its effective numerical constants and arbitrary external forces remain OPEN. This review does not certify that final theorem by accumulation of auxiliary lemmas.
