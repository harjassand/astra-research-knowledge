# Read-off completion: canonical warm support and noncommuting moment cut
30 October 2026. Separate constructive completion of the reviewed fixed-window support lemma and weighted seed effect. It closes this finite source interface at the stated hardware/resource scope, not global record-phase insertion or a whole factory.

## 1. Native footprint conversion from actual ready apparatus
Assume the source good module has actual strong-ready native apparatus and DATA in the common physical Pauli span around P_ref with both-sector radius r_src. Read-off ideal evolution acts only on the capture bath/records. Let X be the union of physical Q/apparatus sites touched by a low-order insertion coefficient, |X|<=ell.

Define c_act as the maximum number of native owners whose FULL strong-ready/ownership/read predicate can be affected by one physical site. Define f as the maximum DATA footprint size of one owner forest-prefix operator. Both are finite constants of the actual bounded-degree finite-program hardware; include malformed tags, full read footprints, and resource ownership labels. They are not the old numerical values of a different gate list.

Untouched owner predicates remain strong-ready because no nominal Q operations run. Hence at most c_act ell owners are active/dirty. In the exact native forest representation, every nonidentity prefix factor lies in one such owner's full footprint. Its arbitrary DATA operator expansion adds at most f c_act ell physical DATA sites. Together with directly touched DATA, and converting physical Pauli support to the sum of BOTH CSS-sector weights, this gives

 r_can <= r_src+C_rad ell,       C_rad=2(1+f c_act),
 M_BUSY <=c_act ell,             sum_h B_h<=c_act ell.

This is the same support-cone reasoning used in the frozen actual native recipient's finite endpoint, not an assumption of clean scratch after noise. Arbitrary auxiliary coefficients and coherent superpositions of owner/location sets are retained. The bounds hold coefficientwise, so the common span of all low orders lies in the simultaneous canonical support cuts. For initially non-ready apparatus, its existing owner/forest budget must be added; this note does not silently reset it.

Let c_U be the maximum raw local-energy increase per canonical BOTH-sector Pauli support, computed from the actual finite local distance tables and check incidence. For an imperfect fixed baseline with d differing basis coordinates, the reviewed |U_D-U_0|<=L d yields

 E_D <=c_U(r_src+C_rad ell)+L d+R c_act ell.        (WC1)

These definitions give explicit finite structural constants; optimizing their numerical values is unnecessary for a fixed-threshold existence statement. If a different native implementation lacks the bounded-owner forest property, WC1 is an additional premise, not automatic.

Choose ell=delta N with delta sufficiently small that the canonical radius, WC1 energy, and BUSY density lie strictly inside the SAME receiving allowances. In particular include Ld in the true-code basin, and retain the native warm-moment gap. The read-off Dyson truncation uses K=floor(delta N/q)+1. Its actual positive simultaneous-support cut then has failure at most the Dyson tail, since every low-order coefficient is already in that space.

## 2. A noncommuting cut can preserve the O(N)-boundary joint moment
Let rho be the actual positive seed-window output and P the simultaneous native support cut above. The weighted seed effect earns

 Tr(H rho)<=exp(nu_seed N),
 H=F_Q product_(j in B) W_j,
 nu_seed=nu_w+C_Q eta (N_Q/N)tau_seed+(|B|/N)log A_seed.

Here B consists ONLY of the O(N) boundary records actually driving the quantum receiver. At fixed seed size n0 each W_j<=w_max I. The actual native global envelope is F_Q<=exp(gN)exp(s E_D), with E_D<=c_E N globally because its local terms and local controller alphabets are bounded. If |B|<=c_BN, then

 ||H||<=exp(C_H N),       C_H=g+s c_E+c_B log w_max.    (WC2)

No commutation of P and H is required. Gentle projection and duality give

 Tr(H P rho P)
 <=Tr(H rho)+||H|| ||P rho P-rho||_1
 <=exp(nu_seed N)+2 exp(C_H N) sqrt(epsilon_support).    (WC3)

Keep P rho P unnormalized for the CP/TNI receiving map. Normalizing, if desired, separately divides by its trace, at least1-epsilon_support. The same complete trace-norm reasoning applies uniformly to a supplied source channel with retained reference and the stated common-support premise.

## 3. Noncircular parameter order and tail margin
First fix the code, actual native hardware and rate/proof parameters, the positive warm/barrier margin, all classical seed geometry n0 and phase/root weights, and the conservative constants c_act,f,c_U,c_E,c_B,C_H. Choose a strictly positive delta meeting the support/energy/BUSY margins. Fix the seed reset/copy schedule and exponents; they determine the finite tau_seed and constants in its weighted effect.

Only then choose eta. Put a0=2 eta (N_S/N)tau_seed and alpha=delta/q. For sufficiently large N, K>=alpha N and a0<alpha. The reviewed bound gives

 epsilon_support <=exp[-c_tail N],
 c_tail=-a0-alpha log(e a0/alpha),

a conservative expression diverging to +infinity as eta tends to0. Therefore choose eta so c_tail>2C_H+2mu for a fixed mu>0, while also meeting the seed residual and joint moment margin. Equation WC3 becomes

 Tr(H P rho P)<=exp(nu_seed N)+2 exp(-mu N).

Thus a fixed positive warm coefficient gap survives the good support cut. The required eta can be exceptionally small; no practical threshold or uniform-in-n0 claim is made.

This proof uses a fixed O(N) weight norm. For arbitrary subsets of the O(NT) bulk records, the product norm may grow with |S| and WC3 need not preserve the desired coefficientwise subset law. No such extrapolation is made. Bulk-record classification and the later joint signed phase maps still require their own localized receiving proof.

## Scope
Earned at this finite interface: an explicitly scheduled read-off capture window admits a positive, exponentially close, canonical-small/energy-small/BUSY-small source and retains its quantum-plus-all-boundary-root warm moment, under actual ready-source and native bounded-footprint assumptions. Still missing: global record phase insertions jointly with the consumer, later strong-hot support law, final noisy classical computation/correction, a native classical majority implementation, and an autonomous acquisition scheduler. These are not supplied by the finite-window completion.
