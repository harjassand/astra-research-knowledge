# Polylogarithmic caps remove quantitative mixing and polynomial absorption requirements

Status: personally derived, UNREVIEWED. New extension, not a dependency of the frozen v1 bundle. The fixed hard-network application below retains the earned F and W_r from that bundle; it is not a general weakly reversible recurrence theorem.

## 1. Finite fibers yield a sufficiently crude bound
Suppose the conservative fiber at integer size N has at most C(1+N)^d states. After removing a common resource factor z^q, all total rates are at most C(1+N)^m. Suppose every state has a directed path to killing, with each enabled edge rate at least c>0. No equilibrium or mixing estimate is assumed.

A simple path to killing uses at most C(1+N)^d edges. Each step has probability at least c/[C(1+N)^m]. Before killing, the total rate is at least c. In blocks of at most C(1+N)^d jumps, success probability is at least exp[-C'(1+N)^d log(2+N)], uniformly at each restart. The expected block duration is at most C(1+N)^d/c. Hence

    sup E tau_kill <= z^(-q) exp[C''(1+N)^d log(2+N)].          (1)

This is an earned finite-graph bound, including the worst possible slow internal transport. Its assumptions are graph reachability and polynomial upper/constant positive lower bounds on enabled rates, not recurrence. Fixed-species mass-action conservative fibers with bounded positive rate constants satisfy the size/rate estimates whenever their graph reaches the killing set. The required reachability is NOT automatic.

## 2. Polylogarithmic cap and actual stopped process
Assume the actual residual s is preserved by conservative motion and killing; killing reduces N by a fixed integer. Assume resource z>=s, q>a>=0, and competing birth rate <=C z^a(1+N)^b. Take

    L(s)=floor((log s)^p),  0<p<1/d,
    D={s>s0, N<=L(s)}.

Stop at the actual first exit from D. The first-birth hazard before killing at size N is at most

    C s^(-(q-a)) (1+N)^b exp[C(1+N)^d log(2+N)].

Summing over the descending size ladder up to L(s) gives

    tail birth risk <= s^(-(q-a)+o(1)),
    tail stopped time <= s^(-q+o(1)).                         (2)

Here L(s)^d log L(s)=o(log s), since pd<1. Neutral births that remain inside D restart the tail with probability o(1); cap exits are terminal zero events. The geometric renewal bound is therefore uniform, without any invariant-cap assertion.

Suppose the earned fixed finite head has first-up risk O(s^(-v)), v>0, polynomial stopping time, and probability of exiting neutrally into the tail at most rho<1 uniformly for large s. This last condition gives a bounded head/tail renewal denominator even when a tail returns to the head with probability one. Head/tail renewal then gives first-up risk O(s^(-u)) for any fixed u<min(v,q-a), and polynomial mean excursion time. This last head assumption is indispensable, not established here for arbitrary graphs. For the existing hard network v=1, q-a=3, the head calculation already supplies the needed renewal bounds, and one may use any u<1.

## 3. A tilt compatible with the cap
Assume each nonzero residual exit is exactly +1 or -1, as in the hard network. For bounded upward jumps of size at most J, replace the condition below by alpha J<u and retain a uniformly nonzero downward jump. Choose

    0<alpha<u,
    phi(s)=Gamma(s+1)^alpha exp[(log s)^(1+p/2)].

For fixed integer j, the tilt ratio at s+j tends to1: its log derivative is (1+p/2)(log s)^(p/2)/s. Thus the +/-1 trace contraction is

    E[phi(s_next) 1_alive]/phi(s) <= C s^(alpha-u)+C s^(-alpha) ->0.

The same holds after multiplying phi by any fixed polynomial. The actual stopped cost W=E integral_0^T phi(s_t)dt is finite, bounded by poly(s)phi(s), zero outside D, and satisfies LW=-phi(s) inside D. This follows by the earned trace/time bounds and first-jump decomposition, not an assumed finite expected return time to a compact set.

## 4. Incoming forcing is still controlled in the hard-network application
Retain s=B-g_N, g_N=4 floor(N/3)+(N mod3). Outside D, only clearing can enter at large s: other reactions preserve N or increase it, and L(s+1)-L(s)<=1. Every incoming state therefore obeys

    L(s)<N<=L(s)+3,  B=s+g_N.

Its positive LW contribution is at most poly(s)phi(s). On this collar the existing earned F has negative drift for every composition, and W_r vanishes at current and all target states. Since F=(A!C!B!)^alpha here,

    log(phi(s)/F)
      <= (log s)^(1+p/2)-alpha log(B!/s!)
      <= (log s)^(1+p/2)-c alpha (log s)^(1+p)
      <= -c' (log s)^(1+p).

This beats every polynomial prefactor and thus absorbs the entire incoming forcing. Threshold leakage has finite support because N is capped at bounded s.

For bounded N and B->infinity, the tilt exp[(log s)^(1+p/2)] beats every fixed power of B, while B-s=g_N is fixed. The negative W drift therefore dominates the existing polynomial positive LF. Consequently F+W_r+W gives the same explicit-network global Foster conclusion, using only (1), not polynomial or summable absorption.

## 5. What changed, and what remains open
This replaces a quantitative fast-fiber stability condition by a finite-fiber accessibility condition, under an earned resource-order gap, finite-head downward bias, and quantitative outer-collar matching. The last requirement is stronger than negative drift alone: one needs log[F/Gamma(s+1)^alpha]>=c N log s on the incoming collar, a negative F margin of at least F times an inverse polynomial, and polynomial interface rates/value prefactors. For the hard network B-s=g_N supplies this separation. The condition z>=s by itself does NOT supply it. The growing cap's actual feedback is controlled; it is not assumed closed. No uniform mixing, spectral gap, stationary distribution, or polynomial hitting-time bound is required.

This does NOT show that an arbitrary weakly reversible network admits a suitable residual, a positive resource-order gap, an inward finite head, or an outer certificate F. In particular a growing cap cannot create inward bias in an all-zero residual component. Those are the remaining global structural issues. The point is that potentially exponentially slow conservative composition is no longer, by itself, an obstruction to this specific gluing mechanism.
