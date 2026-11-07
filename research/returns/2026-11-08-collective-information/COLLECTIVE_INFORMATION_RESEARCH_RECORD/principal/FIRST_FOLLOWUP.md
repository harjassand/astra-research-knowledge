# Principal follow-up before cross-exchange

## A. New thermodynamic drives do not change the conditional projection in a count-energy system
If microscopic energy is U_t(k_1,...,k_B), all microstates with the same block counts have the same energy. Conditional law on each count shell is product uniform, independent of t, U and temperature. Thus projection P is constant even when the thermodynamic weights move. This is a real repair to the moving-projection obstacle, but relies on a special known physical structure; it is not a generic-fluid theorem.

## B. Arbitrary-source finite-horizon averaging without an exponential Gronwall
Let F be a fast Markov generator, P its conditional limiting projection, and ||e^(tF)(I-P)||_(infinity->infinity)<=M exp(-gamma t). Let B_t be slow Markov, ||B_t||<=L, and V_B its operator-norm variation on [0,T]. P has norm1 and Q<=2. For terminal retained f, ||f||<=1, backward coarse solution g_t obeys g'_t=-P B_t g_t, ||g_t||<=1. Set R=integral_0^infty e^(sF)Q ds, ||R||<=M/gamma, and h_t=R Q B_t g_t (Q redundant once R defined; count constants conservatively). Then Fh=-QB g. Dynkin for h_t yields
|E f(PX_T)-E f(Y_T)| <= (M/gamma)[4L+2 V_B+6 T L^2],
with inessential conservative coefficients to audit. Initial X arbitrary with known count-law; no global equilibrium source required. B_t variation, local energy evaluation, and actual preparation charged. It follows by h boundary <=2*(2M L/gamma); derivative <=(2M/gamma)(variation(B)+T L^2); B h <=2M T L^2/gamma. Thus coefficient6 is safe (possibly4 enough). No derivative of the unknown coarse g is solved microscopically; only the retained generator. This is standard stochastic averaging made explicit, not novelty.

At piecewise changes, h jumps add (2M/gamma)*sum||Delta B||. Allows extensive new field/drives, finite horizon T. To maintain epsilon for arbitrary preparations at growing B,T, fast mixing must scale at least with the given polynomial sufficient bound. This is NOT a fixed-noise/fixed-separation theorem uniform growing horizons.

## C. Locality may remove the total-volume factor from the reversible all-time bound
For disjoint blocks with uniform-shell conditionals and local mobilities, QBP f is a sum of bounded-overlap local fluctuation terms multiplying count increments. Conditional product independence makes disjoint local fluctuation covariances zero. If each block jump aggregate q_i has conditional Var(q_i)<=C m_i and mean>=c m_i in each available direction, then
||QBP f||² <=C' E_coarse(f),
where C' depends on overlap/locality and mobility bounds, not total number of blocks. Therefore relative coupling delta²<=C'/gamma, rather than Lambda/gamma~total microscopic volume/gamma. Proving this uniformly near count boundaries and for correlated neighboring mobilities is essential; cannot simply assert independence of summed terms. Need explicit finite-population Efron-Stein or bounded-differences variance with availability factors min(k,m-k).

This could give a size-uniform collective closure for macroscopic phase transitions under common-equilibrium kinetic drives, while keeping hidden mixing finite within blocks. General thermodynamic drives retain only the finite-horizon bound until a sharper time-dependent measure argument is proved.

## D. Acquired kinetic table and reuse
Microscopic flip rates factor as b(local neighbor pattern,control)*exp[-beta Delta U_t(k)/2]. The unknown bounded local b is unchanged by toggling the central spin. With degree/local-pattern size fixed, prepare those patterns while stirring paused and estimate elementary rates, then compute conditional means by hypergeometric finite-population probabilities. No new target experiment; new large N and block geometries require declared shared local mechanism. Exact size transfer is a model premise, not experimentally certifiable from finite small boxes. Control dependence must be supplied finite basis or regularity; no arbitrary unseen-drive extrapolation.

Count-field simulation is still potentially exponential in T for rare-event direct sampling. For a fixed number of blocks, full count-state matrix has polynomial dimension in microscopic volume and scaling/squaring allows polynomial log T arithmetic. For growing block count, Monte Carlo costs O(number of coarse jumps*T*epsilon^-2), not binary-time fast-forwarding. Kinetic all-time error and computational evaluation horizon are separate.
