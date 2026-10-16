# Independent audit: flat-low product-envelope obstruction

## Verdict

**Valid for the stated class**, on the actual eight-site, open 2-by-4 Schlögl generator with the exact decimal rates in the supplied scientific synthesis. Any nonnegative differentiable backward supercaloric product envelope with every factor identically one at counts 0 through 15 must have initial value strictly greater than 0.26 at (50,...,50), deadline one. Strict positivity is sufficient but not needed for this obstruction.

This is a necessary lower bound on an UPPER ENVELOPE, not a lower bound on the actual eight-site hitting probability. The approximately 3.8e-8 quantity is a source-reported splitting estimate with substantial empirical error; this audit does not verify that probability. The obstruction already rules out a useful small upper certificate within this exact factor class, independently of the estimate.

Files: `check.py` is a newly written independent exact-arithmetic verifier; `result.json` records its successful execution. No producer script was executed. This is same-team independent reconstruction, not external mathematical review.

## Actual instance and assumptions

There are eight coordinates on the open 2-by-4 grid, ten undirected / twenty directed nearest-neighbor edges. Four vertices have degree two and four degree three. Each coordinate has birth rate

    b(n) = 2.676 n(n-1) + 108.102

and death rate

    a(n) = 0.040 n(n-1)(n-2) + 37.881 n.

Each directed diffusion edge i -> j has rate D n_i, D=8.2207. All decimals are exact rationals here. The target is A={max_i n_i <=15}; the retained box is {0,...,162}^8. First attainment of any coordinate 163 is failure overflow. The generator is stopped at target and killed on overflow, with value one on target and zero at overflow.

Let v(t,n)=product_i w_i(t,n_i), for chronological time 0<=t<=1, with w_i(t,k)=1 for every k<=15 and all t. Assume each factor is nonnegative, differentiable in time on continuation states (or sufficient absolute continuity for the comparison), with nonnegative terminal values. Assume

    (partial_t + Q) v <= 0

at every retained continuation state, with the stopped boundary just specified. The all-state condition matters. A certificate imposed only on a smaller subset does not inherit this theorem automatically.

## Exact sparse-state reduction

Fix vertex i and state n=m e_i, 16<=m<=162. Every inactive factor is identically one at zero and at one. Its time derivative at zero is exactly zero; differentiating v leaves only partial_t w_i(t,m). Births at inactive sites leave v unchanged, their deaths and departures have zero rate, and there are no arrivals into i from empty sites. A departure from i into a neighbor changes the active factor to w_i(t,m-1), while the receiving factor remains one. The active site's birth and death supply their original differences.

Consequently the exact inequality at this state is

    partial_t w_i(t,m)
      + b(m)[w_i(t,m+1)-w_i(t,m)]
      + [a(m)+degree(i) D m][w_i(t,m-1)-w_i(t,m)] <= 0,

with w_i(t,15)=1 and w_i(t,163)=0 interpreted as the failure payoff in this row. At m=162 the birth term is -b(162)w_i(t,162); it is not silently suppressed. At m=16 a departure leaves active count 15 and a receiving count one, hence is indeed a global target entrance.

For an unbounded nonnegative product envelope, its actual value at 163 need not vanish. Replacing that nonnegative boundary contribution by zero only decreases the generator, so the same killed scalar inequality remains necessary. Nonnegative overflow payoffs also preserve this implication. Negative overflow payoffs would not be admissible probability upper-envelope boundaries and are not covered.

The independent script directly enumerates all actual reaction and diffusion jumps for all 8*147=1176 sparse states and verifies the resulting rational coefficient dictionaries. It does not merely substitute degree into an assumed scalar formula.

## Time orientation and first-hit comparison

Let Y be the one-dimensional chain with births b and deaths mu_d(n)=a(n)+d D n, stopped upon hitting 15 or 163. Define sigma=tau_15 wedge tau_163 and

    q_d(s,m)=P_m(tau_15 <= s, tau_15 < tau_163).

This is a DEADLINE first-hit probability, not terminal low occupancy or eventual absorption probability. In remaining time s=1-t, u_i(s,m)=w_i(1-s,m) satisfies partial_s u_i >= L_d u_i. Its initial values at s=0 are nonnegative; its success boundary is one and its failure boundary zero. The finite-state comparison principle therefore yields u_i(s,m)>=q_d(s,m). Equivalently, applying optional sampling to the chronological supermartingale w_i(t,Y_t), stopped at sigma wedge 1, gives w_i(0,50)>=q_d(1,50), since success contributes one and the remaining terminal contribution is nonnegative.

Taking products of these nonnegative scalar inequalities is purely algebraic. It does NOT assert independence of the original eight-site coordinates:

    v(0,(50,...,50)) >= q_2(1,50)^4 q_3(1,50)^4.

## Exact finite-deadline lower certificate

Independent enumeration over every integer 16<=n<=162 proves

    mu_2(n)-b(n) >= c_2=415031/2500, minimum at n=31;
    mu_3(n)-b(n) >= c_3=961869/2500, minimum at n=16.

For f(n)=n, the stopped generator satisfies L_d f<=-c_d before sigma. The stopped state is always at least 15, including upper exits. Dynkin's formula at sigma wedge t gives

    c_d E[sigma wedge t] <= 50-E[Y_(sigma wedge t)] <=35.

Monotone convergence proves E sigma<=35/c_d, in particular sigma is finite almost surely. Markov's inequality gives P(sigma>1)<=35/c_d. Therefore

    q_d(1,50) >= 1-35/c_d-P_50(tau_163<tau_15).

There is no eventual-to-deadline leap here: the expected stopping time bound explicitly controls the deadline tail. The event inclusion used is that failure to reach the lower boundary by one is contained in {sigma>1} union {upper boundary reached first}.

The exact scalar overflow probability H_d is computed by positive increments Delta_16=1 and

    Delta_(n+1) = mu_d(n) Delta_n / b(n), 16<=n<=162;
    H_d(m) = [sum_(k=16)^m Delta_k]/[sum_(k=16)^163 Delta_k].

The checker independently verifies both boundaries H(15)=0, H(163)=1 and every rational harmonic equation b(n)(H(n+1)-H(n))+mu_d(n)(H(n-1)-H(n))=0. Uniqueness of the finite absorbing-chain Dirichlet problem identifies these values as actual first-upper-exit probabilities. It verifies exactly H_d(50)<10^-20 for both degrees; descriptive values are approximately 2.97457e-26 and 1.65618e-27.

Define the deliberately conservative rational lower bounds

    ell_2 = 32753099999999999999584969 / 41503100000000000000000000;
    ell_3 = 87436899999999999999038131 / 96186900000000000000000000.

These are 1-35/c_d-10^-20. Exact integer arithmetic verifies

    ell_2^4 ell_3^4 > 26/100.

Its descriptive decimal is 0.2648517164359188796903574063253095047505. This independently reproduces the claimed obstruction with a slightly weaker certificate than using exact H_d values. Decimal rendering is not used to prove any comparison.

## Limits and provenance

- The flat value ONE for every low count at every time is essential. Merely requiring the PRODUCT to be at least one on the target does not imply those factorwise assumptions.
- Arbitrary non-flat factors, pairwise or larger cluster factors, sums of products, and general tensor representations are not ruled out.
- This is a necessary-condition obstruction, not a proof that the comparison product itself is globally supercaloric or is the optimal envelope in this class.
- Adding the existing global overflow budget cannot repair a lower bound already greater than 0.26.
- The exact checker uses the supplied actual rates/topology, corroborated against `/workspace/shared/pr102_review/SCIENTIFIC_SYNTHESIS.md`. No functional repository checkout was available here; this audit does not independently verify correspondence to Git commit 3e8a972f... . Pin/source provenance must remain attached to the parent's repository acquisition, separately from this arithmetic proof.
- No new probability estimate, eight-dimensional interior solve, compressed useful envelope, or practical rare-event speedup was established.
