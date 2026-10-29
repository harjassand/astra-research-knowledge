# Actual canonical thermal charge readouts from acquired annihilation defects

29 October 2026. This is a theorem for the unchanged finite canonical
Hamiltonian, conditional only on the explicit matrix/gap and finite-K gates
in the two companion proofs. It is not a full Gibbs-state sampler. The
ordinary harmonic/number-conserving Bogoliubov prediction is granted; the
operation here is an explicit error receiver for a bounded physical query.

## 1. Acquired input and the actual Gibbs energy/defect budgets

Use LOWER_OPERATOR_PROOF.md and TRIAL_NORMALIZATION.md. Thus T is a real
M-by-M PSD matrix, T1=0, with unique zero mode, acquired gap lambda>0 and
upper norm Lambda. U,beta>0, and the two conserved flavor populations both
equal K. No grand-canonical conditioning, occupation cutoff, many-body gap,
Gibbs matrix element, mixing assumption or sampled field is supplied.

Let d=M-1 and D=binomial(K+M-1,M-1). The exact canonical Hilbert dimension
is D^2. Write Etr=C sqrt(K)+Rup(K) for the acquired variational upper bound.
Let L_K be the exact lower constant (C3), retaining sum_j Y_j†Y_j. Define

`Eup=Etr+2 log(D)/beta`,

`Dexc=min(2K,Eup/lambda)`, `Bfast=Eup-L_K`.          (T1)

These are finite scalar acquisitions. For the ACTUAL state
rho=exp(-beta H)/Tr exp(-beta H), entropy is at most 2log D, and the
Gibbs variational principle gives

`Tr rho H<=Eup`, `Tr rho Nexc<=Dexc`,

`Tr rho sum_j Y_j†Y_j<=Bfast`.                     (T2)

The last implication uses the retained global operator inequality, not a
trial-to-Gibbs state comparison. Exact normalization of rho is never used
as an oracle. At fixed M,U,beta and positive gap, Etr=C sqrt(K)+O(1),
L_K=C sqrt(K)+O(1), and Bfast=O(log K).

## 2. A finite-sector one-body fluctuation bound

For any Hermitian one-particle matrix C0 with ||C0||<=c, put c00=u^T C0 u.
On the two K-particle sectors let

`G_C=dGamma_b(C0)+dGamma_c(C0)-2K c00 I`.

If a state has mean depletion at most Dexc, then

`||G_C||_rho<=5 c sqrt[2K(Dexc+1)]`.               (T3)

Here ||A||_rho=(Tr rho A†A)^(1/2); no commutation between rho and A is
required. To prove (T3), split C0 into its u/Q diagonal and offdiagonal
blocks. The Q number term has norm at most 2c Nexc, hence GNS norm at most
2c sqrt(2K Dexc). For w=QC0u, ||w||<=c, the remaining term is A+A†,
where A=b0†b(w)+c0†c(w). The operator Cauchy inequality and the exact
bosonic number identities give

`||A||_rho<=c sqrt[2(K+1)Dexc]`,

`||A†||_rho<=c sqrt[2K(Dexc+2)]`.

Each is at most c sqrt[4K(Dexc+1)]. Thus the sum is bounded by
(2+2sqrt(2))c sqrt[2K(Dexc+1)]<5c sqrt[2K(Dexc+1)].
This pays the otherwise unbounded one-body operator using the fixed
canonical charge and the actual thermal depletion budget.

## 3. Exact mixed commutators and their finite-K error

Let e_j be the real orthonormal eigenvectors used in the lower proof,
T e_j=t_j e_j. The commuting charge modes are Q_j=sum_i e_j(i)q_i.
For any l,j, define the single-particle matrix

`C_lj=u(e_l e_j)^T+(e_l e_j)u^T`

`       -(e_l e_j^T+e_j e_l^T)/sqrt(M)`.

The product e_l e_j is pointwise. Direct commutation yields

`i[Q_l,J-j]=dGamma_b(C_lj)+dGamma_c(C_lj)`.

In particular ||C_lj||<=2 (commutator of two matrices of norm at most1)
and u^T C_lj u=2 delta_lj/sqrt(M). Therefore (T3) implies the convenient
conservative bound

`||i[Q_l,J-j]-4K delta_lj/sqrt(M)||_rho`

`<=16 sqrt[K(Dexc+1)]`.                           (T4)

For a real vector t in R^d set

`qtilde_j=Q_j/K^(1/4)`, `Jtilde_j=J-j/K^(3/4)`,

`F_t=exp(i sum_j t_j qtilde_j)`, `chi(t)=Tr rho F_t`.

The unitary F_t is a product of number-conserving onsite phase rotations,
with opposite signs on the two flavors. Conjugating C_lj by any fraction
of F_t changes its one-particle matrix by at most 4|t|/K^(1/4), since
||diag(E t)||<=|t|. Its two-flavor second quantization changes by at most
8K^(3/4)|t| in operator norm. The exact Duhamel commutator formula and
(T4) consequently give, for every j,

`|Tr rho[Jtilde_j,F_t]+(4/sqrt(M))t_j chi(t)|`

`<=sqrt(d)|t|[16 sqrt((Dexc+1)/K)+8 K^(-1/4)|t|]`. (T5)

To see the ordering explicitly, the Duhamel integrand is
F_t exp(-is T_t) C_lj exp(is T_t), where
T_t=sum t_l Q_l/K^(1/4). Its expectation is bounded by the GNS norm of
C_lj's centered second quantization plus the displayed OPERATOR-norm
conjugation error. Thus (T5) does not assume that rho is invariant under
these phase rotations. We kept the loose constant8 instead of gaining
the integral of s.

## 4. Stein identity with an acquired finite-K Gaussian coefficient

Write a=(1-epsilon)/(8K+4) as in the lower proof, and set

`b_j=sqrt(aK t_j)`, `bmax=sqrt(aK Lambda)`,

`A_j=Y_j/K^(1/4)=sqrt(U)qtilde_j-i b_j Jtilde_j`,

`Sigma_K=diag[2b_j/sqrt(UM)]`.                     (T6)

These are native matrix functions. The limiting covariance is
Sigma_infty=diag sqrt[t_j/(2UM)]; the displayed Sigma_K is used in the
finite-K bound and does not claim to equal the exact unbounded thermal
covariance. The exact algebra is

`A_j†F_t+F_t A_j=2sqrt(U)qtilde_j F_t+i b_j[Jtilde_j,F_t]`.

Both expectations on the left are bounded by ||A_j||_rho, using GNS
Cauchy with the unitary F_t. By (T2), sum ||A_j||_rho^2<=Bfast/sqrt(K).
Combining with (T5) yields an approximate Gaussian Stein equation

`partial_j chi(t)+(Sigma_K t)_j chi(t)=r_j(t)`,

with the VECTOR bound

`|r(t)|<=sqrt(Bfast)/(sqrt(U)K^(1/4))`

` +(d bmax/(2sqrt(U)))|t|`

`       *[16sqrt((Dexc+1)/K)+8K^(-1/4)|t|]`.        (T7)

This calculation uses only exact finite-sector commutators and the actual
Gibbs energy/entropy budget. There is no Gaussian closure assumption.

## 5. A complete bounded-query receiver

Integrate the scalar radial equation for chi(s t), starting at chi(0)=1.
The Gaussian integrating factor is nonexpansive in the final variation-
of-constants formula. Hence for EVERY real query vector t,

`|chi(t)-exp(-t^T Sigma_K t/2)|<=min(2,Err_K(t))`,

`Err_K(t)= |t| sqrt(Bfast)/(sqrt(U)K^(1/4))`

` +(d bmax/(2sqrt(U)))|t|^2`

`    *[8sqrt((Dexc+1)/K)+(8/3)K^(-1/4)|t|]`.        (T8)

At fixed M,gap,U,beta and bounded query norm this tends to zero at most
O(K^(-1/4)sqrt(log K)), with fully explicit finite-K constants in (N1)--
(N8),(C3),(T1). It proves the K^(1/4) SCALE in this bounded weak sense.
It does NOT infer convergence of unbounded second moments from weak/TV
information. The general depletion/energy budgets remain separately valid.

For example, the native positive two-outcome instrument has conditional
success probability [1+cos(sum_j t_j Q_j/K^(1/4))]/2. Its actual canonical
success probability is [1+Re chi(t)]/2. The positive proxy law uses

`p_proxy=[1+exp(-t^T Sigma_K t/2)]/2`.

Its binary TV error is at most Err_K(t)/2, plus any declared interval/
rational probability rounding. Sine queries are controlled similarly, with
proxy1/2. Select a finite query from a known distribution FIRST and then
emit its binary outcome: the joint finite-output TV error is at most the
known weighted sum of these bounds. No independent Gaussian oscillator,
continuous-velocity TV approximation or uncharged phase-space cutoff is
needed to produce this normalized finite law. Computing the probability
and sampling an ideal rational approximation are distinct costs; ordinary
fair-bit Bernoulli sampling can pay the latter after outward rounding.

This is a computational readout distribution for the original Hamiltonian;
it does not acquire physical control for implementing the detector in a
laboratory. Complex exponentials are used only as bounded mathematical
observables. Canonical ED, number-conserving harmonic methods and tensors
receive these SAME input/query contracts.

## 6. Normalizer and honest many-mode limits

The free energy is acquired only in the interval

`L_K-2log(D)/beta <= -log(Z_K)/beta <= Etr`.         (T9)

Its width is O(log K) at fixed M; a fixed-relative partition function,
trace-norm approximation to the whole Gibbs state, or full occupation
sampler has NOT been constructed. Those cannot be inferred from (T8).

All-M operation requires evaluating the actual T, gap, square roots and
pseudoinverse with certified errors. For the bounded-range frustrated
family lambda can shrink as M^(-2), and the constants and usable K grow
accordingly. The theorem can qualify a joint M,K sequence by its explicit
gates; it does not assert accuracy at K=rho M, a stable positive-density
ordered phase, practical speedup over a matched harmonic/tensor algorithm,
or historical priority. The consequence is a paid, nonperturbative-in-U
collective canonical READOUT description in a high-occupation regime, not
a solution of general frustrated matter.
