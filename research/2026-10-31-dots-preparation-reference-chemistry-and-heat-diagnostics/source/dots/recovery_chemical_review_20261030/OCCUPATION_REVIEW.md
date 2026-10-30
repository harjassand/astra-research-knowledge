# Independent review: occupation-normalized dormant return
30 October 2026. Reviewer `producer-workspace/review_dormant_extension`.

## Verdict and exact bytes
**Scoped PASS for V1 PLUS the explicit dormant-stop completion.** V1 alone omitted an event in its lower-occupation survival accounting; it is not retroactively accepted as complete.

- `OCCUPATION_NORMALIZED_DORMANT_RETURN_V1.md`: SHA256 `78b1efd84271f8d0c0fe4de54b421a5d917bca87f9fdd1af8056a6e65614f7a9`.
- `OCCUPATION_V1_DORMANT_STOP_COMPLETION.md`: SHA256 `aa4dc6b695e9f565e6e2104aac00751424d0b1e300c4fa7ae3283ba2af4dfacc`.

Both frozen files are retained under `frozen/`. The accepted statement is the SAME positive-D first episode's inequality

 V <= C (b)_q (1+A_in)^(-2) U,

where V is its inverse-m dormant-entry payoff, U its actual physical integral of A, and the episode stops at clearing, either actual connector birth, or first D=0. Fixed positive rates, a0>=2, m=a0+2, active positive-D input and b>=q remain required. No low-A truncation is part of the claimed episode. The full connector-cycle forcing bound and global recurrence are NOT accepted.

## 1. Resolvent drift checked directly
Let u>=1+a0, d>0, s>=2, and g(u,d)=u^-s/(u^3+nd). Fixed-d increments of u have relative decrease bounded above and below by fixed multiples of 1/u. Enabled decrements by one or two have relative increase O(1/u). Increasing d can only help a decrease estimate.

For simultaneous (u,d)->(u+1,d-1), d>=u implies

 g(u+1,d-1)/g(u,d) <= (u/(u+1))^s d/(d-1)
                         <= (u/(u+1))^2 u/(u-1).

For u>=3 the last ratio is at most 1-c/u with a fixed c>0. If d<u and n<=C u, the harmful denominator contribution is O(1/u^2), so the same conclusion holds for sufficiently large u. States with bounded u under this relation have bounded d,n and form a finite exception set. At d=1 the zero cemetery continuation is even smaller than a positive d=0 value.

For z=x+eta c, n<=C_eta z+d. Thus the favorable bound applies to reactions 2 and 6 above a fixed shell threshold. Reactions 3 and 4 have z increments of opposite signs of size 1-eta. Choosing this positive size small enough lets reaction 2 absorb reaction 3. The resulting negative psi drift is of order d(a+c+d-1)psi/z, including the a=c=0,d>=2 face via reaction 6.

For phi, the C-poor region c<=M x gives z comparable to x and hence psi comparable to phi, with fixed constants. The possible conversion-3 drift is O(d phi), which a sufficiently large C2/C1 absorbs using the psi margin since n/x is bounded below on sufficiently large active shells.

In the C-rich region, reaction 4 supplies -c cd phi/x. If d>=x, the simultaneous transitions are favorable and reaction 6 additionally supplies -c d(d-1)phi/x. If d<x, an upper bound on their harmful denominator contributions divided by cd phi/x is

 C(a+d)n x / [c(x^3+nd)] <= C'/x,

using a,d<x and n<=c+2x. This is absorbable for large x. For bounded x, d is bounded, their positive contributions are O(phi), and the negative reaction-4 term grows with c. Thus the stated regional negative nd phi/x margin is valid beyond a fixed shell threshold.

Both creation channels have positive contribution at most C a F_s. Half the quadratic clearing loss absorbs this for sufficiently large a. At bounded a and large shell size the nd margin absorbs it. Since F_s is comparable to phi_s, the final combination dominates

 [a^2+nd/x] phi_s >= c x^(-s-1)

in the relevant large-a or bounded-a/large-n cases. This proves the central asymptotic drift with constants depending on rates,s,a0,eta and profile coefficients. No useful numerical constants are established.

Small shells must be handled by actual finite killed values and finite maxima of value/profile ratios, as in the preceding local review. They are not covered by blindly rescaling a wrong-sign pointwise drift. Independent finite-difference diagnostics actually show positive drift for some trial parameter choices at finite n; these are consistent with the asymptotic theorem and make that distinction material.

## 2. Upper return value
The sole dormant entrance remains reaction 2 at d=1. At s=a0 its payoff intensity is at most C x^(-s-1), precisely the running source paid by the resolvent drift. The generator in this argument already kills at D=0; restoring the terminal reward adds only this explicit source. Scaling F_s and applying stopped Dynkin gives V<=C x^-a0/(x^3+nd).

Connector birth killing reduces V. Thus the no-connector upper bound is uniform in b>=q, without supposing the operational connector rates vanish. Small active shells have finite no-connector killed values; their profile denominators are positive and there are only finitely many composition inputs, so a larger uniform constant covers them. The bound follows over all low-A excursions because the supersolution was verified on all positive-D states, not solely an incoming band.

## 3. Lower occupation and the corrected missing event
Set t0=epsilon x/(x^3+n d_in) in operational time. Until a factor-band exit or a creation/clearing/connector event, A is comparable to its incoming value and d<=d_in. Total fast event intensity is at most C(x^2+n d_in); its expected count before t0 and these stops is at most C epsilon x. A factor-band exit therefore has probability O(epsilon). Creation/clearing intensity O(x^2) has integrated probability O(epsilon).

The actual episode ALSO stops at D=0. This event was not listed in V1's survival probability union. The frozen completion repairs it:
- If d_in>=x, extinction requires at least d_in>=x negative-D jumps, bounded by the total fast-event count.
- If d_in<x, negative-D intensity is at most C x d_in within the band and with no creations. The probability of even one such event is at most C epsilon d_in x^2/(x^3+n d_in)<=C epsilon.

The normalized operational connector hazards kI/[(A)_a0(b)_q] and kT A b/[(A)_a0(b)_q] are uniformly bounded because A>=a0>=2 and b>=q. Also t0<=epsilon/x^2. They therefore add only O(epsilon) probability. For bounded incoming A use a fixed-width band and alter only constants. Taking epsilon sufficiently small leaves probability at least one half of surviving in-band through t0 in the REAL episode.

Before connector stopping, b is unchanged. Physical time change therefore gives

 (b)_q U = E integral A/(A)_a0 ds
          >=c x^(1-a0) t0
          =c epsilon x^(2-a0)/(x^3+n d_in).

No conditioning on an observed long-lived path is used. Combining this lower bound with the upper V proves the stated occupation-normalized inequality.

## 4. Evidence and exact remaining scope
`check_resolvent_drift.py/json` independently evaluates exact six-jump killed differences on all positive-D states for n=32,64,128,256, exponents 2 and 4, and trial eta values .5,.9,.99. It explores fixed coefficient ratios as a diagnostic only. Some finite cases have positive drift for these chosen profiles, confirming why neither a finite test nor arbitrary coefficient choice substitutes for the asymptotic constants and finite-shell value argument. The proof above, not a finite fit, supplies the large-shell estimate.

The earlier nonbalanced local review and its finite-shell generator tests remain unchanged. The author-reported solve through n=256 is not independently replayed in this receipt. No all-exponential-moments, dormant Green, complete section-cycle coefficient-one drift, or global recurrence conclusion follows. In particular an unpriced continuation source proportional to U cannot be silently identified with the complete-cycle source needed by a new global Lyapunov proof.
