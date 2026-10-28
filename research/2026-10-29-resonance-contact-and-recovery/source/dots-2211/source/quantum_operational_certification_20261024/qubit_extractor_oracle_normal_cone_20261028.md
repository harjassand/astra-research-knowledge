# The full channel-oracle normal cone of a qubit subsystem extractor

28 October 2026. New candidate theorem and acquisition certificate; independent internal review pending. This extends the positive-operator-block certificate at the objective level. It does NOT inherit that source's coarse localization premises or establish historical novelty.

## 1. Physical channel and conventions

Let N:M_2->M_d be any physical qubit-input CPTP channel, d=2g, and define its three ordinary signed contrasts C_j=N(sigma_j/2), j=X,Y,Z. They are Hermitian and traceless. Let B_j=U(sigma_j tensor I_g)Udagger be a fixed physical Pauli triple on the receiver. Its extraction channel is D_B=Tr_G Ad_Udagger.

Every physical CPTP decoder D:M_d->M_2 has a unital-CP adjoint with images A_j=D^*(sigma_j). In auxiliary-qubit/receiver order its unital-map Choi matrix is

 K_A=(I_2 tensor I_d+sum_j sigma_j^T tensor A_j)/2,
 K_A>=0, Tr_aux K_A=I_d, Tr K_A=d.

Set H_C=sum_j sigma_j^T tensor C_j and J_C(A)=sum_j Tr(C_j A_j). Then

 Tr(H_C K_A)=J_C(A),
 F_e(D N)=(1+J_C(A))/4.                                      (1)

The factor1/4 in fidelity is essential: all curvature statements below first concern the UNSCALED objective J_C. The N(I/2) term contributes the fixed1/4 because N,D are trace preserving.

At the subsystem extractor K_B=2P_B, where P_B is the rank-g projection onto the logical maximally entangled vector tensor the full gauge space, transported by I_aux tensor U. This full gauge support is material to the necessity statement.

## 2. Necessary AND sufficient normal-cone characterization

Define the ordered matrix

 Y_B=sum_j C_j B_j,
 Q_B=I_2 tensor Y_B-H_C.                                     (2)

Then the fixed extraction D_B maximizes entanglement fidelity among ALL CPTP decoders if and only if

 Y_B is Hermitian and Q_B>=0.                                (3)

No assumption that C_j B_j is individually Hermitian, that different gauge coefficients commute, or that a positive operator-block representation exists is required.

Proof. The exact finite SDP is maximize Tr(H_C K), K>=0, Tr_aux K=I_d. Its dual is minimize Tr Y over Hermitian Y with I_2 tensor Y-H_C>=0. The primal has a strict feasible point I_(2d)/2, is compact and finite-dimensional, so its optimum has an attained dual witness and complementary slackness applies. If B is optimal, Q K_B=0.

On P_B, the Pauli transpose identity gives

 (sigma_j^T tensor C_j)P_B=(I_2 tensor C_j B_j)P_B.

Thus complementary slackness implies [I_2 tensor(Y-Y_B)]P_B=0. The map T->(I_2 tensor T)P_B is injective: in U's frame, applying it to the maximally entangled vector tensor EACH gauge basis vector forces T to vanish on both logical basis states for every gauge vector. Hence Y=Y_B, proving necessity including Hermiticity and the displayed operator order.

Conversely (3) supplies an actual dual feasible matrix. The same transpose identity gives Q_B P_B=0, so its objective equals Tr(H_C K_B). Primal/dual equality proves global optimality. Symmetrizing a non-Hermitian Y_B without re-establishing the exact kernel is NOT this certificate.

## 3. A complete curvature bound

Suppose the stronger known or true margin is

 Q_B>=mu(I_(2d)-P_B), mu>0.                                 (4)

For any unital-CP candidate A,

 J_C(B)-J_C(A)=Tr(Q_B K_A)>=mu Tr[(I-P_B)K_A].

The Pauli expansion gives

 Tr[(I-P_B)K_A]=(3d-sum_j Tr(B_j A_j))/4.

Unital positivity implies -I<=A_j<=I, so sum_j Tr A_j^2<=3d. Therefore

 sum_j ||A_j-B_j||_F^2 <=8 Tr[(I-P_B)K_A],
 J_C(B)-J_C(A)>= (mu/8) sum_j ||A_j-B_j||_F^2.               (5)

For two PHYSICAL Pauli triples the first inequality is equality. The actual entanglement-fidelity gap is at least mu/32 times the squared distance, by(1). A strict margin identifies the extractor's complete adjoint uniquely; it does not imply that its attained fidelity is close to one.

For a feasible empirical optimizer within zeta of the unscaled empirical optimum, with coefficient error E=(sum_j||Chat_j-C_j||_F^2)^(1/2), (5) gives

 D<=[4E+sqrt(16E^2+8mu zeta)]/mu,
 D=(sum_j||A_j-B_j||_F^2)^(1/2).                             (6)

At zeta=0 this is8E/mu. The output A may be a nonunitary decoder; it must be physically rounded before being used as reflection gates. The earlier exact sign/odd-polar rounding remains a separate mechanism, not a consequence of SDP feasibility.

## 4. An acquired fitted-normal-cone certificate

Assume the TRUE fixed B is full-CPTP oracle-optimal for the actual C, without supplying its margin. Construct any EXACT physical candidate Pauli triple A, and known Hermitian coefficient matrices Ctilde_j. They need not describe a physical noise channel; they are a mathematical fitting certificate. Tracelessness or full source-channel feasibility can optionally be imposed, but is not needed for the following implication.

Form P_A=K_A/2, Y_A=sum_j Ctilde_j A_j and verify EXACTLY

 Y_A=Y_A^dagger,
 I_2 tensor Y_A-sum_j sigma_j^T tensor Ctilde_j
       >=kappa(I-P_A), kappa>0.                              (7)

For a fixed candidate A these are linear equality/PSD constraints in Ctilde and kappa, with a convex residual-fit objective. All coefficients are known. Exact algebraic constraints or certified outward bounds must enforce the kernel and Hermiticity; a small floating residual cannot simply be ignored because the prescribed kernel has zero eigenvalues.

If e is a verified upper bound on (sum_j||Ctilde_j-C_j||_F^2)^(1/2), then

 (sum_j||A_j-B_j||_F^2)^(1/2) <=8e/kappa.                    (8)

Indeed use candidate curvature (5) against the true physical B, then true optimality J_C(B)>=J_C(A):

 (kappa/8)D^2<=J_Ctilde(A)-J_Ctilde(B)
             <=sum_j Tr[(Ctilde_j-C_j)(A_j-B_j)]<=eD.

A simultaneous ordinary-data bound supplies e by measured residual plus data/finite-arithmetic allowances. Candidate-dependent selection is harmless on that same simultaneous event. This is a certificate of proximity UNDER the true oracle-normal-cone premise; fitting (7) alone does not certify unknown source membership, a common global mixer, locality or held-out future stationarity.

The positive-operator-block source is a sufficient subcone: its block floor tau yields Q_B>=4tau(I-P_B). Then(5) reduces to its tau D^2/2 curvature and(8) to2e/tau. The present cone is strictly larger, as the physical examples below show.

## 5. Exact physical examples outside the positive-block subcone

### A. Negative scalar contraction with identity still oracle-optimal

Take a qubit Pauli channel with probabilities

 (p_I,p_X,p_Y,p_Z)=(2/5,3/10,3/10,0).

Its Bloch contractions are (2/5,2/5,-1/5), so C_j=lambda_j sigma_j/2. For B_j=sigma_j, Y_B=3I/10 and Q_B has eigenvalues0,1/5,1/5,4/5. Thus mu=1/5, the identity decoder is uniquely full-CPTP oracle-optimal, and its entanglement fidelity is2/5.

The unique scalar coefficient block in C_j=sum_k B_k T_kj is diag(1/5,1/5,-1/10), which is not PSD. Hence this physical strict normal-cone example is outside the earlier positive-block family. High oracle quality is not implied by a strict identification gap.

### B. Gauge-only input contrast, yet extraction remains full oracle

Let output be logical L tensor gauge G, both qubits. For input Bloch vector r, define

 N(rho)=[I_4+lambda sum_j r_j sigma_j tensor I_2
                    +epsilon r_Z I_2 tensor Z]/4,
 lambda=1/2, epsilon=1/4.

Its normalized Choi matrix is

 J_N=[I_8+lambda sum_j sigma_j^T tensor sigma_j tensor I_2
                   +epsilon Z^T tensor I_2 tensor Z]/8.

The depolarizing part has minimum eigenvalue(1-lambda)/8, and the perturbation norm is epsilon/8, so J_N>=I_8/32. Tr_output J_N=I_2/2; hence this is an actual CPTP channel.

For B_j=sigma_j tensor I_2,

 C_j=lambda B_j/4+delta_(j,Z) epsilon I_2 tensor Z/4,
 Y_B=3lambda I_4/4+epsilon Z tensor Z/4,
 Q_B=lambda(I-P_B)+(epsilon/4)(I_aux tensor Z_L-Z_aux^T tensor I_L) tensor Z_G.

The second term annihilates P_B and has norm epsilon/2, so Q_B>= (lambda-epsilon/2)(I-P_B)=3(I-P_B)/8. This gap is attained. Extraction is uniquely full-CPTP oracle-optimal with F_e=(1+3lambda)/4=5/8.

The gauge-only I_L tensor Z_G term in C_Z cannot belong to any sum_k B_k T_kZ with T in B's commutant: every such sum has zero partial trace over L. Thus this is another strict enlargement, not just a scalar sign exception.

CRITICALLY, Tr_L C_Z=epsilon Z_G/2 is NONZERO on the gauge-only output. A coarse rule declaring every disjoint-from-logical-support signed marginal zero is therefore false for this channel. Normal-cone optimality alone does not justify earlier support localization, even though the desired B has exactly on-site logical support. A new acquisition/support mechanism is required before transferring this cone to a global local-inverse theorem.

## 6. Boundaries and exact operational meaning

A physical rotated unitary source already shows why Hermiticity matters: for C_X=Y/2,C_Y=-X/2,C_Z=Z/2 and B=standard Paulis, Y_B=I/2-iZ is not Hermitian. The identity extractor is not optimal; the inverse rotation is. Replacing Y_B by its Hermitian part is not a legitimate complementary witness.

At zero margin the characterization remains valid but does not identify a unique extractor or supply curvature. For example a source with all C_j=0 has Q_B=0 and every decoder has the same fidelity. The normal cone says nothing by itself about noise capacity, adaptive-source promises, calibrated control accuracy, physical register access, common-global-algebra compatibility, or a practical advantage over equally informed conventional recovery SDPs. The new scoped result is the exact characterization, its curvature/acquired-fit consequence, and explicit wider physical examples with a localization failure retained.
