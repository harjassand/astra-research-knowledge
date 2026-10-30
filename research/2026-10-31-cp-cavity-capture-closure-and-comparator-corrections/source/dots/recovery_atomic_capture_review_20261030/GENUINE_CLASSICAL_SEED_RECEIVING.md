# Fixed-size capture of supplied genuine classical outcomes
30 October 2026, 17:14 UTC. Measurement-assisted seed receiving candidate. This deliberately does NOT claim coherent-pointer capture. The fixed-size source noise/moment premise is the accepted positive subset-moment/reset lift, used with its actual hypotheses.

## 1. Operational reference, not an immutable latch
The input is the genuine classical output m of an ACTUAL finite measurement instrument. Conditional on the complete outcome vector m, the physical raw-bit registers are in the computational product state |m>, tensored with an arbitrary DATA/bath state rho_(QB)^m. This factorization follows from the one-dimensional conditional classical bit subspaces; no independence of DATA/bath from m is assumed.

The original m is an analysis reference to a historical instrument outcome. The hardware is not given a protected immutable m register. Every raw physical latch is exposed to the stated noise immediately. Detector/output errors belong inside the supplied finite source instrument and its ATG error dictionary. If the source supplies only coherent pointers, this contract has NOT been met by merely writing a classical symbol m.

All following bounds are uniform in m and in the conditional retained bath state. Hence one may average over the genuine outcome distribution afterward. No conditional independence of future errors is inferred.

## 2. Actual finite seed circuit and subset premise
Choose seed size n0 FIRST, fixed independently of the computation horizon. Reset the n0-1 targets to zero with actual onsite resets, then copy the raw bit through a bounded-fanout CNOT tree. Depth O(log n0), storage O(n0), degree/body and gate strength are fixed constants. The reset time, gate duration and any raw-bit exposure during resetting are included. Pre-resetting targets before the source arrives is permitted if its actual waiting interval is also counted; it is not essential.

Use the accepted positive subset-moment/reset source lemma on the entire finite interval. Relative to the ideal raw |m> and target |0> inputs, it supplies commuting toggling-frame bit-defect projectors B_i with

 Tr[(product_(i in A) B_i) rho_toggled] <= p0^|A|     (S1)

for every finite A, with uniform constants conditional on m and arbitrary bath. The exact exponent p0=O(eta^a)+p_reset and circuit lightcone inflation are those of the imported lemma, not an assumption of independent Pauli faults. Z phases are immaterial to the classical copy relation. The reset target purity is not assumed; its residual parameter must be explicitly calibrated.

The nominal ideal seed circuit is block-disjoint between records and computational-basis linear. Each record j has a fixed seed defect cone C_j of size <=c0. Define A_j=OR_(i in C_j) B_i. The C_j are disjoint ideal cones; common-bath/q-body correlations are already in (S1). Witness expansion gives

 Tr[(product_(j in S) A_j) rho_toggled] <= p_seed^|S|,
 p_seed=c0 p0.                                      (S2)

If A_j=0, every physical seed bit after the ideal copy equals m_j. If A_j=1, no promise is imposed on that seed block. This is an actual positive commuting defect law, not a signed-HP trajectory.

## 3. Pay the EXPONENTIAL seed weight jointly
Let W_j be the atomic combined phase/root initial test for a record, expressed in the ideal-copy output chart. On its zero-cone-defect subspace, W_j=w_vac I, with w_vac=1+K V_root(vacuum), and phase factor1. On the finite seed space W_j<=w_max I, where a conservative bound is w_max=exp(C s n0), including the finite animal count, graph degree and root factor.

Because the CNOT seed map is a basis permutation, W_j and A_j commute in the toggling input chart, and

 W_j <= w_vac+(w_max-w_vac) A_j.                     (S3)

For any set S, expand the product of these POSITIVE upper bounds and apply (S2). This proves the JOINT moment

 Tr[(product_(j in S) W_j) rho_seed]
   <= [w_vac+(w_max-w_vac)p_seed]^|S|
   = A_seed^|S|.                                   (S4)

The dependence on n0 has not disappeared: choose n0 first, then calibrate reset residual and eta so (w_max-w_vac)p_seed is below a specified small epsilon_seed. Choose the root parameters so w_vac is also close to1. Then log A_seed is small, rather than an unexamined C n0 that could defeat a later phase barrier. Reset duration may be very large but is fixed after n0/source accuracy are fixed; its noise constant is paid before choosing eta. No uniform claim is made as n0 tends to infinity or eta changes while hardware is held fixed.

## 4. Initial signed phase flags and mixed weights
Let P_j be the seed phase-good cut relative to m_j and Q_j=I-P_j. In the same chart Q_j<=A_j. The exact initial ket/bra union decomposition has three non-all-good sector choices for every newly marked record: QXQ, QXP, PXQ. For any selected union D, positive-state Cauchy-Schwarz gives a trace/cb bound for each term using

 ||P_L rho P_R||_1 <=sqrt(Tr(P_L rho) Tr(P_R rho)).

The set of records constrained bad on the ket and bra has union D, so (S2) bounds the term by p_seed^(|D|/2) or better. Summing its at most 3^|D| choices yields

 initial-mark norm <=(3 sqrt(p_seed))^|D|.            (S5)

This is a norm bound on signed components, not a probability for those components.

Keep phase/root weights on a disjoint set R of remaining records. Since W_R commutes the cuts and cones, the same CS estimate uses the positive quantities Tr(W_R P_L rho) and Tr(W_R P_R rho). Expanding (S3) jointly with the required bad-cone factors gives

 Tr(W_R product_(j in L) A_j rho)
    <=p_seed^|L| A_seed^|R|.

Therefore the exact initial union component has the mixed weighted norm

 <=(3 sqrt(p_seed))^|D| A_seed^|R|.                  (S6)

This supplies the initial support/moment interface for the signed killed-flag construction without summing one-record gentle errors. Constants depend on fixed seed geometry and the imported moment convention only. A reference-stable formulation applies the same positive CS argument with an arbitrary retained reference; the supplied rho_seed is the actual positive joint state, not a presumed input-independent logical channel.

## 5. Interface and explicit limitations
Good seed sectors enter the old phase cut and have the joint weighted moment (S4); initial marked sectors are bounded by (S6), and their entire record internals may thereafter be analytically unrestricted. The new local-stochastic parameter need not be literally eta: it includes the declared reset calibration and fixed-cone exponent. Later growth contributes its separately controlled nominal/physical phase-mark parameter.

For quantum waiting, retain the ORIGINAL instrument outcome m as the analysis frame label. A final genuine read m' can differ on bad-capture records and on separately bounded local read errors. The ATG deterministic common-span receiving must then fold m'-m into record faults while propagating new boundary DATA errors through the final frame; this note does not assert that quantum receiving theorem.

The proof is not a coherent unknown-pointer encoder. It assumes an actual classical instrument boundary and includes no claim that finite-time dephasing alone is such a boundary. It does not grant perfect classical software, indefinite output storage, ideal final readout, autonomous scheduling, or native controller initialization.

### Complete-map version of the initial CS estimate
For fixed genuine m, view the seed preparation as a CPTP map T_m from the arbitrary conditional DATA/bath input, adjoining the fixed raw |m> and whatever reset-target initialization its uniform reset lemma permits. Uniformity of the subset/weighted bounds over every positive input and every retained reference gives the corresponding EFFECT inequalities, for example

 T_m^*(W_R product_(j in L) A_j) <= p_seed^|L| A_seed^|R| I.

A common Stinespring dilation then bounds the complete trace norm of the cross map X -> W_R^(1/2) P_L T_m(X) P_R W_R^(1/2) by the geometric mean of the two effect norms. This justifies the map-level version of (S6), rather than extrapolating a bound for one positive state to arbitrary signed inputs. No initially input-correlated bath is hidden inside a fixed logical channel: the conditional bath is part of the input space of T_m, and the norm contract/reset lemma is uniform on that space.
