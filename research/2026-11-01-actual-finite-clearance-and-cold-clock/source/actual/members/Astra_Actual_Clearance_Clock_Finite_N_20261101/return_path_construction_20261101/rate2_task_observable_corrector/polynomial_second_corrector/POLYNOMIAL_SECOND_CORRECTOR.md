# A finite polynomial second corrector, with its actual-chain debts exposed

**Author continuation, unreviewed.** This note banks a constructive degree-two
polynomial inverse and works out the linear correction for the residual -RA.
It does not claim a moderate-cone admission theorem. Existing compact and
weighted-source components remain unchanged.

## 1. The reference is an algebraic operator, not an occupation law

At fixed algebraic parameters (L,E,Z,n), define

    Q0 u(A)=3L²[u(A+1)-u(A)]+NA[u(A-1)-u(A)],
    μ=3L²/N.

No actual trajectory is frozen, and no Poisson fiber law is assumed or used.
For any polynomial r(A)=r0+r1 A+r2 A², whose coefficients may depend on the
parameters, set the zero-at-A=0 polynomial

    χ(A)=α A²+β A,
    α=r2/(2N),       β=[r1+r2(μ+1/2)]/N.

Direct finite differences give the exact inverse identity

    Q0 χ= -r(A)+rbar,
    rbar=r0+r1 μ+r2(μ²+μ).                               (1)

The numbers μ and μ²+μ arise by algebra from Q0A and Q0A²; they are not assumed
conditional moments of the count chain. The zero-at-A=0 convention fixes a
parameter-dependent additive ambiguity whose motion would otherwise need its
own charge.

## 2. Actual-minus-reference and parameter motion are explicit

The actual upward/downward A intensities are

    β_+=1+A(C+D)+AE+3CD,
    β_-=A+3A(A-1)+AE+AB.

Let n=A+B+C+D+E and Z=C-D. With C+D=2(L-A) and
CD=(L-A)²-Z²/4, their differences from the reference are exactly

    δ_+=β_+-3L²=1+AE-4AL+A²-3Z²/4,
    δ_-=β_--NA=A[(n-N)-2L+4A-2].                         (2)

For each actual channel r write a_r=ΔA in {±1} and p_r for its complete
parameter jump (ΔL,ΔE,ΔZ,Δn). For any parameter-dependent χ, the identity

    Gχ=Q0χ+E_fast+E_param,
    E_fast=δ_+[χ(A+1;p)-χ(A;p)]
           +δ_-[χ(A-1;p)-χ(A;p)],
    E_param=Σ_r λ_r[χ(A+a_r;p+p_r)-χ(A+a_r;p)]             (3)

is exact. It separates two distinct debts: imperfect reference rates and
actual parameter motion during every reaction.

For χ=α(p)A²+β(p)A,

    E_fast=δ_+[α(2A+1)+β]+δ_-[α(-2A+1)-β],
    E_param=Σ_r λ_r[(A+a_r)² Δ_rα+(A+a_r)Δ_rβ].            (4)

Both AB↔CD channels have p_r=0, so they contribute **nothing** to E_param.
They still contribute their actual jumps to the martingale bracket. The full
parameter table is:

| channel | ΔA | ΔL | ΔE | ΔZ | Δn |
|---|---:|---:|---:|---:|---:|
| 0→A | 1 | 1 | 0 | 0 | 1 |
| A→0 | -1 | -1 | 0 | 0 | -1 |
| 2A→AC | -1 | -1/2 | 0 | 1 | 0 |
| AC→2A | 1 | 1/2 | 0 | -1 | 0 |
| 2A→AD | -1 | -1/2 | 0 | -1 | 0 |
| AD→2A | 1 | 1/2 | 0 | 1 | 0 |
| 2A→AE | -1 | -1 | 1 | 0 | 0 |
| AE→2A | 1 | 1 | -1 | 0 | 0 |
| AE→CD | -1 | 0 | -1 | 0 | 0 |
| CD→AE | 1 | 0 | 1 | 0 | 0 |
| CD→AB | 1 | 0 | 0 | 0 | 0 |
| AB→CD | -1 | 0 | 0 | 0 | 0 |

The coefficient differences in (4) can either be computed exactly or charged
by their own derivative bounds along these actual parameter segments. For
example |Δα| is bounded by the sum of the four coordinate increments times
segment suprema of |α_L|, |α_E|, |α_Z|, |α_n|. This is a finite computation, not
an unspecified fast-equilibrium error.

The exact χ jump is

    Δ_rχ=α(2Aa_r+1)+βa_r+(A+a_r)²Δ_rα+(A+a_r)Δ_rβ.       (5)

Thus its bracket is Σλ_r(Δ_rχ)², with the literal row bound

    |Δ_rχ|<=(2A+1)|α|+|β|+(A+1)²|Δ_rα|+(A+1)|Δ_rβ|.

A full degree-two correction is not paid until these coefficient-motion terms,
its endpoint size, and this actual bracket have been bounded on the admitted
region.

## 3. A particularly simple correction for the actual ratio task

Define

    R=E²/(NL),
    F1=R(1-AE/(NL)),
    D0=(EL/N)(4-3R)-R/L.

F1 is the first corrected observable for f(l,e)=e²/l. Suppose its existing
residual is explicitly split as

    G F1=D0-RA+E1.                                       (6)

This equation defines E1 exactly; it does not assert that E1 is already small.
Apply (1) to r(A)=-RA. The second corrector is just

    χ=-RA/N=-AE²/(N²L),      F2=F1+χ.

It satisfies

    Q0χ=RA-3RL²/N.

Consequently (3) proves the actual-chain identity

    G F2=D1+E1+E_fast+E_param,
    D1=(EL/N)(4-3R-3E/N)-R/L,                            (7)

where

    E_fast=(R/N)[-1+A(n-N)+2AL+3A²-2A-AE+3Z²/4],
    E_param=-(1/N)Σ_r λ_r(A+a_r) Δ_rR.                   (8)

The mean term -3RL²/N has **not** disappeared. Relative to the nominal factor
EL/N it is exactly -3E/N. At E/N=0.15 and R=1, for example, the leading bracket
4-3R-3E/N is 0.55 rather than 1. This is only a drift arithmetic observation,
not a proof that this boundary is reached or retained.

A useful deterministic endpoint bound is

    |χ|=(A/L)(E/N)²<=(E/N)².                             (9)

Thus under E<=νN, the extra correction costs at most ν²; including a possible
exit jump, its two-endpoint comparison costs at most 2(ν+1/N)².

## 4. Exact finite-jump parameter bound

For u=ΔL, v=ΔE, with L>1,

    ΔR=R[(2v/E+v²/E²-u/L)/(1+u/L)].                      (10)

For positive E and actual |u|<=1, |v|<=1,

    |ΔR|<=D_L|u|+D_E|v|,
    D_L=R/(L-1),
    D_E=RL/(L-1)(2/E+1/E²).                              (11)

This is exact finite-jump domination. AB↔CD have u=v=0, so ΔR=0 there.
Let s_L,q_EE be the exact rate sums from the compact component. Since each
active A+a_r is nonnegative and at most A+1, (8) gives

    |E_param|<=(A+1)[D_L s_L+D_E q_EE]/N.                 (12)

No fast AB rate appears in this parameter-motion bound.

## 5. A paid integrated error bound in the unweighted source budgets

Stop on a region with

    L>=ell0>1, E>=m>=1, L<=λN, E<=νN, L/E<=η,
    R<=rmax, |n-N|<=d,

and physical horizon h. Use pre-stop occupation budgets

    H0=∫A dt,       P0=∫AB dt,       S0=∫CD dt,
    Z2=∫Z² dt.

These may be actual path values or deterministic stopped ceilings. Put

    c0=ell0/(ell0-1),       c_m=2+1/m.

Equation (8) and A<=L imply

    ∫|E_fast|dt <=rmax[h/N+(d/N+5λ+ν+2/N)H0+3Z2/(4N)].   (13)

For (12), use s_L<=1+A+3AL+AE and q_EE<=A²+2AE+2CD. Straight polynomial
bounds yield

    ∫|E_param|dt <=c0 rmax {
       h/(N ell0)
       +[3λ+ν(1+1/ell0)+(4+2/ell0)/N
         +c_m(3λη+2λ+(η+2)/N)]H0
       +2c_m S0/(Nm)}.                                  (14)

For clarity, the two bounds behind (14) are

    ∫(A+1)s_L/L dt
      <=h/ell0+[3λN+νN(1+1/ell0)+4+2/ell0]H0,

    ∫(A+1)q_EE/E dt
      <=[3ληN+2λN+η+2]H0+2S0/m.

They use A<=L, A/E<=η, and CD<=L². There is no replacement of dt by an e
increment. In a cone λ=Hν², η=Hν, the root's separately paid unweighted
H0=O(ν), S0=O(νN) would make the new fast-A/parameter debts O(ν²), plus mass,
finite-size, and imbalance terms. The original -RA occupation cost was O(ν).
This is a genuine improvement **if those input budgets have been received**.
In particular the unweighted storage charge must be the actual entrance
W0+h; a uniform O(ν) occupation / exp[-cνN] claim requires that charge to be
Theta(νN). It is not automatic for a restart close to the upper E ceiling.
It does not erase E1 or the remaining Z2/N debt.

## 6. The new martingale cost is small and explicit

From Δχ=-(a_r R+(A+a_r)ΔR)/N and (11), every stopped χ jump satisfies

    |Δχ|<=jχ,
    jχ=(rmax/N)[1+c0(1+1/ell0)+c0 c_m(η+1/m)].            (15)

The exact total reaction rate obeys

    q_A<=1+AB+3CD+A(3L+2E).

Therefore the χ martingale bracket is at most

    vχ=jχ²[h+P0+3S0+(3λ+2ν)N H0].                       (16)

This pays the fast AB/CD channels by their actual event compensator, not by
assuming independent fluctuations. If P0,S0=O(νN) and H0=O(ν), this bracket is
O(ν/N). Freedman applies to the new martingale with (jχ,vχ). For the **combined**
observable F2, either sum the exact channel jumps before squaring, or safely use
q_F2<=2q_F1+2q_χ and jump cap j_F1+jχ. No independence is asserted.

## 7. Degree-two extraction is finite, but not yet a closed cone proof

At fixed (L,E,Z,n), all actual rates are polynomial of degree at most two in A.
Since F1 is affine in A at fixed L,E, its exact generator residual
G F1-D0 is a polynomial of degree at most three in A, with rational parameter
coefficients (denominators arise from L±1 and L±1/2). Direct symbolic computation
confirms that the cubic coefficient is generally nonzero.

Thus one can acquire r0,r1,r2,r3 by a finite coefficient extraction from the
12-channel sum. Applying (1) to the degree-at-most-two part leaves:

* the honest algebraic mean r0+r1μ+r2(μ²+μ);
* the explicit cubic r3A³;
* the actual-minus-reference and coefficient-motion terms (4);
* the endpoint and actual martingale costs (5).

It would be incorrect to claim that a degree-two inverse alone annihilates the
entire exact finite-jump residual. This note supplies the inverse and a fully
charged simple instance, not bounds for a particular bulky quadratic coefficient
choice. The outstanding admission/consumer obligations are E1, imbalance, all
physical exits, and whichever further quadratic/cubic terms are actually used.

## 8. Verification

`check_polynomial_second_corrector.py` checks the inverse, all twelve parameter
jumps and actual rate differences, the linear specialization, its integrated
pointwise inequalities, and its finite-jump/bracket costs. It also verifies that
the exact F1 residual has degree three in A. Results are in
`polynomial_second_checks.json`. These are author exact checks, not independent
receipt or a clearance certificate.
