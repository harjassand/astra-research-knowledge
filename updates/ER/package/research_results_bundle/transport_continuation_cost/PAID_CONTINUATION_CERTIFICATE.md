# Paid continuation cost for finite ring transport

## Result and boundary

The new manuscript's catastrophic extrapolation budget is avoidable at its stated example accuracy. The actual artificial-restart response has a positive spectral representation after shifting and squaring its argument. One legitimately acquired noisy scalar at restart rate r=d/8 suffices for the example's kappa accuracy 0.01, with node tolerance 1/425 rather than approximately 1.49e-10. This is an application of established positive-real/Herglotz machinery, not a claim to invent that machinery.

This does not make the full algorithm practical. Retaining the manuscript's time estimator still gives approximately 1.57e45 samples at the single node. An elementary, explicitly proved time-cutoff improvement removes another unnecessary inverse-precision factor and lowers this conservative sufficient budget to approximately 1.76e28 samples, each reaching times of order 3e9 in model units. Neither trajectory production nor the locality-based production simulator was run. These are sufficient upper bounds, not complexity lower bounds or measured runtime predictions.

The earlier impossibility of extracting full resets from physical onsite dephasing does not refute this manuscript: it deliberately adds a different generator and pays to remove it. This review accepts that distinction and concerns the paid scalar acquisition and continuation only. It is not a manuscript-wide audit, an implementation, a thermodynamic-limit result, or evidence of practical advantage.

## Source and actual continuation variable

Source: user-supplied manuscript research_note(20261012-141327).md, dated 12 October 2026. Relevant parts are Sections 3–8 and 10.4. The source manuscript is not reproduced in this bundle.

The source sets B=S+A, A*=-A, P equal to occupation dephasing, Q=I-P, and S_Q>=dI. Its artificial measurement changes B to B+rQ. The constrained space is K=ker(PAQ), with orthogonal projector Pi, and

    C = Pi(S_Q+QAQ)Pi on K,    j=Pi J,
    f(r) = <j,(C+rI)^(-1)j>/n,    ||j||^2/n <= a=t^2/2.

This exact quotient is essential. The calculation below varies artificial r and keeps physical d fixed. It does not replace onsite damping by a scalar damping on the original many-body space.

## The positivity that does and does not hold

### The response is not generally Stieltjes in r

For the four-site periodic model with hopping t=1, physical d=1 and H_diag=sum_i Z_i Z_(i+1), an exact calculation across all number sectors gives

    f(r) = 1/[4(r+1)] + (r+1)/[4((r+1)^2+16)].

The uncancelled poles -1+4i and -1-4i exclude a positive Stieltjes representation in r. This is a full infinite-temperature trace with interactions, not a dilute-particle replacement. Here the coefficient of each ZZ term is one; in the source's U(n_i-1/2)(n_(i+1)-1/2) convention it is U=4, V=0. The exact script is check_restart_response.py. This example does not claim failure of complete monotonicity, which is a weaker property than being Stieltjes.

### A shifted square variable really does have a positive measure

Put D=C-dI and w=r+d. D is accretive. The Hermitian-operator subspace has a real Hilbert-space form preserved by P, Q, A, S and Pi. Consequently the scalar

    F(w)=<j,(D+wI)^(-1)j>/n

is real for w>0. For Re w>0 its real part is nonnegative: setting v=(D+wI)^(-1)j gives

    Re <j,(D+wI)^(-1)j> = Re <v,(D+wI)v> >= 0.

Also wF(w) tends to M=||j||^2/n as w tends to positive infinity. The standard positive-real/Herglotz representation therefore has a finite positive measure on the imaginary-frequency axis, total mass M. Reality on positive w makes that measure even. Pairing frequencies and pushing forward under x=omega^2 gives

    F(w) = integral_[0,infinity) w/(w^2+x) mu(dx),
    mu >= 0,    mu([0,infinity))=M<=a.

Hence

    f(r)/(d+r) = integral mu(dx)/[(d+r)^2+x]

is Stieltjes as a function of z=(d+r)^2, on the principal-square-root domain. Nonuniform damping and noncommuting coherent/dissipative parts do not invalidate this statement. They generally replace a discrete oscillator measure by a measure with a continuous part. No spectral measure is computed, supplied as input, or fitted in the algorithm below.

For a direct spectral interpretation, replace D by D+eta I with eta>0. Its positive frequency density is pi^(-1) Re F_eta(i omega); it is even and integrates to M. Boundary atoms are retained when eta tends to zero. This is the usual positive-real representation, not a claim that D itself is self-adjoint.

Established references: Wilhelm Cauer, The Poisson integral for functions with positive real part, Bulletin of the AMS 38 (1932), 713–717, https://doi.org/10.1090/S0002-9904-1932-05510-0; Ivanenko et al., Quasi-Herglotz functions and convex optimization, Section 2.1, https://arxiv.org/abs/1812.08319. The transport-specific application and error accounting here are derived from the source's exact quotient.

## A one-node confidence-valid certificate

Let c=1+r/d>1 and y=x/d^2. The elementary kernel identity gives

    0 <= c f(r)-f(0) <= (a/d)(c-1)/(c+1).

Indeed the dimensionless kernel gap is

    c^2/(c^2+y)-1/(1+y)
      = (c^2-1)y/[(1+y)(c^2+y)],

whose maximum on y>=0 is (c-1)/(c+1), attained at y=c. A certificate of this maximum is

    (c-1)/(c+1) - gap
      = [(c-1)/(c+1)] (y-c)^2/[(1+y)(c^2+y)] >= 0.

Suppose a legitimately acquired node estimate f_hat has error at most delta on its confidence event. The interval

    [ c(f_hat-delta) - (a/d)(c-1)/(c+1),
      c(f_hat+delta) ]

contains f(0) on that same event. It can also be intersected with [0,a/d]. Its midpoint has deterministic bias at most

    (a/(2d))(c-1)/(c+1)

and statistical/numerical error amplification only c.

For the source's example a/d=1/4 and r=d/8, c=9/8. Therefore

    estimate = (9/8) f_hat - 1/136,
    error <= 1/136 + (9/8) delta.

Taking delta=1/425 makes this total exactly 1/100. No exact node oracle or cancellation of millions of weighted samples is used. All errors of the node acquisition method, including time bias and numerical law error, must fit inside delta.

### A sharper data-dependent interval and its scope

Write u=d f(r)/a. The measure has mass at most a; adding missing mass at y=infinity makes it a probability measure without changing the data. Convexity of v/[c-(c^2-1)v] and Jensen's inequality give the sharp one-node moment-class interval

    (a/d) u/[c-(c^2-1)u] <= f(0) <= (a/d)c u,
    0<=u<=1/c.

With noisy data, use u_low=max(0,d(f_hat-delta)/a) in the lower bound and u_high=min(1/c,d(f_hat+delta)/a) in the upper bound, provided their interval is nonempty. Its maximal width over admissible u is (a/d)(c-1)/(c+1), matching the uniform certificate.

The lower endpoint is attained by a single spectral atom; the upper endpoint is attained by a mixture at y=0 and y=infinity, or approached with an arbitrarily large finite second atom when exact full mass is required. At u=1/(c+1), the single atom is y=c, and the endpoint gap is precisely (a/d)(c-1)/(c+1). Thus positivity alone does not identify the endpoint exactly from one node. This sharpness concerns the positive-measure information class, not a claim that every extremal measure is realized by the finite spin family.

## Independent improvement without positivity

For completeness, interpolating the operator resolvent itself gives the exact identity

    C^(-1) - sum_j w_j(C+r_j I)^(-1)
      = [product_j r_j] C^(-1) product_j(C+r_j I)^(-1).

Accretivity therefore yields

    |f(0)-sum_j w_j f(r_j)| <= (a/d) product_j r_j/(d+r_j).

The three nodes d/8, 3d/16, d/4 have weights 6,-8,3, absolute sum 17 and bias at most 1/1140 when a/d=1/4. This already greatly improves the source's contour bound. It is separate from, and unnecessary for, the stronger one-node certificate at accuracy 0.01.

## Where the remaining sample cost comes from

Use the source's n=8, t=1, d=2, h_sum=18 and sigma=1/128. Thus a_H=36, s_*=8.5 and

    R = 2/sigma + [1+(s_*+a_H)/sigma]^2/d
      = 32456321/2 = 16228160.5.

The source sets lambda=delta/(8aR^2), uses exponential stopping, and has sample bound

    N >= 128 (n t^2/lambda)^2 delta^(-2) log[2(number of nodes)/failure].

When this branch of lambda is active, the dependence is

    N >= 8192 n^2 t^4 a^2 R^4 delta^(-4) log[...].

The extra delta^(-2) comes from making the time regularizer sufficiently small and then multiplying a bounded readout by lambda^(-1); ordinary sampling contributes the other delta^(-2). It is not a product-of-estimated-means issue. At failure probability 0.01, the reproduced sufficient budgets are:

- Original ten-node prescription: delta=1.48739e-10, lambda=1.41198e-25, log10 N per node=74.14975.
- Three-node exact resolvent bound with delta=0.01/(4*17): log10 N per node=50.09459.
- One-node positive-measure certificate: delta=1/425, lambda=2.23364e-18, log10 N=45.19628.

The last number is still prohibitive before charging the work within each trajectory.

## An elementary time estimator change with a full bound

The delta^(-4) dependence is not forced. A coarse hypocoercive estimate permits deterministic time truncation followed by uniform-time sampling.

On F-perp, decompose x=p+q and put T=QAP, D_r=S_Q+QAQ+rI. Then

    p'=T* q,    q'=-Tp-D_r q.

Use ||T||<=a_H, ||D_r||<=M_*=s_*+a_H, ||Tp||>=sigma||p|| and Re D_r>=dI. Define

    eta=d/[2a_H^2+M_*^2+2d a_H],
    V=||p||^2+||q||^2+2eta Re<Tp,q>.

The derivative of the cross term obeys

    d/dt [2 Re<Tp,q>]
      <= -||Tp||^2+(2a_H^2+M_*^2)||q||^2.

Since eta a_H<=1/2, V lies between one half and three halves of ||x||^2. Combining derivatives gives

    V' <= -eta sigma^2||p||^2-d||q||^2,
    ||exp(-B_r t)|| <= sqrt(3) exp(-beta t),
    beta=min(eta sigma^2,d)/3.

Consequently |C_(n,r)(t)|<=a sqrt(3) exp(-beta t), and the response tail after T_cut is at most a sqrt(3) exp(-beta T_cut)/beta. Choose

    T_cut=beta^(-1) log[4a sqrt(3)/(beta delta)].

The tail is delta/4. Draw U uniformly on [0,T_cut], use exactly the source's initial-state/sign/final-current readout, and return

    Z_cut=n t^2 T_cut sY.

Its mean is the truncated response and |Z_cut|<=n t^2 T_cut. Hoeffding with statistical allowance delta/4 requires

    N >= 32(n t^2 T_cut)^2 delta^(-2) log(2/failure).

The remaining delta/2 can pay numerical sampling-law error, rare-event aborts and rounding. Global-reset and Poisson caps work as in the source, now with fixed maximum total time T_cut. There is no conditional renormalization or unpaid rare-trajectory approximation. The per-trajectory numerical accuracy must be tightened in proportion to delta/(n t^2 T_cut). This changes only the time sampling and its proof, not the monitored physical model.

At the same n=8 constants and delta=1/425,

    eta = 0.0004240657,
    beta = 8.62764e-9,
    T_cut = 2.99767e9,
    log10 N = 28.24581 at 99% confidence.

Thus a justified estimator change removes the R^4 delta^(-4) construction and substitutes beta^(-2) delta^(-2) times logarithms. It is a substantial paid proof-budget reduction, still nowhere near a usable computation. No improved mixing theorem, conditional variance theorem, cheap coherent propagation or successful implementation is silently credited.

## Reproduction and stopping point

Run check_paid_bounds.py to reproduce the exact weights, one-node kernel certificate, rational budgets and cutoff budget. Run check_restart_response.py for the exact interacting four-site non-Stieltjes-in-r example. The optional check_general_restart.py is explicitly only a numerical nonuniform-damping diagnostic; its continued-sheet squared pole locations are not a counterexample to the principal-sheet Stieltjes representation and are not used in any proof.

Close this branch here. It establishes useful continuation and estimator improvements, but does not establish materially usable comparable-coupling many-body transport. Reopen only with a concrete lower-variance acquisition method, a quantitatively effective current-specific relaxation theorem, or an evaluated monitored solver whose complete cost makes the remaining bill plausible. Further tuning of the present upper-bound constants alone is not such a result.
