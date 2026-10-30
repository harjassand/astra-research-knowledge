# General killed-fiber absorption and summable tail criterion

Status: personally derived, not yet reviewed. This is a reusable analytic ingredient, not a recurrence theorem by itself.

Let a finite conservative fiber have total population N and a distinguished count a in [0,N]. Hidden composition may have arbitrary dimension. Suppose fast transitions change a by uniformly bounded increments, total fast rate is at most C N^D, and their drift in a is at least c N^D whenever a<=epsilon N. Kill at rate at least c_0(a)_D, for an integer D>=1. Assume all constants are uniform over hidden composition and N sufficiently large. No mixing or stationary fiber distribution is assumed.

Set s=N^(D/(D+1)) and W_N(a)=(a+s)^(-D). Bounded-jump Taylor expansion gives

    Q W_N <= -D drift_a/(a+s)^(D+1)
             + C N^D/(a+s)^(D+2)
             - c_0(a)_D/(a+s)^D.

For a<=s the negative drift term is bounded away from zero since N^D/s^(D+1)=1. For s<a<=epsilon N, the killing term is bounded away from zero and the negative drift absorbs Taylor error. For a>=epsilon N, the absolute fast contribution is O(1/N), while killing is bounded away from zero. Thus QW_N<=-c_1 uniformly, and

    sup_x E_x tau_kill <= C N^(-D^2/(D+1)).

Only the displayed drift/rate inequalities supply the hypotheses; the function W is explicitly constructed.

Suppose now that between such killing events, a phase/resource factor z^q multiplies both fast and killing rates, while competing births have intensity at most C z^p N^b, with p<q. Each kill reduces N by a fixed positive amount and keeps a residual z bounded below by a large parameter S. Then

    P(birth before next kill) <= C S^(p-q) N^(b-D^2/(D+1)).

If

    D^2/(D+1)>b+1,

the sum over the decreasing N ladder converges uniformly over arbitrarily large initial N. This yields a true infinite-fiber tail return estimate O(S^(p-q)), not just a bound on each fixed fiber. In particular b<=D−2 is sufficient, since D^2/(D+1)=D−1+1/(D+1).

The actual hard-network trace uses D=3,b=1,q=4,p=1, producing the summable N^(-5/4) risk. This lemma identifies which part of that construction is structural and which numerical exponent is incidental. It does not assert these inward-drift and rate conditions for arbitrary weakly reversible networks.
