# A weighted full-chain source-time budget on a growing cone

**Author continuation; independently unreviewed.** The earlier compact C²
component is preserved unchanged. This note earns actual weighted occupation and
source-time bounds on an explicitly stopped growing domain. It neither assumes
E[A]≈L²/N nor replaces physical time by de/(2l²). Cone admission, its exit costs,
weighted imbalance control, and a boundary-clearance consumer remain separate.

## 1. Domain, padding, and a literal absorption condition

Use the full twelve-channel rate-2 chain in the parent component. N=T⁵ is a fixed
reference, κ=T^-3, l=L/T, e=E/T³, L=A+(C+D)/2, a2=A(A-1).
Fix p>1, time horizon ST, e0>0, ν>0, H>g>0, c>0, ε>=0. Assume

    κ/e0 <= 1/(4p),     e0-κ >=1,     e0 <= νT².            (1)

A useful padded pre-stop cone is

    e0 <= e <= νT²,
    g(e+κ)²+1/T <= l <= H(e-κ)²-1/T,
    B>=cN>=1,     A<=εN.                                 (2)

Every complete actual jump segment then lies inside

    e>=1,       g e²<=l<=H e²,

because |Δl|<=1/T and |Δe|<=κ. Padding is not a premise about a future state;
it is part of the current admission/stop rule. For the weighted occupation
proof itself, the weaker current-state upper bound l<=He² and e>=e0 would
suffice, but (2) also preserves the separately derived clock derivative bounds.

Stop at the first failure of (2), or time ST. Write this physical stop as τ₀.
All estimates use pre-stop states; terminal positive storage is defined at the
actual exit endpoint, where e>=e0-κ>0. No upper B bound is required.

The main literal statewise absorption condition is

    C+D+4pA+12E <= B/2.                                   (3)

One sufficient parameter choice, valid everywhere in (2), is

    2Hν²+4pε+12ν <= c/2.                                 (4)

Indeed L<=HTe²<=Hν²N and E<=νN. The statewise condition (3) can be used directly
if sharper entrance information is available. A path cannot be assumed to remain
in this domain; every such exit remains part of the stopped result.

## 2. Exact weighted generator and the positive storage

Set

    φ_p(e)=e^-p,        ψ_p(e)=e^(1-p)/(p-1),
    W_p=Aφ_p(e)+3T³ψ_p(e).                                (5)

Both terms are nonnegative. Let

    d_+φ=φ(e+κ)-φ(e),     d_-φ=φ(e-κ)-φ(e),
    α_+=(1/κ)∫_e^(e+κ) φ(u)du,
    α_-=(1/κ)∫_(e-κ)^e φ(u)du.

The full generator acts exactly as follows:

    G(Aφ)=φ GA+[a2(A-1)+2CD(A+1)]d_+φ+2A²E d_-φ,
    G(T³ψ)=-(a2+2CD)α_+ +2AE α_-,                         (6)

where

    GA=1-A-3a2+A(C+D)+3CD-AB.

The first line is a finite-jump product identity, not a first-order expansion.
The 2A→AE and CD→AE contributions to its derivative part are nonpositive. The
AE→2A and AE→CD contributions combine exactly into 2A²E d_-φ. All other
channels have ΔE=0 and remain in φ GA.

Condition (1) and elementary one-step bounds give

    0<=-d_+φ<=pφ/E,
    0<=d_-φ<=2pφ/E,
    (3/4)φ<=α_+<=φ,       φ<=α_-<=2φ.                    (7)

For example, (1+r)^-p>=1-pr>=3/4 for r=κ/e<=1/(4p).
For the backward derivative,
(1-r)^(p+1)>=1-(p+1)r>=1/2, so its reciprocal is at most 2.
These inequalities also prove the stated α_- bound. There is no expansion with
an unspecified O(κ²) term.

Combining (6)-(7), retaining the negative source coupling, yields

    G W_p
      <=φ[1-AB+A(C+D)+4pA²+12AE]-(3/2)CD φ
      <=φ-(AB/2)φ-CD φ.                                  (8)

The omitted -Aφ, -3a2φ, the nonpositive d_+φ term, and -3a2α_+ can only
improve the inequality. The second line is precisely (3).

This is the key point: the bounded tail primitive 3T³ψ pays the CD source
term, while the actual AB capture pays the positive AE-loss weight changes.
A frozen equilibrium and a deterministic time-change are unnecessary.

## 3. Paid weighted occupations and source time

Define the actual additive functional

    Q_p(t)=∫₀^(t∧τ₀) [(AB/2)+CD] e^-p ds,
    H_p(t)=∫₀^(t∧τ₀) A e^-p ds,
    S_p(t)=∫₀^(t∧τ₀) CD e^-p ds,
    φ0=e0^-p,       D_p=W_p(0)+ST φ0.                     (9)

Since B>=cN before τ₀,

    H_p <=2Q_p/(cN),       S_p<=Q_p.                      (10)

Stopped Dynkin and (8), with W_p terminal nonnegative, give the unconditional
expectation bounds

    E Q_p(τ₀)<=D_p,
    E H_p(τ₀)<=2D_p/(cN),    E S_p(τ₀)<=D_p.              (11)

These bounds concern the actual stopped chain. Standard localization suffices:
total count is at most its finite initial value plus rate-one Poisson immigration,
all other reactions conserve or reduce total count, and the lower e stop keeps
the weight finite. Fatou's lemma preserves the nonnegative left-hand terms.

The source-time integral S_p is not inferred from an approximate path. It is
part of the negative generator drift in (8), paid on every actual sample path
up to a martingale deviation.

## 4. Exact jumps and a weighted bracket budget

For the eight channels with ΔE=0, the W_p jump is exactly ±φ. The four other
jumps are:

| channel | exact ΔW_p |
|---|---|
| 2A→AE | -φ+(A-1)d_+φ-3α_+ |
| CD→AE | φ+(A+1)d_+φ-3α_+ |
| AE→2A | φ+(A+1)d_-φ+3α_- |
| AE→CD | -φ+(A-1)d_-φ+3α_- |

Consequently every active row satisfies

    |ΔW_p| <=[7+2p(A+1)/E]φ.                              (12)

On the upper cone,

    A/E<=L/E<=H e/T²<=Hν,    1/E<=κ/e0.

Thus, with

    J_p=7+2p(Hν+κ/e0),       j_p=J_p φ0,                  (13)

all stopped jumps are bounded by j_p. The pointwise φ weight in (12) remains
available; replacing it by φ0 is only for a simple deterministic tail bound.
In particular AB↔CD contribute exactly (AB+CD)φ² to the W_p bracket.

Every channel changes A by ±1. The total rate is therefore the A bracket:

    q_A=1+A+3a2+A(C+D)+3CD+AB+2AE.

Under (3) and B>=1,

    q_A<=1+3AB+3CD.

Indeed 3A+C+D+2E<=B/2, and A[1+B/2]+AB<=3AB. Hence the exact W_p bracket
obeys the useful weighted bound

    q_W=Σ_r λ_r(Δ_r W_p)²
       <=J_p² φ²(1+3AB+3CD).                              (14)

No large upper bound on B was substituted for its capture occupation.

Stop additionally at Q_p=Qbar. Since φ²<=φ0φ and
3ABφ+3CDφ<=6[(AB/2)+CD]φ, the stopped bracket is at most

    v_p=J_p² φ0[ST φ0+6Qbar].                             (15)

If x_p=Qbar-D_p>0, reaching Qbar before the physical stop forces the W_p
martingale to be at least x_p, by (8) and terminal W_p>=0. The unit-clock
construction and bounded-jump exponential martingale therefore give

    P(Q_p reaches Qbar before τ₀)
      <=exp[-x_p²/(2(v_p+j_p x_p/3))].                    (16)

This is a one-sided probability; no unnecessary factor two is needed. The
martingale bracket and jump cap have been paid using the same occupation budget
whose exit is being tested, which is legitimate by stopping at its first hit.
For initial states entering a new stage, apply the identical statement
conditionally on the entrance sigma-field; no reset of the chain is performed.

## 5. Explicit growing-range cost and the useful p=2 specialization

For p>=2, the initial cone gives

    D_p<=HT e0^(2-p)+[3T³/(p-1)]e0^(1-p)+ST e0^-p.         (17)

For 1<p<2, the alternative bound A/E<=Hν gives

    D_p<=[Hν+3/(p-1)]T³ e0^(1-p)+ST e0^-p.                (18)

These bounds contain no power of the upper e range. Fix the admission constants
and use Qbar=2D_p (or twice the applicable deterministic ceiling in (17)-(18)).
Then, on the complement of (16),

    H_p<=4D_p/(cN)=O(T^-2),
    S_p<=2D_p=O(T³),

and the exponent in (16) is order T³ for a fixed positive e0 and an entrance
with D_p of order T³. If using a deterministic ceiling, insert that ceiling
consistently into Qbar, v_p, and the lower martingale margin; the exact formula
(16) is the primary claim. This holds with the entire growing interval

    e0<=e<=νT²,       E<=νN,       L<=Hν²N,

subject to the explicit stops and (1)-(4). No convergence of E or time-change was
used to earn these bounds.

Most importantly, **one p=2 budget is enough for every exponent p>=2**. Namely

    W_2=A/e²+3T³/e,
    C+D+8A+12E<=B/2,
    D_2<=HT+3T³/e0+ST/e0²,
    H_p<=e0^(2-p)H_2,    S_p<=e0^(2-p)S_2.                (19)

This supplies a reusable weighted budget for the decreasing clock derivatives
without paying a separate failure probability for each derivative exponent.

## 6. What this closes, and what it does not

The expected scaling heuristic A≈e⁴/T³ and dt≈Te^-4de suggested H_p=O(T^-2).
Equations (8)-(19) actually prove that weighted scale, plus the source-time
budget S_p=O(T³), with a literal full-chain stochastic cost. The cancellation is
through the positive storage A e^-p+3T³ e^(1-p)/(p-1), not through assuming the
heuristic or propagating a full state approximation.

This earns weighted capture, source, and fast-A occupation. It does **not** earn
that the process enters or remains in the padded cone, that B stays above cN,
that A stays below εN, or that a terminal boundary is reached. It also does not
by itself bound the clock residual's weighted imbalance integral, for example

    T^-3 ∫ Z² e^-4 dt.

Controlling only L and A allows Z² comparable to L², so silently deleting this
term would be invalid. A separate imbalance admission/control or another
corrector is required. All clock derivative claims remain subject to their
own receipt, and the corrected-clock exit consumer is not proved here.

## 7. Exact checks

`check_weighted_source_time.py` builds all twelve reactions directly and verifies
(6), the exact jump formulas, and the bracket for p=2,3,5 by rational symbolic
algebra. Exact rational finite-state checks test (7), (8), (12), and (14) under
their admitted conditions. The resulting `weighted_exact_checks.json` is a
supplementary check, not independent receiving review or a clearance certificate.
