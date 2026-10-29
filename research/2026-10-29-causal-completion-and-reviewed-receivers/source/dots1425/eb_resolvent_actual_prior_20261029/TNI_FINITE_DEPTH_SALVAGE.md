# Safe finite-depth salvage for state-dependent EB events
2026-10-29. Root-derived replacement for the rejected left-renewal claim; independent review pending.

Let Ψ be CPTP and Ψ=E+R, where E is CP entanglement-breaking (not necessarily TP), R is CP, and E†I≥αI, α>0. Then R†I≤(1−α)I, so ||R^m||diamond≤(1−α)^m.

The noncommutative expansion Ψ^m−R^m is a sum of CP words containing E, hence is CP and entanglement-breaking. Its trace deficit is the positive effect (R^m)†I. Fix a density operator τ and complete it by the EB replacement event
B_m(X)=(Ψ^m−R^m)(X)+Tr[R^m(X)]τ.
This is CPTP and EB, with halfdiamond distance from Ψ^m at most(1−α)^m: the difference is R^m minus its replacement completion, each term having diamond norm at most(1−α)^m.

For any state with arbitrary reference, telescoping and CPTP trace contraction give
T(ρ,Ψ^mρ)≤Σ_(k=0)^(m−1)T(Ψ^kρ,Ψ^(k+1)ρ)≤m T(ρ,Ψρ).
Therefore
T(ρ,B_mρ)≤m T(ρ,Ψρ)+(1−α)^m.
If Ψ is the actual universal recovered channel, averaging yields
**e_avg(B_m)≤m√δ+(1−α)^m.**
Choosing m of order log(1/δ)/α yields a square-root-loss times logarithmic factor, not the constant√δ bound of the state-independent branch theorem. The reference version retains the product-barycenter assumption needed for recovery factorization, and the comparator is EB on the noisy system only.

This construction neither normalizes the invalid left-resolvent nor assumes its trace preservation. It is a separate valid finite-depth channel construction. Existence/acquisition of a suitable event E with a uniform full-rank effect remains an additional obligation for any proposed channel family. No cheap physical implementation or novelty claim is asserted.
