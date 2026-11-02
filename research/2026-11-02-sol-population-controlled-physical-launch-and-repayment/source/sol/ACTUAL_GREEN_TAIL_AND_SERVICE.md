# Actual killed-Green landing tails and a nonlinear service operation

Author derivation. These are complete local operations with their actual input/output contracts, not a global recurrence proof. No actual trajectory is replaced by an equilibrium fiber.

## 1. A reference-weight identity controls actual landings

For the diagnostic's conservative pair, use physical fiber index k with x(k)=x(0)+kw. Its genuine forward/backward rates satisfy the EXACT edge balance identity with the positive reference weight

    w(k)=2^k / product_i x_i(k)!.

This identity is used algebraically, not as a law of the input or of a surviving trajectory. Add ALL noncore hazards h(k), including the constant total zero-source hazard2, and put G=(-Q_core+diag h)^(-1). Diagonal killing preserves the exact weighted symmetry

    w(i)G(i,j)=w(j)G(j,i).                                   (G1)

Every row sum of G is an actual mean exit time <=1/2. Thus

    G(i,j)<=w(j)/(2w(i)).                                    (G2)

For any set B of exit locations, the COMPLETE actual exit law obeys

    P_i(exit location in B)
       <=[1/(2w(i))] sum_(j in B) w(j)h(j).                  (G3)

If -log w(j)>=-log w(i)+a on B, (G3) is <=|B|h_max exp(-a)/2. Here |B| and h_max have explicit polynomial count bounds from the fixed raw list. A linear-in-population reference barrier therefore gives a paid exponentially small cold landing probability, with its actual source/landing weight. No uniform mixing gap or conditional independence is used. It is NOT a uniform assertion from arbitrary high-energy entries; the barrier separation must actually hold at the input.

## 2. Uniform actual-time service from every fiber composition

Fix actual A=2,D=1 until the first noncore event. Write S=B+E and suppose

    |B-C|<=R, |E-F|<=R,
    S>=max(64(R+1),96).

The conservative rates are f=4(B)_2(C)_2 and g=2(E)_2(F)_2. The desired noncore service is I2 with h_high=2BC. ALL competing noncore hazards total h_low=2+2B+E<=5S. The invariant S and the two differences stay fixed throughout this entire actual core episode.

Let u(B)=1/(B+1). Direct genuine generator differences give

    L_core u <=8C^2 -4(E)_2(F)_2/[(B+1)(B+3)].               (G4)

At B=0 or1 the absent forward channel is simply omitted; the displayed upper bound remains valid. For B<=S/16, the size assumptions give C<=S/8, E,F>=S/2 and (B+1)(B+3)<=S^2/64, hence L_core u<=-S^2. For B>=S/16, C>=S/32, so h_high>=S^2/256, while the positive part of L_core u is <=32S^2.

Set epsilon=1/16384 and

    F_T(B)=16384/S^2 *[1+epsilon/(B+1)].

Then on EVERY feasible physical fiber state

    (-L_core+h_high+h_low)F_T>=1.                           (G5)

Indeed the low-B part is >=16384 epsilon=1; on the other part it is >=16384(1/256-32epsilon)>1. The positive killed inverse therefore proves, at the SAME first noncore stop,

    E sigma<=16385/S^2,
    P(first noncore channel is not I2)<=81925/S.              (G6)

The bounds hold from arbitrary fiber composition, including the cold endpoint. They preserve every competing source, the physical clock and its actual output. They do not require finite stationary activity. A first exit can still be neutral or positive at the global receiver; (G6) is a proved source-service operation, not a recurrence conclusion.

## 3. Compatible receiving values and the remaining joint sign

For each source s, Phi_L(x(k)-s) is independent of the enabled exit index k. Thus (G1)-(G6) can be used with the exact source-indexed receivers of the quotient construction, while the complete joint law is retained whenever later activation depends on the actual entry composition. The finite-horizon feedback implementation does precisely that.

The outstanding operation is to pay genuine rare repeated-source loans across successive normalizations and cold boundary entries at this SAME global candidate, or replace it. The source probability bound and the Green inverse do not by themselves make that global return drift negative.
