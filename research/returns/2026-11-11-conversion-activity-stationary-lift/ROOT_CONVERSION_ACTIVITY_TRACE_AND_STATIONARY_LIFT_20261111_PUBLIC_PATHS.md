Conversion-activity trace, harmonic occupation lift, and stationary perturbations
11 November 2026 Brisbane / 10 November UTC

1. Scope and exact assumptions.

This is a conditional STATIONARY completion interface for the existing elementary prefix design. It handles zero-conversion states and absolute occupation observables without assuming a physical-time spectral gap. The remaining conversion-clock coercivity inequality is NOT proved here for every reaction structure or every compiled design.

Fix an actual irreducible fine class Gamma and a reference generator Q=G+C. G consists of reversible binding/release channels; C consists of marked zero/unary conversions, including null and parallel labels. Let mu>0 be the reference invariant probability. Assume G is detailed balanced with respect to mu, and Q is invariant under mu. In the accepted actual-binding reference these follow from recursive prefix activities and complex balance. Consequently C itself is invariant under mu. All rates and mu below are proof objects; no unknown-error activity, stationary normalizer, hitting distribution or spectrum is supplied to the compiler.

G preserves the decoder. Each decoded fibre is finite, every fine species has positive decoded size, and N_fine<=n=|D z|. The existing local activation path reaches a state enabling a conversion in at most L_D=(D+1)^2+2 binding/release steps, unless the decoded class is a no-conversion singleton. That exact case is treated separately.

Put b(z)=sum_e q_e^C(z), beta=mu b, and A={z:b(z)>0}, B=Gamma\A. We use the all-marked conversion intensity, not all binding activity. Assume beta<infinity. Positive elementary rate bounds a_-,a_+ and the reference moment bounds in the accepted construction imply this. Independent fixed conversion multipliers r_e in [1-eta,1+eta] give the actual generator Q'=G+C'. Binding rates are identical after the already accepted error absorption.

2. Conversions cannot land in B; binding trace is exact.

For y in B, invariance of C gives sum_x mu(x)q_C(x,y)=mu(y)b(y)=0, where the marked matrix includes diagonal null labels. Every summand is nonnegative. Therefore NO positive-rate conversion from A can land in B. Its graph is unchanged by admitted positive multipliers. This observation uses invariance of C separately, not merely invariance of G+C.

Let H(z,a) be the G-hitting distribution of A from z in B. It is supported on the same decoded fibre. The finite-fibre activation path proves the hitting time is almost surely finite with finite moments. Deleting time spent in B produces the exact binding trace G_A on A; it is reversible with respect to the unnormalized restriction mu_A. Its off-diagonal rates are
 G_A(a,a')=G(a,a')+sum_(z in B)G(a,z)H(z,a').
The diagonal is the conservative one. The exact trace of Q' is G_A+C', with C' unchanged, because conversions stay in A. Neither a population truncation nor a modified physical reaction is introduced.

3. Conversion-activity time as an ANALYSIS representation.

On A define
 nu(a)=b(a)mu(a)/beta,
 Qhat=(G_A+C)/b,
 Qhat'=(G_A+C')/b.                                    (1)
The same REFERENCE b divides both generators. nu is an invariant probability of Qhat. This is the time change by integrated reference conversion activity after deleting B-time; it is not an emitted physical clock.

The reference marked conversion kernel
 P(a,a')=sum_(e:a->a')q_e^C(a)/b(a)
is stochastic AND invariant under nu: nu P=nu. This follows directly from invariance of C under mu. Null labels remain self-loops in P and are still counted.

For Dhat=Qhat'-Qhat and every f in L2(nu),
 |Dhat f|<=eta[P|f|+|f|],
 ||Dhat||_(L2(nu)->L2(nu))<=2eta.                      (2)
The second line is Jensen plus nu P=nu. Huge binding rates never enter this norm. No lower bound on b outside A, no minimum stationary atom and no finite-tree exponent appears.

Both activity-time processes are conservative in this prefix setting: conversion marks have total rate1 and respectively at most1+eta. Between their finitely many marks on a bounded activity-time interval, the binding trace stays inside a finite decoded fibre. Thus neither process can make infinitely many binding jumps in finite activity time. Null conversion marks cause no exception.

4. The one remaining coercivity input and the complete density bound.

Assume a KNOWN POSITIVE lower bound lambda for the L2(nu) contraction of Qhat on mean-zero densities. Equivalently, require the natural-form Poincare inequality
 Var_nu(f)<=lambda^-1 Ehat(f),
 Ehat(f)=-<f,Qhat f>_nu
       =beta^-1 E_Q(f_ext),                            (3)
where f_ext equals f on A and is G-harmonic on B. The second equality is the reversible binding-trace identity, with all conversions staying in A. The energy uses the reference Q and mu. The mean in(3) is nu f, not mu f. This is a CONVERSION-weighted trace inequality; it is not the failed all-firing criterion or a physical-time gap assertion.

If 2eta<lambda, Qhat' has a unique invariant probability with density F=1+g relative to nu, and
 nu g=0,
 ||g||2<=r:=2eta/(lambda-2eta).                        (4)

Proof on the actual countable chain: Dhat is a bounded L2 perturbation by(2). For two equal-mass densities, dissipativity and(3) give contraction at rate lambda-2eta. Start Qhat' from nu and let g_t be its density minus1. The forward equation and ||Dhat^*1||2<=2eta imply
 d||g_t||2/dt<=-(lambda-2eta)||g_t||2+2eta,
so ||g_t||2<=r. Moreover
 ||g_(t+s)-g_t||2<=exp[-(lambda-2eta)t]||g_s||2
uniformly for s>=0. Thus the densities converge strongly in L2 to a nonnegative mass-one F satisfying(4) and invariance. Irreducibility gives uniqueness and positivity. Bounded perturbation agrees with the conservative jump process established above; no unproved uniform gap of finite population cutoffs is substituted for(3).

5. Exact physical occupation lift through B.

For a nonnegative physical observable O define the binding-occupation reward on A
 R_O(a)=O(a)+sum_(z in B)G(a,z)
                    E_z^G integral_0^tau_A O(Z_t)dt.   (5)
In particular R_1>=1. Detailed balance of G and finite-fibre Green reciprocity give, for every boundary function f with integrable positive/negative parts,
 mu[O f_ext]=sum_(a in A)mu(a)R_O(a)f(a).              (6)
This identity can be proved within each finite fibre from H=(-G_BB)^-1G_BA and the mu-symmetry of the killed Green matrix, and then summed by monotone convergence. It does not require enumerating those matrices in the compiler.

Let w_O=R_O/b on A. Since mu is a probability, beta nu(w_1)=1. Define the normalized inverse-clock reward constants
 B_O=beta||w_O||_L2(nu)
    =[beta sum_(a in A)mu(a)R_O(a)^2/b(a)]^(1/2).      (7)
There is no required inverse-beta or rare-atom bound in these constants.

Extend F harmonically into B: F_ext(z)=E_z^G F(Z_tau_A). The invariant physical law is exactly
 mu'(z)=mu(z)F_ext(z)/mu(F_ext),
 mu' O=nu(F w_O)/nu(F w_1).                           (8)
To verify stationarity, the density solves G F_ext=0 on B, where conversion inflow/outflow vanish. On A the Schur-complement equation is the stationary trace equation. Finite expected total firing intensity, established below, justifies the countable stationary sums. The elementary physical network is nonexplosive independently: all positive increases of its total molecule count arise from zero/unary sources and have at most linear total intensity; a linear-birth comparison prevents finite-time population explosion. Thus the finite invariant probability in(8) gives positive recurrence on the actual irreducible class.

If B_1 r<=1/2, then |mu(F_ext)-1|<=B_1 r, and
 TV(mu',mu)<=B_1 r/(1-B_1 r)<=2B_1 r,                 (9)
 |mu' O-mu O|<=2[B_O+(mu O)B_1]r.                    (10)
For(9), conditional Jensen and(6) give mu|g_ext|<=B_1 r, including all states in B, followed by the normalization inequality. For(10), apply Cauchy--Schwarz to nu[g(w_O-(mu O)w_1)] and use nu(Fw_1)>=1/(2beta). These are WHOLE physical-law TV and ABSOLUTE observable errors, before decoding if desired. Weighted inverse-clock occupation, not event-law TV alone, pays them.

6. All reward constants have polynomial numerical bounds for this lift.

Here the only additional global assumption remains(3). The rewards in(7) are paid by the already available local path and reference moments. Let m count all fine labels and set
 r_n=min(1,a_-/[m a_+(n+1)^2]),
 T_n=(L_D/a_-)r_n^(-L_D),
 K_n=1+m a_+(n+1)^2 T_n.
The G-hitting time of A from B has expectation<=T_n: follow the bounded activation path in successive blocks until A is reached. Before A no conversion is enabled, so the earlier path argument uses binding rates alone. Total binding intensity at A is <=m a_+(n+1)^2. On a fibre, O<=(1+n)^j therefore gives
 R_O(a)<=K_n(1+n)^j.                                 (11)
This bounds a reward without dividing by a small fibre probability.

On A, b>=a_- since enabled mass-action factorials are positive integers. Also beta<=m a_+ mu(1+n). Consequently
 B_O^2<= [beta/a_-]mu[K_n^2(1+n)^(2j)].               (12)
For fixed R, L_D,m,j are fixed; K_n is a fixed-degree polynomial majorant in n,a_+,a_-^-1. The inherited actual-binding reference moments mu n^h<=C_(R,h)W^p_(R,h) for every fixed h make(12) an explicit computable polynomial in W whenever the compiled rate reciprocals and maxima are polynomial. A rational upper bound 1+B_O^2 may replace B_O; no square-root, normalizer, moment or hitting-probability oracle is emitted.

Equation(12) applies to decoded coordinates, all fine populations, and the quadratic bound for ALL marked physical firing intensities. Conversion errors enlarge that intensity by at most1+eta; binding rates are already actual. Thus(8) has finite polynomial stationary populations and total firing intensity, and(10) pays absolute decoded first moments. The reference static accuracy can then be combined by the triangle inequality on the SAME design.

7. Compiler interface and real unresolved operation.

Suppose a computable reciprocal-polynomial lower bound lambda in(3) is constructed for the ACTUAL elementary design used by the accepted nominal/finite-horizon compiler, uniformly over all absorbed binding-error references. Let C be a rational polynomial majorant of1,B_1 and every B_O+(mu O)B_1 needed for decoded first moments. For desired additional error epsilon/2, a sufficient rational choice is
 eta<=min(1/2,lambda/4,epsilon lambda/(16C)).           (13)
Then r<=4eta/lambda, (9)--(10) pay epsilon/2, and the tolerance reciprocal remains polynomial. The inherited absorption bounds the ACTUAL conversion distortion by8D delta, so choose delta<=eta/(8D), delta<=1/(16D), and the already constructed finite-horizon tolerance. No physical rate, network or clock is changed by this argument. Compiler binary work and full-cycle firings still use that SAME accepted elementary design and finite-horizon theorem; an activity-time mixing statement alone does not pay physical-time transient costs.

The all-R uniform construction of(3) is NOT supplied. A physical-time gap can vanish in the sequestered-prefix example, and ALL-binding-activity weighting can fail; neither directly refutes(3). Conversely, nominal product form, a bounded activation path, a first-conversion entropy estimate, or a finite-horizon mixing theorem does not prove(3). A bound only for another catalytic table, one finite class, nominal binding constants alone, or a different decoder is insufficient. The conditional theorem does not replace the full universal stationary/transient question with a gap subproblem, require this method, or claim every design has a positive conversion-clock gap.

What is constructed here is the exact separation G/C, deletion of b=0 states, a bounded conversion-only L2 perturbation in the correct clock, the countable stationary-density argument, and a harmonic physical-law/absolute-moment lift with paid polynomial rewards. This resolves those interfaces CONDITIONAL on the still-unconstructed compatible coercivity, without claiming the original full compiler.

8. Source and overlap contracts.

P3_PRO_66BC05_ELEMENTARY_RETURN_20261110.md201873UTF8/SHAfe306673d7dcabdce82db5a17150221130b3bd1e2397e2efbc19a3883b7f9266 supplies the accepted nominal/finite-horizon lift and actual-binding reference. Its available obstruction helper explicitly leaves b=0 harmonic extension, dual moment weights, canonical mixing and all-firing payment as separate operations. The exact recursive reference and local path/reward estimates are reused from ROOT_BIMOLECULAR_CONVERSION_SEGMENT_ENTROPY_20261110.txt11646UTF8/SHAbe7491e8094bc68c699d6d8364d51959f4a3550bf33c3ce64a9d54b9848ffa97. They are not new discoveries here.

ROOT_ACTIVITY_WEIGHTED_TIME_STATE_ERROR_TRANSFER_20261110.txt6172ASCII/SHA53f280c6cf029f961c1819ffc0f511d4ee07fab85783ee9fb19a8dfe4623f52e already proves a different generic all-activity relative-form transfer under physical-gap and activity-weighted assumptions. The dissipative perturbation principle is inherited mathematical machinery. Equations(1)--(12) change the clock, the zero-activity-state treatment, and physical occupation lift for the present conversion-only perturbation, rather than silently applying that older all-activity criterion.

Anderson--Craciun--Kurtz0803.3042v1, https://arxiv.org/pdf/0803.3042v1, Theorem4.1/proof and Section4.1 were refreshed. They provide conditioned product-form stationarity under complex balance and the detailed-balance foundation. They do not assert the conversion-clock gap or this error-uniform compiler. No new full-source transfer, numerical experiment, physical realization or native retrieval is assumed.
