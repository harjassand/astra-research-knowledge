# A finite ordinary polar-inverse learner for general orientation-preserving qubit channels

28 October 2026. New candidate; independent review pending. This is a stronger alternative to the isotropic/Haar construction, not an automatic extension of its acceptance status. It targets the canonical rotation of a channel, not an inverse of irreversible noise.

## 1. Actual quantum target and access

The stationary independently restarted calibration channel is an UNKNOWN physical qubit CPTP map with Bloch action x->B x+c. Suppose det B>0 and sigma_min(B)=a>0. Physical trace-distance contraction implies ||B||op<=1. Its unique proper polar decomposition is B=R S, with R in SO(3), S positive definite. Define U_R to be the qubit unitary corresponding to R, up to irrelevant global phase. The target operation is Ad_U_Rdagger. No claim is made that removing R reverses S or c, improves a full recovery oracle, or discovers a quantum code.

This includes unknown-axis amplitude damping with nonsingular damping factor, anisotropic Pauli contraction with positive determinant, and arbitrary affine translation consistent with the CPTP condition. Negative-determinant or singular B are outside this target's stated smooth class.

After training, any joint service map A:P M->P M' followed by the SAME U_R may be used, including a coherent retained-memory completion. Training records/program must be private and inaccessible to the service source/external controller. The acquired program remains available only to the trusted decoder implementation and is NOT included in the accessible service output; it cannot be exposed through later controller or source access. Records are not mathematically traced while remaining physically accessible. The training and service interfaces must enforce this retirement. In addition, the service initial memory/input must be independent of the training data conditional on the fixed channel. The guarantee is the diamond distance of the record-AVERAGED learned inverse from Ad_U_Rdagger. It does not cover record-resolved error or unreset calibration-correlated memory. There is no complete-Pauli-source premise.

## 2. Only finite Pauli preparations and readouts are required

On each of N fresh probes independently choose u and v uniformly from {+-e_x,+-e_y,+-e_z}. An explicit bounded implementation chooses each of two axes using independent two-bit draws: accept 00,01,10 as x,y,z and reject11, with at most L draws per axis. Two additional independent bits choose the signs. Couple to the exact unbounded-uniform ideal; over N_total pilot-plus-final probes, a cap failure has probability at most 2 N_total 4^(-L). Choose L so this is at most a declared beta_rng, then abort the whole protocol on any cap failure (or debit beta_rng in record TV for a declared fallback). Each execution uses at most N_total(4L+2) random bits. If a pilot selects the final horizon, use its predeclared finite maximum N_total for this bound. Cap failures, random-bit imperfections and any forced-service fallback are charged separately; an exact unlimited geometric sampler is not assumed free. Prepare rho_u and measure v.sigma, with outcome Y in {-1,+1}. Its mean is v^T(Bu+c). Form the actual rational matrix

 M=(9/N)sum_t Y_t v_t u_t^T.

Because E u=E v=0 and E uu^T=E vv^T=I/3,

 E M=B,
 E||M-B||_F^2=(81-||B||_F^2)/N <=81/N.                     (1)

Translation cancels in the EXPECTATION, not by pretending each observed sample was unital. Every actual outcome remains a valid measurement of the original CPTP channel. The learner chooses a nearest proper rotation Q(M) in SO(3), with ANY deterministic algebraic tie rule, and implements its inverse. It is a physical unitary for every record, including singular/bad estimates.

M has rational entries from finite integer counts. A proper Procrustes minimizer can be constructed by real-algebraic eigenvalue isolation and an orientation-corrected singular decomposition; ties are resolved by deterministic algebraic basis choices. This is a terminating finite operation, not a supplied unknown source matrix. A qubit SU(2) representative follows by algebraic square roots. Finite gate synthesis/control accuracy is charged separately. Source calls and preparations/readouts are ordinary, with no protected calibration reference or continuous random controls.

## 3. Explicit mean-bias bound, not an assumed covariance symmetry

Write E=M-B, F=R^T E, O=R^T Q(M), K=O-I. Let Omega(F) be the skew-symmetric solution of

 S Omega+Omega S=F-F^T.

Its Frobenius norm is <=||F||_F/a, since the inverse Sylvester map has norm <=1/(2a). It is LINEAR in E, hence E[Omega]=0 for the fixed-horizon experiment (1).

On the good event ||E||_F<=a/2, M is nonsingular with positive determinant. Thus Q(M) is its ordinary polar factor. The elementary polar stability inequality gives ||K||_F<=2||E||_F/a. For completeness: if M=QH and B=RS, add the two polar optimality gaps; each is at least its minimum singular value times ||Q-R||_F^2/2. Their sum is Tr((Q-R)^T(M-B)), so ||Q-R||_F<=2||M-B||_F/(sigma_min(M)+sigma_min(B)). This is stronger than the displayed loose bound.

Symmetry of O^T(S+F), together with K^T=-K-K^T K, gives the EXACT identity

 S(K-Omega)+(K-Omega)S
   =-F^T K+K^T F-K^T K S.

Since ||S||op<=1 and a<=1, the Sylvester bound implies

 ||K-Omega||_F <=4||E||_F^2/a^3                          (good event). (2)

On the bad event, ||K||_F<=2sqrt(3), ||Omega||_F<=||E||_F/a,

 P(bad)<=4 E||E||_F^2/a^2,
 E[||E||_F 1_bad]<=2 E||E||_F^2/a.

Combining these with E Omega=0 yields

 ||E K||_F
 <=[4/a^3+(8sqrt(3)+2)/a^2] E||E||_F^2
 <20 E||E||_F^2/a^3 <=1620/(a^3 N).                       (3)

The same estimate holds for E[O^T-I]. Thus first-order matrix estimation fluctuations cancel in the genuinely averaged decoder; nonlinear fitting bias and bad records are explicitly second-moment controlled. No exact Haar, finite-group or isotropic symmetry is needed.

## 4. Transfer to a physical complete channel

The actual residual decoder Ad_Qdagger composed with Ad_R has Bloch matrix O^T. Its record average is a physical unital channel with Bloch difference T=E O^T-I. For the difference L of two unital qubit channels, so L(I)=0 and Tr L(X)=0, with Bloch difference matrix T, its normalized Choi matrix is

 J=(1/4)sum_(i,j) T_ij sigma_i tensor sigma_j^T,
 ||J||_F=||T||_F/2, ||J||_1<=||T||_F.

The qubit Choi bound ||L||diamond<=2||J||_1 therefore gives

 half || E[Ad_Qdagger composed Ad_R]-id ||diamond
 <=min(1,1620/(a^3 N)).                                    (4)

Composition after ANY independent joint service source A preserves (4), including arbitrary coherent physical/environment correlations. The source need not be decomposed into classical error branches. The comparison is to its specified polar-frame-corrected output, not automatically identity or an optimal recovery.

A supplied positive lower bound a0<=a lets the caller choose N>=1620/(a0^3 epsilon_fit). The constant and a dependence are not asserted optimal. This is an O(1/epsilon) ordinary-call upper bound for a fixed conditioned physical family, not a generic efficient environment-learning theorem. Arithmetic and controlled-gate resources may dominate.

## 5. Optional finite pilot to acquire a usable conditioning bound

One may acquire a lower bound without changing the fixed-horizon mean-zero proof. Use a SEPARATE independently restarted pilot of N0 probes. Each matrix sample entry lies in[-9,9]. A union bound and Hoeffding give simultaneous Frobenius radius

 r0=27 sqrt(2 log(18/beta)/N0)

with failure probability <=beta. Accept only if a rigorously computed interval proves det(M0)>0 and sigma_min(M0)>r0. Then any conservative rational/dyadic a0<=sigma_min(M0)-r0 is a valid positive lower bound on sigma_min(B), and B has positive determinant by nonsingularity along the straight segment. Exact-boundary or unresolved numerical cases may return ABSTAIN. Impose a finite declared Nmax and proceed only when the required final N<=Nmax; otherwise abstain.

The final bank is FRESH and independent of the entire pilot. Conditional on any pilot record, its chosen N is fixed and its matrix estimator is still unbiased. Thus the proof above applies conditionally, with a valid a0 on the pilot good event. Comparing protocols sharing the actual abort branch gives unnormalized final loss <=epsilon_fit+beta. Conditional-on-acceptance bounds require the acceptance denominator. This does not certify source stationarity, hidden-memory independence or promise that every finite pilot accepts. Adequate pilot cap/excitation remains a real requirement.

Using one adaptively stopped bank for both margin selection and fitting is NOT licensed by this argument; optional stopping can destroy the mean-zero cancellation. The separate pilot is part of the actual resource bill, not a free known parameter.

## 6. Controls, reuse and significance limits

Every actual inverse is an algebraically specified qubit unitary. Exact mathematical channel identities do not grant perfect physical gates. A per-probe preparation/readout discrepancy O(nu/N_total), a complete pilot/final record-TV debit and deployed decoder discrepancy O(nu) can be paid by a whole-protocol hybrid. The received endpoint compiler is an available finite synthesis dependency, not a claim that it or the present learner was executed as a production compiler.

The same random inverse reused in a long coherent process need not produce independent noise. The separate one-axis reuse result explains why J^2 sensitivity can remain; no noncommuting J-use theorem is imported here without proof. The strongest ordinary alternative is the SAME finite tomographic/proper-polar estimator. What this construction establishes is a complete operational average guarantee under private retirement and independence, including nonunital/non-Pauli calibration, not a historical novelty or practical speed advantage claim.

Original isotropic and phase constructions remain intact. This source removes their symmetry obligation for the stated one-use polar target, at looser conditioning constants and with explicit bad-fit control. A new physical or oracle-recovery advantage beyond removing the canonical frame remains an unresolved scientific obligation.
