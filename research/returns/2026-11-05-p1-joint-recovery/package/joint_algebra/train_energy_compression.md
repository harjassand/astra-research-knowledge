# Uniform finite-angle compression from the XXX boundary train identity

5 November 2026. This is a complete causal positive-instrument construction with an explicit error, coherent-memory, and processing bill. It is derived from the ordered integrable monodromy, without an inference from its ordinary eigenvalues. It gives an arbitrarily accurate compression family in an explicit joint regime. Its retained-memory rate tends to one as accuracy increases; it does not solve the optimal joint endpoint.

The train/boundary relation is standard rational-XXX/Yang–Baxter machinery; its proof is reproduced below to fix the normalizations and chronological orientation. The rational R-matrix and braiding framework are reviewed, for example, in Claeys, Herzog-Arbeitman, and Lamacraft, *Correlations and commuting transfer matrices in integrable unitary circuits*, SciPost Physics 12, 007 (2022), Sections 2.1–2.2, https://arxiv.org/html/2106.00640v3 . No novelty claim is made for that algebraic machinery. The source-specific deduction here is the positive spectral instrument together with its physical recovery, rank, and resource guarantees.

The two rank guarantees below are complementary. The elementary binary version has numerical constants and no external density-of-states input. A compact-window version uses a proved product-state Berry–Esseen theorem and saves order log n qubits per n-carrier block.

## 1. Notation and the exact boundary identity

Take n>=2 consecutive physical output carriers. Write

    c=cos(theta), s=sin(theta), r=1-s^4,
    U_j=c I+i s P_(S,j), U=U_n ... U_1,
    H_n=sum_(j=1)^(n-1) P_(j,j+1).

The source is only a mathematical leg in these identities; the receiver measures H_n on the emitted carriers alone. All Hilbert–Schmidt norms in this note use normalized trace, including the source when it is present.

The exact identity is

    [H_n,U]=s^2 (U P_(S,1)-P_(S,n) U).                 (1)

It holds for every n and every physical angle. Consequently

    ||[H_n,U]||_op <= 2 s^2,
    ||[H_n,U]||_(2,tau)^2 = (3/2) s^4  (n>=2).        (2)

### Proof by the rational train relation

Put L_j(u)=u I+i P_(S,j), u=cot(theta), and M=L_n...L_1. The permutation relations give

    [P_(j,j+1),L_(j+1)L_j]=P_(S,j)-P_(S,j+1)
                         =-i(L_j-L_(j+1)).

After multiplication by the surrounding L factors and summation over j, every interior missing-factor product cancels:

    [H_n,M]=-i(L_(n-1)...L_1-L_n...L_2).

Use L_j^(-1)=(u I-iP_(S,j))/(u^2+1) on the two boundary products, then normalize the monodromy. This gives (1). For (2), the two SWAPs have squared norm one and

    tau(P_(S,1) U^dagger P_(S,n) U)=1/4.

Indeed U_1 commutes with P_(S,1), U_n commutes with P_(S,n), and the remaining collisions touch neither endpoint carrier. Tracing the first endpoint SWAP supplies I_S/2. Thus the two boundary terms have overlap 1/4, independently of angle and block length.

## 2. Exact physical loss functional and its charge value

Let W_a=U(sigma_a^S tensor I)U^dagger, and let a completely refined positive instrument on the block have effects A_x>=0 with sum_x A_x^2=I. Isometrically encode the support of each A_x and retain x as a classical record. The balanced retained-norm map is the Lüders map

    Lambda(X)=sum_x A_x X A_x.

Its total source-granted loss for the logical Pauli triple is exactly

    d = 1-b-h
      = (1/6) sum_(a,x) ||[I_S tensor A_x,W_a]||_2^2.   (3)

Here b is the source-identity acquisition and h is the remaining source-traceless squared norm. The reference at tracial logical input is exactly tracial source times the instrument's block reference state; this is the balanced physical loss, including every outcome, rather than a selected branch.

For any Hermitian bath operator A, define

    D_U(A)=(1/6)sum_a ||[I tensor A,W_a]||_2^2.

Pauli completeness gives the useful exact alternative

    D_U(A)=(4/3)||Q_S[U^dagger(I tensor A)U]||_2^2,     (4)

where Q_S removes the source-identity part. In particular,

    D_U(H_n)=s^4(1+r^(n-1)).                           (5)

To prove (5), conjugate (1):

    U^dagger H_n U-H_n=s^2(P_(S,1)-U^dagger P_(S,n)U).

The first source-traceless SWAP part has squared norm 3/4. The second has squared norm (3/4)r^(n-1), since backwards propagation of each source Pauli through n-1 fresh tracial carriers retains precisely r^(n-1) of its source-traceless norm. The cross inner product vanishes: its full overlap is 1/4 as above, equal to the overlap of the source-identity parts. Equation (4) now gives (5).

## 3. A finite smooth spectral instrument

Let F(E)=(f_x(E)) be a real nonnegative vector with ||F(E)||=1 and Euclidean Lipschitz constant L_F. Set A_x=f_x(H_n). These are positive complete effects, so the resulting instrument is CPTP without postselection.

In an eigenbasis of H_n, for every matrix W,

    sum_x ||[f_x(H_n),W]||_2^2
      <= L_F^2 ||[H_n,W]||_2^2.                        (6)

This is the scalar inequality ||F(E)-F(E')||^2<=L_F^2(E-E')^2 applied to each matrix element. It is a Hilbert–Schmidt statement; no operator-Lipschitz theorem is assumed. Combining (3), (5), and (6) gives the all-angle bound

    0<=d<=delta:=min{1,L_F^2 s^4(1+r^(n-1))}.           (7)

### Compact overlapping windows

For any w>0, use the functions

    f_l(E)=cos(pi(E-lw)/(2w)) for |E-lw|<=w,
           0 otherwise.

Between two consecutive grid points exactly two functions are nonzero, and their squares sum to one. Only finitely many windows meet the spectrum. Each effect is supported on an energy interval of width 2w, and

    L_F=pi/(2w),
    delta_grid=min{1, pi^2 s^4(1+r^(n-1))/(4w^2)}
              <=min{1,pi^2 s^4/(2w^2)}.                (8)

The number of nonzero outcomes is at most ceil(2(n-1)/w)+3. Coherence between different eigenvectors in the same support is retained, including complex multiplicity and chirality coherence. No fine spin-path or energy-eigenvector measurement is made.

## 4. Uniform support-rank bounds

### 4.1 Compact-window rank from a primary theorem

For tracial input, H_n has mean (n-1)/2 and variance

    sigma_n^2=3(n-1)/4.

Theorem 1 in Cramer, Brandao, Guta, Alhambra, and Scandi, *A Berry–Esseen Bound for Quantum Lattice Systems*, arXiv:2605.03829v1, Section III, proves Kolmogorov error at most K/sqrt(n) for a product state and a bounded finite-range Hamiltonian with variance bounded below by a constant times n. Here each local term has norm one, the range is one, and sigma_n^2>=3n/8 for n>=2, so K is independent of n and theta. Thus every interval of length 2w contains at most the fraction

    rho_(n,w)=min{1,4w/sqrt(6pi(n-1))+2K/sqrt(n)}        (9)

of all eigenvectors, counting degeneracies. Each effect therefore has rank at most floor(2^n rho_(n,w)). This invokes the theorem, not an assumed Gaussian density. The source's product-state result has no polylogarithmic loss. It states K as an O(1) constant; this note does not substitute an unproved numerical value for K.

Primary source: https://arxiv.org/html/2605.03829v1 ; https://arxiv.org/pdf/2605.03829 . Theorem 1 and its variance hypothesis were checked directly.

For fixed w>0 this gives, once n is sufficiently large,

    log_2(max_x rank A_x)
      <= n-(1/2)log_2 n+log_2(w+1)+O(1).               (10)

An exact finite implementation may compute its actual support ranks directly from H_n; the elementary alternative below avoids the unspecified Berry–Esseen constant entirely.

### 4.2 Elementary two-outcome cut with numerical constants

Put ell=n-1 and Z=2H_n-ell I=sum_j sigma_j dot sigma_(j+1). Exact tracial moments are

    tau Z=0,  tau Z^2=3ell,
    tau Z^4=27ell^2-30ell+24 <=27ell^2.                 (11)

For the fourth moment, one bond contributes 21; an unordered disjoint bond pair contributes 54 after summing its six orderings; an adjacent pair contributes 30. Every term involving three or four distinct bonds has a singly occurring extreme bond and zero trace. There are ell-1 adjacent pairs, giving (11).

Write sigma=sqrt(3ell). Holder interpolation gives E|Z|>=sigma/sqrt(3), and mean zero gives E Z_+=E Z_->=sigma/(2sqrt(3)). For w_Z=sigma/(4sqrt(3))=sqrt(ell)/4, Cauchy–Schwarz gives

    E Z_+ <= w_Z+sigma sqrt(Pr{Z>=w_Z}),

and similarly for -Z. Therefore

    Pr{Z>=sqrt(ell)/4}>=1/48,
    Pr{Z<=-sqrt(ell)/4}>=1/48.                          (12)

Define a(E)=0 below -w_Z, a(E)=pi(E+w_Z)/(4w_Z) between -w_Z and w_Z, and a(E)=pi/2 above w_Z. Use

    A_-=cos(a(Z)), A_+=sin(a(Z)).

Both effects have rank at most

    R_n=floor((47/48)2^n),                              (13)

their squares sum to I, and their vector Lipschitz constant with respect to Z is pi/sqrt(ell). Since Z=2H_n-ell I, (5)-(7) give

    delta_bin=min{1,4pi^2 s^4(1+r^(n-1))/(n-1)}
             <=min{1,8pi^2 s^4/(n-1)}.                 (14)

This is an explicit positive rank-reducing operation for every n>=2 and every physical angle. Neither a thermodynamic limit nor a large-n spectral approximation is used.

## 5. Exact block recurrence and terminal physical recovery

Apply the chosen n-carrier instrument independently to successive blocks. Let b,h be its actual balanced source-identity and source-traceless coefficients, as in (3). Because each effect commutes with collective rotations, the three Pauli Gram matrices are scalar. Old source-identity information passes unchanged; its overlap with newly acquired information vanishes by the new block's zero logical trace. These facts hold for arbitrary old source/memory correlations, so

    a_(j+1)=a_j+b q_j,  q_(j+1)=h q_j,
    a_0=0, q_0=1.

Thus, for K blocks and N=nK,

    a_K=b(1-h^K)/(1-h),  q_K=h^K,
    d=1-b-h,  0<=h<=r^n,  0<=b<=1-r^n.                (15)

The upper bounds follow from contraction of the balanced processing map on the two orthogonal source sectors. In particular, with B_n=1-r^n,

    d/(1-h)<=min{1,delta/B_n}=:f_bar.                  (16)

### Actual readout, including the unsharp effects

Let V_x encode range(A_x) isometrically and use Kraus map K_x=V_x A_x. At tracial block input, the unnormalized output reference in branch x is V_x A_x^2 V_x^dagger/2^n. Its Petz map is exactly

    R_x(Y)=V_x^dagger Y V_x.                            (17)

The A_x factors cancel the inverse square roots of A_x^2 on its support. There is no inverse filter with a small success probability or a large condition number.

At the end, unpack the last compressed block, embed it by (17), apply the original inverse partial-SWAPs to a dummy qubit initialized at I/2 in reverse chronological order, discard that block, and continue backwards. Petz maps compose with the consistent reference states here. This is the Petz map of the actual compressed output channel. The recovered qubit channel is depolarizing with visibility a_K. Therefore its exact half-diamond error is (3/4)(1-a_K), and

    epsilon_Petz <= (3/4)[r^N+(1-r^N)f_bar],
    f_bar=min{1,delta/(1-r^n)}.                         (18)

All quantities are finite-angle expressions. If N=nK+t with 0<=t<n, keep the last t carriers raw. Then q=h^K r^t and a=b(1-h^K)/(1-h)+h^K(1-r^t). Bound (18) still holds: each processed block obeys b>=(1-f_bar)(1-h), and a raw tail obeys it with zero loss. This proves a>=(1-f_bar)(1-q) by induction, while q<=r^N.

## 6. Coherent memory, integer packing, and paid processing

For a chosen instrument, let R=max_x rank A_x and q=ceil(log_2 R). Without packing across blocks, K full blocks need Kq retained qubits. Collection or decompression of the final block gives the core peak

    M_core <= (K-1)q+n+a_enc                            (19)

for K>=1 and N=nK. Here a_enc includes the outcome flag and encoder workspace; the explicit finite-dimensional implementation below permits a_enc=O(log(number of outcomes)+1), including the final dummy. A raw tail or an incomplete packed group costs at most its raw carrier count.

For B blocks packed together, every classical label pattern has conditional dimension at most R^B. A fixed conditional unitary embeds this into

    q_B=ceil(B log_2 R)

qubits. If N=BnG, the corresponding core peak is

    M_core <= (G-1)q_B+Bn+a_enc.                        (20)

For arbitrary N, keep the final incomplete group separately, at an additional O(Bn) cost. No fractional qubit is credited as a complete memory cell.

For the elementary instrument,

    (47/48)^33=0.49919299048... <1/2.

Thus B=33 gives q_33<=33n-1. For N divisible by 33n,

    M_ret <= N-N/(33n),
    M_core <= N-N/(33n)+O(n).                          (21)

For compact windows, sufficiently large n at fixed w permits q<=n-(1/2)log_2 n+O(log(w+1)+1) without grouping. Its saving is O(log n) per block and hence O(N log n/n) over the whole stream. This is an extensive saving in N for fixed block parameters, while its fractional size vanishes when n grows.

### Encoder and decoder are finite operations, with their cost counted

Diagonalize the known finite matrix H_n. In that basis, coherently attach a flag with amplitudes f_x(E), measure only the flag, and conditionally relabel the support basis into the retained register. This retains arbitrary superpositions within each support. Decompression reverses the support relabeling and energy-basis change. Group packing is another known conditional subspace embedding. These are deterministic channels; no outcome is rejected.

A generic finite-dimensional synthesis supplies a conservative addressed-gate bound

    G_(n,w,B)=2^O(B(n+log(number of outcomes)))

per packed encoder/decoder. One may use a full unitary extension on Bn plus the flag qubits; no efficient Bethe-basis transform is asserted. The known matrices can be compiled offline, but their physical gates are still paid. The complete reader uses O((N/(Bn)+1)G_(n,w,B)) encoder/decoder gates plus exactly N inverse collision gates. A discrete universal gate set adds a polylogarithmic factor in N G_(n,w,B)/nu for total channel-approximation budget nu. The final half-diamond error is at most the right-hand side of (18) plus nu.

This processing cost is exponential in the chosen block size under the present guarantee. It must not be described as near-linear processing uniformly in accuracy.

If carriers arrive at fixed spacing Delta and one packed encoder takes service time tau_enc, provision

    P=max{1,ceil(tau_enc/(Bn Delta))}

independent processors or the corresponding coherent queue. This adds O(P(Bn+a_enc)) coherent cells, together with paid routing. Equations (19)-(21) are core storage bounds; the total physical peak includes that service provision. The final inverse-dummy pass also has a sequential dependency and its time is paid. No change of the specified source clock is assumed.

## 7. Explicit angle–accuracy choices and their limit

For any n,w,theta,N, equations (8), (9), (18), and (19)-(20) are a complete parameterized law for the compact-window construction. Equations (13), (14), (18), and (20)-(21) give a numerical-constant alternative.

In the useful joint regime n s^4<=1,

    1-r^n >= n s^4/(1+n s^4) >= n s^4/2.

Consequently

    f_bar_grid <= min{1,pi^2/(n w^2)},
    f_bar_bin <= min{1,16pi^2/[n(n-1)]}.                (22)

For a desired ideal error 0<eta<3/4, choose an integer n>=2 satisfying

    n(n-1)>=24pi^2/eta,  n sin(theta)^4<=1,

and choose N, rounded up to a multiple of 33n, satisfying

    r^N<=2eta/3.

Then the elementary physical reader has half-diamond error at most eta, with the memory and gate counts above. Finite control of total error nu gives total error at most eta+nu. Here n=O(eta^(-1/2)); the angle condition is roughly eta at least a constant times theta^8, with the displayed integer condition being the precise statement. The collection horizon remains O(sin(theta)^(-4)(log(1/eta)+1)).

At that choice the core retained-memory saving is Omega(N sqrt(eta)), and the retained fraction is 1-O(sqrt(eta)). The compact-window version instead permits logarithmic saving per block; for fixed w its small-loss requirement is n=O(1/eta), with the stated rank constant threshold.

There is also a conservative arbitrary-angle choice with no joint-regime restriction. Since B_n>=s^4, (14) implies f_bar_bin<=min{1,8pi^2/(n-1)}. Choosing n-1>=12pi^2/eta and the same r^N bound, with N rounded to a multiple of 33n, attains error eta for every 0<theta<pi/2. Its horizon is O(sin(theta)^(-4)log(1/eta)+eta^(-1)); the extra eta^(-1) term can make it much less economical than raw output storage at fixed angle. It is included to make the operation's angle and accuracy quantifiers complete, not as an optimized endpoint claim.

These are parameterized upper bounds at their chosen collection horizon. A comparison with the simple all-output reader at exactly the same target error must include the extra acquisition budget used for compression loss, the rounding, and the service resources. A saving at fixed N does not alone prove an improved optimized total-space bound. The following fixed-error comparison does include those costs at leading order.

### A strict fixed-error weak-angle improvement over raw output storage

Fix 0<epsilon<3/4, set e=4epsilon/3 and L=log(1/e), and choose a fixed integer n>=2 such that

    p_n=16pi^2/[n(n-1)]<=e/2,
    n>=4224pi^2/(e L).                                  (23)

This n depends on epsilon and is fixed before theta tends to zero. For all sufficiently small theta, n s^4<=1. Choose the used-carrier count, rounded upward to a multiple of 33n, so that

    r^N <= (e-p_n)/(1-p_n).                             (24)

Equations (18) and (22) give ideal half-diamond error at most epsilon, while the elementary packed core retains at most (1-1/(33n))N qubits. Rounding adds at most 33n carriers, fixed in this limit. Since -log r~s^4,

    limsup_(theta->0) s^4 M_core
      <= (1-1/(33n)) log((1-p_n)/(e-p_n))
      <= L-L/(66n) < L.                                (25)

The simple all-output inverse-dummy reader at the same target has leading coefficient L. To verify the second inequality, p_n<=e/2 gives

    log((1-p_n)/(e-p_n))
       <=L+2p_n/e <=L+64pi^2/(e n^2).

Condition (23) makes the last extra term at most L/(66n), while packing subtracts L/(33n). This is a strict, potentially extremely small, leading-coefficient improvement over that particular full-storage benchmark. It pays the extra acquisition needed to offset the compression loss. It leaves the theta^(-4) order unchanged and is not an optimality statement.

For finite controls, choose a total synthesis error nu(theta)->0 and apply (24) with epsilon replaced by epsilon-nu(theta). For example, polynomially small nu in s makes precision overhead polylogarithmic in N. At fixed n, the generic block circuit has a fixed, potentially enormous, gate count before precision overhead. With fixed primitive gate times and fixed arrival spacing, Section 6's service provision then adds O(polylog N)=o(N) coherent cells. Thus (25) also holds after adding that circuit-service overhead. Addressed processing still includes its exponential-in-n prefactor, the final sequential inverse sweep, and routing. Required gate and idle-memory protection must attain the stated total error budget; their time, work, and any additional coherent cells remain part of the implementation cost. A hardware model requiring further protection cells needs those added to the core/service counts before making a physical-cell comparison. No faster arrival clock or free quantum queue is assumed.

## 8. What this construction does and does not close

The operation provides uniform positive low-loss effects, actual rank reduction, causal storage, and terminal recovery. Its loss control uses an exact ordered boundary identity, so there is no fixed-n Taylor extrapolation and no ordinary-eigenvalue-to-singular-value inference. Its coarse energy supports preserve the complex multiplicity coherence excluded by the real multiplicity-rank-one obstruction.

It does not make the compressed register into fresh homogeneous sites. Multiple commuting charges would require a joint rank estimate and a simultaneous commutator budget; iterative compression would require control of the changed physical interface. Neither follows from (1). The passive matched-cascade semigroup's asymptotic extraction as its width grows also remains unproved. The unrestricted optimal joint memory/processing endpoint remains open here.

## Reproduction

train_energy_compressor.py and train_energy_checks.jsonl contain 58 checks: the exact moment formulas, the train relation at finite angles, the exact charge-loss value, complete finite spectral instruments, and direct two-block physical contractions versus recurrence (15). Maximum train residual was 2.284e-15, maximum charge-loss residual 2.221e-16, minimum instrument bound slack 2.941e-5, and maximum two-block recurrence residual 3.054e-16. These checks validate the proved algebra and physical bridge; they are not searches for optimal projectors.
