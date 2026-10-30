# Independent audit of root's continuous-noise initializer handoff
2026-10-30. Source: producer-workspace/LOCAL_STOCHASTIC_HANDOFF.md. Read against producer-workspace/basin_review.md and the reviewed raw/F comparisons.

## Verdict
**Scoped PASS for the handoff argument, conditional on the stated Tanner linear-cutoff version of the accepted continuous-noise simple-compiler drift/killed theorem.** The initializer proof does not itself establish that compiler's Tanner substitution; it uses that as its declared underlying memory theorem. It correctly upgrades a physical LS-support initializer, including coherent conditional faults and retained environment, without a physical ideal cleanup.

It does NOT permit replacing the LS-support contract by a final recovered logical score. The physical initial output must actually be representable as a support-indexed CPTP error on Enc(rho) tensor ready auxiliaries, with a support distribution independent of the logical input. The word 'decoded' in the first sentence should be read in this strong physical sense, not as permission to assume only correct ideal-decoder statistics.

## 1. Initial moment is correct without Pauli probabilities
For a fixed physical support E, all dressed DATA-Pauli/controller matrix terms acting on the encoded/ready vacuum lie in joint syndrome/flag sectors with occupied vertices contained in Gamma(E). The raw animal operator is diagonal in those labels, so its restriction to that entire coherent span is bounded by the largest allowed occupancy weight. Arbitrary off-diagonal amplitudes between such sectors cannot violate this operator bound.

For S subset A, assign each hit vertex to one incident fault site. There are at most b^{|S|} assignments; each assignment requires at least ceil(|S|/k) distinct faults. Thus LS gives Pr[S subset Gamma(E)]<=b^{|S|}p^{|S|/k}. Expanding the positive product then gives exactly

    E f_A <= [exp(a)(theta+b(1-theta)p^{1/k})]^{|A|}.

If the product with the rooted-animal counting base is strictly below one, the sums for both V_+ and W_+ converge to O(N). The accepted global F<=V_+ transfers the initial moment. Neither independence nor a fictitious Pauli mixture was used.

## 2. The linear-distance total-support cap gives a common logical span
On |E|<=alpha N, the finite-depth frame enlarges DATA support to at most s_f alpha N. Each CSS-sector minimum representative has no larger weight. For each Pauli term, its difference from that representative has zero syndrome and weight <=2s_f alpha N<d. It is therefore a stabilizer. The sectorwise reduced representatives also have total weight below ell, so every component is safe.

This is a coefficientwise common-correctable-span assertion. After the canonical gauge, the full support-conditioned CP map factors as id_L tensor an ancillary map, including retained bath and controller coefficients. Summing the good support ensemble retains this factorization. A support-sampling law independent of the logical input ensures a genuine fixed initialized channel.

The LS binomial union bound makes the discarded large-support mass exp(-cN) at small fixed p. This argument genuinely relies on ell=Theta(N). It would not handle positive-density LS faults with ell=Theta(sqrt(N)).

## 3. Initial gentle compression and the killed process compose
On the good support ensemble component safety is already exact. Therefore outside the accepted basin P, the raw V_0 threshold must be at least M. Since F>=V_0 and the good ensemble is subnormalized,

    Tr[(I-P) rho_good] <= Tr[F rho_good]/M <= C N/M.

The gentle projection inequality for subnormalized states gives

    ||rho_good-P rho_good P||_1 <= 2 sqrt(C N/M).

The estimate is stable under a reference, and P acts as I_L on the canonical logical factor, so the compressed initialization retains logical/ancillary factorization. The accepted proof has [P,F]=0, hence projection does not increase the F moment: Tr[F P rho_good P]<=Tr[F rho_good]. The killed drift therefore starts with O(N) moment exactly as needed.

One need not renormalize the compressed state. Its scalar mass may be below one, and the later killed map is still a_t id_L with 0<=a_t<=1. The full-versus-killed Duhamel comparison and trace preservation charge that mass loss along with the initial support failure and gentle-compression error. Adding the terms yields

    C N^{3/2}(1+t) exp(-c' N)

after reducing the positive exponent and changing constants. No bath reset, postselection on a rare quantum outcome, or physical syndrome measurement is inserted.

## 4. Retain these scope qualifications
- The initial joint environment must arise from a fixed logical-independent pre-preparation state and the declared local-support error channel. An arbitrary logical-dependent initial bath is not covered.
- If a source theorem proves LS only on a subnormalized successful factory event, add its bad-event CP norm separately and use the unnormalized moments. There is no need to divide by its success probability.
- An additional 'preparation error' term is valid only as an actual state/channel trace/diamond approximation to this physical initializer contract. A score after a different ideal recovery is not sufficient.
- Bounded locality/incidence of the full preparation-to-gauge footprint, including flag and unary-energy vertices, is essential. It is part of the stated k,b,s_f constants, not automatic for a global Pauli feedforward computation.
- All native/simple-controller scope distinctions survive: this is a handoff into the assumed accepted simple compiler, not a new two-site continuously coherent noisy-controller realization.

No source file was modified by this audit.
