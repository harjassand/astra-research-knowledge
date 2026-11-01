# Exact p=2 storage-coefficient tradeoff

**Separate author addendum, unreviewed.** The fixed-coefficient-3 proof and its
check results are unchanged. This addendum improves only the weighted occupation
admission/cost. It does not establish entrance, cone survival, or clearance.

## 1. Exact finite-step quantities

Let e=E/T³, N=T⁵, φ=e^-2, and choose k>3/2. Use the positive storage

    W_k=A/e²+kT³/e.

Assume every pre-stop E is at least an integer m>=8. Set

    a=m/(m+1),       b=m/(m-1),
    d=m(2m-1)/(m-1)²,
    σ=2ka-3 >0.                                          (1)

The positivity condition on σ is literal: k must exceed (3/2)(1+1/m), not merely
3/2 at a fixed finite m. For the same secants as in the fixed-3 proof, direct
finite algebra gives

    α_+/φ=E/(E+1),
    α_-/φ=E/(E-1),
    E d_-φ/φ=D(E)=E(2E-1)/(E-1)².                        (2)

Thus α_+>=aφ, α_-<=bφ and D(E)<=d<=5/2 for E>=m>=8.
The last inequality follows from E²-8E+5>=0. Both E/(E-1) and D(E) decrease
with E>1, while E/(E+1) increases. No continuum approximation enters these
constants.

## 2. Full A² cancellation removes the extra A cap from this drift gate

Rewrite the exact A generator using L=A+(C+D)/2:

    GA=1+2A-5A²+2AL+3CD-AB.

The exact finite-jump storage generator is

    G W_k=φ GA+[a2(A-1)+2CD(A+1)]d_+φ
           +2A²E d_-φ-k(a2+2CD)α_+ +2kAEα_-.             (3)

The d_+φ term and -k a2α_+ are nonpositive. By (2),

    G W_k <=φ{1+A[2+2L+2kbE-B]+(2d-5)A²}-σCDφ
           <=φ{1+A[2+2L+2kbE-B]}-σCDφ.                  (4)

The actual -5A² in GA absorbs the backward weight derivative because d<=5/2.
This is why an extra upper bound A<=εN is unnecessary **for this particular
weighted drift estimate**. Of course A<=L is still used, and any A control
required by a separate clock/cone consumer remains its own burden.

Choose θ in (0,1). Under the literal statewise gate

    2+2L+2kbE <= (1-θ)B,                                 (5)

one obtains

    G W_k <= φ-θABφ-σCDφ.                                (6)

All twelve channels are present. Compared with the coarse fixed-3 condition,
the AE-storage cost is exactly controlled by 2kb, tending to 2k as m grows,
and the retained CD source coefficient is σ, tending to 2k-3.

In a growing cone l<=He², e<=νT², with B>=cN, a sufficient parameter gate is

    2/N+2Hν²+2kbν <= (1-θ)c.                             (7)

This is an explicit resource tradeoff, not a universal moderate-density claim.

## 3. Exact jump and bracket costs of the tradeoff

The four E-changing jump formulas in the fixed-3 proof remain exact with every
3 replaced by k; the other eight jumps are ±φ. The forward φ difference is
at most 2φ/E, and the backward difference is at most dφ/E. Hence

    |ΔW_k| <=[1+kb+d(A+1)/E]φ.                            (8)

For a cone l<=He², e<=νT², set

    J=1+kb+d(Hν+1/m),       j=J φ0,      φ0=e0^-2,         (9)

where the physical stop uses e>=e0 and E>=m (for example
m=ceil(T³e0)). One-step positivity requires e0>T^-3; the padded cone from the
fixed-3 proof remains an available stronger convention. Then j bounds every
stopped jump, including the exiting jump.

The exact total rate simplifies to

    q_A=1+AB+3CD+A²-2A+2AL+2AE
       <=1+AB+3CD+A(3L+2E).                              (10)

Gate (5) and kb>3/2 imply

    3L+2E <=(3/2)(2L+2kbE)<=(3/2)(1-θ)B.

Consequently one may take

    C_B=1+(3/2)(1-θ),
    q_W<=J² φ²[1+C_B AB+3CD].                            (11)

If separate ratio bounds L/B<=r_L and E/B<=r_E are already admitted, the
possibly sharper choice C_B=1+3r_L+2r_E is valid. This does not require an upper
B count; the actual capture occupation still pays its bracket.

## 4. Literal probability/occupation certificate

Stop at time ST or any physical/domain/gate exit, and define

    Q_k=∫[θAB+σCD]e^-2 dt,
    D_k=W_k(0)+ST φ0,
    C_Q=max(C_B/θ, 3/σ).

Stop additionally at Q_k=Qbar>D_k. The bracket and exit cost are

    v=J² φ0[ST φ0+C_Q Qbar],
    x=Qbar-D_k,
    P(Q_k reaches Qbar before the physical stop)
       <=exp[-x²/(2(v+jx/3))].                           (12)

The derivation is the same positive-storage Dynkin/Freedman argument as for
fixed3, with (6) replacing its drift. On the complementary event,

    ∫A e^-2 dt <=Qbar/(θ cN),
    ∫CD e^-2 dt <=Qbar/σ.                                (13)

Also E Q_k<=D_k, so the same bounds hold in expectation with Qbar replaced by
D_k. In the cone,

    D_k<=HT+kT³/e0+ST/e0².                                (14)

Thus the growing-range O(T^-2)/O(T³) weighted scales remain available. All
higher p>=2 weights follow from e>=e0 by the monotonicity relation in the
fixed3 proof.

There is a real price for making the admission gate less restrictive:

* k approaching 3/2 makes σ small, worsening source-time and bracket costs;
* θ approaching zero worsens capture occupation and the bracket constant;
* finite m worsens both b and σ;
* none of these parameter changes pays physical-domain exits.

## 5. A concrete moderate E/B gate, not a clearance claim

Take the exact rational parameters

    k=8/5,      m>=100,      θ=1/10.

Conservatively use the m=100 constants

    a=100/101,     b=100/99,     d=19900/9801,
    σ=17/101.

If B>=100, L/B<=1/10, and E/B<=1/5, then

    (2+2L+2kbE)/B
       <=1/50+1/5+64/99
       =4289/4950 <9/10.                                 (15)

Therefore this **weighted occupation gate** admits E/B as large as 0.2, with
a strictly positive capture coefficient θ=0.1 and source coefficient 17/101.
The sharper admitted-ratio bracket coefficient is C_B=17/10, so

    C_Q=max(17,303/17)=303/17.

One still inserts the actual cone ratio Hν in J. These finite constants demonstrate
the requested storage-resource tradeoff. They do not imply that the actual chain
can reach these ratios while retaining all other task requirements, or that the
interior-removal interface is ready at this threshold.

## 6. Exact checks

`check_storage_tradeoff.py` verifies (3), the full A² cancellation identity, and
all twelve jumps symbolically with arbitrary k, then tests the exact inequality
and bracket with rational arithmetic for admitted states and rational k values.
`storage_tradeoff_checks.json` records the result. Independent receipt is pending.
