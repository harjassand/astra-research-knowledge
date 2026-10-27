# Reciprocal concavity for integrated noncommuting resolvent products

## Status and exact external input

A proof, not a numerical conjecture. The noncommuting input is the following exact specialization of Haonan Zhang, *From Wigner–Yanase–Dyson conjecture to Carlen–Frank–Lieb conjecture*, arXiv:1811.01205v2, Theorem 1.1(2), PDF page 3:

https://arxiv.org/pdf/1811.01205

For positive definite matrices A,B and every n>0,

    (A,B) -> Tr[(B^(-1/2) A^(-1) B^(-1/2))^n]

is jointly convex. Its parameters are p=q=-1, exponent s=n, and invertible fixed K=I. These satisfy precisely the theorem's range -1 <= q <= p <= 0 and s>0. This is a statement about a trace of a positive sandwich, NOT operator convexity and NOT scalar Feynman parameterization. The paper's theorem and parameter range were checked directly in the primary PDF. The application below is elementary once this input is available.

## The integrated theorem

Fix positive definite S,Q in finite dimension d. For n>1/2 put

    P_X(t) = X(tI+X)^(-1),
    I_n(S,Q) = integral_0^infinity Tr[(P_S(t) P_Q(t))^n] dt,
    J(u,v) = I_n(S/u,Q/v),  u,v>0.

For nonintegral n the trace notation denotes the positive sandwich, which has the same eigenvalues as the product. The original application uses integer n>=2.

**Claim:** J is positive, finite, jointly convex and homogeneous of degree -1; consequently h=1/J is concave and homogeneous of degree 1.

**Proof of convexity.** For each t>0 define A=I+ut S^(-1) and B=I+vt Q^(-1). Then

    P_(S/u)(t)=A^(-1),  P_(Q/v)(t)=B^(-1).

The integrand of J is exactly the convex trace function above composed with an affine map in (u,v). Integrating preserves convexity. Integrability follows from the bound by d near zero and O(t^(-2n)) near infinity. Positivity is immediate for positive definite matrices.

**Homogeneity.** Changing variable w=c t gives

    J(cu,cv)=J(u,v)/c.

**Convexity plus negative homogeneity implies reciprocal concavity.** More generally, let J>0 be convex and homogeneous of degree -1 on a convex cone. Set h=1/J. For x,y in the cone, write a=h(x), b=h(y). Homogeneity gives J(x/a)=J(y/b)=1. Convexity therefore gives

    J((x+y)/(a+b))
      = J([a/(a+b)] x/a + [b/(a+b)] y/b) <= 1.

By homogeneity the left side is (a+b)J(x+y). Hence h(x+y)>=h(x)+h(y). Degree-one homogeneity then gives concavity. This closes the proof.

## Exact reciprocal rescaling consequence

Apply midpoint concavity of h to x=(1/3,1), y=(1,1/3). Their midpoint is (2/3,2/3), so

    h(1/3,1)+h(1,1/3) <= 2h(2/3,2/3) = (4/3)h(1,1).

Equivalently, writing C=I_n(S,Q), A=I_n(3S,Q), B=I_n(S,3Q),

    C/A + C/B <= 4/3.                         (1)

This holds for every real n>1/2, not just the three needed integer degrees.

More generally, for any c>0,

    I_n(S,Q)/I_n(cS,Q) + I_n(S,Q)/I_n(S,cQ) <= 1+1/c.

## Singular PSD matrices and zero overlap

Replace S,Q by S+epsilon I,Q+epsilon I and take epsilon down to zero. At every t>0 the resolvent products and their positive-sandwich trace powers converge. Uniformly for 0<epsilon<=1, a bound is

    d * min(1, ((||S||+1)(||Q||+1))/t^2)^n,

which is integrable for n>1/2. Dominated convergence proves continuity of all the integrated quantities. The division-free form of (1),

    3 C(A+B) <= 4 A B,                         (2)

therefore holds for all PSD S,Q.

If SQ != 0, all A,B,C are strictly positive and (1) follows from (2). If SQ=0 (orthogonal supports, including either zero matrix), all three integrals vanish, and (2) plus every direct-payment inequality below reads 0<=0. No undefined 0/0 ratio is asserted.

## Low-order source payment

Let alpha=(2/3)^n. Weighted Cauchy and (1) give

    alpha A + 2 B
      >= (sqrt(alpha)+sqrt(2))^2 / (1/A+1/B)
      >= (3/4) ((2/3)^(n/2)+sqrt(2))^2 C.       (3)

For n=2,3,4 this coefficient strictly exceeds 2+4/2^n:

    n=2: (3/4)(2/3+sqrt(2))^2 > 3,
    n=3: (3/4)((2/3)^(3/2)+sqrt(2))^2 > 5/2,
    n=4: (3/4)(4/9+sqrt(2))^2 > 9/4.

The respective exact margins are sqrt(2)-7/6, 2/sqrt(3)-7/9, and 2sqrt(2)/3-65/108, each positive. Therefore the integrated degree contributions required by the exact flat-rank-two physical reset interface are nonnegative for n=2,3,4, strictly positive whenever SQ!=0. The known separate n=1 resource and pointwise n>=5 argument are not reproved in this note.

## Scope

This establishes the previously live reciprocal-rescaling interface for genuinely noncommuting matrices. It does not assert a noncommuting Stieltjes representation. It uses an established trace-convexity theorem with its exact hypotheses checked; the new task-specific step is the integrated homogeneous reciprocal-concavity application and resulting source payment.
