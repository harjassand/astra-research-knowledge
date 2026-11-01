# Coupling-adapted polynomial reference: exact identities and a one-sided candidate

**Separate author candidate, unreviewed.** This does not replace any frozen paid
component. All identities concern the actual twelve-channel generator. The
reference is used only for finite polynomial algebra, not for a stationary
preparation or an assumed conditional distribution.

## 1. Exact reference matching

Let n be the actual total count (the parent's coarse S), and set

    λ0=1+3L²-3Z²/4,
    k=n+2L-E-2=B+4L-A-2,
    β=E.

The quantity L²-Z²/4 is a coarse parameter; it is **not** the actual CD, which
is (L-A)²-Z²/4. Physical states satisfy λ0>=1. Require k>0. Define the frozen
algebraic operator

    Qc u=(λ0+βA)[u(A+1)-u(A)]
         +(k+β)A[u(A-1)-u(A)].                           (1)

Here L,E,Z,n are held as algebraic parameters only. Direct full-generator
calculation yields

    GA=λ0-kA-3A²,
    G(A²)-Qc(A²)=-6A³+5A²-8LA.                          (2)

In particular the E-dependent variance is matched, not silently dropped.
Equivalently, the actual upward/downward A rate discrepancies are

    δ_+=A²-4AL,
    δ_-=4A²-4AL.                                        (3)

Both are nonpositive on physical states, their difference is -3A², and their
sum is 5A²-8AL. The reference has not been asserted to be an actual coupled
trajectory, despite these useful rate inequalities.

For r(A)=r0+r1A+r2A², put μ=λ0/k and

    α=r2/(2k),
    b=[r1+r2(μ+1/2+β/k)]/k,
    χ=αA²+bA.

Then finite differences give exactly

    Qcχ=-r(A)+rbar,
    rbar=r0+r1μ+r2[μ²+μ(1+β/k)].                         (4)

The displayed first and second moments are algebraic centering constants,
not assumed moments of the actual count chain.

## 2. Every reference error and parameter motion remains present

For coefficients held fixed at the current coarse state, the actual-minus-
reference correction is

    E_fast=α[-6A³+5A²-8LA]-3bA².                         (5)

The full actual generator additionally contains

    E_param=Σ_r λ_r[(A+Δ_rA)²Δ_rα+(A+Δ_rA)Δ_rb],          (6)

with actual parameter jumps from the previous note. This is exact. For example

    Δk=Δn+2ΔL-ΔE,
    Δλ0=6LΔL+3(ΔL)²-(3/2)ZΔZ-(3/4)(ΔZ)².

The possible Δk values are:

| channel | Δk |
|---|---:|
| 0→A, AE→2A | 3 |
| A→0, 2A→AE | -3 |
| AC→2A, AD→2A, AE→CD | 1 |
| 2A→AC, 2A→AD, CD→AE | -1 |
| AB↔CD | 0 |

A rational-coefficient use must stop with k>=k_min>3 and L>=ell0>1, so complete
exit jumps remain away from all denominator poles. AB↔CD contribute zero to
(6), but retain their actual martingale jumps. The earlier coefficient-jump and
bracket formulas apply without assuming any fiber law.

## 3. Linear correction of -RA: positive fast discrepancy

Use R=E²/(NL), F1=R(1-AE/(NL)), and the exact decomposition

    GF1=D0-RA+E1,
    D0=(EL/N)(4-3R)-R/L.

Set q=R/k and χ=-Aq. Equations (2)-(6) give

    G(F1+χ)=D0-Rλ0/k+E1+3RA²/k+E_param,
    E_param=-Σ_r λ_r(A+Δ_rA)Δ_rq.                        (7)

The new frozen-reference error +3RA²/k is nonnegative. There is no explicit
E/N rate-mismatch term in it; its absolute magnitude is controlled by A²/k.
The mean drift -Rλ0/k must still be kept. In particular,

    D0-Rλ0/k
      =(EL/N)[4-3R-Eλ0/(kL²)]-R/L,
    Eλ0/(kL²)<=(E/k)(3+1/L²).                            (8)

It would be incorrect to replace λ0/k by 3L²/N or erase this mean term.

For every actual jump,

    Δq=[ΔR-(R/k)Δk]/(k+Δk).                              (9)

With the exact D_L,D_E from the preceding note,

    |Δq|<=[D_L|ΔL|+D_E|ΔE|+(R/k)|Δk|]/(k-3).            (10)

Thus no uncharged continuous-parameter approximation is involved.

## 4. Sign-preserving lower-drift cost avoids the large AE term

For q=E²/[NL(n+2L-E-2)] with positive denominators:

* AE→2A and AE→CD decrease q (E decreases and k increases);
* immigration and AC/AD→2A also decrease q (L and k increase);
* AB↔CD leave q unchanged.

Their contributions to E_param in (7) are therefore nonnegative and need not
be charged in a **lower-drift** bound. The only negative rows are A death, all
three 2A-source reactions, and CD→AE. Let P_- be the sum of the absolute values
of precisely those negative contributions. Then E_param>=-P_- exactly, and

    P_- <= {D_L a2(2A-1)
           +D_E[a2(A-1)+2CD(A+1)]
           +(R/k)[a2(5A-2)+2CD(A+1)]}/(k-3).             (11)

The three polynomials are the exact negative-row sums of
λ(A+ΔA)|ΔL|, λ(A+ΔA)|ΔE|, and λ(A+ΔA)|Δk| respectively.
In particular the AE rate does not occur in (11). This is not an absolute-value
bound on all parameter motion and must not be used as an upper-drift bound.

Suppose the stopped region additionally has

    E>=m>=1, L>=ell0>1, L<=λN, L/E<=η, R<=rmax,
    k>=k_min>3,

and use actual or received stopped budgets H0=∫A dt, S0=∫CD dt. Let
c0=ell0/(ell0-1), c_m=2+1/m. Then (11) gives the literal integrated charge

    ∫P_- dt <= B_-,
    B_- = rmax/(k_min-3) {
           c0[2λN+3c_m ληN]H0 +2c0 c_m S0/m
           +[7λ²N²H0+2S0]/k_min }.                      (12)

Proof: a2(2A-1)<=2A³, a2(A-1)<=A³, and a2(5A-2)<=5A³.
Use A³/L<=A²<=λNA, A³/E<=ηλNA, CD<=L², and E>=m.
No deterministic time-change or fast-state distribution is used.

Consequently the actual corrected observable has the conditional lower-drift
certificate

    G(F1+χ) >=D0-Rλ0/k+E1-P_-,                          (13)

and the integrated additional negative debt is bounded by (12). If
k_min=κ0N, λ=Hν², η=Hν, and a separately received **actual entrance** source
charge earns H0=O(ν), S0=O(νN), then this extra lower-drift debt is O(ν³), plus
explicit finite-m and finite-N terms. This scaling is not automatic for a restart
near the E ceiling: the unweighted source-storage charge W0+h must actually have
the claimed size. E1, original imbalance errors, and every physical exit remain
unresolved by (13).

## 5. Endpoint and actual martingale costs

The correction size is

    |χ|=(A/L)E²/(Nk)<=E²/(Nk).

If E<=νN and k>=κ0N, it is at most ν²/κ0 before the stop; for two endpoints
including the possible exit jump, a safe bound is

    2(ν+1/N)²/(κ0-3/N),       provided κ0N>3.             (14)

On the domain in section 4, an explicit jump cap is

    jχ=rmax/k_min
       +rmax/(k_min-3){c0(1+1/ell0)+c0c_m(η+1/m)
                       +3(λN+1)/k_min}.                (15)

This follows directly from Δχ=-(ΔA)q-(A+ΔA)Δq and (10).
AB↔CD have exact χ jumps ∓R/k, and therefore bracket contribution
(AB+CD)R²/k². No independence or variance cancellation is assumed.

For horizon h and actual stopped budgets P0=∫AB dt, S0=∫CD dt, H0=∫A dt,

    vχ=jχ²[h+P0+3S0+(3λ+2ν)NH0]                         (16)

bounds the χ martingale bracket. Apply the bounded-jump martingale inequality
with (jχ,vχ), and combine with F1 by its exact jumps or
q_(F1+χ)<=2q_F1+2q_χ. The extra bracket is small when the actual source budgets
are small; this is a conditional cost statement, not a paid cone survival bound.

## 6. Scope and verification

This candidate improves the reference mismatch and, for a lower barrier, removes
the large AE parameter-motion term by its genuine sign. It still requires the
existing E1 to be controlled, plus the actual padded-cone admission/exit proof,
imbalance control, and the requested boundary interpretation. Neither (4) nor
(13) is a substitute for those operations.

`check_coupling_adapted_reference.py` verifies all moment/inverse identities,
actual parameter jumps, the negative-row polynomial sums, the linear generator
decomposition, and rational state inequalities. Its result is recorded in
`coupling_adapted_checks.json`; independent receipt is pending.
