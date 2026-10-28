# Exact entanglement-breaking boundary and constructive assisted entanglement for pure-success/reset channels

26 October 2026. Source-specific application of standard pure-state random robustness, local filtering and recurrence/hashing, with self-contained acquisition below. Independent PASS: `pure_success_reset_eb_assisted_classification_independent_audit.md`. No claim of novelty of those general ingredients, no unrestricted WH3 entropy theorem and no unassisted quantum-capacity claim.

## 1. Complete channel-family classification

Consider E(rho)=pVrhoV*+qTr(rho)tau, V:C3->R an isometry, p+q=1. Use X=dP_OmegaV+I3 tensor Y, T=3d+3TrY, p=3d/T, qtau=3Y/T. Let G=V*Pker(Y)V.

* p=0: the replacer is entanglement breaking (EB).
* p>0 and G!=0: the channel is NOT EB and admits a strictly positive two-way-classically assisted entanglement-generation rate.
* p>0 and G=0: restrict to suppY (which contains ranV), and let r1>=r2>=r3>0 be the eigenvalues of R=V*Y^+V. Then

E is EB  iff  d sqrt(r1 r2)<=1.                          (1)

At strict reverse inequality it has a constructive positive assisted entanglement rate. Equality in(1) is separable, not an unresolved PPT boundary. If q=0, Y=0, the channel is reversible and the non-EB conclusion is immediate.

For faithful reset density tau, condition(1) is equivalently
p sqrt(lambda1 lambda2)<=q,
where lambda1,lambda2 are the two largest eigenvalues of V*tau^-1V.

This class therefore has no EB-versus-positive-assisted-rate gap. This is not a statement about arbitrary quantum channels or their unassisted capacities.

## 2. Actual whitening and self-contained separable decomposition

When G=0, remove the unused kernel of Y and whiten the reference by Y^-1/2. The actual unnormalized Choi operator becomes

I3 tensor I_suppY + d P_psi,
psi=(I3 tensor Y^-1/2 V)Omega3.

The nonzero squared Schmidt coefficients of psi are r1,r2,r3, WITHOUT normalizing their sum. In a Schmidt basis write psi=sum_i sqrt(r_i)|ii>. The partial transpose has antisymmetric-pair eigenvalues1-d sqrt(r_i r_j). Thus d sqrt(r1r2)>1 is NPT.

Conversely define product vectors
alpha_theta=sum_i r_i^(1/4) exp(i theta_i)|i>,
beta_theta=sum_i r_i^(1/4) exp(-i theta_i)|i>.
Average their product projectors over independent phases. This average equals
P_psi+sum_(i!=j) sqrt(r_i r_j)P_|ij>.
A finite average over three cube-root phases for each of the three labels suffices, because all nonzero phase exponents have absolute value at most2. Therefore

I+dP_psi = d Average(P_alpha tensor P_beta)
 +sum_i P_|ii>
 +sum_(i!=j)[1-d sqrt(r_i r_j)]P_|ij>
 +identity on reference Schmidt spectators.

Every coefficient is nonnegative under(1), including the equality boundary. This is an explicit separable cone decomposition. Invertible local whitening preserves separability in both directions. Finally, separability of a TP Choi state is equivalent to EB: a decomposition sum_j w_j alpha_j tensor beta_j gives POVM effects3w_j alpha_j^T, whose sum isI because the Choi input marginal isI/3. This also explains why EB channels cannot create entanglement under arbitrary adaptive LOCC use without pre-shared entanglement.

The white-noise/pure-state boundary is established prior art: Vidal and Tarrach, *Robustness of entanglement*, arXiv:quant-ph/9806094, Eq.(41) and AppendixB, give random robustness from the two largest Schmidt amplitudes. The primary PDF was inspected on26 October2026: https://arxiv.org/pdf/quant-ph/9806094 . The decomposition above supplies the conventions and source acquisition needed here.

## 3. A physical distorted-success receiver for every faithful non-EB case

Let W:C2->C3 contain the top-two eigenvectors of R and R_W=diag(r1,r2). Set

Q=Y^-1/2 V W R_W^-1/2, Q*Q=I2,
J=Q*Y^-1/2=R_W^-1/2 W*V*Y^-1,
kappa=||J||^-2, K=sqrt(kappa)J.

K is a fixed contraction with an erased rejection branch. Here kappa is a CP scaling factor, NOT an identity-throughput fraction and need not be<=1. The sender prepares a Bell pair of qubits locally, retains one half and encodes the transmitted half by W. The receiver applies K.

The accepted Bell-half state is exactly

(3kappa/(2T))[I4+dP_chi],
chi=sqrt(r1)|00>+sqrt(r2)|11>.

Its success probability and Bell fidelity are

a=(3kappa/(2T))[4+d(r1+r2)]>0,
F=[1+(d/2)(sqrt(r1)+sqrt(r2))^2]/[4+d(r1+r2)],
F-1/2=[d sqrt(r1r2)-1]/[4+d(r1+r2)]>0.

This decoder deliberately DISTORTS the reversible success Schmidt weights. For arbitrary unknown qubit inputs its heralding probability can depend on the input. No input-independent conditional channel or undistorted-success claim is made. The entanglement-generation protocol uses the specified Bell halves, for which a is fixed and explicitly charged.

## 4. Recurrence followed by hashing: positive rate with all losses paid

A bilateral twirl preserving Phi2 converts the accepted state to an isotropic Bell-diagonal distribution(F,(1-F)/3,(1-F)/3,(1-F)/3). Shared random local Clifford operations suffice; unlike a Pauli-only twirl, this also equalizes the three non-target Bell probabilities. Acceptance information is returned from receiver to sender so both retain the same pairs.

After EVERY recurrence round, reapply the fidelity-preserving bilateral Clifford twirl before using the scalar recurrence again. The un-twirled recurrence output is generally Bell diagonal but not isotropic. This free LOCC step leaves its target fidelity and passing probability unchanged.

For F in(1/2,1), the standard recurrence step has
Ppass(F)=F^2+2F(1-F)/3+5(1-F)^2/9,
R(F)=[F^2+(1-F)^2/9]/Ppass(F).
It retains fraction Ppass(F)/2 of input pairs. Exactly R(F)-F=(1-F)(2F-1)(4F-1)/(8F^2-4F+5)>0 on (1/2,1). The only fixed point above 1/2 is 1, so monotone iteration converges to 1. After a finite number k of steps, F_k>=13/16. Then one-way hashing has positive yield1-H2(F_k,(1-F_k)/3 repeated3).

Thus an explicit achievable rate per ORIGINAL channel use is

a * product_(j=0 to k-1)[Ppass(F_j)/2]
  *[1-H2(F_k,(1-F_k)/3,(1-F_k)/3,(1-F_k)/3)] >0.          (2)

Every factor is charged. It can be extremely small near the EB boundary; no uniform positive lower rate is asserted. Independent memoryless uses, known/calibrated source parameters, local quantum operations, shared randomness and two-way classical communication are assumed. Recurrence uses two-way communication; hashing later uses one-way communication. No experimental implementation or finite-blocklength error guarantee is asserted.

The standard protocol and formulas are directly verified in Bennett, DiVincenzo, Smolin and Wootters, *Mixed State Entanglement and Quantum Error Correction*, arXiv:quant-ph/9604024v2, §3.2.1 Eqs.(42)-(43) and §3.2.3: https://arxiv.org/pdf/quant-ph/9604024 . This is prior art, not a new recurrence/distillation theorem.

## 5. Singular visible kernels, including rank-one overlap

If G!=0 and d>0, set B=||Y||, g1=||G||>0. Choose epsilon>0 with epsilon(B+epsilon)<d^2 g1; for example

epsilon=[sqrt(B^2+d^2 g1)-B]/2,

which makes the product d^2 g1/4. Define R_epsilon=V*(Y+epsilon I)^-1V. Its largest eigenvalue is at leastg1/epsilon, and its second largest is at least1/(B+epsilon). Thus d sqrt(r1_epsilon r2_epsilon)>1.

Build the finite physical receiver of §3 using Y+epsilon I, but apply it to the ORIGINAL Y. The actual accepted reset covariance is
N=JYJ*=I2-epsilon JJ*, 0<=N<=I2.
The accepted Bell state is proportional I2 tensor N+dP_chi. Its unnormalized Bell-fidelity witness is

<Phi|S|Phi>-(TrS)/2 = d sqrt(r1r2)-(TrN)/2 >0.

Therefore its actual F exceeds1/2, and §4 applies using its ACTUAL success probability and fidelity. No fictitious added reset is implemented. This proves positive assisted rate even when rankG=1, where exact noiseless qubit acceptance is impossible by the separately received kernel classification.

If YV=0, the stronger simple code projection already gives perfect accepted Bell pairs at probabilityp; the regularized proof need not be used. If G=0 but Y has an external kernel, it is removed as in §2 and the faithful-on-support criterion applies. These cases exhaust singular reset support configurations.

## 6. Comparator scope and relation to earlier capability

The earlier optimal encoded-qubit left inverse minimizes conditional noise while preserving success exactly, but it is not optimal over Schmidt-distorting filters. The present receiver deliberately changes class. It may reveal distillability even when the best undistorted-success channel, after Pauli twirl, has Bell fidelity at most1/2. Neither conditional-fidelity optimization nor this constructive recurrence rate is claimed globally rate-optimal.

The EB side has zero assisted entanglement-generation capacity because EB maps are measure-and-prepare and preserve separability under adaptive LOCC. The non-EB side has a positive rate by(2). If one uses free classical teleportation to convert distilled Bell pairs to quantum transmission, this also establishes positivity of two-way-classically assisted quantum capacity for this FAMILY. It gives no unassisted capacity conclusion and no implication for the still-open original WH3 entropy value outside received regions.

## 7. Executed source fixtures

The checker `pure_success_reset_eb_distillation_check.py` acquires the actual encoded channel Choi operator and applies its physical contraction, rather than evaluating only a target Bell vector.

A faithful coherent example uses d=4, V=[I3;0], A=diag(1,9,100), D=diag(1,2,3), C=(1/10)[[1,1,0],[0,1,1],[1,0,1]], and Y=[[A+CD^-1C*,C],[C*,D]]. Then R=A^-1, so d sqrt(r1r2)=4/3. The filter gives F=41/76>1/2. Its charged acceptance is approximately0.03474016; twelve recurrence steps followed by hashing give approximately1.15965e-9 ebits per original use. The small number is retained, not replaced by conditional yield. In contrast, the optimal undistorted-success noise trace is10, so its Pauli-twirled Bell fidelity is13/28<1/2. This comparison only concerns that twirled state: its untwirled output may still be distillable by subsequent filters.

This graph is genuinely irreducible with respect to code versus exterior: a projection commuting with Y and Pcode is block diagonal. Since D is simple its exterior block is diagonal; the cross equation and its adjoint force that block to commute with C*C. Every off-diagonal entry of C*C is nonzero, so the exterior block is scalar; invertibility of C forces the code block to be the same scalar. There is no nontrivial common reducing projection.

A singular example uses V=I3, Y=diag(0,1,1), d=1/2. Its visible kernel has rank one, hence no exact noiseless qubit can be extracted at positive rate. The regularized filter nevertheless gives actual F approximately0.64104034 and acceptance approximately0.12786405. Six recurrence steps followed by hashing give approximately3.55700e-5 ebits per original use. The checker also reconstructs the explicit 27-product separable decomposition at the faithful boundary d=3,r=(1,1/9,1/100).
