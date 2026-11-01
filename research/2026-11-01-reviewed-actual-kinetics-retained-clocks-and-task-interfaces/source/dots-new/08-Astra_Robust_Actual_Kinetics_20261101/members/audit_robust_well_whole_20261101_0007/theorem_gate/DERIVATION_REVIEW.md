# Independent robust-kinetics theorem review

## 1. Verdict and exact boundary

**PASS, theorem-only; no source correction required.** The main source is `LOCALIZED_DENSITY_ENVELOPE_CANDIDATE.md`, SHA `cb68b2f121f89e2553b4f6330dee2b60ae185309b715491fe4ec487cac7b5366`. The separately scoped generic note is `GENERAL_ENVELOPE_CONSERVATIVITY_NOTE.md`, SHA `7a30632dc9f42e5eaaa8a16c0e26ce93cd72ff8611fd9faca929d23cc053bbfc`. Their author freeze is SHA `ee3dd448fccfe85cf42742b681c8a72cf41aff7ecb2b5787868fc44f7c5f2663`, 5735 bytes. These documents and the pending root source-comparison sketch were read in full and snapshotted. The root sketch is not treated as a previously accepted premise: its needed comparison is independently proved below.

Acceptance is of the mathematical statements under their actual-model and global-envelope premises. It is not acceptance of the executable, its finite outputs, numerical/reading/work budget, an unrestricted envelope parser, or physical preparation. The fixed atom-weight program and arbitrary C2 global-envelope theorem are distinct interfaces.

## 2. Actual family and global diffusion

Write x=y² and r(x)=(2x²+3x-1)/(1+x)². Direct algebra gives

    r(x)+1=x(3x+5)/(1+x)²>=0,
    r(x)-1=(x-1)(x+2)/(1+x)²,
    b'(y)=2y(x-1)[2kappa+e r(x)].

For 0<=e<kappa, the bracket is strictly positive. Thus b and v have the same monotonicity intervals; b(0)=1+kappa and b(±1)=1. In particular b<=v_* on the transition slab, so the denominator 2v_*-b there is at least v_*. The exact identity g=(v-1)x/[kappa(1+x)] proves 0<=g<=(v-1)/kappa<=v/kappa globally. All scalar tail and monotonicity claims are consequently global, not sampled facts.

The actual potential is F=vU+e g V. It is smooth everywhere and homogeneous of degree four in z even though it is generally not factorizable in y and z. Euler gives z.grad_z F=4F. Since yv'>=-kappa, it remains to bound yg'. Its only negative region lies within 0<x<1; there r(x)<=1 and

    yg'=2x(x-1)r(x)>=2x(x-1)>=-1/2

whenever r is nonnegative, while r<0 gives a nonnegative product. Therefore yF_y>=-(kappa+e/2)U and F>=U. With K_L=1+(kappa+e/2)/4,

    L[1+y²+K_L z^T M_z^-1 z]
      =2(1+K_L m)/beta-2yF_y-8K_L F
      <=2(1+K_L m)/beta-8U.

This strengthens the stated upper drift bound. The Lyapunov function is proper for every finite SPD M_z. Smooth local coefficients, stopping and the bound give a nonexplosive actual SDE from every deterministic initial point. The mobility is unchanged, constant diag(1,M_z), with unit longitudinal mobility and zero cross block. No mathematical current below is imposed as a force, control or new mobility.

The complete even-atom grammar is a valid sufficient certificate for global 0<=V<=U: every atom is nonnegative and every fixed weight lies in [0,1]. The pure-term lower floor gives U>=d0||z||^4/m. Declared interval weights represent an entire family of fixed time-independent actual models. They are not averaged into one generator and do not license adaptive time-dependent choices. The theorem can use another genuinely established global certificate; the executable cannot infer one from a few probes or from omitted terms.

## 3. Common normalization and actual starting law

Z0=int exp(-beta U) is finite, positive and unknown. The three densities exp(-beta F)/Z0, exp(-beta vU)/Z0, exp(-beta bU)/Z0 share exactly this scale, and obey w_b<=w<=w_v. Homogeneity gives int w_t dz=t^-alpha. Thus M_b<=M_actual<=M_v and S_actual<=S_v without evaluating the actual conditional angular partition. Finiteness follows from the entire v^-alpha tail, and b>=v gives a valid majorant for the b tail too.

A common density rescaling cancels in the source/mass/mean expressions. Using differently normalized actual and nominal probability densities would not preserve the pointwise comparison and is not allowed. The actual full Gibbs law conditioned on A is exactly w1_A/M_actual: its unknown total Gibbs partition cancels upon conditioning. None of these identities replaces it by the nominal law w_v1_A/M_v. Matching only a nominal marginal, using a fixed ray, or declaring a finite-bit approximation does not supply the required law.

## 4. Upper-source/lower-price comparison, independently derived

Let the already explicit nominal current j_E satisfy div j_E=w_v1_E in the distributional sense. The accepted well-current interface matching and whole-tail proof apply to this nominal witness; the actual density need not be its divergence. For every nonnegative smooth compact test f in the actual killed domain,

    <1_E,f>_w <= int_E f w_v = -int j_E.grad f.

The right side is nonnegative. With actual D=diag(1,M_z), weighted Cauchy gives

    <1_E,f>_w²
      <= [beta int j_E^T D^-1 j_E/w] E_w(f,f)
      <= [beta int j_E^T D^-1 j_E/w_b] E_w(f,f).

This is exactly where both the upper source and lower density are needed. No current for the unknown true source is substituted or assumed.

The killed form is a Dirichlet form, so positive-part contraction allows the positive-source variational supremum to be restricted to nonnegative functions. Nonnegative compact approximants are obtained by smooth positive-part truncations and local core approximation. The inequality therefore extends to the killed form domain. For r>0 take f=(K+r)^-1 1_E>=0. If its current price is B_E, then

    Q_E(r)=E_w(f,f)+r||f||_w²
          <=sqrt(B_E E_w(f,f))<=sqrt(B_E Q_E(r)),

so Q_E(r)<=B_E. Monotone zero-resolvent convergence earns finite actual Q_E before any finite mean, zero inverse operator or spectral gap is claimed. This supplies the positive-source comparison from the previously unreviewed root sketch, within the actual process assumptions proved here. It does not supply conservativity for arbitrary unbounded/state-dependent mobility.

No new boundary source is created: the nominal current has continuous normal flux at its piecewise y interfaces, its possible tangential jumps do not enter the normal distributional derivative, and compact killed-core tests have zero target trace. Current smoothing or pointwise decay at infinity is unnecessary. Finite weighted resistance and form-core closure are sufficient; the nominal full-tail estimates and the finite multiplier below price infinity honestly.

## 5. Homogeneous squared-density prices and the mixture issue

Use pi_s=s^alpha exp(-beta sU)/Z0. If h=2s-b>0, direct normalization gives

    int pi_s²/w_b=[s²/h]^alpha,
    int z^T M_z^-1 z pi_s²/w_b
        =[s²/h]^alpha E_pi_h[z^T M_z^-1 z].

Scaling z by h^-1/4 proves the latter expectation equals a fixed finite constant times h^-1/2. The constant may depend on U, beta and M_z, but cancels in the ratio to the nominal h=2s-v price. Its finite upper bound is the already proved coercivity/virial bound. There is no pointwise uniform ratio between the actual and nominal Gibbs densities; this argument is an integrated homogeneous identity.

For s>=v,

    2s-b=(2s-v)-e g >=(1-e/kappa)(2s-v)>0,

because g<=v/kappa<=(2s-v)/kappa. Hence longitudinal prices inflate by at most L_e^alpha, and linear-z transverse prices by at most H_e=L_e^(alpha+1/2), where L_e=(1-e/kappa)^-1. The declared strict inequality e<kappa is essential to this finite uniform multiplier; no endpoint extension is accepted.

The well homotopy contains a positive scalar mixture times z. Its square has nonnegative cross terms. For s,t>=v, the cross product has exact denominator s+t-b and price proportional to

    (st)^alpha (s+t-b)^-(alpha+1/2).

The same comparison s+t-b>=(1-e/kappa)(s+t-v) gives at most H_e times each nominal cross term. Integrating the nonnegative weights therefore bounds the entire mixture norm by H_e times its nominal norm, and hence by H_e times the inherited Cauchy upper. This checks the potentially delicate mixture step without assuming linearity of a squared norm. Conditional far-tail and S-current terms are covered as the special case s=t=v. Every relevant denominator stays positive over the full domain.

The rare slab A-current must be priced separately. It has j_y=M_v pi_(v_*) and j_z=0; its exact lower-density price is beta M_v² R_e, with the stated R_e. Charging H_e there would be valid but would erase the localized gain. Combining this exact slab price with H_e times the complete accepted non-slab cost gives B_A in (6), with no missing beta factor. Independently pricing the old nominal S current gives B_S=H_e beta S_v² R_v(1+C_s). The 128/16 tail constants and all nominal basin terms are retained, not recomputed with an unearned actual source.

## 6. Actual mean and trial-form lower bound

Positivity and inverse-form Cauchy give 0<=Q_AS<=sqrt(Q_A Q_S). At positive resolvent parameter the actual killed-process identity is

    M_actual E_actual,A int_0^tau_B exp(-rt)dt
      =Q_A(r)+Q_AS(r).

Only after finite B_A,B_S are earned does monotone convergence give the finite actual mean. Dividing by M_actual>=M_b proves (7). Since B_S=eta_v² C, C=H_e beta M_v² R_v(1+C_s), the proposed rational upper is exactly the inequality

    B_A+eta_v sqrt(B_A C)
      <=(1+eta_v/2)B_A+(eta_v/2)C.

It does not require B_S<=eta_v² B_A.

The nominal bounded scalar transition h has energy C0=1/(beta R_v), equals one on A, zero on B, and lies in [0,1]. It belongs to the actual killed form domain: the same compact core approximants converge because both actual L2 norm and actual energy are bounded by the nominal ones, with the same constant D. Equivalently direct finite-mass cutoffs and its zero target trace give membership. Actual energy is at most C0 because h has only a y derivative and w<=w_v.

Crucially <1_A,h>_w=M_actual exactly. Optimizing its scalar amplitude in the zero-resolvent variational formula yields Q_A>=M_actual²/C0. Therefore the mean is at least M_actual/C0>=beta M_b R_v. This is stronger than the root sketch's valid weaker M_b²/(C0 M_v); no nominal overlap or denominator has been silently substituted.

## 7. Spectral normalization using a mass lower bound

The source uses k0=C0/M_b, rather than C0/M_actual. This is still valid but needs checking directly. Let N=||h||_w², so N>=M_actual>=M_b. Positivity, 0<=h<=1_D and separate inverse-form Cauchy give

    Q_h<=(sqrt(B_A)+sqrt(B_S))²=:U_B.

For the h spectral law with X=lambda/k0,

    E X=E_w(h,h)/(N k0)<=M_b/N<=1,
    E(1/X)=k0 Q_h/N<=C0 U_B/M_b².

Finite Q_h removes a zero spectral atom but not spectrum accumulating at zero. Form/inverse Cauchy implies N²<=E_w(h,h)Q_h<=C0 U_B, so the displayed epsilon is nonnegative. This proves the spectral admission without pretending the mass lower bound is the actual mass.

The actual initialization comparison uses rho_actual=S_actual/M_actual. Its error function rho+sqrt[rho(1+rho)] is increasing, so the declared upper rho=S_v/M_b is safe. The spectral lemma then gives (10) for the exact actual Gibbs|A survival and hence its CDF. Rational upper (11) follows because

    (1+eta_v)(B_A+eta_v C)
      -(sqrt(B_A)+eta_v sqrt(C))²
       =eta_v(sqrt(B_A)-sqrt(C))²>=0.

A finite rate interval and midpoint penalty must refer to this k0 and be received consistently; the previously proved 3/16 relative-width penalty applies. Outward exponential queries remain a separate arithmetic obligation. None of this gives exponential moments, relative extreme tails, all-start passage laws or a preparation mechanism.

## 8. Localized asymptotic condition and full-tail limits

The expansions are exact to the stated orders:

    b(1+h)=1+(4kappa+2e)h²+O(h³),
    b(y)=v_*-(2kappa-e)y²+O(y⁴).

For the basin limit, b>=v gives the previous integrable full-basin scaled majorant [1+(9kappa/16)x²]^-4, and the pointwise limit has curvature 4kappa+2e. Thus M_b/M_v tends to sqrt[2kappa/(2kappa+e)]. No finite basin tail is discarded.

For R_e put u_e=(v_*-b)/v_* on [0,1/2]. The derivative formula gives

    -b'(y)>= (3/2)(2kappa-e)y,
    u_e(y)>=3(2kappa-e)y²/(4v_*),
    0<=u_e<=7kappa/(16v_*)<7/16.

Consequently (1+u_e)^-alpha has a fixed Gaussian majorant after y=x/sqrt(alpha), using log(1+u)>=u/(1+u_max). Its pointwise limiting curvature is (2kappa-e)/v_*. This proves the entire-slab ratio R_e/R_v ->sqrt[2kappa/(2kappa-e)]. These dominated-convergence arguments are valid for every fixed admissible kappa,e; no uncontrolled local Laplace replacement is needed.

The sufficient strict condition is

    L_e G_b<v_*, equivalently
    0<=e<7kappa²/(16+23kappa).

At kappa=1 it is exactly e<7/39. Since G_1<G_b and G_b>1, this suppresses all H_e-inflated non-slab terms relative to the main barrier, with the previously proved polynomial prefactors. For the separate S contribution, the exact positive identity

    a(v_*+1)-2v_*=kappa/8+9kappa²/16>0

implies G_b>=v_*/a. Hence the strict condition also implies L_e<a and eta_v H_e tends to zero. This last step is necessary for the conservative rational mean and spectral joins, not just the A-current.

The limiting sufficient mean upper/lower ratio and one plus the conservative spectral defect are therefore

    (M_v/M_b)² (R_e/R_v)
      ->(1+e/(2kappa))/sqrt[1-e/(2kappa)].

Subtracting one is O(e/kappa) near zero (leading coefficient 3/4 in e/kappa). The actual initial-law error tends to zero. These are conservative limits of certificates, not identities for actual member dynamics or a finite-dimensional error estimate. At the threshold the residual estimates need not vanish; no endpoint or uniform shrinking-gap extension is established. Large defects may correctly fail a requested finite tolerance. Arbitrary perturbations not vanishing at the specified critical points need not share this improvement.

## 9. Separate generic-envelope note: conservativity and all starts

For the note, F need only be actual C2 with vU<=F<=bU globally. Its derivatives need not satisfy the special Lyapunov bound. The finite **constant** SPD D assumption is sufficient by another argument.

Close C_c^infinity in the weighted symmetric gradient form. Smooth Euclidean cutoffs chi_R approach one in L2(w) and have E(chi_R)<=C²||D||m(total)/(beta R²). The triangle bound for energy makes this sequence form-Cauchy, so closedness puts 1 in the domain with E(1)=0. Spectral calculus gives P_t1=1 almost everywhere, and symmetry gives invariance. This uses each finite matrix, not a uniform upper bound on its norm across models.

It is important to identify this with the **minimal SDE**, not invent a conservative extension through infinity. On each bounded smooth domain, C2 F gives locally Lipschitz drift and constant nondegenerate diffusion; integration by parts identifies its stopped/killed SDE with the local Dirichlet form. Uniqueness of the local martingale problem supplies that identification. Increasing bounded domains have form cores whose union is dense in the global closure. The variational resolvents converge to the global form resolvent. Their SDE limits are precisely the minimal process up to explosion. Thus the closed-form semigroup is the minimal SDE semigroup for w-almost every starting point, and the latter is conservative almost everywhere.

To remove exceptional deterministic starts, fix delta>0. Each bounded-domain surviving transition has a Lebesgue density (local bounded-drift Girsanov against nondegenerate Brownian motion suffices). The minimal process surviving to delta is exhausted by those bounded-domain events, so its subprobability law at delta is absolutely continuous. Since w is strictly positive, it charges no w-null exceptional set. The Markov property therefore gives, for t>delta,

    P_x(zeta>t)>=P_x(zeta>delta).

Local existence implies the right side tends to one as delta decreases to zero. Every deterministic starting point is therefore nonexplosive. This closes the exceptional-start gap without assuming global bounded drift or a Lyapunov estimate absent from the generic envelope.

All subsequent source comparisons, masses and trial energies use only w_b<=w<=w_v and the fixed mobility. They therefore extend to this genuinely received C2 global-envelope class. This does **not** enlarge the fixed-atom executable parser or acquire an envelope from local data. Cross mobility, unbounded/state-dependent mobility, nonreversibility and nonsmooth local coefficients remain outside the note's declared interface.

## 10. Why finite formal Gibbs mass alone would be insufficient outside scope

The supplied warning is substantive. For beta=1 on the line, set w(x)=(1+x²)^-1, D(x)=(1+x²)². The formally symmetric generator is

    Lf=(1+x²)² f''+2x(1+x²)f'.

The transform u=atan x has L u=0 and transformed diffusivity one, so its minimal process is Brownian motion with generator partial_uu on (-pi/2,pi/2), killed at its finite exit. The x process explodes despite int w=pi. The cutoff-energy estimate in the generic note fails because D is unbounded. This verifies why finite formal mass is not a substitute for the actual constant-bounded-mobility/minimal-process argument; no stronger parser inheritance follows.

## 11. Independent checks, preservation and scope

The independent script passed **1,095 exact assertions** without importing candidate code. It checks profile/drift identities, global parameter fixtures, density-pricing denominators, strict threshold and S exponent gap, rational source joins, lower-mass spectral normalization in independently constructed finite weighted forms, and the excluded unbounded-mobility counterexample. All source hashes match.

The initial script invocation stopped because SymPy lacked the theorem's e<kappa branch assumption for one radical identity. That script and failure explanation are preserved. The successful version verifies the squared rational identity, while the proof and admitted-parameter fixtures supply positivity. This was a test-assumption issue, not a candidate-source failure.

The full actual Gibbs|A law remains a mathematical premise for every fixed model member. No finite local-probe acquisition, empirical calibration, hidden-term discovery, physical sampler, fixed-ray initialization, or small-TV mean guarantee has been earned. Uniform absolute CDF bounds permit separately justified TV error for that bounded observable only. Ordinary positive source comparison, Dirichlet forms, homogeneous scaling and Laplace asymptotics receive full credit; no historical priority, proprietary algorithmic separation or physical device is accepted.
