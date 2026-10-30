# Resolvent extension and the actual good-input occupation gap

30 October 2026. New working addendum, not independently reviewed. Previously accepted sources remain unchanged.

## 1. The resolvent drift works for every fixed s>0

The accepted occupation proof used s>=2 only in the simultaneous `(z,d)->(z+1,d-1)` finite-difference check. Replace that check as follows. Fix s>0 and choose L>4/s.

- If d>=Lz, the denominator ratio for d->d-1 is at most d/(d-1)<=1+2/d<=1+s/(2z), whereas the inverse-power factor is `1-s/z+O_s(z^-2)`. Their product is at most `1-c_s/z` for large z.
- If d<Lz, then n<=C_eta z+d<=C_(eta,s)z. Since the denominator is at least z^3, changing d changes its relative value by O_s(z^-2), while z->z+1 supplies the negative order s/z term.
- Bounded z,d,n are finite-shell exceptions. If z is bounded while n grows, d>=Lz eventually, so this is not an omitted infinite face.

The same split applies to the x profile on c<=Mx. On c>Mx choose M much larger than L. For d>=Lx the simultaneous changes are favorable. For d<Lx, n<=c+(L+1)x<=C c and their possible positive denominator terms divided by the negative C-return magnitude cd phi_s/x are at most C_s(a+d)n/(c x^2)<=C_s L/x. This is small for large x; for bounded x and large n, d is bounded and the negative term grows with c. Thus the C-return absorbs the denominator increases also for 0<s<2. Conversion signs and creation bounds are unchanged. Thus the paired resolvent proof gives, for EVERY fixed s>0,

`(Q-k0(a)_2)F_s <= -c_s x^(-s-1)`,
`F_s <= C_s x^-s/(x^3+nd)`,

with zero value at the d=0 killing boundary, on sufficiently large shells. Finite-shell values handle the remainder as before.

## 2. Sharper positive-D physical time

Set s=a0-1>0. The negative operational drift pays the physical-time integrand `1/(A)_a0<=C x^-a0`. Before the first connector event B=b is fixed. Therefore the SAME stopped positive-D episode (connector/clearing/dormant exit) obeys

`(b)_q T_+ <= C x^(1-a0)/(x^3+nd)`.

The independently reviewed lower occupation bound is

`(b)_q U_+ >= c x^(2-a0)/(x^3+nd)`.

Hence

`T_+/U_+ <= C/x`.                                      (G+)

This compares the actual time and occupation of the same stopped episode, without a high-A path restriction or a stationarity premise.

## 3. Restore actual dormant feedback before the first connector event

The reviewed full first-connector time bound from ANY active dormant input y is

`T_full(y) <= C f_m(A_y)/(b)_q`.

Use it only at the actual d=0 entry law from the initial positive-D episode. The reviewed occupation-normalized return theorem gives

`E[f_m(A_exit); d=0 exit] <= C (b)_q x^-2 U_+`.

Strong Markov therefore yields

`T_full <= T_+ + C x^-2 U_+ <= C x^-1 U_+ <= C x^-1 U_full`.

No product of independent marginal estimates is taken, and the dormant continuation is the full actual local fast/clearing episode, including repeated seeds/returns. This is a first-CONNECTOR theorem; it must not be confused with the full section cycle where B can change.

## 4. Initial dormant state

At active d=0, A>=m. The initial first-event waiting time W has A constant, so its occupation is exactly A E W. Clearing or a connector event terminates. A seed has output A-1 or A-2 and positive d. Its x differs from input x by a fixed bounded factor and its actual continuation satisfies the preceding inequality. Summing these disjoint outcomes gives

`T_full/U_full <= C/(1+A_initial)`

uniformly over every active initial composition, including dormant inputs, with b>=q. All constants depend only on fixed model parameters. Small A does not give a small ratio; the bound correctly remains O(1) there.

## Scope

This supplies the graph-earned good-input gap required for section correction, without stopping upon low-A excursions. It does not make the non-small low-A dormant section transient in the needed weighted norm, and it does not finish off-section seed-phase continuation, negative activation credit, or global recurrence. Its new s>0 drift extension and resulting full local occupation gap remain working results pending independent review.
