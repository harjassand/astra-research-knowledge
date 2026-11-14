# Full cylindrical relative partition bound

## Scope
A rectangular strip of width400<=w<=800 and periodic height L=1600, with minus spins just outside its two vertical sides. EVERY subset of the strip is included: empty rows, multiple intervals, arbitrary holes and winding configurations. Physical energy E=8P-.04A includes perimeter to the fixed minus exterior. Full strip energy E_full=(16-.04w)L.

## Transfer representation
Represent row y by subset S_y of {1,...,w}; r(S) is its number of nonempty contiguous plus runs, with r(empty)=0. Its horizontal boundary is2r(S). Therefore
 E-E_full=sum_y [16(r(S_y)-1)+.04(w-|S_y|)] +8 sum_y |S_y symmetricdifference S_(y+1)|,
with periodic y.
Define diagonal D_S=exp[-16(r(S)-1)-.04(w-|S|)] and K_ST=t^|S symmetricdifference T|, t=e^-8. The exact relative partition function is
 Z_rel=Tr[(D^(1/2) K D^(1/2))^L].
K is the w-fold tensor product of [[1,t],[t,1]], so is positive semidefinite and has operator norm (1+t)^w. For a nonempty row, r>=1 gives D<=1. For an empty row, D=e^(16-.04w)<=1 because w>=400. Thus ||D^(1/2) K D^(1/2)||<=(1+t)^w.

For the trace, drop only the nonnegative missing-area cost:
 TrD <= e^16 sum_S e^(-16r(S)).
Each row pattern is uniquely represented by its2r transition bonds among the w+1 bonds including fixed minus endpoints. Hence
 sum_S e^(-16r(S)) = sum_(k even) binom(w+1,k)t^k <=(1+t)^(w+1).
The transfer matrix is positive semidefinite, so Tr(T^L)<=||T||^(L-1)Tr(T), and Tr(T)=Tr(D). Consequently
 **Z_rel <= exp(16)*(1+exp(-8))^(wL+1).**
For w800,L1600, log Z_rel<446. An entirely rational looser certificate uses exp(-8)<1/2980 and log(1+x)<x, yielding log Z_rel<16+1280001/2980<446. Exact rational exp(8)>2980 follows from a finite Taylor partial sum (companion test).

## Preimage use and limitations
At a growth edge whose current plus region is this full strip, the exterior is unchanged and recoverable. Removing an interior plus adjacent to an exterior plus raises its relative energy by16 compared with minus exterior. Therefore arbitrary actual exterior plus spins only decrease the weighted preimage sum, and this isolated-cylinder bound is conservative.
A partially added column can be enclosed in widthw+1 cylinder. Its isolated energy is at most E(full widthw)+15.96. Relative to full widthw+1 cylinder this loses at most64+15.96=79.96 (since L*.04=64). Thus the same argument gives logpreimage <=446+79.96 for interior widths through800, before polynomial edge records.

This does NOT yet close the whole duration/congestion problem. Initial bootstrap filling and prewrap growth require separate reconstruction; path-record multiplicities and first-majority stopping must be retained. The cylinder partition bound itself sums all states and therefore also safely includes configurations above the actual stopping threshold, but that overcount cannot justify changing the stopping rule or an otherwise invalid path.
