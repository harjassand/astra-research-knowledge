# Direct phase-product counting with superlinear operation count

27 October 2026. Conditional on the supplied ETH manuscript. A constructive original-input extension for local phase products and bounded-formal-degree arithmetic programs. This is not a general circuit theorem or a practical speed claim.

## Theorem

Fix locality k>=1 and b>=1. Put q=2^b, d=2^(b-1), and let zeta be primitive of order q. The input consists of n independent Boolean variables and m phase gates, each specifying at most k variables and a table f_j with values in Z/qZ. Let L be the explicit bit description, including indices and tables. Define

    Z=sum_(x in {0,1}^n) zeta^[sum_j f_j(x|S_j)].

For lambda=ceil(log2 n), nu=ceil(log2 lambda), put

    h=ceil(log2(2+km/n))+nu+1,       a=h/lambda.

For sufficiently small a, a deterministic exact algorithm computes Z in

    (L+n)^O_(k,b)(1) * 2^[O_(k,b)(n sqrt(a) [log2(2/a)]^(3/2))]

bit operations and polynomial space. For m=n^(1+o(1)) this is subexponential in the ORIGINAL input count n, even when m/n exceeds every fixed power of log n. All summaries are manufactured. There is no supplied low rank or decomposition. For m<=n*2^[(log2 n)^alpha], fixed alpha<1, the exponential term is

    2^[O_(k,b,alpha)(n (log n)^[-(1-alpha)/2] (log log n)^(3/2))].

The binary special case computes zeros of a degree-k F2 polynomial p with m listed monomials: use factors corresponding to (-1)^p, obtain Z, and return (2^n+Z)/2.

## 1. A representation whose degree depends on precision

Multilinearly interpolate each local phase table, obtaining G_j(X) over Z[zeta], with degree at most k and at most 2^k coefficients. Let pi=zeta-1. Every coefficient of G_j-1 is divisible by pi: modulo pi all table values equal one, so their nonconstant finite differences vanish and the constant term of G_j-1 vanishes too.

Choose P=n+2 and ell=dP. Work in the commutative Q-algebra

    A=Q(zeta)[V]/(V^ell),

with factors B_j(X,V)=1+V(G_j(X)-1). The coefficient of V^t in their product has input degree at most kt, even when every factor receives independent copies of its inputs. Therefore the entire retained product has degree at most

    D_input=k(ell-1)=O_(k,b)(n),

independently of m. Scopes remain at most k. For binary monomial phases the factors are simply 1-2V*x^S. No intermediate-state counting variables are introduced.

## 2. Exact truncation and reconstruction

In Z[zeta], pi^d generates (2). Indeed, 2=Phi_(2^b)(1)=product_(a odd)(1-zeta^a), each (1-zeta^a)/(1-zeta) is a cyclotomic unit, and there are d factors. For b=1, pi=-2 directly. A product selecting t nonconstant factor terms is divisible by pi^t. Hence every discarded term with V-degree at least ell=dP vanishes modulo 2^P. At Boolean inputs, evaluating the retained V-polynomial at V=1 recovers the original phase product modulo 2^P; summing over inputs preserves this congruence.

Use the integer basis 1,zeta,...,zeta^(d-1), with zeta^d=-1. Each input contributes one signed basis vector. Every coordinate of Z is an integer in [-2^n,2^n], and thus its residue modulo 2^(n+2) uniquely determines it by centered reconstruction. This charges O_(b)(n) output bits regardless of operation count. The manuscript's rational interpolation works coordinatewise in the fixed-dimensional field Q(zeta); its identities are algebraic and require no ordering of coefficients.

## 3. Constructing summaries from the raw scopes

Include a neutral factor for each variable. The incidence count M is at most km+n. Fix in all possible ways the variables appearing in more than

    b0=ceil(M/n)ceil(sqrt(lambda))

scopes. There are at most n/sqrt(lambda) such variables, leaving N>=n/2 free variables for large n. These are disjoint branches on original inputs. Substitute the phase tables, simplify constants, and retain neutral factors. The remaining incidence bound b_inc satisfies log2(b_inc)=O(h), while maximum scope w<=k.

For each branch put lambda'=ceil(log2 N) and choose

    r=floor(sqrt(lambda/h)),      t=ceil(log2 r),
    Q=floor(lambda'/(128t)),      tau=1/(r lambda'),
    D_aux=r^(2Q),
    A0=ceil(log2(2 b_inc r^2 lambda')),
    R=ceil(sqrt(8Q A0))+32.

Run all source feasibility guards. In the asymptotic range a->0,

    A0=O(h),
    R/Q=O(sqrt(a log(2/a))),
    D_aux<=(2N)^(1/64),
    b_inc=N^o(1).

Thus 2(b_inc+w)D_aux^2<=N<=M_branch and 2Qr^2<=N eventually hold. The source's R-point central interval contains all integers within R/4 of the binomial mean. Its exceptional spectral fraction is at most

    2 exp(-R^2/(8Q)) <= 2^(1-A0)
                       <= 1/(b_inc r^2 lambda')=tau/(r b_inc).

Lemma 4.7 therefore deterministically builds the labels, replacement forms, small shared summaries and group partitions. When a is below a sufficiently small fixed constant and n is sufficiently large the guards hold uniformly. Failed guards use exhaustive enumeration; outside this range the displayed exponential factor is already 2^Omega(n), after enlarging its constant. This makes a uniform algorithm, not only a statement about a favorable subsequence.

## 4. Counting and full arithmetic costs

Apply Proposition 3.4 to these factors in A. Since D_input=O_(k,b)(n), the Taylor perturbation order satisfies

    q_Taylor=floor(D_input R/Q)
             =O_(k,b)(n sqrt(a log(2/a))).

For q_Taylor<=N/2, the subset-pair cost has logarithm at most

    N[H2(q_Taylor/N)+q_Taylor/N]
      =O_(k,b)(n sqrt(a) [log(2/a)]^(3/2)).

The measurement enumeration and group sums cost exponent O(N/r)=O(n sqrt(a)). The high-incidence branches add n/sqrt(log n), which is absorbed because h>=nu+1. Other q_Taylor ranges are absorbed by increasing the constant.

Each factor has at most 2^k explicit coefficients. Evaluation requires polynomially many operations in d-dimensional cyclotomic vectors and truncated V and Taylor polynomials. All array dimensions are polynomial in L+n. The source row denominator (R-1)!Q! has polynomial bit length. Even the conservative common denominator obtained by raising it to O(km) has bit length polynomial in L+n. Input coefficient heights, multiplication of m factors, and all enumeration sums add only polynomially many bits. The retained-degree denominator gives a sharper bound but is not needed. Hermite reconstruction has polynomial dimension and rational bit cost, by the Appendix B argument applied in each coordinate. At T=0, sum the V-coefficients, reduce in the integral basis modulo 2^P and reconstruct centered coordinates. Traverse all branches and enumerations sequentially for polynomial space.

## 5. Raw arithmetic-program compiler and exact outputs

For a raw arithmetic circuit over F2 or Z/2^b with S gates and formal degree at most fixed k, compute the formal degree bottom-up, then propagate canonical Boolean multilinear polynomials. Addition combines coefficient dictionaries; multiplication forms pairs, takes the union of their variable supports (x_i^2=x_i on Boolean inputs), and combines coefficients modulo q. Each dictionary has at most sum_(j<=k) binom(n,j)=O_k(n^k) entries. A conservative bound is O(S n^(2k)) elementary coefficient operations, with polynomial space and index bit cost. This is paid before counting. The actual nonzero support m is discovered by execution of the compiler, not supplied as a free representation. If the discovered density is outside the theorem's favorable range, the algorithm reports that bound and may use exhaustive counting. A formal-degree promise is checkable syntactically; a claim of low semantic degree alone is not used.

For one output P(x) modulo q, its target counts follow from q fixed-order Fourier sums, including the binary formula above. For t=O(n) outputs P_i of formal degree at most k, introduce b*t Fourier-character bits, encoding lambda_i in Z/qZ. Then

    sum_(x,lambda) zeta^[sum_i lambda_i(P_i(x)-target_i)]
       = q^t * #{x: all P_i(x)=target_i}.

There are N=n+b*t=O(n) independent bits, no trace variables, degree at most k+1, and at most b times the total discovered monomial support plus O(bt) phase monomials. If this total is n^(1+o(1)), the original-input subexponential bound applies. Exact division by q^t recovers the original target count. Large S affects the explicit compilation cost; it does not enter the exponential counting parameter.

## 6. Exact diagonal-phase circuit amplitudes and marginals

For U=H^(tensor n) D H^(tensor n), with D the product of the supplied local diagonal phase gates, the amplitude at y is

    <y|U|0^n>=2^(-n) sum_x zeta^P(x) (-1)^(x dot y).

The extra phases are unary gates. Each requested amplitude is exact at the same cost; outputting all 2^n amplitudes still pays that output size.

For output positions A of size a0, complement B, and target z,

    Pr[Y_A=z]=2^(-(n+a0))
      sum_(x_B,x_A,x'_A) zeta^[P(x_A,x_B)-P(x'_A,x_B)]
                          (-1)^[z dot (x_A+x'_A)].

This follows by summing Fourier characters over the unspecified outputs, which forces the two B-input copies to agree. The sum has n+a0<=2n independent bits, at most 2m+2a0 local gates, and the same locality. Hence requested prefix probabilities also admit exact subexponential strong simulation. Sequential conditional sampling is a consequence only after implementing certified comparisons of fixed-degree algebraic probabilities with random dyadic thresholds; the executed companion does not claim an implemented fast sampler.

## Scope and scientific status

The construction combines a common divisibility filtration with source-manufactured summaries. It removes superlinear operation count from lifted degree and works at growing incidence m/n=n^o(1). It does not cover arbitrary programs, unrestricted quantum circuits, or dense degree-k polynomials with Theta(n^k) monomials. For those densities h/log n need not vanish. The consolidated report subsequently extends the IQP application to arbitrary Hadamard/diagonal alternation with O(n) Hadamards, and contains the targeted primary-source comparison; see also HADAMARD_EXTENSION_AUDIT.md. Results remain conditional on the supplied manuscript, with no historical-priority claim.

The finite companion checks use exhaustive assignments with exact integer arithmetic to validate truncation, reconstruction and Fourier marginal identities. They are not executions of the asymptotic replacement solver and establish no practical speed advantage.

## Optional uniform locality and phase-order range

For explicitly given phase gates, the same argument can retain the dependence on k and d rather than treating them as fixed. Put c=k*d and

    h=ceil(log2(2+km/n))+nu+1,       a_uniform=c^2*h/lambda.

Use r=floor(a_uniform^(-1/2)), with the same Q, tau and spectral-tail construction. Since a_uniform->0 implies c<=sqrt(lambda/h), all arithmetic dimensions are polynomial in n and the explicit description; in particular d<=sqrt(lambda). Also log r<=O(nu), A0=O(h), and

    D_input/N=O(c),
    q_Taylor/N=O(c*sqrt((h/lambda)log(2/a_uniform)))
               =O(sqrt(a_uniform log(2/a_uniform))).

The balance and bit-cost arguments are unchanged, with universal polynomial overhead in L+n+k+d. Thus the same form of runtime, now with a_uniform, is valid in the vanishing-a_uniform range. For constant phase order and m=n*polylog(n), this includes k=o(sqrt(log n/log log n)). For monomial phase gates their local evaluator has polynomial size in k; for arbitrary local truth tables the 2^k table length is already charged in L. This extension is a theorem for explicitly described phase gates. The raw arithmetic-program compiler has the separately stated n^(2k) work and n^k storage; its fixed-polynomial claim is only for fixed k and is not silently extended here.

Governing source: OpenAI, The Exponential Time Hypothesis is False, 25 October 2026, Definition 3.1, Proposition 3.4, Lemma 4.7 and Appendix B:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
