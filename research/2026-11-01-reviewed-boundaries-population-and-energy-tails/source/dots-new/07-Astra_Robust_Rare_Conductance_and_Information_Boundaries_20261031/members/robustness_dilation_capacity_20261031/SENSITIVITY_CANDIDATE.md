# Necessary geometric accuracy and localized robustness

Status: derived result, independently unreviewed. No earlier freeze is changed.
These are consequences of the proved variational sandwich plus ordinary one-
dimensional Laplace estimates, not a claim about arbitrary-start passage times.

Fix kappa=beta=1, s=1+(1-y^2)^2 and any fixed p2 or p4 anchor class. A common
geometric profile r defines F=U(r(y)z); the sandwich is uniform over every fixed
finite SPD transverse M and every admitted angular energy U in dimension m.

## 1. A small profile error really can amplify exponentially with dimension

Let 0<epsilon<1/4 and r_epsilon=s(1+epsilon*y^2/(1+y^2)^2).
The relative spatial error is at most epsilon/4, yet it is macro-dependent:
there is no uniform angular rescaling that removes it. The monotonicity proof in
PROOF_CANDIDATE applies, so r has its global positive minimum at y=+/-1 and
its unique slab maximum at0. Put a=1+epsilon/4. Taylor expansions give

    r(y)=2[1-(1-epsilon)y^2+O(y^4)] near0,
    r(1+x)=a+(4+3epsilon/4)x^2+O(x^3).

Therefore, as m tends to infinity with epsilon fixed,

    R0(r) ~ 2^m sqrt(pi/[m(1-epsilon)]),
    MA(r) ~ a^(-m) sqrt(pi*a/[m(4+3epsilon/4)]),
    k_free(r) ~ (m/pi) (a/2)^m
                   sqrt[(1-epsilon)(4+3epsilon/4)/a].

The extra Jensen resistance has the SAME leading asymptotic as R0: its integrand
near0 is 2^m[1+p(1-epsilon)y^2+O(y^4)]^(-m/p).
It follows that Rplus/R0 tends to1 and the full k_M/k_free tends to1 UNIFORMLY
in admitted M and U, because every k_M is squeezed between those scalar bounds.
No transverse spectral gap or interchange of unknown mixing limits is invoked.

For the nominal profile epsilon0, k_free~(2m/pi)2^(-m). Thus, for ANY chosen
admitted matrices at each dimension (including identities),

    k_M(r_epsilon)/k_M(s)
      ~ (1+epsilon/4)^m
          sqrt[(1-epsilon)(4+3epsilon/4)/(4(1+epsilon/4))].

In particular the logarithm divided by m tends to log(1+epsilon/4)>0.
For small fixed epsilon this is Theta(m epsilon). Hence a theorem promising a
fixed relative accuracy from dimension-independent arbitrary geometric-error
budgets would be false. This is a real potential family with smooth conservative
full diffusions and finite Gibbs mass, not a loose bound mistaken for necessity.

The Laplace steps require no unproved concentration hypothesis: the displayed
smooth functions have unique nondegenerate extrema on the relevant pieces.
Restrict to a fixed neighborhood, substitute x=v/sqrt(m), and dominate by a
Gaussian using quadratic Taylor bounds. The remaining compact part has a strict
extremum gap. The explicit y^-4m tail estimate makes the unbounded remainder
exponentially negligible relative to a^-m/sqrt(m). The same compact-slab argument
handles both resistance integrals. These are ordinary one-dimensional limits;
no finite numerical error guarantee is inferred solely from them.

## 2. A global worst-case budget is not a universal physical floor

Instead let e_flat=y^2(y^2-1)^2/(1+y^2)^4, with supremum1/16. For
l=s(1-delta e_flat), u=s(1+delta e_flat), both profiles retain value2 at the
barrier and value1 at the basin minima. The local expansions are

    l=2[1-(1+delta)y^2+O(y^4)],
    u=2[1-(1-delta)y^2+O(y^4)],
    l(1+x)=1+(4-delta/4)x^2+O(x^3),
    u(1+x)=1+(4+delta/4)x^2+O(x^3).

For every actual non-geometric F between these radial envelopes, the asymptotic
width of the OUTER interval in(R) is

    sqrt[(4+delta/4)/(4-delta/4)]
       *sqrt[(1+delta)/(1-delta)].                    (W)

This is finite and near1 for fixed small delta, INDEPENDENT of m. It does not say
all actual rates are equal or identify their separate angular partitions.
In contrast, replacing these envelopes by the global constants
l_global=(1-delta/16)s, u_global=(1+delta/16)s produces an outer-width penalty
[(1+delta/16)/(1-delta/16)]^(2m), which grows exponentially. That global comparison
is valid but throws away the location of the error. At delta1/500, expression(W)
is about1.002127; a finite requested-width computation must still pay intrinsic
Jensen slack and all numerical enclosure error.

Thus the relevant robustness question is not only the maximum geometric defect,
but where it occurs relative to resistance and basin concentration. The same
ordinary comparison machinery, supplied these acquired scalar envelopes, already
exploits that information. It must receive equal access in any comparison.
