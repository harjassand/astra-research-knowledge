# Exact annealed hole identity with explicit beta-v activity

2026-11-02. **Proved for the commuting stabilizer reference (and independent onsite bounded-dimensional bath). Not yet a native-clock perturbation theorem.**

## 1. Reference and local source labels

Let H0=sum_a epsilon_a q_a, q_a=(I-S_a)/2, epsilon_a>=0, with commuting stabilizer generators. Shift the vacuum energy to zero. Their actual valid syndrome set S is a binary linear subspace; every valid sector has the same dimension. Let V_lambda be bounded local insertion labels, with v_lambda=||V_lambda||. Hermitian total perturbations may use non-Hermitian individual labels.

For a connected used-label set A, let C_A include every check that fails to commute with at least one label in A. Including all meeting checks is allowed. Then |C_A|<=b_c |A| for a bounded local dictionary. Write

  H_C=sum_{a in C_A} epsilon_a q_a >=0,
  H_out=H0-H_C.

H_out commutes with every source insertion in A and with H_C.

## 2. Exact local Boltzmann replacement

For a chronological word lambda_1,...,lambda_k drawn from A with time gaps t_j>=0, sum t_j=beta,

  e^{-t0 H0} V_lambda1 e^{-t1 H0} ... V_lambdak e^{-tk H0}
    = e^{-beta H_out} O_word,

where

  O_word=e^{-t0 H_C} V_lambda1 e^{-t1 H_C} ... V_lambdak e^{-tk H_C}.

This is an exact identity; H_out is moved through every insertion using its commutation, not by an approximation. Since H_C>=0,

  ||O_word|| <= product_j v_lambdaj.

The operator is supported on the physical union of source supports and the affected check supports. That union has O(|A|) sites at bounded degree/weight. No large stabilizer filling is needed to define this replacement operator.

Sum over positive repetition counts of every distinct label, all chronological orders, and their ordered time integrals. The time-simplex/count identity gives

  ||O_A|| <= product_{lambda in A}(exp(beta v_lambda)-1).        (H1)

All internal signs are retained in O_A. There is no local dimension factor, beta-energy growth, or ground-state projection in (H1).

## 3. Exact hole partition bound for actual syndrome constraints

Let z_a=exp(-beta epsilon_a) in [0,1] and

  Xi(z)=sum_{s in S} product_a z_a^(s_a).

Releasing the penalties in C means replacing z_a by 1 there. Then

  Xi(z with z_C=1)/Xi(z) <= product_{a in C} 2/(1+z_a) <=2^|C|.  (H2)

Proof: character orthogonality gives the exact binary-code Walsh transform

  Xi(z)= [1/|S^perp|] product_a(1+z_a)
          sum_{u in S^perp} product_{a:u_a=1}[(1-z_a)/(1+z_a)].

Every summand is nonnegative. Releasing C sets its transformed parameters to zero, so the dual sum can only decrease, while the prefactor changes by the product displayed in (H2). Constants and equal syndrome-sector dimensions cancel. Dependencies among stabilizer checks are fully retained.

Consequently

  |Tr(e^{-beta H_out} O_A)|/Z0
       <= 2^|C_A| product_{lambda in A}(exp(beta v_lambda)-1).   (H3)

This is an annealed full-trace bound: initial syndrome is summed, not fixed.

## 4. Several compatible used-label components

Assume distinct source components have disjoint actual insertion supports and disjoint marked affected-check sets; this is the conservative source-overlap convention used in the existing construction. Every insertion in one source commutes with the affected checks and insertions of another. Thus its time-ordered word can be grouped exactly, and

  coefficient = Tr[e^{-beta H_out(union C_i)} product_i O_Ai].

Applying (H1)-(H2) gives

  |coefficient|/Z0 <= product_i [2^|C_Ai| product_{lambda in Ai}(exp(beta v_lambda)-1)].

In particular, for v_lambda<=v,

  q_hole = 2^b_c [exp(beta v)-1]

is an explicit dimensionless activity per distinct label. Pauli/matrix dictionary l1 overhead belongs inside v, not hidden in a claim about physical perturbation strength.

This bound is not product **equality** and does not make the normalized source gas independent. Remote denominator cancellation remains to be proved.

## 5. Independent onsite bath extension

If H_B=sum_j h_j is onsite, shift each h_j so its minimum is zero. Include every acted-on bath site in the local hole. Its local heat kernels are contractions, and removing h_j changes its partition factor by

  dim(B_j)/Tr(exp(-beta h_j)) <= dim(B_j).

Thus for dimensions <=d_B and at most b_B bath sites per label,

  q_hole = 2^b_c d_B^b_B [exp(beta v)-1].

Arbitrary source operators on those bath sites are allowed. An interacting bath cannot be locally removed this way without an additional boundary estimate; global thermal Hölder remains valid but does not produce this exact local replacement identity.

## 6. Why this does not complete connected normalization

Uniform bounded moments do not imply volume-uniform logarithmic analyticity: perfectly correlated bounded variables have partition zeros approaching zero with volume. Here reference constraints and source closure must supply locality.

Nor can released-check holes be treated as independent polymers. For an even-parity syndrome space, at zero temperature releasing k>=1 checks gives 2^(k-1) allowed zero-cost patterns. Two distant holes therefore do not factor even though a single released check adds no state. Actual local Pauli histories obey stronger orbit/closure constraints and those labels must be retained.

Finally, reducing a small closed Pauli word to a stabilizer character may require m^p filling checks. A naive signed-gas pin estimate then charges O(p_defect m^p), which cannot be paid by a linear O(m) source charge. In the independent-defect example, the exact character mean is (1-2p_defect)^(m^p)<=1 while the absolute cluster estimate grows exp(O(p_defect m^p)). Exact positivity/annealed cancellation, not a blanket polynomial-count claim, is needed.

## 7. Native transfer boundary

The raw native clock Hamiltonian is not a positive commuting check sum. Removing its local terms can lose a large self-pressure and does not establish (H1)-(H3) with J replaced by an induced check energy. The proved dynamic-flux rod lemma provides a plausible replacement: resum winding singletons into positive defect-time penalties, retain endpoint and connected clock corrections, then construct the analogue of these local replacements. Arbitrary clock matrix pins and preservation of positivity under this resummation remain unproved. No native imperfection window is claimed from this identity alone.
