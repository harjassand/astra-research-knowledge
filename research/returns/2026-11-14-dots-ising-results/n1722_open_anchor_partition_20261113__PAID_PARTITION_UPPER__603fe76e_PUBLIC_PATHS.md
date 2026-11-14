# Paid open-anchor partition upper and a half-row witness

Candidate constructive extension, under independent review. No full-residence claim.

## 1. Exact partition model
F is an m-by-h rectangle, bottom boundary plus, the other three sides minus. Let Q(m,h)=Z_F/w(allplus_F). Put t=exp(-2theta), q=exp(-2phi), delta=2phi*m-4theta>0. Then

 Q(m,h) <= exp(mh t) * [m/(1-exp(-delta))]
             * P(q)^2 * ((1+t)/(1-t))^(m-1),              (A)
 P(q)=product_(j>=1)(1-q^j)^(-1).

The bound pays both interface roughness and bulk rearrangements. It is not entropy-free.

## 2. Sort each minus column without changing its area
Let d_i be the number of minus sites in column i. Compress them against the top minus boundary. Horizontal disagreement between two columns is at least|d_i-d_(i+1)|, with equality after compression. Left/right boundary terms and field depend only on d_1,d_m and sum d_i.

A column with d missing sites and b minus blocks NOT touching the top has vertical energy excess4theta*b over its compressed version. The number of height-h binary columns with these statistics is
 binom(d,b) binom(h-d,b).
Thus its weighted preimage sum is
 U(h,d)=sum_b binom(d,b)binom(h-d,b) exp(-4theta*b)
       <=exp(2t sqrt[d(h-d)])<=exp(ht).
The first inequality follows from binom(k,b)<=k^b/b! and
 sum_b x^b/(b!)²<=exp(2sqrt x).
Multiplying m columns pays exp(mht). No source pattern is discarded and no column independence in the original Gibbs measure is asserted: this is a positive overcount after the horizontal energy inequality.

## 3. Bound the compressed height model
Its exact relative energy is
 E(d)=2theta sum_(i=1)^(m-1)|d_i-d_(i+1)|
       -2theta(d_1+d_m)+2phi sum_i d_i.
Let a=min_i d_i and u_i=d_i-a. The uniform retreat costs delta*a. Select a minimum index j, paying at most m choices, and split u into two nonnegative height walks starting at0 and ending freely at the two sides.

For either outward walk z_0=0,...,z_l, the contribution is
 exp[-4theta Down(z)] q^(sum_(i=1)^l z_i),
where Down is the total downward variation. Define its future-minimum envelope
 b_i=min_(k>=i) z_k, e_i=z_i-b_i.
Then b is nondecreasing, e_0=e_l=0, and Down(e)=Down(z): a jump of b can occur only when e_i=0 and cannot contribute to a downward step. Areas add exactly.

Dropping the compatibility between b and e only increases the sum. The monotone envelope sum is at most P(q). For the nonnegative bridge, discard its favorable area factor. Since its upward and downward variations agree,
 exp[-4theta Down(e)]=t^(total variation of e).
The half-line kernel K(a,b)=t^|a-b| has row sums at most(1+t)/(1-t). Its length-l return sum is bounded by this row norm to power l. The two walks therefore contribute at most P(q)^2*((1+t)/(1-t))^(m-1). Finally sum a>=0 geometrically. This proves (A).

Using log P(q)<=pi²/(12phi),
 log Q <=mh exp(-2theta)+log[m/(1-exp(-delta))]
          +pi²/(6phi)+(m-1)log coth(theta).
The extensive pressure term is explicit; it prevents an unrestricted all-R claim at fixed temperature.

## 4. Actual paths from an open plus segment
Use L=8R, theta4, phi4/R. Set m=4R. Fix a row segment of m-1 consecutive plus sites. If necessary, add its adjacent endpoint to obtain a plus segment of lengthm; the source-weight pushforward is bounded by B0=1+exp(4theta), because that site has at least one fixed plus neighbor. The initial edge has congestion at most B0.

Then fill the m-by-(L-1) rectangle extending from this anchor, row by row, skipping original plus spins. Stop at first B. Once the rectangle and anchor are full they contain mL=n/2 plus sites, so completion is guaranteed independently of all other spins. All updates are native upward single-site flips.

At a fixed edge, original prefix spins are summed. Unknown boundary spins can be replaced by minus in each source/allplus-reference ratio, while the bottom anchor remains plus. If periodicity identifies the upper boundary with the same anchor, replacing ONLY its upper boundary incidences by minus still increases each ratio; this is an algebraic boundary relaxation, not a claimed physical spin configuration.

A partial last row can be enlarged to a full rectangle with the added sites forced minus in the numerator. Dropping that restriction enlarges the partition sum. Completing this reference row multiplies its weight by at most exp(2phi*m). Hence each endpoint ratio is at most exp(2phi*m) times the bound (A) at h=L-1. Both heatbath endpoints and the initial source pushforward are paid:

 K <=2 B0 exp(2phi*m) Q_bound(m,L-1).

The original-current coordinate-cut lemma gives N_fixedsegment<=n K C_kappa. There are at most2n row/column segment labels, paid by positivity:

 N_segments/C_kappa <=4n² B0 exp(2phi*m) Q_bound(m,L-1).    (B)

This set includes ALL non-target states with any contiguous plus segment of length4R-1 in a row or column. No exterior/core/collar restriction remains. It includes the previously supplied diagonal band counterexample, whose row runs have exactly4R-1 plus sites. It is not all high-mass states or all winding shapes.

## 5. Conservative finite arithmetic
At theta4,m4R,delta16, use t<1/2800, pi²<10, log coth4<2/2799 and1/(1-exp(-16))<2. Also B0<=2exp16. Then the multiplier in(B) has logarithm at most

 log(64n²R)+48+(2/175)R²+(5/12)R+8R/2799.

The finite same-clock capacity upper can be subtracted from this expression. The R² thermal pressure is retained. The supplied finite examples R80,200,1000 may pass; R10000 does not pass this bound and is not covered by its smallness certificate. The symbolic inequality(B) remains valid there but may be vacuous.

## Scope
This combines rearrangement, partition enumeration and current conservation. It is not a new physical dynamics, Gibbs entrance assumption, mixing theorem or full mean-exit-time solution. The pointwise partition proof and prefix/source accounting require independent review before any result is reported as established.
