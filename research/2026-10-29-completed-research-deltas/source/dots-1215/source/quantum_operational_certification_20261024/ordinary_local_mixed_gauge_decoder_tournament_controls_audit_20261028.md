# Independent physical and finite-control review: local mixed-gauge tournament

28 October 2026. This is a proof review, with **zero new source calls and no new simulation**. It does not alter the frozen local pilot, its data, or its qualifications. The final receipt will bind the reviewed manuscript separately. The Bures estimator and global common-algebra risk lemma are imported only through their already received finite interfaces.

## Scope and verdict

The construction is sound under its explicit known-register, common local algebra, positive Pauli-gauge instrument, calibrated X/Z contrast, memoryless source, and paid-control assumptions. Arbitrary noncommuting gauge states do not invalidate the physical marginal experiment or the difference-observable tournament. This remains a structural-family theorem protecting **one logical qubit**, not unrestricted noise identification, a hardware result, or a superiority claim over an equally informed conventional learner.

The source must supply an actual known physical n-qubit tensor product and a valid common-support width w. No random dimension reduction, latent retained frame, or free alignment of separately estimated physical bases is used. The estimate on every patch is expressed in the same known physical coordinates that its later controls address.

## 1. True-patch reduction retains the margin

For j in {X,Z}, write the global calibrated contrast as X_j=B_j K_j, where K_j=|X_j| is positive, commutes with B_j, and satisfies K_j>=kappa rho. On a true patch I with B_j=B_j^I tensor I, put R_j=Tr_out K_j. Partial trace gives

    X_j^I=B_j^I R_j,   [B_j^I,R_j]=0,
    R_j>=kappa rho_I.

Since B_j^I is a Hermitian unitary, |B_j^I R_j|=R_j, including on the kernel. Thus the relative sign margin survives partial trace exactly. Also [B_j^I,rho_I]=0. No commutation among gauge matrices, gauge spectral lower bound, or product state across physical patches is needed. The two true patch reflections give a representation of the one-qubit Pauli algebra, so their commutant supplies a local multiplicity subsystem; this is a proof decomposition, not a supplied gauge basis or an implemented unknown inverse.

The lower bound kappa rho is assumed only for X and Z. H_Y>=0 does not imply the same calibrated Y margin. This restriction must be maintained in the manuscript's generic-index notation.

## 2. Correlated parallel banks are real marginal experiments

Let a color consist of disjoint physical patches I_1,...,I_k. After N_B independent source calls, the stored state is r^{tensor N_B}; within each copy it may be entangled across these patches. Reordering tensor factors, the marginal on the N_B copies of a particular patch I is exactly (r^I)^{tensor N_B}.

Let Phi_I be that patch's entire Bures estimation instrument, including local quantum memory, random purification, finite-Clifford measurements, its own adaptive control, and its final classical estimate. It is a trace-preserving channel on its own bank. For an event F of the estimate at I, with induced POVM effect M_F^I, the tensor product of all the disjoint instruments gives

    Pr(F)=Tr[(M_F^I tensor I_rest) r^{tensor N_B}]
         =Tr[M_F^I (r^I)^{tensor N_B}].

This is the ordinary local Bures estimator's required marginal law. The other estimators can have correlated outcomes; their independence is not used. Each estimator's decisions may depend on its own records, but not on another patch's outcomes in a way that changes its prescribed experiment. Uniform anchor labels are genuine input controls; the estimator guarantee is applied to the anchor mixture, not conditioned on per-copy labels.

The starts-modulo-w coloring has q=min(w,M) nonempty colors for M=n-w+1. No two same-color intervals overlap. Four banks per color therefore consume exactly 4qN_B source calls. There are 4M state estimates, so beta_A/(4M) per estimate suffices by a union bound. With dimension and rank bound both 2^w, the received Bures interface has D=4^w and gives precisely

    N_B=ceil[(80*4^w/m) log(48*4^w*M/beta_A)].

No sample is cloned. Each source call contributes disjoint registers to the estimators of its color; overlapping candidates use different color banks.

## 3. Every estimated decoder is an actual channel

For arbitrary learned Hermitian reflections X',Z', define P=(I+Z')/2 and

    V=[P; X'(I-P)].

Then V†V=P+(I-P)=I, without requiring X' and Z' to anticommute. A fresh output qubit, the literal isometry, and discard of its residual register therefore define a CPTP channel on every estimation history, including failures. The exact pullbacks are

    A_Z=Z',
    A_X=(X'-Z'X'Z')/2,
    A_Y=i(X'Z'-Z'X')/2.

These, not the raw X' treated as if it anticommutes with Z', are the actual measurement operators used for comparison. They are Hermitian contractions because a unital positive adjoint maps the interval [-I,I] into itself. They have the candidate's actual patch support.

Finite algebraic or rational range projectors can specify exact reference reflections. A backward-error certificate applies to the nearby Hermitian matrix whose sign is implemented. Exact diagonalization of an unknown source operator, floating vectors declared exactly unitary, and a smallest nonzero source eigenvalue are not prerequisites.

## 4. Difference measurements retain the essential covariance

For two frozen candidates let H_j=(A_j^b-A_j^a)/2. Choose j uniformly from X/Z, sign s uniformly, and one anchor uniformly. The intended outcome is that of sH_j on this one actual source output. Then

    E Z=r_a-r_b,
    E Z^2=(1/8) sum_(j=X,Z) Tr rho (A_j^a-A_j^b)^2.

Because (A-B)^2<=2I-{A,B} for a contraction A and reflection B, the manuscript's CPTP two-axis relations give

    E Z^2<=2(ell0_a+ell0_b)<=4(r_a+r_b)/kappa.

The relevant small quantity is excess two-axis risk over the common unknown floor; the floor cancels both in the mean and in this second moment. Subtracting independent noisy decoder error tests would not reproduce the second moment.

### Disjoint candidates need no long-distance quantum gathering

For disjoint candidate patches, A_j^a and A_j^b commute. Measure their two local spectral observables on the **same** source output, keep the joint outcomes (a,b), and return s(b-a)/2. The product spectral PVM refines the spectral measure of their difference, hence its first and second moment operators are exactly s(A_j^b-A_j^a)/2 and (A_j^b-A_j^a)^2/4. This is valid for entangled outputs; it does not replace the joint state by a product of marginals.

No quantum state need be routed between distant disjoint patches for this implementation. It does require both local measurements, the joint classical record, and paid classical communication/storage. Independently resampling from the two outcome marginals is not equivalent and is forbidden.

For overlapping width-w intervals, their union is a contiguous interval of width at most 2w-1. A generic spectral measurement therefore needs dense controls only on this nearby union. An O(nw) SWAP gather is a possible conservative alternative for arbitrary unions, not a necessary cost of the preferred interval implementation. The final deployed decoder acts on one selected width-w patch, not on a tournament-sized union.

## 5. Finite spectral controls do not need an eigenvalue gap

For each unsigned H_j construct C_j=V_j diag(c_l)V_j†, with V_j an exactly unitary reference circuit, rational c_l in [-1,1], and certified ||C_j-H_j||op<=xi. Measure V_j†, read its computational basis label, and return s c_l. The mean bias is at most xi and

    ||C_j^2-H_j^2||op<=2xi.

Thus the actual reference measurement has second moment at most 4(r_a+r_b)/kappa+2xi. For disjoint patches one may instead approximate each local contraction within xi, preserve both contraction bounds, and use their commuting joint measurement; the difference retains the same total xi error.

A gap-free finite construction is approximate Jacobi diagonalization. For a d_c-dimensional Hermitian matrix, eliminating a largest off-diagonal entry decreases squared off-diagonal Frobenius mass by at least a fraction 2/[d_c(d_c-1)]. The desired backward residual is therefore reached after O(d_c^2 log(d_c/xi)) exact rotations; finite rotation and coefficient errors receive smaller predetermined budgets and a final residual certificate. One asks for a nearby diagonalizable matrix, not for stable eigenvectors of the exact matrix. Rounding/clipping the spectral labels and compiling the known unitary are included in the residual/reference and implementation budgets. Small or degenerate eigenvalues do not require division by an unknown gap.

The raw-sign construction has the same distinction: an exactly physical reflection of a certified nearby matrix is sufficient. The proof never requires estimating an exact spectral projector of the unknown source at a tiny gap.

## 6. Independent check of the finite comparison constants

Let R=r_a+r_b. With xi<=kappa t/4096, N_pair>=512 L/(kappa t), variance at most 4R/kappa+2xi, and centered range at most 2, a conservative Bernstein bound is

    |Zbar-E Z|<=sqrt(2 variance L/N_pair)+4L/(3N_pair).

The main square-root term is at most (1/8)sqrt(tR). The remaining square-root slack, range term, and mean bias total less than

    t[1/sqrt(524288)+1/384+1/4096] < t/96.

This proves the manuscript's looser (1/4)sqrt(tR)+t/96 bound with room. L=log[2(M-1)/beta_Q] and M-1 fresh comparisons yield the asserted union bound; conditional independence of each new source bank from previous choices is sufficient.

The balanced bracket correctly avoids treating two bad near-tied candidates as a fast small-gap decision. Its fixed comparison cap yields a relative-plus-additive winner bound instead. Following a minimum-risk branch of depth h, eta=1/(2h) gives r_selected<=2r_min+t h^2. The stated m=kappa^3 epsilon/2^17 and t=kappa epsilon/(320h^2) imply r_selected<kappa epsilon/160 and then uniform decoder regret <=epsilon/20. M=1 must skip the comparison logarithm and h denominator, as the manuscript does.

## 7. Memory, routing, and conventional comparator

One sequential color/bank can store nN_B output qubits, **plus** the Bures estimator's purification/Schur and compilation workspace. The collective controls across N_B stored copies are not supplied by output-line locality for free. The architecture must pay memory-bank connectivity and routing; a conservative serialization onto a declared finite nearest-neighbor storage layout gives a finite polynomial overhead in the total storedproducer-workspace/workspace qubit count. This acquisition-routing cost is distinct from local candidate execution and the disjoint/overlap comparison improvement.

For fixed w, generic w-qubit candidate controls and at-most-(2w-1)-qubit overlapping comparison controls have finite dense synthesis costs polynomial in 2^w and precision. The O(poly(w)4^w) decoder and O(poly(w)16^w) comparison scaling are generic-unitary costs, not shallow-circuit or constant-depth claims. Jacobi's explicit finite fallback can require extra polynomial classical work beyond a shorthand cubic diagonalization count. All source inputs, resets, purification ancillas, quantum lifetimes, local readouts, joint classical outcome records, and synthesis/arithmetic errors belong in the linked finite process budget. A required fixed endpoint would add final output routing.

An equally informed conventional subsystem learner can use exactly the same correlated-bank marginal experiment, acquired reflections, physical difference measurements, and balanced tournament. No fair comparison may deny it these controls. The unlocalized construction removes the flat-gauge promise at a collective-memory and polynomial-n source/control price. The preferred coarse-localization improvement below independently proves logarithmic-n source dependence; neither construction inherits the previous flat-gauge pilot's discrete exact-word certificate.

## 8. Preferred coarse overlap localization and the expansion comparator

Fix any padded width-w true interval I_* containing both exact logical generators. The global X contrast obeys

    B_Z X_X B_Z=-X_X.

For an interval J disjoint from I_*, B_Z acts entirely on the traced-out complement. Unitary invariance of partial trace then gives X_X^J=-X_X^J, hence X_X^J=0 exactly. This uses the exact common anticommuting algebra, not flat gauge, a gauge basis, or an approximate support fit. On I_*, the sign margin yields ||X_X^I_*||_1=Tr Hbar_X>=kappa.

Two coarse X+/X- banks with m0=kappa^2/512 give

    ||Xhat_X^J-X_X^J||_1<=2sqrt(2m0)=kappa/8.

An additional certified kappa/16 trace-norm calculation error puts the true score at least 13kappa/16 and every disjoint score at most 3kappa/16. Selecting the first score above kappa/2 therefore finds an interval J overlapping I_* on the simultaneous coarse good event. It does not identify the logical algebra or certify source-family membership. If no score passes, the deterministic fallback interval and all later costs remain; the coarse bad event is paid, not postselected away.

The two-bank coloring proof is unchanged. There are 2M estimates, confidence beta_0/(2M) each, and exactly

    2q ceil[(40960*4^w/kappa^2) log(24*4^w*M/beta_0)]

coarse source calls. The retained input controls are still ordinary X eigenstates and uniformly chosen actual anchors.

All width-w intervals overlapping J have starts within w-1 of its start. Their number is at most R_max=min(M,2w-1), they form a contiguous list of starts, and they include I_* on the coarse good event. Fresh fine banks may be conditioned on the entire coarse record because their chosen patches are then fixed and the source resets independently. The manuscript's R_max-based logarithms, maximum height, color count, and comparison cap give a genuine predetermined finite horizon. The joint failure ledger now includes beta_0 as well as beta_A, beta_Q, and beta_C. The R_max=1 branch correctly skips all logarithms involving R_max-1 and all divisions by the bracket height.

The union of these candidate intervals is obtained by extending J by w-1 sites at each end, clipped at the physical boundaries. Its width is at most min(n,3w-2), and it contains I_*. This proves both alternatives:

1. Fine acquisition and tournament retain width-w deployed decoders, with at most 2w-1 fine candidates. Source dependence on n is only the coarse confidence logarithm; physical output, memory, coarse estimator count, and control/record handling still scale with n.
2. An equally informed conventional learner can skip selection by learning directly on the expanded patch K. Four fine banks at m_exp=kappa^2 epsilon/32768 give uniform decoder regret at most 616m_exp/kappa^2<epsilon/20. The simpler construction pays exponential dependence on the larger width W, potentially up to 3w-2, rather than denying this alternative to the conventional baseline.

For the expansion route's whole-process predetermined horizon use W_max=min(n,3w-2), even if a boundary-truncated selected patch has a smaller actual W. The smaller actual route can be executed within this worst-case cap. This also fixes its memory, workspace, synthesis and implementation-precision budgets before source outcomes.

Both final complete source caps include one additional payload call, not merely the calibration/selection/encoder-training calls. Its actual decoder controls are included in the linked implementation allocation. No payload is delivered for free by the proof.

## Evidence status

This review supplies mathematical derivations and finite-interface checks only. It generated no outcomes, accessed no sourceproducer-workspace/private pilot data, and changed no frozen pilot artifact. The companion controls receipt binds the final manuscript and this review. There is no remaining mathematical objection under the stated contract.
