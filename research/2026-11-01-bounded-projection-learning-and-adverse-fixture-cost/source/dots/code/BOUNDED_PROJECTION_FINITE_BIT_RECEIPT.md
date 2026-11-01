# Finite-bit and exceptional-event closure for bounded projection

Independent co-constructor check of root `BOUNDED_PROJECTION_ACQUISITION.md`, frozen SHA256 `57eef80f88aa8229a2019b8f4884562a01beb40cfe0ff06744ac3abb0fca68dd`, 2026-11-01. This is not a historical-priority or physical-experiment receipt. No code for the new construction was executed and the existing inverse-Gram receiver was not changed.

## Mathematical checks

The corrected Duhamel identity, bounded-coefficient quadratic error bounds, repaired-Gram PSD claim, root zeta bound, prefix lower-confidence witness, and determinant progress all check. In particular the proof uses ridge leverage ONLY as a potential argument; neither inverse-Gram computation nor tiny determinant subtraction is required experimentally. The sharper projection recurrence with one sqrt(lambda) coverage term is valid by comparing P_K target directly with P_K actual-prefix.

The FW finite-step proposal is valid with the following explicit guards and accounting. Mean reports must be binary (or a specified finite alphabet), input epsilon/delta rational, and all source means clipped/checked in [-1,1]. Check Gbar PSD exactly before any FW call. Permanently latch failure on a violated guard, negative residual upper radicand, missing novel prefix after rejection, or iteration-cap violation. Never retry acquisition after the latch. Dictionary descriptors remain unique and length<=H, so m<=W=sum_(j=0)^H k^j even off-event.

## Exact FW cap with root constants

Use full gradient gap g=<grad q(c),c-s>, signed l1-ball vertex s, and B=m. Set

 C=16mB^2, delta=B^2 alpha, theta=delta/C=alpha/(16m).

The root's alpha ensures theta<1 and m alpha<1. Because every mean is in [-1,1], max_ij|Gbar_ij|<=1+m alpha<=2. Thus

 (s-c)^T Gbar (s-c)<=8B^2<=C/2.

Whenever g>delta, the exact quadratic decrease under c<-(1-theta)c+theta s is at least delta^2/(2C). On the whole coefficient ball the nonconstant objective range is at most

 R=8B^2,

since |c^T Gbar c|<=2B^2 and |2c^T Khat d|<=2B^2. A safe cap is

 T_m=ceil(2 C R/delta^2)+1.

The PSD guard makes the FW gap a valid upper bound on convex objective suboptimality. Under the bounded-mean guard, all of these facts hold OFF the statistical event as well. With b=nextpower2(m), alpha=lambda/[128(b+4)b^2] and m<=b<2m,

 delta=Theta(lambda/m), T_m=O(m^7 lambda^-2).

Constants can be computed as integers/rationals before starting a call. The cap is deliberately loose and NOT a recommendation to execute this many iterations in a fixture.

## Denominator and bit-work bound

Define B0 to include 1, the total encoded tolerance bitheight L0, H log2(k+1), log2(H+2), and confidence-log/input bookkeeping. Use one common sample count n_b per precision epoch, so every empirical mean is an integer divided by n_b, with O(B0) bits. This follows from the standard one-bit Hoeffding prescription and a finite job-confidence allocation; all exponents below are fixed constants.

Let D be the denominator of the fixed rational theta for this stage. Start every FW solve at zero (a valid feasible point). After t iterations each coefficient is on the D^t grid, bounded in magnitude by B. Its numerator/denominator bitheight is O(t log D+log B). In particular every coefficient is representable over D^T_m with O(T_m B0) bits. Different signed-vertex choices, including those caused by preceding forward/backward states, do not alter D or this bound. The target enters vertex selection and objective evaluation, NOT the step denominator.

Use common-denominator integer dot products. At a given stage all forward, backward and prefix-query solves have the same theta and cap, so targets introduce at most another constant multiple of T_m B0 bits, not an exponential recurrence in H. Rational matrix entries have O(B0) bits. Gradient and gap evaluation costs O(m^2) integer arithmetic operations on O(T_m B0) bits. With schoolbook multiplication/division, a conservative bound per QP is

 O(m^2 T_m^3 B0^2)=O(m^23 lambda^-6 B0^2).

Exact rational PSD guards can use fraction-free minors and have smaller W degree. Outward integer-square-root enclosures on the residual quadratic forms have O(T_m B0+log H) input bits and polynomial arithmetic of smaller degree. The same applies to corrected-output bilinear forms. Dictionary generation and chronological descriptor bookkeeping additionally pay their H factor.

There are O(H) forward/backward and prefix-query QPs per failed requested-word stage, and at most W stages. Accepted requests are deployment work and are not charged to the finite lifetime acquisition total. Therefore a conservative acquisition-only digital bound has W-degree at most24:

 poly(k,H) (W+1)^24 (1+lambda^-1)^6 poly(B0).

This is intentionally inefficient but explicit. It establishes polynomial bit work, not practical runtime. The source INFORMATION epsilon^-2 result does not imply epsilon^-2 digital runtime: this safe optimizer alone may cost epsilon^-6.

## Source jobs and expectation

At each fixed precision epoch, caching all canonical dictionary G/K/H pairs gives O(k b^2) unique jobs. Dictionary changes within that epoch add rows/columns without recalibrating old pairs. The at-most2H prefix scans per addition require O(Hm) scalar jobs each, giving O(HW^2) over all stages. Thus the finite worst-case number of jobs is O((k+H)(W+1)^2), with a harmless logarithmic epoch alternative also valid. Each job costs O(b^6 lambda^-2 B0) binary reports. Total shots are bounded by

 poly(k,H) (W+1)^8 lambda^-2 B0.

Actual stationary preparation, every discarded or failed report attempt, endpoint work and both chronological descriptors must also be charged; assume/parameterize an upper physical cost per attempt to turn episode counts into a physical-work theorem.

A simple finite confidence allocation may use W1=1+kW, E=ceil_log2(W)+1 and Nmax=E*(W1^2+1). Give each keyed mean failure probability beta/Nmax and choose n_b uniformly within its epoch. Computing W,W1,E,Nmax does not enumerate words. The union bound is valid for adaptively chosen descriptors under the conditional-unbiasedness premise. Taking

 beta=delta_stat/(W+1)^64

is more than sufficient for the displayed W-degree24: the bad-event expected acquisition contribution is polynomial in the remaining displayed parameters. Exponent32 would also suffice for these bounds, but64 provides slack without changing anything except a constant in logarithmic calibration cost. This proves polynomial expectation, NOT an absolute bad-event contribution <=delta_stat and NOT a bound on unlimited deployment traffic.

On the simultaneous good event replace the number of additions by the polynomial near-rank potential ceiling. For an explicit loose ceiling, the inequality

 (log(3/2)-1/16)m <= r log(1+m/(r lambda))+log(3/2)

is satisfied only for m=O(r log(1/lambda)); for example 1+ceil(64r log(8/lambda)) is safe for r>=1, lambda<=1/128. This is an analysis ceiling, not a supplied rank-dependent stopping rule.

## Status

No mathematical or finite-bit obstruction was found in the bounded-projection corrected-output construction. The particular execution recipe above is fully specified in principle but has not been implemented or empirically run. A practical implementation may improve the optimizer only with a replacement verified work/bit ledger; an emulator is not a physical calibration experiment. Historical novelty and a consequential application remain separate unresolved questions.

## Preferred rounded-FW refinement (supersedes the fallback digital exponent)

The root subsequently supplied an elementary improvement; this co-constructor has checked it independently. After every fixed FW step, round each coefficient TOWARD ZERO to a common dyadic grid h satisfying

 h<=delta^2/(24 C B m), C=16mB^2, theta=delta/C.

Keep the exact FW-gap stopping test. On the coefficient ball, entry bounds |Gbar_ij|<=2 and |Khat_ij|<=1 imply ||grad q||_infinity<=6B. Toward-zero rounding preserves the l1 constraint and changes coefficients by at most m h in l1. The whole segment remains in the ball, so rounding changes q by at most6Bm h<=delta^2/(4C). The unrounded step decreases q by at leastdelta^2/(2C). Every rounded step with gap>delta therefore still decreases q by at leastdelta^2/(4C).

A safe rounded cap is ceil(4 C R/delta^2)+1. With the root's even looser R=8mB^2 this is O(m^8 lambda^-2). Stop only after recomputing the exact FW gap at the rounded iterate; its <=delta condition implies the same true projection error used in the mathematical theorem. Rounding is not an additional unaccounted approximation: it is incorporated in reaching that certified gap.

All coefficients remain on a single fixed grid. Their bitheight is O(log B+log(1/h))=O(B0), rather than O(T B0). The fixed step, current coefficients, and common-denominator scalar means therefore permit exact per-step gradient/gap arithmetic with O(B0)-bit integers (up to harmless logarithms of m). Each QP costs conservatively O(m^10 lambda^-2 poly(B0)) digital work; across O(HW) failed-stage QPs the W degree is at most11. Guards, roots, descriptor processing and calibration are also polynomial with no worse inverse-lambda exponent beyond2. Beta=delta_stat/(W+1)^64 remains ample.

Thus BOTH source reports AND this safe elementary digital implementation have epsilon^-2 dependence up to rank/horizon polynomial factors and logarithms. This supersedes the epsilon^-6 digital limitation of the unrounded fallback above. It does not make the constants practical, nor is this a full receiver implementation.

`rounded_fw_stress.py` verifies the rounded-step feasibility, fixed-grid invariant and exact per-step decrease on a rational nearly singular two-variable convex problem. It converged in927 iterations with maximum coefficient bitheight37. This is a synthetic optimizer diagnostic, not physical acquisition. `bounded_projection_stress.py` independently tests exact corrected-return certificates using small active-face QP solves and39 validated UNSAMPLED scalar means, including a physical reachable Gram determinant below alpha^2 and a far-prefix lower witness. The enumerative diagnostic solver is not offered as a polynomial general solver. Outputs are retained in the correspondingly named STRESS_OUTPUT files.
