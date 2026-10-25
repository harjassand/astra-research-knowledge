# WH3 mutual-information half bound: rank-two states and all qubit references

Status: proved, independently checked on 2026-10-24. Dependency: the ordinary rank-two trace/Frenkel theorem in wh3_rank_two_trace_scalar_shift_proof.md. No complete comparison or fixed score lift is assumed.

Let W3(X)=(Tr(X)I3-X^T)/2 and N=W3 tensor id_R. All logarithms are natural. Define

F(rho_AR)=S(rho_AR)-2S(N rho_AR)+S(rho_R),
f(a)=S(a)-2S(W3(a)).

We prove:

1. f is concave on all qutrit density matrices.
2. For every rho_AR of rank at most two, with arbitrary finite R,
   I(B:R)_(N rho) <= (1/2) I(A:R)_rho.
3. The same inequality holds for EVERY rho_AR with dim R<=2, with no rank restriction on rho_AR.

All these states also obey 2S(N rho)-S(rho)-S(rho_R)>=ln3.

## 1. Scalar marginal concavity, including noncommuting directions

The eigenvalues of W3(a) are (1-p_i)/2 when the eigenvalues of a are p_i. Hence

f(a)=sum_i g(p_i),
g(p)=-p ln p+(1-p)ln((1-p)/2).

In the interior,

g'(p)=ln2-2-ln[p(1-p)],
g''(p)=(2p-1)/[p(1-p)].

For a Hermitian trace-zero tangent H in an eigenbasis of a, the spectral Hessian is

sum_i g''(p_i)|H_ii|^2
+2 sum_{i<j} [(g'(p_i)-g'(p_j))/(p_i-p_j)] |H_ij|^2,

using the continuous divided difference at repeated eigenvalues.

Every off-diagonal coefficient is nonpositive. Indeed, for p_i>p_j, the condition p_i+p_j<=1 gives p_i(1-p_i)>=p_j(1-p_j), and therefore g'(p_i)<=g'(p_j).

If all p_i<=1/2, all diagonal coefficients are nonpositive as well. Otherwise exactly one p_1>1/2. Set q=1-p_1<1/2 and

h(x)=x(1-x)/(1-2x), 0<=x<1/2.

The ratio h(x)/x=(1-x)/(1-2x) is increasing, so sum_{i>1}h(p_i)<=h(q). Weighted Cauchy-Schwarz and sum H_ii=0 give

|H_11|^2 <= [sum_{i>1}h(p_i)] [sum_{i>1}|H_ii|^2/h(p_i)]
<= h(q) sum_{i>1}|H_ii|^2/h(p_i).

Since g''(p_1)=1/h(q), while g''(p_i)=-1/h(p_i) for i>1, the diagonal Hessian is nonpositive. Therefore f is concave in the faithful interior; entropy continuity extends concavity to the closed state space.

Unitary invariance and concavity imply f(a)<=f(I3/3)=-ln3, by averaging unitary conjugates of a.

## 2. Rank-two states

For each two-dimensional code V, the proven ordinary relative-entropy comparison is

2D(N_V rho||N_V sigma) >= D(rho||sigma)+D(M_V rho||M_V sigma),

where M_V=Tr_A composed with V. Its BKM Hessian form says that F is convex on this logical state space. Faithful interior convexity extends to the closed logical state space by continuity.

Let rho_AR=sum_i w_i |psi_i><psi_i| have rank at most two. Its spectral vectors lie in one such code, hence

F(rho_AR)<=sum_i w_i F(psi_i).

For a pure psi_AR, apply the antisymmetric Stinespring isometry A3 -> B3 tensor C3 for W3. The B and C channels agree up to the fixed harmless output basis convention, so

S(N psi_AR)=S(W3(psi_A)),
S(psi_R)=S(psi_A).

Consequently F(psi_AR)=f(psi_A). Concavity from Section1 yields

F(rho_AR)<=sum_i w_i f(psi_i,A)<=f(rho_A).

The exact information identity is

2I(B:R)_(N rho)-I(A:R)_rho = F(rho_AR)-f(rho_A).

This proves the MI-half claim. Since f(rho_A)<=-ln3, it also proves the absolute entropy target on all rank-at-most-two states.

## 3. All qubit references by purification duality

Take any rho_AR with dim R<=2 and purify it to psi_ARE. After the antisymmetric Stinespring isometry, the state Omega_BCRE is pure. Both marginal channels A->B and A->C are W3 up to a fixed unitary, so

I(B:C|R)_Omega=2S(BR)-S(R)-S(E)=-F(rho_AR),
I(B:C|E)_Omega=2S(BE)-S(E)-S(R)=-F(rho_AE).

Conditional-mutual-information purification duality therefore gives

F(rho_AR)=F(rho_AE).

This also follows immediately from the displayed entropy expressions and purity. The A marginal is the same in the two reduced states. Moreover rank rho_AE=rank rho_R<=2. Section2 applies to rho_AE, with E allowed to have any finite dimension, and gives

F(rho_AR)=F(rho_AE)<=f(rho_A).

Thus the full MI-half inequality and the absolute ln3 bound hold for every qubit-reference input, including high-rank states. This is an entropy duality argument, NOT an amplified two-dimensional-code metric comparison.

## Scope of the remaining problem

The unrestricted absolute WH3 entropy inequality and the stronger unrestricted MI-half conjecture remain distinct open targets. Any violation of either must have both rank rho_AR>=3 and rank rho_R>=3. Equivalently, in a minimal purification, both untouched systems R and E must have dimension at least three. A qutrit R and qutrit E are the first unclosed purification sector. This does not assert that every state in that sector is hard or violates either inequality.

## 4. Arbitrary classical flags with qubit reference blocks

The MI-half theorem also holds whenever the reference has a direct-sum decomposition R=directsum_j R_j with dim R_j<=2 and the input is block diagonal:

rho_AR=directsum_j p_j rho_(A R_j).

Let J denote the classical block label and a_j=Tr_(R_j)rho_(A R_j). The exact chain-rule decompositions are

I(A:R)=I(A:J)+sum_j p_j I(A:R_j)_(rho_j),
I(B:R)=I(B:J)+sum_j p_j I(B:R_j)_(N rho_j).

Concavity of f gives the ordinary classical-reference inequality directly:

2 I(B:J)-I(A:J)
= sum_j p_j f(a_j)-f(sum_j p_j a_j) <=0.

Every conditional qubit block satisfies the MI-half bound proved above. Adding these inequalities proves I(B:R)<=I(A:R)/2, regardless of the number of classical blocks or total reference dimension. The absolute ln3 bound follows as before.

The same conclusion permits multiplicity factors uncorrelated with A within each block, i.e. blocks rho_(A R_j) tensor tau_(K_j). Such factors contribute no conditional mutual information and can be discarded for this calculation.

This is a direct-sum statement, NOT a tensor-product statement. A tensor product of two qubit memories is an irreducible four-dimensional quantum memory and is not covered merely because each tensor factor is a qubit. Conditioning on a quantum subsystem does not turn the classical chain-rule proof into such an extension.

Accordingly a remaining violation requires an irreducible reference sector of dimension at least three, rather than merely a reference Hilbert space of total dimension at least three.
