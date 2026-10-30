# Majority-coordinate insertion: uniform joint-shell Green transport

Status: conditional theorem and the three finite certificates passed child adversarial review; see INDEPENDENT_MAJORITY_GREEN_AUDIT.md. The structural all-width extension and macroscopic physical-shift corollaries also passed the child check; see INDEPENDENT_UNIFORM_COLLAR_AUDIT.md. This strengthens polynomial shell comparison but is NOT a global recurrence theorem.

## Exact joint object
Use the killed joint-shell generator Q_R from JOINT_SHELL_FOREST_TRANSPORT.md: states (c,j), actual populations C=c and A=R+h_j-c; all within-shell reactions retained, all residual-changing reactions killed. Phase changes and conservative composition are coupled exactly. G_R=(-Q_R)^(-1) is the actual occupation kernel until first residual exit.

Assume finite phase width, bounded orders, and |Delta C|<=1 for EVERY retained R-preserving transition (with phase transitions row-local in the concrete application). The concrete network has these properties. Shell transience is earned by an enabled immigration path to killing, not assumed from global recurrence.

## Insertion and the unmatched interior row
Choose m=floor(R/2), or more generally m/R in a fixed compact subinterval of (0,1). Remove rows c=m,m+1 from shell R. Remove rows c=m,m+1,m+2 from shell R+1. The retained sets correspond bijectively under

    phi(c,j)=(c,j),       c<=m-1,
    phi(c,j)=(c+1,j),     c>=m+2.

Below the cut, A increases by one and is of order R. Above it, C increases by one and is of order R. The other population is unchanged, so all zero-rate/enabling patterns on retained states are preserved, including the true low-A and low-C endpoints.

For every original retained rate lambda,

    lambda_(R+1)(phi x,phi y) / lambda_R(x,y) = 1+O(1/R),

uniformly over retained states and enabled edges. This follows directly from falling-factorial ratios in the increased macroscopic coordinate. Positive sums and killing rates obey the same estimate.

## The finite interface obligation
Eliminate the removed rows EXACTLY in each shell. This is a finite positive Schur-complement computation. It is enough to verify:
1. the eliminated block reaches retained states or killing;
2. the effective off-diagonal/killing supports agree after phi;
3. corresponding nonzero effective rates have the SAME asymptotic power of R.

All three are finite algebra/graph tests, not a Lyapunov assumption. The leading coefficients are strictly positive. Since all counts in the interface are proportional to R, these coefficients are continuous positive functions of m/R. On a fixed compact subinterval, their ratios are uniformly bounded above and below. Thus every modified boundary-row rate has a constant-factor comparison. There are only a fixed number of such rows.

## Uniform forest comparison theorem
Apply the positive directed-forest formulas to each exact Schur complement. A forest uses at most one outgoing edge per state. There are O(R) unchanged rows, each contributing 1+O(1/R), and O(1) boundary rows contributing fixed constant factors. Consequently every corresponding forest monomial has a ratio in [C^-1,C], uniformly in R. The same holds after summing positive monomials, for both determinant and nonzero Green numerator. Therefore

    C^-1 G_R(x,y) <= G_(R+1)(phi x,phi y) <= C G_R(x,y)

for retained x,y, with C independent of R. Zero entries match by the equal-support condition. Full Green entries restricted to retained states equal these Schur-complement inverse entries exactly.

This is valid even with multiple composition wells and arbitrarily slow shell mixing. It does not compare a mixture of frozen phase stationary laws.

## Exact finite algebra for the hard coupled network
For the rank-three network and exact offsets with K=4,8,12, the removed two-row/three-row blocks have identical effective supports and degrees. check_majority_collar_degrees.py records the computation in MAJORITY_COLLAR_DEGREES.json: respectively 4,100,324 nonzero effective rates.

The computation uses rate-form Schur elimination, never signed determinants. Each edge carries its leading exponent d in R. When eliminating v,

    d_out(v)=max_w d_vw,
    d_new(i,j)=max(d_old(i,j), d_iv+d_vj-d_out(v)), i!=j.

Self-loops are discarded. This is exact leading-degree arithmetic because every effective rate is a sum/product/quotient of strictly positive rates, with no subtraction or leading cancellation. Immigration has degree0, activation degree1, clearing and fast conversion degree3. In the interior all original enabling conditions are satisfied; coefficients do not affect degrees. Endpoint rows are retained under the majority map and do not enter this finite calculation.

Every removed state can reach killing by immigration, or leave the removed block by a fast move. Hence the eliminated blocks are transient. The JSON is a finite exact certificate for all sufficiently large R, not a numerical eigenvalue extrapolation. The general theorem applies to any other fixed-width joint shell passing the same explicit support and degree tests.

## Physical-shift corollary on macroscopic composition regions
Fix epsilon>0. If both queried states have A>=epsilon R, choose the cut m near (1−epsilon/2)R, above both C coordinates for large R. Then phi leaves their C coordinates unchanged and adds one A. The same finite support/degree test is valid at this cut: positive leading coefficients vary continuously with m/R, while degrees and support do not change. Hence

    G_(R+1)((c_x,j_x),(c_y,j_y)) is comparable to G_R((c_x,j_x),(c_y,j_y))

with a constant depending on epsilon but not R. This is a genuine physical fixed-C shift on that macroscopic region. The analogous fixed-A comparison holds when both C counts are at least epsilon R, by placing the cut below both queries. The constant is not claimed uniform as epsilon tends to zero. Mesoscopic composition sectors remain an explicit gap.

## Precise remaining limitations
- The transport moves C as well as R on half the shell. The corollary gives physical fixed-C shifts only in a macroscopic region; it does not give the shifts required uniformly by every connector reaction.
- The bound is a constant, NOT 1+O(1/R). One may not silently absorb it into a small commutator.
- Queries in the finitely many removed rows are not covered by the displayed inequality. They can be treated with additional finite Schur reconstruction, but that extension is not claimed here.
- Residual-changing excursions and their feedback into neighboring shells remain to be controlled. This theorem compares exact killed-shell Green kernels; it does not prove their global forcing contraction.

The structural extension in UNIFORM_FAST_COLLAR_DEGREE_THEOREM.md replaces the three fixture checks by a proof for arbitrary fixed K in the hard network, now checked separately in INDEPENDENT_UNIFORM_COLLAR_AUDIT.md.
