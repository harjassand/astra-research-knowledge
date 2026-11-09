ROOT: GRAPH-PRESERVING CATALYTIC CLOCK WITH A POPULATION-UNIFORM NOMINAL GAP
10 November 2026 Brisbane. Complete nominal construction from accepted actual-class geometry. Independent coefficient-error robustness is NOT a conclusion.

SETUP. R is any FIXED finite weakly reversible reaction structure on N^d. Actual classes are Gamma_R(x). The accepted effective global Presburger congruence Psi_R, marked-coordinate balancing table and local-witness constant H are premises, as supplied in P3_FULL_MEAN_CALIBRATION_AFTER_B4D193_XI_20261110.txt/SHA2065553f36160d0a28891fd32e8b4bf44e929110331a4ab80791d6168c6503e9. Every marked table element (a,u,v) has disjoint u,v, Psi_R(a+u,a+v), bounded g=u-v and H>=||g||_2^2. If x,y in one class have max_i|x_i-y_i|>H, an available element lies below (min(x,y),(x-y)_+,(y-x)_+) with a positive marked coordinate of g in a largest-difference coordinate. The opposite translations x->x-g,y->y+g stay in the actual class and strictly reduce squared pair energy.

THEOREM. There is a computable finite integer K_R and a fixed finite catalytic augmentation consisting ONLY of y_r+w->z_r+w for original r and |w|_1<=K_R (including w=0), on the SAME species, with the EXACT SAME directed state-transition graph as R. For every ordinary positive rational lambda, polynomial-bit rational rate constants in (0,1] can be constructed so that on EVERY actual finite/infinite class:
 (i) the nominal process is nonexplosive and has exactly pi_lambda(x)=Z_Gamma^-1 lambda^x/x! as its unique stationary law;
 (ii) its stationary Dirichlet form satisfies Var_pi(f)<=C_R*V_lambda^p_R*E(f,f), with V_lambda=1+sum_i(lambda_i+lambda_i^-1), independently of the initial-population/class parameter;
 (iii) C_R,p_R and the entire fixed compilation are finite and computable. The process may be nonreversible; the inequality yields L2 contraction by the stationary variance identity.
This is a statement about nominal rates and a polynomial numerical-activity gap. It does not make reaction firings, physical implementation or independently perturbed rates free.

1. FIXED ORIGINAL WORDS FOR ALL REQUIRED COARSE MOVES.
For each marked balancing pair a+u,a+v, enumerate original reaction words in both directions until they are found. Existence is guaranteed by actual-class equivalence, so this fixed preprocessing terminates. Each translated word remains enabled. Also, for every bounded nonzero difference g with ||g||_infty<=H, the context set {a: Psi_R(a+g_+,a+g_-)} is effective Presburger and upward closed. Compile its finitely many Dickson-minimal contexts and original words in both directions. This is a finite close-pair connector table.
All stored words have bounded fixed lengths and coordinate excursions, with computable maxima. No claim is made that compilation is efficient in variable R. The word tables concern fixed populations and are not variable-input path searches.

2. PAIR PATHS AND PRODUCT WEIGHTS.
For x,y in one class, repeatedly use the marked pair move until their coordinate differences are <=H; then use a close-pair connector. The pair sum S=x+y is constant. Each coarse step decreases integer squared energy by >=1, hence there are at most O_R((1+|S|_1)^2) steps. Replace each coarse move by its stored original word. Concatenating the x-side path, close connector, and reversed y-side path gives an ORIGINAL directed path from x to y of length <=C_R(1+|S|_1)^2. Reverse portions use the separately stored legal return words, not nonexistent reverse reactions.
At a pair step, g is sign-conformal to x-y and |g_i|<=|x_i-y_i|. For integers A>=B and 0<=t<=A-B, (A-t)!(B+t)!<=A!B!, by convexity of log factorial and symmetry. Therefore
 W_lambda(x-g)*W_lambda(y+g)>=W_lambda(x)*W_lambda(y),
where W_lambda(x)=lambda^x/x!: lambda factors cancel because the pair sum is unchanged. At every coarse pair position u,w on either path half,
 pi(x)*pi(y)<=pi(u)*pi(w).
This is the operation supplied by the geometry; individual weights need not increase.

For any point z on a stored original word begun at u, z-u has a fixed bounded integer offset. Exact factorial/activity ratios consequently give
 pi(z)>=c_R*V_lambda^-b_R*(1+|u|_1)^-b_R*pi(u)
for a computable fixed integer b_R>=1. Both points lie in the same actual class, so no conditioning-normalizer cost is hidden. Increase b_R to cover all finitely many words and their lengths/offsets.

3. CONDITIONAL MOMENTS PAID USING ANY CLASS ANCHOR.
Fix ANY u in Gamma and put N=|u|_1, B=max_i|log lambda_i|. Z_Gamma>=W_lambda(u)>=exp[-N(B+log(max(1,N)))]. Also sum_(x in N^d)e^|x| W_lambda(x)=exp[e*sum lambda_i]. Hence
 Pr_pi(|X|_1>s)<=min(1,exp[D0-s]),
 D0=e*sum lambda_i+N(B+log(max(1,N))).
Integrating this exponential tail gives, for each FIXED integer j>=1,
 E_pi(1+|X|_1)^j<=C_j*(1+D0)^j
 <=C_(j,d)*V_lambda^(2j)*(1+|u|_1)^(2j).
Use B<=V_lambda, log(max(1,N))<=N, and split the tail integral at2(1+D0). Constants can be bounded by integer factorial sums. This holds on rare and infinite classes; the anchor is the present coarse-path endpoint, not an assumed high-probability event.

4. CATALYTIC RATE CONSTRUCTION.
Choose positive integer circulation a_r on the finite complex graph: sum a cycle containing each reaction, using weak reversibility. Let D=max_r |y_r|_1 and c=[(1+sum_r a_r)*V_lambda^D]^-1. For each original r and |w|<=K, choose
 kappa_(r,w)=c*a_r/(w!*lambda^y_r).
Every coefficient is positive rational and <=1. At complex y_r+w, kappa_(r,w)*lambda^(y_r+w)=c*a_r*lambda^w/w!. For each fixed w the a_r circulation balances, so summing all translated cycles gives complex balance even when translated complexes coincide. Thus the full product-Poisson law is formally stationary, as is its restriction to each closed actual class.

Every catalytic copy is enabled only where its original reaction is enabled, and has the SAME population change; w=0 includes all original edges. Thus the entire directed graph, not just a lattice or hull, is exactly preserved.
For x>=y_r, its total r-channel intensity is
 c*a_r*lambda^-y_r*x^falling(y_r)*F_K(|x-y_r|_1),
 F_K(n)=sum_(j=0)^K binom(n,j).
The multinomial falling-factorial identity proves this equality. For all integer n>=0, F_K(n)>=c_K(1+n)^K with computable c_K>0: use binom(n,K)>=(n/2)^K/K! for n>=2K and F_K>=1 on the remaining finite set. Consequently, any enabled original edge at z has nominal rate >=c_R*V_lambda^-p0*(1+|z|_1)^K. Its actual stationary edge flow is at least that rate times pi(z). Combining the stored-word density comparison gives, for a word begun at u,
 edge_flow>=c_R*V_lambda^-p1*(1+|u|_1)^(K-b_R)*pi(u).
All reaction firings of the accelerated process still count. Its intensities have fixed polynomial growth in the actual populations.

5. UNIFORM CONGESTION BOUND.
Use the deterministic pair path just constructed in the identity Var_pi(f)=1/2 sum_(x,y)pi(x)pi(y)(f(x)-f(y))^2, followed by path Cauchy-Schwarz. Fix an actual directed edge. There are only finitely many stored-word types/positions by which a coarse move can traverse it; each fixes its coarse start u as the edge endpoint minus a fixed offset. For a corresponding pair partner w, the original pair sum is S=u+w. The number of ordered original nonnegative pairs with sum S is <=prod_i(S_i+1)<=(1+|S|_1)^d. To allow every possible repeat conservatively, bound both path length and occurrence count by C_R(1+|S|_1)^2. With J=d+4, the aggregate path numerator is therefore at most
 C_R*pi(u)*sum_(w in Gamma)(1+|u+w|_1)^J*pi(w)
 <=C_R*pi(u)*(1+|u|_1)^J*E_pi(1+|X|_1)^J.
The pair product inequality justifies replacing each original pi(x)pi(y) by pi(u)pi(w). Divide by the preceding edge-flow lower bound and use the anchor-at-u moment estimate. The ratio is at most
 C_R*V_lambda^p2*(1+|u|_1)^(3J+b_R-K).
Choose the FIXED catalytic degree K>=3J+b_R. The exponent is nonpositive, so the congestion is uniformly <=C_R*V_lambda^p2 on all edges and ALL classes. Nonnegative sums permit Tonelli on infinite classes. This proves the asserted Poincare inequality initially on finitely supported functions and then by form closure.

6. NONEXPLOSION AND STATIONARITY.
The nominal formal invariant pi is finite, positive on its class, and has every polynomial population moment by3. The total intensity is polynomial, hence sum pi(x)q_x<infinity. For a nonsingleton irreducible class, the embedded jump chain has finite invariant probability proportional to pi(x)q_x. Its stationary mean holding time is1/sum pi q>0; the ergodic theorem for this chain with independent exponential holding times makes elapsed holding time diverge almost surely. Thus the minimal CTMC is nonexplosive from this invariant jump law and, by positivity/irreducibility, from every state. Its stationary occupation law is pi. A singleton class is trivial. Stationary variance dissipation plus the Poincare inequality yields exponential L2 contraction with the stated lower bound, without a reversibility assumption.

7. WHAT REMAINS UNPROVED.
Independent relative perturbations of the finitely many catalytic rate coefficients generally destroy the exact circulation and hence the exact nominal law. The proof above does not give the perturbed stationary density, uniform positive recurrence, first-moment control, TV error, reaction-activity cost or polynomial tolerance needed for a ROBUST kinetic compiler. A population-dependent acceleration is not a free physical speedup. The new full question may use this nominal theorem, discard the construction, or establish a genuine obstruction under its full quantifiers.
The stronger P3 inverse-height compiler9E0579 remains accepted separately and can compose with a robust realization when its actual error/cost interface is constructed. No arbitrary nonequilibrium original-rate recurrence theorem, practical chemical device, historical priority or independent validation is claimed.
All source/access/transfer/resource/Sol/Dots holds persist. New failed governing source https://web.math.wisc.edu/~dfanderson/papers/2023/AndersonKim2023.pdf returned Anubis Access Denied9e4edb5b6b850c41: no retry/alternate recovery; only search metadata was available. The independent primary2309.06970v2 and2402.05343v1 are distinct already accessible sources, not recovery routes for that held paper.
