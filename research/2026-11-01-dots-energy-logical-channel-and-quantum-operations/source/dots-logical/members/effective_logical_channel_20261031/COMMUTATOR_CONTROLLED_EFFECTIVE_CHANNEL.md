# A certified ordinary effective logical channel for rapid zero-field Glauber noise

Status: candidate for independent review. This intentionally changes the output task from a retained source-plus-system process to the ENTIRE SYSTEM, arbitrary reference, and prescribed SYSTEM-ONLY control records. The final source and its path are discarded. It is an ordinary stochastic-averaging/adiabatic-elimination construction, not a novelty claim or a replacement for source-output/source-intervention simulation.

## 1. Input and output contract

The known classical source is an open zero-field nearest-neighbor Ising chain on n bits s_i in{-1,1}, with finite positive local Boltzmann factors. Its unit-rate heat-bath generator Q updates each site at rate one by its Gibbs conditional law. Equivalently its flip rate is [1-s_i tanh(J_left*s_left+J_right*s_right)]/2, with the appropriate one-neighbor boundary formula. Its physical generator is lambda Q, lambda>0. Source innovations are exogenous. This does not infer unknown coupling or quantum backaction from a classical transition law.

The supplied Hermitian system operators A_i have acquired norm upper bounds alpha_i; b=sum_i alpha_i. Let H0 be the system Hamiltonian, D_i=i[A_i,.], L0=i[H0,.], and V=sum_i s_i D_i. The full Heisenberg generator on source-indexed system observables is

    L_lambda=lambda Q+sqrt(lambda) V+L0.

The system dimension can be large; all operator execution costs remain paid. We use the complete operator norm on the direct-sum observable algebra, including an arbitrary reference. Equivalently, its dual is complete trace norm on classical-source/quantum-system states. Initial source/system/reference correlations and the initial source law are arbitrary. No stationary source preparation is required. The effective simulator begins with the SAME reduced system/reference state and does not receive the source label.

At p prescribed times allow supplied system-only CPTP instruments, retaining all outcome records. Feedback controlled by earlier retained records is allowed when its bounds hold uniformly across the record blocks. Source measurements, resets or interventions, source-conditioned controls, and final source output are outside this theorem. Numerical implementation and control errors are added separately.

## 2. Acquired one- and two-spin closure

Let s be the column vector of spin functions. Direct heat-bath calculation gives Qs=M s, M=-I+B, with B supported on nearest neighbors. For an interior site,

    B_(i,i-1)=[tanh(J_left+J_right)+tanh(J_left-J_right)]/2,
    B_(i,i+1)=[tanh(J_left+J_right)-tanh(J_left-J_right)]/2.

At a boundary the sole coefficient is tanh(J). Assume a certified kappa>0 with max_i sum_j |B_ij|<=1-kappa. This is a directly acquired row-sum certificate, not an assumed spectral oracle. Then ||exp(tM)||_infinity<=exp(-kappa*t) and R1=(-M)^(-1) exists with absolute row sums<=1/kappa. Here the matrix infinity norm is maximum absolute row sum.

The stationary covariance C is explicit:

    C_ii=1, C_ij=product_(edges between i,j) tanh(J_edge).

Set z_ij=s_i s_j-C_ij for i<j and z_ii=0. Because no event flips two sites,

    Q(s_i s_j)=s_j Qs_i+s_i Qs_j, i!=j.

Replacing repeated-spin terms by1 and subtracting stationary expectations gives a closed homogeneous linear equation Qz=M2 z on unordered distinct pairs. Its diagonal is -2, and its absolute off-diagonal row sum is at most2(1-kappa). Terms landing on a repeated index disappear from this centered basis; they do not introduce a positive diagonal. Thus

    ||exp(tM2)||_infinity<=exp(-2*kappa*t),
    R2=(-M2)^(-1), ||R2||_infinity<=1/(2*kappa).

This argument permits signed weak bonds. Every basis function z_ij has sup norm<=2. No inverse of the exponentially large source generator is needed. For n=1 the two-spin space is empty and the second corrector below is zero.

For |J_edge|<=1/40, the sum of the absolute two-neighbor coefficients equals max(|tanh(J_left+J_right)|,|tanh(J_left-J_right)|)<=tanh(1/20)<1/20. Hence kappa=19/20 is a valid convenient certificate, independent of n. This kappa is the classical spin-closure bound; it is NOT the smaller energy-Lyapunov constant used by the earlier full source compiler.

## 3. Effective generator, coefficient orientation and positivity

Let P embed a system observable as a source-independent observable, and let Pi denote stationary averaging followed by this embedding. Define R on the required centered scalar function spaces by R s_i=sum_j (R1)_ij s_j and R z_ij=sum_(k<l)(R2)_(ij,kl) z_kl. These satisfy QR=-I on their respective centered spaces.

Define analysis maps from system observables to source-indexed observables:

    F1=R V P,
    F2=R (I-Pi) V F1,
    D_eff=Pi V F1, identified as a system map.

Thus QF1=-VP, QF2=-(I-Pi)VF1. Explicitly F1=sum_ij (R1)_ij s_j D_i. The coefficient of D_k D_i in D_eff is

    (C R1^T)_ki=(R1 C)_ki.

The equality follows from reversibility: M C=C M^T. Let D_int=R1 C. It is real symmetric positive semidefinite: it is the integrated stationary correlation matrix of the reversible generator, or equivalently the quadratic form <f,(-Q)^(-1) f>_pi for f=sum_i v_i s_i. Consequently

    L_eff=L0+D_eff
          =i[H0,.]-sum_ij D_int,ij [A_i,[A_j,.]]

is an actual GKSL generator, not just a formal expansion. If S^T S=D_int, Hermitian Lindblad operators L_a=sqrt(2) sum_i S_ai A_i realize it. The antisymmetric part is zero; no unpriced Hamiltonian correction has been discarded.

The correctors obey complete norm bounds

    f1=||F1||cb<=2b/kappa,
    f2=||F2||cb<=4b^2/kappa^2,
    ||D_eff||cb<=4b^2/kappa.

For F2 the factors are: ||D_k D_i||cb<=4 alpha_k alpha_i, R1 row sum1/kappa, R2 row sum1/(2kappa), and centered-pair sup norm2. These bounds tensor with arbitrary references and do not acquire a system- or source-dimension multiplier.

## 4. Exact residual identity and local commutator constants

The intertwiner

    T=P+lambda^(-1/2)F1+lambda^(-1)F2

is an ANALYSIS device. It need not be CP and is not prepared by the simulator. Both semigroups being compared are CP and unital.

Write d=sum_i d_i, with acquired d_i>=||[H0,A_i]||. Since [L0,D_i]=-[ [H0,A_i], . ], its complete norm is at most2d_i. Cancellation of the sqrt(lambda) and order-one terms gives the exact identity

    L_lambda T-T L_eff
      =lambda^(-1/2) (V F2+[L0,F1]-F1 D_eff)
       +lambda^(-1) ([L0,F2]-F2 D_eff).

Here commutators with F maps mean L0 F-F L0. The complete residual norm is bounded by C1/sqrt(lambda)+C2/lambda, where

    C1=2d/kappa+16b^3/kappa^2,
    C2=8bd/kappa^2+16b^4/kappa^3.

Indeed VF2 and F1 D_eff each cost8b^3/kappa^2. The two product commutators in [L0,D_k D_i] yield8bd/kappa^2 after the same centered-pair and resolvent bounds. No factor ||H0|| occurs in this admission certificate. This is because the commutators are computed before applying a generic norm bound, not because H0 evolution is free.

By contractive Duhamel,

    ||exp(tL_lambda)T-T exp(tL_eff)||cb
        <=t*(C1/sqrt(lambda)+C2/lambda).

Adding the two endpoint defects T-P gives a bound valid for every t in[0,T_total] and every initial CQ/reference state. There is no unproved stationary initial-layer argument, and no smallness assumption on T as a map is required for this inequality.

## 5. System controls: only their coupling commutators are charged

For a supplied system-only instrument C_j, regard C_j dagger as a unital CP map on the observable algebra including its outcome records. Extend each D_i trivially on records. Define acquired upper bounds

    gamma_(j,i)>=||C_j dagger D_i-D_i C_j dagger||cb,
    gamma_j=sum_i gamma_(j,i).

With possibly different input/output record algebras the displayed composition uses the corresponding D_i on each side. Stationary scalar source functions commute with the instrument. Therefore

    ||C_j dagger T-T C_j dagger||cb
      <= gamma_j/(kappa*sqrt(lambda))
         +4b gamma_j/(kappa^2*lambda).

The second term follows by expanding the commutator with each D_k D_i. This bound retains every outcome branch; it is not a bound conditional on a rare selected outcome. Adaptive prescribed-time instruments are covered by uniform bounds on their record-controlled maps.

Telescoping the actual and effective controlled evolutions through the SAME T yields the final complete system-channel error

    E_logical <= min(2,
       [4b/kappa+T_total*C1+sum_j gamma_j/kappa]/sqrt(lambda)
       +[8b^2/kappa^2+T_total*C2+4b sum_j gamma_j/kappa^2]/lambda).

Only TWO endpoint defects occur, not two per time segment. Each interval contributes its residual times its actual duration; each control contributes its one intertwining defect. Contractivity on both sides is valid because actual/effective propagators and the record-retaining instruments are CP. By duality this is a trace-norm bound on the complete retained system/reference/record output, uniformly over initial source/system correlations. In particular the effective map acts on the initial system marginal; it does not require a hidden source state estimate.

If a control commutes with all D_i its defect is zero, even if it has a large global circuit or Hamiltonian bandwidth. A universally safe bound is gamma_(j,i)<=4 alpha_i. For a unitary U, gamma_(j,i)<=2||U dagger A_i U-A_i||. Local gates supported away from A_i commute exactly. For a gate sequence the commutator of the composed superoperator can be bounded by telescoping the acquired per-gate commutators; its gate costs still must be paid. General local instruments can use their finite local representations for a CB/diamond norm bound, or the safe4 alpha_i bound on overlapping support. No optimal norm oracle is assumed.

For piecewise or bounded time-dependent H0 with the SAME A_i, T is unchanged, and the same proof replaces T_total*d by the integral of d(t), and the residual bounds likewise. This observation is conditional on real access to the time-dependent system evolution, not a free simulation oracle.

## 6. Acquisition and numerical execution costs

The source is a KNOWN model; this theorem does not learn an unknown Glauber law. If tanh(J_edge) are supplied exactly as rationals (equivalently suitable positive rational Boltzmann ratios), the nearest-neighbor coefficients are obtained by rational tanh addition/subtraction formulas. C is a product formula, and D_int is obtained by an n-by-n rational linear solve. Classical arithmetic cost is polynomial in n and input bit length; rational determinant/intermediate bit lengths are polynomial as well. A verified kappa lower bound gives conditioning for numerical alternatives. No2^n stationary table, source preparation, conditional-fibre circuit, or whole source-generator solve is required. M2 is used for the certificate, not necessarily constructed during execution.

For general multiple A_i, compute a PSD square root of the n-by-n D_int to certified precision, prepare its finite coefficient lists and implement the resulting Lindblad stack using the supplied A_i encodings. Classical coefficient acquisition, coherent list preparation/routing and operator access are paid. Do not assume the square root is sparse or that it has a free optimal block normalization. A conservative acquired stack normalization follows from the actual coefficient sums of its n rows. Numerical errors in D_int obey the generator perturbation bound

    ||Delta D_eff||cb<=4 sum_ij |Delta D_int,ij| alpha_i alpha_j.

A PSD factor approximation gives an actual GKSL implementation; its generator error is bounded from its acquired factor error. Ordinary finite-matrix square-root methods need accuracy, not a fictitious exact eigenvalue/zero oracle. Allocate coefficient and effective simulation error separately from E_logical. Prescribed instruments are the same supplied operations; their actual synthesis errors are also added. Execution of H0 remains a real cost even though the admission bound uses only d. Large commuting spectator evolution may be factored and implemented ordinarily; it is not omitted from the retained system output.

If only A_l is nonzero, only the scalar D_int,ll is needed: solve (-M)v=C[:,l] and take v_l. The effective dissipator has one jump sqrt(2D_int,ll) A_l. This is a particularly strong ordinary competitor, not a free covariance oracle. For a one-qubit system the resulting4-by-4 Liouville exponential is acquired by ordinary certified dense methods, with polynomial precision cost and a CP channel synthesis/representation if requested. No quantum fast-source routine is needed to compute it.

## 7. A concrete useful regime on the same physical fixture

Take the earlier localized coupling b=1, H0=X and A_l=Z, hence d=2, total time1, no controls, and weak-chain kappa=19/20. Define

    U=4/kappa+2d/kappa+16/kappa^2,
    W=8/kappa^2+8d/kappa^2+16/kappa^3.

Then E_logical<=U/sqrt(lambda)+W/lambda, independently of chain length. Numerically U<26.16 and W<45.26. Thus lambda=10^8 gives E_logical<0.002617, leaving most of a0.01 budget for numerical coefficient/channel error; lambda=10^12 gives E_logical<0.000026161, leaving most of a0.0001 budget. These are rigorous conservative upper bounds, not fitted errors or stationary-start numerics. At small lambda or demanding precision the certificate can fail to admit the effective method; that is an honest boundary, not evidence that the exact simulator becomes practical.

This changes what is bought: the expensive full simulator retains a joint source process with arbitrary admitted source operations and high finite-rate precision. The ordinary effective method here certifies the entire logical system channel, references and system-only records, but does NOT reproduce source output, source-conditioned feedback, microscopic paths, or corrections below its explicit finite-rate error. The coefficient solve and effective channel execution are the candidate winner for this restricted task.

## 8. Strong ordinary literature and limits of the comparison

This proof is a finite complete-norm version of the ordinary Poisson-corrector/adiabatic-elimination strategy. It must not be described as inventing effective noise or model reduction. Azouit, Sarlette and Rouchon, arXiv:1603.04630, give effective Lindblad expansions and specific Hamiltonian second-order corrections. Reiter and Sorensen, arXiv:1112.2806, provide effective Hamiltonians and jumps for weakly driven eliminated excited sectors. Their accessible primary abstracts were inspected; no uninspected arbitrary-input diamond theorem is attributed to them.

Le Regent and Rouchon, arXiv:2303.17308v2 (actual primary HTML inspected), formulate Heisenberg elimination using invariant observables and detail second-order slow propagators. Grigoletto et al., arXiv:2603.11982v1 (actual primary HTML inspected), give algebraic reduced Lindblad generators and finite-time error bounds for perturbations. These are strong constructive alternatives, not straw comparisons. The present narrow exercise explicitly acquires the first two spin closures, complete-norm endpoint/control defects and n-dimensional coefficient solve for THIS known source. A bounded search does not establish that these particulars are absent from prior work or that this is a new theorem.

Primary links:
https://arxiv.org/abs/1603.04630
https://arxiv.org/abs/1112.2806
https://arxiv.org/html/2303.17308v2
https://arxiv.org/html/2603.11982v1
https://arxiv.org/abs/1807.02036
https://arxiv.org/abs/2011.04713

The latter two primary abstracts describe general strong-coupling/error-bound machinery and higher-order effective dynamics. An attempted HTML version2011.04713v3 returned404; no theorem was inferred from that failed fetch. The classical random-evolution literature is likewise established; the fetched author-hosted Fouque et al. book front matter contains only a contents listing of the relevant diffusion-approximation/perturbed-test-function chapters, so it is NOT used as evidence for an unseen quantitative theorem. All earlier denied sources remain untouched.

No novelty, classical/quantum computational separation, universal effective-source theorem or practical quantum advantage follows. The substantive intended payoff is a fully certified ordinary logical-channel route that can win on an explicitly weaker output task, with admission governed by the unwanted couplings and their commutators rather than full environment/system bandwidth.

## 9. Exact native-quantum logical-output extension (restricted algebra)

For the SPECIFIC direction-merged geometric source in GEOMETRIC_GIBBS_NATIVE_COMPILER_BINDING.md (accepted source6d35e79d; independent receipt70e39835dc81681e517c6a34f08da49e18258e975e84f572e339b0f653d1a9b8), its adjoint preserves the source-diagonal system-valued observable algebra and restricts there to the classical heat-bath Q. This is the actual generator, not a different collision approximation. Locally, holding the neighboring classical context fixed, the two direction-merged jumps give

    G_i dagger diag(a,b)=diag(r_0*(b-a),r_1*(a-b)).

The off-diagonal terms from the recycling and anticommutator cancel. The same calculation holds for system-valued diagonal blocks, since scalar source coefficients commute with them; merging untouched contexts does not introduce off-diagonal terms from a diagonal observable. Diagonal coupling K=sum_i Z_i tensor A_i preserves this algebra, as do H0, reference identities, and system-only record-retaining instruments.

Every backward-evolved final logical observable therefore remains source-diagonal. For ANY initial quantum source/system/reference state rho, replacing it by source computational-basis dephasing leaves every logical/record/reference output statistic unchanged. This dephasing also leaves its reduced system/reference state unchanged. Apply the complete CQ theorem to that dephased state: the SAME logical error bound follows for arbitrary initial quantum source correlations under this native generator. No physical dephasing or preparation is required of the simulator; it is an equality used in the proof.

This does not identify the raw quantum source state, artificial/physical jump records, or source outputs with a classical bath. It does not permit source interventions, arbitrary quantum lifts sharing only a stationary state, or couplings outside the invariant algebra. The output remains precisely the system, reference and system-only control records.

## 10. Optional ordinary local coefficient acquisition

For a single localized A_l, D_int,ll=(sum_(k>=0) B^k C)_ll. Let I_R be the open subchain consisting of sites within graph distance R of l (clipped at physical endpoints), with boundary interactions outside I_R deleted. Its C^R_(j,l) equals C_(j,l) on retained sites by the same path-product formula. B^R rows agree with B at sites whose distance from l is strictly less than R. A length-k walk starting at l uses only these agreeing rows when k<=R, so (B^k C)_ll=((B^R)^k C^R)_ll for k<=R.

Deleting a neighboring bond cannot increase the heat-bath row absolute sum: it changes tanh(|J_left|+|J_right|) to tanh(|J_remaining|). Hence the same bound r=1-kappa<1 holds for B^R. Each remaining Neumann tail is bounded by r^(R+1)/kappa, since the covariance column has magnitude<=1. Thus

    |D_int,ll-D_int,ll^R|<=2*r^(R+1)/kappa.

If the subchain already contains the whole chain, the error is exactly zero, not merely a nonzero geometric estimate. For r=0, radius0 is exact. The induced logical-channel error over timeT is at most8 alpha_l^2 T r^(R+1)/kappa by contractive generator perturbation, with the SAME system-only controls. The local effective coefficient is itself positive, so this approximation is still a genuine GKSL generator.

Choose R from this explicit bound and acquire only O(R) nearby coupling tables plus an ordinary small tridiagonal solve. This is a standard Neumann/locality argument, not a novel covariance method. The GLOBAL row-sum/zero-field/family certificate must still be acquired or supplied by a known finite program; an arbitrary n-entry input cannot be globally validated without reading it. A uniform known weak-bond program supplies that certificate without an n-state table. Random access to nearby input data and its actual cost are paid; no free QRAM or unverified local-to-global promise is introduced.
