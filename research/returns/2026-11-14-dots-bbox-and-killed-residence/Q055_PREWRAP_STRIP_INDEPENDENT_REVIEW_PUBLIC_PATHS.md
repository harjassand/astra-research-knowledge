# Independent review of the prewrap confined-walk bound

Reviewed flow's STRIP_WALK_BOUND.md and patched strip_walk_bound.py/json.

1. For an oriented y-closed contour, the product of horizontal e^-8 and vertical e^[-8±.04(x−W/2)] weights is exactly exp(−8P+.04 signed area). Centering cancels because net vertical displacement is zero. Summing vertical directions into the matrix diagonal and dropping vertical closure/simplicity is a positive overcount, not a dynamics model.
2. The rooted x-return walks that visit W have total weight R_0W²/R_WW. This follows by first hitting W and then an unrestricted return, or by subtracting the resolvent avoiding W. LDL elimination gives the positive product b^(2W)/(p_W product_{i<W}p_i²), avoiding cancellation.
3. Positive lower pivots imply I−T positive definite. Since T is symmetric and nonnegative, Perron–Frobenius gives spectral radius<1. The Neumann walk sum therefore converges.
4. Actual low-perimeter words pay λ^-12000. The high-perimeter outer-face tail uses area≤640000 and n-independent per-root raw direction count; adding it removes any assumption that original configurations have perimeter below the cutoff.
5. A marked width400 component in a fixed strip has a canonical outer-face root on the left boundary;1601 vertical records is conservative. Its holes and additional components are counted with separate positive/negative gases. Original intersections need not be connected. Raw face conventions, not unrelated graph-filled conventions, must be used.
6. I identified lower-logsum/discount accumulation and denominator rounding issues in the first script. Flow repaired these using downward accumulation before subtraction/division. The current scalar reports marked relative log183.177399 per root and190.555783 including vertical records; unmarked gas log.288671 and hole gas log8.311e−6. These bounds include the explicit full high-perimeter tail.

No remaining local resolvent/encoding objection was found. This review does not itself prove the global canonical-path record injection, source-residence theorem, or native practical sampling runtime.
