# Coherence-only identification of a nonunitary recovery: next bridge

Author working construction, 2026-10-28; **not yet independently reviewed**. Separate from the general-face receipt. No superiority over an equally informed conventional recovery learner is claimed.

## Structured physical family and the bottleneck removed

Let V=[u_0,u_1] be an unknown receiver isometry from a logical qubit to dimension d. Put F=I−VV†. For s in (0,1], p=1−s², and any density matrix tau supported in F, define

    N(rho) = V diag(1,s) rho diag(1,s) V† + p rho_11 tau.

The physical recovery

    D_V(X)=V†XV + Tr(FX)|1><1|

is independent of tau. It has Kraus V† and |1><f_a| for an orthonormal flag basis. For full-rank tau on F, the general-face fixture extends with rank d−1, sigma²=1/2, G=10d and strict dual gap min(2s,s(1+s),1+s,p lambda_min(tau)). Thus a generic all-CPTP unique-oracle certificate becomes poorly conditioned as the flag distribution develops small eigenvalues. Yet the physical recovery itself does not depend on those eigenvalues. A source promise enabling acquisition of the coherent subspace can remove this bottleneck without learning tau. Rank-deficient tau creates nonunique arbitrary off-support extensions, so the general unique-oracle theorem must not be applied there.

## Acquired sufficient statistic

The non-Hermitian coherence

    C=N(|0><1|)=s |u_0><u_1|

contains V up to one physically irrelevant common phase. It is acquired from ordinary logical preparations:

    C=(rho_+x−rho_−x+i rho_+y−i rho_−y)/2.

In each use choose one of these four preparations uniformly and privately. Perform a receiver rank-one projective 2-design POVM (e.g. the uniform union of a complete set of mutually unbiased bases where such a set is supplied). For observed normalized vector psi use Y=(d+1)|psi><psi|−I. Its conditional moments are

    E Y=rho,    E Y²=(d−1)rho+dI,    ||Y||op<=d.

With w=1,−1,i,−i for the four input choices, Z=2wY has conditional mean C. Hence ||Z||op<=2d and both E ZZ† and E Z†Z are bounded by 8d I. A non-Hermitian matrix concentration argument applied through Hermitian dilation should yield operator error of order sqrt(d log(d/delta)/T)+d log(d/delta)/T. **The full tail constants and retained-memory martingale version are not yet proved in this note.** This variance calculation is not itself a completed finite-sample guarantee. A dense 2-design can also impose expensive basis-control costs: input/output measurement synthesis, random-design sampling and calibrated readout must be counted. The mere mathematical existence of a design does not supply a scalable apparatus.

For conditional drift with fixed V, arbitrary conditional s_t and tau_t, the predictable mean coherence is s_bar |u_0><u_1|. Thus orientation is preserved, provided the current probe is initially independent of source memory and its private choice has no side channel. An appropriate simultaneous martingale confidence sequence remains an explicit obligation.

## Constructive recovery and operation transfer

From an operator-norm approximation C_hat, take its leading coupled left/right singular vectors a,b. Form W=[a,b] and, if W†W has a certified positive floor, polar-normalize V_hat=W(W†W)^(-1/2). Coupled singular vectors preserve the relative logical phase; independent phase choices would destroy this information. A rank-one singular-gap perturbation bound followed by polar continuity is expected to give ||V_hat−V e^{i theta}||op=O(||C_hat−C||op/s_bar). **A sharp explicit constant and finite guards remain to be derived/reviewed.** An externally supplied lower bound on s_bar is not needed for abstention-based inference if a confidence-adjusted observed singular gap is used, but finite completion needs s_bar bounded away from zero.

The transfer from a certified isometry error is elementary and already checked algebraically. For isometries V,W with aligned common phase and ||V−W||op<=epsilon, the two compressed channels differ in diamond norm by at most 2epsilon, and

    ||VV†−WW†||op<=2epsilon.

The reset difference is the linear functional X -> Tr((WW†−VV†)X)|1><1|, whose diamond norm equals the operator norm of its Hermitian coefficient. Therefore

    (1/2)||D_V−D_W||diamond <= 2epsilon.

This is independent of flag rank and lambda_min(tau). It establishes only operation substitution after isometry-error certification. Fidelity under the physical native family remains (1+s)/2, not generally near one; no capacity or protected-storage theorem follows. A conventional learner given the same family and probe information can use this same sufficient statistic, so no comparative advantage is established.

## Next hard obligations

1. Prove finite-sample non-Hermitian matrix martingale concentration with explicit constants for the actual 2-design acquisition and adaptive stopping.
2. Prove explicit singular-vector/polar guards and validate complex phase conventions against adversarial perturbations.
3. Realize an output design with accounted control costs, and compare its resources against an equally informed conventional low-rank process estimator.
4. Find a scientifically valuable broader native family whose recovery is identified by such accessible coherence statistics without a small flag-eigenvalue penalty.
