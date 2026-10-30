# Independent audit: strict-power uniform fast clearing

Reviewed 2026-10-30. Source: `STRICT_POWER_FAST_CLEARING_CANDIDATE.md`.

**Verdict: the strict-power bound passes.** The argument is a constructive short-time stochastic production estimate, not a mixing assumption. It holds for fixed positive coefficients, uniformly over a compact box of such constant coefficients. Arbitrary state-dependent controls are not covered by the fluid comparison.

## 1. Uniform deterministic startup along a complex path

The polynomial conservative vector field is locally Lipschitz, preserves the simplex, and is globally bounded/Lipschitz there. Every negative contribution to coordinate j contains that coordinate as a source factor, so on the simplex its total magnitude is <=C z_j. Hence an initially dominant coordinate remains >=e^-C/k throughout [0,1].

Fix a complex path from its pure source mX_i to mA. All species in a current source complex have already appeared either in the initial pure complex or in a preceding target, and so have assigned lower bounds. A genuinely new target species has source exponent zero on its first-introduction edge; its positive production is therefore bounded below by a product of already controlled coordinates. The remaining negative terms are bounded by -Cz_j. Integrating this differential inequality gives the next lower bound c t^(1+sum y_l L_l). Previously proved bounds continue to hold because their inequalities were valid on the entire time interval, not only until the next path edge.

Taking a finite maximum exponent and positive minimum constant over initially dominant species gives z_A(t)>=c t^L uniformly over every initial simplex point. If A was initially dominant, its constant bound can be weakened to a t^L bound for the same L>=1. This argument does not assume deterministic permanence, positive initial coordinates, or a trajectory following one reaction path literally. Uniform coefficient upper/lower bounds supply all constants.

## 2. Shrinking-time fluid estimate

For Y_N(t)=X(N^(1-m)t)/N, each rescaled jump is O(1/N), total rescaled rate is O(N), and the drift differs uniformly from the polynomial ODE drift by O(1/N), including boundary/disabled-source grid points. The latter follows from the falling-factorial polynomial identity, not an interior-only approximation.

Quadratic variation and coordinatewise Doob give E sup_{u<=T}|M_N(u)|^2<=CT/N. Gronwall bounds the pathwise fluid error by a constant times sup|M_N|+T/N for T<=1. Squaring and applying Markov yields exactly the displayed probability bound C(T/N+T^2/N^2)/eta^2, uniformly over initial compositions.

With epsilon=1/[4(mL+1)], T=N^-epsilon and eta=(c/2)(T/2)^L, the first error exponent is kappa=1-epsilon(2L-1). The deterministic-error term has exponent 2-epsilon(2L-2), larger by 1+epsilon. Also kappa>epsilon because 2L epsilon<1. Since epsilon L<1, the resulting lower population c'NT^L tends to infinity and eventually exceeds every fixed factorial enabling threshold.

## 3. Actual killing hazard

Construct the conservative finite-shell chain without clearing, then kill when its integrated rate c(A)_m exceeds an independent unit exponential variable. This realizes the actual killed chain up to its killing event. On the good fluid event, the entire final half-interval has A>=c'NT^L, so (A)_m>=c''A^m for large N. After restoring the physical time scale, accumulated hazard is at least

    c N^(1-m) T N^m T^(mL)
      =cN^(1-epsilon(mL+1))=cN^(3/4).

Conditioning on the full unkilled path gives survival probability exp(-integrated hazard). Therefore the survival bound by O(N^-kappa)+exp(-cN^(3/4)) is correct without conditioning the fluid estimate on survival or assuming any equilibrium law.

The proposed restart using the previously established O(N^(1-m)) uniform mean is valid and noncircular: at the deterministic restart time the surviving state is on the same shell, and the bound applies to every possible composition. Since kappa>epsilon, the stated strict-power mean follows.

## 4. Stronger simplification: the previous mean is not needed

The survival estimate is uniform over starting compositions. For all large N it is <=1/2 at t_N=N^(1-m-epsilon). Strong Markov at multiples of t_N gives

    P_x(tau>j t_N)<=2^-j.

Consequently E_x tau<=2t_N directly, and for every t>=0,

    P_x(tau>t)<=2 exp[-(log 2)t/t_N].

This proves the same strict-power mean and a uniform exponential survival envelope on the improved scale without using the earlier mean theorem at all. Finite-shell nonexplosion is automatic. Only kappa>0 is needed for this alternative restart; the source's stronger inequality is nevertheless correct. This observation was sent to the author rather than silently changing the candidate's proof.

## 5. Catalyst and competing-event scope

For fixed B>=q, multiplying fast and clearing rates by (B)_q is an exact time change. Mean times divide by it, and the improved exponential survival rate is multiplied by it. An independent competing birth clock has intensity <=C(1+NB) before its first event, since N and B are still fixed. Integrated-hazard comparison therefore gives the stated probability bound <=C(1+NB)N^(1-m-epsilon)/(B)_q. For active N>=m and B>=q it has the displayed N^(2-m-epsilon)B^(1-q) form, capped by one if necessary.

The all-composition assertion is for sufficiently large N. Extension to finitely many small states is only over active states/components with clearing access. Inactive holes and B<q remain excluded; the formula cannot be applied to them merely because the algebraic right-hand side is finite.

## Scope

No output-composition distribution, low-B phase-return bias, or higher-dimensional global Foster matching is supplied by this estimate. The bridge is nevertheless genuine: it derives a uniform strict clearing power from deterministic short-time production plus an elementary finite-time martingale bound and the actual killing hazard. No fast mixing, stationary averaging, or arbitrary state-dependent coefficient regularity is assumed.

## Reviewed source hash
dae538e087b0f22e55c60ccc47c07655ed4518acd8e47d3ada2d18292520e1c6  chemical_joint_shell_20261030/STRICT_POWER_FAST_CLEARING_CANDIDATE.md
