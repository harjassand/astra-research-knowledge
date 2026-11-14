# Paired-column thermal partition and critical-anchor extension

New candidate for independent review. This improves a genuinely loose thermal preimage bound; it is not a new physical dynamics or a capacity-acquisition theorem. Do not add to a frozen package before review.

## 1. Exact two-column preimage factor
Use theta4, epsilon=exp(-2theta)=exp(-8), t=epsilon²=exp(-16), z=9/10. Consider an open rectangle of width m=2R+1 and height h=L-1, bottom plus, other three boundary sides minus. Sort each column's d minus sites to its top. If b is the number of extra vertical bubble pairs, its vertical energy excess is4theta b, yielding t^b.

Group columns (1,2),(3,4),..., (2R-1,2R), leaving the last column unpaired. For a pair assume d1<=d2, swapping the two column names for this analysis when necessary. Write n_ab for the count of rows with minus indicator pair(a,b). Then Delta=d2-d1=n01-n10. The internal horizontal disagreement excess over the sorted pair is2n10, with relative weight t^n10. Inter-pair horizontal excess is nonnegative and may be discarded.

Let states be00,01,10,11. The vertical transfer K_ab=epsilon^(Hamming(a,b)) and site matrix
 D=diag(1,z,t/z,1)
encode the pair. With bottom00 and top11,
 Z_h=e00^T (K D)^h K e11.
For the fixed column counts, the exact preimage factor is
 t^(-1) z^(-Delta) times the corresponding count-restricted contribution to Z_h.
The t^-1 removes the two mandatory boundary flips; each column has odd vertical flip count1+2b. The fugacity identity is z^(n01-n10)=z^Delta. Dropping the count restriction is a positive overcount.

Use the positive witness w=(1,20epsilon,20epsilon,1). Direct arithmetic gives
 K D w <=(1+20t)w,
provided t<=z/20, and K e11=(t,epsilon,epsilon,1)<=w. In detail the00/11 ratios are1+19t+(20/z)t², the01 ratio1+t²/z, and the10 ratio1/10+zt+t/z. Hence

 Z_h <=(1+20t)^h,
 pair preimage <=t^-1 exp(c|d1-d2|)(1+20t)^h,
 c=log(10/9)<1/9.

No independence of the actual column preimages is assumed: this is a conditional positive sum bound after the inter-pair excess energies have been discarded. The unpaired column retains the already proved bound exp(h epsilon).

## 2. Remaining height partition, including endpoints
The sorted height energy is
 E_theta(d)=2theta TV(d)-2theta(d1+dm)+2phi sum d_i.
The pair factors contribute at most exp(c TV(d)), so
 E_theta(d)-c TV(d)
 = E_(theta-c/2)(d)-c(d1+dm).
Charge the last endpoint factor by exp(2ch), rather than dropping it. Apply the inherited exact height-walk bound at theta_eff=theta-c/2. Its uniform-height denominator is
 delta_eff=2phi m-4theta_eff=8/R+2c>0.
With q=exp(-2phi), this yields

 Q_mh <= t^-R (1+20t)^(Rh) exp(h epsilon+2ch)
          *m/(1-exp(-delta_eff))*P(q)^2*coth(theta_eff)^(m-1),
 P(q)=product_(j>=1)(1-q^j)^(-1).

The retained true thermal pressure now scales as20Rh exp(-16), rather than the previous mh exp(-8), at the cost of a paid16R prefactor and the endpoint penalty2ch. This is a bound, not a claim of optimal pressure.

Safe rational estimates give

 log Q <=16R+20Rh/8880400+h/2980+2h/9
          +log[m(1+R/8)]+5R/12+2m/2681.

Here exp8>2980, epsilon_eff=exp(-2theta_eff)=(10/9)epsilon<1/2682, logcoth(theta_eff)<=2/2681, and the partition-function integral bound uses pi²<10. The small positive delta_eff is paid by1+R/8.

## 3. Sharper fixed-full-column continuation
The prior full-column transport uses a fixed axial wall of length L, a moving reference wall of length at most L+2, and ordinary unmarked-wall pressure. Replace its crude3^L or4^L selected-wall count by a standard axial displacement tilt, without changing the native path.

Let u=999/1000. Weight east/west steps by epsilon, north byu and south byepsilon²/u. Their sum
 z_axis=2epsilon+u+epsilon²/u <1-1/4000.
Every physical walk of axial displacement(0,L) has tilted weight(epsilon/u)^(-L) times its original Peierls weight. Summing ALL walks (including invalid/backtracking ones) is a positive overcount, so the selected moving wall has activity at most
 100n (epsilon/u)^L /(1-z_axis).
Multiplying by reference energy exp(8(L+2)) cancels epsilon^L and gives

 J_line <=400000n exp(16+L/999+n/6553710000).

Other thermal and essential loops remain in the ordinary full-wall pressure. The displaced wall's canonical root/orientation is included in100n; no free second boundary or hidden source law is used.

## 4. Original-source join and finite receipts
Use the independently reviewed critical solid-anchor join: an actual plus segment of length m=2R+1 grows to a full band, then the fixed-full-column native flow reaches ORIGINAL B. Terminal arrival weights satisfy nu<=Q_mh w, not a Gibbs reset. The stages use disjoint physical coordinates and the global bound is

 N_anchor <=4n² Q_mh J_line C_kappa.

All original A, kappa, capacity, rates, voltage and target are unchanged. This is a source occupation certificate, not a full mean acquisition algorithm.

check.py certifies the transfer witness, the axial tilt denominator, and every finite scalar by rational arithmetic/Taylor bounds. Proposed negative exponents at R80,200,1000,10000 are14,410,3180,33296. Use the stronger previous anchor bounds at the first three instances; the potential new advance is the formerly vacuous R10000 case. These values remain conditional on independent review of the paired-preimage, endpoint, and continuation interfaces.

## Independent review and executed diagnostics
Bridge independently reconstructed and passed the full derivation in BRIDGE_REVIEW.md: pair fixed-count identity and t^-1 factor; positive transfer witness; height-TV and endpoint cost; selected axial-wall tilt with all remaining loop pressure; partial-row auxiliary boundary relaxation and terminal source-density join. It reran the exact R10000 exponent33296. No frozen artifact was modified.

pair_check.py/json independently enumerates all4^h two-column words through h7 at rational epsilon1/10 (inside the witness's valid range), verifies the exact transfer/fugacity identity and every fixed-count bound. These checks support, but do not replace, the symbolic proof.

The finite R10000 anchor estimate can therefore be combined with already reviewed no-anchor minus-sea/plus-background exponents256367/104428, paying three branches to obtain no-essential outsideF occupation/ZA<=exp(-33294). This is a new finite-sector estimate only; the bound still contains a genuine positive quadratic-in-R pressure term and does not prove the desired fixed-temperature uniform growing-R algorithm. The original capacity-acquisition obligation is unchanged.
