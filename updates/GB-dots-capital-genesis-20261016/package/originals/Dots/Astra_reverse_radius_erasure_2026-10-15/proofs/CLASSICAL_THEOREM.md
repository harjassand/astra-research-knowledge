# A small exact SDP for complete conditional RLD contraction of an arbitrary classical channel

Status: internally derived and independently reconstructed. External review and historical priority remain open. The proof is elementary and does not require a generic free-rational Positivstellensatz.

Let T be a nonnegative n-by-m column-stochastic matrix. Drop identically zero output rows. Write t_i for column i. Let C(T) be the supremum, over all finite dimensions, faithful POVMs R_i summing to I and vector tuples z_i summing to zero, of

    N/E = [Σ_y z_y* A_y^{-1} z_y] / [Σ_i z_i* R_i^{-1} z_i],
    A_y=Σ_i T_yi R_i, z_y=Σ_i T_yi z_i.

The unrestricted physical conditional RLD/Petz-chi-square coefficient equals this vector coefficient; Section 5 pays the Hermitian realization explicitly. This theorem does not identify their fixed-dimension coefficients.

## 1. Exact answer

C(T) is the optimum of the SDP

    minimize c over c∈R, u∈R^n,
    [[c diag(t_i), t_i−u], [(t_i−u)^T, 1]] >= 0  for i=1,...,m.

There are only n+1 scalar variables and m PSD constraints of size n+1. Zero entries are handled exactly by these LMIs: if any T_yi=0 then u_y=0 is forced.

For strictly positive T this is equivalently

    C(T) = min_u max_i Σ_y (T_yi−u_y)^2/T_yi
         = 1 − min_{p∈Δ_m} Σ_y [Σ_i p_i/T_yi]^{-1}.                 (1)

The vector u is NOT constrained to sum to one. Imposing that condition changes the answer.

For arbitrary T, define J={y:T_yi>0 for EVERY i}. Then the exact dual formula is

    C(T) = 1 − min_{p∈Δ_m} Σ_{y∈J} [Σ_i p_i/T_yi]^{-1}.          (2)

An empty sum is zero. In particular, C(T)=1 if J is empty. This support-sensitive expression avoids undefined 0/0 conventions at boundary priors. For strictly positive priors p it is the usual reciprocal expression with 1/(+∞)=0 on noncommon rows.

## 2. Inverse elimination and upper certificate

For a faithful POVM let D_R=diag(R_i), S=[sqrt(R_1),...,sqrt(R_m)]. Since SS*=I, P=S*S is a projection. Set z=D_R^{1/2}w. The constraint Σ_i z_i=0 says w∈ker S. The input cost is ||w||². The map to normalized output vectors is D_A^{-1/2}(T⊗I)D_R^{1/2} restricted to ker S.

Consequently N<=cE for all zero-sum z is equivalent to

    F_c(R):=c D_A − Σ_i (t_i t_i^T)⊗R_i + [A_y A_z]_{yz} >= 0.  (3)

Indeed D_R^{1/2}(I−P)D_R^{1/2} has ij block δ_ij R_i−R_iR_j, and (3) is the corresponding BB* norm inequality after congruence by D_A^{1/2}.

If u satisfies the small SDP, put G_i=c diag(t_i)−(t_i−u)(t_i−u)^T>=0 and B=[A_1,...,A_n] (a block row). Then the exact polynomial identity is

    F_c(R) = Σ_i G_i⊗R_i + (B−u^T⊗I)*(B−u^T⊗I).              (4)

Both terms are positive. Thus the SDP optimum is an upper bound in every reference dimension. Identity (4) is a degree-two polynomial certificate comprising a square of affine factors and constant-coefficient simplex localizers, not a numerical certificate.

## 3. Elementary minimax dual

The SDP is equivalent to minimizing over u supported on J the maximum of

    f_i(u)=1−2Σ_{y∈J}u_y+Σ_{y∈J}u_y²/T_yi.

For positive entries on J these quadratics are uniformly coercive. Standard finite-dimensional convex minimax (or epigraph KKT duality with a strictly feasible epigraph) gives

    min_u max_i f_i(u)=max_{p∈Δ_m} min_u Σ_i p_i f_i(u).

The inner optimum is u_y=[Σ_i p_i/T_yi]^{-1}, with value (2). The dual minimum is achieved on the compact simplex. If J is empty, f_i=1 and the formula is immediate. A rational pair (u,p) gives exact upper and lower rational bounds, requiring only rational arithmetic on the common rows.

## 4. Weighted-simplex sharpness witness

First choose p_i>0 for every i, m>=2. Set s=(sqrt(p_i))_i, P=I−ss*, and H=s^⊥, dimension m−1. For v_i=P e_i define

    R_i^0=v_i v_i* on H,       z_i=sqrt(p_i) v_i.

Then Σ_i R_i^0=I_H and Σ_i z_i=Ps=0. Every z_i lies in the support of R_i^0. Since ||v_i||²=1−p_i>0,

    E_0=Σ_i z_i*(R_i^0)^+z_i=Σ_i p_i=1.

For a row y put D_y=diag(T_yi). Its output baseline and vector are

    A_y^0=(P D_y P)|_H,       z_y=P D_y s.

The compressed-diagonal inverse identity gives

    z_y*(A_y^0)^+ z_y
      = s*D_y s − [s*D_y^{-1}s]^{-1}                         (5)

when D_y>0. If D_y has a zero entry, the second term is zero and (5) holds in that limiting sense. A proof is the Schur complement in the decomposition C^m=span{s}⊕H: the Schur complement of A_y^0 in D_y is the reciprocal of s*D_y^{-1}s. For a singular diagonal D_y, regularize D_y+δI. The support condition z_y∈range A_y^0 follows because any x∈ker A_y^0 satisfies D_y^{1/2}x=0, hence <x,z_y>=<x,D_y s>=0; the supported inverse quadratic converges. Since every p_i>0, s*D_y^{-1}s diverges when a diagonal entry vanishes.

Summing (5) over y and using stochasticity yields precisely

    N_0=1−Σ_{y∈J}[Σ_i p_i/T_yi]^{-1}.

Use R_i(ε)=(R_i^0+εI)/(1+mε), keeping z_i fixed, for faithful POVMs. All input and output inverse costs converge to their supported limits. Thus every strictly positive p gives the dual lower bound. Positive priors are dense, and expression (2) is continuous on Δ_m, proving equality for all channels, including zero entries.

For strictly positive T, a boundary p can instead be restricted to its support k. The same construction then uses dimension k−1 (provided k>=2). If k=1, the dual value is zero. A positive optimum permits a maximizing prior with k<=min(m,n): minimize Σ_y 1/a_y over the convex hull of a_i=(1/T_yi)_y. Its nonzero gradient exposes a supporting face of affine dimension at most n−1 (or the hull itself already has dimension at most n−1), and Carathéodory on that face uses at most n vertices. Thus vector reference dimension min(m,n)−1 suffices in the supremum for strictly positive channels. No analogous improved support bound is asserted here for zero-entry channels; m−1 always suffices by positive-prior approximation.

## 5. Physical Hermitian realization in the SAME dimension

The usual conditional-defect algebra proves that any vector inequality gives the physical upper bound, after applying it to matrix columns Z_i=H_i−R_iK, K=ΣH_i, and undoing reference congruence.

For the weighted-simplex lower witnesses no coherent flag is necessary. This same-dimension realization has been independently reconstructed. On the active k-symbol support, choose real h_i not all equal and put H_i=h_i R_i^0. Let K=ΣH_i and Z_i=H_i−R_i^0K. Each Z_i has range contained in span(v_i), and ΣZ_i=0. The synthesis matrix V=[v_1,...,v_k] has its unique kernel span(s). Therefore there is a COMMON row w* such that

    Z_i=sqrt(p_i) v_i w*=z_i w*  for every i.

Explicitly, w*=s*diag(h)P and ||w||²=Σ_i p_i h_i²−(Σ_i p_i h_i)², which is positive for nonconstant h on the active support. Alternatively, the row is nonzero because otherwise v_i* K=h_i v_i* for all i. Hermiticity of K and the nonzero pairwise inner products v_i*v_j=−sqrt(p_i p_j) force all h_i equal, a contradiction. Consequently every input and output conditional trace cost is the corresponding vector cost multiplied by ||w||², and the ratio is exactly the dual value.

Subtract the same scalar α=Tr(K)/(k−1) from every h_i. This makes Tr(K)=0 without changing any Z_i, because ΣR_i^0=I. Keep these H_i fixed while replacing R_i^0 by faithful R_i(ε). Every H_i is supported on R_i^0, and every output tangent Σ_iT_yiH_i is supported on A_y^0, so both input and output RLD costs converge to their supported limits. The reference baseline remains I and its tangent K is fixed. Divide baseline and tangents by k−1 and use a sufficiently small nonzero perturbation to obtain faithful normalized physical state pairs, with the exact quadratic Petz-Q2 identity.

Thus for a nonconstant strictly positive channel the physical AND vector complete coefficients are reached in the supremum with reference dimension at most min(m,n)−1. General channels with zero entries require at most m−1 by positive-prior approximation. A constant channel has coefficient zero and reference dimension one suffices. These are upper bounds, not assertions of minimal dimension for each channel. Inactive symbols can be included with zero baselines/tangents before faithful regularization.

For completeness, an arbitrary vector witness (not necessarily the frame construction) can be physically realized with ONE additional coherent flag dimension: for a_i>0, Σa_i=1, set Rtilde_i=diag(Ma_i,R_i), Htilde_i=[[0,z_i*],[z_i,0]]. Its physical input and output costs are E+M^{-1}Σ||z_i||²/a_i and N+M^{-1}Σ||z_y||²/(Σ_iT_yi a_i); their ratio tends to N/E. Normalization by M+r and a small tangent perturbation give faithful states. This generic conversion pays r+1, but that extra cost is unnecessary for the structured sharp witnesses above.

## 6. Exact non-symmetric benchmark

Take the cyclic, nonsymmetric channel

    T=[[1/2,1/6,1/3],
       [1/3,1/2,1/6],
       [1/6,1/3,1/2]].

The exact answer is C(T)=2/11. An upper certificate is u=(3/11,3/11,3/11), for which every f_i(u)=2/11. The dual lower certificate is p=(1/3,1/3,1/3), giving Σ_i p_i/T_yi=11/3 for every row and 1−Σ_y3/11=2/11. The weighted-simplex vector witness lives in dimension two; the same-dimension Hermitian physical construction also uses dimension two. This is not the m-ary symmetric channel.

For T_lambda=lambda I+(1−lambda)J/m, symmetry gives p uniform and u_y=m/[1/(lambda+mu)+(m−1)/mu], mu=(1−lambda)/m. Formula (1) simplifies exactly to lambda²(m−1)/[1+(m−2)lambda], recovering the independently proved complete threshold.

## 7. Algorithm and bit/conditioning scope

This is an exact rational-data SDP description of polynomial size, and also a convex quadratic minimax problem (or SOCP). It is not a claim that every optimal value/witness is rational or has polynomial exact bit length. Primal/dual rational trial points give rigorous intervals; their gap is an immediately checkable stopping criterion. Positive common entries bounded below by τ control reciprocal arithmetic and smoothness; tiny entries can cause conditioning and must not be rounded to zero. Zero support is handled symbolically by J or directly by the LMIs. Numerical SDP termination alone is not an exact certificate. The generic S^9 free-rational method is neither needed nor relabeled here.

## 8. Literature positioning, checked before and during derivation

The initial search checked complete SDPI/chi-square/conditional variance literature and the strongest available free positivity route. Helton–Klep–McCullough, "The convex Positivstellensatz in a free algebra", Adv. Math. 231 (2012), 516–534, Theorem 1.1(1), already implies a certificate with affine square factors and constant localizers for the degree-two polynomial (3): https://arxiv.org/abs/1102.4859 and primary author PDF https://mathweb.ucsd.edu/~helton/BILLSPAPERSscanned/HKMpreptB.pdf . This was a discovery aid; the elementary sharpness proof renders it unnecessary.

Volčič's generic rational theorem is prior art, not the contribution here: https://arxiv.org/abs/2101.02314 . Related complete entropy/SDPI and fixed-reference quantum chi-square searches did not establish this exact unrestricted conditional RLD formula. No claim of absence or novelty follows from those searches. A targeted predecessor audit of the reverse-chi-square minimax radius and harmonic-mean dual remains necessary. Do not conflate this conditional-excess coefficient with tensor-with-identity SDPI without subtraction (generally 1), SLD, entropy, or capacity.

## 9. Certified numerical implementation

`../solver.py` accepts an exact rational JSON channel, proposes a prior using SciPy, rationalizes it, and then computes exact Fraction primal and dual bounds. Its output gap is rigorous regardless of the numerical optimizer status; a nonzero gap is not concealed as an exact answer. `../examples/cyclic_channel.json` and `../examples/cyclic_certificate.json` give a zero-gap certificate with value 2/11. The package checks independently verify the exact cyclic benchmark and weighted-frame construction; the solver is optional.

For positive T, one may also normalize u=αq and optimize α explicitly: C(T)=1−exp(−R), where R=min_{q∈Δ_n}max_i D_2(q||t_i). Thus the scalar optimization is a reverse order-2 Rényi information radius. This is an algebraic identification, not a historical claim about that radius; the precise contribution to audit is its equality to the complete conditional RLD coefficient.
