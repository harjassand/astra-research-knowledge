# Sparse restart without initial-pattern independence

29 October2026. Root extension of the accepted c_classical_eroder
construction. Independent challenge pending. No new physical primitive
or trajectory run. This is a potential handoff lemma, not a completed
noisy asynchronous communication protocol.

## 1. Uniform over every sparse initial pattern

Keep the accepted register's private Poisson clocks, monotone three-poll
updates and independently clocked supported faults. Fix a bit b to retain.
Let gamma=1/4096 and h=ceil(n/256), h>q. The old spectral/birth/death
inequalities still hold below this SMALLER exit threshold, because h's
pre-exit wrong density is at most1/256<1/64. For a fixed initial wrong
set of size m0<=floor(gamma n), the accepted argument gives

 P(exit by L) <=n(1+lambda)L 2^(m0+q-h)
                                  exp[2n lambda(2^q-1)].  (1)

This event already maximizes over ALL future-dependent fault labels by
the all-wrong monotone coupling. Now take a literal finite union over
ALL initial wrong sets of size<=floor(gamma n), rather than invoking
Markov drift after a future-selected initial state. The binomial entropy
bound gives at most exp[n H(gamma)] such sets, where

 H(gamma)<=gamma log(e/gamma)=(1+12log2)/4096.

Meanwhile (h-m0)log2>=15n log2/4096. The remaining exponent after the
union is therefore at most

    -n(3log2-1)/4096 +2n lambda(2^q-1)
       <=-n/4096+2n lambda(2^q-1),

using log2>=2/3. If lambda(2^q-1)<=1/16384, conclude

 P(there EXISTS an initial wrong set of size<=floor(n/4096)
       whose trajectory exits h by L)
   <= delta_*(L):=min{1,2^q n(1+lambda)L exp(-n/8192)}.   (2)

The initial set MAY NOW depend arbitrarily on the entire future schedule.
For a bit b itself chosen using future randomness, union the b=0 and b=1
events, costing only an additional factor2. This is stronger than a
uniform marginal bound over deterministic starting states: the supremum
over starting states is INSIDE the probability. Its smaller initialization
density and weaker exponential constant are explicitly paid.

The binomial entropy inequality applies also when gamma n is not an
integer. One proof uses a Bernoulli(gamma) measure: each set of size at
most gamma n has mass at least gamma^(gamma n)(1-gamma)^((1-gamma)n).

## 2. A copy clean enough to meet that restart density

Keep the old copy operation but use ell=32 walks (288 fair bits per
three-poll update), not ell=16. Graph radius is32 for restoration and33
for two-layer copy. The update support still has at most four bits and
the old per-bit generator-strength bound is unchanged. These atomic
access and randomness costs are model inputs, not fabricated hardware.

In this section the source initialization must be FIXED independently of
future primitive clocks/coins, as in the accepted original copy theorem.
Source evolution can depend on past destination events, only insofar as
the specified no-feedback copy model permits; it cannot consult future
destination coins through an anticipative initial pattern. This premise
is stronger than merely being on the uniform good event of Section1.
Suppose the source remains below h=ceil(n/256) over the relevant window.
Writing F for the total unweighted probability of a wrong nominal copy
output, the exact expander estimate gives

    F<=F0 n,
    F0=3[1/256+(25/32)^32]/256.                          (3)

For the destination wrong set B, j=|B|, and fixed rates r_i in
[15/16,17/16], its nominal exponential generator is EXACTLY

 G_nom 2^j/2^j
   = sum_(i outside B) r_i p_i
          -1/2 sum_(i in B) r_i(1-p_i)
   <= (17/16)F-(15/32)j.                                (4)

To see the sharper coefficient, retain the positive inside-site term
1/2 sum_B r_i p_i and bound the combined positive sum by sum_all r_i p_i;
there is no need to charge F a second time. The older49/32 coefficient
was valid but unnecessarily loose for this more demanding target.
Faults add at most n lambda(2^q-1). Choose

    lambda<=1/[2^20(2^q-1)],
    l=ceil(n/8192), h_copy=floor(n/4096)+1.

The exact rational inequality

    (17/16)F0+2^(-20) < (15/32)/8192                   (5)

shows the stopped exponential process has nonpositive drift at j>=l.
If h_copy>l+q, the old excursion argument now bounds a comparison
destination started CORRECT by

 P(destination reaches h_copy by L before source exit)
    <= n(17/16+lambda)L 2^(l+q-h_copy).                 (6)

For an actual arbitrary initial destination, overwrite coupling makes
it equal to that comparison after each site's first copy update. For
0<tau<=L the probability of any wrong count>floor(n/4096) during
[tau,L] is consequently at most

 delta_source(L) + n exp(-15tau/16)
       +n(17/16+lambda)L 2^(l+q-h_copy).                (7)

Here delta_source is the original adapted fixed-initial-pattern source
bound at exit h. The ENTIRE copied error pattern, rather than only its
decoded bit, meets the cleanliness threshold. Section1's separate
all-pattern restart theorem can then tolerate future dependence of that
destination pattern when used as an initial register state. It does NOT
make repeated copying from an anticipatively initialized source valid:
the destination-generator argument would lose fresh-coin adaptation.
A naive union over all source patterns costs more than the displayed
copy exponent. This failed composition was caught by C's whole review
and is preserved in HISTORICAL_COPY_SCOPE_ERROR.md. A changing source,
faulty phase switch or recursive handshaken operation remains unbuilt.

## 3. Future-selected activation TIMES need their own bound

The simultaneous starting-pattern event in (2) is at a specified start
time. One cannot apply a strong Markov argument at an anticipative
acceptance time selected by future-dependent fault labels.

A usable sufficient repair is available when the candidate activation
times belong to the superposition of a FIXED finite catalogue of
independent primitive Poisson streams of total rate R. Include every
actual state-changing event, with fixed nominal coin laws. At a Palm
event at time s, all strictly future primitive increments have the
original independent laws. The uniform event (2) maximizes over EVERY
allowed starting pattern, and hence its future probability is<=delta_*(L).
Campbell's formula and a union bound over all candidate events in[0,L]
therefore give

 P(some candidate time s has a bad sparse restart before L)
      <= R L delta_*(L).                                (8)

Also include delta_*(L) for starting at time0, and multiply by2 if the
target bit may be chosen from both values using future information.
No normalized conditioning on an actually accepted event is used.
This bound may be expensive (a polynomial prefactor R n L^2), but still
permits exponential horizons below its displayed distance exponent.

Premises matter: after a selected activation, the candidate register's
updates must really follow the specified restoring operation on that
interval. A spatially inconsistent noisy mode switch, adaptive deletion
of its update clocks, or source feedback can break this premise. Those
are exactly parts of the still-unbuilt handshake/controller operation.
Equation(8) does not construct such a switch or protect an unencoded
acceptance bit. An unbounded or future-selected EVENT-TIME point process
is not the fixed Poisson catalogue assumed here.

## What has advanced

Equations(2),(8) remove two specific illegitimate freshness inferences
for the stated restoring register: future-dependent sparse initial
patterns and anticipatively chosen candidate event times. Equation(7)
separately strengthens fixed-initialization source copying, and may NOT
be iterated by pretending that its future-selected output source is
fresh. The tradeoffs
are more stringent cleanliness/noise, longer finite walks, explicit
failure factors and genuine mode-operation premises. Standard coupling,
entropy union bounds and Palm calculus are ordinary methods; historical
novelty or a completed communication/computation theorem is not claimed.
