# Sharp finite reference dimension resource law

Research handoff dated 15 October 2026. Status: internally proved and independently reconstructed in exact arithmetic. External expert review and historical priority remain open. The proof is algebraic; the included scripts check specified identities and examples, rather than mechanically verify the general theorem.

## Definitions and comparison theorem

Fix integers m >= 2 and r >= 1. The classical symmetric measurement channel is

T_lambda(j|i) = lambda delta_ij + (1-lambda)/m,

where 0 <= lambda <= 1. Its quantum realization measures the input in the fixed m-symbol basis; it does not preserve input coherences. The erasure measurement E_q reveals symbol i with probability q and returns an erasure flag with probability 1-q. Its reveal effects are q|i><i| and its erasure effect is (1-q)I. Here q is the reveal probability, not the erasure probability.

An untouched quantum reference has dimension at most r. For faithful normalized states rho and sigma, define the standard Petz quantity Q2(rho||sigma) = Tr(rho^2 sigma^-1) and D2 = log Q2. E_q dominates T_lambda in reference-dimension-r Petz-D2 order when the output D2 under E_q is at least that under T_lambda for every such state pair with every allowed reference. The marginals rho_R and sigma_R need not coincide. Because both channels measure the classical input, it suffices to examine classical-quantum block-diagonal states; these states are separable. Entanglement is not required.

Put k = min(r,m-1). The exact threshold is

eta_(m,r)(lambda) = lambda^2 / [lambda + ((1-lambda)/m)(k+1)/k].

Then E_q dominates T_lambda if and only if q >= eta_(m,r)(lambda). The notation d in the proof below denotes this same k, and c_(m,r) denotes eta_(m,r). At lambda=0 the coefficient is 0; at lambda=1 it is 1.

For positive reference blocks R_i and Hermitian tangents H_i, write W=sum R_i, K=sum H_i and g_R(H)=Tr(H R^-1 H). Define the conditional input excess as sum_i g_(R_i)(H_i)-g_W(K), and similarly for the target blocks A_j=sum_i T_lambda(j|i)R_i and J_j=sum_i T_lambda(j|i)H_i. The coefficient is the supremum of target excess divided by positive input excess. It is not a multiplicative contraction coefficient for logarithmic D2, and it is not the ordinary tensor-with-identity coefficient without the reference contribution subtracted.

To see the erasure equivalence exactly, set sigma=direct_sum R_i and rho=sigma+t direct_sum H_i, normalized so Tr sigma=1 and sum Tr H_i=0. Then Q2(rho||sigma)=1+t^2 sum g_(R_i)(H_i), with no Taylor remainder. Erasure gives quadratic cost q sum g_(R_i)(H_i)+(1-q)g_W(K). Subtracting the target cost gives t^2 times [q input excess - target excess]. Monotonicity of log gives the same ordering for D2. Every faithful state pair yields such a Hermitian difference; conversely any trace-zero Hermitian tangent yields a faithful state pair for a sufficiently small nonzero t. The lower construction below already has trace zero. Thus the sharp excess constant is exactly the erasure-order threshold.

For m>=2, consider the classical m-symbol symmetric measurement channel T_lambda=lambda I+(1-lambda)J/m, let r>=1 be the allowed quantum reference dimension, and put d=min(r,m-1), mu=(1-lambda)/m. For 0<lambda<1 the sharp conditional RLD/standard-Petz chi-square excess contraction coefficient is

c_(m,r)(lambda) = lambda^2/[lambda+mu(d+1)/d]
                  = m d lambda^2/[m d lambda+(1-lambda)(d+1)].

Input state pairs may have unequal reference marginals. It is also the sharp coefficient for the operator-valued quadratic-defect inequality, with reference matrices of dimension at most r. The same supremum holds for reference dimension exactly r, using a harmless direct-sum extension. It equals the scalar threshold when r=1 and the unrestricted complete threshold once r>=m-1. This statement concerns conditional excess with the reference contribution subtracted, not the usual tensor-with-identity SDPI coefficient.

## 1. Rank-sensitive projection lemma

Let P be an orthogonal projection of rank r on a finite orthogonal direct sum H=direct_sum_i H_i. Write B=diag(P_ii) for its block pinching. Then

(I-P) B (I-P) <= r/(r+1) (I-P).

Proof. Fix a unit vector x in ker P, write x=(x_i), and put p_i=||x_i||^2. When p_i>0 let u_i=x_i/sqrt(p_i), viewed as a unit vector in H_i, and put q_i=<u_i,P_ii u_i>; put q_i=0 when p_i=0. We have sum p_i=1. The nonzero block-supported u_i are orthonormal, so sum q_i<=Tr P=r. Since P x=0 and ||x||=1, P<=I-xx*, hence q_i<=1-p_i. For any p,q>=0 with p+q<=1,

r^2 p+q-(r+1)^2 p q
=(r p-q)^2+(1-p-q)(r^2 p+q)>=0.

Therefore

<x,Bx>=sum p_i q_i
<= [r^2 sum p_i+sum q_i]/(r+1)^2
<=r/(r+1).

This proves the lemma without assumptions on block sizes or commutativity.

## 2. Dimension-sensitive zero-sum inverse lemma

Let R_i>0 be r-by-r matrices summing to I_r, and let z_i in C^r sum to zero. Then

sum z_i* R_i^-1 z_i >= (r+1)/r sum ||z_i||^2.

Proof. Define A:direct_sum_i C^r -> C^r by A(w)=sum_i sqrt(R_i)w_i. Then AA*=I_r, so P=A*A is an orthogonal projection of rank r, with diagonal blocks P_ii=R_i. Put w_i=R_i^-1/2 z_i. Since Aw=sum_i z_i=0, w belongs to ker P. Furthermore

E=||w||^2,   N=<w,diag(P_ii)w>.

The projection lemma immediately gives N<=r E/(r+1).

Combining this with the independent alphabet-size lemma E>=mN/(m-1), valid in any dimension, gives

E>= (d+1)N/d,   d=min(r,m-1).

The alphabet-size lemma can also be proved directly from inverse Cauchy: put D_0=sum z_i*R_i z_i and F=sum z_i*(I-R_i)^-1 z_i. Zero sum gives F<=(m-1)E, whereas ED_0>=N^2 and F(N-D_0)>=N^2. Adding D_0>=N^2/E and N-D_0>=N^2/[(m-1)E] yields the bound.

## 3. Sharp resolvent inequality

For any such zero-sum tuple, scalar spectral Jensen applied to the increasing concave function f(t)=t/(lambda+mu t) gives

lambda^2 sum z_i*(lambda R_i+mu I)^-1 z_i
<=lambda^2 E/[lambda+mu E/N]
<=c_(m,r)(lambda) E.

The N=0 case is trivial. Taking z_i=Z_i x for arbitrary x proves the same inequality in operator order for matrix tuples Z_i with sum Z_i=0.

## 4. Physical conditional RLD defects

With faithful baseline blocks R_i summing to I and Hermitian tangents H_i, put K=sum H_i and Z_i=H_i-R_i K. Then sum Z_i=0 and

sum H_i R_i^-1 H_i-K^2=sum Z_i*R_i^-1 Z_i.

For A_i=lambda R_i+mu I and J_i=lambda H_i+mu K,

sum J_i A_i^-1 J_i-K^2=lambda^2 sum Z_i*A_i^-1 Z_i.

Thus the coefficient in Section 3 bounds the operator-valued excess for physically admissible Hermitian tangents. Congruence handles arbitrary positive W=sum R_i; taking trace handles conditional RLD costs. Congruence and trace do not enlarge the reference dimension. In particular this argument distinguishes the operator directional inequality from the scalar trace inequality while proving the same upper bound for both.

## 5. Hermitian trace attainment on d+1 active symbols

First take reference dimension d. Let n=d+1<=m, and choose n real regular simplex unit vectors v_i in C^d, satisfying <v_i,v_j>=-1/d for i!=j and sum P_i=(n/d)I with P_i=v_i v_i*. Let t=d/n. For active symbols i<=n put R_i^0=t P_i and H_i=h_i R_i^0, with real h_i not all equal, chosen to sum to zero. Set both blocks to zero for inactive symbols. Then sum R_i^0=I and all H_i are Hermitian. Put K=sum H_i and Z_i=H_i-R_i^0 K.

Every active Z_i has range in P_i, every inactive Z_i is zero, and sum Z_i=0. At least one Z_i is nonzero: otherwise v_i*K=h_i v_i* for every active i, making the nonorthogonal simplex vectors eigenvectors of a Hermitian K with unequal eigenvalues, impossible. Write N=sum Tr Z_i*Z_i>0.

The limiting input conditional excess is N/t. The limiting output excess is lambda^2 N/(lambda t+mu). Thus their ratio is exactly

lambda^2 t/(lambda t+mu)=c_(m,r)(lambda).

This is direct attainment in the closure of the trace problem by Hermitian tangents, with possibly nonzero reference tangent K. No conversion from arbitrary vectors or concentration/filtering is needed.

For faithful approximants use R_i(epsilon)=(R_i^0+epsilon I)/(1+m epsilon), epsilon>0, and keep H_i fixed. They still sum to I. Since every H_i is supported in R_i^0, the individual input quadratic costs have finite limits; output baselines stay uniformly positive since mu>0. Their reference baseline is fixed, and their reference tangent K is fixed. Therefore both conditional excesses converge to the values just computed. Since sum Tr H_i=t sum h_i=0, divide all baseline and tangent blocks by d and take a sufficiently small nonzero perturbation to obtain faithful normalized physical state pairs.

For exact reference dimension r>d, add an (r-d)-dimensional direct summand with any faithful POVM baseline and zero tangents, before normalizing the full trace. This summand contributes zero to both defects, preserving their ratio. Thus both exact-dimension and at-most-dimension suprema agree.

The operator coefficient cannot be smaller than this trace coefficient, while the operator upper bound is already established. Hence the two sharp coefficients agree. The simplex construction does not claim equality for every prescribed faithful reference marginal; the optimization permits arbitrary faithful baselines.

## Checks and scope

- r=1: c=m lambda^2/[2+(m-2)lambda].
- r>=m-1: c=lambda^2(m-1)/[1+(m-2)lambda].
- lambda=0: coefficient 0. lambda=1: coefficient 1.
- r=2,m=4,lambda=1/2: c=4/11, strictly between the scalar 1/3 and unrestricted 3/8.
- For fixed m>2 and 0<lambda<1 the coefficients strictly increase with r until r=m-1.
- The dimension-sensitive zero-sum lemma is exact, not a numerical conjecture. Numerical POVM searches are only optional checks.
- This is a mathematical derivation; no priority or literature-novelty claim has been verified.

## Attribution and exclusions

The scalar r=1 comparator m lambda^2/[2+(m-2)lambda] is established prior work: Gu and Polyanskiy, *Non-linear Log-Sobolev Inequalities for the Potts Semigroup and Applications to Reconstruction Problems*, Appendix A, Proposition 40, Eq. (231), https://people.lids.mit.edu/yp/homepage/data/nlsi_potts.pdf . The classical chi-square/KL contraction equivalence identifies the same ordinary comparator. Its derivation here is an exact reconstruction, not a novelty claim.

The conditional-erasure comparison framework is related to Hirche, George, Nuradha and Wilde, https://arxiv.org/html/2608.27171v1 . A focused primary-source comparison did not establish a predecessor for this exact reference-dimension formula; that limited finding does not establish priority. Existing Volcic machinery is not claimed as a contribution of this package and is not needed for this proof.

No assertion is made here about SLD formulas, sandwiched D2, quantum depolarizing channels that preserve coherences, capacities, or a civilization-scale breakthrough. In particular, imposing equal reference marginals changes the optimization and is outside the proved formula.
