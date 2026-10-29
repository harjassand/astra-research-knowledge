# Acquired positive-operator certificates for a hidden qubit algebra

28 October 2026. Root candidate. This is a new construction, not an expansion of received scalar whitening by association. Independent algebra challenge has found no flaw, but full finite acquisition review remains pending.

## 1. The obstruction and changed representation

Scalar Gram whitening fails when the noise contraction varies together with a spectator record. Operator-valued anticommutator whitening resolves commuting sectors, but generally fails when the spectator coefficients do not commute. Instead fit a physical Pauli algebra and certify a POSITIVE OPERATOR-BLOCK representation of its measured contrasts. The positive block supplies a global variational certificate, not a microscopic environmental model.

On a finite output envelope of dimension d=2g let B_X,B_Y,B_Z be an unknown physical Pauli triple: Hermitian unitaries, pairwise anticommuting, B_Y=i B_X B_Z. The true ordinary signed contrasts satisfy

    C_j=sum_k B_k T_kj,
    T_kj=T_jk=T_kj dagger,
    [T_kj,B_a]=0 for every a,
    T=[T_jk]_(j,k=1)^3 >=0 on C^3 tensor C^d.       (1)

The entries of T need NOT commute with each other. All C_j are Hermitian. For the complete n-qubit inverse claim below, ALL local triples must arise from ONE fixed global unitary V: B_(i,j)=V sigma_(i,j) V dagger. Thus different input-qubit algebras commute and jointly represent the full n-qubit algebra; unrelated locally valid triples do not suffice. This is a structural promise on actual reduced conditional means, not something arbitrary finite observations prove about a source. Positive semidefinite T suffices for soundness; a strictly positive margin is needed for the completion guarantee below.

Actual physical examples include history-dependent mixtures of product qubit channels whose own-qubit Bloch matrices are symmetric positive definite but may have different unknown damping axes. Before a common fixed output mixer, each component contributes a positive scalar3-by-3 contraction times its positive spectator state. Their sum is a positive operator block. On an envelope containing the entire true own-qubit algebra, partial trace preserves block positivity, entry symmetry and commutation with that algebra. It can turn globally commuting spectator factors into noncommuting local factors; (1) still survives. No supplied classical sector or its readout is needed. For product unknown-axis amplitude-damping components with every rate at most gamma_max<1, the earlier local backward-cone argument gives a containing-envelope block floor tau>=(1-gamma_max)^|K|/2^|J|, where |K|<=min(n,|J|+2(w-1)). The scalar Bloch minimum contributes one factor; spectator states contribute the other |K|-1 factors. Positive mixtures retain that floor even with noncommuting reduced spectators. This is an instance completion bound, not a numerical input required by the learner.

This source family keeps a common physical orientation. Arbitrary component-specific unitary rotations are not included merely because each component has a polar decomposition. A fixed single contraction can use the separate canonical polar convention; independently changing polar rotations do not necessarily share B.

## 2. Global variational identity

For ANY physical Pauli triple A on the same space define

    F_C(A)=sum_j Tr(A_j C_j),
    D_j=A_j-B_j, Dnorm^2=sum_j ||D_j||F^2.

Then exactly

    2[F_C(B)-F_C(A)] = sum_jk Tr(D_j T_jk D_k).     (2)

Proof: cyclicity gives sum_jk Tr(A_j T_jk A_k)=sum_jk Tr(T_jk A_k A_j). Symmetry T_jk=T_kj cancels off-diagonal terms through anticommutation, and diagonal terms equal sum_j Tr T_jj. The B term is identical. The two cross terms each equal F_C(A), using commutation of T with B and index symmetry. Finally block positivity makes the right side nonnegative: for every basis vector x it is the quadratic form of T on the stacked vector (D_1 x,D_2 x,D_3 x).

Therefore B is a global maximizer of an objective depending ONLY on observable C. If T>=tau I_(3d), then

    F_C(B)-F_C(A) >= (tau/2) Dnorm^2.              (3)

This is global, not a local Hessian calculation. With strict tau it identifies B uniquely as matrices even though the unitary implementing that algebra is ambiguous on the spectator factor. Mutual commutativity of T entries was never used.

For empirical Chat=C+E, any zeta-global maximizer A of F_Chat obeys

    Dnorm <= [Enorm+sqrt(Enorm^2+2 tau zeta)]/tau,
    Enorm=(sum_j ||E_j||F^2)^(1/2).                (4)

This follows by comparing objective values at A and B and using Hilbert–Schmidt Cauchy–Schwarz. Equation(4) is an existence/completion device; the implementable acceptance certificate below does not require supplying tau or trusting a global numerical optimizer.

## 3. A posteriori positive fit certificate

Construct ANY exact physical triple A, and ANY symmetric Hermitian operator block S whose entries commute with all A_j. Verify S>=kappa I_(3d) for an explicit rational kappa>0. Define

    Ctilde_j=sum_k A_k S_kj,
    r=(sum_j ||Ctilde_j-Chat_j||F^2)^(1/2).

Given simultaneous actual data bounds ||Chat_j-C_j||op<=a, let e be any computed rational upper bound on r+sqrt(3d)*a. The completely known certificate is

    Dnorm <= 2e/kappa.                            (5)

Indeed apply (3) to the candidate model Ctilde with true algebra A and competitor B, then use the true model's global maximality F_C(B)>=F_C(A):

    (kappa/2)Dnorm^2
       <=F_Ctilde(A)-F_Ctilde(B)
       <=sum_j Tr[(A_j-B_j)(Ctilde_j-C_j)]
       <=Dnorm e.

Thus a small residual and verified positive block are sufficient to certify a physical generator triple. No candidate-dependent selection penalty beyond the simultaneous data event is needed. No unknown numerical true margin is an input. No global optimality assertion is needed for soundness. A heuristic candidate can be tried first and rejected if it lacks this certificate.

A concrete candidate coefficient construction uses the exact Pauli conditional expectation

    P_A(X)=(1/4) sum_(alpha=I,X,Y,Z) A_alpha X A_alpha,
    L_kj=P_A((A_k Chat_j+Chat_j A_k)/2),
    S_kj=(L_kj+L_jk)/2.                           (6)

Entries are Hermitian, symmetric and in A's commutant. Test block positivity directly; do NOT assume that entrywise or block positive-part clipping preserves this symmetric-entry subspace. Ctilde is reconstructed from the tested S, and its full observed residual is charged. If S has no certified positive gap, this candidate does not pass.

As A approaches B and data errors vanish, (6) approaches T: the Pauli conditional expectation removes B_k B_a for k!=a and retains T_kj. If the actual local T has a fixed positive gap, sufficiently accurate data and candidates eventually pass any fixed positive target in (5).

## 4. A finite physical candidate search, not a free nonconvex optimizer

A direct algebraic FEASIBILITY search can replace global optimization. Fix target delta>0 and a positive rational trial kappa. Impose the exact unitary/Pauli constraints, form S by(6), and ask for S>=kappa I and r<=kappa*delta/4. Require beforehand a<=kappa*delta/(4*sqrt(3d)), using a rational conservative bound. Then(5) certifies Dnorm<=delta. All residual squared norms and matrix PSD conditions are finite real-algebraic constraints; finite quantifier elimination either returns a known algebraic physical candidate or proves this particular search infeasible. A heuristic candidate may be checked first.

For completion, at A=B every coefficient error in(6) has operator norm<=a, hence ||S-T||op<=3a. Each reconstructed contrast fit has operator norm<=4a, so r<=4sqrt(3d)*a. If the actual T>=tau I and kappa<tau/2, sufficiently small a with3a<tau/2 and a<kappa*delta/(16sqrt(3d)) makes the true triple strictly feasible. Density/real-algebraic feasibility then supplies an algebraic candidate even if the true V is not algebraic. Sweep dyadic trial kappa and shrinking a over predetermined finite funded stages. A persistent true positive gap ensures eventual acceptance with sufficient funding, without giving tau to the learner. Search and algebraic arithmetic can be enormous; no efficiency advantage is claimed.

For comparison, an objective-based candidate construction is also possible:

All finite-dimensional physical Pauli triples are unitary conjugates of a fixed standard triple (up to spectator basis). Use real and imaginary entries of a d-by-d unitary U as real algebraic variables; set A_j=U(sigma_j tensor I_g)U dagger. Constraints U dagger U=I are polynomial, the unitary group is compact, and the empirical objective has rational coefficients when shadows are rational. Finite real-algebraic quantifier elimination can return an algebraic candidate within any rational zeta>0 of the global maximum. This is a terminating finite method, not a polynomial-time or practical optimizer. A dense certified rational-unitary net is an alternative with its full search and precision bill. The supplied candidate can then be checked by (6) and (5).

Finite confidence stages have predetermined caps and shrinking a,zeta. For a uniformly positive true local block gap tau, (4) implies convergence of the candidates, (6) implies a positive candidate gap, and (5) eventually accepts at any desired operator tolerance. For merely semidefinite/unexcited true blocks the finite algorithm may ABSTAIN. It requests the unknown payload only after acceptance. Throughput and conditional-on-acceptance risk are separate from the good-event guarantee.

The candidate U and S may be real algebraic. All norms, eigenvalue lower bounds and residuals must be certified by finite algebraic isolation or outward interval arithmetic. Strict acceptance guards absorb those finite uncertainties. The actual reflection gates can be compiled from the known algebraic A, with whole-process synthesis/error debits. The same received coherent three-reflection extraction circuit remains physical; no arbitrary estimated signed map is executed on the payload.

## 5. Local ordinary acquisition and continuing memory

Use all three independently random physical input axes and independent signs, plus random product-Pauli output readout. Current preparation/readout coins are private and independent of the prior source/controller state; the source cannot choose its current map based on these undisclosed coins except through their actual quantum input. The global mixer V and associated joint qubit algebra remain fixed across histories and stages. For each local envelope J, the importance-weighted signed shadow Y_(i,j)=3 1{axis_i=j} sign_i Z_J has the actual conditional contrast as mean, second moment at most3*3^|J| I and centered increment at most6*2^|J|, as in the separate three-axis acquisition source. These statistics require positive physical outputs and private current coins, not commuting spectator coefficients.

At every allowed prior history assume (1) with the SAME B and some positive operator block T_h. Conditional averaging over a bank retains (1), with Tbar>=0. Thus matrix martingale intervals control the actual predictable means even when retained quantum memory and previous measurements change T_h. There is no iid environment assumption.

For support discovery, any disjoint interval has zero signed contrast: it traces out the full true own-qubit algebra, and every term B_k T_kj has zero conditional Pauli trace. A confidence-positive local contrast norm therefore certifies overlap. Expanding an overlapping width-w interval by w-1 on either side contains the true width-w support, producing an envelope of width at most3w-2. Under a positive local block margin tau, Tr(B_j C_j)=Tr T_jj>=d tau, so the containing interval has nonzero signal. Coarse/fine finite confidence unions, actual preparation/readout count, source cap and rational guard costs remain explicit rather than replaced by an oracle for C.

Once (5) is at most delta for each acquired input-qubit triple, each X/Z operator error is at most delta. The actual3n-block coherent receiver then differs from the exact fixed inverse by operator norm at most3n delta. It transfers to arbitrary future joint source memory by the separately received complete-norm telescope, with no private-frame CP-mixture claim. A finite J-slot common controller pays J times this per-use complete error plus one bad-record and whole-process implementation allowance.

The contrasts identify a mixer/algebra, not an optimal code or all native noise. A known code decoder may follow the acquired inverse. The comparison is to the same fixed exact inverse and code operation. Local qubit preparation/control/readout, bounded supports, candidate search, finite gate synthesis, ancillas and holding are substantive resources.

## 6. Scientific scope

The new mechanism is a positive operator-block variational certificate that survives noncommuting spectator noise, plus an acquired positive-fit guard that does not require a supplied true gap or a globally optimal numerical candidate for soundness. It directly addresses the useful failure of scalar and commuting-sector whitening. It does not learn arbitrary correlated channels, certify source membership, infer an absent rank/positivity promise, solve efficient nonconvex optimization, or establish practical advantage. Existing local-unitary learning, Pauli-algebra extraction and SWAP sewing are prior machinery; the nearest primary comparison remains the separately saved Huang et al. and noisy-learning comparison.
