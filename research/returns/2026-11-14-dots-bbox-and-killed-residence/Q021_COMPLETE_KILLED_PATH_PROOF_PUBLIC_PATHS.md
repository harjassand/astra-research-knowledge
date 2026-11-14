# Native killed-chain path certificate: complete analytic assembly

## 1. Model and claimed conclusion

On the1600-by1600 square torus let n=2560000, S the plus-spin set, P(S) its physical nearest-neighbor edge perimeter, and
 E(S)=8P(S)-|S|/25, w(S)=exp(-E(S)).
The all-minus state a has w(a)=1. Kill on K={a} union B, where B={|S|>=n/2}. On D={0<|S|<n/2}, the ORIGINAL per-site heat-bath flip rate is q(S,S')=1/[1+exp(E(S')-E(S))]; conductance c(S,S')=w(S)q(S,S') is symmetric. No1/n clock rescaling is used.

The assembled bound is rho<exp(1000) for native killed canonical-path congestion, and hence a uniform mean killing-time bound M<22000000 exp(1000). The proof uses the explicitly stated finite contour certificates in Section2. Its analytic reconstruction does not require a low-perimeter restriction on initial states, a restricted thermal background, or a change of target. Numerical certificate files are part of the proof inputs and must accompany this text; this is not a claim to have analytically evaluated their large finite sums by hand.

## 2. Static counting certificates and precise scopes

### 2.1 Small-box hull and gas
For a fixed contractible bbox R of cell dimensions W,H<=400, the sum of weights of filled raw geometric hulls F with bbox exactly R, relative to w(R), is at most exp(878). The sharper directed value is877.768275. This is an unrooted, fixed-bbox count; it includes vertex-touching outer-face walks.

Certificate construction: put s=W+H,A=WH. For each even P>=2s and each rational r<exp(.02), enumerate all rooted nonbacktracking closed square words with weight r^(twice signed area), giving upward coefficient Z_P(r). A physical outer-face walk of length P gives P distinct rooted encodings; a proper rotational period would repeat an edge. Its area is at most A. Therefore the required relative sum is bounded by
 sum_(P even>=2s) exp(16s-8P) min_r [r^(-2A) Z_P(r)/P].
Include r=1 with Z_P<=4*3^(P-1), and the complete geometric tail beyond the saved moments. Directed computation of this explicit finite sum plus tail is `flow_resume_20261114/hull_entropy_bound.py/json`, with the exact saved moment tables and contour interface described in HULL_ENTROPY_BOUND.md. No Ferrers-corner assumption is used.

Raw-face encoding justification: represent occupied unit squares by the plane graph of ALL their grid edges, including internal edges. Augmented-connected occupied squares form a connected geometric graph because a diagonal adjacency shares a vertex. Every graph edge belongs to an occupied square cycle, so there are no bridge edges. The outer-face walk therefore traverses each of its boundary edges once, may revisit vertices, and has no immediate backtrack. Its winding reconstructs the filled outer hull. Bounded EMPTY faces (not the occupied unit-square faces) reconstruct the holes. Physical perimeter and area factor exactly as E(S)=E(hull)+sum_h[8P(hole)+|hole|/25]. Independent orientation-coded negative loops may also overcount nested patterns; their nonnegative costs and compatibility removal preserve an upper bound.

Internal minus boundaries contribute an extra log factor below0.000001: root each boundary among at most401² vertices, use4^P words of length P>=4, and discard nonpositive minus-area contribution and compatibility. The sum is bounded by exp[401² sum_(P>=4)(4exp(-8))^P]. Physical area/perimeter decomposition is exact for raw outer and bounded empty faces; these auxiliary faces must not be confused with the original fixed-diagonal graph-fill convention.

The standalone gas of any collection of original augmented components each fitting a400-square has log normalizer below0.000001. This follows from the source's stronger650-square certificate (`CORE650_OCCUPATION.md` and core650_occupation.py/json). Different original components have disjoint physical boundary interactions because physical edges belong to augmented connectivity. These gases count full configurations, not merely one droplet.

### 2.2 Critical-width strip marked mass
Inside any OPEN400-by-h rectangle, h<=1600, the isolated Gibbs mass of subsets containing an augmented component spanning all400 columns, divided by exp(-6400), is at most exp(191), times an unmarked/negative-loop gas whose log is below0.289. The vertical-root multiplicity1601 is ALREADY included in191. Every full400-by-h rectangle has E=6400.

Certificate construction: for width W, track a boundary word's x-coordinate0..W, assign horizontal weight exp(-8), vertical weights exp[-8 ± (x-W/2)/25]. For y-closed words their product is exp(-8P+A/25). Dropping y-closure, nonbacktracking and simplicity only increases the sum. The resulting symmetric nonnegative tridiagonal matrix T has off-diagonal lambda exp(-8), diagonal lambda exp(-8)[exp((2x-W)/50)+exp(-(2x-W)/50)]. Use lambda=1 for W<=399 and lambda=9999/10000 for W400.

Positive directed lower LDL pivots of I-T prove convergence of R=(I-T)^(-1). The weight of x-closed words from0 visiting W is R_0W²/R_WW=b^(2W)/(p_W product_(i<W)p_i²). For W400, remove the discount only for P<=12000 by multiplying lambda^-12000. For longer actual hulls use area<=640000 and the complete per-root tail exp(25600) sum_(P>12000)(4exp(-8))^P. Thus there is NO initial-state perimeter assumption. Marked fixed-root relative log is183.177399; adding1601 roots gives190.555783<191.

Unmarked positive loops: n sum_(W=1)^400 H_W(corrected)<0.288671. All negative/internal boundary cycles together have gas log n sum_(P>=4)(4exp(-8))^P<0.000008311. Marking one spanning component and dropping all compatibility is an upper bound, whether or not the entire subset is connected. See `flow_resume_20261114/STRIP_WALK_BOUND.md` and strip_walk_bound.py/json for directed scalar arithmetic.

### 2.3 Full cylindrical mass
For a full-height cylinder of width400<=w<=800, with minus spins just outside its two sides, EVERY subset is included. Relative partition log is below446.

Proof: write each row as arbitrary subset S of w sites and r(S) its number of plus runs, r(empty)=0. Relative to the full strip, define D_S=exp[-16(r(S)-1)-(w-|S|)/25]. All D_S<=1, including empty rows since w>=400. K_ST=t^|S symmetricdifference T|, t=exp(-8), is a tensor product of [[1,t],[t,1]], hence positive semidefinite with norm(1+t)^w. Exact relative partition is Tr[(D^.5 K D^.5)^L]. Its trace is sumD<=exp16 sum_S exp(-16r(S))<=exp16(1+t)^(w+1), because row patterns correspond to even subsets of the w+1 transition bonds. Positivity gives Tr(T^L)<=||T||^(L-1)TrT, hence Zrel<=exp16(1+exp(-8))^(wL+1). For w<=800,L1600 its log is<446. Rational check: exp8>2980 by a finite Taylor sum, and log(1+u)<u, so logZrel<16+1280001/2980<446. This includes holes, multiple intervals, empty rows and winding; no subclass exclusion remains.

## 3. The canonical paths

Use augmented plus connectivity with the fixed northeast/southwest diagonal, in addition to physical edges. Order ORIGINAL components by a fixed root order. Classify a component by deterministic connected exploration with local lifts. Stop if either lifted bbox span reaches400; call it large. If exploration exhausts first, its whole bbox is contractible and has both spans<400. This definition applies to winding components without presuming a global bbox. Before reaching400, a lifted box cannot wind or identify two torus vertices because its spans are<L/2.

Erase each small original component completely before considering the next. Keep its original membership even if the current remainder disconnects. Delete in descending lifted row and ascending position within each row. A deleted site has no active plus above or left, and no other original component is a physical neighbor. Thus it has k<=2 plus neighbors. Deletion energy is16k-32+1/25, so inverse rate<3. Each completed horizontal run of length ell<=400 decreases energy by at least16-ell/25; its temporary rise is at most(ell-1)/25<=15.96.

At the first large component, stop all deletions permanently. Explore its ORIGINAL connected prefix. After each original vertex that enlarges the prefix bbox, fill that enlarged bbox immediately. Maintain an explicit overwrite set U consisting of the old filled rectangle, new original witness, and sites filled so far. Choose new sites in fixed lexicographic order among sites in the enlarged bbox having at least two neighbors IN U. This order depends only on the record, not on unknown exterior spins. Already-plus original sites are included as bookkeeping no-ops. Axial extensions form a contiguous added-row interval. Diagonal extensions bridge the original witness and fill the new row and column; two-neighbor filling is always available.

When the first bbox span reaches400, orient it as width400. Extend the other dimension one row at a time, in a fixed order, until it wraps the full1600 circumference. Then add full-height columns, in a fixed cyclic order, until first majority. Check the target after EVERY actual flip and stop immediately, including during incomplete rectangles/rows/columns. If there is no large component, deletion reaches a. Each site is deleted at most once and, after the single switch to addition-only work, added at most once. Path length is at most2n. A repeated undirected edge in opposite phases is handled by summing phase contributions below.

## 4. Conditional deletion comparison and reconstruction

Let T be the FULL collection of previously erased ORIGINAL components. Remove T from the ORIGINAL initial configuration first. Original component nonadjacency gives exact factorization w(initial)=w(initial without T)w(T). Do not split T at an overwrite boundary and do not restore T to the current configuration when asserting this factorization. Sum T by its small-component Gibbs gas only after dropping compatibility.

During addition phases, U is all plus in the current state z; every site outside U is unchanged from the remaining original configuration. Let S be that remaining original subset in U. Then
 initial=(z outside U) union S union T.
This reconstructs the initial state uniquely from edge state, geometric U record, S and T. T may cross U and may be partially regrown; the formula still holds.

For fixed exterior eta, deleting sites of U gives
 E_eta(S)-E_eta(U)=E_minus(S)-E_minus(U)+16 times[number of physical bonds from an exterior plus to a removed interior site].
Hence actual exterior plus spins only reduce the weighted preimage ratio. One may bound it by the isolated geometry without enumerating or deleting thermal companions.

Use a deliberately generous common bound100n^4 geometric records per phase. For bootstrap: old rectangle anchor n, dimensions<=n, direction/orientation flags<=32, witness local-site<=2n, progress<=n give<=64n^4. Progress counts scheduled positions INCLUDING already-plus no-ops, not just actual flips; otherwise decoding U could incorrectly depend on the unknown initial subset. More economical records exist but are unnecessary. Prewrap and cylinder records (anchor, orientation, dimensions and prefix length) are smaller. No exploration-history or seed-root record is required: the reconstructed initial state, not its history, is the injected object. The geometric record fixes U; the marked component is then summed as part of S. With length2n, log[(100n^4)(2n)]<80.

## 5. Each phase's weighted load

### 5.1 Erosion
At gatev on the current active row, encode erased top rows A, erased current-row prefix D0, and whole earlier components T. Then initial=z union A union D0 union T. Record original active width W<=400 and left edge (at most sum_W W=80200 possibilities). Complete the current row to a full width-W plus wire F. Every erased upper component connects in the original active component to the gate through this row; therefore A union F is augmented-connected. Full wiring maximizes attractive contacts, so inserting A into the actual rough residual costs at least insertion above F. Summing possible top heights<=400 and applying Section2.1 gives factor400 exp(878+small hole allowance), since E(rect(W,h))-E(F)=(h-1)(16-W/25)>=0.

For D0 with k runs, make all lower contacts plus and allow at most one right contact with the retained gate. Insertion energy is at least16k-|D0|/25-16. Number of length-m binary strings with k runs is binom(m+1,2k). Thus the row-prefix sum is bounded by exp32(1+exp(-8))^401, log<32.135. Together with native inverse rate1+exp(.04), length2n,80200 width/anchor records,400 heights and source gas, the directed value in erosion_congestion.json is943.348529<944. This argument compares to a WIRED ROW; it does not replace an arbitrary residual by a full rectangle.

### 5.2 Incremental bootstrap
For an axial extension of transverse widthw and current new-row interval lengthell, E(U)-E(full enlarged bbox)=(w-ell)/25<=15.96. For a diagonal witness next to a w-by-h rectangle, perimeter starts P_old+4 and remains so under the chosen two-neighbor fills; the difference to the completed bbox is initially(w+h)/25<=31.92 and decreases. Untouched original exterior plus sites are excluded from U and handled by Section4, not inserted into this isolated energy calculation.

The explored original prefix remains inside S and spans BOTH dimensions of R=bbox(U). Thus S has a marked augmented component with exactly bbox R; other restricted components need not be connected to it. Sum that component by Section2.1 (hull plus negative boundaries), all other S components by the small-box gas, and T separately. Bound its relative energy factor by exp32. Native two-neighbor additions have inverse rate<2<exp1. All gas/hole logarithms together are<1. Common record and length log<80. Therefore log load<878+32+1+1+80=992.

### 5.3 Prewrap growth and final seam completion
U is a full400-by-h rectangle plus an active next-row prefix. Its isolated OPEN energy is<=6400+15.96. S still contains the original connected width400 seed, so Section2.2 applies without assuming S itself connected. Its marked log allowance191 ALREADY includes vertical roots. Unmarked/negative gas plus erased T have total log<1. A first protuberance costs at most15.96, hence inverse rate1+exp15.96<exp17. With common records and length, log load<191+16+1+17+80=305.

Keep this OPEN comparison through the final row completing the periodic wrap. Cut the seam between the growth-origin row and final new row, which does not cut the original local seed. For any subset S of current U, let B(S) count occupied-occupied seam bonds. E_open(S)=E_periodic(S)+16B(S), so
 E_periodic(S)-E_periodic(U)=E_open(S)-E_open(U)+16[B(U)-B(S)]>=E_open(S)-E_open(U).
Thus the open-height1600 bound is conservative. Do not compare an unfinished last row directly to the full cylinder, which would create an unjustified6400 penalty.

### 5.4 Cylinder thickening
After complete wrap, U is a full-height cylinder of widthw plus a prefix in the next column. Before first majority its enclosing width is<=800. A complete extra column changes full-strip energy by-64; its partial prefix raises the previous full-strip energy by at most15.96. Therefore E(U)-E(enclosing full cylinder)<=79.96<80. Section2.3 sums ALL subset preimages, without a seed restriction. The prior T gas costs log<1, native inverse rate log<17, common record/length log<80. Hence log load<446+80+1+17+80=624.

## 6. Congestion, uniform duration and limitations

Define rho=max_e c(e)^(-1) sum_(x in D) w(x)|gamma_x| m_e(gamma_x), where m_e counts EVERY occurrence of the unordered edge in the path, not mere membership. For an unordered edge e, sum the contributions of all four phases; a path can use the same undirected edge in different phases, which this sum explicitly pays. The reconstructed initial weight bounds above multiply by length<=2n as required by Cauchy–Schwarz. Consequently
 rho <= exp944+exp992+exp305+exp624 <4exp992<exp994<exp1000.
All comparisons use the original native conductance, not a guided chain.

For functions vanishing on K, telescoping each canonical path and weighted Cauchy–Schwarz give ||f||²_w<=rho E(f,f), so the killed spectral rate is at least1/rho. Reversibility and L2 contraction give survival from x at time t at most min(1,sqrt(Z_D/w(x))exp(-t/rho)). Integrating yields
 E_x tau_K <=rho[1+.5log(Z_D/w(x))].
The physical torus has2n nearest-neighbor edges, so P<=2n. On D, P<=4|S| gives E(S)<=(32-.04)|S|<15.98n, whereas E(S)>=-|S|/25>=-.02n. Hence the energy span is at most16n. Together with |D|<=2^n, 1+.5log(Z_D/w(x))<22000000. Thus M<22000000 exp1000.

The finite geometry tests are supporting evidence, not substitutes for these arguments or the full-size contour arithmetic: creative test_full_paths.py covers27487 initial states/76587 actual flips; bridge's independent code covers larger scaled tori. This certificate is a finite-volume killed-chain mathematical result. It does not establish a new engineering capability or the user's broader civilisation-changing goal.
