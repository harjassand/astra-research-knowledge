# Final source-bound review: reciprocal-proposal critical theorem

Reviewer: `/root/reciprocal_energy_challenge`. Scientific date: 22 October
2026, Australia/Brisbane. This review is distinct from the earlier focused
local calculation. It binds the assembled principal proof below and does
not alter any predecessor source.

## Exact source and verdict

Reviewed the complete `RECIPROCAL_PROPOSAL_THEOREM.md`:

- Bytes: **21,709**.
- SHA256: **584c2fcbedcead37578b91596ace85eeb75426537d564cdd646d44831f4dbc6a**.
- The file was read in full; its bytes and SHA256 were then independently
  compared against the principal's frozen identity.

**ACCEPT WITHOUT REPAIR for Theorem 1 and its Sections 2-7 proof**, conditional
on the unchanged, already accepted symmetric lower constructions explicitly
identified in Section 7. The new local operation is correct; its complete
finite absorption interface and the uniform all-return/one-budget upper
prove the enlarged-class critical limits. No extra symmetry, stationarity,
degree bound or minimum-probability hypothesis has been introduced.

The separate counterconstruction named in Section 8 is **outside this
review**. The principal owns its independent acceptance. This review does
not certify that claim merely because the theorem file refers to it.

I did not re-audit the old branching lower, run old scientific suites, or
audit implementation speed. Historical originality, formal verification,
external mathematical acceptance and practical performance remain unknown.

## 1. New local weighted-energy operation

The precise new class is positive finite pi,q with a fixed target-independent
row-stochastic Q having reciprocal off-diagonal support. The screen uses
the full flow ratio r=q_y Q_yx/(q_x Q_xy), and the second reciprocal factor
uses the full target Hastings ratio. A nonreversible proposal Q is permitted;
the resulting target kernel is reversible.

The auxiliary B used in (7)-(9) is correctly oriented:

- B_xy=Q_yx off diagonal from A into S;
- B_xx is the actual rejection diagonal on A;
- B_xx=1 on absorbed E.

For each output y the sum is controlled by an OUTGOING row of Q at y,
not by a generally unbounded counting column of Q. Its total is at most
two. Reciprocal support ensures the denominator is positive wherever the
retained off-diagonal transition is positive; diagonal zero terms are
omitted. Thus the weighted Jensen step is valid even with arbitrarily
small positive reverse proposal probabilities.

The cancellation p-1=theta p gives exactly

    T_xy^p/B_xy^(p-1) = Q_xy a_xy^p r_xy^(-theta p).

This identity is the required whole-energy mechanism. An estimate on the
unpowered off-diagonal alone would not imply it.

In (10), the true rejection diagonal first subtracts accepted outflow
over every original edge. Only then is the negative contribution from
the killed complement discarded. For r>=1 the weighted defect is at
most w-1. For r<1 its convex dependence on a reduces its maximum on
[0,r^eta] to zero or the endpoint r^eta. This yields the exact H_w
in (4), including its piecewise expression (5).

At theta=eta, H_w=w as a supremum; finite positive attainment is not
claimed. At theta=c eta, w=1, the exact finite scalar is F(c_eff) with
c_eff=c(1-eta)/(1-c eta)<=c. Since F is increasing, replacing it by
F(c) is an upper bound in the correct direction. The proof does not
silently set c_eff=c. These facts establish Lemma 2 with the full
diagonal and both required interfaces.

## 2. Global mass, absorbed mixture and initial energy

The G component is unchanged by proposal asymmetry. From A={W<h}, every
G proposal into B is accepted. Its exact row mass on A is b, including
the original rejection diagonal. The q-density Jensen column bounds
2b on A and 1+b on E follow as stated; the weighted actual row masses
are b+w e on A and w on E.

This density calculation is properly kept separate from the reverse-Q
Jensen representation. Combining the components with the actual lazy
mixture coefficients gives the A bracket

    alpha(b+w e)+beta(1+H_w)
      =1+beta H_w-alpha(1-b)+alpha w e.

The E coefficient relative to its weighted input is one. The positive
part in Gamma bounds both, so (13) is valid. With v=q1_A D^-1, the
initial transformed p-energy is exactly b, not one and not a conditional
starting density. Iteration and weighted Holder yield (14).

P^E has the original A rows restricted to S, while E is absorbing and
other exits are killed. Its rows are not normalized. Therefore (11)
is the exact original first-B-hit event from the restricted starting
subprobability. All times accumulate in a single vector. This does
not assume strict contraction and creates no extra sampler oracle.

## 3. Full-return finite certificate

For each positive edge, the two reciprocal factors give
a_xy/a_yx=t_xy, proving pi-reversibility of Lbar. The lazy mixture
then has spectrum in [0,1]. Proposal Q need not have any stationary
distribution used by the proof. The independent-MH Dirichlet form and
the alpha/2 component give the same anchored bounded-test estimate.

The constants in (17) check:

- Restriction of the y Dirichlet sum to A0={W<=M} gives a lower bound
  pi(A0)/2 times the weighted anchored square deviation.
- pi(A0)>=1/2 and D_Cbar>=alpha D_G/2 imply the factor 8/alpha.
- Spectral decay bounded by 1/(2t+1), and Var_pi(f)<=1/4, give
  2/[alpha(2t+1)].

The single test-dependent E covers all j=0,...,N. It includes the
high-W tail and every relevant anchored-test deviation. Its q mass
is bounded by the same bar e, uniformly over bounded tests. No
unobserved test set is provided to the actual sampler.

Equation (18) then propagates each first-hit measure through the
ORIGINAL remaining Cbar, including all later global attempts, exits
and returns. The exceptional absorbed matrix is used only to count
first-hit mass. Bad initial hits cost q(E); later bad first hits cost
(14); good hits and stationary comparisons are weighted by first-hit
mass whose total is at most one. The remaining no-hit mass costs
b rho^N. These are exactly the terms of (16).

Consequently no return was discarded, no killed row was conditioned,
and no deterministic horizon was replaced by an optional count.

## 4. One-budget information controls and uniformity

The binary and three-cell entropy bounds involve only pi,q. They
therefore survive the enlarged Q class without additional constants.
For the three-cell inequality, d=pi(A)<=h b. The derivative used in
the proof is nonpositive when d<=b(1-a); h+a<=1 makes the replacement
d=h b valid. The resulting k+a log R upper uses one KL budget, not
independent allocations K to both tails.

With u of order loglog n and cutoffs (21), the estimates for bar e
are support-uniform: the uncapped argument is bounded above by a
constant times n^-1 (log n)^4 u^5 and below by a positive constant
times n^-1 (log n)^4, while 1-b stays uniformly bounded away from
zero. Thus the cap is eventually inactive, log bar e=-log n+
O(loglog n), and its powered asymptotic is uniform.

The proof separately controls the accumulated multiplier through
N theta, N Delta and N bar e. Merely having Gamma->1 would not
suffice, but that insufficient premise is not used. The bound
x^(1-theta)<=x+theta handles arbitrarily small b additively; no
uniform lower bound on an individual q atom is smuggled into an
expansion. The no-hit term follows from the actual accepted global
escape probability, with b rho^N<= (log n)^-2 eventually.

All constants depend only on fixed K,alpha and the fixed critical
offset/policy, not on degree, proposal asymmetry, support size,
target/proposal minimum atoms or a stationary measure for Q.

## 5. Interior critical upper

At c=c_* the inequality H_1<=F(c_*) gives a deficit bounded by the
already controlled O(h log(1/h)). This proves the uniform sum upper
(23) in the enlarged class.

The subsequent information allocation is necessary and valid. Along
any sequence of instances, bounded k has a convergent subsequence.
If its limit is less than K, a fixed c strictly above c_* makes
beta F(c)<alpha exp(-k_limit). This c remains below one, meets the
finite local lemma eventually, and supplies a zero eventual deficit.
The first-hit transport then vanishes faster than 1/log n. If the
limit is K, the same single information inequality forces the
leading high-W tail mass to vanish and leaves only the transport
amplitude. The near-supremum contradiction correctly handles the
class supremum without assuming it is attained.

This proves the interior upper for the enlarged class. It does not
reopen or need a second proof of the old symmetric lower.

## 6. Global dominance and the equality boundary

At theta=eta the exact local interface is H_w=w. The canonical
w=max(1,r_b), r_b=alpha(1-b)/beta, therefore gives exactly

    Delta_w=[beta-alpha(1-b)]_+.

For r0>=1 this is O(h log(1/h)), including r0=1 where the finite
cutoff can leave r_b slightly less than one. The proof never divides
by r_b-1 or assumes a positive uniform gap. The weight stays bounded
by max(1,alpha/beta).

Equation (25) supplies the correct accumulated Gamma bound. Its
additive small-b control leads to b/r_b=(beta/alpha)(exp(k)-1).
The finite entropy allowance delta_n tends to zero and places k in
the actual interval [0,K+delta_n]. The convex maximum in (27) is
therefore justified only after the transport and one-budget premises
have been established. Both endpoints and the resulting limit have
the stated constants. No new difficulty arises from arbitrary Q
because its dependence has already been removed by Lemma 2.

## 7. Lower inclusion and the claim's scope

For symmetric Q, the full proposal factors reduce exactly to q_y/q_x
and pi_y/pi_x. Both off-diagonal entries and actual rejection diagonals
therefore match the old native kernel at every finite time. Every old
admitted symmetric lower family belongs to the enlarged class.

Conditional on the explicitly preserved accepted lower proofs, exact
inclusion supplies the matching liminf. No new limiting argument in
Q, perturbed proposal, or nonattained norm extremizer is needed.
The ordinary Q=I family and the appropriate transport family are
separate admitted families, so they supply a maximum without spending
K twice.

I have not re-audited the accepted tree construction or its finite
checks. The Section 7 inclusion is the reviewed new interface. The
main file identifies the unchanged lower dependencies rather than
pretending to derive them from a favorable finite numerical curve.

Theorem 1 proves equality of the LEADING critical minimax limits.
The sentence that proposal asymmetry cannot increase the critical
minimax risk is understood in that explicit asymptotic sense. It
does not establish pointwise finite-time TV ordering between arbitrary
proposal kernels. The surrounding scope exclusions and ordinary
IMH comparison make that distinction correctly.

## Resources and review independence

First observed final-review clock: 2026-10-22 02:28:56 UTC
(12:28:56 Australia/Brisbane). The principal's exact file was read
in full and hashed. No numerical jobs, old scientific replay,
network queries, paid resources or unrelated owner work were used.

The earlier focused challenge checked the local lemma before the
assembled principal source existed. This final review now checks
its integration into the complete claimed upper and exact lower
inclusion. It is a continuation of one reviewer, not two independent
audits counted twice. Model inference, token, total discovery and
monetary costs are unknown. A separate JSON receipt records the
final review's identity and observed completion time.
