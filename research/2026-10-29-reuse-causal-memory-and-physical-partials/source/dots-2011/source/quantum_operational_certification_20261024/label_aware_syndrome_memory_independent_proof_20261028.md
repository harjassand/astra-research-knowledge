# Independent proof and finite-resource audit: label-aware syndrome memory acquisition

28 October 2026. This reviews the new manuscript's two DISTINCT constructions, not a claim that arbitrary correctable noise admits the exploration operation. All conclusions below require its exposed pre-noise port, fixed V, and declared classical-X-pattern/quantum-memory source form. Its qualitative CP inequalities are trusted promises, not learned model tests.

## 1. Complete maps, not only marginal probabilities

The four representatives E form a transversal of the quotient of three-bit strings by the subgroup `{000,111}`. For every fixed physical error f, translation by f permutes its four cosets. Therefore each target gauge g has exactly one injection label e whose translated pattern is either e_g or e_g XOR111. Summing that identity with ANY CP maps F_f gives `A_I,g+A_X,g=T/4`; no iid or positivity-of-contrast premise is needed for this sum.

For each e,f the physical map on an encoded basis vector has the same logical-X branch on both logical basis values and has no phase. It consequently proves the stated injected majority-subsystem identity on ALL four logical matrix units and all incoming memory matrix units. The mixed logical input then gives `I8/8 tensor T(omega)` including retained memory, and linearity extends the equality to an arbitrary external memory reference. Individual readout-conditioned memory branches are not equal to T(omega); the manuscript correctly does not claim this.

In Part A, insert the conditional iid coefficients into A_I,g−A_X,g. The coefficients become `t(3−t²)/8` for g=0 and `t(1+t²)/8` for the three other gauges. For t in [0,1] both are nonnegative, with the latter never larger than the former. Nonnegative combinations of the K_a are CP, regardless of noncommuting/coherence-preserving Kraus operators. For the traced current memory state, the same three gauges minimize at every history, so averaging a finite bank commutes with taking this particular minimum gap: it is precisely average c/16. This is stronger than merely asserting a flat output marginal. It does not assert that future excitation episodes arrive within any finite cap.

Future uninjected majority blocks are F_(e_g) and F_(e_g XOR111). Their CP differences are nonnegative in the equal-rate mixture subclass, because each weight-at-most-one pattern is at least as probable as its complementary weight-at-least-two pattern for p<=1/2. Outside that subclass, the exact majority extraction remains a specified decoder, not automatically a full-CPTP oracle.

## 2. Why the retained injection labels legitimately identify coordinates

For the Z preparation branch, the pair of independent uniform labels (logical bit l, injection e) parametrizes all eight computational strings bijectively. Multiplication by the known sign `(-1)^(l+e_i)` is just the i-th coordinate Fourier coefficient of the physically prepared string. For each error f, change variables from x to y=x XOR f in this finite sum. It gives `Z_i/8 tensor (-1)^f_i F_f(omega)`, hence after summation and V conjugation the complete signed operator is `C_i/8 tensor H_i(omega)`.

For the X preparation branch, averaging the four injected encoded X operators gives X1 X2 X3/8. Every physical X_f commutes with that operator. Its complete signed output is therefore `C_X/8 tensor T(omega)`. These are identities on all memory operators before tracing memory, not inferences from scalar conditional moments.

Each asserted conditional expectation averages the fresh injection, axis, sign and readout labels given the COMPLETE PRIOR record. Retaining the current e in a known multiplier inside the random statistic does not condition the asserted expectation on e and does not give it to the source in advance. A source allowed to choose F_f from that current private label would invalidate this derivation; that dependence is expressly excluded. Readout backaction and arbitrary exposed-past adaptation remain compatible because the derivation holds separately at each actual prior conditional memory state.

Under Part B's H_i>=_CP0 and T−H_i>=_CP0, every normalized current memory state has theta_i in [0,1]. A bank's contrast is the fixed C_i times the nonnegative predictable scalar average theta_i/8. An informative bank therefore identifies the SAME C_i even if different coordinates become informative in different stages. No nonnegative majority-sector contrast is needed. The complete X contrast is always present. In Part A the coordinate gap t/8, averaged over the instrument, lies between the majority minimum gap and twice that gap, but this does not compare entire four-fit and two-fit sample budgets.

## 3. Four correlated empirical matrices: explicit concentration constants

For a single measured qubit the product-shadow second-moment map is `rho -> rho+2 Tr(rho) I`. Its threefold tensor product, evaluated on any three-qubit density operator, is a sum over reduced density operators with nonnegative coefficients and is bounded above by `3³ I`. Each importance-weighted record in (8) is twice a sign times the shadow on one of two equally likely input axes. Thus

    E[Y_v² | past] <= 2*27 I,
    ||Y_v-E[Y_v|past]|| <= 2d+1/8 <= 4d, d=8.

The centered conditional variance is no larger than the displayed second moment. The received matrix martingale bound applied to a bank of N_s samples gives tail at most

    2d exp(-N_s a_s² / (2(54+32 a_s/3))).

Since a_s<=1/128 and N_s a_s²=216 L, the exponent magnitude is at least `(1296/649)L > L`. Consequently the tail is at most `2d*2^(-L)`. The union over FOUR matrices and S+1 possible stages is at most `8d(S+1)2^(-L)<=beta` with exactly the manuscript's L. Neither independence among those four matrices nor independence of successive source outputs was used. Fixed stage budgets and a finite union also cover stopped/unreached later stages; conditioning on a favorable future excitation event is unnecessary and would not be justified.

The received finite rational Jacobi primitive contributes at most a_s/4 Frobenius, hence operator, error. On the simultaneous confidence event the total perturbation is e_s=5a_s/4. The rational guard and previously received opposite-sector sign inequality therefore imply the claimed component norm error c=b/8. Every retained reflection is exactly physical even on a bad record. A permanent certificate needs fixed V, not persistent training occupation after retention.

The first stage meeting a_s<=c gamma/5 has `a_s>b gamma/80`, unless it is stage zero; the displayed loose bound covers that case too. Therefore `N_s<51200*27*L/(b² gamma²)` and the accumulated geometric bill is strictly less than 4N_s/3. Setting gamma=theta/8 gives the stated sufficient threshold b theta/320. This checks the tighter component-accuracy payment; no free replacement of c by b was made. The exact worst-case cap is its stated integer geometric sum. Persistent biases or itemwise informative reached stages establish only their explicitly funded completion claims.

## 4. Majority assembly without a commuting fit

The TRUE C_i commute, so the true sum T is unitarily equivalent to Z1+Z2+Z3, with minimum absolute eigenvalue one. Its sign is `(C_1+C_2+C_3−C_1 C_2 C_3)/2`, the exact majority reflection. This polynomial is used ONLY to identify the true target. The construction does not evaluate it on the generally noncommuting learned reflections.

Instead, the sum of the three fitted reflections differs from T by at most 3c. A further finite rational Jacobi approximation within b/8 gives total perturbation at most b/2. The estimated matrix has gap at least 1−b/2. Applying the same sign lemma with the TRUE gap one and this estimated gap gives

    ||S_Z−B_Z|| <= 2(b/2)/(1+(1−b/2))
                 = b/(2−b/2) < b.

This is the valid sharper denominator; it is not an assumption that fitted coordinates commute. The independently fitted S_X has error at most c. Both final controls are exact reflections, so their three-controlled-gate circuit is a literal unitary followed by the declared discards, hence CPTP on every accepted record. The previously received complete-reference extraction inequality then gives uniform clean loss at most `(9/2)b²<=epsilon/4` for every emitted gauge state and coherent reference/memory. The exact mathematical fixture also supplies noncommuting rational component reflections for which a finite certified diagonal truncation produces a physical majority reflection, and checks the actual three-gate SWAP matrix.

Uniformity is what permits later gauge occupation or memory changes under the same U. For one service the parent accepted-risk argument pays bad-record probability, calibration discrepancy and actual-memory service implementation error. The oracle wording needs separate future dominance. Further adaptive reuse needs the distinct received complete-CP-domination contract: privately retired fresh frame keys, discarded gauge/receiver records, common controller and complete whole-horizon implementation budget. Neither a collective optimum nor an ideal-computation comparison follows here.

## 5. Wider class, necessary failures, and actual evidence

Part B genuinely reaches sources outside the earlier majority-contrast class. For example, ordinary independent unequal flips `(1/4,1/4,1/100)` have positive coordinate biases but a native majority sector of signed weight −9/160; majority Bell loss is 53/800 whereas the optimal syndrome decision gives 1/100. The author's separate `(49/100,49/100,0)` example has positive coordinate biases and an INJECTED majority sector −2399/20000. Thus the new coordinate construction is not merely the old raw-majority-sign theorem with relabeled margins. The preserved deterministic-X1 failure is outside Part B's coordinate-positivity promise and prevents extending the claim to arbitrary native-correctable channels.

The independent script uses a different rational entangling mixer and a noncommuting two-Kraus retained-memory instrument. It checks both a mixture-of-iid source and a genuinely correlated physical-pattern instrument, the latter with positive coordinate biases but without majority dominance. It independently verifies 8,192 complete logical/memory channel entries and 6,144 signed-memory entries. A separate full enumeration of 3,456 actual injection, logical-probe and product-Pauli readout events retains the 2-by-2 conditional MEMORY instrument, including off-diagonal entries, and reproduces all five expected matrices (unsigned plus four signed records). It also checks a noncommuting-fit physical rounding fixture, 256 literal coherent-extraction entries, and nine exact finite-budget/guard cases. All arithmetic is exact rational/Gaussian rational. There are zero source outcomes and zero RNG draws; this is not a sampled acquisition run or a general finite-Jacobi/elementary-gate compiler execution.

For every calibration block the new physical costs remain two fair injection bits and at most one X gate in addition to known encoding, resets, ordinary logical probes and three physical output measurements. Four correlated matrix records are classical reuse of one measured block, not extra copies. Finite samplers, stored matrices, rational arithmetic, control compilation, routing and complete implementation errors remain separately paid. The strongest conventional learner has the identical port, retained labels and structural information and can use this same procedure. No performance advantage over that comparator is received.
