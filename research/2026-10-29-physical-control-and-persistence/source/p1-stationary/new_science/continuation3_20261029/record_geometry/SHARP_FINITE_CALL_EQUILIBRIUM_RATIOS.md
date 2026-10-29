# Sharp invariant-ratio control from one unknown physical binary operation

29 October 2026. Existing record-geometry role, complementary construction.
The root's `BOUNDED_REVERSIBLE_EXCURSION_COMPILER.md` extends the fast pair
below to arbitrary reversible microscopic kernels. This note proves the
restricted iid construction, its sharp bounds, and literal selector options.
Neither note claims historical priority, hardware validation, or a new Ising
solution. Close primary precedents are separated in `PRIMARY_COMPARISON.md`.

## 1. The physical interface and the objective

A native call changes an actual binary state by an independent Bernoulli(p)
increment, conditional on a frozen unknown parameter p in an open interval
I contained in (0,1). The same p applies from both bit values. A causal
controller observes endpoint labels, may use independent randomness, and
must make between one and N calls. Its output is the actual final bit.
No free identity branch, protected hold, overwrite, or microscopic copy is
supplied. Constant hidden parameters may differ between devices and edges.

The finite-call model must describe the actual endpoint kernels, including
whatever boundary evolution, reads and decision timing the apparatus has.
Counting calls alone is not a hardware timing proof. The physical completion
time is generally random even with a hard native-call cap. Raw word keys,
intermediate labels and the completion count can be retained, but the claim
below is about the endpoint kernel, not independence from that larger record.

Let A and B be the two bit values. We seek an endpoint kernel satisfying

    K_p(A,B) / K_p(B,A) = r

for every unknown p. Its invariant law is then
pi(A)=1/(1+r), pi(B)=r/(1+r). This asks for the correct invariant ratio,
not p-independent transition probabilities. The latter remains obstructed
by the earlier signed-continuation result at its stated bounded-time interface.

## 2. A sharp, fast pair for the integer ratio N

Define a_N(p)=1-(1-p)^N.

**High-direction program A_N.** Starting at A, call the source until its
first flip or until N calls have been made. Stop on whichever occurs first.

**Low-direction program B_N.** Starting at B, make one call. If it does not
flip, stop. If it flips to A, use an independent L uniform on {0,...,N-1}
and continue until the next flip or L additional calls, whichever comes first.
For L=0, stop after the already completed first call. L may be drawn before
the first call so no new randomizer is required at the intermediate endpoint.

Every path uses at least one and at most N calls. There is no discarded
trial, no reset to the starting microscopic state, and no controller-created
output substituted for the physical bit. A return after two flips is a
physically executed trajectory.

The high direction ends opposite its start precisely if a flip occurs in
the first N calls. The low direction ends opposite precisely if the first
call flips and none of the next L calls flips. Therefore

    F_A(p) = a_N(p),
    F_B(p) = (p/N) sum_{ell=0}^{N-1}(1-p)^ell = a_N(p)/N.       (1)

Thus the complete endpoint kernel is reversible for (1,N)/(1+N), for every
unknown p. Its off-diagonal entries are an ordinary Metropolis pair,
multiplied by the unknown symmetric mobility a_N(p).

The exact costs are

    E_A tau = a_N(p)/p,
    E_B tau = 2-a_N(p)/(Np).                                 (2)

To obtain the second identity, condition on the first flip and use
E[min(G,ell)]=[1-(1-p)^ell]/p for a geometric(p) waiting time G.
Both costs lie in [1,N]. If p>=p_min>0 they are at most
max(1/p_min,2), even when N is large. At the target stationary start,

    E_pi tau = 2N/(N+1),                                    (3)

independent of p. Neither this stationary mean nor the pointwise mean is
a preparation/mixing bound. The worst possible native-call count is still N.

The earlier pair that ends opposite with probabilities N p(1-p)^(N-1)
and p(1-p)^(N-1) has the same exact ratio, but both transitions become
exponentially small in N at fixed p. The fast pair avoids that loss. The
slower family remains useful for bounded fair-bit selectors in Section 6.

## 3. Sharp universal bias and transition bounds

**Lemma (first coefficient).** For any randomized causal controller using
1<=tau<=N calls, the opposite-endpoint probability F(p) is a polynomial
of degree at most N and

    F'(0)=E[tau on the all-no-flip path] in [1,N].             (4)

Proof. Fix an independent controller seed. The finite decision tree is a
sum of stopped path probabilities p^f(1-p)^(t-f), where t<=N. No-flip
paths end at the initial bit. At first order in p, exactly one flip occurs.
The first flip can occur at any of the t_0 call positions on the controller's
all-no-flip path. After that flip, any subsequent no-flip suffix still ends
at the opposite physical bit, regardless of the changed stopping decision.
Each such branch has coefficient one at order p. Paths with at least two
flips contribute O(p^2). Thus F'(0)=t_0. Integrate over the seed; the degree
is uniformly bounded, so this integration preserves the polynomial identity.
No physical access to p=0 is used. QED.

If F_A(p)=r F_B(p) on any open physical interval, polynomial identity extends
the equality to p=0. Equation (4) gives

    1/N <= r <= N.                                          (5)

The fast pair saturates r=N. No exponentially larger exact ratio is possible
under the stated single-source, mandatory-first-call, hard-cap interface.
Equivalently, the dimensionless invariant-weight bias is at most log N.

Furthermore, for every such controller and every p in [0,1],

    F(p) <= 1-(1-p)^N,                                     (6)

because at least one of the first N potential increments must flip for the
actual endpoint to change. The A_N rule attains this bound simultaneously
for all p. At ratio N, the fast pair therefore maximizes both off-diagonal
entries pointwise in p among all admissible pairs. This is a conductance/
transition-probability statement; it does not imply fastest absolute-eigenvalue
mixing, absence of oscillation, or superiority per wall-clock time.

The open-interval requirement matters. A finite possible set of p values
need not give polynomial identity. Multiple native operations with different
known p-dependences can evade (5). In preserved source B, for example,
p_1(h)=3p_0(h), so the two selected operations already give ratio3 in one
call. A genuinely available zero-call branch also changes (4).

## 4. A separate sharp lower bound on stationary native cost

The mean-cost conclusion has an independent optimality proof. Fix p>0 and
let any physical stopping protocol use the same symmetric source, at least
one call, and finite expected call count from each starting bit. Suppose
its endpoint kernel preserves pi=(1,r)/(1+r), r>=1. Start the macro in pi.

Write O_A and O_B for the expected numbers of pre-call visits to A and B
during this macro. The expected net change of the physical bit is zero,
because its starting and terminal distributions are both pi. Conditional
on each pre-call state, the native expected signed increment is +p at A
and -p at B. Finite mean permits stopped-sum expectation, so

    0=p(O_A-O_B),  hence O_A=O_B.

The mandatory initial call contributes pi(B) pre-call visits to B. Thus

    E_pi tau = O_A+O_B >= 2pi(B)=2r/(1+r).                   (7)

The first-hit/residual-horizon construction with mean horizon r attains
this bound: B is a pre-call state only when the macro starts in B.
For the integer fast pair r=N, equations (3), (5), (6), and (7) are all sharp.

The corresponding general occupation-measure argument is useful to the
root's hidden-state extension. If a single P has a unique invariant probability
mu and a stopped endpoint kernel preserves nu with finite stationary mean
tau, its pre-call occupation measure M satisfies M P=M and M>=nu. If
uniqueness applies to the normalized finite measure M, M=c mu, so
c>=ess sup(dnu/dmu). For nu proportional to mu(1_A+r1_B), the root's
occupation identity attains c=r/Z when B has positive mass. Reducible P
needs componentwise treatment; a component wholly in A has a smaller
necessary cost and must not be assigned this global lower bound blindly.

## 5. Arbitrary ratios and the speed/cost distinction

For any 1<=r<=N, keep A_N as the high-direction rule. In the low direction
choose A_N with probability

    w=(N/r-1)/(N-1)

and B_N otherwise, interpreting N=1 separately. The low opposite probability
is w a_N+(1-w)a_N/N=a_N/r. Thus arbitrary ratios within (5) attain the
pointwise maximum high transition (6), if the required selectors are supplied.
Its pointwise expected calls are at most max(1/p,2), but for r<N this
fastest-amplitude mixture need not attain the minimum stationary cost (7).

An alternative draws a positive horizon H<=N with mean r. Starting at A,
stop at the first flip or H. Starting at B, use the low rule with

    Pr(L=ell)=Pr(H>ell)/r,  0<=ell<N.

Then a(p)=1-E[(1-p)^H] and b(p)=a(p)/r. The stationary cost is exactly
2r/(1+r). H on floor(r),ceil(r) suffices. The root proves the stronger
reversible hidden-state version, including diagonal blocks and native
occupation. This note does not replace that proof with an iid calculation.

## 6. Finite selectors, and an exact rational fallback

For r=N=2^b the fast pair needs exactly b fair bits for L and no ratio coin.
Known integer-energy Gibbs weights W=2^{-E}, with E integer-valued, give
precisely this clean family: choose N=2^{|Delta E|} on each local edge.
State/site selection, sensing, counters and boundary latency are additional.

For general N, uniform selection by fair-bit rejection uses unbounded
randomizer time. Likewise, a known real mixing weight is not automatically
a bounded-bit operation. These costs cannot be hidden in an ideal selector.
Precomputed selectors can be a supplied paid resource, but do not establish
a bounded total preparation time.

There is nevertheless an exact bounded-bit implementation of EVERY rational
ratio r in [1,N], at the cost of the slower amplitude. For integers 1<=m<=N
define C_{m,N}: allow up to m calls for the first flip; stop if none occurs.
After a first flip, continue until a second flip or until N total calls.
The opposite terminal event is exactly one flip among N calls, with its
first occurrence in the first m positions. Consequently

    F_{m,N}(p)=m p(1-p)^(N-1).                              (8)

For a dyadic a in [1,N], randomize m between floor(a) and ceil(a), with
the appropriate dyadic probability. This realizes slope a in (8) with
bounded fair bits. To obtain rational r=u/v in lowest terms, r<N, choose
D=2^b large and k=ceil(D/v) such that a=uk/D<=N; set c=vk/D. Then
1<=c<=a<=N, both a,c are dyadic, and a/c=r. Such a D exists because
a<r+u/D; D>=u/(N-r) suffices, with harmless equality handled by checking.
Use the a-slope and c-slope programs in the two directions. At r=N, use
the deterministic slopes N and1. Thus irrational target ratios are the
basic obstruction to exact bounded-fair-bit polynomial coefficients, not
all non-dyadic rational ratios. The fast pair's particular mixture can have
additional arithmetic restrictions that the slower family avoids.

This fallback is offered as an exact option, not an efficient recommendation:
its common mobility p(1-p)^(N-1) can be extremely small. Its rational
arithmetic and finite selector are checked separately by the executable.

## 7. Unbounded return is a strong ordinary alternative

Make one call. If it does not flip, stop. If it flips, continue until the
next flip and then stop. For p>0 this is an exact physical endpoint identity,
with expected native cost 1+p(1/p)=2 but unbounded duration. Mixing this
identity with a one-call proposal permits arbitrary invariant ratios, and
ordinary proposal/acceptance followed by physical return on rejection gives
the standard Metropolis kernel. A hard cap cannot be replaced by a bound
on expected calls: the all-no-flip derivative argument loses uniform tail
control in this example. This alternative retains its real return, sensing
and clock costs and is not ruled out to protect the bounded construction.

## 8. Interacting consequence and literal check

On a finite spin graph, suppose the addressed primitive for site i leaves
all other bits fixed and has the same p_i in both orientations of each
local edge. Conditional iid increments over a whole local excursion are
required here. The parameter may depend on frozen hidden disorder and
the fixed neighbour context. Use the same native choice in both directions
and implement the known Gibbs weight ratio by the pair above. Each compiled
local kernel obeys exact target detailed balance in every hidden sector.
A fixed scan or an independent fixed random scan therefore preserves the
target even outside a contraction regime. Hidden disorder remains visible
in time correlations. Finite calibration may select and freeze an operation
within this structural class without creating target-ratio error; it cannot
prove the structure or grant an arbitrary history-adaptive schedule.

The executable checks the complete four-site graph K4 at beta*J=log2,
with target weights 4^(number of agreeing edges), and different frozen
native p values (1/20,1/8,1/4,9/20). All local ratios are4 or64 and all
residual selectors use at most6 fair bits. A uniform site uses two more.
This is a strong-coupling fixture, not the earlier contractive ring.

Exact rational results:16 states;64 local rows;256 detailed-balance pairs;
positive diagonals; exact stationarity; hard cap64; target all-aligned mass
256/275; stationary native-call mean536/275=1.9490909.... All38,914 finite
path/selector cases for caps1 through10 also check the fast and slow
polynomial identities and literal stopping rules. All deterministic stopping
trees through cap4 check (4) and the sharp ratio bound. The full fitted
matrix is saved in `SHARP_GIBBS_EXACT_KERNEL.json`.

These are ideal population checks, not acquired counts or a demonstrated
physical device. Preparation from arbitrary hidden memory additionally needs
the sector and convergence conditions in `SECTOR_INVARIANCE_AND_PHASE_PRECISION.md`.
For a single source run without gaps, the raw native chain is unchanged:
biased completion states do not constitute biased physical-time equilibrium.
