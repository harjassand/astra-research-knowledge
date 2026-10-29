# Finite coherence-only acquisition of a nonunitary recovery

2026-10-28. Author construction, pending independent review. This supersedes the open concentration/perturbation obligations in `flagged_loss_coherence_sufficient_statistic_20261028.md` only as explicitly proved below; that working note is retained. The received general-extremal-face theorem is unchanged.

## 1. Physical promise and what is identified

Logical input is a qubit, receiver dimension d>=3. A fixed unknown isometry V=[u_0,u_1] has orthonormal columns; F=I−VV†. At every calibration history h before the current private input choice, the conditional native map has the form

    N_h(rho)=V diag(1,s_h) rho diag(1,s_h) V†
              +(1−s_h²) rho_11 tau_h,                (1)

where 0<=s_h<=1 and tau_h is any density operator supported on F. No rank, eigenvalue floor, fixed flag state, memory reset or known s_h is required. Retained quantum memory may generate arbitrary conditional changes satisfying (1). Fresh logical probes must initially be uncorrelated with that memory, and their current private settings must have no input side channel. The conditional-channel promise is assumed, not verified from finite training data.

The target receiver is the specified family rule

    D_V(X)=V† X V + Tr(FX)|1><1|.                    (2)

It preserves coherent code-subspace information and resets every complement direction to logical |1>. This is a CPTP nonunitary receiver with Kraus V† and |1><f_a|. The target remains defined when tau_h is rank-deficient; unseen complement directions are assigned by (2), not claimed to be statistically identified as an unrestricted oracle. Native entanglement fidelity after this receiver is (1+s_h)/2, not generically near one.

Its sufficient statistic is

    C_h=N_h(|0><1|)=s_h |u_0><u_1|.                 (3)

For T uses the predictable average is C_bar=s_bar |u_0><u_1|, s_bar=T^(-1)sum_h s_h. The rank-one vectors are independent of every tau_h, even when the generic strict-dual-gap certificate would vanish. If s_bar is zero or too small, the finite mechanism abstains. Persistent finite completion requires a positive lower bound on the bank-average coherence eventually; none is silently supplied.

## 2. Finite output measurement, not Haar access

Fix a known, calibrated complete set of d+1 mutually unbiased orthonormal bases B_b={psi_bj}. These are available in prime-power dimension. Their finite algebraic tables may be constructed and checked once: each basis is orthonormal and cross-basis squared overlaps equal 1/d. No assertion of complete MUB existence is made for arbitrary d. A supplied weighted projective 2-design with accounted measurement realization could replace this interface, but is not assumed free.

Two concrete instances:

- Odd prime d: computational basis plus columns d^(-1/2) exp(2 pi i (a x²+jx)/d), for a,j,x in Z_d. These are finite Fourier/chirp bases.
- d=4: joint eigenbases of the two-generator Pauli classes (ZI,IZ), (XI,IX), (YI,IY), (XZ,ZY), (XY,YZ). Their generated nonidentity commuting classes partition the fifteen nonidentity two-qubit Paulis. The exact fixture below checks their MUB and moment identities.

The finite complete-MUB 2-design property is established in Klappenecker and Rötteler, Theorem 3; its prime-power constructions are in the same source. At each use choose basis b uniformly and privately, apply its calibrated inverse basis transform, and measure the computational outcome j. This realizes POVM effects |psi_bj><psi_bj|/(d+1). The design is finite: d+1 settings, d outcomes each, not a Haar oracle.

Input setting q is uniform on +x,−x,+y,−y, requiring two unbiased random bits. Basis choice uses m=ceil(log2(d+1)) fresh bits with rejection of labels >=d+1. Reject-and-redraw L times then abort the bank if none accepted: failure probability <=2^(-L) per use; choose L>=ceil(log2(T/delta_rng)). Aborting does not assert an incorrect certificate, and a union bound pays its probability in any success/completion claim. Accepted labels are exactly uniform; no hidden bias remains. Independent ideal coins and their physical realization are control assumptions.

Generic dense measurement-basis compilation costs O(d²) two-level rotations per basis, not O(poly(log d)) for free. Each rotation must be realized in the selected hardware gate set/connectivity and synthesized to its allocated tolerance. For d=2^n a stabilizer MUB implementation can improve that interface if an actual compiler is supplied; this theorem does not claim that implementation merely from the design property. Classical storage of explicit basis tables is O(d³) complex entries, reducible with the finite constructive representations above. These costs can dominate the resources even though the estimator does not reconstruct the flag environment; no quantified comparative advantage is established.

## 3. Actual estimator and conditional moments

For the observed basis vector psi define Y=(d+1)|psi><psi|−I. The 2-design identity gives, for every receiver density rho,

    E[Y|rho]=rho,
    E[Y²|rho]=(d−1)rho+dI,
    ||Y||op=d.                                    (4)

Let w_q be 1,−1,i,−i for q=+x,−x,+y,−y and record Z=2w_q Y. For logical Pauli eigenstate output densities rho_q,

    E[Z|history]=(rho_+x−rho_−x+i rho_+y−i rho_−y)/2=C_h.

The factor and sign include the logical relative phase. Furthermore

    E[ZZ†|history]=E[Z†Z|history]
      =4[(d−1) rho_avg+dI] <=4(2d−1)I,             (5)

where rho_avg=(sum_q rho_q)/4. Thus this is an acquired rank-one contrast, not a supplied cross-channel matrix or error syndrome.

For X_h=Z_h−C_h, conditional means vanish. We have ||X_h||op<=R=2d+1, and both conditional second moments are <=vI, v=4(2d−1), because subtracting the mean removes respectively C_h C_h† and C_h† C_h. Apply rectangular matrix Freedman (Tropp 2011, Corollary 1.3) to the d by d martingale sum, with variance bound Tv and dimension factor 2d. With ell=log(2d/delta), define

    eta_stat = [sqrt(2Tv ell)+(2R ell)/3]/T.        (6)

Then with probability >=1−delta,

    ||C_hat−C_bar||op <= eta_stat,
    C_hat=T^(-1) sum_h Z_h.                       (7)

Indeed the cited inequality is 2d exp[−a²/(2(Tv+Ra/3))]; the numerator in (6) is a conservative root. This fixed-bank consequence remains valid under the conditional drift/memory promise, not just IID data. Repeated banks use summable delta_b (e.g. delta_total*6/(pi² b²)) and their own finite caps; a selected acceptance bank is then covered simultaneously. Do not reuse a single fixed-bank delta after optional stopping.

Preparation/readout bias and matrix representation error add to eta_stat. One explicit conservative hardware interface: if the actual conditional joint distribution of q,b,j differs in total variation by <=beta from its ideal counterpart for every history, the mean estimator changes by at most 4d beta since ||Z||<=2d. The centered actual estimator has variance at most 4(2d−1)I+8d² beta I by a bounded-function TV comparison, and increment bound <=4d (rather than R) without further assumptions. Thus a robust version of (6) uses v_beta=4(2d−1)+8d² beta, R_beta=4d, then adds 4d beta to eta. A known matrix arithmetic bound eta_num is added too. These are conservative calibration requirements, not an unmeasured environment assumption. In particular constant uncontrolled beta does not vanish with more samples.

## 4. Observed singular-gap guard and physical isometry

Use an exact algebraic representation of C_hat, or a nearby algebraic matrix C_tilde with certified operator error eta_num already included in eta. Let its largest singular value be a and choose a coupled unit singular pair l,r satisfying C_tilde r=a l and C_tilde† l=a r. Use an exact/certified algebraic SVD; a raw floating residual is not treated as exact. Accept only if

    a > 4 eta.                                   (8)

One may also reject when the second singular value exceeds eta, a necessary promise-consistency check; passing this is not a general validation of (1). Form W=[l,r], certify W†W>0 and set

    V_hat=W(W†W)^(-1/2).                          (9)

This is a physical isometry. l and r may only receive a common phase: independent phase conventions would alter the encoded logical phase.

**Perturbation proof with observed denominator.** Write C_bar=s_bar u_0 u_1†. Under (8) the good event implies s_bar>0. Hermitian dilation A=[[0,C_bar],[C_bar†,0]] has unique positive eigenvector z=(u_0,u_1)/sqrt(2), eigenvalue s_bar, with its remaining eigenvalues <=0. The acquired pair gives z_hat=(l,r)/sqrt(2), positive eigenvalue a for its dilation. Projection onto z-perp gives

    ||P_zperp z_hat|| <= eta/a,

because (aI−A) restricted to z-perp has inverse norm at most 1/a. Align their common phase. For unit vectors the Euclidean distance is <=sqrt(2) times this sine, so

    ||W−V e^{i theta}||F <=2eta/a <1/2.

Consequently W has full column rank. Its polar factor minimizes Frobenius distance to an isometry, so triangle inequality gives

    ||V_hat−V e^{i theta}||op <=4eta/a.            (10)

No flag eigenvalue or unrestricted-channel oracle enters. Guarded algebraic matrix functions are finite; numerical implementations must certify their residuals or absorb a separate resulting isometry error.

## 5. Complete receiver and operation guarantee

Execute (2) with V_hat. For isometries V,W with phase-aligned operator distance epsilon, the compressed maps X->V†XV and X->W†XW differ in diamond norm by <=2epsilon. This follows by expanding the difference into two left/right multiplication terms, equally valid with an arbitrary reference. Their complement projectors differ in operator norm by <=2epsilon. The remaining reset-map difference is a Hermitian linear functional followed by a fixed state; its diamond norm equals the coefficient's operator norm. Therefore

    (1/2)||D_V−D_Vhat||diamond <=2epsilon
                                <=8eta/a.         (11)

Clip at 1. A separately certified implementation half-diamond error eps_exec adds. Good-event failure delta contributes separately to an unconditional trace-distance substitution guarantee; actual calibration randomness/source records are coupled, not replaced by a stationary fictitious channel. Future arbitrary states jointly correlated with memory are allowed for comparison to the same fixed receiver D_V. Future optimality or fidelity needs a separately maintained physical family promise; operation closeness does not establish capacity or high fidelity.

**Finite execution.** A two-column QR elimination constructs a unitary U sending the columns of V_hat to computational vectors 0 and 1. At most (d−1)+(d−2) two-level rotations plus two column phases suffice; no full environment fit or arbitrary dense d-column decomposition is needed. Execute U, coherently retain the span{0,1} as the output logical qubit, and measure only whether its complement was entered; on the complement prepare |1>. For d=2^n with code labels differing in the least significant bit, measuring the other n−1 bits implements that flag and preserves code coherence. Other dimensions require a specified qudit code/complement measurement. Each synthesized rotation, coarse measurement and reset has its own control tolerance; telescoping adds their channel errors. Two-level rotation count is not a hardware-native gate count: compilation to finite gates, precision, connectivity and ancilla costs remain implementation inputs and may scale with d.

For target operation error xi, the sufficient statistical condition is eta/a<=xi/8, not merely the rank guard. With fixed s_bar>=s_min>0, ideal controls give sample scaling O(d log(d/delta)/(s_min² xi²)+d log(d/delta)/(s_min xi)), with explicit constants supplied by (6) and the observed guard. Fixed calibration bias creates an irreducible floor. Classical formation of a dense C_hat costs O(Td²), storage O(d²), and dense SVD O(d³); structured updates or iterative solvers may improve those but are not claimed here. This is not an efficient-in-qubit-number general-noise construction.

## 6. Equally informed conventional baseline and scientific scope

A conventional learner told family (1), given the same four probe choices, output design and resources, can estimate the same rank-one contrast and perform the same SVD/polar receiver. It shares the bound. It would be unfair to compare this with generic full-environment tomography or a recovery algorithm deprived of the family promise. The contribution at actual scope is a concrete sufficient-statistic route that removes the flag-eigenvalue requirement of the earlier generic all-CPTP unique-oracle certificate. It also treats arbitrary-rank flag states and retained-memory conditional drift. It is not a demonstrated practical or historical superiority result.

Unknown arbitrary decoder families, changing V, coherences with uncontrolled phase, uncalibrated acquisition/control, and scalable high-fidelity preservation remain outside the theorem. The mechanism may be useful scientific capital if broader recoverable families admit similarly accessible contrast statistics; that extension remains open.

## Sources and evidence

- A. Klappenecker and M. Rötteler, *Mutually Unbiased Bases are Complex Projective 2-Designs*, arXiv:quant-ph/0502031, Theorem 3 and finite constructions, https://arxiv.org/pdf/quant-ph/0502031. Governing theorem and construction passage read in this pass. Used for finite design existence/identity, not novelty of this protocol.
- J. A. Tropp, *Freedman's inequality for matrix martingales*, ECP16 (2011), 262–270, Corollary 1.3, https://tropp.caltech.edu/papers/Tro11-Freedmans-Inequality.pdf. Actual rectangular bound and dilation passage read. Used only for the tail inequality; moment constants and receiver perturbation are derived here.
- Ordinary finite-MUB sampling pilot with adaptive public-history drift and a compiled two-column QR matrix: `flagged_loss_coherence_finite_receiver_pilot_20261028.py/.json`. Simulation only; the learner does not access the hidden source-state labels.
- Exact algebraic physical fixture and finite MUB checks: `flagged_loss_coherence_finite_receiver_exact_20261028.py/.json`.
- The earlier `general_extremal_recovery_face_acquisition_20261028.md` supplies a different, reviewed generic support/dual route; its receipt does not automatically cover this structured theorem.
