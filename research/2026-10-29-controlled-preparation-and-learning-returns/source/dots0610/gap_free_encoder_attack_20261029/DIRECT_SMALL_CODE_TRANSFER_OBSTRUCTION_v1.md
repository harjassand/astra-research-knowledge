# A pointwise obstruction to replacing the full-singlet transfer by a fixed small code
2026-10-29. New author proof, receiving review pending. This is a limitation of the same unweighted full-array star-loss certificate, NOT a lower bound on all learning algorithms or on local verification.

## Construction
Let n=2m>=4 and let R=P_sym be the rank n+1 projector onto the completely symmetric spin sector. The source unitary U=I−2R is in the true collective algebra (true local frame identity). It is a globally spin-sector-conditioned phase; no local-noise implementation is asserted. Choose the candidate local frame W=Z on the first site of each pair (1,2),(3,4),...,(n−1,n). Phases making each Z an SU(2) element do not change any subspace or conjugation. Put
 Q=W[P_4 tensor |s><s|^(tensor(m−2))]W†,
where P_4 is the two-dimensional four-spin singlet space and s=(01−10)/sqrt2. Thus Q is a two-dimensional singlet subcode in its candidate frame, with one logical four-spin block and singlet spectators.

Every vector of Q has computational weight m, because W commutes with J_z. Consequently A=E†RE has rank at most one, where E is an orthonormal encoding isometry onto Q. Only the weight-m Dicke state in R can overlap Q.

An explicit orthonormal four-spin singlet basis consists of s_12 s_34 and
 [|t+>_12|t−>_34+|t−>_12|t+>_34−|t0>_12|t0>_34]/sqrt3.
After applying Z on sites1,3, their amplitude sums over weight2 are 2 and −2/sqrt3. Each remaining twisted singlet is t0, with amplitude sum sqrt2. Therefore the two coordinates of E†|Dicke(n,m)> are, up to the displayed sign,
 v0=2^(m/2)/sqrt(binomial(n,m)), v1=−v0/sqrt3.
It follows that A=|v><v| has nonzero eigenvalue
 w=Tr A=(4/3) 2^m/binomial(n,m).
This is <=1 for n>=4 (n4 gives8/9, not2/3).

## Completed decoder calculation, not a raw-loss substitution
Use the usual projection decoder E† followed, on leakage, by replacement with an arbitrary fixed logical density matrix tau. The surviving logical Kraus operator is K=I−2A. The leakage effect is L=I−K†K=4(A−A²). For logical dimension2 the total entanglement fidelity is exactly
 F_e=|Tr K|²/4+Tr(tau L)/4
    =(1−w)²+Tr[tau(A−A²)].
Since A is rank one with eigenvalue w, the reset contribution is at most w−w². Hence completed Bell infidelity satisfies
 1−F_e >= w,
with equality when tau is the nonzero eigenvector of A. In contrast the raw Bell loss is 2w−w². A maximally mixed reset generally does not attain the bound. Bare endpoint logical Pauli twirling preserves F_e, so it cannot remove this example. A more informed recovery exploiting U is outside this fixed-decoder comparison and is not excluded.

## Same star losses are exponentially smaller
For a candidate twisted star swap S_i=W Swap(1,i)W†, the unitary loss is
 delta_i=||[U,S_i]||_F²/(2D)=2||[R,S_i]||_F²/D,
where D=2^n. For any rank-r projector R and Hermitian unitary S,
 ||[R,S]||_F²=2[r−Tr(R S R S)]<=2r.
Thus delta_i<=4(n+1)/2^n and
 sum_i delta_i<=4(n²−1)/2^n.
Combining with binomial(n,m)<=2^n yields
 (completed Bell loss)/(sum_i delta_i)
 >= 2^(n/2)/[3(n²−1)].
There can be no polynomial-in-n pointwise upper transfer factor from these exact unweighted star losses to every fixed small code, even for this permitted collective-algebra source and candidate local frame. A zero denominator would only strengthen the obstruction; the finite fixtures have positive denominator.

## What the global orbit changes, and what it does not
The full candidate singlet sector P=W P_sing W† is also contained in weight m. Hence Tr(PR)<=1. Its normalized raw Bell loss for this U is 4a(1−a), a=Tr(PR)/d, so at most4/d. The physical permutation orbit lets a chosen small subcode inherit this full-P loss rather than its concentrated fixed-Q loss. This is a genuine pointwise transfer distinction, not exclusive availability of polynomial learning: a high-rate subcode K'>d/2 with full-path testing has a comparable transfer bound without that orbit.

Both error scales in this counterexample become exponentially small. It proves neither a sample-complexity separation nor an experimentally consequential noise advantage. A local matching test of Q can still verify it with a constant gap; what fails is an automatic polynomial acquisition bound for that Q from this particular global star bank. Candidate-dependent acquisition, another recovery or another statistical objective remain possible.

## Reproducible check
check_small_code_obstruction.py constructs the exact indicated subspace numerically for n=4,6,8,10, computes A, the physical projection/reset fidelity and every twisted-star loss using the symmetric-sector isometry, and checks the analytic formulas. It also records exact rational lower bounds for n20,40,80,160. The program avoids attributing a numerical asymptotic test to a proof; the displayed inequalities supply the all-size result.

## Extension to the actual full product-block code (root contribution, independently checked)
Take n=4h and Q=W(P_4)^(tensor h)W†, with K=2^h. This addresses the full h-logical-qubit block code rather than the smaller spectator construction. Again Q lies in magnetization zero, and A=E†RE is rank one. The squared amplitude sums of one twisted four-spin block total 4+4/3=16/3, so
 w=Tr A=(16/3)^h/binomial(4h,2h).
For dimension K the exact completed fidelity is
 F_e=(1−2w/K)² + 4 Tr[tau(A−A²)]/K².
The largest possible reset contribution is 4(w−w²)/K². Therefore even the best fixed reset gives
 1−F_e=4w(K−1)/K².
The star-loss upper bound is unchanged. Their ratio obeys
 (completed Bell loss)/(sum_i delta_i)
 >= (1−1/K)(8/3)^h/(n²−1).
This grows exponentially with h, while the actual completed error tends to zero exponentially. The same limitations on the meaning of this pointwise distinction apply. The program additionally constructs the h1,2,3 product codes, checks their Dicke projection and optimal completed reset loss, and records the exact-rational ratio lower bound.

## Decoder scope strengthened: every exact left inverse (independent reviewer contribution)
The preceding fixed-reset formula in fact covers every CPTP decoder D that exactly decodes the original noiseless code, D(E rho E†)=rho. This includes product local block decoders, not only a single global projection/reset.

Choose Kraus operators D_a. Since the restricted channel is identity, D_a E=c_a I with sum_a|c_a|²=1. Trace preservation gives
 sum_a c_a* D_a P_perp = E†(sum_a D_a†D_a)P_perp=0.
Therefore the decoder kills the sum of code/leakage cross terms. The leakage amplitude B=P_perp U E has rank at most one: R E has rank one and so does its projection. Its decoded contribution must be of the form Tr(L rho)tau for one fixed density matrix tau, with L=B†B=4(A−A²). The code contribution is K rho K†, K=I−2A. Thus the fidelity formula and optimal lower bound hold for every such exact left inverse. A recovery designed to invert this particular U while not decoding the noiseless E exactly is not covered; neither are general adaptive acquisition strategies. This strengthens the comparator match without establishing a general recovery impossibility.
