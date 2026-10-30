# Whole receiving proof: protected classical record to distributed native Pauli
30 October 2026. Construction completion of ROOT_DISTRIBUTED_PAULI_FEEDFORWARD.md. Independent review required. This note is binding where it makes the root candidate's open obligations precise.

## 0. Earned resources and source domain
Use the accepted finite bounded CP/TNI cavity extension (ROOT_TNI_CAVITY_RECEIVING.md with its review and TRACE_FACTOR_COMPLETION), exact-target finite gate/reset receiving, disjoint ABO polynomial-qudit computation-code rectangles, and actual top-down output decoder with the polynomial-qudit-to-qubit port. Use the SAME native hardware, canonical forest, global energy cut, singleton BUSY witness and live-prefix receiving constants as the accepted selectable-pulse/register work. These are supplied resources, not new hardware realizations. In particular local weak terms have at most q physical system legs, bounded incident complete norm eta, arbitrary retained finite bath, and the total interval dynamics is CP-divisible. Reset reservoirs already excluded from that bath stay excluded.

The input algebra is a CLASSICAL direct sum over z of a native logical matrix algebra L and an admitted auxiliary space A_z. A branch source embedding J_z is the supplied common native KL/error-module chart together with the protected computation-code sparse module for the classical word z. It accepts product logical/auxiliary inputs and their complete reference extensions; positive input auxiliaries may differ with z. It must not be a state-dependent assignment carrying unspecified unknown L information in the auxiliary. Equivalently, the theorem is uniform on the stated algebra, not on all physically correlated initial states. Approximate instrument ingress costs epsilon_in in complete norm. The accepted destructive measurement instrument may supply classicality and outcome-conditioned auxiliaries, but does NOT alone prove this remaining-bank source chart: a caller must supply that chart. No coherent quantum-program conclusion is asserted.

The source chart is a genuine linear channel domain, not a nonlinear moment cone. More precisely J_z is a fixed CPTP embedding/preparation channel from L tensor A_z into the physical admitted module, uniform over reference extensions, with

 J_z^*(P_native)=I,
 J_z^*(F_native tensor I_proc,bath)<=exp(w_E0 N) I,
 J_z^*(G_BUSY tensor I_proc,bath)<=exp(w_B0 N) I.        (H0)

The constants are uniform in z and N. Here P_native is the actual native basin cut and both witnesses are in their received SAME physical chart; when a witness acts also on apparatus its full operator is used. The chart restricts the native canonical radius to its received initial margin. Impose a strict barrier gap

 max(w_E0,nu_E)+q_t < s' e_cut-gamma_0, gamma_0>0,

and the other radius/boundary margins of the native cut theorem. A fixed auxiliary preparation channel with these operator inequalities is an equivalent allowed input. They hold on the ENTIRE auxiliary input space declared for the theorem, not just one state correlated with L. Thus every maximally mixed logical probe in H8 and arbitrary positive auxiliary/reference test satisfies the same envelopes. A family of warm states lacking such a common preparation/domain is explicitly outside the channel/diamond claim. The original native theorem's constants and boundary estimate, including its code-radius boundary, remain required; H0 does not replace them.

Fix explicit physical Pauli representative matrices. The Boolean functions c_i^X(z),c_i^Z(z) are computed by an actual bounded-fanout reversible circuit over the received gate library. The convention fixes the X/Z layer ordering. Its physical product P(z) normalizes the zero-reference code and induces P_L(z). All 2N command outputs are independently encoded computation blocks; the original record is retained protected if wanted. No unencoded master bit is copied to many DATA sites.

## 1. One chronological circuit, including the waiting bank
The schedule consists of:
W: Native correction ON, ordinary protected command computation, then all output-decoder stages above the terminal physical stage. Output blocks are distinct after the command circuit; their shrinking cones have no inter-output gates. All idles, preparations, routing and finite resets count. Pad cones so every command reaches its level-one block at the same fixed time. Allow a fixed additional native relaxation interval while those blocks are protected by scheduled identity rectangles (these rectangles belong to the associated decoder cone).
F: Native nominal generators ALL OFF. Run the terminal physical recovery/inverse encoder, actual finite reset/port, and two controlled-Pauli layers, with all cones padded to a common fixed duration tau_F. Every native resource (DATA plus tags/monitor as ONE site), private hub, processor wire and remaining live ancilla either belongs to an active gate block or an explicit idle location. There are no other nominal interactions with an active block. Duration, block size and number of terminal locations per region are constants independent of N. All command physical bits are produced only inside F, not stored naked throughout W.
C: All nominal command–DATA couplings OFF. Resume the SAME native correction, without resetting DATA, tags, hubs, or histories; residual weak couplings still satisfy eta. Optional fixed cooldown returns to the original receiving thresholds.

For synchronization, an output's protected identity padding can be included in its last higher-level stage only if its number of padding rectangles is bounded by the stated stage-size constant. Choose parallel identical shrinking schedules, with only a fixed cooldown added at the base-code protected boundary. The actual finite number of base-level identity locations for that fixed cooldown is a (possibly huge) constant absorbed in B. Do not place a polynomial waiting time at level one and retain the old O(x0) bound.

### 1.1 Time-dependent active-location cavity lemma
Refine time into fixed layers whose active gate blocks are disjoint. During W only processor blocks are active; native dynamics is the complement. During F native idle/gate blocks are also active. The Hilbert space itself never changes: a site moves between the active list and its retained complement. At the switches there is no physical projection or impulse.

Impose the actual complete-loss native cut P during W. It acts only on the complement of every processor block. On this restricted space the total generator is CP/TNI. Each compressed weak term retains its processor support and norm; it need not annihilate trace. For any selected current active blocks R, let P_R be normalized partial-trace generator reduction. Then

 K^R = P_R K + sum_{j in R} L_id,j

has CP/TNI propagators by reduced short-step product limits and independent intended gates. Other nominal interactions act wholly in the current complement, so (P_j-I) kills them. Convex multilinear interpolants are CP/TNI contractions. On F this is the ordinary full-system construction with native generators off. No simultaneous all-time partition is needed: derivatives are assigned to their locations in their actual intervals. Ordered partition differentiation and the same q-leg incidence counting therefore give

 ||E(S)||_diamond <= product_{j in S} x_j,
 x_j <= [2*3^(q-1)g eta tau]^(1/q)+delta_j,             (H1)

using worst fixed gate size/time and exact-target defects if convenient. Fixed CP/TNI maps at a boundary may be inserted without changing (H1).

Location support also survives switching. In each interval a selected good block has exactly its intended map, with an arbitrary joint complement map. Matrix-unit expansion on faulty active blocks proves the same signed location span without estimating coefficient norms. Compose intervals on their actual wires; native physical sites formerly in the complement become ordinary input wires in F. Crucially, during W the imported canonical killed dynamics has EXACT native logical identity on its admitted chart. Processor partial traces and native-only cuts commute that logical tensor factor. Thus every W cavity retains native logical identity, including its arbitrary bath coefficients. No claim of native identity follows merely from calling DATA a bath.

One physical cross-noise term in F touching command cone i and native idle site j may mark BOTH locations faulty. The active list includes j, so this error cannot hide inside a free bath coefficient. Its support is paid in the region containing j. The final active-space restriction is the reason W's bath convention cannot simply be continued through F.

### 1.2 Fixed selected-time live-prefix cut
Let T_W be the ACTUAL polynomial waiting time. Native full-versus-killed error on the admitted source is epsilon_kill(T_W), from the operator-uniform native boundary theorem with processor/bath included. Native logical independence is used only inside the killed chart, not asserted for the uncut process.

At the fixed end of W insert, in the ANALYSIS only, the joint native spectral cut Q onto E<=eN and M_BUSY<=bN in the SAME forest chart. It is native-only, logical-independent and CP/TNI. It commutes the canonical labels needed by the accepted native receiving theorem. Obtain energy tail t_E from the killed energy relaxation, and BUSY tail t_B from the actual full dynamics; transfer the latter to killed at cost epsilon_kill. The commuting joint-cut loss is at most

 d_pre <= t_E+t_B+epsilon_kill.

For clarity, the H0 envelopes give
 bar_w_E=nu_E+(w_E0-nu_E)exp(-a_E T_W),
 bar_w_B=nu_B+(w_B0-nu_B)exp(-lambda_B T_W),
 t_E=exp[-(s'e-q_t-bar_w_E)N],
 t_B=exp[-(2c_B delta_B b-bar_w_B)N].
Choose the fixed padding so both displayed exponent gaps are positive constants (or use the more conservative received native relaxation bounds). The processor gates act on witness-disjoint sites; native incident noise bounds and source inequalities are uniform on that processor space. The full BUSY inequality is not assumed for the killed generator.

Uniform gentle compression on subnormalized states gives

 epsilon_W = epsilon_kill + 2 sqrt(d_pre).              (H2)

This is a completely bounded source-restricted estimate with references, not a positive conditioning of the signed processor-good map. Choose the fixed padding cooldown by the explicit native moment relaxation inequalities; require the native source barrier throughout W and moment-floor gaps below e,b. Its duration may be very long but is N-independent. Polynomial T_W yields epsilon_kill=poly(N)e^{-cN} and exponential t_E,t_B with the received strict budgets.

Apply Q to the ONE whole killed-circuit expansion. Since Q is a fixed CP contraction, H1 and all joint fault sieves remain valid. Every computation-good coefficient still has native logical identity, and EVERY coefficient after Q has safe native physical support. No two marginal channel estimates have been multiplied. Q's tail is proved only for the actual killed circuit; cavities need contraction, not their own favorable energy tails.

## 2. Joint computation/output-region accounting
Let x_j be the admitted disjoint-rectangle recursion, with x_j<=x_* r^(s^j), r=x0/x_*<1, s>=2. For the polynomial logical command circuit with L rectangles define

 b_comp <= L x_k exp(L x_k).

Choose k=O(log N) so b_comp<=e^{-c_comp N}. Every output decoder has the actual quantum receiving identity on the entire hierarchical sparse input span, not merely correct classical labels. With B including actual totalizing refreshes, padding, final recovery and port/reset locations, its joint bad-output strength can be bounded by

 p_dec <= product_{j=0}^{k-1}(1+x_j)^B-1
       <= exp[B x0/(1-r)]-1.                            (H3)

If terminal port/reset is instead accounted separately, remove it from B and include those locations below; NEVER count it twice. Fix the first convention here: B includes port/reset and terminal decoder, while c_gate below includes controlled-Pauli gates and native/hub idles only.

Partition final native sites into disjoint recipient regions: each DATA resource i receives its two command decoder cones plus its final controlled gates/idles; private hubs form idle-only regions. Shared physical gate blocks are assigned once, with a fixed enlargement constant g_reg for their native support. In the explicit two-site command–DATA architecture each control belongs to one DATA region; no inter-region ideal gate occurs in F. All remaining protected record/processor outputs must be kept outside these cones, and their correctness is included in b_comp or, if post-computation record retention is desired, its protected identity circuit is included in the same whole bad-computation event. Record retention is not free.

For one DATA region the exact OR indicator and prefix-free disjoint stage sieves give

 p_i <= (1+p_dec)^2 (1+x0)^{c_gate}-1.                 (H4)

Idle-only hub regions have the corresponding fixed location OR bound. Set p=max_i p_i and M<=C_M N. Different decoder stages, final controls, computation rectangles and recipient regions use disjoint physical spacetime location sets. Their bad predicates can be expanded into inclusive sets using the same full signed expansion. Consequently every joint conjunction of r specified bad regions has norm <=p^r, and the conjunction with computation-bad has norm <=b_comp p^r. Shared baths and noise touching several regions are already allowed by H1; these are NOT independence probabilities.

Let at most t=floor(delta N) bad recipient regions be allowed, K=t+1. The exact cardinality sieve gives

 b_tail <= binom(M,K) p^K (1+p)^{M-K},
 b = b_comp+(1+b_comp)b_tail.                         (H5)

Indeed restriction to computation-good is subtraction from the unrestricted map, yielding 1+b_comp, not division by a probability. A sufficient exponential condition is
 C_M H(delta/C_M)+delta log p+(C_M-delta)log(1+p)<0
(with a small strict rounding margin). Shrink fixed x0, eta and finite reset defects after choosing delta and hardware; no N-dependent noiseless primitive is introduced.

## 3. Native physical support, with live histories retained
Write f for the maximum owner DATA footprint and a for the maximum number of readiness predicates touched by a physical native site. Let r_in=eN/h, m_in=bN. On a good coefficient, at most t bad regions in F affect native support of size ell<=g_reg t. Arbitrary bad command outputs, even coherent and entangled with bath, only couple nominally to their own DATA recipient. Residual cross-couplings are paid by the additional faulty native active locations. Before F, Q gives the same safe native support even on decoder-bad histories.

For each fixed z and each support coefficient:
1. The input forest contributes at most 2f m_in canonical CSS weight when expressed in bare DATA.
2. Conjugating an error by the dense physical Pauli P(z) preserves its support. P(z) preserves the zero-code sector and all DATA-independent readiness predicates. Thus its intended density costs NO additional physical error weight.
3. Bad recipient regions contribute at most 2ell CSS weight and at most a ell additional BUSY owners.
4. The final inverse of the SAME forest contributes at most 2f(m_in+a ell).

Hence a conservative single-bank bound (better than the CNOT two-input bound) is

 m_+ = m_in+a ell,
 r_+ = r_in+4f m_in+2(1+fa)ell,
 E_+ = c_U r_+ + R m_+.                               (H6)

All these are coefficient-span bounds, not expected energies and not unions over all possible masks. Operators on private hubs can spoil owner histories and are covered by a, f. A DATA-only ideal Pauli leaves BUSY exactly unchanged; the two forest contributions are needed because it need not commute with history payloads.

Choose e,b,delta strictly so r_+/N<r0 and E_+/N<e_cut and inside the SAME common KL target module; also impose the native barrier/moment-floor margins required for subsequent cooldown. Existence follows from the accepted hardware hierarchy: first positive small e,b,g_reg delta, then proof ratios, weak first amplitude, and finally eta/reset defects. The previous CNOT budgets are conservative sufficient budgets because H6 is smaller than its 2r_in+6fm_in bound. No new choice of the actual native machine is made between stages.

The good map in the common warm output chart therefore has, for every z, EXACT factorization

 G_z = Ad_{P_L(z)} tensor A_good,z,                    (H7)

with A_good,z possibly signed and mapping the source auxiliaries to warm syndrome/history/retained-bath labels. This is the common two-sided KL statement for all good coefficient supports, not a claim that the signed map is positive. A correctly decoded command label alone would not imply H7. The good FT quantum-output identity, actual controlled-gate locality, and native common KL support are what prove it. Retained garbage may depend on z. No dependence on unknown L is hidden in A_good,z.

## 4. Positive classical-branch repair without an outcome-count factor
Let T be the CP/TNI physical map with native killed W and Q, followed by F. It differs from the actual physical channel by at most epsilon_W. Split T=G+B in the ONE full signed expansion, ||B||<=b by H5. Let Gamma_z be the CP/TNI output compression into the common warm chart and the correct protected record label z (if that record is part of the specified output). It includes a common computation-code analysis decoder solely to identify its sparse label, not an actual physical readout. Re-embedding will retain the protected physical record/error module. H7 lies wholly in this range.

For branch z define

 A_pos,z(X)=Tr_L[(Ad_{P_L(z)^dagger} tensor Id)
                 Gamma_z T_z((I_L/d_L) tensor X)].     (H8)

This map is CP/TNI and its output is in the same warm auxiliary support. Logical maximally mixed insertion, Gamma_z, and partial trace are complete contractions. Therefore

 ||A_pos,z-A_good,z||<=b,
 ||T_z-J_out,z(Ad_{P_L(z)} tensor A_pos,z)||<=2b.        (H9)

The second inequality compares T_z directly with G_z and the repaired factor; no extra gentle projection is needed because the signed good map has exact range and bad MAP norm b. The possible incorrect-label or coherent record components of T_z belong to B and are already paid. The input is genuinely classical: define H8 separately on each direct-sum block and add the resulting CP maps. The induced complete norm of a block-diagonal input-controlled map is the MAXIMUM of its branch complete norms, not their sum. Thus no factor |{z}| appears, even though each A_pos,z differs.

Re-embedding H8 is an analytical comparison, not physical depolarization/reset of L, not observation of a successful branch, and not permission to throw away a retained bath. All retained raw/control garbage and the native apparatus stay in the auxiliary output. The comparison preserves z-conditioned correlations needed downstream.

Including input approximation, the physical full-retained-bath feedforward output has a positive exact-logical warm comparator with

 E_FF <= epsilon_in+epsilon_W+2b.                     (H10)

## 5. Cooldown, trace and resources
The warm comparator satisfies the actual same-chart envelopes
 P_w F P_w <= exp([g+s E_+/N]N) P_w,
 P_w G_BUSY P_w <= exp(2C_B delta_B m_+) P_w.
Apply the accepted energy and BUSY relaxation/cut proof for a fixed tau_cool. It gives a positive common-chart restored source with additional error epsilon_C (native exit plus selected-time gentle energy/BUSY cuts); all retained processor/command garbage is now bath with the same bounded incident couplings. By default the post-cooldown target specifies native DATA only, with z retained as the input-branch index and any physical record now included in auxiliaries. If a protected output record z must also survive C, run actual protected identity rectangles on that record during C, include their bad-event OR in b_comp, and apply the same concurrent CP/TNI receiving argument to C; they are not free bath dynamics for that stronger output claim. No future nominal helper coupling to DATA is permitted unless a later operation explicitly pays it. This is the same hardware and does not reset histories.

Let E_total=epsilon_in+epsilon_W+2b+epsilon_C, omitting epsilon_C when only warm delivery is requested. The comparison is CP/TNI and is NOT silently normalized. Its trace defect on the admitted classical source algebra is at most E_total because the actual complete physical operation is TP. After the common benchmark native DATA decoder and tracing auxiliaries, its logical action is the desired classical controlled Pauli with a branch-dependent auxiliary survival effect. Complete trace-defect duality bounds the difference from the normalized ideal classical feedforward channel by another E_total. Therefore

 ||Out_actual - FF_ideal||_diamond <= min(2,2E_total).  (H11)

The final decoder here is the same mathematical DATA benchmark, not a noiseless physical terminal detector. If retaining the full bath is required, H10 is the positive TNI comparator and its trace loss must remain visible; do not replace it by an outcome-independent bath channel.

Logical command work is polynomial N for explicit Pauli matrices (linear maps cost O(N times record_length) before routing). Fixed concatenated-code gadgets, space, actual routing/idles and shrinking schedules at k=O(log N) cost polynomial N for e^{-Omega(N)} global error, potentially enormous exponents. The 2N exposed output floors stay O(x0), but the native outer radius converts their JOINT sparse law to exponential bank reliability. Native waiting time is the actual resulting polynomial and fits the received exponential horizon asymptotically. Fixed F has constant duration and bounded recipient degree; global processor geometry is only the supplied gate/routing architecture. No bounded-dimensional geometric layout or practical advantage is inferred.

This closes a scheduled protected-CLASSICAL-record-to-native-Pauli interface under the supplied source chart. It does not establish that the previously destructive measurement leaves an arbitrary surviving bank in that chart, nor teleportation/gate injection, universality, autonomous scheduling, arbitrary coherent controlled gates, physical final readout, or superiority to an ordinary FT processor using the same resources.
