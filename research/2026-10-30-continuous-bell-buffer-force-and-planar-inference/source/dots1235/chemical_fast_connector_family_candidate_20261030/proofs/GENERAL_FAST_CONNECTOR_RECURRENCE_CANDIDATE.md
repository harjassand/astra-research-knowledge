# Conditional global closure for a structural fast-connector family
Status: NEW UNREVIEWED synthesis. In particular UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md and its reset/repair obligations are not yet certified. This file states what follows IF those exact arguments pass; it must not be reported as a proved global theorem yet.

## Family
Any fixed number k>=2 of composition species, including A. Any finite strongly connected graph of homogeneous degree-m composition complexes containing every pure mX_i. Every fast complex carries the common catalyst qB. Integers q>m>=2. Add connector0->A+B->mA+qB->0. All rate constants are arbitrary fixed positive numbers.

Candidate conclusion: the full chain is nonexplosive, every closed communicating class is positive recurrent, and every invariant class law has all exponential moments of N+B. This is a structural subclass, not arbitrary weakly reversible reaction networks.

## Two earned-value obligations, not a supplied barrier
Let h=q-m and a=(m-1)/(q-1)<1. The proposed N-directed value uses

    r=N-H(B)=N-aB+O(1),

with H defined exactly in UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md. The independently derived complementary value uses

    Z=B-N-h I(x),

where I indicates an enabled fast composition reaction.

The N-directed candidate asserts a finite actual stopped cost W_r with LW_r=-phi(r) above its threshold, polynomial-in-r times phi upper bound uniform in ALL hidden states, and exterior positive leakage bounded by a constant (only immigration enters).

UNCAPPED_ACTIVITY_CREDIT_TRACE.md derives W_Z with LW_Z=-phi(Z) above threshold, uniform polynomial-in-Z profile, and exterior leakage at most C AB in the fixed-width Z threshold strip (only active activation enters). Both satisfy a first-holding lower bound phi(residual)/[C(1+N+B)^(m+q)]. Choose one sufficiently small rational factorial exponent alpha satisfying both trace conditions; phi(u)=Gamma(u+1)^alpha for positive large u.

## Global drift, with no entropy selector or capped boundary
The two residuals cannot both stay bounded at infinity. Since a<1 and I is bounded,

    max(r,Z)>=c(N+B)-C

for a graph-dependent c>0. Thus W_r+W_Z is normlike by the first-holding lower bounds: a factorial on a linear fraction of N+B beats the polynomial total-rate denominator.

If both residuals exceed threshold, both generator contributions are negative. If Z is in its leakage strip while N+B grows, r grows linearly with N+B, so phi(r) absorbs the polynomial C AB. If r is in its leakage strip and N+B grows, Z grows linearly and phi(Z) absorbs the constant leakage. If both residuals lie below threshold, N+B is bounded. Consequently

    L(W_r+W_Z)<=-1

outside a finite set, and indeed the negative margin dominates exp(theta(N+B)) for every fixed theta>0.

The linear total-population localization in the N-directed file already gives nonexplosion independently. State-level weak reversibility makes communicating classes closed. Standard stopped occupation/regeneration applied to the displayed drift then gives the candidate recurrence and moment conclusions without assuming integrability of W_r+W_Z under an invariant law.

## Why this would remove the higher-dimensional entropy mismatch
Neither component is a radial function assumed valid after freezing composition. Both are actual stopped costs with uniform bounds earned through fast accessibility, physical clearing resets, and connector race estimates. They need not be invariant under fast composition jumps; their Poisson equalities account for those jumps. No sum of radial N! and product-coordinate factorial barriers is being selected by an assumed entropy gap, and no moving cap is needed.

## Exact open point
The full N-directed value must survive hostile review of correlated reset kernels, section-return drift, and actual bad-event/initial-state repair. The complementary trace and strict-power clearing result do not alone prove this global synthesis. A failure there leaves the global conclusion open; it cannot be patched by assuming the claimed finite value.
