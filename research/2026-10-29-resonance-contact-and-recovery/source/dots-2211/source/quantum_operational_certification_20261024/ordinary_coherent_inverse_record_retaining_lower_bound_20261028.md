# Ordinary coherent inverse acquisition: a record-retaining lower bound and its limit

28 October 2026. New candidate; independent review pending. This is a lower bound for an explicitly stronger, record-retaining loss. It is NOT automatically a lower bound for a deployed channel after calibration records are discarded.

## 1. Actual family and permitted resources

Fix a known p in (0,1/2). Every source use is independently initialized and implements the isometry

 A|psi> = sqrt(1-p)|psi>|0>_M + sqrt(p) Z|psi>|1>_M,
 N_theta = (V_theta tensor I_M) A, V_theta=exp(-i theta Z).

Calibration has N fresh uses. On each use the learner prepares an arbitrary physical qubit state, obtains an arbitrary measurement outcome on the physical output only, and may adapt preparation/measurement to all earlier CLASSICAL outcomes. No source memory M is accessible. Fresh ancillas within a probe are also harmless to the fidelity bound below, but no coherent register is carried between probes. Classical randomness is included in the record. The final decoder D_y is an arbitrary qubit CPTP map depending on record y; it need not be a fitted unitary. The hidden angle can be promised to the learner to belong to just two values. Thus the lower bound is not due to a hard model search.

At service, use the fixed input |+>. The exact inverse comparator applies V_theta^dagger to the physical output and leaves the source memory untouched. Its complete output is Psi=A|+>, independent of theta. Define

 l_theta(D) = (1/2)|| (D Ad_Vtheta tensor id_M)(|Psi><Psi|) - |Psi><Psi| ||_1,
 R_theta = E_(y~P_theta) l_theta(D_y).

This R_theta is exactly the half trace distance between the REAL and REFERENCE classical-record-plus-service states when both keep y with its SAME actual law P_theta. It also equals expected conditional service loss. An arbitrary later controller that may read the record and access the relevant retained memory can detect this distinction. We do not assert a lower bound for a port that never exposes these memory distinctions, nor for the norm after y is traced out.

## 2. One decoder cannot invert both nearby orientations accurately

Psi has Schmidt coefficients sqrt(1-p),sqrt(p) across physical output/memory. For any Hermiticity-preserving qubit map L, invertible filtering on the memory converts (L tensor id)(Psi) to its normalized Choi matrix (in the |+>,|-> input basis). The inverse filter has squared operator norm 1/(2p), so

 ||J_normalized(L)||_1 <= ||(L tensor id)(Psi)||_1/(2p).

The elementary qubit Choi inequality ||L||diamond <= 2||J_normalized(L)||_1 then gives

 (1/2)||D Ad_Vtheta-id||diamond <= l_theta(D)/p.       (1)

One proof of the Choi inequality writes every pure input/reference state as (I tensor B)|Phi>, with ||B||op^2<=2; convexity covers mixed inputs, and a qubit reference suffices for the diamond norm. No channel model is inferred from this inequality.

Choose theta_plus=delta and theta_minus=-delta with 0<2delta<=pi/2. By unitary precomposition invariance, triangle inequality and the exact qubit unitary distance,

 l_plus(D)+l_minus(D)
   >= p (1/2)||Ad_Vplus^dagger-Ad_Vminus^dagger||diamond
   = p sin(2delta).                                           (2)

This holds for every CPTP D, including nonunitary, randomized and highly inefficient decoders.

## 3. Fresh ordinary calibration cannot separate the two laws too quickly

Condition on an identical classical history y_<t. Both worlds use the SAME prepared state and measurement. Purify the prepared state if needed, and retain a purification of A's output only for the mathematical fidelity bound. The two purifications differ by exp(-i 2delta Z) on the physical qubit. Their overlap has magnitude at least cos(2delta): for any density rho,

 |Tr(rho exp(-i 2delta Z))| >= cos(2delta).

Discarding inaccessible registers and measuring cannot decrease root fidelity. Therefore every pair of conditional outcome laws has Bhattacharyya coefficient at least c=cos(2delta). Inductively summing the classical history tree gives

 BC(P_plus,P_minus) >= c^N,
 TV(P_plus,P_minus) <= sqrt(1-c^(2N)) <= sqrt(N) sin(2delta). (3)

This proof permits arbitrary classical adaptation and fresh within-probe ancillas, and does not grant a coherent multi-query strategy. Random coins are included with the same law in both worlds. Fixed caps with fewer than N uses can be padded by uninformative outcomes.

Integrating (2) against the overlap min(P_plus,P_minus) gives

 R_plus+R_minus >= p sin(2delta) [1-TV(P_plus,P_minus)].       (4)

For N>=1 take delta=1/(4 sqrt(N)). Then TV<=1/2, and sin(2delta)>=1/(pi sqrt(N)). Consequently

 max(R_plus,R_minus) >= p/(4 pi sqrt(N)).                    (5)

A uniform record-retaining guarantee R_theta<=epsilon therefore requires

 N >= p^2/(16 pi^2 epsilon^2).

The constants are deliberately loose. The scaling matches the inverse-square precision dependence of the coherent operator-norm fallback in its ordinary, complete-record metric. It is not a lower bound for its n/locality factors, or for protocols with coherent multi-use interrogation, source-memory access, different target/comparator, or discarded-record average loss. Both source worlds have strictly positive X contrast 1-2p and Z contrast 1; lack of excitation is NOT the cause of (5).

## 4. Why discarding the calibration record changes the problem

For a simple exact cancellation example, take true theta=0 and choose the decoder W_s=exp(-i s delta Z), where s=+1 or -1 equiprobably and the sign is independent of the source. Since <Psi|Z tensor I|Psi>=0, each conditional complete output has loss |sin(delta)|. Thus retaining s gives that same loss.

After s is discarded the actual decoder channel is

 (Ad_Wplus+Ad_Wminus)/2 = cos^2(delta) id + sin^2(delta) Ad_Z.

Psi and (Z tensor I)Psi are orthogonal. Its averaged complete output loss is therefore EXACTLY sin^2(delta), not |sin(delta)|. This is not an acquired estimator or a proof of a globally achievable 1/N learner; it is an explicit reason why (5) cannot be applied to a record-discarded loss by Jensen in the wrong direction.

A useful next question is whether an actual unbiased/covariant ordinary estimator can exploit this cancellation uniformly in theta, while retired records remain genuinely inaccessible to subsequent controllers and source interactions. Any such result would concern a different operational interface, not refute (5).

## 5. Zero-contrast boundary

At p=1/2 the reduced calibration channel is complete Z dephasing, unchanged by V_theta. All system-only calibration records are identical for every theta, no matter N. Equation (2), now with p=1/2, gives a constant record-retaining lower bound for two fixed separated angles. This separate obstruction violates strict X excitation and is NOT used to establish the positive-gap lower bound (5).

This note supplies an analytical minimax claim and reproducible finite checks, not a hardware result, a generic no-go theorem for unknown-noise recovery, or a historical novelty claim. It concerns the exact resource and comparator definitions above. Parent sources remain intact.
