# Independent mathematical challenge of the assembled killed-congestion argument

## Verdict and scope
I found no additional missing state class or exponential factor in the CURRENT phase-summed full-history construction, conditional on the supplied directed magnetic-moment/strip certificates being valid as recorded. The earlier isolated-energy-rise argument would have been insufficient; the present weighted preimage interfaces address that issue. This is a detailed independent proof review plus finite tests, not machine-checked formal verification or an independent rerun of every large moment table.

One formal correction was requested and accepted by source: define load with edge-occurrence multiplicity, or explicitly loop-erase paths. Phase-summed load bounds already pay occurrences, so no extra numerical factor is needed.

## 1. State coverage and native paths
For every nonempty below-majority state, deterministic original-component exploration either exhausts a contractible small component (erase it), or reaches a lifted span400 (grow). A winding component cannot exhaust while remaining in a lifted box with both spans<400<L/2; this prevents a missing winding class. Earlier erased components are ORIGINAL components, not newly merged residual components.

The bootstrap explored prefix is a connected subset of ORIGINAL spins inside overwriteU and spans bbox(U). During prewrap growth the original seed still spans400 columns but need not span the current height; the marked-strip bound uses precisely that weaker property. During cylinder growth all subsets are counted, so no topology restriction is silently retained.

Native additions and deletions are single flips. No-op additions merely update bookkeeping. First majority is checked after each actual addition, and all-minus after deletion. Before majority a full-height cylinder of widthk obeys kL<n/2, giving k<=799; its enclosing next-column width is<=800. Deletions≤n and additions≤n give length≤2n.

## 2. Inverse reconstruction and erased histories
At a growth edge choose the PRE-FLIP current state z and its geometric record U. Given S=(X\T)∩U and the FULL earlier erased original-component collectionT,

 X=(z\U)∪S∪T.

This is an injection: no original seed/residual labels beyond these data are required to recover X. T can cross U. Factor w(X)=w(T)w(X\T) first, using original-component nonadjacency; then compare X\T to z with their common exterior. Only afterwards discard compatibility in the T gas. Splitting T at U is invalid and has an explicit exp16 counterexample in RECORD_ENERGY_CHECK.md.

At erasure edges, upper-deletedU, current-row-deletedD and wholeT reconstruct X=eta∪U∪D∪T. The active residual need not be guessed among current components. The wire is an isolated-active comparison, not an equality of full-state wire energies. This distinction was tested against1220 actual finite companion-contact cases.

## 3. Record multiplicities
Bootstrap records: physical anchor n, two side lengths≤L,8 extension directions, witness offset≤L, progress≤2L yield≤16n³. Prewrap and cylinder records use anchor, orientation, length/width and active prefix, each≤4n². A common10n⁴ bound safely dominates these at n=2560000. The marked prewrap vertical root count1601 is separately present in the strip certificate; it is not silently removed. Multiplying common record count by path length gives20n⁵, log≈76.7734<80.

A pre-flip growth denominator uses the corresponding pre-flip overwrite shape; the quoted partial-shape energy bounds hold at that stage. Deletion uses its pre-flip state. Cross-phase contributions to the SAME undirected edge are added. No disjoint-support assumption is required.

## 4. Outer boundary and entropy interfaces
An allowed augmented component is a connected union of closed unit squares. In the plane, each physical outer boundary edge is incident to exactly one occupied cell and the unbounded empty face. Every such edge occurs once in the outer-face walk; it cannot be a graph bridge because it belongs to an occupied cell's four-edge cycle. Thus the outer word is nonbacktracking even when it revisits vertices. A proper rotational period would imply zero displacement over one period and repeat a physical edge, impossible. Therefore P distinct rooted words justify the /P factor in the fixed-bbox hull bound. The global n translation factor is removed ONLY because the rectangle anchor is fixed and paid by records.

Raw geometric filling preserves the bounding box; its signed-area word reconstructs filled area. Hole boundaries and remaining components must retain their orientation/area factorization. Counting all compatible positive/negative canonical loops independently overcounts, rather than loses, actual configurations. Vertex-touching and nested components do not create a missing shape class. This counting argument does not require replacing fixed-NE components by a different dynamics/connectivity convention.

Reviewed quantitative scopes:
- Hull K<878: all even lengths through1900 plus complete higher-perimeter tail, all400×400 aspect ratios; fixed anchor only. Internal holes paid separately.
- Erasure:80200 width/left-anchor choices,400 wired heights, row-run sumexp32(1+exp−8)^401; full earlier-component gas. Log load<944.
- Strip: W<=399 uses undiscounted resolvent; W400 removes the discount throughP12000 and pays the full remaining tail. Marked log190.555783 includes1601 vertical roots. Unmarked outer gas .288671 and negative-cycle gas .000008311 remain paid. No occupation/perimeter cutoff is reused as a uniform restriction.
- Final wrap row: compare to the OPEN strip through completion. The seam identity adds16[B(U)−B(S)]>=0 to the deletion energy, so opening is conservative. Comparing prematurely to the full cylinder would lose an unbudgeted~6400 factor and is not done.
- Cylinder: the full transfer partition includes empty/multi-interval rows, holes and winding sets. Width400..800 gives D<=1; PSD trace bound yields log<446. Partial-column comparison pays<80. Above-majority states may be counted in this upper sum, but actual paths still stop at first majority.

## 5. Poincare and physical-time constants
With occurrence multiplicity m_e(γ), define
 rho=max_e c_e^{-1} sum_x w_x |γ_x| m_e(γ_x).
Telescoping, Cauchy–Schwarz and f=0 on{a}∪B give sum_D w f²<=rho sum_undirected c(df)². This Dirichlet form is exactly that of native per-site heat-bath rates. There is neither an extra factor1/n nor a lost factor2 from directed versus undirected edges.

The killed gap is≥1/rho. Hence survival≤min(1,sqrt(Z_D/w_x)exp(−t/rho)), and mean≤rho[1+.5log(Z_D/w_x)]. Since E_x<=16n and E_y>=−.02n onD,
 log(Z_D/w_x)<=n(log2+16.02), mean<2.2×10^7rho.

The supplied phase loads give rho<exp944+exp992+exp305+exp624<exp994<exp1000, subject to all above certificates. This fits the updated source sufficient target rho<=10^446. The original box63 target10^82 is obsolete and must not be reused.

## 6. Independent finite full-chain check
`test_killed_congestion.py` builds the entire255-state killed3×3 native chain at finite test energy .8P−.04A and scaled path threshold2. It computes actual occurrence-counted canonical loads, the symmetric killed operator, its lowest eigenvalue and exact mean hitting times. Observed rho59.9079, gap .573801 versus required1/rho .0166923; all exact means obey the spectral bound. Maximum mean2.13188 versus bound337.831. This confirms clock/convention implementation on a complete finite example, NOT the R200 entropy constants.

## Remaining reporting discipline
The conclusion concerns a uniform killed-duration bound and the resulting occupation/numerator control. It does not by itself give a tight capacity, a completed rare-event sampler, a civilization-level invention, or an independently validated full physical prediction. Large numerical certificates and the source renewal transfer should be identified explicitly when assembling the final theorem.
