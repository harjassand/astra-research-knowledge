# Ledger audit and a positive-rank isotypic bound

5 November 2026. This audit uses the exact general ledger in `joint_root/general_acquisition_ledger.md`. It does not evaluate its optimum over memory width.

## 1. Audit conclusions and a short decoder-bound proof

The average-state factorization N_j(I/2)=I_S/2⊗sigma_j is exact, including each classical-history block: the next source and fresh carrier are jointly tracial on this average input, their collision changes nothing, and receiver processing acts only on memory and carrier. Supported logical Pauli images remain in the support of the average state by channel positivity.

The balanced discriminant V_j is a Hilbert-Schmidt contraction by the sandwiched order-two data-processing inequality. For a direct second-variation proof, first use traceless supported Hermitian perturbations omega+tA; the constant and linear terms cancel under the trace-preserving map. Add the component proportional to omega, which is orthogonal in the balanced metric, and split general matrices into Hermitian and anti-Hermitian parts. Since the physical receiver acts trivially on S, the source identity and traceless sectors contract separately. The collision split and the Petz entanglement-fidelity normalization in the root ledger are correct.

The final-decoder lower-error inequality also has an elementary proof. For the attained memory channel E with average sigma, set

\[
y_\mu=\sigma^{-1/4}E(\sigma_\mu/2)\sigma^{-1/4},\qquad
z_\mu=\sigma^{1/4}D^*(\sigma_\mu)\sigma^{1/4}.
\]

For any CPTP decoder D,

\[
F_e(DE)=\frac14+\frac14\sum_{\mu=1}^3\langle z_\mu,y_\mu\rangle.
\]

For Hermitian B=D^*(sigma_mu), Kadison gives B^2<=I, and

\[
\|\sigma^{1/4}B\sigma^{1/4}\|_2^2
\le\operatorname{Tr}(\sigma B^2)\le1.
\]

The first inequality follows from Tr(sigma B^2)-Tr(sqrt(sigma)B sqrt(sigma)B)=||[sqrt(sigma),B]||_2^2/2. Hence Cauchy-Schwarz and sum||y_mu||²=3a give F_e<=(1+3sqrt(a))/4. Half-diamond error is at least 1-F_e, establishing epsilon>=(3/4)(1-sqrt(a)) without invoking a separate comparison theorem.

**Refinement correction.** For an unrefined actual receiver, the positive-effect witness made by revealing all hidden Kraus labels satisfies

\[
\operatorname{Tr}(H_nZ_{\rm refined})\le\frac34\sum_{j\le n}(\ell_j^P+\ell_j^Q).
\tag{A}
\]

Equality holds for a fully Kraus-refined receiver. Revealing labels increases the balanced squared norm by data processing and can only improve Petz fidelity. The root's lower bound on cumulative loss remains valid after replacing its original equality by (A).

The root's quantum-retention-time corollary also checks: a classical branch with effect E_x contributes Tr(E_x²)/(4Tr E_x)<=p_x/2, p_x=Tr E_x/2. The occupancy bound is nonvacuous when C_epsilon=4epsilon-8epsilon²/3<1, equivalently epsilon<(3-sqrt(3))/4. Its qubit-time conclusion does not imply a peak-width law.

## 2. Exact rank-sensitive isotypic lemma

At prefix n let d=2^n, let H_n=I-T_nT_n^*, and let P_inv be collective SU(2) twirling on bath operators. Write

\[
(\mathbb C^2)^{\otimes n}=\bigoplus_j\mathbb C^{r_j}\otimes\mathbb C^{d_j},\qquad
d_j=2j+1,\qquad w_j=r_jd_j/d.
\]

Let beta_n(theta)>0 denote the smallest eigenvalue of H_n restricted to the nontrivial SU(2) operator sectors, i.e. the complement of P_inv. This is distinct from the full gap, which has fourth-order scalar directions at fixed n>=2.

For ANY Kraus-refined prefix instrument of retained branch dimension at most m, put A_x=sqrt(K_x^dagger K_x)>=0. Then rank(A_x)<=m and sum_x A_x²=I, including initialized workspace and all history in the prefix instrument. Define

\[
D_n(m)=\sum_jw_j\left(1-\frac{m}{d_j}\right)_+.
\]

**Lemma.** Its positive witness obeys

\[
\boxed{\operatorname{Tr}(H_nZ)\ge\beta_n(\theta)D_n(m).}
\tag{B}
\]

This is an exact finite-angle statement with a spectrally defined beta_n; it does not assume a uniform asymptotic formula for that quantity.

**Proof.** For a positive rank-m A, let B_j=P_jAP_j. The j-block of P_inv(A) is (Tr_irrep B_j/d_j)⊗I_(d_j). Because B_j is positive of rank at most m,

\[
\|\operatorname{Tr}_{\rm irrep}B_j\|_2^2\le m\|B_j\|_2^2.
\]

To see this, diagonalize B_j=sum_l lambda_l|v_l><v_l|, use that every reduced rank-one projector has Hilbert-Schmidt norm at most one, and apply (sum_l lambda_l)²<=m sum_l lambda_l². Ordinary partial-trace Cauchy-Schwarz gives the alternative upper bound d_j||B_j||². Consequently

\[
\|P_{\rm inv}A\|_2^2
\le\sum_j\min(1,m/d_j)\|P_jAP_j\|_2^2
\le\sum_j\min(1,m/d_j)\operatorname{Tr}(P_jA^2).
\]

Sum over x and use sum_x A_x²=I. Then (1/d)sum_x||(I-P_inv)A_x||²>=D_n(m). Exact SU(2) equivariance gives H_n>=beta_n(I-P_inv), proving (B). The proof also applies to continuous records by replacing sums with integrals.

A useful simpler estimate is

\[
D_n(m)\ge\left[1-m\,2^{-n}\binom{n}{\lfloor n/2\rfloor}\right]_+,
\tag{C}
\]

because sum_j r_j=binom(n,floor(n/2)). The binomial factor is asymptotic to sqrt(2/(pi n)). Thus positive rank-m effects cannot concentrate in the scalar operator algebra when m is much smaller than sqrt(n), even though that algebra itself has exponentially large dimension.

If gamma_n is the full nonidentity gap, the two bounds can be combined. Since beta_n>=gamma_n and the witness has identity-vector overlap at most m/d,

\[
\operatorname{Tr}(H_nZ)
\ge\gamma_n(1-m/d)+(\beta_n-\gamma_n)D_n(m),\qquad m\le d.
\tag{D}
\]

This uses positivity of the effects and their rank, beyond the ordinary cap Z<=(m/d)I.

## 3. Fixed-prefix and ledger consequences, with quantified limits

For each fixed n, the nonscalar spin-l blocks satisfy H_n=theta² l(l+1)I+O_n(|theta|³), so

\[
\beta_n(\theta)=2\theta^2+O_n(|\theta|^3).
\]

For n=2,m=2 the tracial weights are 1/4 for the singlet and 3/4 for the triplet. Hence D_2(2)=1/4, and (B) gives witness energy at least theta²/2+O(theta³). This is strictly stronger in angle order than the unconstrained fourth-order scalar gap. Exact leading-order loss-free effects would have to be scalar on every magnetic irrep; the triplet cannot be covered by positive effects of rank at most two.

Let r=1-sin(theta)^4 and let L_N be the root's exact final weighted loss. Combining (A), (B), and the minimum final weight of all losses before cut n<N gives

\[
\boxed{L_N\ge\frac43(1-r^{N-n})\,\beta_n(\theta)D_n(m).}
\tag{E}
\]

A receiver achieving error epsilon therefore necessarily satisfies

\[
\frac43(1-r^{N-n})\beta_n(\theta)D_n(m)
\le1-r^N-(1-4\epsilon/3)^2.
\tag{F}
\]

This includes every branch, initialized workspace, arbitrary feedback and classical history. It is a concrete width-dependent weighted-loss inequality, but its evaluated regimes remain limited.

**What is not proved.** No lower estimate for beta_n uniform over a growing prefix has been obtained. Even a bound of order theta² at n~theta^-2 would not by itself force large memory for a fixed positive target error, because the entire right scale is then theta². There is no cumulative entropy-production inequality here. The ordinary full-gap bounds remain stronger for other width/error regimes. In particular, (E)-(F) do not solve N=Theta(theta^-4 log(1/epsilon)) jointly in theta and epsilon.

The physical pure-frame cascade in `slow_generator_derivation.md` additionally shows why one must not infer a universal a_N<=C(m)theta² statement: its fixed m=4 accessible visibility has a positive quartic-time weak-angle limit. That example transmits only classical information and does not settle high-fidelity recovery.
