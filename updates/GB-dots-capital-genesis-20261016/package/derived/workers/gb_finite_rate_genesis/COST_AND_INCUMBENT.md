# Exact exposure cost and the matched incumbent

Date: 2026-10-16. All optima below concern a proved sufficient EFFECT CERTIFICATE, not the unknown actual physical logical error.

## 1. Exposure kernel and an exact certificate optimum

For a parent protected by full pinching at Poisson intensity lambda(t), let j(t)>=0 bound its complete weak interaction, a=integral_0^tau j(t)dt, and Lambda=integral_0^tau lambda(t)dt. The uncapped parent certificate is

    C[j,lambda] = integral integral j(t)j(s)
                  exp[-|L(t)-L(s)|] dt ds,
    L(t)=integral_0^t lambda(v)dv.                         (1)

For scalar parity dephasing gamma, lambda=2gamma. Rates are representation/qualified generator parameters; lambda is not an acquired Hamiltonian peak or an energy measurement.

The Poisson count Lambda is a PHYSICAL measurement count only if actual full pinchings are the implementation. In a physical telegraph-Pauli implementation of gamma(Ad Z-Id), the actual mean involution-flip count is integral gamma=Lambda/2. Its rate-2gamma pinching cuts are LATENT labels of another dilation of the same averaged channel. They are not acquired detector events or twice as many physical pulses. Accordingly the same-pinch incumbent comparison in Section 4 is not a same-pulse-count comparison for the telegraph implementation; that hardware comparison must use the actual flip/ramp/control costs.

Push the action measure j(t)dt forward through L to a positive measure mu on [0,Lambda] of mass a. Then C is its energy for kernel K(u,v)=exp(-|u-v|). Among ALL positive measures of mass a,

    C >= 2a^2/(Lambda+2).                                (2)

Equality is attained by

    mu_* = a/(Lambda+2) [Lebesgue measure on [0,Lambda]
                        + delta_0 + delta_Lambda].        (3)

Proof: the K-potential of mu_* is constant 2a/(Lambda+2). For nu=mu-mu_*, its total mass is zero and

    E(mu)=E(mu_*)+E(nu),

where E(nu)>=0. An elementary positive-kernel decomposition is

    exp(-|u-v|)=exp(-u)exp(-v)
      +2 integral_0^min(u,v) exp[-(u-x)]exp[-(v-x)] dx.

It expresses E(nu) as a square plus an integral of squares, proving (2). Also E(mu_*)=2a^2/(Lambda+2). This argument establishes the global minimum of the UNCAPPED certificate. The capped parent effect can be smaller, and the actual error need not saturate any certificate.

For constant j=J on [0,tau], (3) is attained by the finite profile

    lambda(t)=0                           for 0<=t<h,
              (Lambda+2)/tau               for h<t<tau-h,
              0                           for tau-h<t<=tau,
    h=tau/(Lambda+2).                                     (4)

The middle interval has length tau Lambda/(Lambda+2); the integrated intensity is Lambda. At Lambda=0 use lambda=0. A stipulated maximum rate lambda_max must obey (Lambda+2)/tau<=lambda_max for this schedule; otherwise this optimizer is infeasible and (2) remains only a lower bound on the certificate. For a bounded nonuniform j, use zero intensity over the first/last action a/(Lambda+2) and lambda=(Lambda+2)j/a in the middle, subject to the same physical admissibility checks.

For a constant rate lambda=Lambda/tau the certificate is

    C_const = 2a^2 [Lambda-1+exp(-Lambda)]/Lambda^2,

with value a^2 at Lambda=0. The optimal schedule changes a finite-exposure constant; it does not change the leading 2a^2/Lambda law.

## 2. A paid count cap

For constant intensity and N~Poisson(Lambda), an exact count cap M with OVERFLOW DECLARED A WHOLE-PARENT BAD EVENT has sufficient parent budget

    p_M <= min(1, rho_M
         + 2a^2 exp(-Lambda) sum_(n=0)^M Lambda^n/[n!(n+2)]),
    rho_M=Pr(N>M).                                       (5)

This uses E[sum gap^2|N=n]=2tau^2/(n+2) on nonoverflow trajectories and the trivial effect I on overflow. Independent own-parent caps preserve the selected-parent product theorem. This is not the same as silently dropping extra events and retaining the original kernel. Conditional capping of the action-squared quantity can improve (5).

Physical positive-duration measurements require additional separation/endpoint handling. A cap on COUNT does not ensure enough separation between Poisson arrivals. Noise during finite measurement ramps must be included in the actual dilation or qualified residual model. The sharp generator theorem cannot convert lambda into feasible serial gate starts.

## 3. Full reservation and a conditional receiving certificate

For the scheduled-memory transfer retain all existing constants and their scope. If its accepted sufficient budget has the form

    delta_ideal + A nu/kappa + B kappa theta + C p <= R,

then theta is the WHOLE reserved time (correction, acquisition, reset, protector, inverse/readout, finite ramps, tails). The weak action a and the protector exposure Lambda refer to the same ACTUAL implemented interval where their Hamiltonian/generator model holds. One may insert p=min(1,C[j,lambda]) ONLY after qualifying the support, endpoint, independent geometry, and common-dilation conditions.

If entering/final finite-strength channels have a separately qualified independent complete-pinch component with weights q_in,q_out, the supplied endpoint-failure repair is

    p_total <= 1-q_in q_out + q_in q_out p_internal.

This is a conservative certificate floor, not an observed logical-error floor. For physically isolated generator-wise dephasers, q_e=product_a(1-exp(-2gamma_a s_e)); concurrent noise during those endpoints needs a new qualification. One cannot use the new interior kernel to declare the endpoints perfect.

For a separately proved full-process CP-control contamination model, fault weights must be added with its actual causal joint premises. For coherent residuals one needs the supplied common-dilation and initial-frame covariance theorem, e.g. sqrt(p_actual)<=sqrt(p_ref)+b_RMS, and must charge the complete ramp/wrapper action. A scalar budget without covariance does not imply zero-character correctness.

No hardware values for J,lambda,theta,residual actions, reset cost or detector support were acquired. The formulas are exact conditional cost targets.

## 4. Strongest equally informed incumbent

If exact full-G pinching is available as the same resource, N deterministic equally spaced internal pinchings give N+1 gaps and

    p_det <= min(1,a^2/(N+1))

for constant J. This is the supplied deterministic measured-cell construction, with the gap count stated explicitly. For integer expected Poisson count Lambda=N>0,

    a^2/(N+1) < 2a^2/(N+2).

Thus the deterministic incumbent has a strictly smaller UNCAPPED certificate than every Poisson intensity profile at the same expected count, before both are capped at one. It also has a fixed finite count and controllable spacing. The result is a dominance statement about these bounds under the same ideal pinching primitive, not a comparison of measured device performance. If the physically available primitive is only an autonomous continuous dissipator and not exact event pinching, deterministic full measurements are a DIFFERENT acquired interface; both acquisition costs must be compared rather than declared equivalent for free.

The strongest random/DD incumbent in primary art already supplies bath-retaining suppression O(g^2 T/rate), with explicit finite-width accumulated errors and overlap exceptions in Wang's 2026 continuous-process randomized compiling treatment. The present result improves a local joint-EFFECT interface and answers a supplied sharp-product question. It does not invent Zeno protection, Pauli tailoring, Poisson randomization, or a superior physical control protocol.
