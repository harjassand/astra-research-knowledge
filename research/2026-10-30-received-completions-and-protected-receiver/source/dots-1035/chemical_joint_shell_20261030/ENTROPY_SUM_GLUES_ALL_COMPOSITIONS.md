# Entropy-separated sum gluing: an actual two-population corner certificate

Status: child adversarial review passed; see INDEPENDENT_ENTROPY_SUM_AUDIT.md. No whole-project independent review or global recurrence claim. The corner is truncated in B and is NOT assumed invariant. Outer B-feedback remains open.

## Ingredients already earned
Use the coupled hard network, N=A+C, and a consecutive B-corner J={0,...,K}, K>=3, with its complete-linkage halo H. Choose a rational alpha in (0,1/2), also bulk-admissible if bulk compatibility is wanted.

1. The explicit global F from EXACT_LOW_PHASE_FORCING_CLOSURE.md has LF<0 at every B<4 and, for large N, whenever A/N<=epsilon0 or A/N>=1−epsilon0, for some fixed epsilon0 in (0,1/2). On finite B sets its negative margins are at least c N^(−D)F. Its positive drift elsewhere is at most C N^D F.
2. The robust phase theorem gives a common certificate depending only on (N,B), valid on A/N>=epsilon1, for any fixed 0<epsilon1<epsilon0, at every B in J. It is defined on the whole halo H.

The second theorem also permits a fixed exponential radial factor exp(−d r). Indeed replace each inflated tilt by

    r^(alpha delta) exp(−d delta) 2^|delta|.

The first-down proof is unchanged: exp(−d delta) is a fixed edge constant, while the strict polynomial exponent gap remains. The policy-maximization proof still gives an eventually fixed positive rational-Puiseux v_d(r). Thus

    W(N,B)=exp(−d r) Gamma(r+1)^alpha v_(d,B)(r),
    r=N+beta_B,

has LW<=−exp(−d r)Gamma(r+1)^alpha throughout A/N>=epsilon1, B in J, for large N. Invisible fast composition changes still contribute exactly zero. No derivatives of the actual coefficient choices are used.

## Explicit selection by entropy, with no commutator
Let H(t)=−t log t−(1−t)log(1−t), with endpoint values0. Choose

    alpha H(epsilon1) < d < alpha H(epsilon0).

On every fixed finite B set, the exact low-phase recursion and positive rational-Puiseux asymptotics give uniformly over ALL compositions A+C=N:

    log F = alpha log(A! C!) + O(log(N+1)),
    log W = alpha log(N!) −d N + O(log(N+1)).

The uniform factorial/binomial estimate therefore yields

    log(W/F)=N[alpha H(A/N)−d]+O(log(N+1)).

No selector is differentiated. Define the SUM

    U=F+W

on the halo, extending W positively elsewhere in any manner if a globally defined function is desired. Only halo values enter LU at states of J.

- If A/N<epsilon1, F has negative drift, while W/F is exponentially small. The polynomial bound on |LW| therefore makes LF+LW negative.
- If epsilon1<=A/N<=epsilon0, both drifts are negative.
- If epsilon0<=A/N<=1−epsilon0, W has negative drift and W/F is exponentially large. Its polynomial negative margin dominates any positive LF.
- If A/N>=1−epsilon0, both drifts are negative.

The needed global polynomial bound |LW|<=C N^D W on J holds even outside its comparability cone: actual connector rates are polynomially bounded, fixed count/phase shifts of W have polynomial ratios, and all fast transitions contribute zero. Similarly |LF|<=C N^D F follows directly from the finite recursion and bounded reaction jumps.

Consequently there are c>0,D<infinity,N0 such that the ACTUAL physical generator satisfies

    L U <= −c N^(−D) U

for EVERY composition A+C=N>=N0 and EVERY B in J. U is normlike on this two-unbounded-population strip. This is an earned joint selection/coupling mechanism, not a frozen background, supplied Lyapunov barrier, or finite-fixture claim.

## Actual stopped-corner consequence
Let tau be the first physical exit from J. Until tau, all A/C composition motion, phase switching, and connector feedback remain present. The normlike drift proves nonexplosion before tau and finite expected hitting time of a finite head or the exit.

From every finite-head state an enabled finite immigration path exits J. All rates on these finitely many paths are finite. If an attempted finite immigration path fails at a wrong jump, its landing state belongs to a finite set because there are finitely many channels and bounded jumps. The drift bounds its expected return-to-head-or-exit uniformly. Thus repeated attempts have a uniform positive success probability and finite mean duration, giving E_x tau<infinity without first assuming finite-head occupation. No recurrence of the full network is imported. Applying stopped Dynkin and Fatou, and bounding finite-head occupation through the first head visit, gives

    E_x U(X_tau) <= U(x)+C,
    E_x tau <= C'(U(x)+1).

The same drift controls occupation integrals of c N^(−D)U outside the head. Thus an actual two-population Dirichlet/Poisson corner transfer is earned for boundary data dominated by U. This goes beyond the earlier one-unbounded-coordinate finite-phase corner transfer.

## What is NOT closed
The function U and its exit law are controlled inside J, but exit values feed into the generator outside J. No inequality absorbing that OUTER B-halo feedback has been proved. Extending W arbitrarily beyond the halo does not fix this. General recurrence, a global all-state Foster function, and an efficient construction are not claimed.

The standard policy/positive-matrix step and the entropy comparison are not presented as novelty-cleared. The scientific gain is the explicitly earned coupling of those steps with the chemical boundary construction, at exactly the stated scope.
