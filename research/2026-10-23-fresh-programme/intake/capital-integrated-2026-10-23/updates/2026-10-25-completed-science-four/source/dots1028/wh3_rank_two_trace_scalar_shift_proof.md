# Rank-two WH3 trace comparison via a scalar-shift variational argument

Status: complete proof, independently cross-checked with the root derivation on 2026-10-24. No numerical premise. The root independently supplied the shorter quadratic sum-of-squares identity below.

## The target

Let N=W3 tensor id_R, where W3(X)=(Tr(X)I3-X^T)/2. For every Hermitian X of rank at most two,

2||N(X)||_1 >= ||X||_1+||X_R||_1.

The proof below is dimension-independent in R. Its physical co-reduction/Gram identification uses A dimension THREE; do not extend that identification to W_d for d>3, whose skew Kraus environment has dimension d(d-1)/2.

## 1. A universal scalar quadratic shift

For every complex square matrix T, there is z in C such that, with U=T+zI and F=Tr(T*T),

UU*+T*T <= F I,
U*U+TT* <= F I.

These two left sides are identical: TT*+T*T+conj(z)T+zT*+|z|^2 I.

To prove existence, minimize its largest eigenvalue over z. The variational characterization of the largest eigenvalue and convex minimax give

min_z max_density rho [Tr rho(TT*+T*T)+2Re(conj(z)Tr rho T)+|z|^2]
= max_density rho [Tr rho(TT*+T*T)-|Tr rho T|^2].

The minimax exchange is legitimate on a compact disk: all centers -Tr(rho T) lie in the disk of radius ||T||op, and projecting z into that disk decreases every displayed quadratic. The density-matrix set is compact convex, and the objective is convex in z and affine in rho.

It remains to bound the right side by F. Diagonalize rho=diag(p_i), put u_i=sqrt(p_i), P=I-uu*, and D0=diag(T_ii). The exact deficit is

F-Tr rho(TT*+T*T)+|Tr rho T|^2
= sum_{i!=j}(1-p_i-p_j)|T_ij|^2 + ||P D0 P||_F^2 >=0.

Here ||P D0 P||_F^2=sum_i(1-2p_i)|T_ii|^2+|sum_i p_i T_ii|^2. This completes the shortest proof. For an independent alternate verification of the diagonal part: each off-diagonal |T_ij|^2 has coefficient p_i+p_j<=1. For the diagonal entries a_i=T_ii, the needed inequality is

sum_i 2p_i |a_i|^2-|sum_i p_i a_i|^2 <= sum_i |a_i|^2,

i.e. diag(1-2p)+pp* >=0.

If every p_i<=1/2, this is immediate. Otherwise p_1>1/2 and q=sum_{i>1}p_i=1-p_1<1/2. Minimizing the quadratic form over a_i, i>1, or taking a Schur complement, reduces positivity to

p_1^2/[1+sum_{i>1} p_i^2/(1-2p_i)] >= 2p_1-1.

Since x/(1-2x) is increasing on [0,1/2),

sum_{i>1}p_i^2/(1-2p_i) <= q^2/(1-2q).

The resulting denominator is p_1^2/(2p_1-1), proving the claim. This also covers complex a_i; zero probabilities cause no difficulty.

## 2. The square-root shift consequence

Let T be d by d, set S_L=sqrt(I+TT*), S_R=sqrt(I+T*T), and s=Tr S_L=Tr S_R. The z from Section1 satisfies

sqrt(I+UU*)+S_R <= [s-(d-2)] I,
sqrt(I+U*U)+S_L <= [s-(d-2)] I.

Indeed let t_i be the singular values of T and a_i=sqrt(1+t_i^2)-1>=0. The i-th eigenvalue of D_R=[s-(d-2)]I-S_R is

1+sum_{j!=i}a_j >=1.

Moreover

(D_R^2-I)_i - (F I-T*T)_i
=2 sum_{j<k; j,k!=i}a_j a_k >=0.

Therefore UU*<=F I-T*T<=D_R^2-I. Operator monotonicity of the square root gives sqrt(I+UU*)<=D_R. The adjoint version follows identically.

## 3. Exact variational formula for the signed fidelity

For a PSD block matrix H=[[A,C],[C*,B]], define Z=diag(I_d,-I_d) and

f_Z(H)=Tr|sqrt(H) Z sqrt(H)|=F_root(H,ZHZ).

Then

f_Z(H)=inf_T {Tr[A sqrt(I+TT*)]+Tr[B sqrt(I+T*T)]+2Re Tr(C*T)}.

For faithful H, use the standard fidelity variational formula

F_root(H,ZHZ)=inf_{S>0} (Tr HS+Tr ZHZ S^{-1})/2.

This variational formula itself has an elementary proof: set K=H^(1/2) S H^(1/2) and Q=H^(1/2)(ZHZ)H^(1/2). Then TrK+Tr(Q K^(-1))-2Tr sqrt(Q)=||K^(1/2)-K^(-1/2)sqrt(Q)||_F^2>=0, with equality exactly K=sqrt(Q). Its unique minimizing S therefore satisfies SHS=ZHZ. Uniqueness applied to the inverse problem implies ZSZ=S^{-1}, or SZS=Z. Every positive S with this property has the form

S(T)=[[sqrt(I+TT*),T],[T*,sqrt(I+T*T)]].

Conversely every such S(T) is positive and satisfies SZS=Z. Its variational objective is Tr H S(T), giving the formula. Boundary H follows by continuity (or approximation in the application below).

## 4. A block-coherence theorem

Suppose H>=0, Tr A=lambda, Tr B=mu, and Tr C=0. Put

Y=[[mu I-B,C],[C*,lambda I-A]].

Assume Y>=0. (This positivity is automatic for the Gram/co-reduction application.) Then

f_Z(Y) >= f_Z(H)+(d-2)(lambda+mu).

Proof: fix any T in the variational objective for Y and choose U=T+zI from Section2. The cross term is unchanged because Tr C=0. The two square-root bounds imply

objective_H(U)
<= (lambda+mu)[s-(d-2)]-Tr(A S_R)-Tr(B S_L)+2Re Tr(C*T)
= objective_Y(T)-(d-2)(lambda+mu).

Since f_Z(H)<=objective_H(U), taking the infimum over T proves the assertion. Faithful regularization preserving the diagonal logical marginal handles all boundaries. In fact Y is the global-transpose/spin-flip image of physical co-reduction of H, so it is PSD whenever H>=0 with the stated marginal.

## 5. Exact physical WH3 Gram transfer

It suffices to consider X=lambda psi psi* - mu phi phi*, lambda,mu>0, with normalized orthogonal psi,phi. The semidefinite cases are immediate.

Let G be the six-dimensional Gram matrix of the R-valued physical rows of psi and phi, ordered (physical index, logical index). Then G>=0 and Tr_A G=I2. With cyclic skew Kraus K_k satisfying

K_k* K_l=(delta_kl I-|l><k|)/2,

the Gram matrix of the six output vectors K_k psi,K_k phi is (I6-G^{Gamma_A})/2.

Let D=diag(lambda,mu), H=(I3 tensor sqrt(D))G(I3 tensor sqrt(D)), and Z=I3 tensor diag(1,-1). Signed-Gram nonzero-spectrum equivalence gives

||X_R||_1=f_Z(H),
2||N(X)||_1=f_Z(I3 tensor D-H^{Gamma_A}),
||X||_1=lambda+mu.

Full transpose followed by conjugation with I3 tensor sigma_y sends I3 tensor D-H^{Gamma_A} to

H+I3 tensor D_swap-(Tr_L H) tensor I2,

which, in logical-block ordering, is exactly Y from Section4. The identity used is sigma_y Q^T sigma_y=(Tr Q)I2-Q, applied to every physical block. f_Z is invariant under full transpose and under this conjugation, because sigma_y Z sigma_y=-Z.

Section4 with d=3 therefore proves

2||N(X)||_1 >= ||X_R||_1+lambda+mu.

## Consequences and scope

On every fixed logical two-dimensional code V, N_V trace-dominates F_V=(id logical directsum M_V)/2 on every Hermitian logical operator. Frenkel's positive integral formula for Umegaki relative entropy then implies the ordinary comparison

2D(N_V rho||N_V sigma) >= D(rho||sigma)+D(M_V rho||M_V sigma).

Faithful Taylor expansion gives the ordinary BKM comparison, and Bregman integration gives the corresponding ordinary entropy convexity statement on that code. No auxiliary logical/reference amplification is asserted: a general amplified Hermitian input need not have rank at most two. This proof does not construct a positive decoder, CPTP two-state decoder, or fixed complete signed Gram lift.

Primary external ingredient for the entropy transfer: Frenkel2023, https://arxiv.org/html/2208.12194 , Equation(1). The scalar-shift and block variational derivation above are provided explicitly for independent checking; no historical novelty claim is made.

Final qualification: the argument does not by itself imply ordinary SLD comparison. The previously used complete SLD-to-BKM bridge cannot be reversed at this unamplified level.

## Why the scalar centering lemma cannot be blindly operator-amplified

A natural but false extension replaces the scalar z by an operator on an auxiliary factor and the scalar Frobenius budget by a partial trace:

(T+I_A tensor Z)(T+I_A tensor Z)*+T*T <= I_A tensor Tr_A(T*T).

Take A=E=C3 and T=P_Phi, the normalized maximally-entangled rank-one projector. The expectation of the left side in Phi is

2+(2/3)ReTrZ+(1/3)TrZZ*
=1+(1/3)||Z+I3||_F^2 >=1.

The right side is I_A tensor I_E/3 and has expectation 1/3. No Z can satisfy this proposed extension. This is an obstruction to that operator-valued centering construction only. It is neither a counterexample to an amplified channel comparison nor an entropy counterexample.
