# Full matching pulses and a positive reusable native register
30 October 2026. Root composition candidate. Requires independent whole review; the local live-prefix/cycle lemma has its own scoped receipt.

## 1. Exact register and physical schedule
Take B copies of the SAME accepted native CSS Tanner bank, each with size N, linear distance, full private controllers/resources, and zero-reference recovery. The bank interaction graph has fixed bounded degree. A preinstalled edge couples corresponding DATA factors of its two resource sites. Native hub/resource sites are not regrouped into a site containing all B banks. Thus the added physical degree and local dimensions are independent of B and command depth.

A round has: native relaxation on ALL banks for fixed dwell t_d; bounded coefficient shutoff; one fixed-duration window tau with ALL nominal native generators off; and reactivation. During the window, a chosen matching receives actual transversal CNOTs. Unmatched banks have identity windows. Every private hub and resource factor remains in the local-noise budget. Weak perturbations stay on throughout. The direct target Hamiltonian on a matched DATA pair is H=(pi/(2 tau))(I-CNOT) tensor I_aux, with norm pi/tau and exact endpoint CNOT. All controls are externally specified; local bounded calibration deviations are charged as noise. Wrong global commands and an autonomous noisy scheduler are not supplied.

Abrupt bounded coefficient switches are one allowed implementation with no state kick. A finite-ramp implementation must receive its own enlarged owner/insertion constants; it is not silently implied by the abrupt result. The present whole construction first uses the abrupt model.

The code's transversal CNOT acts on all corresponding logical coordinates. There is no individual logical-coordinate addressability claim inside a positive-rate bank. B may grow. Routing across the bank graph can use three such CNOT rounds for a neighboring logical-bank SWAP, paying every dwell/window. Neither full Clifford nor non-Clifford universality follows.

## 2. A joint pulse error expansion, not other logical banks hidden as a bath
Use the accepted finite bounded joint-CP-divisible CP-cavity theorem on the ENTIRE pulse window. Intended gates are disjoint two-resource gates and one-site identity locations. Auxiliary controller sites have identity locations. Fixed site dimensions include DATA plus tags/monitors. No native strong payload remains on. The external bath may be shared; all logical banks remain system factors.

For x=[2*3^(q-1)*g*eta*tau]^(1/q), g<=2 (or the actual fixed primitive bound), the exact pulse fault maps satisfy

 ||sum_(F contains S)E_F||_diamond<=x^|S|.

Use an explicitly qualified approximate pulse discrepancy in x if the intended finite gate is not exact. The theorem's finite/bounded joint model is retained; this does not automatically extend the native memory's normal infinite-bath interface.

Partition locations into G<=B groups, one for each matched pair and each idle bank. Each group has M_j<=c_loc N locations, with c_loc including private apparatus. They are disjoint location sets. At a good group at most K locations are faulty; each such location has at most g sites, so its post-ideal physical error support is at most ell=g K. A Clifford endpoint may spread errors only inside its same constant-sized gate box. No Pauli probability model is asserted.

The exact bad-group indicator sieve gives

 b_p(N)<=binom(M_max,K+1)x^(K+1)(1+x)^(M_max-K-1),

when K+1<=M_max, and zero otherwise. For any selected groups, multiplying their disjoint sieve polynomials gives their joint bad-map norm <=b_p^number_selected. Consequently the FULL bad-union map has

 epsilon_p <=(1+b_p)^G-1.                              (MR1)

This is inclusion-exclusion on signed MAPS, not a probabilistic union bound. For K=Theta(N) and sufficiently small fixed x, b_p<=exp(-c_pN). There is no exp(eta B N tau) Dyson prefactor.

## 3. Every good pulse history has the same logical gate and small native endpoint
At input, every bank is in its common canonical logical module with E<=eN and physical BUSY<=bN. The new independently reviewed local lemma LIVE_PREFIX_AND_FIXED_CYCLE.md gives, per output bank of a matched pair,

 b_out=b+c_act ell/N,
 r_out=2e/h+6 f b+2(1+f c_act)ell/N,
 e_out=c_U r_out+R b_out.                              (MR2)

Here f counts physical DATA footprint, hence the factors of two for the BOTH-CSS convention. Idle banks satisfy a weaker bound covered by these constants. Ready predicates are DATA-independent; an ideal DATA CNOT does not create BUSY. Histories may become dirty only inside already BUSY owners or new fault cones. The same forest chart at output, not a clean new apparatus or a physical frame inverse, gives MR2.

Choose all densities below the actual code/KL/native warm margins as in the local receipt. A fixed common correctable-span decoder on each bank then factors EVERY good two-sided fault coefficient as the intended joint matching logical CNOT times an auxiliary/bath map. This includes arbitrary coherent correlations across groups. The good sum G_p is signed but has the exact form

 G_p=V_out (Ad_U_L tensor A_good) V_in^*,

on the admitted input module, with output range in the same logical-independent warm syndrome/history subspace. The isometries denote the actual common logical/error chart; they are analysis tools, not physical gates. Their coherent range and all-logical factorization are required, as in the local positive-restart receipt.

## 4. Positive logical-factor repair directly from the BAD MAP
Write the actual restricted pulse channel Phi_p=G_p+B_p, ||B_p||_diamond<=epsilon_p. Compress Phi_p to the common output chart to obtain a CP/TNI map Psi. Since G_p already lies in that range,

 ||Psi-(Ad_U_L tensor A_good)||_diamond<=epsilon_p.

Remove U_L in this analytical chart and define

 A_pos(X)=Tr_L[(Ad_U_L^dagger tensor Id)Psi(I_L/d_L tensor X)].

This map is CP/TNI and supported in the SAME warm auxiliary cut. Complete contraction gives ||A_pos-A_good||_diamond<=epsilon_p. Reembedding Ad_U_L tensor A_pos therefore yields a positive exact-logical warm source channel tildeG_p with

 ||Phi_p-tildeG_p||_diamond<=2 epsilon_p.                (MR3)

No separate gentle projection charge is necessary HERE: Phi_p-G_p is already a complete bad-map bound. This sharper receiving argument must not be used where only a bad population is known. It does not physically depolarize the logical input. It also does not pretend projection onto a broad code subspace alone gives correct logical information; the exact good-map factorization is essential.

The source contract begins with a logical/reference input and a logical-independent positive auxiliary state, or the known-target factory. The new positive factor map preserves this structure through every round. No arbitrary initially logical-dependent bath is newly admitted.

## 5. Native relaxation on the full register
During dwell all banks run their original native generators, with no nominal bank-to-bank coupling. Use the product of individual canonical memory cuts. Each bank witness F_i commutes all other banks' cuts. Its same operator drift survives COMPLETE-LOSS compression to the product cut: the omitted total outgoing gains are positive. Terms not touching bank i vanish on F_i by identity annihilation, while touching terms use that bank's O(N) incident budget. Thus the source term is rho N for each bank, not rho BN.

Every retained canonical edge inside the joint cut acts as logical identity on EVERY touched bank: its actual per-bank distance margin is unchanged. This gives one joint logical-identity killed evolution with arbitrary cross-bank bath correlations. The original boundary-map argument can be summed over possible first exiting banks, giving

 epsilon_mem <= B C N(1+t_d) exp(-c_mem N),             (MR4)

with the SAME per-bank warm allowance and fixed constants. This joint-cut receiving step must be checked against the actual original full/killed proof; a global radius proportional to BN is invalid because the product code's minimum distance remains order N.

The local receipt derives exact positive-moment relaxation:

 log Tr(F_i rho_cut)/N <=nu_E+(w-nu_E)e^(-a_E t_d),
 a_E=lambda_E/s, nu_E=g+s rho_E/lambda_E,

and the independent full-Hilbert BUSY moment has

 log Tr(G_busy,i rho_full)/N<=nu_B+(w_B-nu_B)e^(-lambda_B t_d).

For source values w=g+s e_out and w_B=2C delta_B b_out, choose the stated fixed dwell so both are strictly below their energy/BUSY cut exponents. The resulting per-bank energy and BUSY tail exponents c_E,c_B are positive constants. To transfer BUSY to the joint killed state, first bound the FULL-state UNION of bad BUSY counts by B exp(-c_BN), then compare full and joint killed ONCE. Do not multiply the global comparison by B a second time.

The common energy/BUSY input projection is logical-independent in the canonical chart. Its bad mass is bounded by

 p_cut<=B[exp(-c_EN)+exp(-c_BN)]+epsilon_mem.

A conservative complete gentle projection estimate gives a positive exact-logical input-cut channel with dwell error <=epsilon_mem+2sqrt(p_cut). All comparisons retain the actual auxiliary history; nothing is reset or independently resampled.

## 6. Close the cycle and compose
Use the actual simultaneous parameter choice from the local fixed-cycle lemma, NOT arbitrary previously chosen rates. The inequalities require stationary floors strictly below the input thresholds and MR2 strictly within native warm/KL/BUSY margins. The governing native small-first-edge family makes g,q_t and activity small and permits rho_E/lambda_E small before eta is fixed; dwell is finite after those choices. All hardware/rates/durations are fixed independently of N, B and command count.

Each idealized comparison round is a CP/TNI channel with exact matching logical action and a positive supported auxiliary map. Hence channel telescoping through R rounds gives a conservative total error

 epsilon_boot + R[2((1+b_p)^B-1)+epsilon_mem+2sqrt(p_cut)],       (MR5)

up to the explicitly counted initial/final dwell choice. Constants depend on fixed physical/code choices only. Choose N large enough relative to log(BR/epsilon), and keep total elapsed time within the actual native horizon. The bound can always be capped by2. The schedule cost is fixed dwell plus fixed pulse per round, O(BN) resident native hardware and O(N) two-site gate terms per selected bank edge. Source preparation has its separate polynomial temporary cost.

At requested endpoints, physical bare DATA has the common correctable span supplied by the energy/BUSY caps. The SAME fixed product ordinary DATA decoder therefore returns the actual cumulative logical CNOT circuit; it does not manufacture a command-dependent logical gate. That decoder remains an analysis/readout benchmark unless a physical extraction interface is separately supplied.

## Scope to review
This would supply a genuinely scalable addressed BANK interaction register beyond the earlier fixed-colocated-finite-group tracker, without growing onsite group labels or resetting live controllers. It remains externally scheduled and does not provide arbitrary intra-bank logical addressability, H/S/T gates, noisy instruction distribution, physical final detection, geometry/finite-speed wiring, practical advantage or historical novelty. The root pulse note and local receipt alone do not certify MR1-MR5; this entire composition awaits review.
