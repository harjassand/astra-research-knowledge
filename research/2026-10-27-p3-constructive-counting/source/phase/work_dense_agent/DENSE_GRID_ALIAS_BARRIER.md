# Dense incidence and the replicated-input rank barrier

27 October 2026. Conditional analysis of the replacement mechanism in Sections 3--5 of the governing ETH manuscript. This is a limitation of a specific natural extension, not a lower bound for circuit counting.

## Attempted extension

For dense low-degree equations, both scope size and incidence can be linear in the original input count. One proposed repair is to use a single complete auxiliary array, put the same variable in all its factor incidences, and measure summary rank only after identifying these aliases. This eliminates multiple array copies and gives perfectly balanced groups. A short central spectral interval still has full original-input summary rank whenever f(0)!=1. The theorem below quantifies every spectral polynomial of the same form.

## Setup

Let r>=2, Q>=1 and n=r^Q. Variables have indices a in [r]^Q, factors have indices d in [r]^Q, and all factors read every variable. On the D=n^2 incidence coordinates define J by (Jx)_(a,d)=x_a. Let Pi_i exchange a_i and d_i. Set W=(1/2)sum_i(I-Pi_i), V=product_i Pi_i, and let E_j project orthogonally onto W=j. On E_j, V=(-1)^j. For deg f<=R-1 let M=V f(W), B=I-M. Let C be any matrix with ker C contained in ker B, as in the source.

## Exact alias-aware rank theorem

Let j0 be the least j in {0,...,Q} with f(j)!=(-1)^j, or Q+1 if none exists. Then

    rank(BJ) = sum_(s=j0)^Q binom(Q,s)(r-1)^s,
    rank(CJ) >= rank(BJ).

If R<=Q, necessarily j0<=R, and therefore

    rank(CJ) >= sum_(s=R)^Q binom(Q,s)(r-1)^s.

The degree-R-1 polynomial interpolating parity at 0,...,R-1 attains equality when C consists of exceptional spectral rows. This is sharp within the spectral-polynomial family.

### Proof

Work over the reals for orthogonality; rational matrices have the same rank over Q and R. Split H=R^r as span(1) orthogonally summed with the zero-sum subspace U. For S subset [Q], let H_S have U in its coordinates in S and span(1) elsewhere. The original input space is the orthogonal direct sum of H_S, of dimensions (r-1)^|S|.

In one coordinate, replication sends v to v tensor 1. Its symmetric and antisymmetric projections are A_+(v)=(v tensor 1+1 tensor v)/2 and A_-(v)=(v tensor 1-1 tensor v)/2. Both maps are injective on U: their squared norms there equal (r/2)||v||^2. On span(1), A_- vanishes and A_+ is injective. U-dependent images are orthogonal to 1 tensor 1.

Consequently E_j J vanishes on H_S when |S|<j. When |S|>=j it is a sum of mutually orthogonal injective tensor-product maps, one per choice of j antisymmetric coordinates in S, and hence is injective on H_S. Images for different S are orthogonal because in a coordinate of their symmetric difference one has a U-dependent factor orthogonal to constants and the other has a constant factor. Thus

    ker(E_j J) = direct sum_(|S|<j) H_S.

Since BJ=sum_j[1-(-1)^j f(j)] E_j J and the spectral output spaces are orthogonal, its kernel is the intersection of these nested kernels over exceptional j. It is exactly the kernel for the least exceptional j0, proving the formula. Since ker(CJ) is contained in ker(BJ), the summary lower bound follows.

If j0>R, f matches parity at 0,...,R. The R-th finite difference of parity is (-2)^R, whereas a degree-R-1 polynomial has zero R-th finite difference. Contradiction. Interpolating the first R values gives j0=R by this same argument.

## Implications

Whenever f(0)!=1, rank(CJ)=n: the excluded fully symmetric spectral space alone determines every input. Including additional low eigenvalues can repair this exact issue but cannot provide an asymptotic saving: the sharp lower bound is

    rank(CJ)/n >= Pr[Bin(Q,1-1/r)>=R].

If R/Q tends to zero, the fraction tends to one. If R<=(1-1/r-delta)Q with fixed delta>0, it is at least 1-exp(-2delta^2 Q). A vanishing rank fraction therefore requires R/Q>=1-1/r-o(1), whereas the source reconstruction with lifted degree Theta(n) needs R/Q to vanish. Small rank relative to the ambient incidence dimension n^2 is insufficient.

## Signed and weighted aliases do not repair the complete grid

Replace J by J_w with (J_w x)_(a,d)=w_(a,d) x_a, where every w_(a,d) is a nonzero rational number. The original incidence input can be recovered by dividing its row by this weight. For every j,

    rank(E_j J_w) >= sum_(s=j)^Q binom(Q,s)(r-1)^s.

To prove this, choose a base symbol 0 in [r]. For any a with at least j nonzero coordinates choose j such coordinates S, and set d=a outside S and d=0 on S. The two indices differ in exactly S. At the output row (a,d), the projector E_j reduces to 2^(-j) times the alternating sum over the j-dimensional swap cube: antisymmetry in any coordinate outside S vanishes, so the only surviving choice of j antisymmetric coordinates is S itself. Its coefficient on x_a is 2^(-j) w_(a,d), which is nonzero. Every other variable in that row has strictly fewer nonzero coordinates. Consequently E_j J_w x=0 recursively determines every x_a with support size at least j from the variables with support size less than j. The latter number is sum_(s<j) binom(Q,s)(r-1)^s, proving the nullity bound.

If j0 is any exceptional spectral level, ker(BJ_w) is contained in ker(E_j0 J_w), because different spectral outputs are orthogonal. Taking the least exceptional level and using j0<=R gives

    rank(CJ_w) >= rank(BJ_w)
                  >= sum_(s=R)^Q binom(Q,s)(r-1)^s.

Thus arbitrary signs and nonzero scales cannot improve the sharp unweighted lower bound. In the particularly relevant case f(0)!=1, the diagonal rows (a,a) immediately certify rank n, since all swaps fix those rows and their entries are w_(a,a)x_a.

This does not exclude a nonspectral representation, incomplete incidence grids with purposefully reused summaries, transformations of the equations, output-specific cancellation, or unrelated algorithms. Dense linear systems and individual quadratic exponential sums have specialized efficient algorithms. No hardness claim or historical-priority claim is made for the elementary ingredients.

## Checks and source

The accompanying Python script constructs 2^Q E_j J directly from swap expansions and Krawtchouk coefficients. Exact modular ranks attain the proved rational upper ranks, certifying equality for the recorded cases. These are implementation checks; the proof is the general justification.

Governing manuscript: OpenAI, The Exponential Time Hypothesis is False, 25 October 2026, Sections 4.1--4.3 and Proposition 5.3:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
