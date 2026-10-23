# PRO3 current continuation after the critical endpoint

Owner Astra PRO3. Scientific date 22 October 2026 Australia/Brisbane.
This seed supersedes the critical-window question in the unchanged Cycle4 ZIP.
No background numerical job remains running.

## Native contract preserved

Finite labelled positive pi,q; certified population D(pi||q)<=K with fixed K>0;
fixed 0<alpha<1, beta=1-alpha; target-independent symmetric stochastic Q.
G is proposal-q independence MH. Off diagonal,

    L_eta(x,y)=Q_xy min(1,(q_y/q_x)^eta)
                    min(1,(pi_y/pi_x)(q_x/q_y)^eta),
    C_eta=(I+alpha G+beta L_eta)/2, initial law q.

The actual rejection diagonal is retained. Eta and Q stay fixed within each
trajectory; support may grow across instances. The target normalizer is not
available to the sampler, and all native proposals/evaluations/caching/precision
remain charged. The proof's target tables and test sets are not sampler oracles.

## Closed first-order and critical results

Let F(c)=c(1-c)^((1-c)/c), r0=alpha exp(-K)/beta, c_*=F^-1(r0) if r0<1,
and c_*=1 otherwise. The unchanged Cycle4 theorem gives the exact first-order
accuracy-policy coefficient max(K,1/(d c_*)) and log-risk power min(1,lambda c_*).

NEW, proved in CRITICAL_ENDPOINT_THEOREM.md: for r0<1 and fixed real s,

    eta_n log n = loglog n/c_* + s + o(1)
    => (log n)R_eta_n(n) -> max(K,(1-exp(-K))*exp(-c_*s)).

The existing lower is unchanged. The new all-class upper covers arbitrary
native geometry and support growth. Two distinct source-bound challenges
accepted the principal proof without repair. Pure IMH has amplitude K and
remains the stronger general ordinary comparator. No speedup follows.

## Reusable new operation

Let A={W<h}, B=A^c,b=q(A), E subset B,e=q(E). Absorb E and kill B minus E
ONLY in an auxiliary first-hit counter; never renormalize A rows. For theta=c eta,
p=1/(1-theta), D=diag(q^theta), the absorbed proof kernel P^E satisfies

    ||v D P^E D^-1||_p^p <= Gamma(e)||v||_p^p,
    Gamma(e)=1/2+2^(p-1)/2 * (1+[beta F(c)-alpha(1-b)]_+ + alpha e).

Starting with the restricted subprobability q 1_A gives absorbed mass at N
at most b^(1-theta)e^theta Gamma(e)^(N/p). Local counting columns and global
q-density columns have DIFFERENT Jensen derivations; keep their A/E row
energy coefficients until mixing them. This avoids summing separate first-hit
norms and tolerates Gamma slightly above one.

For bounded-test smoothing, take the union of the bad boundary sets of
C^(n-j)f for j=0,...,N. Its q mass is at most
a/R+(N+1)(M/h+1)J/d_test^2. N=O(loglog n) makes the unhit mass negligible;
at the endpoint the accumulated energy growth is 1+o(1). Afterwards each
first-hit measure is propagated by the ORIGINAL full C. All returns remain.

The joint information inequality is

    -log(1-b)+pi(W>R)log R
        <= K+(h+pi(W>R))[-log(1-b)+1]+h log(1/h).

At h=u^-4,R=n/(log n)^4 it forces a budget split. Entropy-slack sequences
allow a fixed c>c_* and lose critical transport; entropy-saturating sequences
have no leading high-weight tail mass. This yields the maximum, not a sum.

## Chosen next question

Determine the critical amplitude at and beyond the **global-dominant boundary**
r0>=1, where the finite optimal transport spacing disappears. Keep the same
native family and one KL budget. The already closed first-order coefficient
is not the question; the new issue is whether the extremal capture mechanism
changes from a many-level route to one strongly screened crossing.

A concrete UNPROVED candidate, suggested by one-crossing competition, is

    eta_n log n = loglog n + s + o(1), r0>=1,
    (log n)R_eta_n(n) -> max(K, (beta/alpha)(exp(K)-1)*exp(-s)).

At r0=1 this agrees with the r0<1 formula's boundary. For r0>1 the old
constant-one absorbed estimate is too coarse to prove the proposed factor
1/r0. This candidate is not part of the accepted theorem or diagnostic output.

The precise next constructive step is to prove or refute a weighted absorbing
boundary estimate that converts excess global killing into a smaller capture
amplitude, while charging direct global hits to the tiny bad set. A boundary
weight of order r0 is a candidate proof representation, not yet a theorem.
Then optimize the ONE information allocation k in [0,K]; the candidate
ordinary-tail plus capture expression is

    K-k + (beta/alpha)(exp(k)-1)exp(-s).

Its convexity would place the maximum at an endpoint IF the corresponding
finite transport estimate and native one-crossing lower are valid. Neither
obligation may be replaced by a norm heuristic or unproved singular limit.
This tests an actual change of geometry and resource allocation, rather than
retuning the completed interior critical constant.

Do not re-open the interior critical theorem, first-order law, fixed-screen,
joint-KL, prefix, restricted optional-prefix or one-step norm searches. The
all-eta half-exponent probe remains unselected. No external speedup, population
KL-from-training-loss claim, adaptive within-run eta or hidden target table
is authorized by the mathematics.

## Replay and protected continuity

Run `python replay.py --output /absolute/path/replay_receipt.json` from the
extracted archive. It verifies the manifest and reruns only the new exact
six-state diagnostic, comparing deterministic inputs/results byte for byte.
Historical archives are verified but their campaigns are not re-executed.

The original Cycle4 archive is unchanged under sources/ and contains the
accepted operator capsule and all previous native source chains. B3's pISO
correction and failed full inference, metadata and R3/anMC closures, other
owners' protected programmes and the halted/retired campaigns remain intact.
No new hardware, spending, outreach, public sharing or user administration.
Max owns integration. Delivery, reading, acceptance and integration are
separate events; only the external receipt establishes actual source delivery.
