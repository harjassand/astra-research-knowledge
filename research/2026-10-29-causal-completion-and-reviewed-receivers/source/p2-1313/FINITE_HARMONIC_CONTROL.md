# Finite harmonic controls with a global comparison

Root construction, 29 October 2026. The companion conventional author supplied the monotone polynomial/Fourier formulas independently. Root introduced the nearby exact smooth extension and its use as a global bounded perturbation of the causal-completion model. Reviews remain separately scoped.

## 1. Why changing the comparison helps

The ideal smooth periodic plateau in [CAUSAL_BOUNDARY_COMPLETION.md](CAUSAL_BOUNDARY_COMPLETION.md) is not a finite trigonometric polynomial. An analytic finite sum cannot equal a nonconstant plateau on an open interval. Using its small on-band error as if it also controlled arbitrarily many derivatives would be invalid.

Instead construct a finite physical Hamiltonian and a nearby smooth exact reference. Their difference is bounded in **global** operator norm. Its effect can be charged once along the full dynamics, with the unbounded background noise retained. The derivative constants of the physical approximation do not enter the finite polynomial remainder.

## 2. Explicit finite control

For integer r>=0 set

    C_r=(2r+1) binom(2r,r)/4^r,
    P_r(s)=C_r integral_0^s (1-t^2)^r dt,
    g_r(x)=P_r(cos(Lx)),   L=sqrt(pi).                       (1)

P_r is odd, monotone, bounded by one on [-1,1], and P_r(1)=1. Its degree is 2r+1. Differentiating g_r gives -L C_r sin(Lx)^(2r+1), whose finite sine series integrates to

    g_r(x)=sum_(j=0)^r A_(r,j)cos((2j+1)Lx),
    A_(r,j)=(-1)^j C_r binom(2r+1,r-j)/(4^r(2j+1)).        (2)

For 0<c<1,

    sup_(|s|>=c)|P_r(s)-sign(s)|
       <= C_r(1-c^2)^(r+1)/(2c(r+1))
       <= c^(-1)(1-c^2)^(r+1).                            (3)

The first bound follows from

    integral_c^1(1-t^2)^r dt
       <= c^(-1)integral_c^1 t(1-t^2)^r dt.

The second uses C_r<=2r+1. No floating approximation is needed for the coefficients.

## 3. Nearby exact extension

Fix protected support a<a_0<a_1<L/2 and c_i=cos(La_i). Choose smooth even zeta(s) in [0,1], zero on |s|<=c_1, one on |s|>=c_0. Define

    f_r(x)=g_r(x)+zeta(cos Lx)[sign(cos Lx)-g_r(x)].         (4)

Zeta vanishes in a neighborhood of the sign discontinuities, so f_r is smooth. Convex interpolation proves |f_r|<=1. Oddness of P_r and evenness of zeta prove f_r(x+L)=-f_r(x). It is exactly (-1)^m for |x-mL|<=a_0. The only place f_r differs from g_r has |cos Lx|>=c_1; hence

    ||f_r-g_r||_infinity <= delta_r,
    delta_r=c_1^(-1)(1-c_1^2)^(r+1).                       (5)

For a_1=L/4, delta_r<=sqrt(2)2^(-r-1). The smooth comparison is allowed to depend on r. On the protected core every one of its derivatives is exactly zero. Fixed finite derivative bounds suffice for domain passage elsewhere, while the sharp finite-core remainder uses the same initial C_0.

## 4. Compare the complete physical evolution

Let F_f and F_g be normalized propagators of the same polynomial residual Hamiltonian and controls

    H_f=sum_j[x_j f_r(p_j)+z_j f_r(q_j)]
                       +sum_(j,l)z_(jl)f_r(q_j)f_r(q_l),

with H_g using g_r instead. Define

    Gamma=integral_0^T [sum_j(|x_j|+|z_j|)
                              +2sum_(j,l)|z_(jl)|]dt.      (6)

Single-mode differences have norm <=delta_r. Product differences have norm <=2delta_r because both factors are contractions. Thus the complete bounded perturbation identity gives

    ||F_g(T)-F_f(T)||<=Gamma delta_r.                       (7)

This is a global operator-norm comparison on all physical input and complete memory, provided the common propagators exist as constructed in the central theorem. It does not assume the actual noisy trajectory stays in the code band. The same argument holds with independent external reference and admitted tester isometries inserted at the declared times; the integrated coefficient envelope must be uniform over branches.

Combining with the central causal comparison yields

    ||F_g(T)V_0-J[U_L(T) tensor W_g(T)](I_L tensor Q)||
                      <=2E_k(T)+Gamma delta_r.              (8)

Here W_g denotes the auxiliary **gauge** propagator from the central theorem, not the finite control profile g_r. Neither term is a physical device error probability. An integer r satisfying Gamma sqrt(2)2^(-r-1)<=eta_control suffices at the stated geometry. Harmonic degree therefore grows logarithmically in the algorithmic control precision at fixed Gamma.

## 5. Coupling and implementation costs

There are r+1 odd single-mode harmonics. With A_r=sum_j|A_(r,j)|, Parseval gives the simple certified bound

    A_r<=sqrt(2(r+1)).                                    (9)

The companion derives a stronger O(log r) bound and retains exact coefficient sums. A ZZ product requires (r+1)^2 products, or 2(r+1)^2 mixed cosines via

    cos(kLq_i)cos(lLq_j)
       =[cos(kLq_i+lLq_j)+cos(kLq_i-lLq_j)]/2.              (10)

Its coefficient action is A_r^2 times the intended logical ZZ action. This is an explicit nonlinear interaction target. A waveform generator alone does not create cos(kLq_i +/- lLq_j), nor does an ideal harmonic synthesis specify the quantum pump, capture or control-line noise.

**Stronger collective construction (conventional companion).** If 2a<a_0, use f_r(q_i+q_j). Its SSS action is Z_i Z_j tensor f_r(u_i+u_j), exactly ZZ on the sum band. The finite implementation g_r(q_i+q_j) uses only r+1 mixed harmonics cos[(2m+1)L(q_i+q_j)], maximum harmonic 2r+1, and coefficient action A_r. Its global discrepancy is delta_r, so its logical pulse action enters Gamma with weight one, rather than the product route's weight two. The wider product construction remains available when the sum-band condition fails. Equal collective participation and period calibration are substantive physical conditions.

One sufficient implementation delivers the required sum concurrently. The same noiseless endpoint can result from sequential q harmonics because those harmonics commute. The noisy path need not be equivalent: an individual h(q) has [p,h(q)]=-i h'(q), which is nonzero inside the protected band. Noise inserted between harmonics can therefore couple to the logical action before the final cancellation. A sequential/Floquet implementation needs its full micromotion and duration bound or a completed-port comparison; endpoint equality is insufficient.

## 6. Calibration and unavoidable control channels

Bounded harmonic coefficient errors add through their integrated operator norm. These include unwanted logical rotation area, missing terms and extra bounded couplings. Noise along the intended native generator is not polynomial gauge noise. For example, on the code band f(q) tensor Z_M is Z_L tensor Z_M. Starting memory in |+>, exp[-i theta Z_L Z_M] produces logical dephasing probability sin(theta)^2 after memory is traced. Complete memory retains the coherent entanglement. Increasing polynomial correction order does not remove it.

A wavevector error is not globally norm-small just because its coefficient is small. For a qualified prefix Q_p,

    ||[cos((k+Delta k)q+Delta phi)-cos(kq)]Q_p||
          <=|Delta k| ||qQ_p||+|Delta phi|.                 (11)

The analogous p bound applies. Compact syndrome support alone permits arbitrarily far-translated finite-energy envelopes, so it does not give a uniform occupied-range bound. Period calibration must use a supplied moment/range estimate for the relevant comparison prefix. The periodic auxiliary after boundary spreading is not automatically a physical-moment-qualified prefix.

No physical calibration tolerance, synthesis duration, finite control-pump error or apparatus performance is acquired here. Initial encoded supply, holding, eventual destructive readout/flags and any reset/renewal remain charged. Strong conventional hybrid, Gaussian and finite-energy fault-tolerant routes are retained as alternatives, not dismissed by this conditional construction.

## 7. Status and evidence

Equations (1)-(8) are analytic constructions. Exact rational polynomial and Fourier checks are useful diagnostics. They neither certify the continuum propagation proof nor turn the nonlinear target into a built device. The no-plateau, sequential-path, wavevector and direct-logical-control failure channels are productive limitations, not physical no-go theorems for other architectures.
