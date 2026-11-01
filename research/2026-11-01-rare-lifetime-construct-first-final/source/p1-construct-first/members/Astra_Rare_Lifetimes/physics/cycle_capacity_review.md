# Independent review of root's bounded-cycle rare-target robustness theorem

Reviewed 1 November 2026. This review reconstructs the algebra independently
and reports numerical diagnostics separately. It is not external review or
historical novelty clearance.

## Reviewed hypotheses

Let pi be uniform on a finite state space, and let

`L=sum_a lambda_a (I-P_a)`, `Lhat=sum_a lambdahat_a (I-P_a)`

be irreducible positive-sign Markov generators. Each known permutation P_a
is a disjoint union of cycles of length at most ell>=2. Rates are positive,
and `|lambdahat_a/lambda_a-1|<=epsilon<1`. The SAME permutations and SAME
stationary pi are indispensable. Real functions suffice; complex forms obey
the same estimates with real-part energies.

All statements extend to a supplied common pi invariant under each P_a,
because pi is constant on every individual permutation cycle.

## Fourier sector calculation

For `D_a=I-P_a`, define `E_a(f)=Re<f,D_a f>_pi`.
On a nonconstant Fourier mode of a length-m cycle, D_a has eigenvalue
`1-exp(i theta)` and E_a weight `1-cos theta`.

`|1-exp(i theta)|/(1-cos theta)=1/|sin(theta/2)|`.

Thus, with `K=csc(pi/ell)`, the exact cycle Fourier decomposition gives

`|<f,D_a g>|<=K sqrt(E_a(f) E_a(g))`.

Modes constant on a cycle contribute zero to both sides. A disjoint-cycle
direct sum and Cauchy–Schwarz retain K. Summing with nonnegative lambda_a
gives the global sector bound independent of the number of states, sites,
primitive terms, and rarity of a target.

Relative-rate uncertainty yields

`|<f,(Lhat-L)g>|<=epsilon K sqrt(E_L(f) E_L(g))`,

and `(1-epsilon)E_L <= E_Lhat <= (1+epsilon)E_L`.

## Mean hitting normalization and duality

Fix nonempty target B and A=B^c, assumed nonempty. Let
`u_B=0`, `L_A u_A=1_A`; then `u(x)=E_x tau_B`.
Put `b=pi(A)`, `M=E_{pi(.|A)} tau_B`, and

`C=1/<1_A,u>_pi=1/(bM)`, `h=1-Cu`.

Hence `h|B=1`, `pi(h)=0`, and `(Lh)|A=-C`. The adjoint problem gives
`u*_B=0`, `L*_A u*_A=1_A`. Its scalar average is identical because

`<1_A,L_A^-1 1_A>=<1_A,(L_A*)^-1 1_A>`.

Consequently `h*=1-Cu*` has the same C. Since L1=L*1=0,

`E_L(h)=E_L(h*)=C`.

For the fitted solution hhat, `E_Lhat(hhat)=Chat`. Directly using its
constant boundary and mean-zero normalization gives

`<h*,Lhat hhat>=Chat`, `<h*,L hhat>=C`.

Therefore the root's exact sensitivity identity is correct:

`Chat-C=<h*,(Lhat-L)hhat>`.

The form estimates imply

`|Chat-C|<=a sqrt(C Chat)`, `a=epsilon K/sqrt(1-epsilon)`.

Writing `r=sqrt(Chat/C)` gives `|r-r^-1|<=a`, equivalently

`|log(Chat/C)|<=2 asinh(a/2)`.

Because b is unchanged, `Mhat/M=C/Chat`; the same symmetric bounds follow.
No target mass or hitting time appears. There is no assumption of reversibility
or positive gap in this ROBUSTNESS step. Computational acquisition of M remains
a separate obligation.

## A slightly more general finite form

If `delta=max_a |log(lambdahat_a/lambda_a)|`, comparing both energies directly
gives

`|<f,(Lhat-L)g>|<=2 K sinh(delta/2) sqrt(E_L(f) E_Lhat(g))`.

Indeed `|lambdahat-lambda|<=2 sinh(delta/2) sqrt(lambda*lambdahat)`
termwise. Hence

`|log(Chat/C)|<=2 asinh(K sinh(delta/2))`.

For ell=2, K=1 and this reduces exactly to the familiar reversible bound
`|log(Chat/C)|<=delta`. Along a smooth log-rate path, differentiation gives
the weaker but transparent `|d log C/dt|<=K max_a|d log lambda_a/dt|`.

## Acquisition and adaptivity

The stated experiment must expose the MARKED clock for each known primitive,
including null events when the permutation fixes the current state. Counting
only visible state changes can confound lambda_a with occupation and cannot
silently substitute for this service.

For an exposed Poisson clock, the time T_m to m events satisfies
`lambda_a T_m ~ Gamma(m,1)`. The sample `lambdahat_a=m/T_m` has a simultaneous
relative-error guarantee after `m=ceil(7 epsilon^-2 log(2p/delta_fail))` events
per primitive for `0<epsilon<=1/2`, by the standard gamma Chernoff bound and
a union bound. The total event count is p*m; mean time per separately measured
primitive is m/lambda_a. Parallel acquisition has a different wall-clock bill.
No finite quota certifies that an unknown rate is zero. A known positive support
or a lower-rate promise is required for guaranteed completion.

One simultaneous rate event certifies EVERY nonempty proper target B, including
a target selected adaptively after data acquisition. This follows from the
uniform global form estimate; it does not require a union bound over targets.

## Prior art and exact constants

Nonreversible capacity/Poisson variational principles are established:
Gaudillière and Landim, arXiv:1111.2445 (published 2014).
Landim and Xu, ALEA 13 (2016), 725–751, §4, explicitly develops cycle
decomposition, sector conditions and capacity comparison:
https://alea.math.cnrs.fr/articles/v13/13-29.pdf .

Thus cycle-to-sector reasoning is conventional machinery. The exact Fourier
constant and the acquisition/hitting-sensitivity composition are reconstructed
here; no historical novelty claim is established.

One printed constant in the Landim–Xu PDF needs caution: Assertion4.B writes
`<Lf,g>^2<=2m E(f)E(g)` for a directed cycle of length m. For a constant-rate
uniform cycle, the exact Fourier ratio is `csc^2(pi/m)`, which exceeds 2m for
sufficiently large m (for example m=32). The screenshot was checked, so this
is not solely text extraction. The present proof does not rely on that printed
constant. No conclusion about the rest of their results is drawn here.

## Executed diagnostics

`cycle_capacity_audit.py` generated 72 irreducible random cycle families at
state counts 7,13,31,63 and maximum cycle lengths 3,4,6. It solved primal,
adjoint and perturbed hitting systems, verified the normalization energies
and sensitivity identity, and checked the arcsinh inequality. Maximum identity
error was 2.34e-15; the largest attained log ratio was 0.699 of its sufficient
bound. These are floating diagnostics, not interval-certified evidence or a
substitute for the proof above.

## Review result

PASS for the algebraic theorem under the stated shared-invariant bounded-cycle
model. Acquisition is valid only with its exposed known marked-clock interface.
Practical speedup, applicability to a less structured unknown source, and
historical novelty remain separate questions.

## A necessary structural restriction: long directed cycles

Relative rates and a known common invariant law are insufficient without a
size-independent sector restriction. On the n-cycle, let
`L0=2I-P-P^-1` and `Le=2I-(1+e)P-(1-e)P^-1`, where `0<e<1`.
Both have uniform stationary measure and the two primitive rates change by
relative e. Their primitive permutations each have cycle length n.

For a singleton target, the equilibrium-complement mean hitting time is

`M0=n(n+1)/12`,

and

`Me=n/(n-1) sum_{k=1}^{n-1} Re[1/(2-(1+e)e^{2pi i k/n}-(1-e)e^{-2pi i k/n})]`.

At fixed e and n growing, `Me~n/(4e)`, so `M0/Me~en/3` diverges.
This is the ordinary diffusive-to-ballistic drift effect, not a new physical
discovery. It demonstrates that the bounded-cycle/sector condition removes a
real source of inferential instability rather than merely improving a loose
sufficient proof.
