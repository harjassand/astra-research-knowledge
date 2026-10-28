# A finite scalar interface for robust normalized quadratics

Status: an exact rational upper-certificate compiler, feasible lower
receiver, and explicit approximation gap are constructed and executed up
to 100000 branches. Generic secant, knapsack, conic optimization and
interval-statistics hardness are prior. A matching ordinary SOCP succeeds
and is faster in the measured 4096-branch comparison. No new generic
optimization advantage, end-to-end rare-event acquisition, physical
capability or historical novelty is established.

This wave pays for an explicit computational input rather than assuming
unmeasured preparation or calibration. Its output is a finite checkable
operation. The remaining scientific acquisition interface is kept separate.

## 1. Exact input/output contract

Given rational vectors 0<=l_i<=u_i, r_i>=0, at least one u_i>0, define

    F*=max_(l<=w<=u, sum w>0) [sum_i r_i w_i^2]/[sum_i w_i]^2.   (1)

The compiler returns rationals L,U with L<=F*<=U, an actual corner
attaining L, a single rational multiplier nu giving a global upper proof,
and a computable factor kappa with U<=kappa L. It is not an exact solver
for (1) in general. Every coefficient/interval is read and charged.

For the source rare-event local inequality, set

    l_i=P_i ell_i,   u_i=P_i up_i,   r_i=B_i/q_i.               (2)

Here P and q are given distributions, q_i>0 on success-reachable edges,
B_i>=1 are already verified child second-moment bounds, and
0<=ell_i<=h_i<=up_i<=1 are already verified continuation enclosures.
Zero-weight coordinates are removed. The supplied-box cost is an input,
not something solved by this compiler. A neural prediction is not an
enclosure. This wave does not obtain those scientific child bounds on an
implicit high-dimensional dynamics model.

The source N487/BN proof is fully read at revision
97970d87d04c7b0c932c69d3403b155d844acfc6; its fixed-proposal corner reduction
requires up to 2^k tests. Its separate state-space acquisition obstruction
remains open. Local algebra below is proved independently of the source.

If sum l_i=0, all l_i=0 and (1) is exactly max_(u_i>0) r_i: the inequality
sum w_i^2<=(sum w_i)^2 gives the upper, attained by one nonzero coordinate.
If every numerator coefficient vanishes on its interval, the answer is
zero. Below assume S0=sum l_i>0 and a positive numerator is possible.

## 2. One scalar is enough for a global rational upper certificate

For w_i in [l_i,u_i], the elementary secant identity gives

    r_i w_i^2 <= r_i(l_i+u_i)w_i-r_i l_i u_i.                  (3)

Put c_i=r_i(l_i+u_i). For any positive rational nu define

    eta(nu)=sum_i {max[(c_i-nu)l_i,(c_i-nu)u_i]-r_i l_i u_i}.

If eta<0, then for every w in the entire box, with S=sum w_i,

    sum r_i w_i^2 <= nu S+eta
                    <= [-nu^2/(4eta)] S^2.                  (4)

The last inequality is the completed square

    [-nu^2/(4eta)](S+2eta/nu)^2 >=0.

Thus U(nu)=-nu^2/(4eta) is a global certificate. Checking it requires one
pass over the inputs, no sorting, nonlinear optimizer, unknown true h, or
convex-envelope oracle. The scalar's rational bit length is not treated
as constant. Any numerical ordinary solver may propose nu; (4) is then
rebuilt exactly and trusted independently of its floating result.

## 3. Exact solution of the secant relaxation

Replace each numerator term by its secant. Let d_i=u_i-l_i and write
w_i=l_i+d_i z_i, 0<=z_i<=1. The relaxed numerator is

    N0+sum_i c_i d_i z_i,       N0=sum r_i l_i^2,

while S=S0+sum d_i z_i. At any fixed S, the largest relaxed numerator is
the continuous-knapsack envelope Nbar(S): fill intervals in nonincreasing
order of density c_i. This is a concave piecewise-linear function. This
greedy exchange argument is ordinary fractional knapsack, not a new
optimization principle.

On a segment beginning at (S,N), of width d and density c, evaluate both
endpoints of [N+c(s-S)]/s^2 and, when it is inside the segment, the point

    s*=2S-2N/c.                                               (5)

For c=0 the ratio decreases, so no interior candidate is needed. This
finds the exact global maximum U of the secant relaxation in O(k log k)
rational arithmetic operations, with O(k) storage. The largest prefix
corner value supplies L; the implementation additionally tries every
singleton and complement corner in O(k) operations. Only the final best
corner is materialized, avoiding repeated O(k)-size allocations.

At a relaxed maximizer S*, a supporting slope is nu=2U S*. For an interior
linear segment, stationarity in (5) makes nu its density. At a breakpoint,
the left/right derivative conditions place nu between the adjacent
densities. At the domain endpoints it is respectively above/below all
relevant densities. In every case the supporting intercept is

    eta(nu)=Nbar(S*)-nu S*=-U(S*)^2<0.

Hence U=-nu^2/(4eta): the scalar certificate (4) is exactly the sorted
secant optimum, not a looser after-the-fact fit. `box_compiler.py` checks
this identity with exact rational arithmetic.

These are arithmetic-operation counts, not a unit-cost real-RAM runtime
claim. Prefix rational denominators can grow with total input bit length.
The full algorithm and verification have polynomial bit cost in the
explicit input length; the measured implementation uses Python Fraction.

## 4. A posteriori quadratic rounding gap

If the relaxed maximum is a prefix corner, L=U=F*. Otherwise it occurs
with exactly one fractional coordinate in the greedy representation.
Let its adjacent prefix corners have masses S and S+d, and mixing weight
theta in (0,1). Their interpolated mass is s*=S+theta d. The interpolated
numerator is U(s*)^2, while their interpolated squared denominator is

    (1-theta)S^2+theta(S+d)^2=(s*)^2+theta(1-theta)d^2.

The maximum of the two actual corner ratios is at least the ratio of
these interpolated numerator and denominator. Therefore

    L <= F* <= U <= L[1+theta(1-theta)(d/s*)^2].               (6)

The singleton/complement improvements only increase L. An immediate
input-only bound is

    U/L <= 1+(max_i d_i/[2 sum_i l_i])^2.                     (7)

Thus many sufficiently small uncertain branch masses have a certified
near-exact answer without corner enumeration. No stochastic assumption
on inputs or blanket approximation guarantee for concentrated boxes is
made. The actually returned U/L is checked exactly, not inferred from a
finite numerical diagnostic.

## 5. Exact optimization is already NP-hard in a narrow positive case

Take given positive integer weights a_i with A=sum a_i, target integer
0<T<A/2, P_i=q_i=a_i/A, all B_i=1, and common continuation interval

    h_i in [ell,1],          ell=T/(A-T).

For mu=sum q_i h_i, (h_i-ell)(1-h_i)>=0 gives

    [sum q_i h_i^2]/mu^2 <= [(1+ell)mu-ell]/mu^2
                         <= (1+ell)^2/(4ell)
                          = A^2/[4T(A-T)].                   (8)

Equality requires every h_i be an endpoint and the q-mass at 1 equal
ell/(1+ell)=T/A. Therefore equality in (8) holds exactly if the a_i admit
a subset of sum T. Restricting SUBSET SUM to T<A/2 remains NP-hard: append
a dummy weight 2T+1 to a PARTITION instance of total 2T. It cannot belong
to a subset of sum T, and the new total is 4T+1. All constructed rationals
have polynomial input bit length.

Consequently exact robust maximization is NP-hard even with P=q, B=1 and
one common strictly positive interval. This does not establish hardness
of a specified approximation gap or a runtime lower bound for the present
fixtures. Interval-statistics hardness and Kantorovich-type inequalities
are established prior; this direct reduction fixes the source operator's
particular weighted contract. No historical priority is claimed.

## 6. Strong ordinary comparator: exactly the same bound is an SOCP

Let C=sum r_i l_i u_i. Introduce positive variables t,nu and real z_i with

    z_i >= (c_i-nu)l_i,       z_i >= (c_i-nu)u_i,
    A=C-sum z_i >=0,
    ||(nu,t-A)||_2 <= t+A.                                   (9)

The cone is equivalent to nu^2<=4tA. Minimizing t therefore computes
the best scalar upper certificate (4). Tight choices of z_i recover
eta, and Section 3 proves the sorted solution attains this SOCP optimum.
This is an ordinary conic relaxation; the secant compiler does not escape
or outperform this mathematical representation.

`ordinary_socp.py` solves (9) with the installed CVXPY/Clarabel stack. Its
floating nu is only a proposal. Quantization to a 40-bit dyadic followed
by exact recomputation of eta and t yields a rigorous certificate, checked
by the same one-pass rational receiver. Numerical solver residuals and
reported objectives are not proof premises.

On the shared 4096-branch input, the ordinary solve plus exact recovery
took 0.11213 seconds, versus 0.17039 seconds for the exact sorted compiler
plus verification in that matched run. The ordinary certified upper was
only 1.1615e-9 relatively above the exact secant optimum, compared with the
secant's own 1.5244e-8 gap to its feasible lower corner. Thus the ordinary
method is already adequate for the demonstrated accuracy, and faster in
this comparison. This is a finite measurement, not a universal runtime
claim or a result for every optimized ordinary implementation.

Breakpoint/resource-allocation algorithms are established, including
linear-time methods for related continuous quadratic knapsack problems
[Kiwiel](https://rcin.org.pl/Content/139702/PDF/RB-2006-59.pdf).
Their exact problem is not silently identified with (1); the comparison
prevents presenting sorting or one-dimensional duality as a new generic
mechanism. No optimality claim for the compiler's complexity is made.

## 7. Independent alternative: binaryize the same fixed proposal

A different route retains the fixed P,q and replaces the many-way branch
by a balanced binary tree. A subset S has transition/proposal masses
P_S,q_S and continuation interval

    ell_S=sum_(i in S)P_i ell_i/P_S,
    up_S =sum_(i in S)P_i up_i/P_S.

At each artificial binary node combine the two child moment bounds by
the four exact corner tests of the source local inequality, with branch
probabilities P_L/P_S and q_L/q_S. Round each moment bound upward to 48
binary significant bits. Backward induction gives a safe root bound;
the complete path likelihood still equals P_i/q_i at original leaf i.
It uses k-1 binary nodes, four corners per node, and logarithmic artificial
depth. No new physical transitions are implied by the artificial tree.

This alternative was retained until actual execution. At k=4096 it used
16380 rational corner checks and 0.13840 seconds, returning
1.0423939899021377, versus secant U=1.006800121782372. Both are valid but
their quality differs. At k=16 the two retained cases gave binary bounds
1.0195203144555052 and 1.1947590323179753. No optimized grouping or proposal
search is claimed; binaryization is not defeated as a whole method. Its
cost and outputs are preserved in `BINARY_ALTERNATIVE.json`.

The ordinary SOCP remains the stronger matched comparator because it
attains essentially the same secant bound with exact recovered validity.
The comparison is not limited to exhaustive corners or crude Monte Carlo.

## 8. Acquired finite instances and independent consumer

Sixteen cases were fully generated, read and checked. Twelve cases with
k=2,3,5,8,12,16 also received exact exhaustive corner enumeration. The
large cases k=1024,4096,10000,100000 received exact scalar certificates and
actual feasible corner lower receivers. All pass. They are constructed
rational fixtures, not experimental samples or a distributional theorem.

The largest input uses midpoint proposals and heterogeneous continuation
widths, with B_i=1. Its exact upper has decimal display

    U=1.005243261216975...,
    U/L-1=2.1259499332412705e-11... .                           (10)

The simple global Kantorovich-type comparator gives 5.263157894736842...
on that input. This comparison alone would overstate novelty or advantage:
the ordinary SOCP matches the stronger secant bound as Section 6 explains.

`independent_consumer.py` imports no producer code and performs no sort or
optimization. It independently reconstructs all 100000 explicit input
coordinates from their recorded definition, verifies (3)–(4) through nu,
eta and the completed-square inequality, and evaluates the actual corner
for L. It also checks the saved 16- and 4096-coordinate inputs. All pass.
This is a second code path by the same worker, not an independent peer
audit. Exact certificate and corner values, rather than hashes, establish
the finite inequalities.

In the retained final 100000-coordinate run, input generation cost
0.70506 seconds, compilation 3.39905 seconds, and linear verification
0.86175 seconds. Peak process memory for the full sixteen-case producer
was 129646592 bytes on macOS. Source reading, design and writing are not
included in these execution timers. The complete ledger, original rerun
and ordinary-import costs are preserved separately.

## 9. What changes in the research decision

The many-way local verification bottleneck can be replaced by a cheap
finite rational upper certificate with a computable precision contract.
Exact tight maximization remains NP-hard, and concentrated boxes can have
a poor secant gap. The operator's high-degree interface is acquired at
its explicit-input scope; ordinary conic optimization already supplies it.

The consequential source gap is still the acquisition of good continuation
and second-moment bounds on an implicit high-dimensional state space.
Nothing here bypasses that input, learns a committor, removes its precision
cost, or proves a useful global path variance from a local fixture. The
source's original backward interval routine already solved its probability
problem; moving its cost into this interface would repeat that failure.

Decision: use an ordinary secant/SOCP or the exact scalar compiler for
supplied high-degree boxes, with its returned gap. Do not treat solving
this local operation as an end-to-end rare-event discovery or a new
scientific platform. The paid comparison rejects a claimed advantage over
the strong ordinary alternative, while preserving the exact operation,
its hardness boundary and independently consumable certificate as usable
outputs. Historical priority and a substantially enabling new research
capability remain UNKNOWN/NOT_ACHIEVED respectively.
