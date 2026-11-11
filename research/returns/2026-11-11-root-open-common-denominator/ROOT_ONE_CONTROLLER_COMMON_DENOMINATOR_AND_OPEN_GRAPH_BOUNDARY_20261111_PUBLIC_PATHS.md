An open-network common-denominator lift and its initialization boundary
ROOT, 11 November 2026 Brisbane

This note investigates open, arbitrary-order kinetics after the completed
conservative fixed-D path compiler. It derives an exact useful operation in
a RELAXED one-controller model. That model has one initially supplied
zero-payload controller, so it does NOT answer a compiler question requiring
canonical zero-auxiliary initialization and every decoder column nonzero.
Its limitations are structural, not an unproved claim that the same service
is already available under those stricter conditions.

1. A NONEXPLOSION AND ESCAPE BUDGET WITHOUT A STATE-SPACE ORACLE

For any finite mass-action network write lambda_r(x)=k_r(x)_(y_r),
N(x)=omega.x, with positive INTEGER omega, and assume the explicit input
drift promise
 sum_r lambda_r(x) omega.(z_r-y_r)<=A, ALL x in N^d.   (1)
A>=0 is rational input, not a supplied law/sample/moment oracle. Its truth
defines the admitted input class. The condition is on actual stochastic
falling-factorial intensities, not deterministic concentration monomials.

Stop the minimal process when N first reaches B or at tau. The stopped
Dynkin inequality and nonnegativity give
 P(sup_(t<=tau) N(X_t)>=B)<=(N(x0)+A tau)/B.          (2)
Bounded N contains finitely many states and bounded total marked intensity.
Thus explosion would require arbitrarily large N; (2) rules it out. Original
null/parallel labels remain counted. This proof does not assert uniform
stationary moments or irreducibility. Pure immigration is allowed.

The class includes genuinely nonlinear positive birth feedback. For example,
0->A, A->0,2A->3A,3A->2A with rates a,b,c,d>0 has
 L N=a-bn+c n(n-1)-d n(n-1)(n-2)
 <=a+(c+3d)n^2-d n^3
 <=a+4(c+3d)^3/(27d^2).                             (3)
This is not per-source nonpositive drift; its higher-order death pays the
quadratic birth. A is an effective rational envelope with all reciprocal-rate
costs visible.

2. ONE CONTROLLER MAKES EVERY AVERAGED RATE SHARE ONE DENOMINATOR

For each distinct nonempty complex c choose a private ordered prefix chain
C_(c,j),1<=j<=|c|. Its decoder is the j-molecule original payload. Also use
C_empty with decoder ZERO. All C states carry one unit of a conserved
controller count. Initialize C_empty=1. Captures/releases are
 C_empty+X_i1 <-> C_(c,1),
 C_(c,j-1)+X_ij <-> C_(c,j).
Central original label r is C_(y_r,|y_r|)->C_(z_r,|z_r|), interpreting the
empty complex as C_empty. All fine channels have arity<=2 EACH side.
There is exactly one controller on every actual path. Every decoded original
edge is enabled correctly; hidden releases connect every state of this
controller sector through its canonical encoding. Directed reachability and
communicating classes project exactly within this sector, for ANY R.

Give controller state C_(c,j) a positive activity w_(c,j), w_empty=1.
Use hidden reverse coefficients K and forward coefficients
 K w_(c,1), K w_(c,j)/w_(c,j-1), respectively.
At decoded x its unique hidden equilibrium has partition
 q(x)=1+sum_(c,j) w_(c,j)(x)_(c_j),
 P(C_(c,j))=w_(c,j)(x)_(c_j)/q(x).                  (4)
Detailed balance follows by one-molecule factorial cancellation. The fibre
is finite although the full state space is infinite. No partition is computed.

Let K_c=sum_(r:y_r=c) k_r for nonempty source complexes. Choose full source
activities w_(c,|c|)=theta K_c and central coefficient
 k_r/(theta K_c) for nonempty source c, or k_r for empty source.
Then EVERY averaged original labelled intensity is EXACTLY
 bar_lambda_r(x)=lambda_r(x)/q(x).                  (5)
The denominator is common, including for original null/parallel labels.
Consequently the entire averaged process is the original embedded marked
jump chain with its holding times multiplied by q(x)>=1. It inherits the
reference escape bound (2) on every finite horizon under the same jump-chain
coupling. This common time change is absent from the independent multi-prefix
partition-ratio formula of the conservative compiler.

There is also a global fine CENTRAL intensity bound: if its controller is in
any nonempty source state the sum of outgoing original-label coefficients
is theta^-1; in the empty state it is at most m. Hence
 sum central intensity<=m+theta^-1                 (6)
at EVERY population, not merely before an escape threshold. Decoded positive
population jumps are bounded by the largest original product size. Thus
the controller-sector fine process has polynomial finite-horizon population
and ALL-event bounds from Poisson domination, even after an unlikely escape.
This avoids charging an unbounded rare continuation by an exponential
population estimate. It does not create physical proposal clocks.

3. SOURCE-ACTIVITY WEIGHTS REMOVE AN ARTIFICIAL EXPONENTIAL IN ORDER

Suppose molecular lists are explicit, so variable maximum order D is at
most complete input length. Fix a NUMERICAL threshold B>=1, put U=1+B, and
compute the actual source-activity envelope
 Gamma=2+m+sum_r k_r U^|y_r|.                         (7)
For a complex c which is a nonempty SOURCE, choose
 w_(c,j)=theta K_c B^(j-|c|).
For a product-only complex choose
 w_(c,j)=theta B^-j.                                 (8)
If c is both a source and product, use the source rule. These activities
have polynomial binary descriptions in the explicit input; they are proof
weights. The emitted adjacent rate ratios are just B or B^-1 except for
the first capture. On N(x)<=B,
 q(x)<=1+theta D[Gamma+2m].                          (9)
All hidden first-capture births from the empty controller have total rate
<=C K theta m B. The source chain's upward/downward ratio is at most B^2;
the product-only ratio is at most one. The exact one-dimensional birth-death
hitting-time formula bounds return to the empty state by
 C D^2[1+(Gamma/k_min)^2]/K.                         (10)
Indeed each product of source-chain birth/death ratios is at most B^(2|c|),
and K_c U^|c|<=Gamma while K_c>=k_min. There are at most D^2 such products.
The product-only chain is at worst unbiased and costs D^2/K. Impossible
prefix lengths simply truncate a chain. There is no 2^D factor from replacing
this finite sum by a product of loose one-step probability estimates.

Markov's inequality for (10), and a bound on ANY new first capture during
that same return interval, give a common empty-controller atom if theta is
small by a polynomial in D,m,B,Gamma,k_min^-1. The central proposal rate (6)
and the completed uniformization lemma then pay a full marked-path averaging
error with K polynomial in the SAME envelope and inverse accuracy.

Minimum first-source capture coefficients also do not conceal order:
 B^(|c|-1)/(K theta K_c)
 <=Gamma k_min^-2/(K theta).
Other adjacent inverse coefficients cost at most B or B/theta. Thus a common
rate normalization, fault tolerance and full firing ledger can be polynomial
in (7), with a UNIVERSAL degree independent of D. Gamma pays genuine source
activity at the selected threshold, not an unearned polynomial-in-D kinetic
clock for arbitrarily high molecularity.

4. WHAT THIS DOES NOT SUPPLY

The conserved C_empty controller is a ZERO-decoder species present initially.
Replacing it by an assertion that such a token will appear from nothing
violates zero-auxiliary canonical initialization and nonzero decoder columns.
Allowing controller multiplicity to grow removes (6) and changes (4)--(5).
No exact token-free replacement has been constructed here. A controller
restricted to one invariant sector also does not prove graph statements for
all other controller-count sectors.

For a strict controller-free compiler, the reference drift bound (1) pays
reference escape only. It does NOT control the compiled process outside the
threshold. The full physical expected work must still be paid there under
all predictable faults; a small TV failure probability cannot multiply an
infinite/exponential unpaid continuation. Feedback, reflective cutoffs or
new decoded corrective edges are not free. Corrective firings must remain
actual original enabled labels under the full graph contract.

5. PRIMARY COMPARISON

Gupta--Briat--Khammash1304.5404v3 Condition1(DD),Theorem2/Proposition4 were
read. Uniform moments use BOTH negative drift and a diffusivity bound, with
admitted moment orders restricted by1+2c2/c5; ergodicity additionally uses
irreducibility. These are sufficient stability contracts, not a universal
physical elementary compiler or an all-order moment consequence of (1).
https://arxiv.org/pdf/1304.5404

The reference nonexplosion/escape argument (2) is derived directly and needs
none of those stronger stationary assumptions. Prior marked-path and
predictable-fault constructions retain their actual scopes. No held source,
archive or alternative provider is used in this note.
