# Independent audit of the three-mode construction

Verdict: the central strict-improvement certificate is correct. I independently reconstructed its averaged quartic polynomial directly from the two gradient columns, without importing the report's Hessian or coefficients. All signs, the factor 1/2 in the Taylor expansion, and normalized angular averages agree. No mathematical correction to this construction is needed.

## Exact reconstruction

Put r=exp(κx), F=(4cos(3y),-3sin(3y)), and η=(x+10)(-x) on [-10,0], extended by zero. After the left rotation R_y is removed, the gradient columns of H=r^-1 R_y ηF are

r^-1 (4(η'-κη)cos(3y),-3(η'-κη)sin(3y)),
r^-1 (-9ηsin(3y),-5ηcos(3y)).

The baseline gradient is r diag(κ,1). Direct quartic expansion and normalized angular averaging give

J(Φ₀+λH)-J(Φ₀) = λ² I₂/2 + λ⁴ J(H).

Both odd coefficients vanish identically: the relative-angle shift π/3 changes both perturbation columns' signs while keeping the baseline fixed. The quadratic density is αη'²+γηη'+βη², with the report's α and β and

γ = -2033κ³/2 + 5829κ²/2 - 2938κ + 1044.

Since η vanishes at both support endpoints, the mixed integral is zero. An independent rational termwise interval bound places I₂ between -17082.785386 and -17082.785333, proving the advertised I₂<-16000.

## Boundary conditions and remainder

The cutoff is continuous and piecewise smooth, hence its derivative jumps do not create distributional singularities in its first weak derivative. H vanishes at both ends of [-10,0]; its normal derivative need not vanish. Only potential traces, not normal jets, are prescribed. The baseline and perturbation are periodic and the entire seeded construction is W1,4 on its finite strip.

The gradient bound is a Frobenius norm bound, not a bound on each entry separately. Its column norms are at most 130 exp(9) and 225 exp(9), since κ<0.9, η≤25, |η'|≤10, |F|≤4 and |F_y+JF|≤9. Therefore |DH|≤sqrt(67525) exp(9)<260 exp(9).

The elementary estimate |G(A)|≤15|A|⁴ follows from |det A|≤|A|²/2; the coefficient obtained by summing absolute terms is 359/24<15. Integrating over a width-10 strip with normalized angular measure gives |J(H)|≤150·260⁴·(11/4)³⁶≈4.48706·10²⁷<10²⁸. There is no missing factor 2π.

With λ=10^-16, the negative quadratic contribution is less than -8·10^-29; the quartic error is less than 10^-36 and the seed overhead is less than 2·10^-36. The asserted strict improvement greater than 7·10^-29 follows. The seed-to-target exponential segment has duration log(10^9)/κ>10, so the support fits without touching the seed.

## Significance and limitations

This gives an actual finite-width incoming path from zero to (cos y,sin y), with physical frequencies 1,2,4 and action strictly below the exact circular-family required supply. Thus that restricted endpoint formula cannot be a dominating storage for unrestricted compatible strips. It is not a negative closed-loop construction and does not refute quasiconvexity. It does not identify full required supply, prove numerical usefulness of the tiny conservative gap, or independently validate the source's heat certificate.

Replay: python independent_audit.py. This uses SymPy and exact rational arithmetic for every acceptance gate; printed decimals are illustrative only. The audit script checks the direct quartic expansion, odd-coefficient cancellation, all quadratic coefficients, root isolation, an independent rational sign box, derivative-bound arithmetic, the G bound, quartic remainder arithmetic, and seed overhead.

## Addendum: a substantially stronger rational-amplitude certificate

The same construction admits the simple choices L=6, λ=2·10^-7 and seed radius ε=10^-4. For t=-x in [0,6], η=t(6-t), and η'=dη/dx=2t-6; the sign used in improve_gap.py is correct.

Writing d=η'-κη, the exact angular quartic average is exp(4κt)Q(t), where

Q=(46331d⁴+266916d³η+700152d²η²+994176dη³+614592η⁴)/64.

The new script certify_improved_gap.py derives Q from the independently expanded full energy. Since Q has degree at most 8 in t, it forms

A(t)=Σ[j=0 to 8] (-1)^j Q^(j)(t)/(4κ)^(j+1)

and checks the identity A'+4κA=Q. Thus J(H)=exp(24κ)A(6)-A(0). Each rational function of κ is enclosed with exact rational interval arithmetic on its previously verified isolating interval. The exponential is enclosed using the Taylor sum through degree 120; the omitted positive tail is bounded by the first omitted term divided by 1-x/122. This supplies a rigorous enclosure without numerical quadrature.

Results (decimal endpoints rounded outward here):

- -173.019158 < I₂ < -173.019156, so I₂<-173.
- 903279636156734 < J(H) < 903279636193987, so J(H)<10^15.
- exp(6κ)<10^4, so the exponential segment is longer than six and the cutoff fits.
- The previous exact seed-overhead coefficient bound remains valid: overhead <2ε⁴=2·10^-16.

Consequently the total incoming action minus c/4 is strictly less than

(-173/2)(2·10^-7)² + 10^15(2·10^-7)⁴ + 2·10^-16
= -9299/5000000000000000
= -1.8598·10^-12.

In particular the certified gain is greater than 1.8·10^-12. This is a stronger version of the same restricted-storage refutation; its interpretation and boundary conditions are unchanged. The canonical report and receipt were not modified by this audit.

Replay: python certify_improved_gap.py. Every acceptance gate uses exact arithmetic; printed decimals remain illustrative.
