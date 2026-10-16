# Tracked Pauli control: exact error-label bridge

## Verdict
**Yes, with an essential private-randomness/coarse-graining qualification.** Independent full initial Pauli twirls plus ideal, independently timed, exactly undone Pauli frame updates convert the lifted endpoint theorem into a positive Pauli-labelled joint data–bath channel. The endpoint bounds then constrain actual Pauli Kraus-label subsets, uniformly in the persistent bath state. This is stronger than a physical-syndrome bound and introduces no noise-free dephasing damage to the data.

It is an exact statement for isolated clean identity-control intervals. It is not automatically a statement about a channel retaining the initial random seed as an accessible classical output, about arbitrary compiled gates, noisy pulses, untracked dephasing, or correction-interleaved memory dynamics. Generic local interactions require the incidence/coloring qualification below.

## 1. Precise setup
Let the finite data Hilbert space D be partitioned into disjoint bounded patches D_i of m_i qubits. Let B be any finite persistent bath, with arbitrary external reference allowed. During a fixed interval [0,T], the lab Hamiltonian is H(t)=H_B(t)+sum_a h_a(t), Hermitian and with well-defined propagators. The h_a may have arbitrary shared/noncommuting bath factors. Bounds are operator norms on the full data–bath space; there is no weak-coupling approximation or bath reset.

Each patch has 2m_i Hermitian Pauli generators, chosen as single-qubit X and Z. Every generator has an independent Poisson clock of rate gamma_ij>0. A clock event applies its ideal instantaneous physical Pauli pulse. The noise Hamiltonian is fixed independently of these private clock realizations and of the initial frame; the bath receives no direct clock/seed/controller information beyond its ordinary interaction with the controlled data.

Choose an initial full Pauli F0=product_i F0_i uniformly and independently on each patch, independently of data, bath, external reference, and all clocks. Apply F0 noiselessly. Let G_eta(t) be the ordered product of subsequent physical pulses, starting at identity. The cumulative physical frame is F(t)=G_eta(t)F0. At T apply its exact inverse F(T)^dagger noiselessly. All relative/global Pauli phases are handled by these actual unitary products; global phases are immaterial.

The theorem concerns the averaged output channel after using the frame record to perform this inverse and then coarse-graining the initial seed. Future actions must not exploit retained private records in ways excluded from this channel model. A sufficient operational interface is to use fresh seeds/clocks each interval and discard their records after completing the tracked inverse. Independence of the fresh randomness, not independence of the data and bath, is required.

## 2. Exact toggling and initial-frame twirl
Let W_eta solve

 dW_eta/dt = -i G_eta(t)^dagger H(t) G_eta(t) W_eta(t),   W_eta(0)=I_DB.

This includes bath-only evolution. The exactly corrected joint propagator for initial frame F0 is

 U_corr(F0,eta)=F0^dagger W_eta F0.

Indeed the usual toggling frame F(t) removes all instantaneous pulses, and its Hamiltonian is F0^dagger G_eta^dagger H G_eta F0. No physical Paulis need commute: their anticommutation phases cancel in conjugation.

Expand the full operator W_eta in the Hermitian data-Pauli basis, with d_D=dim(D):

 W_eta = sum_P P_D tensor B_{P,eta},
 B_{P,eta} = (1/d_D) Tr_D[(P_D^dagger tensor I_B) W_eta].

Uniform F0 has orthogonal conjugation characters:

 E_F0 chi_P(F0) chi_Q(F0)=delta_PQ.

Therefore the exact averaged joint channel, for arbitrary input rho_DB, is

 E(rho_DB) = E_eta sum_P (P tensor B_{P,eta}) rho_DB (P tensor B_{P,eta})^dagger.   (1)

Thus P is a genuine positive Kraus/instrument label of the averaged channel, not a signed quasiprobability or merely a syndrome. The trajectory eta remains a Kraus multiplicity; generally there is no single bath operator B_P per Pauli. Equivalently use a Stinespring environment or a discrete Kraus compression within each P branch. Moreover

 sum_P E_eta B_{P,eta}^dagger B_{P,eta}=I_B.                                  (2)

The Pauli label is a valid CP unraveling; no claim is made that it is an already recorded experimental variable or that there is a unique physically distinguished fault mechanism.

## 3. Exact lift: commuting conjugation checks
Introduce a mathematical reference R isomorphic to D and normalized maximally entangled state

 |Phi>_DR = d_D^(-1/2) sum_x |x>_D |x>_R.

For an arbitrary pure bath/reference input |b>, form

 |w_eta,b(t)> = (W_eta,DB tensor I_R) (|Phi>_DR tensor |b>).

This is normalized. In this vectorization convention, conjugation A -> G A G^dagger is represented by

 C_G = G_D tensor G_R^*.

For a Hermitian Pauli generator P, P^*=P^T, so C_P=P_D tensor P_R^T. In particular the Y transpose sign must be retained. C_X and C_Z commute even though X and Z anticommute, because the two signs cancel. These 2m_i checks have the 4^m_i Bell-Pauli states as their joint eigenbasis on patch i. Identity/Bell is their all-plus sector.

Set |v_eta,b>=C_G_eta |w_eta,b>. Between jumps, G_eta is fixed and

 d|v>/dt=-i (H_DB tensor I_R)|v>.

At a jump P, G'=PG, hence |v'>=C_P|v>. This is exact even with noncommuting physical frames. Consequently its averaged density matrix obeys the exact finite-dimensional lifted Lindblad equation

 dot sigma = -i[H_DB tensor I_R,sigma]
             +sum_ij gamma_ij(C_Pij sigma C_Pij^dagger-sigma),                 (3)

with initial state |Phi><Phi| tensor rho_B (and arbitrary bath purification).

The final Bell-Pauli label projectors commute with every C_G, so their probabilities are identical for |v> and |w>. The dephaser is a representation of tracked control in error-amplitude space; it is not an untracked dephasing channel applied to the intended logical state.

## 4. Normalization and bath operator effects
Define |P>>=(P tensor I_R)|Phi>. These are orthonormal. The Choi/error-amplitude expansion is exactly

 |w_eta,b> = sum_P |P>> tensor B_{P,eta}|b>.

There is no dimension factor in the label probability:

 Pr(P | rho_B)=Tr_B[B_{P,eta} rho_B B_{P,eta}^dagger].

For any Pauli-label event A, its bath effect is

 E_A = sum_{P in A} E_eta B_{P,eta}^dagger B_{P,eta}.                           (4)

If the lifted endpoint theorem gives Pr(A)<=b_A for every normalized bath state, then positivity and the quadratic-form criterion give E_A<=b_A I_B. This remains uniform in bath-reference entanglement.

For an arbitrary physical input rho_DB, including pre-existing data–bath correlations, the CP label instrument in (1) has event probability

 Tr[(I_D tensor E_A)rho_DB] <= b_A.

Thus the use of a factorized mathematical Bell probe in proving (4) does not impose a physical data–bath product-state assumption.

## 5. Applying the grouped endpoint theorem
Select patches S such that **no Hamiltonian term h_a touches two selected patches**. Group all terms touching selected patch i into V_i; absorb terms touching no selected patch into H0. Then the lifted H0 commutes with all selected conjugation checks, and lifted V_i changes Bell labels only in selected group i. Terms may touch unselected data and share any bath operators. Treat those other factors as part of the unrestricted environment in the block proof.

A safe bound is J_i=sum_{a touching i} sup_t ||h_a(t)||. Lifted left multiplication has the same operator norm. Pauli components diagonal within the selected group can be absorbed into H0; all remaining off-diagonal blocks have norm <=J_i without asserting that diagonal removal preserves the total norm.

Let d_i=4^m_i be the number of Bell-error labels and gamma_i=min_j gamma_ij. Construct the d_i^2 by d_i^2 positive comparison generator M_i on density-block labels (a,b):

 - diagonal entry: -2 sum_j gamma_ij 1[character_j(a) != character_j(b)];
 - coefficient J_i for every change of the ket label a to a different label;
 - coefficient J_i for every change of the bra label b to a different label.

With 0 the identity-Pauli label, define

 q_i(T)=sum_{a!=0} [exp(T M_i)]_(a,a),(0,0),   qbar_i=min(1,q_i).

The existing grouped endpoint proof applies exactly and gives the genuine operator inequality

 sum_{P: P_i!=I for all i in S} E_eta B_{P,eta}^dagger B_{P,eta}
       <= product_{i in S} qbar_i(T) I_B.                                   (5)

For beta_i=2 gamma_i-2(d_i-2)J_i>0, a conservative closed form is

 q_i(T) <= exp[4(d_i-1)J_i^2 T/beta_i]-1.

The sharper finite-matrix majorant is preferable. In the strong-pulse regime and bounded patch size, the factor scales as O(C(m_i)J_i^2 T/gamma_i), with a quadratic short-time transient. Different Paulis on one patch are a grouped event; one must not multiply a separate small factor for every flipped X/Z character because a single Pauli Hamiltonian term may flip several characters.

If all Hamiltonian terms touch at most one patch, (5) holds for every patch subset directly, despite an arbitrarily persistent shared bath. This is a true final local-Pauli-label subset condition for the averaged joint channel.

## 6. Generic bounded-support interactions: coloring loss
If terms touch multiple patches, the direct product (5) for arbitrary S is false: a term J X_i X_j creates two nonidentity labels at order J^2 T^2, not order J^4 T^4. Full Pauli twirling removes cross-label coherence but does not change this order.

Define a conflict graph with an edge between two patches whenever a retained h_a touches both. A proper coloring with chi colors guarantees that no term touches two patches of the same color. Apply (5) separately to S intersected with each color class. Since the full event implies each color-restricted event,

 E_S <= min_c [product_{i in S_c} qbar_i] I_B.

For a uniform qbar<1, choose a largest S_c to obtain

 E_S <= qbar^(ceil(|S|/chi)) I_B <= (qbar^(1/chi))^|S| I_B.

This is an all-subset local-stochastic bound with a coloring loss. Bounded patch sizes and bounded interaction range/degree can make chi and J_i uniform; the phrase “bounded local Hamiltonian” alone is insufficient without an explicit bounded per-patch incident interaction sum and bounded conflict degree. Merging patches is another option only if it leaves groups uniformly bounded and removes cross-group terms; arbitrary overlapping interactions cannot simply be merged without checking group growth.

## 7. Private-record caveat and sharp failure example
Equation (1) coarse-grains F0. If the full seed is retained as an accessible classical output, the actual channel instead contains blocks

 |f><f|_C tensor U_corr(f,eta) rho U_corr(f,eta)^dagger.

Cross-Pauli terms do not cancel inside each f block. For one qubit, no telegraph jumps, and H=JZ, the conditioned propagator is cos(JT)I-i chi_Z(f)sin(JT)Z. Its conditioned Choi state has nonzero I/Z coherence at generic JT. The seed-labelled channel is not Pauli diagonal on each seed block. Averaging the seed gives the positive I/Z mixture, but releasing that seed later is a materially different interface.

This is not a claim that trusted classical bookkeeping itself causes physical damage. It states exactly what is traced out in the theorem and why one cannot condition a later proof on the entire seed/controller record while retaining the same twirled instrument without additional work. Direct bath access to seeds/clocks can also defeat suppression by producing frame-aware Hamiltonians, outside the fixed/exogenous-noise premise.

Without initial F0 twirling, lifted Bell probabilities can still be bounded, but they are diagonal Choi weights only; coherent cross-Pauli terms prevent automatically interpreting them as the Pauli-labelled joint channel (1).

## 8. What is and is not established
In the absence of data-coupled noise, W_eta=I_D tensor U_B; the corrected data action is exactly identity for every trajectory, not merely on average. Hence this tracked-control construction has no noise-free physical-dephasing penalty. The lifted dephasing is harmless to the intended Bell/error-identity sector.

A known nontrivial gate is covered only after explicitly constructing a tracked implementation whose ideal corrected action is that gate and whose interaction-picture noise preserves the required support/norm/independence conditions. An arbitrary continuously acting gate does not automatically satisfy them.

The theorem supplies an exact endpoint CP Pauli instrument and uniform bath effect bounds. It does not itself produce chronological microscopic fault times, justify intermediate measurements, accommodate finite-duration noisy pulses or noisy inverse-frame corrections, or prove a decoder/memory threshold. Fresh independent twirled intervals may provide an interface for a separate sequential proof, but intervening operations and controller records must be handled explicitly.

No literature novelty claim is made. This transfers the supplied proved endpoint-group majorant to a precise clean tracked-control channel using elementary vectorization and Pauli twirling.

## 9. Independent exact-matrix checks
check_bridge.py uses own NumPy/SciPy matrices only, with a one-qubit data system and two-dimensional shared bath. It compares the exact four-frame classical telegraph process with the lifted Lindblad semigroup for all bath matrix units, verifies full joint data–bath twirling on an entangled input, and checks the grouped effect bound.

Results in exact_matrix_check.json:
- Endpoint-effect agreement: maximum discrepancy 6.12e-16.
- Twirled joint-channel versus Pauli-labelled Kraus channel: norm discrepancy 1.78e-16.
- Bath Kraus completeness: discrepancy 9.94e-18.
- Lifted generators commute exactly.
- Worst bath error effect eigenvalue 0.0120517; grouped majorant 0.1214593.

These checks support algebra/normalization only; the analytic proof, rather than finite testing, establishes the uniform statement. No Willow arrays or other experimental data were accessed in this task.

## 10. Sharper optional factor: union of detecting generators
The full grouped matrix is sufficient, but full Pauli labels admit a useful stronger elementary alternative. Every nonidentity patch Pauli anticommutes with at least one of the 2m_i generating X/Z Paulis. For each selected patch choose one such generator j_i as a witness. The event “all selected patch labels nonidentity” is contained in the union, over witness choices, of events “all chosen lifted binary characters are negative.”

For a fixed witness choice, decompose the whole incident V_i by the chosen lifted involution C_i:

 V_i^-=(V_i-C_i V_i C_i)/2,   V_i^+=(V_i+C_i V_i C_i)/2.

Then ||V_i^-||<=J_i; V_i^- flips only the selected witness on patch i, and V_i^+ preserves every selected witness and can enter H0. All other lifted pulse clocks commute with the selected witnesses. Condition on those clocks and remove their jumps by their own toggling frame: this conjugates H0 and V_i^- without changing their parity signatures or norm bounds and leaves the selected clocks independent. The single-parity subset theorem therefore applies for every fixed witness choice, uniformly in the conditioned paths.

Let

 B(J,gamma,T) = {exp(-gamma T)[cosh(kappa T)+(gamma/kappa)sinh(kappa T)]-1}/2,
 kappa=sqrt(gamma^2+4J^2).

Positive operator effects obey the same union bound as probabilities. Summing the product witness bounds factorizes, giving (5) with the alternative factor

 q_i^witness = min(1, sum_{j=1}^{2m_i} B(J_i,gamma_ij,T)).

The cap follows by dropping patches whose uncapped factor exceeds one and applying the same argument to the retained subset. For a common minimum rate gamma_i, a sufficient factor is min(1,2m_i B(J_i,gamma_i,T)); monotonicity in gamma follows directly from the positive paired-gap integral representation. Per-patch minima require a hybrid proof, rather than merely taking the minimum of two product bounds. Choose in advance, independently of outcomes, which selected patches retain their full Bell-label groups and which use a single detecting witness; split V_i into odd/even parts only on witness patches, so the resulting H0 preserves every retained full group and witness check, and condition only the omitted commuting clocks. The positive block comparison remains a Kronecker sum of full-group matrices and binary witness matrices, giving the product of grouped factors and chosen-witness B factors; union only over the witness choices then gives the corresponding product of grouped factors and witness sums. Choosing the better proved factor on each patch therefore justifies the product of per-patch minima under the same no-term-touches-two-selected-patches hypothesis; caps at one follow by dropping those patches as before.

This replaces the exponential-in-patch-size group constant by a conservative linear factor 2m_i for full Pauli labels; it is still only an endpoint theorem. In the one-qubit numerical example, the witness sum is 0.0671030, smaller than the grouped 0.1214593 and still above the exact worst-bath endpoint probability 0.0120517. The same coloring argument applies with this improved per-patch factor.
