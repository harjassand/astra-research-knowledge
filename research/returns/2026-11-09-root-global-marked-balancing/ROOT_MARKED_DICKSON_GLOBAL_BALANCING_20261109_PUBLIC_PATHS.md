ROOT: GLOBAL MARKED-COORDINATE BALANCING AND LOCAL MEAN WITNESSES
9 November 2026. Constructed after reading the entire P3 80D545 return, not a blinded independent replication. Uses accepted global Presburger class access and P3's multiset/entropy construction. No external-priority claim.

SETTING.
Fix R. Let Psi_R(x,y) be its accepted computable global mutual-reachability predicate on N^d. Actual SCC equivalence is translation invariant in the forward sense: if x~y then x+z~y+z for z>=0, by translating actual enabled paths. Weakly reversible R is included; this argument also applies to the accepted fixed arbitrary-directed SCC predicate. No lattice-fibre substitution.

FINITE MARKED TABLES.
For each i=1,...,d form the Presburger set
 T_i={(a,u,v) in N^(3d): (u_j=0 or v_j=0) for every j, u_i>=1, Psi_R(a+u,a+v)}.
By Dickson's lemma its componentwise-minimal elements F_i are finite. They are computable, not advice: minimality is a Presburger formula; quantifier elimination and finite enumeration with a Presburger coverage/emptiness test compute all of F_i. Compile actual forward and return R-words for each endpoint pair by finite path enumeration. All these finite costs depend only on R.
Put H=max(1, max_{i,(a,u,v) in F_i} sum_j(u_j-v_j)^2), ignoring empty tables. H is a computable fixed-R positive integer.

STRICT ENERGY REDUCTION.
Take actual same-class populations x,y with ||x-y||_infty>H. Select a coordinate i of maximum absolute difference and exchange the names x,y if needed so x_i-y_i>H. Write p=(x-y)_+, q=(y-x)_+, c=min(x,y).
The triple (c,p,q) belongs to T_i. Some minimal (a,u,v) in F_i lies componentwise below it. Thus a<=c,u<=p,v<=q,u_i>=1.
Let g=u-v. Translate the compiled a+u->a+v word to x and the compiled return word to y. The resulting populations
 x'=x-g, y'=y+g
are nonnegative, belong to the SAME ACTUAL CLASS and obey x'+y'=x+y. Both words are legal since x>=a+u and y>=a+v.
Sign compatibility gives (x-y).g=sum_j(p_j u_j+q_j v_j)>=p_i u_i>H>=||g||_2^2.
Therefore
 ||x||_2^2+||y||_2^2-||x'||_2^2-||y'||_2^2
 =2[(x-y).g-||g||_2^2]>0.
This is the crucial marked-coordinate step. Unmarked minimal triples could act only on small-difference coordinates and would not justify this descent.

UNIVERSAL MIDPOINT BALANCING.
Repeatedly reduce any pair with fixed sum until its integer nonnegative energy cannot decrease. Termination proves: for EVERY x~y there exist u~x,v~x with u+v=x+y and ||u-v||_infty<=H. Thus EVERY fixed R passes P3's BAL test; exceptional class boundaries create no remaining transfer assumption.
The balancing OPERATION itself has polynomial COMPLETE-BINARY cost without simulating the potentially long descent: enumerate the constant number of integer u in |2u_j-(x_j+y_j)|<=H, set v=x+y-u, require nonnegativity and query Psi_R(x,u),Psi_R(x,v). Existence was just proved; at most (H+2)^d candidates, each with O_R(input bits) description. Actual physical path lengths or the naive descent length are not claimed polynomial.

UNIVERSAL LOCAL CARATHEODORY WITNESS.
For rational m in conv(Gamma), take a finite rational convex representation and clear weights to a finite multiset of mean m. Whenever two multiset entries differ in infinity norm by more than H, use the STRICT ENERGY REDUCTION above, preserving total sum and class membership while strictly lowering total squared norm. This terminates with diameter<=H, hence every entry lies within H of its mean m. Caratheodory reduces support to <=d+1.
For m in CLOSED conv(Gamma), approximate it by rational finite convex combinations. Their local witnesses eventually lie in one finite integer box about m; pass to a convergent subsequence of weights on this finite set. The limiting witness has mean exactly m and all support points within H of m.
For rational input m, enumerate Gamma intersect {x:|x_i-m_i|<=H}; it has at most (2H+2)^d points. Exact class checks and constant-size rational linear feasibility compute the exact witness mu in polynomial COMPLETE-BINARY time, including its positive rational weights and populations. No supplied decomposition, interior margin, large population loop or oracle. Finite fixed-R tables/H/compilation are paid once.

EXPLICIT TARGET-CENTRED ENTROPY CONSEQUENCE.
Let L be complete input bits, lambda0_i=m_i+1, P0=product Pois(lambda0_i), pi0=P0 conditioned on Gamma. For every local witness point n, set z=m_i+1>=1, |n_i-z|<=H+1.
For n_i>=1, log(n_i!)<=n_i log n_i-n_i+1+log n_i and log t<=t-1 imply
 -log Pr(Pois(z)=n_i)<= (n_i-z)^2/z+1+log n_i
 <=(H+1)^2+1+log(max(1,n_i)).
For n_i=0 its negative log probability is z<=H+1. Since n_i<=2^L+H, the product bound
 -log P0(n)<=K, K=10d(H+3)^2(L+1)
is a computable conservative bound. Hence P0(Gamma)>=exp(-K) and
 D_KL(mu||pi0)=sum alpha log alpha-sum alpha log P0(n)+log P0(Gamma)<=K.
P3's entropy/regularization argument therefore applies to EVERY actual class, not just balance-certified subclasses. With F(h)=log E_pi0 exp(h.(X-m)), F>=-K,F(0)=0 and tau=epsilon^2/[8192(K+1)], its unique regularized minimizer satisfies
 ||h_tau||<=128(K+1)/epsilon,
 ||grad F(h_tau)||<epsilon/64.
The accepted paid radius-to-selector and ordinary rational rounding yield a deterministic calibration algorithm of EVERY-run cost poly_R(L+epsilon^-1), including finite/infinite classes, zeros/boundary means, full-law moments and ordinary output. This closes population-size dependence for inverse-polynomial accuracy. It DOES NOT close polynomial COMPLETE-BINARY dependence for arbitrary accuracy: epsilon^-1 may be exponential in L.

INTRINSIC CONSEQUENCE / LIMITS.
P3's factorial Jensen gap and calibrated-law local anchor now also extend to ALL actual classes: for an exactly calibrated law at a relative-interior mean, E phi(X)-phi(m)=O_R(L+1) and some actual local point has probability>=exp[-O_R(L+1)]. Boundary means remain approximation targets; existence of an exact positive-activity calibration there is not asserted.
These constructions do not themselves bound a numerical log-activity radius by poly_R(L), control all normal/tangential directions at binary accuracy, give polynomial physical reaction paths, or establish independent novelty. The FULL unrestricted inverse-height/compiler question remains OPEN.

PROOF CLARIFICATIONS TO 80D545.
Its Graver lattice proof has strict squared-energy descent because the balanced difference is coordinatewise no larger in magnitude than the old conformal difference, with at least one strict decrease when its old infinity norm exceeds H_Lambda. For an abstract BAL(H) property without conformality, the stated infinity-diameter-H multiset argument instead uses the threshold ceil(sqrt(d)*H) (or Euclidean diameter sqrt(d)*H); this harmless fixed-constant correction preserves its conditional consequences. The marked actual-class proof above supplies its own strict descent and infinity bound H directly.
The complete modular-creation inverse family remains accepted, but it still reduces to ONE nonlinear scalar total plus multinomial proportions and does not establish generic coupled inverse height.
