# Root join: finite sampled certificates plus stationary count intensity

Status: NEW conditional construction, independent review pending. The actual stationary count identity and the concrete global odd current/trial are separate proof obligations. No continuous-record TV claim is made.

Let a stationary reversible Markov process preserve pi. Let A and B be disjoint basins, S their complement, s=pi(S). Let L_t in{+1,-1} be its actual stationary last-visited-basin label, with nonexplosive completed-transition count N_t. Assume an actual stationary augmentation exists. Let psi be a mean-zero scalar trial in[-1,1], +1 on A and -1 on B; choose the measurable sign Z=sign(psi), with a fixed convention at zero. Then |Z-psi|<=1_S, and L differs from Z only in S.

Receive a rate k>0, epsilon>=0, Npsi=||psi||_2^2<=1, and both

 <psi,P_t psi>/Npsi <= exp(-kt)+epsilon,
 ||P_t psi-exp(-kt)psi||_2 <= v(epsilon)*sqrt(Npsi)

for every deterministic t. A sufficient reversible spectral choice is v=sqrt(epsilon). The separately accepted sharp storage theorem, when its energy-solution premises are received, allows v=0.5sqrt(epsilon(1+epsilon))+epsilon/EulerNumber.

Assume additionally the stationary completed-transition intensity satisfies

 E_pi N_t <= (1-s) k t/2.

This is the proposed capacity/current join: for symmetric basins of mass M and total unnormalized mass Ztot=2M+S_mass, actual intensity2cap/Ztot and trial upper cap<=C0 with k=2C0/M yield precisely that inequality. It is NOT inferred from the one-time CDF.

## Per-bin cluster bound

For a uniform deterministic mesh Delta and x=k Delta/2, r=exp(-2x), stationarity and |Z-psi|<=1_S imply

 E Z_0 Z_Delta <= Npsi(r+epsilon)+2s <= r+epsilon+2s.

Hence the odd-flip probability of L satisfies

 P_pi(L_0 != L_Delta) >= (1-r-epsilon)/2 -3s.

For every nonnegative integer N, 1_{N>=2} <=(N-1_{N odd})/2. Since every full-basin transition flips L, the assumed intensity and 1-exp(-2x)>=2x-2x^2 give

 P_pi(N_Delta>=2) <= (x^2+epsilon/2+3s)/2.

No independence of crossings is assumed.

## Initial law and full finite-horizon coupling

Let the actual initial law on the AUGMENTED state have density <=R relative to its stationary augmented law. This holds for the stationary process conditioned on X0 in A, because L0=+1 there, with R=1/pi(A). For symmetric basins R=2/(1-s). Such domination applies to every full future-path event, and is not a mixing or reset assumption.

Observe n bins. For the actual Z grid, the independently reviewed vector-to-path theorem gives a coupling to the sampled symmetric two-state chain of correlation rate k, flip rate k/2, and the SAME initial Z law, with failure at most

 delta_grid=min(1,sqrt[R*n*d^2/(2(1-r^2))]),
 d=sqrt(Npsi)*v(epsilon)+(1+r)*sqrt(s).

For the conditional-A initialization the initial L and Z agree. Their entire grids differ with probability <=R*n*s. (For a general augmented initial law, use R*(n+1)*s and receive matching initial comparison labels.)

The actual hysteretic path has a bin with >=2 flips with probability <=R*n*(x^2+epsilon/2+3s)/2. A genuine continuous-time comparison chain of flip rate k/2 has such a bin with probability <=n*x^2/2 by its Poisson jump count.

Couple the grids maximally, then complete each path using its actual conditional path law. On the complement of those failures, both hysteretic paths have exactly the same number of flips, the same order and directions, and each corresponding pair of jump times lies in the same mesh bin, hence differs by at most Delta. Therefore a sufficient total failure bound is

 delta_grid +R*n*s +R*n*(x^2+epsilon/2+3s)/2 +n*x^2/2,

capped at1. Endpoint conventions and any deterministic-time jump atoms must be handled by the actual process; ordinary nondegenerate diffusion first-hit laws and the comparison CTMC have no such atoms for this initialization.

This is a jump-matching/time-error coupling on a finite horizon, NOT total variation of exact real-valued jump-time laws. For scaled horizon nx bounded, epsilon->0 and s=O(epsilon), taking x of order epsilon^(1/4) gives vanishing failure and vanishing scaled timing error. This does not itself control unbounded mean passage times or arbitrary feedback/continuous observation services. It does not replace the raw-sign record by a cadlag process: L is the distinct hysteretic observable.

## Computational and physical burdens

A consumer must receive all inequalities including intensity, actual stationary augmentation, initial density domination, scalar numerical enclosures, and a finite horizon/mesh. No rare trajectory must be simulated merely to evaluate these analytical bounds, but raw-model acquisition, proof construction and query complexity are fully charged. Simple finite-state event accumulators cost O(nJ) arithmetic operations plus precision cost; arbitrary predicates or bounded real accumulators are not promised cheap. Actual preparation and observation are separate physical obligations.
