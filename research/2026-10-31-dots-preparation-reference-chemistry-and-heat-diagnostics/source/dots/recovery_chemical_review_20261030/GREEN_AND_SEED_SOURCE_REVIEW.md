# Independent scoped review: dormant Green and seed-interrupted source
30 October 2026. Reviewer `producer-workspace/review_dormant_extension`.

## Decision and frozen sources
**Scoped PASS** for both local statements, with the explicit kernel/marker details below. These are two missing local inputs, not a complete recurrence proof.

- `DORMANT_GREEN_NONBALANCED_V2.md`: SHA256 `e85e99a7fd41aa3a749852b8a64fb30265b982c38f980f4ad46b9695498986f7`.
- `SEED_INTERRUPTED_SOURCE_V2.md`: SHA256 `590a18947f89b8e88f17b8dfd744a8cc37500953944a977e066027a05f0192ce`.

Copies are retained under `frozen/`. The source constants may depend on fixed positive rates, m,q,theta,alpha; there is no uniform theta limit or useful numerical constant assertion. D=0 and frozen C are essential for the Green, and the source estimate starts at D=0,B=q,A>=m. At a true seed the residual uses conserved A+C+D and the ACTUAL off-section B. No artificial reset to the section is accepted.

## 1. Exact residual identities
For B>0 write B=j(q-1)+v, 1<=v<=q-1, and H(B)=j(m-1)+v; H(0)=0. Then activation at positive B increases H by exactly m-1, so it leaves r=A+C-H(B) unchanged. Immigration is residual-neutral except the positive-B residue wrap, where it increases r by q-m. The compulsory B=0 immigration is neutral. A clearing decreases r by either zero or q-m; at B=q it is exactly neutral. These statements follow directly from the residue formula, not a continuous linear approximation to H.

A true seed decreases A by one or two while increasing D by the same amount. Its residual is therefore unchanged BEFORE versus AFTER the seed when the terminal formula uses A+C+D. The inverse-A factor changes by a fixed bounded ratio; for large A this ratio is 1+O(1/A). The seed's B phase remains unchanged.

## 2. Finite-corner values are earned independently
Before the seed, the law is the three-complex connector with clearing rate d+s, whose clearing gains are independently marked seed with probability p=s/(d+s). Its complexes 0,A+B,mA+qB form one linkage class of rank two because q>m. A positive complex-balanced point solves ab=i/t and a^m b^q=i/(d+s); substitution produces a unique positive solution.

The standard deficiency-zero/product-form theorem applies to this REFERENCE connector, not the full nonbalanced network. Weak reversibility makes each reachable communicating class closed: a reverse complex path transports the original enabled source while keeping spectators. Nonexplosion is independently justified with 1+A+B. Where both clearing thresholds hold, the high-degree negative term eventually dominates tAB outside a finite set; on either threshold strip, AB is bounded by a constant times A+B. Thus the required global linear upper drift is available without calling the actual birth intensity globally linear.

The conditional product-Poisson measure has finite polynomial-exponential moments. In each class choose a reachable clearing-enabled regeneration state. Its expected cycle occupation of W and of every polynomial-intensity reward envelope is finite. Each cycle has a fixed positive chance of a seed mark. Marking a cycle does not increase its reward, so geometric regeneration bounds the stopped total. Weighted rewards from any fixed initial state to the regeneration state are finite: otherwise a regeneration cycle with positive probability of visiting that state would have infinite reward. The terminal seed reward is paid by its rate times a bounded W multiplier. Section entries are paid by incoming jump-intensity occupation. This establishes actual finite-input values independently of the desired uniform Green.

Frozen C is unbounded but only multiplies every reward and the initial weight by exp(theta C); normalized finite-corner values therefore depend only on finitely many A,B inputs. No uniform bound over infinitely many independently chosen C values is assumed.

## 3. High-A block and finite-A/high-B kernel coupling
Choose A0 first. For A>A0,B>=q, the next-mark competition ratios are uniformly O(A^(1-m)) for activation and O(A^-m) for immigration. Weight multipliers for any one birth are bounded, and birth repetitions increase A, so a positive geometric majorant sums them. A surviving clearing changes the inverse-A factor by 1+O(1/A) and never increases the exponential residual.

When a clearing enters B<q, its low approach has at most q immigrations before reaching high B, or an earlier activation. At positive low B, the immigration race is O(1/A); the compulsory B=0 immigration is neutral. Consequently the low approach has normalized terminal factor 1+O(1/A), bounded running reward and bounded section-entry multiplicity. If A crosses into the head at clearing, stop the high block there rather than assert its large-A estimate beyond the boundary. High running costs include the potentially O(1) wait at B=0.

The resulting nonseed weighted continuation is at most 1-p+O(1/A), hence at most rho<1 after increasing A0. Its geometric Green and the head-entry coefficient are finite with constants independent of the later B0 choice. An entry into a finite corner can be priced by its actual boundary value, rather than enlarged into a head coefficient.

For A<=A0,B>=B0, collapse the stated zero-, one-, or two-preparatory-event routes before seed/clearing. Intermediate A is retained INSIDE the step, even if it exceeds A0. Competing immigration before an activation is O(1/B0); competing high births before a mark are still smaller. Every error endpoint changes A,B by bounded amounts and has a bounded W multiplier.

The leading surviving endpoints are exactly (A-m,B-q), (A-1,B-1), and (0,B). They do not increase r. Repetition reduces A to zero and then holds it there. Thus the n-step kernel is bounded by (1+A0)^alpha(1-p)^n even when its one-step weighted row sum exceeds one. Its Green is finite. Leading crossings below B0 enter a fixed finite corner.

After applying this leading Green, head-to-head and head-to-high error coefficients tend to zero with B0. Select B0 only AFTER fixing A0 and the high/head coefficient. The finite-corner reward constant may grow with B0; it is an additive source and does not enter the small coupling product. Applying both inequalities to finite/truncated positive kernels before taking monotone limits establishes the uniform Green without subtracting undefined infinities. This is a legitimate two-region closure, not a circular assumption of the same Green.

## 4. All three Green rewards and actual marks
Each block/step has a bounded number of prescribed events, while high-birth repetition has a summable weighted geometric majorant. This pays running W, bounded terminal seed W, and section-entry count W. In the finite corner the polynomial-intensity reference argument pays the same rewards. A source stop at the first section return is dominated by the Green's sum of all section-entry rewards. The initial visit may be counted once as an additional W source.

This establishes the same theta and same alpha profile Green. It says nothing about making its constant close to one, about the process after D becomes positive, or about full-network recurrence.

## 5. Rare degree at the section, with seed interruption retained
The proposed rare-event union is valid. In its complement, I=0 and H<=1. If H=1 then L=0, so no nonneutral immigration occurs and positive residual is impossible. If H=0, the initial clearing goes from B=q to B=0. A low activation followed by clearing maps low B=l to l-1 with zero residual change. A seed interrupting that pair likewise creates no positive residual because activation is neutral and true seed preserves total composition. A positive terminal residual must therefore be the low immigration wrap into q, requiring at least q-1 positive-low-B immigrations after the B=0 launch. This contradicts L<=q-2.

Thus every positive terminal increment lies in the displayed union. With q-1>=m and 2(m-1)>=m, its minimum rare-factor degree is m. H>=2 is an allowable over-cover even though high activations by themselves are neutral; the estimate does not require every covered path to have positive residual.

## 6. Explicit tilted generating-function domination
The analytic marking paragraph can be made precise without independence assumptions. Above the half-input boundary, put z_L=C/a, z_H=C a^(1-m), z_I=C a^-m. Absorb the bounded residual immigration tilt exp(theta(q-m)) into C. One low approach is bounded coefficientwise by a fixed-degree positive polynomial in z_L l with constant term at most one. Repeated high births are bounded by (1-z_H h-z_I j)^-1. The product B(l,h,j) has B(1,1,1)=1+O(1/a).

A surviving marked block is bounded by (1-p)B. Terminal block rewards are bounded by a constant times B. Therefore the complete marked stopped path is coefficientwise bounded by a fixed multiple of

 B(l,h,j) / [1-(1-p)B(l,h,j)].

For a large enough, this has a common analytic neighborhood of (1,1,1) with positive coefficients. A derivative of marker order (u,v,w) introduces the factor z_L^u z_H^v z_I^w, with constants depending only on the fixed orders. The associated factorial moments dominate the event indicators L>=q-1, H>=2, H>=1 and L>=1, and I>=1. This yields exactly the four claimed joint TILTED orders, not a product of marginal probabilities. Stopping earlier at a section return or half-input boundary removes positive terms and preserves the domination.

## 7. Weighted half-input entrance and conclusion
Only clearing lowers A on D=0. Crossing A<a/2 before seed therefore needs at least floor(a/(2m)) surviving clear marks. The same tilted block majorant gives a rho^k entrance-weight bound. If a boundary crossing occurs before the block's low approach, its fixed bounded final multiplier is priced separately; no unproved low-A continuation is hidden inside the large-A block.

At this ACTUAL boundary state, apply the alpha=0 Green using its actual B phase and frozen C. A first section-return reward and a seed reward are both dominated by Green rewards. Strong Markov gives exponentially small weighted exceptional continuation. No probability times an independently averaged large reward is used. For bounded initial a, the same uniform Green and the positive minimum of (1+a)^-m give the remaining finite constant.

Consequently E[(w_sigma-w_0)_+] <=C_theta w_0(1+A_0)^-m is established for the stated seed-interrupted episode. It bounds a positive source; it does NOT supply a negative useful-activation margin or continue a seed through the positive-D processor back to the original section.

## 8. Independent checks and remaining gap
`check_dormant_phase_budget.py/json` independently verifies the exact residual increment identities and exhaustively explores the complement of the rare-event union for 12 fixtures spanning (m,q)=(4,5),(4,8),(6,7),(6,9). It checks 659 reachable states and 375 seed/section terminal cases; no positive terminal increment occurs in the complement. Finite enumeration supports the algebra, not the asymptotic kernel bounds.

The accepted occupation-normalized return comparison may now use this local Green when its exact phase/source contract fits. It does not automatically establish the complete positive-D-to-section cycle, the useful negative term, or high-b continuation costs. No general weak-reversibility theorem, historical novelty, hardware chemistry or full recurrence is claimed.

## Primary reference
Anderson, D. F., Craciun, G., & Kurtz, T. G. (2010). Product-form stationary distributions for deficiency zero chemical reaction networks. Bulletin of Mathematical Biology, 72, 1947–1970. https://arxiv.org/abs/0803.3042 . The authors' abstract was checked on 30 October 2026 for its complex-balance/closed-class scope; the explicit reference connector, nonexplosion and kernel estimates above were checked directly. No denied source was retried.
