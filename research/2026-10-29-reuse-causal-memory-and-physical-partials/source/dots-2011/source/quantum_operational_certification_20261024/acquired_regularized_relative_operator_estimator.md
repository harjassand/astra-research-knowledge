# Acquired regularized relative operator estimation from ordinary state copies

27 October 2026. Independent auditor construction at root request; local post-cutoff, separate peer receipt requested. This is a state-acquisition theorem, not yet a decoder theorem or a claim about unknown reset backgrounds.

Let rho be any d-dimensional density matrix. Given copies of rho, supplied0<t<=1,0<epsilon<=1/8 and0<beta<1, one can acquire a classical Hermitian estimate rhohat (or declare abort) such that, with probability at least1-beta, there is no abort and

    -epsilon(rho+tI) <= rhohat-rho <= epsilon(rho+tI).

No spectral gap, known eigenbasis, known background, or access to an unknown whitening operation is assumed. All whitening below is classical matrix processing of observed estimators, not a transformation of unknown quantum copies. The deterministic copy cap is

    N <= (2052 d/t) ceil[100 epsilon^-2 log(2d(J+1)/beta)],

where J+1<=ceil(log2(1/t))+2 is the number of stages. Constants are deliberately loose. The estimate is not asserted PSD or trace one.

## Primary input and weighted variance

Use the covariant unbiased debiased Keyl estimator Y on n fresh copies. Primary source: Pelecanos--Spilecki--Wright, Theorems1.3 and1.4, https://people.eecs.berkeley.edu/~jswright/papers/debiased-keyl.pdf (independently opened27 October2026). Its second-moment formula has the main covariance terms and subtracts a positive combination of (P tensor P)SWAP with P>=0; E ell<=d.

For ANY fixed W>=0, contraction of that formula gives

    E[(Y-rho) W (Y-rho)]
      <= [rho TrW + I Tr(rho W) - rho W rho]/n
         + d TrW I/n^2
      <= [rho TrW + I Tr(rho W)]/n + d TrW I/n^2.       (1)

Indeed, each subtracted term contracts to P Tr(PW)>=0. This proves the weighted matrix inequality directly; no entrywise-to-operator inference or diagonal phase assumption is required.

For H=rho+tI and W=H^-1, sandwiching(1) by H^-1/2 gives

    E[(H^-1/2(Y-rho)H^-1/2)^2]
       <= [2d/(nt)+d^2/(n^2t^2)]I =v I.              (2)

Here rho<=H, TrH^-1<=d/t and Tr(rho H^-1)<=d. If a known positive G satisfies G>=aH, then positivity of covariance contraction and congruence yield

    E[(G^-1/2(Y-rho)G^-1/2)^2] <= a^-2 v I.          (3)

This step does not commute G with rho.

## One acquired stage

Suppose the previous scale tprev satisfies t<=tprev<=2t and its successful estimate obeys relative error at most1/8 with respect to rho+tprev I. Set

    G=rhohat_prev+tI.

Then

    (3/4)H <= G <= (5/4)H.                          (4)

Abort deterministically if G fails (t/2)I<=G<=4I. Successful preceding histories never abort (t<=1 and rho<=I).

Acquire k independent batches of n0=ceil(512d/t) copies. Form the classical Hermitian matrices Z=G^-1/2 Y G^-1/2. Conditional on the preceding classical history, their mean is R=G^-1/2 rho G^-1/2, with norm<=4/3. Equations(2),(3) give variance<= (16/9)(2/512+1/512^2)I. Consequently E Z^2<=2I.

Let eta=4 delta/5 for the desired stage accuracy0<delta<=1/8. Spectrally clip each Z to[-B,B], B=8/eta, and average the clipped matrices to Rhat. Pointwise |Z-clip_B Z|<=Z^2/B implies bias norm<=eta/4. Also E(clip_B Z)^2<=E Z^2<=2I; its centered variance is at most2I and its centered norm is at most2B=16/eta.

The standard two-sided Hermitian matrix Bernstein inequality, with deviation3eta/4, gives failure probability at most

    2d exp[-3 k eta^2/64].

Thus k=ceil[64 eta^-2 log(2d/beta_stage)] suffices (with slack). Dewhiten classically:

    rhohat=G^1/2 Rhat G^1/2.

On success, -eta G<=rhohat-rho<=eta G, and(4) gives the claimed stage error delta H. Clipping and dewhitening are functions of known classical matrices. No physical whitening oracle or source-dependent measurement is used: every Y batch is the ordinary state-tomography measurement.

## Initialization, schedule, cap and conditional failure

Use scales1,1/2,1/4,... until the last dyadic scale above t, then append t if needed. Ratios between consecutive scales are at most2. At the first stage G=I; because H=rho+I lies between I and2I, equation(3) with a=1/2 applies. R=rho has norm<=1, so n0=ceil512d also gives E Z^2<=2I. The same clipping proof applies. Since G<=H, choosing eta=4delta/5 is conservative at initialization.

All nonfinal stages use delta=1/8; the final stage uses delta=epsilon. Allocate beta_stage=beta/(J+1). Conditional on any successful past, the current batches remain independent ordinary measurements on fresh copies, so the stage bound applies. A union bound over first failures controls both bad estimates and any ensuing abort by beta. No assumption is made on behavior after an earlier failure; the copy cap holds on every path.

The reciprocal scales sum to at most4/t. Each n0<=513d/t_stage. Since eta=4delta/5 and delta>=epsilon, all batch counts are bounded by ceil[100 epsilon^-2 log(2d(J+1)/beta)]. This proves the stated deterministic cap. Singular rho is harmless because supplied regularization t>0 ensures all comparison matrices are invertible.

## Scope

This construction supplies an acquired regularized Loewner-relative estimate with O((d/t)epsilon^-2 polylog(d/(t beta))) copies and classical output. It does not by itself supply a CPTP Choi estimate, a relative-error recovery instrument, a model-free reset decomposition, or a positive background estimator. Those require separately paid source/decoding bridges. No historical novelty is claimed.
