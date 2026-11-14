# Every configuration containing a full plus row or column

## Statement
Use the original torus, ferromagnetic rate-one heatbath, decreasing core A, target B={M>=0}, actual soft clock kappa and original voltage v. Let n=L², L>=8, theta>=4 and phi>=0. Let H be ALL non-target configurations containing at least one full plus row or full plus column. There are no interior/exterior core restrictions, collar restrictions, small-hole conditions, or Gibbs assumptions on the actual current.

Set q=4exp(-2theta)<1 and
 J=exp(4theta) *[100n4^L/(1-q)] *exp[100n q^4/(1-q)].
Then the construction below gives
 N_H=sum_H w(x)v(x)<=4nL J C_kappa.                    (1)
The contour/topology interface has been checked independently by fluid and compute; precise source/clock and finite capacity imports are unchanged.

At theta4, q<1/700 yields
 N_H/ZA <=404n²L exp(16)4^L exp[n/2397570000] (C_kappa/ZA).
The explicit L-dependent interface entropy and n-dependent thermal pressure are paid. This is not a bound uniform in arbitrary L/R.

## 1. Original voltage and coordinate current budgets
The original v(x) is the probability that the rate-kappa clock, accepted only when the chain lies in decreasing A, rings before actual B. Attractive heatbath with a shared clock couples ordered initial states, and implies v is decreasing. Thus every upward native edge e=(z,z^a) carries i_e=g_e(v(z)-v(z^a))>=0.

Kirchhoff on the cut{z:z_a=-} gives sum_(e flips a)i_e<=C_kappa: internal currents cancel and target drains subtract a nonnegative quantity. Direct source-target overlap does not invalidate this upper. This is the actual core clock, not a reset/restart model.

For any assigned upward paths from a source family to first B, weighted voltage telescoping gives
 N_family=sum_e i_e A_e,
 A_e=(1/w(z)+1/w(z^a)) sum_(sources using e)w(source).
Consequently A_e<=K pointwise implies N_family<=nK C_kappa.

## 2. One line and the first-B prefix
Fix one full plus column D. Visit all other columns in cyclic order starting to one side of D; within each column visit consecutive rows. Skip any already plus spin, otherwise flip it upward. Stop at the first B hit. D stays fixed. This defines genuine original native edges, though the actual random dynamics need not follow this analytical path.

At an edge whose site has order index k, the processed prefix F is exactly all earlier prescribed sites, including skipped sites. Those F spins are plus in the current configuration. Each original source pattern on F is summed in A_e; all other original bits are uniquely fixed by the edge. The index of the flipped site fixes F, so skipped-site counts add no labeling factor.

If k sites outside D have been processed, total magnetization is at least L+2k-(n-L)=2k+2L-n. Hence first B occurs by k=ceil((n-2L)/2). For L>=8 this is strictly before processing the last complete exterior column adjacent to D's opposite side. Both endpoints of every used edge therefore leave that last column unprocessed. The upper-endpoint analysis uses F union{a}, and enlarges the fiber by dropping the forced-original-minus condition at a.

## 3. Fixed-edge boundary comparison
For each assignment x_F, the ratio w(x_F,b)/w(plus_F,b) decreases when any unknown external boundary spin b_j changes from minus to plus: a neighboring x_i=minus contributes factor exp(-4theta), while x_i=plus contributes1. Replace all unknown exterior boundary spins by minus, preserving D plus, to upper-bound each term.

After this replacement we have an artificial torus with one full plus column D and a full unprocessed minus column on its opposite side. This is only a pointwise weight-ratio comparison. It does NOT impose a minus collar or a core law on the actual source. Arbitrary exterior macroscopic clusters are allowed before the comparison.

The field factor relative to allplus_F is exp(-2phi Nminus_F)<=1. Drop it BEFORE the zero-field contour overcount. No positive-field partition on an enlarged free region is silently substituted.

## 4. One fixed wall, one counted moving wall, all remaining thermal walls
Use the actual fixed zero-coupling triangulation. The interface between the full plus D column and the complete opposite minus column is a fixed noncontractible dual cycle of PHYSICAL length L. Remove its constant contribution. Every remaining artificial spin configuration has at least one additional noncontractible wall separating the other sides, of physical length at least L.

The processed prefix is full columns plus at most one contiguous partial column. Its allplus reference has total boundary length at most2L+2. After removing the fixed opposite cycle, its moving boundary has length at most L+2. Thus the ratio for any original prefix pattern is bounded by
 exp[2theta(L+2)] exp[-2theta P_remaining].

Choose one moving winding cycle deterministically. It is counted as a selected cycle of length s>=L. Every other wall, including internal thermal holes, extra winding cycles and nested islands, remains in the full wall set. The full set and the fixed plus phase in D determine the configuration, with no2^(number of regions) ambiguity.

A cycle of physical length s has total dual length at most2s: consecutive zero-coupling crossings cannot occur in the degree-three dual. Rooting an oriented physical edge and summing nonbacktracking walks gives the loose bound100n4^s for all cycles. Every physical cycle has s>=4. Dropping compatibility constraints only enlarges the positive sum:
 selected wall sum <=100n q^L/(1-q),
 other wall sets <=product_gamma(1+exp(-2theta P_gamma))
                 <=exp[100n q^4/(1-q)].
Multiplying by exp[2theta(L+2)] yields exactly J, because exp(2theta L)q^L=4^L. This is a FULL wall-set argument, not an outer-contour-only pressure estimate.

Each endpoint's preimage weight sum divided by that endpoint's weight is therefore at most J. Thus A_e<=2J and the fixed-line family has occupation at most2nJ C_kappa.

## 5. Pay every line label
There are2L row/column choices. Source families may overlap. Positivity, not independence or unique source decoding, gives N_H<=sum_lines N_line, hence equation(1).

## Finite certificates and strong same-set baseline
full_line_scalar.py/json use exact rational bounds and finite exponential Taylor lower sums, including exp(8)>2800 and log4<7/5. They combine equation(1) with the original optimized capacity certificates at L=8R and unchanged r/clock:

R80,r5: N_H/ZA<=exp(-596).
R200,r5: N_H/ZA<=exp(-1836).
R1000,r6: N_H/ZA<=exp(-10234).
R10000,r7: N_H/ZA<=exp(-105199).

H contains the earlier width2R core-image winding-annulus family outside B. Thus its SAME non-target Gibbs mass is at least .99711925,.99279925,.96399925,.63999925 timesZA, respectively. Direct v<=1 therefore does not yield the tiny occupation scale; the actual-current factor is essential.

## Checks and exact remaining gap
Fluid's ising_full_corridor_20261113/contours.py/json explicitly decomposed all256 binary4x4 corridors under the actual SW-NE triangulation, verifying the fixed winding cycle, a second moving winding cycle of physical length at leastL, and minimum remaining physical cycle length4. The analytic topological argument, not this finite enumeration, is the general proof interface. Compute independently checked the prefix stopping, boundary comparison, phase encoding and original-clock use.

The excluded set is configurations with NO completely plus row or column. That is not the same as 'no winding': a rough winding domain can avoid every straight line. This theorem does not cover that complementary occupation, prove where actual current concentrates, or close total native residence/exit time. It supplies a broader finite high-mass occupation certificate, not a claimed civilization-changing breakthrough or literature-novel general principle.
