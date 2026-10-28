# A universal noisy-design preparation operation

Every projective 2-design, without an incoherence or hemisphere input,
admits the following operation. For a supplied dimension d>=2 and

    0<=t<=t_d=sqrt(1-1/d^2),

replace every pure preparation S_i by

    sigma_i(t)=t S_i+(1-t)I/d.                       (1)

For EVERY preparation vector p,

    D(sum p_i sigma_i(t)||I/d)<=(1/2)D(p||w).        (2)

It also has the full convex-order conclusion of Theorem A, with sigma_i
in place of S_i. This is a quantified change to the preparation channel,
not a proof of the unmodified entropy inequality for all designs.
For t<1 equality in(2) holds only at p=w.

The retained pure-state fraction t_d is about0.9428 in d3,0.9682 in d4,
and0.9922 in d8. The added white fraction is asymptotically1/(2d^2).
The elementary ordinary DPI-plus-convexity comparator guarantees(2)
only at t<=1/2, because it discards the design moment structure. This
compares that specified argument, not every known sharp depolarizing-
channel or frame theorem. Historical priority is UNKNOWN.

A particularly simple directly evaluable rational compiler is

    t_rat=2(d^2-1)/(2d^2-1),
    sigma_i=[2(d^2-1)S_i+I/d]/(2d^2-1).             (1a)

Its exact threshold slack is

    1-1/d^2-t_rat^2=(d^2-1)/[d^2(2d^2-1)^2]>0.

Thus the scalar coefficients need only O(log d) bits, and the new
matrices take O(nd^2) arithmetic operations once the design is supplied.
No hemisphere optimizer or irrational root qualification is needed.
The white fraction is exactly1/(2d^2-1): t_rat is6/7,16/17,30/31,126/127
in dimensions2,3,4,8, respectively.

Even allowing the BEST state-independent depolarizing SDPI constant
does not close the matched generic-composition gap. For traceless Y,
the states rho_u=I/d+uY obey
`D(rho_u||I/d)=(d/2)u^2 TrY^2+O(u^3)`. Depolarization replaces u by tu,
so its optimal contraction coefficient is at least t^2. Consequently
generic preparation DPI followed by any scalar state-independent
depolarizing coefficient cannot guarantee1/2 when t>1/sqrt2. The new
moment-aware compiler passes that threshold in every d>=2. This is a
precise limitation of that proof template, not of every established
source-aware entropy argument.

## Mixed-atom extension of the transport theorem

The proof of Theorem A in `PROOF.md` only needs positive trace-one
atoms, mean I/d, and the covariance inequality

    sum w_i (Tr sigma_i Y)^2<=Tr Y^2/[d(d+1)]

for traceless Hermitian Y, together with the same hemisphere condition.
Section2 uses exactly this inequality; its Cauchy argument, the matrix
lemma and hinge duality then apply unchanged. Rank-one atoms are used
only in the separate cheap incoherence sufficient condition.

For(1) the covariance is exactly t^2 times the pure-design covariance,
so that inequality is automatic whenever0<=t<=1.

## A universal hemisphere bound from two moments

For fixed unit v let Y=Tr(S_i |v><v|) under the design weights. Then

    mu=EY=1/d, Var(Y)=v_d=(d-1)/[d^2(d+1)].

Put a=(d-2)/(2d)>=0. The mixed-atom score minus1 is
`2t(Y-mu)-2a`. Using z_+=(|z|+z)/2 and Cauchy--Schwarz gives

    sum w_i(2Tr sigma_i |v><v|-1)_+
       <=sqrt[a^2+t^2 v_d]-a.                     (3)

This is at most1/d^2 exactly when

    t^2 v_d<=2a/d^2+1/d^4=(d-1)^2/d^4,

equivalently t^2<=1-1/d^2. Thus(3) pays the hemisphere condition for
every v. Apply the mixed-atom transport theorem and ordinary Gibbs
duality to prove(2). No eigensolver, state grid or optimization enters
this universal admission step. A rational receiver needs only the
single inequality `d^2 t^2<=d^2-1`, after the design is qualified.

For t<1 every mixture in(2) is faithful. For nonscalar K, its centered
score variance is `4t^2 TrK0^2/[d(d+1)]`, strictly below the pair-score
variance `2TrK0^2/d`. Hence the exp inequality is strict. The Gibbs
argument with K=logM gives strictness unless M=I/d; then equality
requires D(p||w)=0. This proves the equality statement.

## Sharpness for this mechanism, not for entropy truth

Fix t>t_d, t<=1. Put b=a/t, R=sqrt(v_d+b^2) and use the two-radius law

    y_-=mu+b-R, y_+=mu+b+R,
    Prob(y_+)=(R-b)/(2R), Prob(y_-)=(R+b)/(2R).       (4)

It has mean mu and variance v_d, and both radii lie strictly in[0,1].
For the lower endpoint, `(mu+b)^2-R^2=mu^2+2mu b-v_d>0`.
The center mu+b is less than1 since t>=t_d>1/2. For the upper endpoint
it suffices that

    t>=(d-2)(d+1)/(d^2-2)=1-d/(d^2-2),

which follows from t>=t_d>=1-1/d^2. The mixed score-minus1 at the two
radii is exactly `+/-2tR`, so(3) is attained and exceeds1/d^2.

This scalar extremizer has a finite actual projective-design lift.
In the orthogonal C^(d-1) choose a finite weighted projective 2-design,
and add an independent four-phase relative twirl to
`sqrt(y)e0+sqrt(1-y)e^(i theta)phi`. Sector decomposition of the
symmetric square gives the design in C^d, as detailed in
`DESIGN_OBSTRUCTION.md`.

No SIC existence premise is needed for the orthogonal design. In any
dimension r, mix with probabilities1/(r+1) and r/(r+1) the uniform
computational basis and the uniform flat vectors
`(zeta_1,...,zeta_r)/sqrt r`, with independent fourth roots zeta_j.
Its second moment is `(I+Swap)/[r(r+1)]`: the flat part has moment
`(I+Swap-D)/r^2`, where D projects onto the diagonal |jj> span, and
the basis part has moment D/r. Equal global rays may be grouped.
This gives an explicit finite, possibly exponential-size construction
in every r. The root independently supplied the same lift using three
phases instead of four; neither version relies on unknown SIC/MUB
existence in the orthogonal dimension.

Thus t_d is the largest universal retained fraction for the full
convex-order/hemisphere mechanism, even among actual finite designs.
It is NOT proved to be the largest fraction for entropy(2). The latter
can hold when the mechanism fails, as the qubit SIC demonstrates.

## Exact qutrit interface

For the48-state design in `DESIGN_OBSTRUCTION.md`, choose t=16/17.
It qualifies because `9(16/17)^2<8`, receiving ALL p on that actual
frame. At t=19/20, the same frame has hemisphere value37/330,
exceeding1/9 by1/990: an exact failure of full convex order after
the smaller noise. Neither statement is an entropy counterexample.
`certify_noise.py` records the rational admission and this obstruction,
plus actual strict entropy controls. Frame acquisition is paid
separately from the cheap scalar receiver.
