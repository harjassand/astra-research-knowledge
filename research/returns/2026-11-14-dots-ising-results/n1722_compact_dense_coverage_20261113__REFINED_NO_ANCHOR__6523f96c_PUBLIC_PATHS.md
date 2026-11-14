# Refined no-anchor contour pressure, without a hole-size restriction

Candidate extension; independent reviews underway. Original Ising Gibbs weight, target B, voltage v, core A and capacity remain unchanged. Let m=2R+1 and E be the event that there is NO solid length-m horizontal or vertical plus segment anywhere on the torus.

## Exact run inequality
Every cyclic row and column has plus runs of length at most m-1=2R; a fully plus row/column would violate E. If P_x,P_y count the two directional disagreement bonds, then Nplus<=(m-1)P_x/2 and Nplus<=(m-1)P_y/2. Adding gives Nplus<=(m-1)Ptotal/4=R Ptotal/2. Thus

 w(x)/wminus=exp[-8Ptotal+(8/R)Nplus] <=exp(-4Ptotal).       (1)

This uses actual plus volume, not filled area. It holds with arbitrary thermal holes, multiple domains, and either background phase. It is stronger than the prior relaxed m-based run count.

## Exact short-loop count
For the actual deterministic physical-plus resolution, contraction of zero-energy dual edges sends each wall to a physical edge-simple nonbacktracking closed walk. Length4 walks are precisely the n unit dual plaquettes. Length6 walks are precisely the 2n rectangles of sides1 and2. A self-touching edge-simple closed walk needs at least8 edges. No orientation/root factor is needed for these two exact UNORIENTED loop counts; the physical disagreement collection determines spins up to ONE global sign. For lengths>=8 retain the conservative100n3^p count. The positive product bound therefore has pressure

 A(t)=n exp(-4t)+2n exp(-6t)+100n (3exp(-t))^8/(1-3exp(-t)). (2)

This fixes the earlier extremely loose p4 entropy factor. Invalid collections may be included as a positive overcount. The adaptive rule is deterministic; there is no independently chosen plaquette-pairing factor.

## Minus-sea outside F
If every physical plus component has a nonwinding embedded filled outer domain but the configuration is outside F, at least one actual outer contour has physical P>4sqrt5R>8.9R. Mark one such contour and apply(1), retaining all other loops through A(4). Since e4>54, q4=3exp(-4)<1/18,

 A4 <= n/54^4+2n/54^6+100n/(17*18^7),
 N_(E,minussea,outsideF)/ZA
 <=220n exp(A4) exp[-(2.89)*(8.9R)].                (3)

Here log18>2.89, ONE global phase factor2 and the marked contour root count are paid; 2*100/(1-1/18)<220. Neither a small-hole nor a single-droplet assumption remains. ZA>=wminus and v<=1 suffice.

## Plus-background candidate branch
For the remaining no-essential-wall plus-background topology, suppose all minus sites belong to nonwinding contractible minus components. Their actual total area H>n/2 because the source is outside B. For each component, physical isoperimetry gives area<=P_i²/16. Its boundary edges are disjoint from those of other minus components, so

 Ptotal=sum P_i >=4sqrt(H)>4sqrt(n/2)=16sqrt2 R.

No bound on the filled areas or number of holes is required. Tilt total perimeter by1/2 in(1), leaving loop tension7/2. Since exp(7/2)>33 and3/33=1/11,

 A35 <=n/33^4+2n/33^6+100n/(10*11^7),
 N_(E,plusbackground,Bc)/ZA <=2 exp(A35-8sqrt2 R).   (4)

The precise same-encoding topological premise is being checked independently. Do not use(4) for a phase with winding minus components without proving the relevant decomposition. The global phase factor2 is paid only once.

## Intended finite union and remaining obligations
Compute's independently reviewed solid critical-anchor native join yields occupation/ZA<=exp(-515),exp(-1521),exp(-4423) at R80,200,1000, respectively. Its R10000 bound is vacuous. If the no-essential topology dichotomy is verified, union of this anchor event and(3),(4) controls the original zero-essential sector OUTSIDE F at those three instances. The core and F\A contributions are NOT discarded; they remain in the exact original source identity. Capacity acquisition and a uniform growing-R polynomial theorem are still independent missing obligations. No full North Star or general exit-time estimator is claimed here.
