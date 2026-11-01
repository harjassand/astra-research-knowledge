# Pending independent mechanism review: seeded time-change support bridge

This is a reconstruction of the candidate mechanism, not acceptance of a frozen
constructor, receiver, or package. No prior accepted files are modified. The
arguments below currently reveal no mathematical blocker. Every assertion is for
the displayed conservative common-seed class, not arbitrary weak reversibility.

## 1. Exact random clock and killed finite-fiber problem

Let all internal source and target complexes contain A and conserve total count N.
Remove one A from each; write the resulting mass-action generator as Q on
`y=(r,B)`, where `r=A-1`, and its maximum source order as `p>=2`. For `A>=1`,
the falling-factorial identity gives exactly `L_internal=A Q`. Internals cannot
extinguish the last A. Set `d tau=A dt` until the first immigration/death event.
In tau time the internal process is Q, the death rate is the constant mu, and
immigration has hazard `lambda/(1+r)`. The Q process can be constructed on the
entire finite fiber `sum y=M=N-1`, independently of `D~Exp(mu)` and a birth clock
with this state-dependent hazard. Stopping at the earlier core event recovers the
actual chain; no stationarity, mixing time, or eternal seed is assumed.

For finite-fiber verification, let `b(y)=lambda/(1+r)` and
`K=diag(mu+b)-Q`. Then

```
K p_up   = b,
K p_loss = mu*1_{r=0},
K p_down = mu*1_{r>0},
K h_seed = 1/(1+r).
```

These are exact rational linear systems at rational rates. Their solutions obey
`p_up+p_loss+p_down=1`. The physical duration of a bundled cycle has expectation
`h_seed+p_loss/lambda`. The factor `1/(1+r)` in the duration equation is essential:
the tau-time lifetime itself is not the physical holding time.

## 2. Top-order support activation with remaining-interval bounds

Let v be the homogeneous order-p drift on the simplex. Put
`C=max(1,p^3 sum_all_Q_rates)`, `T=1/(4C)`, and let kmin be the minimum top-order
rate. Then on the simplex

```
v_i >= -C y_i,       ||Dv||_infinity <= C.
```

For the first inequality, a negative contribution must have source coordinate i
present, so its monomial is at most y_i. For the second, sum the absolute row
derivatives; the stronger elementary bound is `p^2 sum_top_rates`.

Suppose top-order support closure from every singleton reaches coordinate r.
Choose an initial coordinate at least 1/n. Its trajectory coordinate remains at
least `ell_0=3/(4n)` throughout `[0,T]`, since
`exp(-CT)>=1-CT=3/4`. Divide the interval into n blocks. If every coordinate in a
discovered support is at least ell on the entire remaining interval, a top reaction
whose source lies in that support and whose target introduces j gives
`v_j>=kmin ell^p-C y_j`. Integrating over the next block, and allowing all subsequent
decay until T, bounds the new coordinate by at least
`3 T kmin ell^p/(4n)` on the entire interval after that block. Thus the conservative
recursion

```
ell_(k+1)=min(ell_k, T kmin ell_k^p/(4n)),   delta=ell_n
```

is valid. There are at most n-1 support additions. Hence `phi_r(T)>=delta` uniformly
over every initial simplex point. Maintaining lower bounds on whole remaining
intervals, rather than only at block endpoints, avoids a hidden decay assumption.
The bound uses a finite raw support trace, not a supplied fluid trajectory.

## 3. Uniform finite-fiber concentration, including boundary starting points

For `M>=p`, let `Z_s=Y_(s/M^(p-1))/M`, and write

```
Z_s=Z_0+integral_0^s b_M(Z_u)du+Mart_s.
```

For a top source u, the scaled propensity differs from `z^u` by at most
`p(p-1)/(2M)`. One elementary proof replaces each factorial factor by
`max(z_i-k/M,0)`; all factors lie in [0,1], and product telescoping bounds the
error by the sum of the removed offsets. This remains valid when a reaction is
disabled, so no interior-lattice assumption is present. Each lower-order channel
has scaled drift at most `p*kappa/M`. Consequently

```
||b_M-v||_infinity <= C/M.
```

The predictable quadratic-variation rate of each normalized coordinate is at most
`p^2 sum_Q_rates/M<=C/M`. Finite fibers justify the square-integrable martingale
identities without localization problems. L2 Doob plus a union bound gives

```
P(sup_[0,T] ||Mart||_infinity > delta/4)
    <=64 n C T/(M delta^2)=K0/M.
```

On the complementary event, for `M>=8CT/delta`, the pathwise Lipschitz/Gronwall bound
is

```
sup ||Z-phi|| <= (delta/4+CT/M)*exp(CT)
               <=(3delta/8)*(4/3)=delta/2.
```

Set `w=T/M^(p-1)`. Then `P(r_w<delta M/2)<=K0/M`. The bound is uniform in every
starting state of that fiber. Conditioning on `Y_(s-w)` gives the same inequality
for every `s>=w`, however long s is; errors are not accumulated over successive
blocks. With `K=K0+2/delta`, therefore

```
E[1/(1+r_s)] <=K/M,      P(r_s=0)<=K/M,     s>=w.
```

This last-window argument replaces a stationary-fiber or uniform-mixing oracle.

## 4. Core-event probabilities and sampled drift

The independent death clock yields, without conditioning on absence of births,

```
p_up <= lambda integral_0^infinity exp(-mu s) E[1/(1+r_s)] ds,
p_loss <= mu integral_0^infinity exp(-mu s) P(r_s=0) ds.
```

The omitted no-birth indicator only enlarges these integrals. Since p>=2 and M>=1,
`w<=T/M`. Thus

```
p_up <=lambda(T+K/mu)/M,
p_loss <=(mu T+K)/M,
p_up+p_loss <=a/M,
a=(lambda+mu)T+K(1+lambda/mu).
```

Observe the first core event from a seeded state; if it removes the last A, include
the subsequent A-zero waiting period and its forced immigration. The new seeded
state has total count respectively N+1, N-1, N with probabilities p_up, p_down,
p_loss. For `V=t^N`, `t>1`, the exact ratio is

```
K_emb V/V=t^-1+(t-t^-1)p_up+(1-t^-1)p_loss
         <=t^-1+(t-t^-1)a/M.
```

The candidate cutoff

```
M_cut=max(1,p,ceil(8CT/delta),ceil(2a(t+1))),
rho=(1+t^-1)/2,      B=(t-rho)t^M_cut
```

gives `K_emb V<=rho V+B*1_{N<=M_cut}`. The tail includes `N=M_cut+1`, because
then `M=N-1=M_cut`. On the finite head, simply use `K_emb V<=tV`. The head is
implicit and need not be enumerated. The cutoff and its power may be enormous.

## 5. Classes, physical occupation, and moments

Poisson immigration bounds total count pathwise on finite physical intervals;
every count sublevel is finite with bounded rates. Hence the full chain is
nonexplosive, independently of the embedded drift argument.

Weak reversibility closes all full state classes. Every such class meets the seeded
region because A-zero states have only the outgoing immigration channel. Any finite
full reaction path between seeded states can be recorded by the embedded chain:
bundle seed-loss/immigration pairs, and if the final segment is internal, append
immigration then death to record the desired endpoint. Every specified finite path
has positive probability. Thus seeded states of a full class form one closed
irreducible embedded class. Standard discrete Foster, or directly tight Cesaro
occupations and Fatou, yields an invariant law pi_emb with
`pi_emb(t^N)<=L_t=B/(1-rho)`.

Let H_x be the physical bundled duration. The seeded part is at most the tau-time
Exp(mu) clock, because A>=1; the possible extinction wait has mean 1/lambda.
Conversely the physical core hazard before the first event is at most
`lambda+mu N`. Therefore

```
1/(lambda+mu N) <= E_x H_x <= H=1/mu+1/lambda.
```

Before the terminal endpoint, N never exceeds the starting count. In particular an
upward immigration occurs at the endpoint and contributes zero occupation time at
the new count. Thus `E_x integral_0^H t^N ds<=H*t^N_start`.

Normalize cycle occupations under pi_emb by `E_pi_emb H`. The numerator has finite
mean jump-rate integral, since rates are polynomial in N, the conditional holding
mean is uniformly bounded, and pi_emb has an exponential moment. The cycle Dynkin
identity gives exact balance of incoming and outgoing jumps; nonexplosion and finite
mean jump intensity imply stationarity of this normalized probability. Equivalently,
the Markov-renewal occupation construction proves the same fact. This establishes
positive recurrence in each full class without assuming a stationary moment.

Finally Jensen and `N<=(t^N-1)/(t-1)` give

```
E_pi_emb H >=1/[lambda+mu(L_t-1)/(t-1)],
pi_cont(t^N)<=H L_t [lambda+mu(L_t-1)/(t-1)].
```

The bound is uniform across classes. It also bounds stationary mixtures. Repeating
for rational t above any requested exponential base proves every finite exponential
moment, by exact count-conservative sampled drift, not generic fluid stability.
The previous one-step `F(A,N)` no-go is compatible with this embedded criterion.

## Remaining receiving boundary

This note accepts no code or receipt that has not yet been frozen and checked.
An implementation must acquire the common seed, stripped maximum order and full
graph condition from raw input, validate all support traces, and distinguish a failed
support test from a stability-negative conclusion. Exact constants, factorized huge
powers, bit cost and caps need honest receiving/accounting. In particular p>=2 is
used in `w<=T/M`; an order-one extension is not silently included. Multiple common
seeds are not covered by this proof as written. Conventional finite-fiber random
time changes, fluid concentration, Foster and occupation tools receive full credit;
no novelty or priority assertion is inferred.
