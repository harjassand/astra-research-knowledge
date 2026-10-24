# Three-root dual family covers every strict resource pair

## Result

Fix any θ>0 and any A>B>0, where A=4K/m0 and B=4K/M for m0>0, M>m0, K>0. There is a unique strict triple 0<b<a<c and a unique pair λ<0, μ>0 such that

    A=b^2+c^2-a^2,       B=b^2 c^2/a^2,
    F(ω)=h_θ(ω)+λ+2μω^2

has precisely the three positive roots b,a,c, with h_θ(ω)=ω[(ω/2θ)/sinh(ω/2θ)]^2. Its sign is negative on (0,b) and (a,c), positive elsewhere. Thus the three-root family covers the complete strict physical resource domain; there is no uncovered range of K/M or temperature in this ideal model. The corresponding roots synthesize the exact one-side-resonator cell with backbone mass m0, total mass M, and intercell spring K.

The proof is an existence argument, not a parameter sweep. It does not bound the required optimal internal frequency or spring uniformly as M approaches m0.

## Parameterize the fixed-moment family

For any a>0, define b^2<c^2 to be the two roots of

    z^2 - (A+a^2)z + Ba^2 = 0.

The discriminant is

    (A+a^2)^2-4Ba^2 = (a^2+A-2B)^2+4B(A-B)>0.

The roots are positive (their sum and product are positive), and the polynomial evaluated at z=a^2 is a^2(B-A)<0. Hence b<a<c strictly. This parametrizes all a>0 with the desired moments exactly. Write

    G(x)=integral_0^x g_θ(ω)dω,
    g_θ(ω)=[(ω/2θ)/sinh(ω/2θ)]^2.

The two-band objective is J(a)=G(b)+G(c)-G(a), with b,c determined above.

As a tends to zero, c^2 tends to A and b^2/a^2 tends to B/A, so

    J(a) -> G(sqrt(A)).

For large a, direct expansion of the quadratic roots gives, with d=A-B>0,

    b^2 = B - Bd/a^2 + O(a^-4),
    c^2 = a^2 + d + Bd/a^2 + O(a^-4),
    b = sqrt(B) - sqrt(B)d/(2a^2) + O(a^-4),
    c = a + d/(2a) + O(a^-3).

Since g_θ(x)=O(x^2 exp(-x/θ)) at large x,

    J(a) = G(sqrt(B))
           - g_θ(sqrt(B)) sqrt(B)(A-B)/(2a^2)
           + o(a^-2).

In particular, J tends to G(sqrt(B)) at infinity and is strictly below that limit for all sufficiently large finite a. Since G is strictly increasing and A>B,

    lim_(a->0) J(a)=G(sqrt(A)) > G(sqrt(B)) > J(a0)

for some finite a0. Both endpoint limits strictly exceed J(a0); continuity therefore puts a global minimum of J at a finite interior a. This endpoint-gap argument is why minimizing a one-side-resonator spring constant by a finite sweep would not suffice, whereas the present argument proves existence for every A>B.

## Stationarity gives a quadratic dual

Use three variables (b,a,c) with the two smooth constraints

    C1=b^2+c^2-a^2=A,
    C2=ln(b)+ln(c)-ln(a)=(1/2)ln(B).

Their gradients are independent because b,a,c are distinct. At the interior minimum, Lagrange multipliers η,ζ give

    ∇J = η∇C1 + ζ∇C2.

The three component equations are

    g_θ(b)=2ηb+ζ/b,
    g_θ(a)=2ηa+ζ/a,
    g_θ(c)=2ηc+ζ/c.

Multiplying by the corresponding frequency and setting λ=-ζ, μ=-η yields

    h_θ(x)+λ+2μ x^2=0,   x in {b,a,c}.

It remains to check the multiplier quadrant rather than assume it. If λ,μ are both nonnegative, F is positive. If λ>=0 and μ<0, then

    F(ω)/ω^2 = g_θ(ω)/ω + λ/ω^2 + 2μ

is strictly decreasing: g_θ(ω)/ω=ω/[4θ^2sinh^2(ω/2θ)] is strictly decreasing, as is the nonconstant λ/ω^2 term when λ>0. It cannot have three zeros. If λ<0 and μ<=0, rescale x=ω/(2θ), λhat=λ/(2θ), μ_hat=2μθ and multiply F/(2θ) by sinh^2(x)/x^2. The resulting entire series is

    Q(x)=λhat+x+sum_(n>=1) c_n[2μ_hat+4λhat/((2n+2)(2n+1))] x^(2n),
    c_n=2^(2n-1)/(2n)! > 0.

Every even coefficient is negative, so Q''(x)<0 on x>0 and Q has at most two distinct zeros. These cases exclude every quadrant except λ<0,μ>0.

## The required all-frequency sign follows from a root-count lemma

For λ<0<μ, the bracket

    s_n=2μ_hat+4λhat/((2n+2)(2n+1))

strictly increases to 2μ_hat>0. If all s_n are nonnegative, Q''>0 and Q has at most two positive zeros. Otherwise let N be the largest index with s_N<0. Then s_n<0 for n<=N and s_n>=0 for n>N, with s_n>0 eventually. Termwise differentiation on any compact subset of x>0 shows that

    d/dx [Q''(x)/x^(2N-2)] > 0.

Indeed, for n<N the coefficient is negative and its divided power has negative exponent, so its derivative is positive; the n=N term is constant; for n>N the coefficient and exponent are nonnegative, and some are strictly positive. Therefore Q'' has at most one positive zero, Q' at most two, and Q at most three, by Rolle's theorem. Since b,a,c are three distinct zeros, they are all the positive zeros. They must be simple: a multiple one among three distinct zeros would give at least three distinct zeros of Q' and at least two of Q'', a contradiction.

F(0)=λ<0 while F(ω)>0 for sufficiently large ω because μ>0 and h_θ decays. Three simple roots with no others force

    F<0 on (0,b) union (a,c),
    F>0 on (b,a) union (c,infinity).

Thus the stationary minimizer is exactly the strict-sign dual family required by the global spectral comparison.

In particular, let ΔA=integral 2ω(chi-chi_*)dω and ΔL=integral (chi-chi_*)/ω dω for any finite passive comparator with the same K,M and backbone mass m>=m0. The established trace and determinant identities give ΔA=4K/m-A<=0 and ΔL=0. Since r=F/ω has the strict sign pattern above, r(chi-chi_*)>=0 pointwise, and

    J(chi)-J(chi_*) = integral r(chi-chi_*)dω - μΔA >= 0.

So this covered candidate is also globally optimal against the full passive single-backbone class in the stated resource contract, not only against other one-resonator cells.

## Uniqueness and physical synthesis

For any two-band candidate with the same A,B,

    integral 2ω(chi-chi_*)dω=0,
    integral (chi-chi_*)/ω dω=0.

The second identity is the endpoint-log relation ln(bc/a)=(1/2)ln B. With r=F/ω=g_θ+λ/ω+2μω, the strict sign pattern gives r(chi-chi_*)>=0 pointwise, so the constructed spectrum is the unique minimum among the entire fixed-moment two-band family. Any second three-root pair with the same A,B would have its own strict dual and would also be the unique minimum; hence the pair must coincide. The three-root moment map is therefore bijective onto A>B>0 (at the root-triple level).

Finally set

    M=m0 A/B,   K=m0 A/4,   M_side=M-m0,
    k=a^2 m0 M_side/M.

All parameters are finite and positive for every strict resource pair. The standard two-mass pendant cell has squared frequencies {0,a^2} at q=0 and {b^2,c^2} at q=pi: the q=pi trace is a^2+A=b^2+c^2, and its determinant is Ba^2=b^2c^2. It realizes the globally optimal sign spectrum under the original single-backbone, finite passive network assumptions.

The strict boundary A=B (equivalently M=m0) is excluded: then the side mass is zero and the asymptotic negative term vanishes. No statement here covers multiple intercell links, diffusive transport, material fabrication costs, or a uniform bound on k or c as the boundary is approached.
