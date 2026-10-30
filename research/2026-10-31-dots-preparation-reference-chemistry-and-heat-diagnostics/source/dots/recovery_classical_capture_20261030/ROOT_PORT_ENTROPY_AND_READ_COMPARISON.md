# Rooted port entropy and the full-controller hard-coded read comparison
30 October 2026. Root receiving construction. Conditional on actual rooted classical drift and its receiving basins/compiler; not a complete capture/read theorem.

## 1. A size-independent logarithmic bound for rooted factors
For one fixed physical port p, let

 V_p=sum_(connected A containing p) f_A,  W_p=sum_A |A| f_A,
 0<f_A<=exp(L |A|),  Z_p=1+K V_p.

Suppose the number of size-j rooted animals is at most a0^j. Choose tau>log a0 and C_tau=sum_A exp(-tau|A|)<=sum_(j>=1)(a0 exp(-tau))^j. It is independent of block size.

Use a comparison distribution on a vacuum symbol and the rooted animals, with unnormalized weights1 and K exp(-tau|A|). The actual normalized weights are1/Z_p and K f_A/Z_p. Nonnegativity of relative entropy gives

 log Z_p <= (L+tau) K W_p/Z_p + log(1+K C_tau).       (1)

This holds pointwise on the common diagonal classical basis, hence as an operator inequality. It does not replace the rooted drift by a single-site probability estimate.

If an actual classical generator satisfies L_c^*V_p<=-gamma W_p+bI, then its contribution to a product witness F_Q product_j Z_j is exactly that factor times (-gamma K W_p+Kb)/Z_p, PROVIDED its actions leave F_Q and the other blocks' factors unchanged. After allocating part of -gamma to the read perturbation, (1) turns the remainder into negative log Z_p plus a fixed small vacuum source. Choose K small but K v0 large when V_p>=v0 on a wrong port. This is feasible only when the actual rooted constants supply the required v0/vacuum separation; it is not an arbitrary rescaling of the physical noise threshold.

The initial product moment must be earned at the same localized scale. A mere global H<=delta n_class per record can make log Z_p=O(n_class), and is NOT sufficient to start the quantum extensive barrier with O(number of ports) energy.

## 2. Why a hard-coded full-controller comparator can price delayed reads
Fix the ideal captured bit b in a classical record's correct logical phase. Construct the NOMINAL quantum native memory with b hard-coded, using the actual same padded finite gate template. Its physical Lyapunov F_b, canonical cut and BUSY witness are operators on quantum DATA and all quantum controller scratch/tags, not on the record bit. Their accepted inequalities handle arbitrary private workspace/history states inside the stated energy basin.

A concrete actual read edge has

 H_read=|t+1><t|_hub tensor [P0_port tensor I_W + P1_port tensor X_W]+h.c.

The comparison edge is

 H_b=|t+1><t|_hub tensor X_W^b+h.c.

Their difference is P_wrong tensor K_h, where K_h has fixed bounded support/norm. Since P_wrong and every Z_p commute F_b, and the edge preserves record Z,

 delta L^*(F_b product Z_j)
   = P_wrong i[K_h,F_b] product Z_j.

The actual local relative-norm contract bounds this by J0 P_wrong F_b product Z_j. More general finite QND read legs admit the corresponding termwise bound if their full complete effects are retained. This argument compares ENTIRE physical generators; it does not multiply current bad-port probability by a later wrong-payload rate.

A wrong read can leave bad scratch after the port heals. That scratch remains in the state propagated by the hard-coded nominal generator and its FULL-controller inequality. Thus it is already an internal perturbation consequence, provided the comparison really has the same gate slots, full Hilbert space and actual no-creation/dirty constants. If the imported theorem were only a clean-snapshot statement this argument would fail; the global native theorem is explicitly stronger.

This comparison also shows why instantaneous source flips need not be declared clean native snapshot updates. Classical record-only operations leave F_b invariant even on entangled states. The actual controlled edge may change as the port flips; the difference above prices it exactly. A receiver claiming a current-record semantic channel would still need locking or an irreversible read boundary; this construction instead uses the fixed ideal-bit comparator and weighted perturbation.

## 3. Remaining physical obligations
The rooted classical law in the present work is first proved at an ideal atomic majority level. A fixed-body multi-site majority dissipator is not automatically the old two-site-Hamiltonian/onsite-reset native hardware. Either declare that changed bounded-body hardware resource or instantiate/review its actual finite controller and rooted credits. Safe-phase exits and joint multirecord capture must also be controlled.

Weak local noise acting anywhere in a large classical block needs a ROOTED oscillation bound C eta K W_p/Z_p, not a volume-sized C eta n_class term. Distant bounded-body partners must fit its actual relative-norm/incident-strength argument; do not add free long graph connections to an animal proof. Bad capture blocks with arbitrary port behavior can be treated as persistent bounded-strength hot supports only after their source law and the total-strength quantum receiver are verified.

No reliable raw-bit encoder, infinite retention, final classical frame computation, new quantum input encoder or universal autonomous computer follows from this receiving calculation alone.
