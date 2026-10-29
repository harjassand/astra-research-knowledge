# Independent receiving review: EB resolvent and actual-prior transfer

2026-10-29. Reviewer: review_finite_quantum_sampler. Verdict: PASS for the constant-weight CPTP-branch theorem, with SUPPORT_CLARIFICATION.md mandatory; PASS separately for the finite-depth TNI salvage. The rejected general left-resolvent normalization is correctly rejected. No unrestricted N371 closure, many-noisy-qubit tensorization, cheap recovery implementation or historical novelty is accepted.

## 1. Support and channel types
Let Phi:A->B have a decomposition alpha B_EB+(1-alpha)C into CPTP channels, alpha>0. For a faithful actual input prior sigma, the universal averaged rotated-Petz map R reverses Phi on the prior. It is TP on supp(Phi sigma). The requested mandatory clarification supplies an explicit CPTP extension outside that support: project onto it, apply R, and replace the orthogonal-complement trace by sigma. This is a CP instrument sum, not a coherent projection asserted to be lossless on arbitrary inputs. For faithful sigma every Phi(rho) is supported in supp(Phi sigma), so the extension does not change the relevant recovery theorem. In the unital qubit application Phi sigma is already faithful.

Hence E=R B_EB and D=R C are honest CPTP maps A->A, with E entanglement breaking. The recovered map Psi=R Phi fixes sigma and decomposes as alpha E+(1-alpha)D. At alpha=1 the argument reduces to F=E=Psi, without requiring a residual channel to be defined by division by zero.

## 2. Correct resolvent ordering and trace preservation
Set Q=(1-alpha)D. Since a CPTP map has diamond norm one, ||Q||diamond=1-alpha<1. Thus S=sum_(k>=0)Q^k converges in diamond norm with ||S||diamond<=1/alpha. F=S alpha E is a convex sum of EB CPTP channels D^k E with nonnegative scalar weights alpha(1-alpha)^k summing to one. It is therefore CPTP and EB. In finite dimensions EB closure also follows from the closed separable-Choi set. The order is E FIRST, followed by k uses of D, with k drawn from a geometric distribution; it is not a state-dependent first-hit stopping protocol.

The composition identity is

 id-Psi=(id-Q)-alpha E,
 S(id-Psi)=id-S alpha E=id-F.

There is no illicit commutation of E and D. Tensoring this linear identity with a reference and applying the diamond norm gives T(rho,F rho)<=alpha^-1 T(rho,Psi rho). Also (id-F)sigma=0, so the prior-adapted EB map fixes the actual prior even though E and D need not fix it individually.

The finite-depth approximation replacing the tail by any specified EB replacement channel is CPTP and EB, and has half-diamond error at most (1-alpha)^m. This follows because both omitted tail and replacement have the same scalar trace weight, each of diamond norm (1-alpha)^m. The construction establishes existence/convergent finite approximation, not cheap access to the Petz map or a new physical source inverse.

## 3. Universal recovery and actual-prior averaging
The primary dependency is Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3, Theorem 2.1 and Remark 2.2, with reference stabilization in Remark 2.4. These source passages were directly checked in the preceding nonunital review in this same research session. The beta0-average uses t/2 modular exponents and provides L>=-2log F with unsquared fidelity. Therefore T(rho,Psi rho)<=sqrt(1-exp(-L))<=sqrt(L), for natural-log relative entropy.

When sigma is the ACTUAL ensemble barycenter, the average relative-entropy loss equals the actual Holevo loss delta exactly. Jensen then gives average T(rho_x,F rho_x)<=sqrt(delta)/alpha. No stationarity assumption or kappa is needed because recovery and F are adapted to that prior. This differs materially from insisting on one fixed dephasing selected only by the channel.

For ensemble mean sigma_A tensor omega_R, the recovery factors as R_A tensor id_R on the support of omega_R, and all resolvent algebra factors accordingly. Correlated individual letters are allowed. The resulting comparator is EB on A only; F tensor id_R is not globally EB on AR. An arbitrary correlated barycenter need not yield this factorization and is not accepted.

## 4. Uniform unital self-compatible qubits
The received Pauli-pairing proof supplies an actual constant-weight EB CPTP branch with alpha=1-s2>=1-1/sqrt(2). Input/output unitary gauges preserve the EB property and trace preservation; the EB branch may mix different output conjugations of the same input dephasing. The residual is a CPTP mixture of the unpaired unitaries. Thus the generic theorem yields the coefficient 2+sqrt(2) for every faithful actual qubit prior, including coherent and nonstationary ones.

The mandatory clarification closes the remaining endpoint: a singular qubit mean is pure, so every positive-weight A ensemble letter equals that pure state and constant re-preparation gives zero error. With a product reference mean the letters factor as that A pure state tensor possibly different reference states, so local replacement again has zero disturbance. No singular inverse is needed. These facts justify EVERY actual qubit prior; they do not automatically extend the theorem to arbitrary nonunital channels or many noisy qubits.

## 5. Exact rejected TNI extension
The submitted two-state classical example has E=[[1/2,3/4],[0,0]], R=[[0,0],[1/2,1/4]]. E+R is stochastic and E's effect is bounded below by I/2, but (I-R)^-1 E has column sums 5/6 and 5/4. It is not TP and increases trace on one input. Conversely E(I-R)^-1 is TP, but its deficit identity has the opposite composition order and does not give the desired bound on the original one-step residual. I reproduced both rational matrices exactly. Full-rank event effects alone do not justify the constant-weight proof.

## 6. Separate valid finite-depth TNI salvage
For Psi=E+R with E CP EB, R CP and E†I>=alpha I, positivity implies R†I<= (1-alpha)I, so ||R^m||diamond<= (1-alpha)^m. The expansion of (E+R)^m-R^m contains only CP words with at least one E. Each word is EB under arbitrary CP pre/postcomposition, so the difference is CP EB. Its missing trace effect is exactly (R^m)†I. Adding the replacement event Tr[R^m(X)]tau makes B_m CPTP and EB.

Both R^m and its replacement event have diamond norm ||(R^m)†I||, giving half-diamond distance between B_m and Psi^m at most (1-alpha)^m. Independently, the telescoping identity plus CPTP trace contraction gives T(rho,Psi^m rho)<=m T(rho,Psi rho), including arbitrary reference. Thus the stated average bound m sqrt(delta)+(1-alpha)^m follows under the same actual-prior recovery conditions. This is not a repaired normalization of the invalid left resolvent; it is a different finite channel construction. A uniform positive event effect remains an additional premise. The logarithmically weaker optimized rate and the absence of an implementation/novelty claim are correctly stated.

## Independent evidence
All original and support/salvage manifests verified. Independently constructed actual beta0-averaged recovered maps for 24 coherent-prior unital self-compatible phase-family channels with unrelated input/output gauges. Computed the full superoperator resolvent, checked TP, Choi positivity, qubit Choi PPT, fixed-prior identity and the residual identity. Maximum residual was 3.94e-16, fixed-prior residual 6.33e-15. Actual correlated-letter ensembles with product coherent barycenter and reference dimensions 2,3 satisfied the direct Holevo-loss bound. PPT is only a diagnostic here; the convex EB construction proves EB generally.

For the TNI salvage, an independent NONCOMMUTING quantum event uses residual Kraus diag(4/5,3/5) and an EB event preparing |+> with effect diag(9/25,16/25). At depths 1 through 8, exact rational calculations verify TP of the completed map and all 240 Choi/PPT principal minors; the residual effect norm is exactly (16/25)^m. This complements the general CP-word proof. None of these tests is hardware execution or a proof of cheap implementation.

## Disposition and remaining boundaries
The actual-prior penalty is legitimately removed for the stated uniform unital-qubit class by changing to a prior-adapted EB comparator. The proof does not retain the original fixed dephasing, does not acquire an unknown prior for free, does not prove a dimension-independent many-qubit theorem, and does not solve unrestricted N371. Universal recovery, EB closure and resolvents are established tools; historical priority of this explicit transfer remains unassessed. The support clarification and TNI rejection/salvage distinction must travel with this receipt.
