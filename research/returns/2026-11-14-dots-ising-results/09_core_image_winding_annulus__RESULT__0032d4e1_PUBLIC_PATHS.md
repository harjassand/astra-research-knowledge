# Actual-voltage suppression for a thermal winding annulus

Candidate constructive topology extension of the embedded-square flow. This covers a specified genuinely winding family, not all winding configurations or total residence. It uses the existing finite capacity certificate and native clock unchanged.

## Source family with no unproved annular Peierls theorem
Use theta=4, phi=4/R, integer R>=80, L>=8R, n=L², actual core A=C_r with r+2<=R/3 and r<L/4. Let D be the full periodic annulus of columns 0,...,2R-1, all L rows. Then |D|=2RL and its PHYSICAL perimeter is 2L. Let S be the four full columns -1,0,2R-1,2R. Its size is4L. Define X to be core states with all S minus and Nplus(D)<|D|/2, and define G={x XOR D:x in X}. Every G state has two plus boundary loops, two minus exterior collar loops, positive annular magnetization, and small thermal minus holes inherited by complementing the core interior. Its exterior is the actual r-box thermal gas. This definition intentionally avoids claiming every positive-interior winding state is covered.

S separates interior and exterior even with the fixed nearest-diagonal augmentation. Core constraints factor across its pinned columns. Conditional on a fixed interior pattern, the exterior is precisely the r-core gas with fixed minus boundary pins, not a Gibbs approximation to the entrance current.

Because boundary spins of x on both sides are minus,
 w(x XOR D)/w(x)=exp[-2theta(2L)+2phi(2RL)-4phi Nplus(D)]
                =exp[-4phi Nplus(D)]<=1.
Thus Z_G<=Z_A with no contour count, hole-normalizer or extensive entropy penalty.

## Physical bit-preserving path
From y in G, flip exterior sites one column at a time in cyclic order, starting next to one annulus boundary, listing each column consecutively around the periodic row direction. Stop at the FIRST B={M>=0} visit. Interior D is never changed. Since M_D(y)>0, flipping the entire exterior ends at magnetization M_D-M_outside>0 whenever the initial state was outside B.

For every exterior prefix F, physical boundary counting gives
 P(F)-2 times(number of bonds from F into D) <=2.
For a partial first column this is the two row-end bonds; for a complete strip plus partial next column it is again at most two. At the last column the second old annulus interface only improves the inequality. Every F-D bond initially has product minus one, thanks to the collar. Other boundary products are at most one. Consequently
 log[w(y)/w(y XOR F)] <=4theta-2phi|F|+4phi Nplus_y(F).

The fixed-minus-boundary r-core Peierls/field-tilt estimate is the same core estimate as the capacity-lower theorem: for exterior fields up to3phi, all filled-component flips stay off the boundary pins and preserve r-box constraints. It gives
 E exp(4phi Nplus(F)) <=exp(4phi rho_bar |F|), rho_bar=1/100000.
Pinned exterior spins contribute zero. The inequality survives averaging over all retained interior patterns, because they do not alter the exterior conditional law. Therefore every prefix weight ratio has expectation at most exp(4theta).

For this fixed annulus, an edge's flipped site identifies its unique prefix; each orientation reconstructs at most one source by XOR. As in the existing thermal-flow proof, the unnormalized flow with divergence w on G minus B and sinks in B has
 E(F_D)<=2n exp(4theta) Z_G<=2n exp(16) Z_A.
No physical pin-survival event is imposed. The analytical paths use original native edges and their exact resistances 1/w(z)+1/w(z^i).

## Actual source-voltage occupation
Let v be the original soft-core voltage and C_kappa its original source capacity. Summation by parts and Cauchy on native edges give
 N_G=sum_(G minus B) w v <=sqrt[C_kappa E(F_D)],
 N_G/Z_A <=sqrt[(C_kappa/Z_A) 2n exp(16)].
This is a statement about original voltage, not a reflected or annulus-specific replacement voltage. It does not substitute Gibbs for actual entrance current.

## Direct mass comparison on the SAME non-target set
For original-field core A, its contour exponent is at least(11/6)theta>=22/3 because r+2<=R/3. With q=1/300>4exp(-22/3), the inherited anchored contour sum is
 8 sum_(p>=4)(2p+3)^2q^p=3610627/30072261375000<rho=1/8000000.
Hence each core site is plus with probability at most rho. Union bound on S, Markov on Nplus(D), and exp(-tN)>=1-tN yield
 Z_G/Z_A >=1-4L rho-2rho-4phi rho(2RL)
           =1-36L rho-2rho.
Because |D|<=n/4, an image in B requires at least n/4 original exterior plus spins. Markov bounds that lost core probability by4rho; its image/core weight ratio is<=1. Thus
 Z_(G minus B)/Z_A >=1-36L rho-6rho.
This lower is useful only when positive. It makes the strongest direct v<=1 mass comparison explicit.

## Exact finite scalar receipts
check.py uses exact rational series and finite exponential Taylor lower bounds. Substituting the independently acquired optimized-cut capacity certificate at L=8R gives:
R80,r5: mass lower .99711925, occupation upper exp(-759).
R200,r5: mass lower .99279925, occupation upper exp(-2052).
R1000,r6: mass lower .96399925, occupation upper exp(-10733).
R10000,r7: mass lower .63999925, occupation upper exp(-108620).
These are analytic certificates, not simulations of those tori. The finite inequalities inherit the capacity proof's geometric interfaces.

## Exact limits
One fixed winding annulus is covered. Taking a finite union of translated/oriented annuli costs multiplicity unless separately controlled. Arbitrary rough winding interfaces, several macroscopic exterior companions, and interior defects not obtained from the original core remain excluded. This is a genuine suppression relative to nonrare Gibbs mass in a topologically new sector, not total high-mass occupation, an exit-time theorem, a novel general method, or the North Star.

## Location-free corollary
Let G_union be the union over all L translations and both axis orientations of the width2R source family. Positivity of wv gives N_union<=sum_D N_D, regardless of overlaps. Thus
 N_union/ZA <=2L sqrt[(C_kappa/ZA) 2n exp(16)].
This removes a prescribed location/orientation with only the explicit2L factor; it still does not include rough or variable-width winding domains. For R80,L640 the upper is exp(-751), since1280<exp(8); for R1000,L8000 it is exp(-10723), since16000<exp(10). Its Gibbs-mass lower is at least that of any one annulus. These two exponential comparisons are deliberately rounded conservatively.
