# Independent computable smoothed-gradient and global-affinity specification audit

**PASS after two explicit input/branch clarifications, now incorporated by the author:** a is dyadic rational, and the gap test is rechecked after tightening oracle/evaluation intervals. This is an algorithmic specification, not an executed optimization or a new evaluated affinity gain.

Reviewed `COMPUTABLE_SMOOTHED_GRADIENT_AND_GLOBAL_OBJECTIVE.md` together with the audited annular density evaluator, invariant smoothing bridge, nested lower families and global positive-accuracy reward oracle.

## Truncated actual target and legitimate reference

A finite nested rational policy has rational proper internal transitions. Its occupation vector and absorbing Brownian weights are rational, so its law is a finite computable Brownian mixture. Scaling followed by Brownian completion preserves this class by `omega_x K_a=omega_(ax)`.

The central two-sheet phase box has exact source mass p=(1-2/M)^2. At every elliptope vertex V its height is at least `2-|u|-|v|>=2(1-cos(pi/M))>=6/M^2`, so the previously audited Brownian lower bound applies with r0=1/M^2. The conservative rational floor `c_M=9^(-864M^2)` is valid on this box. It is not claimed near the omitted singular vertices.

The target truncation error follows from the square-root-density distance: its squared value is `2-2sqrt(p)`. Thus the displayed uniform affinity error is correct. Using omega0 as reference avoids the earlier unsupported extension of a finite-Brownian-mixture evaluator to non-Brownian vertex reference components.

## Effective gradient receiving

On the central set the actual mixture density has the floor c=theta*c_M. The formula `g=1_A/(sqrt(p)*sqrt(r))` has the correct normalization; physical smoothing occurs before any atomic competitor enters the derivative. The fixed-a variation kernel estimate gives the stated continuous Lipschitz gradient G=K_a g.

A certified q<=r with missing mass e is upgraded on A to qbar=max(q,c)<=r. The inverse-square-root derivative on [c,infinity) gives exactly the stated L1 error `e/(2sqrt(p)c^(3/2))`. Multiplication by the actual receiving ceiling C_a gives a uniform pointwise evaluation error after K_a.

The simple function gbar can be evaluated by continuous phase cutoffs with all transition strips paid using K_a<=C_a mu. WOS then supplies its true Brownian expectation. This is an actual computable point-evaluation interface, not a claim that arbitrary measurable density versions are automatically computable rewards. The indicator's boundary is mu-null and K_a is AC, so versions do not change G.

Computing the current expectation of continuous G under a finite Brownian mixture uses the already established WOS evaluator and computable mixture weights. Dyadic rational a ensures the scaled starts, constants and rational upper curvature/step choices have the required effective input representation.

## Curvature and finite stopping/gain dichotomy

The second derivative has the correct factor `(1-theta)^2/[4sqrt(p)]`; the receiving difference is at most C_a and the target density denominator is at least c^(3/2). The proposed rational H is a conservative upper bound because p,c<=1.

For s=(1-theta)/2, let [I_low,I_high] enclose the current G expectation and let A be the paid response lower bound, B the verified global upper bound. Then

`gap_up=s(B-I_low)`, `D_low=s(A-I_high)`,
`gap_up-D_low=s[(B-A)+(I_high-I_low)]`.

This identity makes the branch logic precise. After reducing the two interval errors below the prescribed derivative-unit budget, RECHECK whether gap_up is below epsilon. If it is, stop with a genuine global objective-gap certificate. If the refined test still fails, D_low>epsilon/2. A coarse failed test alone would not justify that assertion; the author corrected this explicitly.

For rational alpha=min(1,D_low/H), the curvature estimate gives improvement at least `min(epsilon/4,epsilon^2/(8H))`. Since the affinity objective lies in [0,1], infinitely many non-stopping steps are impossible. All competitors returned by the paid lower oracle and all convex updates remain finite Brownian mixtures, so the evaluator's input class is preserved.

For objective evaluation the missing-density-mass bound has no missing factor of p: Cauchy-Schwarz on A cancels its normalization, giving error at most sqrt(e). Certified numerical lower/upper integrals must include their evaluation errors as usual.

## Unrestricted positive-accuracy objective specification

Affinity-optimum density of the nested finite Brownian-mixture family was proved by the invariant smoothing bridge, including singular maximizers. Evaluating an exhaustive sequence of rational candidate policies therefore gives increasing valid lower bounds for the unrestricted optimum.

The audited dual formula supplies upper candidates `(V_f(0)+E_mu 1/f)/2`. Strictly positive rational polynomials are uniformly dense among positive continuous boundary rewards; their positive minimum preserves continuity of the reciprocal term, and V_f is 1-Lipschitz in uniform reward norm. Positivity can be certified exactly on the compact semialgebraic boundary, reciprocal source integration is effective in the actual phase coordinates, and the global reward oracle supplies a verified upper majorant for V_f. Hence actual upper candidates can approach the same optimum.

Dovetailing these searches terminates for every positive requested interval width. It does not require an effective source-TV modulus. Nor does it decide exact equality of the optimum to one. If a verified dual upper were strictly below one, `f+1/f>=2` would indeed yield a true source reward gap; no such evaluated gap is supplied here.

The alternative fixed-parameter route converges as M increases, a increases to one, and theta decreases to zero, but its parameter limits alone have no numerical stopping scale. The two-sided global search is the stated positive-accuracy stopping mechanism.

## Scope

The earlier density/gradient input-model gap is closed for this truncated-target Brownian-reference construction. The result is an end-to-end existence/specification theorem for certified positive-accuracy affinity optimization. No optimizer implementation, near-unit affinity value, subunit global upper, source membership proof, or Morrey conclusion has been obtained by these arguments alone.
