# Independent review: homogeneous-fiber conductance

## Verdict and binding

PASS as a complete mathematical capacity/mass certificate for the declared smooth coercive homogeneous class. This receipt does not accept the raw-input consumer, numerical integrator or a claim of historical novelty/practical advantage.

I read the entire `HOMOGENEOUS_FIBER_CAPACITY_CANDIDATE.md` and verified SHA-256 `84099bfdd17e90b5ac5b4560af97a8cbb5e7aa10aae8d575b508c9ea6c2db525`. Its text is unchanged. The ordinary conditional-transport capacity principle is the one read in `../acquired_entropic_capacity_20261031/PROOF.md`, SHA-256 `9de2b84db7b432a346605b0b0f04b8737ea8424c47346c2fbb58b2684af4f291`.

A separate file, `HOMOGENEOUS_FIBER_SHARPER_COROLLARY_REVIEWER.md`, derives the improved factor suggested by the parent/author. That corollary does not silently replace any bound in the frozen original.

## 1. Scaling and the actual process

The assumptions mean U(tz)=t^p U(z) for positive t, with p an even integer at least two, m>=1, and U(z)>=a||z||^p with a>0. Smooth homogeneous positive polynomial is understood as strictly positive away from zero. Coercivity makes every polynomial moment under exp(-U) finite.

The substitution z=(beta v)^(-1/p)u gives exactly

    integral exp[-beta v U(z)] dz=(beta v)^(-m/p) Z_U.

Thus q=v^(-m/p) is a valid unnormalized marginal; beta^(-m/p)Z_U is a y-independent common constant. Cancellation of that constant does not make the true projected coordinate Markov. Its generator on u(y) contains -v'(y)U(z)u'(y), as the source states.

The coordinates must be physical orthogonal Euclidean coordinates. A general linear coordinate change would change the isotropic Dirichlet metric and cannot be substituted without paying it. Neither a source coordinate nor a coercivity certificate is silently supplied by this theorem's future raw-input application.

## 2. Conditional current and moment acquisition

The normalized conditional density has logarithmic derivative

    partial_y log rho=(m/p)v'/v-beta v' U.

For w=-(v'/(pv))z, div w=-m v'/(pv) and w.grad_z log rho=beta(v'/p) z.grad U=beta v' U. These cancel exactly. No angular symmetry, convexity, eigenbasis or conditional relaxation estimate enters.

Differentiating the scalar partition scaling (or integrating div(z exp(-beta v U))) gives E U=m/(p beta v). Since ||z||^2 <=(U/a)^(2/p) and t^(2/p) is concave for p>=2,

    E||z||^2 <= [m/(p beta a v)]^(2/p).

Multiplying by (v'/(pv))^2 gives the displayed transport-cost bound, with denominator p^(2+2/p) and v^(2+2/p). For p=2 Jensen is an equality step; coercivity may still be loose. For p>2 no reversal of Jensen is made.

The normalized continuity current contains the unknown Z_U only as an analytic proof object. The proposed bound uses q, beta, m, p, kappa and an acquired a, not a sampled or numerically normalized current. Thus it is legitimate to avoid computing Z_U for this OUTPUT TASK. This does not construct a fiber sampler or give an oracle for arbitrary observables of its angular law.

## 3. Original integrated constants

Let W=v^(m/p), s=1+2/p and C_m=m^(2/p-1)/[p^(1+2/p)(beta a)^(2/p)]. On [0,1/2], -W'=(m/p)(-v'/v)W is nonnegative. Direct multiplication, including the endpoint by continuity, gives

    K W <= C_m (-v') v^(-s) (-W').

For f=(-v')v^(-s), f(0)=0, f>=0 and

    f'=-v''v^(-s)+s v'^2 v^(-s-1).

Here -v''<=4 kappa, |v'|<=3 kappa/2 and v>=1+9 kappa/16. The stated D is therefore an upper bound on f', even if f' changes sign. Integration by parts yields -f(b)W(b)+integral f'W. Its endpoint term has the favorable sign and may be dropped. Evenness doubles both sides, so R1/R0<=1+C_m D.

For the coupled quartic family, U>=d_min sum z_i^4 >=(d_min/m)||z||^4 gives a=d_min/m, and C_m=1/[8 sqrt(beta d_min)]. This cancellation of m is valid; it does not authorize hiding dimension dependence in an arbitrary supplied a. With beta=d_min=kappa=1, replacing v_min by 1 gives D<=59/8 and the original factor 1+D/8<=123/64, exactly as stated. The separate sharper corollary improves this but is not needed for correctness.

## 4. Global model and boundaries

Since v(y)~kappa y^4, q(y) has two-sided tail order |y|^(-4m/p). The condition 4m>p is sufficient and, for this exact model, necessary for normalizability; equality has logarithmic divergence. In particular the quartic example needs m>=2. The stated explicit one-sided tail bound follows from y^2-1 >=y^2(1-1/T^2) for y>=T>1 and direct power integration. No uncharged reflecting wall is introduced.

The proposed weighted Lyapunov function V=1+y^2+K0||z||^2, K0=1+kappa/p, is coercive and nonnegative. Euler's identity gives

    grad V.grad F=2[y v'+K0 p v]U.

The identities y v'=4 kappa y^2(y^2-1)>=-kappa and v>=1 imply the bracket is at least p. Consequently

    L V <=2(1+K0 m)/beta,

with an additional nonpositive drift omitted. Polynomial coefficients are locally Lipschitz, so the usual stopped Lyapunov argument rules out finite explosion. The smooth positive integrable Gibbs density and the conservative elliptic gradient diffusion provide the reversible Dirichlet form used in the capacity argument. No convexity assumption is needed for these statements.

Here v is globally even and the full marginal is q/Z, so the right-tail integral MA equals the left-basin mass before normalization. Applying the conditional-transport lower bound and the y-only Dirichlet upper bound cancels Z, giving the claimed sandwich for cap_mu(A,B)/mu(A). It is NOT an arbitrary-start MFPT, first-passage CDF, or a fast-fiber limiting generator.

## 5. Raw grammar and actual acquisition boundary

The explicit nonnegative mixed quartics need not be convex. For instance U=z1^4+z2^4+10 z1^2 z2^2 is coercive while its Hessian at (1,1) has eigenvalue -8. Positivity of its coefficient grammar, not convexity, provides the required radial lower bound.

For an actual family member, the lowest homogeneous part is (1+kappa)U(z). A direction annihilating its directional derivative must have zero fiber component: otherwise U would be translation-invariant along a nonzero fiber vector, contradicting its coercivity by evaluating the line through zero. Thus the proposed linear derivative-kernel criterion has the claimed one-dimensional kernel. It supplies only a route: physical normalization, recognition of the full F=vU identity and proof of coercivity in the actual transverse coordinates remain necessary. A limited aligned-quartic finder may legitimately return UNKNOWN on rotated or other positive forms.

Exact outward algebraic-root arithmetic can in principle evaluate q at rational y for rational beta/kappa and integer p,m. This is not acceptance of any particular implementation, complexity bound or all-population input parser. The root polynomial theorem does not rely on such an implementation having been executed.

## 6. Checks, comparators and conclusion

I executed 15 independent exact symbolic checks: Euler and conditional continuity identities for coupled homogeneous degrees 2,4,6,8; the weighted Lyapunov algebra for each; both original and improved rational factors; and the nonconvex quartic example. These diagnostics support, but do not replace, the analytic proof above.

Homogeneous scaling, virial identities, concavity, conditional transport and the Dirichlet/Thomson capacity principles are ordinary ingredients. This review establishes the assembled conditional finite-rate certificate, not historical priority, complexity hardness of Z_U, exclusive advantage over ordinary methods supplied with this certificate, or physical performance.

No blocking error was found in the original source. The distinction between an analytical normalized current and the scalar operations actually required by the output is correctly maintained. The raw consumer and its finite numerical/resource receiving must be reviewed separately when available.
