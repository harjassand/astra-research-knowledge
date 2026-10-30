# Independent positive-source / coherent ATG audit
2026-10-30. Scope: the named frozen inputs in INPUT_SHA256.txt, including the counting addendum. Verdict: **PASS as a conditional scheduled-source receiving theorem, with the precise interpretation below.** This is not an autonomous factory, record-memory, or universal-threshold certificate.

## Findings and repairs
The reviewer identified two real counting errors in the initially presented ATG text: (i) excluding *all* size-at-least-T bulk connected sets requires O(nT) potential roots, not O(n); (ii) rooted-union counting requires every component to contain one of the selected roots, not merely some boundary vertex. The author repaired both in the frozen coherent-source manuscript ce2ac017dc0858c26d0fa7ef6006ac5925b4e1813b5c88bee66b72a39d2ae966. The frozen older deterministic certificate must be read WITH COUNTING_PRECISION_ADDENDUM.md. Its broader unamended witness (c) is deterministically sufficient but does not have the claimed rarity bound.

The final source also explicitly uses covering-support terminal tests and pays bounded baseline-bit duplication kappa<=2. Those are necessary for the stated hereditary predicate and the T=1 case. Interpret “correctable radius” with 2(t+t_B)<d (or the stricter radius required by the receiving memory), not merely with arbitrary positive linear fractions.

## 1. Joint HP relative estimate: direct proof
There is a simpler proof than the manuscript's unspecified finite-system-leg expansion. A local adjoint term is a normal HP map N_e^* on H_e tensor H_bath, tensored with the identity superoperator on the complementary system sites. This tensor-locality is the meaning of “system support e”; a merely small total norm is not sufficient.

For a term already centered so N_e^*(I)=0, write F_S=A tensor B where A=exp(theta sum_{i in S intersect e} B_i), B is the complementary positive factor, and identities on bath/reference are implicit. Put r=|S intersect e|. Then

  ||A^(-1/2) N_e^*(A) A^(-1/2)|| <= ||N_e^*||_cb exp(r theta),

because ||A||<=exp(r theta), ||A^(-1/2)||<=1. HP makes this a self-adjoint relative operator, so

  N_e^*(F_S) <= exp(r theta)||N_e^*||_cb F_S.

The untouched B factor cancels exactly in relative congruence. This proof is independent of bath size and remains valid after arbitrary reference amplification. Thus C=1,a=q' suffices for already centered terms; conservative constants in the source are valid. No positivity of each signed term is used.

Center a noncentered HP local term by subtracting {N_e^*(I),O}/2. This preserves support and HP, costs at most a factor two in cb norm, and sums to no change when the perturbation's total adjoint annihilates I. Bath-only trace-preserving dynamics annihilate F_S and may be separated. This centering must be performed on a well-defined summable decomposition; it cannot rescue a model lacking joint bounded local generators or a valid positive total evolution.

After centering, terms missing S vanish exactly. The sum of norms of terms meeting S is at most eta'|S| by per-site incidence, with overcounting harmless. Hence the global number of source sites never enters the differential inequality. Physical scheduled-gate noise pulls back to such terms: if the backward cone of each site has size at most K, a physical q-body term has pulled-back support <=qK, and terms hitting a specified pulled-back site originally hit its forward cone of size <=K. Thus incident strength is at most K eta before centering. Fixed depth and disjoint bounded-size layer gates supply fixed K, including partial non-Clifford gates during a layer. No constant is independent of growing depth/check degree.

## 2. Subset bound and actual reset warm start
For a positive joint state, the operator inequality gives x_S'<=C eta' exp(a theta)|S| x_S. Starting with exact pure product system gives x_S(0)=1 even for an arbitrary bath. Markov on the commuting spectral projectors gives

  Pr[S contained in defect support] <= exp[(-theta+C eta' tau exp(a theta))|S|].

The stationary choice exp(a theta)=1/(a C eta' tau) is admissible when a C eta' tau<1, and substitution gives p=(e a C eta' tau)^(1/a). For a useful p<1 choose the stronger a C eta' tau<1/e; otherwise the bound is valid but trivial. No global fault-path triangle expansion occurs.

For actual replacement resets R_i(rho)=|p_i><p_i| tensor Tr_i rho, the adjoint identity in the manuscript is exact, also on entangled system-bath states. With F=F_S, spectral Jensen for convex z log z yields Tr(rho F log F)>=x log x. Therefore

  (log x)' <= -[kappa(1-exp(-theta))/theta] log x + C eta' exp(a theta)|S|.

The manuscript's beta is a valid upper bound (the exact forcing integral includes a further factor 1-exp(-k t_R)<=1). To obtain any desired sufficiently small constant local-stochastic parameter, first fix a sufficiently large theta, next choose eta'/kappa and eta'tau small enough, then choose finite t_R large enough. These choices are independent of source volume. This is a real warm-input route only when the replacement reset reservoirs and generator are actually part of the physical model; it is not a noisy-clock or legal hardware-initialization compiler.

## 3. Fixed depth, dictionary, and common record span
The graph's bounded degree permits at most 2Delta-1 edge-color CZ layers, then one H layer and one disjoint graph-to-pointer CNOT layer. The depth bound is genuine for the declared circuit; O(nT) spatial size does not enlarge it. No decoding or pointer-retention delay is included in this depth.

Independently expanding a graph-state amplitude gives, in pointer branch m, the boundary vector Z^(a_boundary) psi_(m xor a_bulk xor c), while the measured-graph gauge register carries m xor c. The latter register depends on the defect basis vector and must NOT be erased from a coherent argument. Allowing arbitrary gauge/bath coefficients makes this dependence harmless. Each effective fault-cover vertex has at most two distinct input bits, so a union over choices gives Q<=2q for every prescribed vertex subset, including mixtures of boundary and bulk vertices.

Fix beta solely from the metasyndrome, including its tie rule. With a complete independent Bell-stabilizer sign vector L, corrected signs are L(f+beta(Mf)), independent of the allowed record m. A complete pure stabilizer group fixes a ray; arbitrary phases and branch amplitudes do not invalidate a common span. The boundary frame P(m) may have extensive weight and is used only as an analysis frame. It is not a completed physical correction.

The deterministic cluster argument is sound with the corrected rooted witnesses. Componentwise replacement bounds inferred mismatch weight by true-fault weight. Nonbridging completed components admit a syndrome-equivalent boundary repair; equality of syndromes alone does NOT imply stabilizer equivalence. Collapsing each component yields a zero-syndrome base-code operator, and its weight <d excludes logical action. The separate rooted-union event is needed to bound total repair density; small component size alone would not do so. Quarter occupancy gives a geometric weight per completed witness, and selected-root counting yields the displayed density tail. Taking d,T linear in n and sufficiently small fixed Q makes all polynomial-volume times geometric tails exponential in n.

The relevant primary equations and clustering comparisons were checked directly against [Bergamaschi–Liu, arXiv:2411.04405v1, sections 4–5](https://arxiv.org/html/2411.04405v1). This review uses their deterministic comparisons, not a substitution of signed noise into a stochastic theorem.

## 4. Positive projection, retained bath, and baseline
The bad-support union bound applies to the actual positive diagonal distribution in the input-defect basis. It is not a noise unraveling and does not discard off-diagonal terms. Projecting onto the good basis subspace costs at most 2 sqrt(delta) in joint trace norm. Linearity then puts the entire projected state, including coherences between different good patterns, in the record-controlled direct sum of radius-(t+t_B) Pauli spans, with measured graph and bath retained. The same later CPTP map contracts the comparison. Uniformity over arbitrary reference states supports a complete source-map estimate; it does not by itself supply an arbitrary-input computation or receiver.

In one fixed actual record, b(m)+sigma(P(m)) is one fixed string. The boundary-sign identity gives D(m)=sigma(Rep(f))+b(f); E_B cancels because it appears on both sides. Hence every nonzero good component in that record shares |D|<=nu t+u. The terminal-event bound uses the covering support and pays any duplication of record bits in b. This proves the incoming module and sparse fixed target discrepancy, not physical capture, retention, or programming of that baseline.

## 5. Checks and exclusions
`check_independent.py/json` independently checks 240 centered signed HP examples with retained bath, reset identity/Jensen, and an exact small ATG's common corrected ray in all 128 supported defect-record combinations (including invalid raw records corrected by the fixed metasyndrome decoder). It derives the finite metacheck from ideal amplitudes rather than importing it. `dictionary_replay.json` replays the author's 65,536 exact dictionary branches. These are falsification checks, not substitutes for the uniform proofs or asymptotic distance argument.

Not supplied: autonomous scheduling or termination, trustworthy classical capture/storage, noisy dense final feedforward, arbitrary unknown-state encoding, physical acceptance, a full fixed-baseline memory proof, or universal computation. Decoder runtime may be large and needs separately earned storage. The final Bell-to-known-state conversion requires its actual noisy readout/feedforward interface. The audit closes the coherent scheduled-source mathematical seam only under the stated local-generator/reset and deterministic-decoder interfaces.
