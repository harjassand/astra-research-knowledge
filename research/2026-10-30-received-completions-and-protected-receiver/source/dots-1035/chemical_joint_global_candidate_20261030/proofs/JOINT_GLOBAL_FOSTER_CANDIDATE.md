# Candidate global Foster construction for the explicit coupled rank-three network

Status: INTERNALLY CHECKED CANDIDATE. The existing child reviewer passed the complete coupling in INDEPENDENT_JOINT_GLOBAL_FOSTER_AUDIT.md; a separate whole-proof review and novelty verification remain outstanding. This is a candidate theorem for the one explicit nonlinear network below, plus reusable trace/value mechanisms. It is NOT general weakly reversible recurrence and carries no novelty clearance.

## Network and dependencies
Species A,C,B. Connector cycle 0→A+B→3A+4B→0 has unit constants. The reversible fast chain is

    3C+4B ↔ A+2C+4B ↔2A+C+4B ↔3A+4B,

with increasing-A constants6,1,7 and decreasing-A constants12,1,1.

Use the already checked fractional-factorial bulk theorem, EXACT_LOW_PHASE_FORCING_CLOSURE.md, and INFINITE_PHASE_FIRST_EXIT_CONTRACTION.md. The complementary actual trace is in COMPLEMENTARY_ACTUAL_COMPOSITION_TRACE.md and must also pass review. No stationary distribution or global recurrence is assumed in any construction below.

Write N=A+C. Select one rational alpha in (0,1/2) admissible for the existing bulk theorem. Let F be the explicit exact low-B Poisson correction of (A!C!B!)^alpha. It is globally positive and normlike.

## 1. Convert an earned trace contraction into a finite stopped-cost value
The following elementary step is used twice. Suppose a residual z has jumps ±1 at its successive nonzero-exit times, each neutral excursion is nonexplosive, and uniformly over all other coordinates (and controls, if present),

    P(up)<=C/z,      E(excursion time)<=C z^12.

For phi(z)=exp(k z)Gamma(z+1)^alpha with any fixed k, choose z0 sufficiently large that Psi(z)=(1+z)^12 phi(z) satisfies

    E[Psi(z_next)] <= (1/2)Psi(z),   z>z0.

This follows from the exact factorial ratios and alpha<1. Conditional iteration gives a finite expected sum of Psi over residual excursions, uniformly over all other coordinates. The expected number of excursions before z<=z0 is finite as well, because Psi has a positive minimum for z>z0. Thus the stopped process is nonexplosive, and the value

    V_z(x)= E_x integral_0^T phi(z_t) dt,
    T=inf{t:z_t<=z0},

is finite with V_z(x)<=C(1+z)^12 phi(z), uniformly in the hidden coordinates. In a controlled model take the supremum over all admissible policies; the same bound holds.

Set V_z=0 on z<=z0. In the uncontrolled model, conditioning on the first jump gives LV_z=−phi(z) for z>z0. In the controlled model, fix any allowed row until the first jump and then concatenate epsilon-optimal continuation policies at the finitely many possible targets. Letting epsilon→0 proves L_row V_z<=−phi(z) for EVERY allowed row. This directly earns the common generator inequality; it does not assume an optimal policy, regularity, or an existing Lyapunov barrier.

## 2. The r-value: cone-qualified, but defined at every B
Use h_B from the first trace and r=N−h_B. Its elementary bounds are

    2B/3 <= h_B <= 2B/3+1.

Choose epsilon0 in (0,1/2) so F has negative drift in both extreme composition sectors t=A/N<=epsilon0 or t>=1−epsilon0, for large N. Choose 0<epsilon1<epsilon0. Let H(t) be binary entropy and choose

    alpha H(epsilon1) < d1 < alpha H(epsilon0).

Construct the controlled projected r-value W_r by Step1 with

    phi_r(r)=exp(−d1 r)Gamma(r+1)^alpha.

The coefficient intervals include the actual connector coefficients whenever A>=epsilon1 N: activation factor A/N and clearing factor (A)_3/(N)_3 lie in fixed positive compact intervals for large N. The first infinite-phase trace theorem therefore yields W_r, defined for ALL N,B (zero at r<=r0), with

    0<=W_r<=C(1+r)^12 phi_r(r),
    L_physical W_r<=−phi_r(r)   if r>r0 and A>=epsilon1 N.

Fast composition reactions contribute exactly zero, even if their jump leaves the cone. No physical cone invariance is assumed.

For each fixed finite range of B, the first holding-time cost in the projected model also gives

    W_r>=c_B r^(−3) phi_r(r),   r large.

This lower bound is not needed for the generator comparison below but records the function's actual factorial scale.

Outside the coefficient cone, discard all negative generator terms. Actual connector rates are polynomially bounded, and every target residual is at most r+1. Since r>r0 implies B<=3N/2, the uniform value bound gives

    (L W_r)^+ <= C N^D phi_r(r),   r>r0,

for a fixed D. If r<=r0, the only possible jump from W_r=0 into its positive domain is an immigration from r=r0; its rate is1 and the target value is uniformly bounded over B. Thus (L W_r)^+<=C on r<=r0.

## 3. The s-value: actual at every composition
Use g_N=4floor(N/3)+(N mod3), s=B−g_N, and any d2>0. The complementary actual trace gives Step1 with

    phi_s(s)=exp(d2 s)Gamma(s+1)^alpha.

Define its ACTUAL stopped-cost value W_s. Then

    0<=W_s<=C(1+s)^12 phi_s(s),
    L W_s=−phi_s(s)    for s>s0,
    W_s=0             for s<=s0.

The only possible positive generator contribution on s<=s0 is an activation from s=s0 to s0+1. The target value is bounded uniformly over all N,A by the trace-value bound. Hence

    (L W_s)^+ <= C AB <= C NB   on s=s0,
    L W_s=0                    on s<s0.

For every fixed finite N range, the first physical holding-time cost gives

    W_s>=c_N s^(−4)phi_s(s),   s large.

Again no full-process nonexplosion is assumed here: the trace construction proves nonexplosion up to the relevant stopping target before defining the value.

## 4. F+W_r already has negative drift for ALL large N, uniformly over B
Let U=F+W_r. There is a fixed B0 such that, for large N, F can have positive drift only when

    epsilon0 <= A/N <= 1−epsilon0,    4<=B<B0.

Reason: F is negative at all B<4 and in both extreme-composition sectors. In the remaining balanced cone A,C grow linearly with N. For B>=B0=max(8,K_bulk), F and the bulk factorial function agree at every reaction target, so the previously earned bulk inequality applies.

On the potentially bad set B<B0, r=N−O(1), and

    log[phi_r(r)/F]=N[alpha H(A/N)−d1]+O(log N).

Its exponent is uniformly positive in the balanced cone. Therefore the negative term −phi_r(r) dominates every polynomial multiple of F, including (LF)^+. This closes the bad-F region.

Where A>=epsilon1 N and r>r0, W_r is already nonpositive in drift; wherever F is also negative no matching is needed.

Where A<epsilon1 N, F is negative. Its negative margin is at least F times an inverse polynomial in N (and is much stronger for B>=4). The positive W_r drift is exponentially negligible UNIFORMLY over B with r>r0. To see this, use F>=(A!C!B!)^alpha and split:

- If B<=eta N, then r>=N−2eta N/3−1. Choose eta>0 small enough that d1(1−2eta/3)>alpha H(epsilon1). The factorial comparison gives phi_r/F<=poly(N)exp(−cN).
- If B>=eta N and r>r0, then N−r=h_B>=2eta N/3. The ratio r!/N! has logarithm at most−c_eta N log N, overwhelming the at-most-linear entropy term. Again phi_r/F is superpolynomially small. Also B<=3N/2, so all rate prefactors remain polynomial in N.

Finally, if r<=r0 and N is large, then B is at least a positive multiple of N. F is negative by the bulk/extreme-sector alternatives, with factorially large magnitude, and absorbs the bounded positive LW_r.

Consequently LU<0 for every sufficiently large N and every B. Away from the finite-B bad-F cone, its negative magnitude is at least F times an inverse polynomial in N; in that bad-F cone it is at least a fixed fraction of phi_r(r). These quantitative margins are part of the construction, not just a sign assertion.

## 5. Add W_s and close the last unbounded cylinder
Set

    V=F+W_r+W_s.

For N large, W_s has nonpositive drift except on s=s0. On that slice B=g_N+s0 is asymptotic to4N/3. Thus B>=B0 and F has negative drift by bulk/extreme-sector alternatives. The preceding U estimate there has factorially large negative magnitude, which absorbs the polynomial bound C NB for positive LW_s. Hence LV<0 for all sufficiently large N, uniformly over B.

Now restrict N to the remaining finite range. For B sufficiently large, r=N−h_B is far below r0, so W_r and every target W_r are zero. Meanwhile s=B−g_N=B−O(1)>s0 and

    L W_s=−phi_s(s).

Here F=(A!C!B!)^alpha and (LF)^+<=poly(B)F uniformly over the finitely many A,C choices. But

    phi_s(B−g_N)/F >= c exp(d2 B) B^(−D),

so the negative s-value drift dominates. This closes the actual bounded-N/large-B cylinder; no closed finite corner is assumed.

There is therefore a finite set outside which

    L V <= −1.

V is finite everywhere and normlike because F is. Its generator involves only finitely many finite-rate jumps at each state. Standard stopped Foster localization yields global nonexplosion and positive recurrence of every closed irreducible class. The physical reaction graph is weakly reversible, so its communicating classes are closed.

The same estimates dominate exp(theta(N+B)) outside a finite set for every fixed theta>0: the relevant negative margin is either factorial F, phi_r with bounded B, or phi_s with bounded N. Stopped regeneration therefore yields all exponential moments of N+B in each stationary class.

## Scope and review obligations
This candidate closes all boundaries of THIS explicit three-species, deficiency-two, multistable-fast network if every dependency and value-function gluing step survives review. It does not solve general recurrence, establish a new efficient algorithm, or certify novelty. In particular the finite-head degree certificates, the prior killed-shell exponent, controlled-value construction, and uniform entropy estimates must all be audited together before this is promoted from candidate status.
