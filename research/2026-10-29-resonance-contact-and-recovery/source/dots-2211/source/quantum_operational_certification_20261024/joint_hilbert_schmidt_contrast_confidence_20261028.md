# Direct joint Hilbert–Schmidt confidence for ordinary XYZ contrast records

28 October 2026. **New statistical addendum; independent receiving pending.** This improves the finite certificate's statistical representation. It does not change raw outcomes, retroactively certify a failed hardware implementation, or supply a future-channel stationarity assumption.

## 1. Actual record vector and its exact norm

Fix a known physical output patch of w qubits, dimension d=2^w, and one prepared logical input. The patch is selected before its fresh bank; alternatively every same-bank selectable patch must be included in the finite union budget Q. The bank horizon is fixed in advance or chosen using only earlier records, and all allowed stage/horizon choices are included in Q. Same-bank optional horizon selection is not silently covered. Every block independently chooses the input axis uniformly from X,Y,Z and an independent uniformly random sign in {−1,+1}, and performs independent uniform Pauli readout on the w physical outputs. Prior source memory/history can be arbitrary under the established private-current-coin and positive physical-output interface.

The local shadow is Z=tensor_l(3 Pi_l-I), where each factor has eigenvalues 2,-1 and squared Frobenius norm five. Stack the THREE actual signed contrast records into one REAL Hilbert space of Hermitian matrices:

    Y=(Y_X,Y_Y,Y_Z), Y_j=3*1{axis=j}*sign*Z,
    <A,B>=sum_j Re Tr(A_j B_j),  m=3d².

Exactly one block is nonzero, so every actual record, regardless of its Born outcome, has

    ||Y||_F²=9*5^w=:v.                                      (1)

Given the complete prior record, its mean C_h=(C_X,h,C_Y,h,C_Z,h) is the actual signed contrast vector. Each contrast is half the difference of normalized positive output states, so ||C_j,h||1<=1 and ||C_h||_F<=sqrt(3). This does not require a Pauli source, a positive operator-block representation, reset, independent source memory or a supplied numerical gap.

Let X_h=Y_h-C_h, expressed in any fixed real orthonormal Hermitian basis. It is a real m-dimensional martingale difference. Its Euclidean norm is the stacked matrix Frobenius norm. The bounds are

    ||X_h||<=R:=3*5^(w/2)+sqrt(3),
    E_(h-1)||X_h||²=v-||C_h||²<=v.                           (2)

A rational upper bound on R may be used; for w=2 take R=17 and v=225.

## 2. Rectangular dilation gives a rigorous adaptive bound

Use the symmetric (m+1)-dimensional matrix difference

    D_h = [ 0, X_h^T ; X_h, 0_(m) ].

Its norm is ||X_h||, its conditional mean is zero, and its squared conditional expectation has scalar upper block E||X_h||² and lower block E X_h X_h^T. Both are <=v times their respective identities. Therefore the predictable matrix variance after N records is <=Nv I. Also the largest eigenvalue of sum_h D_h equals ||sum_h X_h||.

Apply the matrix Freedman theorem to this explicit dilation. The primary input is Joel A. Tropp, 'Freedman's inequality for matrix martingales', Electronic Communications in Probability 16 (2011), Theorem 1.2 and rectangular Corollary 1.3, pages 264–265: https://tropp.caltech.edu/papers/Tro11-Freedmans-Inequality.pdf and https://arxiv.org/abs/1101.3039 . The theorem bounds a matrix martingale tail using a uniform increment bound and predictable quadratic variation; no source-specific variance estimate or iid assumption is imported.

For Chat=N^(-1)sum_h Y_h and the ACTUAL predictable average Cbar=N^(-1)sum_h C_h,

    Pr[||Chat-Cbar||_F >= t]
       <=(m+1) exp[-N t²/(2(v+R t/3))].                    (3)

There is no extra factor two: the maximum eigenvalue of the dilation already equals the two-sided vector norm. The dimension factor is m+1=3d²+1, not the original physical d. This is a standard rectangular concentration application, not a new probability theorem.

For a supplied finite union budget of Q patch/bank processes and total statistical failure beta, choose L>=log((m+1)Q/beta). Then a valid joint radius is

    eta=[R L/3+sqrt((R L/3)²+2NvL)]/N.                     (4)

All confidence parameters and the finite union family are declared before using the selected record. Existing data can be analyzed by this separately justified bound because its event was defined without selecting among outcomes, but an adaptive choice among many new bounds must pay their selection/union budget rather than cherry-pick the smallest empirical result.

Use an outward rational eta_plus, verified by the exact polynomial inequality

    N eta_plus² - (2RL/3)eta_plus - 2vL >=0,
    eta_plus>=0.                                           (5)

A positive integer L can be justified by a rational lower bound on exp(L), for example a finite positive Taylor partial sum exceeding (m+1)Q/beta. Thus no uncontrolled floating log/root is needed for an acceptance certificate.

## 3. Integration into acquired positive-fit and native-task certificates

For an exact physical candidate Pauli triple A and exact own-commutant symmetric fitted block S>=kappa I, let r be the full stacked Frobenius residual between its known model Ctilde and Chat. Replace the older conversion sqrt(3d)*a by the directly acquired eta:

    ||Ctilde-Cbar||_F<=r+eta=:e.                            (6)

The already proved complete inverse identification certificate, under the true positive-operator model and common fixed algebra, becomes ||A-B||_F<=2e/kappa. It retains every physicality, source-membership, implementation, acceptance and future-memory condition of the governing theorem.

The separate quadratic native-oracle certificate can use e²/(8kappa). That statement concerns the native channel whose contrasts are Cbar. For a stationary source, Cbar equals the source's fixed contrasts. For a drifting/adaptive source, it is only the actual predictable calibration-average channel. No concentration theorem turns it into a certificate for an arbitrary next native channel. Future task use needs stationarity, a separately proved drift/transfer bound, or the stronger fixed-algebra inverse guarantee with its own accuracy requirement.

Candidate A,S may be selected using the same records: inequalities (3),(6) hold simultaneously and the deterministic certificate is uniform over candidates. There is no need to pretend their fitted residual is independent of Chat. An equally informed ordinary recovery learner can use this same confidence bound. No new sample advantage over such a comparator is asserted.

## 4. Concrete two-output-qubit forecast and limits

For the small sampled pilot, w=2,d=4,m+1=49,R=17,v=225. Taking L=12 covers up to Q=32 finite patch/bank processes at beta=.01 because exp(12)>49*32/.01; the finite Taylor check is included in the program. It therefore covers the 12 original banks plus a predeclared bounded continuation, without unlimited optional sampling.

At N=65,536, eta=.28809, versus the previous stacked conversion sqrt(12)*.1875=.64952. This is an improved but still conservative confidence radius. It does NOT by itself make the existing inverse or one-percent native-task guards pass.

At N=2^22, eta=.03590. If a future observed candidate has a certified kappa=.04 and residual at most .004, the quadratic native-oracle bound would be at most .005. This is a CONDITIONAL funded-sample forecast, not a claim a future bank has passed. The candidate search, exact rational physicality/gap/residual checks, native-task interface, gate implementation and raw record storage still have to be executed before any accepted result is claimed.

The statistical bound is for ideal declared ordinary records. Finite random samplers, calibration-control discrepancies, actual state preparation/readout errors and service controls retain their own norm/record-law allowances. A sampled simulation is not a hardware calibration experiment or a demonstration of arbitrary quantum memory dynamics.
