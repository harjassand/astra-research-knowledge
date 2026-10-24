# Retuned low-temperature cost for the covered optimum

This is a corollary of `THREE_ROOT_GLOBAL_COVERAGE.md`. It keeps A>B fixed and retunes the network as θ tends to zero; it is not the low-temperature law of a fixed device.

Let R=A/B=M/m0>1, let f(u)=(u/sinh u)^2, and let a_θ be the middle root of the globally optimal two-band spectrum at temperature scale θ. Define x_θ=a_θ/(2θ). Then

    x_θ -> x_R,
    sinh(x_R)/sinh(x_R/sqrt(R))=R^(3/4)
    (equivalently sinh(x_R)=R^(3/4)sinh(x_R/sqrt(R))),

where x_R is the unique positive solution. Consequently

    J_opt/(π^2θ/3)
      -> 1 - (6/π^2) integral_(x_R/sqrt(R))^(x_R) (u/sinh u)^2 du,

and the one-side spring obeys

    k_opt = 4θ^2 x_R^2 m0(M-m0)/M (1+o(1)).

## Proof of the retuned limit

For each a>0, b,c are the roots determined by the fixed moments A,B as in the coverage proof. Set a=2θx. For x in any bounded interval,

    b/(2θ) -> x/sqrt(R),
    c/(2θ) -> infinity,

uniformly on compact x intervals: the first follows from b^2/a^2 -> B/A=1/R, and c^2=A+O(θ^2) there. Since G_θ(w)=2θ integral_0^(w/(2θ))f(u)du, this gives local uniform convergence

    J_θ(2θx)/(2θ) -> Γ_R(x)
      = integral_0^(x/sqrt(R)) f(u)du + integral_x^infinity f(u)du.

The integral ∫_0^∞ f=π^2/6 follows, for example, from f(u)=4u^2 sum_(n>=1) n exp(-2nu) and termwise integration. The derivative is

    Γ_R'(x)=f(x/sqrt(R))/sqrt(R)-f(x).

Its zero condition is sinh(x)/sinh(x/sqrt(R))=R^(3/4). The ratio on the left increases strictly from sqrt(R) to infinity: its logarithmic derivative is coth(x)-(1/sqrt(R))coth(x/sqrt(R))>0 because u coth(u) is strictly increasing. As R^(3/4)>sqrt(R), there is exactly one crossing. Also Γ_R'(0)=1/sqrt(R)-1<0 and Γ_R' is positive for large x, so this crossing is the unique global minimum x_R. Its value is strictly below π^2/6 because

    Γ_R(x_R)=π^2/6 - integral_(x_R/sqrt(R))^(x_R) f(u)du.

It remains to show the true minimizers stay on this scale. The trial a=2θx_R has normalized objective tending to Γ_R(x_R)<π^2/6. If a sequence of minimizers had x_θ->0, local uniform convergence would make its normalized objective tend to Γ_R(0)=π^2/6, contradicting that trial.

If instead x_θ->infinity, the quadratic root relations imply

    b^2 = B a^2/c^2 >= B a^2/(A+a^2),
    b/(2θ) >= sqrt(B)/sqrt(A/x_θ^2+4θ^2) -> infinity.

Here c^2<=A+a^2 follows from b^2+c^2=A+a^2, and the last limit uses both x_θ->infinity and θ->0. The first pass band alone then gives

    J_θ(a)/(2θ) >= integral_0^(b/(2θ)) f(u)du -> π^2/6,

again contradicting the strict trial value. Thus x_θ is bounded above and bounded away from zero. Every convergent subsequence has a limit minimizing Γ_R by local uniform convergence and optimality; uniqueness of x_R forces x_θ->x_R.

Finally, ∫_0^infinity f=π^2/6, so J_opt/(2θ)->Γ_R(x_R) gives the stated quantum-normalized conductance limit. Substituting a_θ=2θx_θ into k=a_θ^2m0(M-m0)/M gives the spring asymptotic.

## Large mass-ratio consequence

Let Q_R=1-(6/π^2) integral_(x_R/sqrt(R))^(x_R) f(u)du be the theta->0 normalized limit. A further limit R->infinity gives

    x_R = (1/4)ln(R) + ln(ln R) - ln(2) + o(1),
    Q_R ~ (3/(2π^2)) ln(R)/sqrt(R).

For the first relation, at x=q ln R the left ratio sinh(x)/sinh(x/sqrt(R)) is asymptotic to R^(q+1/2)/(2q ln R). Taking q=1/5 and q=3/10 brackets it below and above R^(3/4), respectively, so x_R is between constant multiples of ln R and x_R/sqrt(R)->0. The defining equation then reduces to e^(x_R)/2=x_R R^(1/4)(1+o(1)), yielding the displayed expansion. For the second, rewrite the limiting ratio as

    (6/π^2)[ integral_0^(x_R/sqrt(R)) f(u)du + integral_(x_R)^infinity f(u)du ].

The first term is x_R/sqrt(R)(1+o(1)). Since f(u)=4u^2e^(-2u)(1+o(1)) and the root equation gives e^(x_R)=2x_RR^(1/4)(1+o(1)), the second term is O(R^(-1/2)); it is smaller by a factor of order ln R. This large-R statement is about the low-temperature limiting ratio and is not a uniform joint limit in R and θ.

These are ideal single-backbone harmonic ballistic design costs. In particular, k_opt shrinking like θ^2 describes a family of retuned devices; it does not imply an existing fixed specimen becomes softer on cooling.
