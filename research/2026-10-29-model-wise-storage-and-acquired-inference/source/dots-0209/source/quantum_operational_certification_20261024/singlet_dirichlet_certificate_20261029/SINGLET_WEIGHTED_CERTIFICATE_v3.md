# Singlet-weighted local certificate with linear-n statistical penalty
2026-10-29. New extension, pending independent review. V1/v2 unchanged.

## Statement
Retain n even, frozen frame, full singlet sector P of dimension d0, and chosen K-dimensional power-of-two subcode E from v1. Replace calibration input I_D/D by P/d0, prepared as below. Define
δ^P_ij=1−Tr[P S_ij N†(S_ij)]/d0,
q_P=(1/[2M])Σδ^P_ij.
For arbitrary CPTP N, the same completed decoder and retired-key logical Pauli service obey
1−Fe(Λ)=(1/2)||Λ_tw−id||diamond
≤(d0/(Kn))Σδ^P_ij=(d0/K)(n−1)q_P.
Since K>d0/2, the coefficient C_P=(d0/K)(n−1)<2(n−1). This improves the maximally mixed physical input's O(n^(5/2)) coefficient to O(n), at the cost of preparing n/2 entangled singlet pairs and a nondemolition input singlet/triplet measurement. It still does not beat direct full logical 2-design validation's O(1) statistical coefficient; it avoids full Schur encoding/decoding on each calibration trial.

## Weighted Poincare proof
Consider matrices X:P H→H, with the ordinary Hilbert–Schmidt inner product on this rectangular map space. Permutation conjugation acts unitarily as
R(π)X=S_π X (S_π|P)†,
since P commutes with all permutations. Thus the SAME complete-transposition gap n applies. For X_a=K_a P (or its rectangular restriction), its invariant projection is G(K_a)P. Schur–Weyl says this is α_a P: the singlet permutation irrep occurs exactly once in H, with SU(2) multiplicity one.

For a transposition S, [S,K_a P]=[S,K_a]P. Summing squared norms and using trace preservation and [S,P]=0 gives
Σ_a||[S,K_a]P||F²=2d0−2 Re Tr[P S N†(S)]=2d0 δ^P_S.
The trace is real: PS is Hermitian, N†S is Hermitian. The expression proves δ^P≥0 without any assumed noise model. Hence
Σ_a||(K_a−G(K_a))P||F²/d0≤(1/n)Σδ^P.
Since EE†≤P,
Σ_a||(K_a−G(K_a))E||F²/K
≤(d0/K)Σ_a||(K_a−G(K_a))P||F²/d0.
Apply v1's orthogonal-Bell-component proof. No operator-norm lift or rare-state exclusion is involved.

## Efficient calibration input without Schur compilation
Start with the pure tensor of n/2 standard two-qubit singlets, which lies in P. Draw a uniform random permutation π∈S_n and permute its physical sites, then apply the frozen local frame. The singlet sector is an irreducible S_n representation, so Schur's lemma gives the EXACT ensemble average
E_π[S_π |singlet-pairs><singlet-pairs| S_π†]=P/d0.
This is not a coherent sum over n! permutations and does not require computing a group twirl. A uniform permutation can be sampled classically by Fisher–Yates with uniform integer draws, and compiled by O(n) arbitrary-pair SWAPs, or O(n²) nearest-neighbor SWAP routing. Equivalently sample a uniform perfect matching and prepare singlets directly on its pairs. Pair orientation/global signs do not change density matrices. O(n) Bell preparations plus routing and local frame rotations suffice; classical random-bit/rejection costs are paid. Individual trials are mixtures drawn from actual pure preparations, not presumed access to a thermal singlet ensemble.

The preparation record must not independently affect N; discard it or keep it unavailable to the source. As usual, N may respond arbitrarily to the quantum input through its fixed CPTP action.

## Correct positive test and an important rejected shortcut
Select a random edge. On the prepared P/d0 ensemble, perform the Lüders two-outcome projective measurement of S, obtaining s. Implement it with a fresh local ancilla |+>, ONE controlled-S, and X measurement immediately BEFORE N; the ancilla is then discarded. The surviving data state has subnormalized form Π_s P/d0 because [Π_s,P]=0. Apply N, then measure S on the same pair (ordinary final Bell readout is sufficient), yielding t. Record failure iff s≠t.

Pr(s,t)=Tr[Π_t N(Π_s P)]/d0,
E[st]=Tr[S N(SP)]/d0=Tr[P S N†(S)]/d0,
so failure probability is δ^P/2 exactly. No quantum ancilla or reference must survive the storage horizon. Input control is local on the chosen pair plus a short-lived ancilla; the output only needs the swap effect.

DO NOT replace the input Lüders measurement by a fully resolving Bell measurement and subsequent preparation. That would reveal/dephase distinctions inside the triplet subspace and can destroy correlations with the rest of the singlet ensemble. V2's uniform pair-Bell shortcut was valid for maximally mixed physical input, not automatically here. A coherent singlet-versus-triplet instrument is the new required interface.

## Confidence and controls
For a prespecified independent validation block, use v1's exact binomial q_U bound with C_P replacing C. Zero failures certify error ε after
m≥(d0/K)(n−1)log(1/β)/ε,
so O(n ε^(−1)log(1/β)) full-channel calls. Each call requires O(n) pair preparations/routing, one constant-size input parity instrument, one pair readout, and full T primitive steps if N=N_T. This is O(n²/ε) physical preparation volume ignoring geometry, not linear total resource cost.

Actual test bias b_test is multiplied by C_P=O(n), rather than O(n^(5/2)); service control error remains separately added. Approximate randomization/preparation is part of b_test. Same-N, independent reset between validation trials, fresh frozen-frame validation, confidence spending for repeat searches/stops, and no future-bath extrapolation remain mandatory. No physical hardware or historical novelty assertion is made.
