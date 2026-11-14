# Paid augmented bbox trial: conditional finite upper improvement

This is a NEW trial potential, not a stronger estimate of the old area-cut energy. It reuses the delivered fixed-diagonal augmentation, filled-domain injection, topology resolution and directed contour-count certificates. All these inherited interfaces remain assumptions. This note supplies the bbox-specific transfer; it is not an independent validation of those inherited interfaces.

## 1. Global trial and original boundaries
Let M_H contain configurations whose augmented plus components have nonwinding embedded filled domains D with lifted bbox semiperimeter b(D)=width+height≤H. Set H790 for R200,L1600. Use the original soft-source reservoir value1, f=1 on M_H outside majority target B, and f=0 elsewhere. Original core r5 is contained in M_H. The reservoir overlap A∩B is paid, not deleted.

Every such domain has V≤H²/4=156025 and P≥2b; the latter follows because each occupied coordinate column and row contributes two physical boundary edges, and augmented connectivity fills the coordinate projection intervals. Thus V/P≤H/8≤R/2. Filling holes does not enlarge the bbox. A simultaneous whole-interior spin flip of disjoint outermost domains preserves the new cut: every newly created interior domain lies inside a flipped domain, and the inherited complete augmented collar separates it from exterior companions. This is exactly the inherited contour-injection assumption, with containment in a rectangle replacing containment in an area-bounded domain.

Consequently the original normalizer bound Z_MH/ZA≤1/(1−u4), u4=6n(3/40)^(2r)/(1−3/40), and original inhomogeneous-field density/target-tilt proofs remain valid: those arguments use only injectivity, cutoff preservation, V/P≤R/2, V≤P²/16 and P≥2r for noncore components. Original theta,field,clocks and kappa are unchanged.

## 2. Structural gates with full support
Use the inherited fact that a relevant added spin is outside every affected filled domain, and joins at most eight disjoint outermost old domains. A gate inside a filled domain cannot create a bbox violation because all newly enclosed sites stay inside that old bbox; the inherited collar prevents joining exterior companions from inside it.

For a nonwinding merger, place the old domains in compatible lifts around the new site. Their projections are connected through that site by unit-coordinate adjacency. Hence b(new)≤sum_i b(D_i)+2. A bbox violation therefore implies sum_i P_i≥2sum_i b_i>2H−4; using S0=2H−4=1576 is a conservative integer threshold.

For first winding or inherited nonembedded topological failure, retain the old topology bound sum_i P_i≥2L−4≥S0. Thus every structural gate is covered by the SAME complete contour tuple overcount as the archived s79/40 area trial: each old V≤156025, total P≥1576, and j≤8. This includes every merger, shape, thermal interior, position and collar mark counted there. No bare-energy approximation replaces that sum.

## 3. Native-rate improvement only for j1
When precisely one outermost old domain is affected, a nonwinding bbox violation requires the added site outside that domain's bbox. In an outer row or column there can be at most one old physical plus neighbor. Any other plus neighbor belongs to the affected domain or would constitute another affected outermost domain, because the gate is outside all old filled domains. Thus k≤1 and ΔE=32−16k−.04≥15.96. Native heatbath rate≤exp(−15.96).

A j1 winding gate would require a contractible old lift spanning at least L−2, excluded by b≤H790<L−2. The inherited planar resolution identifies nonembedded failure with the same topology obstruction. Thus the slow-rate factor covers all j1 structural gates. No rate improvement is assumed for j≥2.

## 4. Completely paid combinatorial sum
Let alpha(z)=sum_(4≤P≤1900) alpha_P z^P be the archived positive unrooted contour-activity upper. It includes all valid filled-domain contours and additional nonnegative walk overcounts, area cap156025 and all n translations. Root/order removal and collar marking are unchanged. Set

 Q_j=3/j! sum_(S≥1576) S[z^S]alpha(z)^j.

Then the NEW trial has

 W_bbox/ZA ≤ {exp(−15.96)Q1 + sum_(j2..8)Qj + n*T_tail
             +n exp[−phi*n*(1/2−rho)+phi]
             +kappa exp[−phi*n*(1/2−rho)]}/(1−u4),

rho=1/500000. T_tail is the archived complete long-contour tail, without discount. Using kappa≤1 solely in this scalar upper is inherited and safe. Winding and all mergers use undiscounted tuple mass; majority overrides and source-target overlap are the final two terms.

## 5. Executed directed scalar
`bbox_paid_scalar.py` reads the archived upward-certified marked convolution output, reconstructs each Qj with outward Decimal arithmetic, and includes the full archived tail and original target/source/normalizer terms. It reproduces the old short sum first.

log Q1≤−6215.662009452948...
log Q2≤−6231.703246380572...
log Q3≤−6248.407594339501...

log(W_bbox/ZA)≤−6230.968562491198...

versus old upper−6215.661915829713..., a15.30664666-log improvement (about4.44million-fold in this bound). With the separately reconstructed C/ZA>exp(−6251), W_bbox/C<exp(20.031438), conservatively exp(21), versus the previous exp(36). This ratio still allows hundreds of millions, and remains conditional on all geometric and flow interfaces; it is not a practical sampler theorem or uniform polynomial guarantee.

The crucial merger entropy is NOT negligible: Q2 is comparable to the discounted Q1. Dropping it would give a false extra improvement. The changed trial invalidates automatic transfer of the old area-cut edge sampler/support witness. A new bbox-edge acquisition construction or adaptation must be supplied separately.

## 6. Small geometry tests and limits
`check_augmented_bbox.py` exhaustively checks every planar4x4 spin configuration with fixed(+1,+1) diagonal augmentation. It checks bbox span-sum bounds on every addition joining old components and the k≤1 rule on every isolated bbox expansion. These are local combinatorial tests, not torus-winding or filled-domain injection proofs. The torus and filled-domain interfaces above still require mathematical scrutiny; this is a candidate significant partial bound, not yet a fully established theorem.

## 7. Fresh directed threshold search
The proof extends to any integer H≤800 with H<L−2, replacing cap by floor(H²/4) and threshold2H−4. `optimized_bbox/certify.py` regenerates the positive coefficients from archived upward magnetic moments and executes a fresh upward-rounded marked convolution. The compiled code self-checks rounding and subnormal behavior; all completed runs report no underflow/overflow flags. It includes all previous tail, target, source and normalizer terms.

At H795 (s159/80) the conditional normalized upper is approximately −6231.488679881962, giving W_bbox/C<exp(19.511321) from the recovered exp(−6251) lower, hence conservatively exp(20). This is the best of the tested local thresholds, not a global optimization proof. Raw inputs, outputs and full-precision certificates are retained in `optimized_bbox/cert_r200/`. These fresh runs change the source trial as stated; the printed generic legacy certificate label W_cut must be interpreted as W_bbox, not old area-cut energy.
