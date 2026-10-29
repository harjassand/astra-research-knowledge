# Finite spectral acceptance test: explicit constants
2026-10-29. New author derivation; receiving review required. This does not by itself finish noisy recovery composition.

Let tau be a density operator. Choose 0<gamma<=1 and zeta in(0,1). Let M be the least power of two at least128/gamma, and s an odd integer at least log2(1/zeta). On an eigenvector of eigenvalue lambda, standard M-point quantum phase estimation of exp(i*pi*tau) estimates phase phi=lambda/2 in[0,1/2]. Map outcome y/M to the unique representative in[-1/4,3/4). Accept an individual test if its representative is at least gamma/4. Repeat s times on the same target with fresh phase ancillas, then accept the majority. All records may be discarded afterward.

## Tail proof
For circular distance Delta=dist(phi,y/M), the QPE probability obeys p_y<=1/(4 M^2 Delta^2), using |sin(pi Delta)|>=2Delta for Delta<=1/2. In each of the two directions from phi, the scaled distances M Delta are separated by one. For a>0 and Ma>=2, the total mass with Delta>=a is at most
 (1/2) sum_(j=floor(Ma))^infinity 1/j^2 <=1/[2(floor(Ma)-1)].
The harmless enlargement includes any displaced lattice offset. With a=gamma/8 and M gamma>=128, this is at most1/30 (and certainly1/28).

If lambda<=gamma/4 then phi<=gamma/8, so |circular error|<gamma/8 gives a representative below gamma/4. If lambda>=gamma then phi>=gamma/2, so the same event gives a representative above gamma/4. The unwrap interval contains the whole phase range[0,1/2] with a margin1/4, so no wrap ambiguity occurs on this event.

Conditioned on a target eigenvalue, repeated QPE flags are independent: every QPE Kraus operator is a scalar function of tau. The probability of at least s/2 wrong flags is at most 2^s (1/28)^(s/2) <=2^-s<=zeta. Thus the final acceptance profile f obeys f(lambda)<=zeta for lambda<=gamma/4 and f(lambda)>=1-zeta for lambda>=gamma. No assumption is made inside the transition band. Degenerate eigenspaces are left coherent because every Kraus operator is scalar there.

## Paid controlled evolution
The sum of evolution times in all controlled phase-estimation powers is T=pi*s*(M-1). Applying CONTROLLED_DME_v1.md to the full circuit gives diamond implementation error at most delta from O(T^2/delta+T+s log M) fresh tau samples, hence polynomial in 1/gamma,log(1/zeta),1/delta. Every tau sample is one forward N(I/k) call. The target is not a sample consumed by DME. QFT and known phase gates have separate finite synthesis budgets, summed in diamond norm. No source inverse, controlled-source, purification or environment interface is assumed.

This test is a quantum instrument statement. Converting its simulation error to normalized accepted training records requires an explicit success lower bound and stopping/cap analysis, still separate. In particular it is not legitimate to normalize without charging acceptance probability.
