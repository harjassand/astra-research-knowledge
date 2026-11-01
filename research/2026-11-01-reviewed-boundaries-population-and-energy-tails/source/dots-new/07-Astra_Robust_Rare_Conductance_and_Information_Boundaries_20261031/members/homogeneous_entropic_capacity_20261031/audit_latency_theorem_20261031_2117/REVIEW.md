# Independent theorem review: conductance versus Gibbs-conditioned mean latency

## Verdict, correction, and exact source boundary

**PASS for the corrected theorem-only source.** With one sufficiently large but thereafter fixed Gaussian fiber dimension, all actual positive transverse mobilities have conductances in an arbitrarily narrow common multiplicative interval, while their Gibbs-conditioned mean hitting times have extended liminf infinity as mobility decreases to zero.

Accepted source: `CONDUCTANCE_LATENCY_SEPARATION_ROOT.md`, SHA-256 `132ac753d4dff456f61eb3e566a113222935dfde54d46e70dc75b4a81a1ac174`.

The first submitted source, SHA-256 `bc42d7780e509e2a86ca0e28cd022c256c9b14fe75f6420f0d269e111f4efb0b`, called minus infinity a natural endpoint for the fixed-u quartic diffusion. That classification was incorrect: it is a no-exit entrance boundary. I reported this immediately. The root corrected only that wording; all equations and the substantive claim were unchanged. Both initial and corrected source snapshots are preserved in this unique audit directory with matching SHA-256 values. The initial snapshot was reconstructed by reversing that exact textual substitution and verified against the originally supplied hash.

This acceptance is not a finite-gamma mean-finiteness theorem, a claim about medians or all quantiles, an executable certificate, a practical deployment guarantee, or a novelty claim. No prior accepted artifact was modified by this reviewer.

## 1. Actual model and normalizable initialization

The model is fixed at beta=1, U(z)=u=||z||^2/2, v(y)=1+(1-y^2)^2, and F=u v. For each gamma>0, the declared actual mobility is diag(1,gamma I_m), with matching reversible drift/noise and zero cross covariance. The same normalized Gibbs law mu applies to all gamma. A and B remain the full fibers y<=-1/2 and y>=1/2, and every process starts from the SAME mu(.|A).

Gaussian integration gives a y marginal proportional to v^-m/2, whose tails are |y|^-2m. The complete Gibbs partition and basin mass are finite and positive for all m>=1, hence certainly for m>=3. A normalized probability density assigns zero mass to z=0, but even that exceptional frozen process would be nonexplosive Brownian motion.

For every fixed positive gamma, the prior global-process proof applies with p=2 and K=3/2:

    V_gamma=1+y^2+(3/(2 gamma))||z||^2,
    L_gamma V_gamma=-2[y v'+3v]u+2+3m <=2+3m.

Here yv'>=-1 and v>=1 imply the bracket is at least 2. Thus the actual smooth full diffusion is nonexplosive, with the finite reversible Gibbs law used by its Dirichlet capacity. Gamma zero is never admitted as a finite-SPD actual family member; it is only a limiting proof device.

There is also an independent useful finite-time check. For W=1+y^2+||z||^2 and 0<=gamma<=1,

    L_gamma W=-2[yv'+2gamma v]u+2+2gamma m
                 <=2u+2+2m <=(2+2m)W.

So even a uniform linear Euclidean Lyapunov bound is available on this range. Its finite-time exit control is not a mixing bound or a mean hitting-time bound. The original proof does not need this strengthening.

## 2. Arbitrarily tight common conductance interval

The homogeneous energy exponent here is alpha=m/2, not m and not m/4. The prior family theorem gives

    0<k_parallel<=k_gamma<=k_free<infinity,
    k_free=1/(MA R0),
    R0=integral_slab v(y)^(m/2)dy,
    Rplus=integral_slab [4/(4-v(y))]^(m/2)dy,
    k_free/k_parallel<=Rplus/R0.

This follows from ordinary fixed-fiber Cauchy, the homogeneous scalar Jensen bound, and the scalar upper trial; the transverse term is either discarded as nonnegative or identically zero. Consequently gamma never enters the interval.

At zero, v/2=1-y^2+y^4/2, while [4/(4-v)]/2=1/(1+y^2-y^4/2). Their logarithms both have quadratic term -y^2. Both normalized scalar bases have a unique strict maximum 1 at the interior point zero on the fixed slab. Ordinary Laplace localization therefore gives the same leading factor for R0 and Rplus and proves Rplus/R0->1 as m->infinity.

For each epsilon>0, select one integer m>=3 with Rplus/R0<1+epsilon, then HOLD THAT m, potential, Gibbs law and initialization fixed while gamma decreases. No interchange of m and gamma limits is used. The existence of such a finite m is a theorem consequence, not an executed numerical tolerance certificate in this note.

The actual conductances need not be equal. In the previously reviewed scalar-mobility path they vary with gamma, and exact k_gamma can contain information not present in a common finite-width interval. The accepted obstruction concerns that common interval and equilibrium law, not a claim that an exactly known conductance plus additional model information can never identify gamma.

## 3. Exact one-dimensional mean-hitting formula

Fix u>0 and b=1/2. The frozen process has generator

    L_u f=f''-u v'f'.

Define Q(s)=integral_(-infinity)^s exp(-u v(r))dr, A(s)=exp(u v(s))Q(s), and

    t_u(y)=integral_y^b A(s)ds,  y<=b.

Then A'=u v'A+1, t'_u=-A, and t''_u-u v't'_u=-1, with t_u(b)=0. For each fixed finite y this integral is finite.

The boundary treatment can be justified directly, without borrowing any unsuitable metastability theorem. For s<=-2, v is convex on (-infinity,s] and v'(s)<0. Its tangent bound gives

    Q(s)<=exp(-u v(s))/(u|v'(s)|),
    A(s)<=1/[4u|s|(s^2-1)]<=1/(3u|s|^3).

Therefore integral_(-infinity)^b A(s)ds is finite: t_u is nonnegative and bounded on (-infinity,b]. The scale density is exp(u v), whose integral towards minus infinity diverges. The finite integral of A is precisely the entrance rather than natural behavior; no path started at a finite point exits through minus infinity.

For a finite left endpoint a<y, stop at sigma_a=tau_a wedge tau_b. Dynkin's formula on [a,b] yields

    E_y sigma_a=t_u(y)-t_u(a)P_y(tau_a<tau_b).

The scale formula gives

    P_y(tau_a<tau_b)
      = [integral_y^b exp(u v(s))ds]
        /[integral_a^b exp(u v(s))ds] ->0 as a->-infinity.

Because t_u(a) is uniformly bounded and the frozen process is nonexplosive, sigma_a increases to tau_b. Monotone convergence establishes E_y tau_b=t_u(y). This exact exhaustion proves the displayed formula and shows why the originally incorrect boundary label did not invalidate it. No unproved boundary term is dropped.

## 4. Lower constants and the m>=3 divergence

For u>=16 set a_u=1/sqrt(u)<=1/4. If y<=-3/4, the barrier interval [-a_u,a_u] lies between y and b. The well interval [-1-a_u,-1+a_u] lies inside (-infinity,-3/4] and entirely to the left of every point in the barrier interval.

On the barrier interval,

    v(s)=2-2s^2+s^4 >=2-2/u.

On the well interval, writing r=-1+x with |x|<=a_u,

    v(r)=1+x^2(2-x)^2
         <=1+81/(16u) <=1+6/u.

Thus the two integration lengths are both 2/sqrt(u), and the exponential difference is at least u-8. The claimed lower bound is exactly

    t_u(y)>=4 exp(-8) exp(u)/u.

The same well interval gives

    integral_(-infinity)^(-3/4) exp(-u v(y))dy
      >=2 exp(-6) exp(-u)/sqrt(u).

Multiplying produces 8 exp(-14) u^-3/2. Under u=||z||^2/2, radial Lebesgue measure is c_m u^(m/2-1)du, with a finite positive dimensional constant c_m. Hence the unnormalized initial Gibbs average of t_u is at least

    8 exp(-14)c_m integral_16^infinity u^(m/2-5/2)du.

The exponent is at least -1 exactly when m>=3; the threshold case m=3 diverges logarithmically. Tonelli is applicable throughout because all quantities are nonnegative. Dividing by the finite positive unnormalized basin mass yields T_0=infinity. This is a divergence in the frozen initial energy mixture, not a divergent Gibbs partition or an invalid starting law.

For each fixed u>0 the point-start mean is finite, as shown above. Infinite mixture mean and finite pointwise conditional means are fully compatible; no unjustified interchange of a signed integral is involved.

## 5. Transfer to actual strictly positive mobilities

All processes can be coupled with the same initial draw and the same longitudinal/transverse Brownian motions. On any compact ball and for 0<=gamma<=1, their drift coefficients are uniformly locally Lipschitz. The drift difference tends uniformly to zero and the transverse noise difference is sqrt(2gamma)I_m. Stopping the processes before exit, ordinary local Gronwall/BDG estimates give uniform-in-time convergence in probability on every fixed finite horizon.

Localization is valid even without assuming uniform mixing. The limit path is nonexplosive and compact on each finite horizon. One may first restrict it to a large compact ball with arbitrarily high probability, then use the stopped difference estimate to prevent the approximating process from leaving a slightly larger ball. Alternatively the uniform linear Euclidean Lyapunov bound above gives common exit control. The initial law has finite W moment for m>=3: its y second moment is finite from the |y|^-2m tail and its conditional transverse second moment m/v(y) is at most m. Thus either route supplies genuine full-process compact-time convergence.

For a continuous path with tau_b^0>t, the maximum of Y^0 on [0,t] is strictly below b. It has a positive gap from the boundary, so every sufficiently close uniformly approximating path also survives to t. Accordingly the hitting-time functional is lower semicontinuous at the relevant continuous paths:

    tau_b^0 wedge H <= liminf_n(tau_b^(gamma_n) wedge H)

along an almost-sure uniformly convergent subsequence. No equality of hitting-time distributions, boundary crossing regularity, absence of atoms, or convergence of untruncated means is needed.

Given any sequence tending to zero, pass to a subsequence realizing the liminf of truncated expectations and then to an almost-sure uniformly convergent subsequence. Fatou yields

    liminf_(gamma down0) E(tau_b^gamma wedge H)
       >= E(tau_b^0 wedge H).

Since T_gamma>=E(tau_b^gamma wedge H), this holds as a lower bound for liminf T_gamma for each finite H. Let H increase to infinity. Monotone convergence and T_0=infinity give

    liminf_(gamma down0) T_gamma=infinity.

Every gamma in this conclusion is positive and finite. No singular process is offered as an implementation. No finite-gamma convergence modulus, gamma-selection algorithm, or finite-gamma mean-finiteness claim is inferred.

## 6. Prior potential theory and scope

I independently inspected the cited [Bovier–Eckhoff–Gayrard–Klein primary PDF](https://ems.press/content/serial-article-files/31525?nt=1), especially Section 2, equations 2.24–2.28, and its H.1/ND assumptions. Those identities involve Green functions and equilibrium-measure-weighted starting laws; the subsequent discussion calls for regularity control when relating them to point-start means. This supports the source's warning against substituting an arbitrary starting law. The paper's growth and isolated nondegenerate-minimum hypotheses are not met here: F(y,0)=0 along an unbounded flat valley. Its metastable asymptotic theorems therefore are not invoked. The present one-dimensional formula, divergence, and mobility limit were checked directly above.

The accepted conclusion is a task separation. Even with the potential, equilibrium law, Gibbs-conditioned initialization, and an arbitrarily narrow common capacity/mass interval, no finite uniform upper bound for this mean hitting time follows over the unobserved positive-mobility family. Obtaining an operational latency statement needs additional information or assumptions relevant to that task.

It does NOT establish: divergence of medians or every quantile; that all fixed-gamma means are finite; that exact capacity values are equal; a numerical construction of gamma for a requested latency; an impossibility with a fully known generator; a general failure of potential theory; or a priority/novelty claim.

## 7. Independent executed checks and preservation

`check_latency_algebra.py` passed **582 exact assertions** without importing candidate code. They check the barrier/well expansions, interval endpoint arithmetic, exponential constants, radial power and threshold, Lyapunov identities, Poisson-generator residual, the two Laplace quadratic coefficients, representative rational interval inequalities, and the corrected source hash. Representative checks supplement the all-point reasoning above; they are not a simulation-based proof.

No latency simulation or finite-gamma numerical certificate was substituted for the analytic argument. Initial and corrected candidate snapshots, input hash/correction record, script, results and this receipt are preserved in this unique directory. Earlier theorem/code freezes remain unchanged.
