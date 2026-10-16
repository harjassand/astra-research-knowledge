# Two arbitrary classical channels: exact small signed-lift SDP

Status: direct constructive specialization for two classical channels on a common input, independently reconstructed. The earlier manuscript Complete quantum information orders (10 October 2026), Appendix A, already states a finite complex-linear complete Petz-D2 lift characterization. This is not the first finite comparison algorithm. See PROVENANCE.md for the corrected positioning.

## Theorem

Let S∈R^{k×m} and T∈R^{n×m} be column-stochastic classical channels with the same input alphabet. Delete identically zero output rows. The following are equivalent:

1. S dominates T in ordinary, unsmoothed COMPLETE binary squared-MMSE order, permitting arbitrary finite quantum references and arbitrary joint input encodings.
2. S dominates T in complete SLD quadratic order.
3. S dominates T in complete standard-Petz/RLD quadratic (equivalently faithful-pair Petz-Q2) order.
4. There exists a REAL, state-independent signed matrix D∈R^{n×k} such that

       DS=T,
       diag(t_i)−D diag(s_i)D^T >=0  for every input i.        (1)

Here s_i and t_i are the source and target columns. Every such D automatically has D^T1_n=1_k. No entrywise positivity of D is required.

Condition (1) is a rational SDP with nk real variables, nm mean equalities, and m LMIs of size n+k:

       [[diag(t_i), D diag(s_i)],
        [diag(s_i) D^T, diag(s_i)]] >=0.                    (2)

The singular lower diagonal blocks are harmless: their off-diagonal blocks already have the requisite support, so the generalized Schur complement is exactly (1). One may omit source coordinates with s_ai=0 separately in each LMI.

If no signed lift exists, an ordinary binary-MMSE failure can be realized with reference dimension at most n+1. If DS=T itself is inconsistent, a scalar-reference witness suffices. These are sufficient bounds, not minimality assertions.

## 1. Signed lift implies complete observable and RLD comparison

Given target Hermitian reference observables A_y, define source observables B_a=Σ_y D_ya A_y. For every input i their first-moment operators agree because DS=T. Their second-moment defect equals

    Σ_y t_yi A_y²−Σ_a s_ai B_a²
      =Σ_yz [diag(t_i)−Ddiag(s_i)D^T]_{yz} A_y A_z >=0.

A real PSD factorization makes the right side a sum of squares of Hermitian linear combinations. Thus noncommuting reference observables are covered. The lift improves every squared-error risk; general POVMs reduce to their first-moment observables, whose spectral measurements have no larger second moment. This proves complete MMSE and SLD dominance by the standard exact variational dictionary.

For RLD, take arbitrary positive reference blocks R_i and arbitrary vector tangents z_i, and write

    A_a=Σ_i s_ai R_i,       z_a^S=Σ_i s_ai z_i,
    B_y=Σ_i t_yi R_i,       z_y^T=Σ_i t_yi z_i.

The scalar covariance matrices in (1), tensored with R_i and summed, give

    diag(B_y)−(D⊗I)diag(A_a)(D^T⊗I)>=0.

Also z^T=(D⊗I)z^S. By inverse weighted contraction,

    Σ_y (z_y^T)*B_y^{-1}z_y^T
       <=Σ_a (z_a^S)*A_a^{-1}z_a^S.                         (3)

The blocks are positive definite because the channels have no identically zero rows and R_i>0. Applying (3) to every tangent matrix column proves RLD trace comparison for Hermitian tangents, without relying on SLD congruence invariance.

Automatic unitality: set e=D^T1_n. From DS=T, Σ_a s_ai e_a=1. From (1), Σ_a s_ai e_a²<=1. Equality in scalar variance forces e_a=1 whenever s_ai>0. Every source row is positive for some i, so e=1_k.

## 2. Failure of mean reconstruction already yields a witness

If DS=T is inconsistent, ker S is not contained in ker T. Choose real h with Sh=0 but Th≠0. Stochasticity gives Σ_i h_i=1_k^TSh=0. With any positive scalar input baseline r_i, the source tangent vanishes while the target tangent does not. A sufficiently small normalized binary perturbation r±t h is faithful and has strictly smaller target MMSE. It also violates RLD order. Rational S,T allow a rational h by exact linear algebra.

Hence assume DS=T has at least one solution.

## 3. Strong finite-dimensional separation of failed covariance constraints

Consider the convex optimization problem

    κ_* = min_{D:DS=T} max_i λ_max(Ddiag(s_i)D^T−diag(t_i)).   (4)

After deleting zero source rows, c_min=min_a Σ_i s_ai>0. For any D, summing the traces of the matrix defects gives

    mn·max_i λ_max(defect_i)
       >= c_min||D||_F²−m.

Thus (4) is coercive on the closed affine mean-reconstruction set, so its minimum is attained. The signed lift fails exactly when κ_*>0.

Introduce κ and impose diag(t_i)+κI−Ddiag(s_i)D^T>=0. A sufficiently large κ makes all matrix residuals strictly positive for any fixed feasible D. Equivalently, use (2) with κI added to the top-left block and remove zero lower coordinates. This gives Slater feasibility. Standard finite-dimensional convex Lagrange duality therefore yields PSD matrices Q_i∈R^{n×n}, Σ_iTrQ_i=1, such that

    inf_{D:DS=T} Σ_a d_a^T A_a d_a
       − Σ_iTr[Q_i diag(t_i)] = κ_* >0,                     (5)
    A_a=Σ_i s_ai Q_i,

where d_a is column a of D. The only use of SDP duality is this finite-dimensional Slater argument, not a free-rational Positivstellensatz.

If some Q_i are singular, replace all Q_i by R_i=Q_i+εI_n. The infimum of the quadratic term cannot decrease, while the right-hand scalar subtraction increases by εm. Choosing 0<ε<κ_*/m retains strict positivity in (5). Every R_i is now faithful, and every A_a=Σ_i s_aiR_i and B_y=Σ_i t_yiR_i is positive definite. The trace normalization ΣTrQ_i=1 is no longer needed after this perturbation.

## 4. The SDP dual produces a quantum-reference RLD failure

For these faithful R_i, minimize the strictly convex quadratic Σ_a d_a^TA_ad_a under the feasible linear constraints Σ_a s_ai d_a=t_i. Ordinary quadratic Lagrange duality, with real multipliers z_i∈R^n and factor two convention, gives

    min_{D:DS=T} Σ_a d_a^TA_ad_a
      =max_{z_i} [2Σ_i z_i^Tt_i
                  −Σ_a (Σ_i s_ai z_i)^T A_a^{-1}(Σ_i s_ai z_i)].

The maximizer exists even when the linear mean constraints are redundant, since a minimum exists and linear first-order stationarity supplies multipliers. Choose such z_i. Because Σ_iTr[R_i diag(t_i)]=Σ_y e_y^TB_ye_y, strict inequality (5) becomes

    2Σ_y e_y^T z_y^T−Σ_y e_y^TB_ye_y
       > Σ_a (z_a^S)^TA_a^{-1}z_a^S.

The target inverse variational formula evaluated at canonical vectors e_y gives

    Σ_y(z_y^T)^TB_y^{-1}z_y^T
      >=2Σ_y e_y^Tz_y^T−Σ_y e_y^TB_ye_y.

Therefore (3) is strictly reversed. This is a vector RLD witness on reference dimension n. No commutation of R_i is presumed. No zero-sum constraint on z_i is needed: both channels preserve the same reference tangent, so its subtraction cancels in their difference.

## 5. Ordinary physical SLD/MMSE and RLD witnesses

To turn the vector failure into a physical RLD failure, use ONE coherent flag with large baseline weight. Pick a_i>0 and set Rhat_i=diag(R_i,M a_i), Hhat_i=[[0,z_i],[z_i^T,0]]. The physical RLD cost for each channel output is its vector cost plus M^{-1} times a finite extra scalar term. Letting M→∞ preserves the strict failure. All tangents are Hermitian and traceless. Normalize the total baseline and choose a small perturbation to obtain faithful state pairs. Thus failure of the signed lift contradicts complete RLD order.

For the SLD/MMSE witness, use a SMALL flag weight instead:

    Rtilde_i=diag(R_i,δa_i),
    Htilde_i=[[0,z_i],[z_i^T,0]].

For a source output a the exact SLD cost is

    4 (z_a^S)^T[A_a+δ(Σ_i s_ai a_i)I]^{-1}z_a^S,

and similarly for the target output. As δ→0, these converge to four times the strictly separated vector costs. A finite positive δ therefore yields a strict SLD failure. Normalize all blocks by their common total trace and take a sufficiently small nonzero binary perturbation amplitude. Positivity follows from the scalar Schur bound t² z_i^TR_i^{-1}z_i<δa_i. The tangent has trace zero automatically; its REFERENCE marginal need not be zero, which is allowed in complete order.

For equiprobable labels ±1 and normalized states ρ_±=ρ±tH, the exact Bayes risk is 1−t²g_ρ^SLD(H). Thus the finite SLD failure is an ordinary, unsmoothed binary-MMSE failure, using reference dimension n+1. This proves the converse without invoking the general Hermitian-smoothed signed-lift theorem.

## 6. Binary-input consequence and relation to earlier algorithms

For binary-input classical channels, earlier one-variable functional calculus proves complete RLD order equivalent to the scalar Fisher inequality f_S(x)>=f_T(x) for every0<x<1. The present theorem therefore also proves equivalence to complete SLD/MMSE AND the common signed-lift SDP. This is a derived consequence of the general proof, not an assumption used in it.

One must NOT justify it by whitening SLD baselines through arbitrary reference congruence: SLD lacks that invariance. The route through (3), finite SDP separation, and the coherent flag avoids that invalid step.

For common classical input and classical output, (2) gives m blocks of order at most n+k and nk variables, substantially smaller than the generic free-rational construction. An earlier internal source already proves a finite complex-linear lift characterization for arbitrary channels; the present formulation is a direct small real classical specialization, not the first finite Petz algorithm. This does not supersede the generic algorithm for noncommuting input POVMs or arbitrary quantum channels. Rational data give a rational SDP encoding of polynomial size, but numerical solver success is not exact feasibility, and no polynomial-bit exact decision or rational-optimum guarantee is asserted.

## 7. Exact positive-channel fixture beyond stochastic degradation

Let

    S=[[3/8,1/8],[1/8,3/8],[1/2,1/2]],
    T=[[13/20,7/20],[7/20,13/20]],
    D=[[11/10,−1/10,1/2],[−1/10,11/10,1/2]].

Both channels have strictly positive entries; S is not an erasure channel. Exact multiplication gives DS=T. For BOTH inputs,

    diag(t_i)−Ddiag(s_i)D^T=(7/100)[[1,−1],[−1,1]]>=0.

Therefore S dominates T in complete ordinary SLD/MMSE and complete RLD order, with this one state-independent compiler. Yet source-column total variation is1/4 and target-column total variation is3/10, so no stochastic degradation exists. This is the previously studied input-noised BEC/BSC pair, now with an especially small explicit global signed-lift certificate; the channel pair itself is not new.

## Priority and scope

Signed complete variance domination, finite CP-defect certificates, and observable-estimation compilation are established in Zhu–Wang (arXiv:2607.24693v2) and Hirche (arXiv:2610.03706). Their general necessity result involves Hermitian smoothing. The specific derivation above exploits COMMON CLASSICAL INPUT and CLASSICAL OUTPUT to convert the finite covariance-SDP dual into an ordinary physical reference witness. No source has yet been verified to contain precisely this common-classical-input unsmoothed converse; this bounded status is not a novelty claim.

No cq-output extension is asserted here. General quantum score spaces require separately proving that the appropriate complete variance SDP has a dual that can be realized by the channel's positive reference baselines; classical diagonal output coordinates are used explicitly in Section4.

## Earlier finite lift theorem

Complete quantum information orders, dated 10 October 2026, Appendix A, Theorem A.1, already states a finite COMPLEX-linear unital lift characterization of complete Petz order two for arbitrary channels, with reference bound 2b². Its proof uses complex quadratic conjugacy, compact-density minimax with coercive attainment, and one-row selection. Its affine Schur SDP is explicit. This is an earlier research manuscript; independent external publication and historical priority have not been established here.

For classical source and target output algebras, that theorem specializes to a complex signed coefficient matrix. If the input is classical (or all POVM effects are simultaneously real in one basis), averaging a feasible complex lift with its entrywise conjugate gives a real feasible lift: reconstruction is real, and the quadratic defect cone is convex. Thus the real signed-lift conclusion is also recoverable as a specialization of that earlier theorem. The present proof independently supplies direct separation, smaller classical coordinates, and a reference n+1 physical ordinary-SLD/MMSE witness.

A generic complex-POVM extension of the real-dual proof is unjustified. For real coefficient variables its dual quadratic form uses Re(A), whereas physical inverse costs use A. For A=[[1,iα],[-iα,1]] and real z=e1, the latter cost is 1/(1−α²) and the former is 1. No general ordinary-SLD equivalence for complex POVMs is asserted.
