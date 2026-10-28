# Independent approximate-on-site acquisition derivation

28 October 2026. Independent derivation for the approximate-on-site extension, not a receipt for the parent manuscript. Originals are unchanged. This note concerns ordinary acquisition only; it does not itself prove the future-memory recovery loss. No source samples, acquired counts, hardware calls, or empirical performance claims.

## Setup

Use the complete nonanticipating Pauli/gauge source of `ordinary_local_multilogical_prequential_contractions_20261028.md`. Its fixed true logical reflections are B_(i,j)=U(sigma_(i,j) tensor I)U†. Assume there exist fixed on-site proper Pauli pairs A_(i,X), A_(i,Z), at unknown sites pi(i), with

    ||A_(i,j)-B_(i,j)||op <= tau, j=X,Z, 0<=tau<=1/4.

The A pairs are exactly Pauli/orthogonal; no approximate feasibility issue is hidden here. The supplied conditional CP margin is kappa>0. At any complete prior history, the signed contrast for a uniformly signed j input on logical i, after averaging all other current logical inputs, is

    Delta_j=B_j R_j, R_j>=0, [R_j,B_(k,l)]=0,
    lambda_j=Tr R_j in [kappa,1].

This is a mathematical conditional expectation, not an observed contrast oracle. The CP/gauge maps and conditional gauge state can change with history. Only U, the true B and the approximate on-site A are fixed. All conclusions below apply to averages over arbitrary such histories.

## 1. A useful exact quadratic identity

For any reflection A close to B and positive R commuting with B,

    Re Tr(A B R)=Tr R - (1/2)Tr((A-B)^2 R).

Here Tr(ABR) is real because BR is Hermitian. Consequently, with A=a.sigma on its site, the Bloch vector m of the reduced traceless contrast obeys

    a.m >= lambda(1-tau^2/2),
    |m| = ||Delta_site||1 <= ||Delta||1 = lambda.

The second inequality is trace-norm contractivity on Hermitian operators, and the final equality follows from R>=0, [B,R]=0, and B^2=I. Set c=1-tau^2/2. These inequalities imply BOTH

    |m-lambda a| <= tau lambda,
    |m/|m|-a| <= tau.                                 (A)

For the first inequality, expand the square and use |m|<=lambda. For the second, a.m/|m|>=c because |m|<=lambda; c>0 ensures m!=0. Thus the bias is relative to the same contrast magnitude lambda, not a flat O(tau) perturbation that must later be divided by kappa.

For an adaptive average, Rbar is still positive, commutes with all fixed B, and has trace lambdabar>=kappa. The SAME statements apply to mbar with lambda=lambdabar. No iid or constant-margin inference occurs.

## 2. Coarse leakage and the correct robust selector

For a candidate site ell different from pi(i), A_(i,Z) acts entirely on the subsystem traced out. Since B_Z Delta_X B_Z=-Delta_X,

    2 (Delta_X)_ell
      = Tr_rest[A_Z Delta_X A_Z-B_Z Delta_X B_Z].

The operator inside the partial trace is Hermitian, and telescoping its two unitary factors yields

    ||(Delta_X)_ell||1 <= tau ||Delta_X||1 = tau lambda_X.

Averaging histories gives wrong-site norm<=tau lambdabar_X, whereas the true site has norm>=c lambdabar_X by (A). Therefore the deterministic average-score gap is

    (c-tau)lambdabar_X >= (c-tau)kappa.                (B)

Crucial algorithm change: choose the site with MAXIMUM finite trace-norm score, breaking ties by a declared fixed ordering. Do not retain the exact-on-site first-above-kappa/2 selector. The latter can mistakenly accept leakage when tau>kappa/2 even though robust matching remains easy.

The unchanged coarse bank

    L0=ceil log2(8 q n/beta),
    N0=ceil(3072 L0/kappa^2)

gives all empirical trace-norm errors<=kappa/8 with failure probability<=beta/2, as proved by the conditional matrix martingale bound in the exact source. Finite score evaluation error<=kappa/16 adds to give per-score error<=3kappa/16. At tau<=1/4,

    c-tau >= 23/32,
    true estimated score - wrong estimated score >=11kappa/32>0.

Thus every MAX-score site is correct. No condition tau=O(kappa) is required. Missing/duplicate match guards remain physical fallbacks, but do not certify source-family membership.

In fact distinct sites follow from the approximation promise at tau<=1/4. If i and k shared a site, exact cross-logical commutation would give ||[A_(i,X),A_(k,X)]|| and ||[A_(i,Z),A_(k,X)]|| <=4tau. For unit Bloch axes x,z orthogonal and v arbitrary, |x cross v|^2+|z cross v|^2>=1; Pauli commutator norms are twice these lengths. Therefore 8tau^2>=1, contradicting tau<=1/4.

## 3. Fine ordinary data and a valid martingale bound

After any correct coarse history, use the SAME actual product preparations and product-Pauli readouts as in the exact source. The realized per-logical matrix is

    F_(i,t)=6 s_i b_(pi(i)) e_(a_(pi(i))) e_(j_i)^T,

where j_i is freshly uniform in {X,Z}; its conditional expectation has columns m_(i,X,t),0,m_(i,Z,t). Every other current sign, axis and outcome is averaged in this conditional expectation. Its range and second moment are unchanged:

    ||F_(i,t)||F=6,
    N_i=Mhat_i-(1/N1)sum_t E[F_(i,t)|past],
    E||N_i||F^2<=36/N1.

Every nonzero scalar coordinate is in [-6,6], so the conditional Hoeffding/mgf argument gives

    P(|(N_i)_(a,j)|>=x)<=2 exp(-N1 x^2/72).

Consequently, for any rational zeta>0, a sufficient fixed bank is

    L1=ceil log2(24q/beta),
    N1=ceil(512 L1/(kappa^2 zeta^2)),

which yields simultaneously ||N_i||F<=kappa zeta except probability beta/2. Indeed a union bound over 6q entries at x=kappa zeta/sqrt(6) is at most 12q exp(-N1 kappa^2 zeta^2/432)<=beta/2.

## 4. Normalize columns before conventional proper Procrustes

Let mbar_j be a true averaged column, mhat_j=mbar_j+N_j the actual empirical column. Define uhat_j=mhat_j/|mhat_j| if nonzero, with any fixed unit-vector fallback if zero. The elementary normalization bound, including that zero fallback, is

    |uhat_j-mbar_j/|mbar_j|| <= 2|N_j|/|mbar_j|
                             <=2|N_j|/(kappa c).

If mhat=0, |N|=|mbar| and the right side is 2, so the same inequality remains valid. Combining with (A),

    |uhat_j-a_j| <= tau+2|N_j|/(kappa c).              (C)

No unknown lambda must be estimated separately. This is conventional column normalization plus proper orthogonal Procrustes; it avoids an artificial tau/kappa bias amplification. This note does not claim that every raw weighted Procrustes analysis must incur that penalty.

For finite arithmetic, each empirical entry is an integer multiple of 6/N1. Thus a nonzero column has norm>=6/N1 and norm<=6. Fix rational eta>0. Bisection of its rational squared norm produces a rational upper r>=|mhat| with r-|mhat|<=6eta/N1 using O(log(N1/eta)) steps and polynomial input/output bit length. The rational column mtilde=mhat/r has norm<=1 and |mtilde-uhat|<=eta. Exact-zero columns get the fixed unit fallback. Every possible record is covered by a fixed finite cap.

Let Mtilde have the two resulting columns and zero Y column; let R be the true proper on-site rotation and D0=diag(1,0,1). Then

    ||Mtilde-R D0||F <= sqrt(2)tau
                      +2||N_i||F/(kappa c)+sqrt(2)eta. (D)

Fit a proper Rhat with objective gap delta in max_SO(3)<R,Mtilde>, using the exact rational quaternion/Jacobi construction in the exact source. The matrices Mtilde are rational and ||Mtilde||F<=sqrt(2) on EVERY record, so the previous finite spectral scaling is more than sufficient. Proper feasibility is exact, including degenerate records. The two-axis curvature proof at margin 1 gives

    ell_i:=||Rhat_i-R_i||F^2/8
      <=2||Mtilde_i-R_i D0||F^2+delta
      <=2(sqrt(2)tau+2 zeta/c+sqrt(2)eta)^2+delta       (E)

on the simultaneous fine event. Stacking before squaring gives the more informative aggregate version

    sum_i ell_i <=2(sqrt(2q)tau
                 +2 sqrt(sum_i||N_i||F^2)/(kappa c)
                 +sqrt(2q)eta)^2+q delta.

Thus with zeta,eta proportional to sqrt(epsilon/q) and delta proportional to epsilon/q, the same conventional physical controls give an acquisition orientation bound O(q tau^2+epsilon) at N1=O(q log(q/beta)/(kappa^2 epsilon)). The kappa denominator belongs to statistical estimation, not to the deterministic approximation floor. Future-memory extraction still requires the parent's separate full-reference physical proof.

## Resource and comparator scope

No calibration quantum receiver is added: each actual call still uses ordinary logical product states and one physical product-Pauli readout. All candidates share that one output record. Classical normalization adds only bounded rational arithmetic on six empirical entries per logical. Fine control remains q one-qubit inverse rotations plus paid routing/compilation. The appropriate conventional baseline has the SAME unknown matching, known physical register, ordinary probes, memory privacy, supplied uniform margin and approximate-on-site promise, and performs maximum-score localization plus normalized proper Procrustes. There is no algorithmic advantage over that baseline.

## 5. Sharper direct two-column least-squares calculation

The parent proposed a sharper bound than (E), which checks independently. Because every proper R has ||R D0||F^2=2, the objective-gap condition is exactly

    ||Rhat D0-Mtilde||F^2 <= ||R D0-Mtilde||F^2+2delta.

With E=||Mtilde-R D0||F, triangle inequality gives

    d_pair:=||(Rhat-R)D0||F <=2E+sqrt(2delta).

The quaternion two-axis relation implies ||Rhat-R||F^2<=2d_pair^2, so sqrt(ell_i)<=d_pair/2. This does not use an eigengap or a hidden good-fit branch. Stacking over all logicals gives

    (1/2)sqrt(sum_i d_pair_i^2)
      <=sqrt(2q)tau +2 sqrt(sum_i||N_i||F^2)/(kappa c)
         +sqrt(2q)eta+sqrt(q delta/2).

For the parent's stated choices

    N1=ceil(65536 q L1/(kappa^2 epsilon)),
    eta=delta=epsilon/(128q),

all ||N_i||F^2<=kappa^2 epsilon/(128q) except probability beta/2: the scalar exponent is at least (65536/55296)L1=(32/27)L1. Since c>=31/32 and epsilon<=1, the statistical, normalization and fit contributions are at most

    [1/(4sqrt(2)c)+sqrt(2)/128+1/16]sqrt(epsilon)
      <=0.256028 sqrt(epsilon) < sqrt(epsilon)/3.

If the parent's separate physical full-reference argument contributes an additional sqrt(q/2)tau in root loss, then the resulting root bound is 3sqrt(q/2)tau+sqrt(epsilon)/3. Squaring via (a+b)^2<=2a^2+2b^2 and adding beta<=epsilon/8 plus nu_cal+nu_svc<=epsilon/4 gives

    actual excess <=9q tau^2+(43/72)epsilon
                  <=9q tau^2+epsilon.

This last sentence checks the scalar composition constants only; its physical premise is deliberately not assumed proved by this acquisition note.

## Independent deterministic evidence

`approximate_onsite_acquisition_independent_check_20261028.py` and its JSON output exercise actual finite-dimensional Pauli/gauge maps with q=1,2 and n=2,3, fixed weak cross-coupling unitaries, noncommuting positive gauge blocks, changing conditional-gauge fixtures, and identity-dominant Pauli maps. A depolarizing mixture spans supplied margins from approximately 9e-5 to 0.95 without changing normalized bias. The script verifies the pointwise and averaged cone/leakage bounds, direct proper-fit geometry, exact rational normalization brackets and the announced constants. It explicitly enumerates 3,600 ordinary preparation/measurement Born events and verifies the fine-feedback identity. These are mathematical fixtures, not sampled acquisition or hardware evidence; numerical checks complement rather than replace the proofs above.
