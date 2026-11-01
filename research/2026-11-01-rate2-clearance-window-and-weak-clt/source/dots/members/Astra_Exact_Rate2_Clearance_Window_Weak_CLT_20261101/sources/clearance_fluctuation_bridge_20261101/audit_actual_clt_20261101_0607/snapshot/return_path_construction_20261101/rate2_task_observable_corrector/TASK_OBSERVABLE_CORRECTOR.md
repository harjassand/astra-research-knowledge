# A full-chain C² task-observable corrector with paid compact-window costs

**Author construction, not independently reviewed.** This is a reusable finite-N,
stopped transport identity and error certificate. It does **not** acquire the
observable, prove boundary clearance, or justify a growing-compact/global passage.
It uses the actual rate-2 count chain, all twelve channels, and no fast-state
stationary law. The primary estimates retain state/channel-specific derivative
weights, so a later clock observable can use decreasing sensitivity near blow-up.

## 1. Model, fixed reference scale, and the actual jumps

Write G for the full generator. Fix N>=1, T=N^(1/5), and put

    L=A+(C+D)/2, Z=C-D, n=A+B+C+D+E,
    z=(l,e)=(L/T,E/T³), h=AE, a2=A(A-1),
    Q=L²-CD=2AL-A²+Z²/4 >=0.

N is fixed, not the current total count. Propensities use falling factorials.
The following table is the entire model. Values in rows with zero rate are
irrelevant; every active transition has a nonnegative endpoint.

| channel r | rate λ_r | ΔL=u_r | ΔE=v_r | Δh=w_r |
|---|---:|---:|---:|---:|
| 0→A | 1 | 1 | 0 | E |
| A→0 | A | -1 | 0 | -E |
| 2A→AC | a2 | -1/2 | 0 | -E |
| AC→2A | AC | 1/2 | 0 | E |
| 2A→AD | a2 | -1/2 | 0 | -E |
| AD→2A | AD | 1/2 | 0 | E |
| 2A→AE | a2 | -1 | 1 | A-E-1 |
| AE→2A | h | 1 | -1 | E-A-1 |
| AE→CD | h | 0 | -1 | -A-E+1 |
| CD→AE | 2CD | 0 | 1 | A+E+1 |
| CD→AB | CD | 0 | 0 | E |
| AB→CD | AB | 0 | 0 | -E |

In particular, the fast AB↔CD channels do not move z. This fact must not be lost
by bounding every slow jump by a uniform nonzero jump size.

Directly summing this table gives

    GL=1+A+AL+h-3A²,
    GE=a2-2h+2CD,
    Gh=-Nh+3EL²+r_h,
    r_h=E-3EQ+2ACD+A(A-1)²+2CD
        +h(N-B+2L+2-7A).                                      (1)

The last coefficient also equals N-n+E+4L+2-8A, hence

    |N-B+2L+2-7A| <= |n-N|+E+4L+2.                           (2)

The useful exact rate sums are

    q_LL=Σλu²=1+A+(3/2)a2+A(C+D)/4+h,
    q_EE=Σλv²=a2+2h+2CD,
    q_LE=Σλuv=-(a2+h),       w_LE=Σλ|uv|=a2+h,
    s_L=Σλ|u|=1+A+2a2+A(C+D)/2+h,
    Σλ|v|=q_EE.                                              (3)

## 2. Exact corrected-observable identity; only C² is required

Let f be C² on an open neighborhood of every segment connecting an admitted z to
its one-jump endpoints. Set g=f_l and

    F_f(x)=f(z)+h g(z)/(NT),
    V=(1+3l²e, 2l²).

For each row let δ_r=(u_r/T,v_r/T³), h'_r=h+w_r, and

    R2_f=Σ_r λ_r [f(z+δ_r)-f(z)-Df(z)·δ_r],
    P_f=(1/(NT)) Σ_r λ_r h'_r [g(z+δ_r)-g(z)].

Then the following identity is exact, without an asymptotic remainder:

    G F_f=(V·Df)/T + R_f,
    R_f= f_l(z)(A+AL-3A²)/T
         + f_e(z)(a2-2h-2Q)/T³
         + f_l(z) r_h/(NT) + R2_f + P_f.                    (4)

Proof: the jump product rule is

    G(hg)=g Gh+Σ_r λ_r h'_r Δ_r g.

The -Nh term in (1) cancels the h f_l/T from GL, and
3EL²/(NT)=3l²e/T because N=T⁵. The leading E drift is 2L²/T³=2l²/T.
This proves (4). It does not replace G by a frozen fast-A generator.

For precise local derivative accounting, retain the exact line integrals

    R2_f=Σ_r λ_r ∫₀¹(1-θ) δ_rᵀ D²f(z+θδ_r) δ_r dθ,
    P_f=(1/(NT))Σ_r λ_r h'_r ∫₀¹
        [f_ll(z+θδ_r)u_r/T+f_le(z+θδ_r)v_r/T³] dθ.            (5)

There is no need to differentiate f three times. Both (5) terms are identically
zero on AB↔CD rows.

### 2.1 Channel-weighted, pointwise residual bound

Let F_ij,r(x)=sup_{0<=θ<=1}|∂_l^i∂_e^j f(z+θδ_r)|. Define

    H_h=E+3EQ+2AL²+A(A-1)²+2L²
        +h(|n-N|+E+4L+2).

Since 0<=A<=L,

    |R_f| <= |f_l(z)|(A+2AL)/T
             +|f_e(z)|(a2+2h+2Q)/T³
             +|f_l(z)| H_h/(NT)
             +Σ_r λ_r [ F_20,r u_r²/(2T²)
                        +F_11,r |u_r v_r|/T⁴
                        +F_02,r v_r²/(2T⁶)]
             +(1/(NT))Σ_r λ_r h'_r
                        [F_20,r |u_r|/T+F_11,r |v_r|/T³]. (6)

All terms are nonnegative explicit charges. In particular the drift correction
is weighted by the actual |f_l(z)|, not automatically its worst compact value.
A clock whose sensitivity decays may use that decay here. Formula (5), rather
than its absolute-value bound, also retains any genuine sign cancellation.

For a simple polynomial bound, h'_r<=(A+1)(E+1)=:h⁺ on every active row. If
F_ij bounds the corresponding derivatives on all segments, the final two lines
of (6) are at most

    F_20 q_LL/(2T²)+F_11 w_LE/T⁴+F_02 q_EE/(2T⁶)
    +F_20 h⁺ s_L/(NT²)+F_11 h⁺ q_EE/(NT⁴).                (7)

This coarse specialization is optional, not part of the exact identity.

## 3. Exact martingale jumps and bracket, including the fast channels

The Dynkin martingale of F_f has exact jump

    Δ_r F_f=Δ_r f + w_r g(z)/(NT)+h'_r Δ_r g/(NT).           (8)

Thus define the channel-weighted bound

    d_r=F_10,r |u_r|/T+F_01,r |v_r|/T³
        +|w_r| |f_l(z)|/(NT)
        +h'_r[F_20,r |u_r|/(NT²)+F_11,r |v_r|/(NT⁴)].

Then |Δ_r F_f|<=d_r and its exact bracket density is

    q_F=Σ_r λ_r(Δ_r F_f)² <= Σ_r λ_r d_r².                 (9)

On AB↔CD, (8) is exactly ±E f_l(z)/(NT). Their combined bracket contribution is

    (AB+CD) E² f_l(z)²/(N²T²),

not a rate times an order-one jump. This is where keeping local clock sensitivity
can be especially important.

The exact h bracket, useful in a compact specialization, is

    q_hh=E²[1+A+2a2+A(C+D)+CD+AB]
          +a2(A-E-1)²+2h[(E-1)²+A²]
          +2CD(A+E+1)².                                    (10)

For a statewise common h⁺ and global derivative bounds define

    a=F_10/T+h⁺ F_20/(NT²),
    b=F_01/T³+h⁺ F_11/(NT⁴), c=F_10/(NT).

The following explicit bounds then hold:

    |Δ_r F_f|<=a|u_r|+b|v_r|+c|w_r|,
    max_r |Δ_r F_f|<=a+b+c(A+E+1),
    q_F<=2[a²q_LL+2ab w_LE+b²q_EE]+2c²q_hh.               (11)

These are bounds on the actual full-chain martingale. They include every product
jump/covariation term, not merely the martingale of the uncorrected f.

## 4. A literal stopped compact-window certificate

Fix K,M,S>0 and a total-count band width d>=0. Let τ₀ be the first of time ST,
L>=KT, E>=MT³, or |n-N|>d (with a chosen consistent first-crossing convention).
Assume the initial state is inside the physical region. Stop further at the
continuous occupation budgets

    H=∫₀^τ A dt <= Hbar,
    J=∫₀^τ A² dt <= Jbar,
    Z2=∫₀^τ Z² dt <= Zbar.                                 (12)

An inequality with strict thresholds can equivalently use the first hitting time
of that clock; its value at the stop is its budget. All integrals use pre-stop
states. The one-jump enlarged scaled rectangle
[0,K+1/T]×[0,M+1/T³] is enough for derivative norms and endpoint corrections.
There is no explosion: n(t)=n(0)+I(t)-D_A(t)<=n(0)+I(t), with I a rate-one
Poisson process, and finite total count gives finitely many states and bounded rates.

Set

    U=ST+Hbar+(3/2)Jbar+(KT/2+MT³)Hbar,
    W=Jbar+MT³ Hbar,
    V_E=Jbar+2MT³ Hbar+2K²ST³,
    V_L=ST+Hbar+2Jbar+(KT+MT³)Hbar,
    Hplus=(KT+1)(MT³+1), Rplus=KT+MT³+1,

    R_h^int= MST⁴+6MK T⁴ Hbar+(3/4)MT³ Zbar
             +2K²T² Hbar+KT Jbar+2K²ST³
             +MT³(d+MT³+4KT+2)Hbar.                       (13)

Here U,W,V_E,V_L bound respectively the integrals of q_LL,w_LE,q_EE,s_L.
Using Q<=2AL+Z²/4, (6)-(7) give the deterministic integrated error budget

    ρ_f=F_10 (1+2KT)Hbar/T
        +F_01[Jbar+2MT³Hbar+4KT Hbar+Zbar/2]/T³
        +F_10 R_h^int/(NT)
        +F_20 U/(2T²)+F_11 W/T⁴+F_02 V_E/(2T⁶)
        +F_20 Hplus V_L/(NT²)+F_11 Hplus V_E/(NT⁴),        (14)

so ∫₀^τ|R_f|dt<=ρ_f. The displayed constants are literal; there is no hidden
Gronwall constant.

For the bracket define

    Φ=M²T⁶[ST+Hbar+2Jbar+2KT Hbar+K²ST³+(N+d)Hbar]
       +Rplus² V_E,

    a*=F_10/T+Hplus F_20/(NT²),
    b*=F_01/T³+Hplus F_11/(NT⁴), c=F_10/(NT),
    v_f=2[(a*)²U+2a*b*W+(b*)²V_E]+2c²Φ,
    j_f=a*+b*+c Rplus.                                    (15)

Indeed B<=n<=N+d before the stop, and (10) is bounded by

    E²[1+A+2A²+2AL+L²+AB]+(A+E+1)²[A²+2h+2L²],

whose integrated bound is Φ. Consequently the stopped martingale bracket is
at most v_f, and all its jumps have absolute value at most j_f.

For every x>0, the bounded-jump exponential martingale inequality gives

    P(sup_{t<=ST}|M_{F_f}(t∧τ)|>=x)
      <=2 exp[-x²/(2(v_f+j_f x/3))].                       (16)

One direct proof uses exp(θy)-1-θy<=θ²y²/[2(1-θj_f/3)] for |y|<=j_f and
0<θ<3/j_f, the compensated jump exponential, optional stopping, then applies
the same bound to both signs. This only uses the actual stopped bracket budget.

The raw observable therefore has the concrete path certificate

    sup_{t<=ST}| f(z(t∧τ))-f(z(0))
                 -∫₀^{t∧τ} (V·Df)(z(s)) ds/T |
      <= ρ_f + 2Hplus F_10/(NT)+x                          (17)

outside the event in (16). If v_f=j_f=0 the martingale is identically zero,
and the tail probability is zero. The endpoint correction includes the crossing jump;
using only the pre-stop bound KT·MT³ would miss that possible overshoot.

If a separately acquired f satisfies V·Df=-1 on this region, (17) controls
f(z(t∧τ))+(t∧τ)/T-f(z(0)). This conditional specialization is the interface to
a remaining-time clock. It is not itself a clearance theorem: all exits, the
clock's boundary interpretation, and any continuation beyond this rectangle
still belong to the consumer.

## 5. The occupation and imbalance budgets can themselves be charged

This section shows that (12) is not an unearned fast-state equilibrium premise.
Assume

    N-d-2KT-MT³>=N/2,      2KT<=N/4.                       (18)

Then B>=N/2 before τ₀. The exact full-chain A generator gives

    GA=1-A-3a2+A(C+D)+3CD-AB
      <=r-(N/4)A,        r=1+3K²T².                       (19)

Hence stopped Dynkin yields

    E ∫₀^τ₀ A dt <=4[A(0)+rST]/N.                         (20)

No channel was deleted. An exponential clock bound is also available. The
A-martingale has unit jumps and bracket density at most

    q_A<=r+C_A A,        C_A=N+d+1+5KT+2MT³.

Stop at τ₀ or H=Hbar, and put

    v_A=rST+C_A Hbar,
    x_A=NHbar/4-A(0)-rST.

If x_A>0, H reaching its budget before the physical stop forces M_A>=x_A,
since terminal A is nonnegative. Thus

    P(H exits before τ₀)<=exp[-x_A²/(2(v_A+x_A/3))].        (21)

The J budget needs no separate probability if Jbar>=KT Hbar.

For imbalance, summing the same twelve channels gives exactly

    GZ=-AZ,
    q_Z=2a2+A(C+D)=2A(L-1)<=2KT A.                        (22)

The stopped process solves dZ=-AZdt+dM_Z. Integration by parts with the damping
factor, or variation of constants, gives the pathwise bound

    sup_{s<=t}|Z(s∧τ)|<=|Z(0)|+2sup_{s<=t}|M_Z(s∧τ)|.

The statement remains valid after freezing at the stop. Before H reaches its
budget, the Z bracket is at most 2KT Hbar, with unit jumps. Consequently, for a
chosen zmax>|Z(0)| and m_Z=(zmax-|Z(0)|)/2,

    P(|Z| reaches zmax before τ₀ or H exits)
      <=2 exp[-m_Z²/(2(2KT Hbar+m_Z/3))].                 (23)

Stopping at that cap guarantees Zbar=ST zmax²; use the strict pre-exit bound in
the occupation integral, so its crossing overshoot is harmless. Alternatively,
without a supremum cap,

    E∫₀^{τ₀∧τ_H} Z² dt <=ST[Z(0)²+2KT Hbar],             (24)

by the exact identity G(Z²)=-2AZ²+q_Z. Markov's inequality charges any Z2 budget
from (24). These are alternative ways to pay the same explicit Z² defect.

The total-count stop must also be paid if a consumer removes it. Precisely,
n=n(0)+I-D_A. Thus an upper-band exit requires I(ST)>=d-(n(0)-N), and a lower
exit requires D_A>=d+(n(0)-N). If these positive thresholds are rounded upward
to integers k_+,k_-, then for k_+>ST,

    P(I(ST)>=k_+) <= exp[-k_+ log(k_+/(ST))+k_+-ST].

On H<=Hbar and for k_->Hbar, the analogous counting-process exponential gives

    P(D_A>=k_-, H<=Hbar)
      <=exp[-k_- log(k_-/Hbar)+k_--Hbar].                  (25)

Use a weaker threshold if the band convention has strict crossing. These are
safe bounds, not assertions that a count-band exit is automatically harmless.

## 6. Scale check and scope

For fixed K,M,S, initial A(0)<=KT and Z(0)=0, take d=d₀T³ (d₀>0), Hbar=h₀T^-2
with h₀ large enough that x_A is a positive order-T³ margin, Jbar=KT Hbar, and
zmax=√T. Conditions (18) hold for sufficiently large T. Then

    Zbar=ST²,    ρ_f=O(T^-1),
    endpoint correction=O(T^-2),
    v_f=O(T^-1), j_f=O(T^-1),
    H-exit bound=exp[-Ω(T³)],
    imbalance-exit bound=2 exp[-Ω(√T)].                   (26)

The constants here depend explicitly on (13)-(15) and the five C² norms; the
formulas, not the asymptotic notation, are the finite-N certificate. Count-band
costs are given by (25), not omitted. K and M remain fixed in this statement.
For fixed target precision one may instead select zmax proportional to T with
a small coefficient, obtaining a small fixed imbalance residual and an
exp[-Ω(T)] imbalance cost. Every such choice must be inserted into (14).

The newly supplied operation is **compile a chosen smooth slow-state task
observable into an actual-chain nearly-transported observable, with exact
finite-jump error, actual fast-channel bracket, and paid stop clocks**. It
avoids propagating an entire state approximation with a large Lipschitz/Gronwall
constant. It does not establish that arbitrary f is useful, construct the
remaining-clock f, or prove a finite-N boundary-clearance probability. In
particular, decay of a special clock's derivatives must be received and inserted
into the local formulas (5)-(9); no global near-blow-up conclusion follows from
this compact specialization alone.

## 7. Reproducible exact checks

Run `python check_task_observable_corrector.py` from any directory. The script
constructs all twelve channels directly, verifies the exact generator/jump-rate
identities, and checks (4) for all monomials through total degree four. It also
performs finite-state deterministic falsification checks of the polynomial
bounds (not a simulation or a proof substitute). Results are in
`exact_checks.json`. The C² identity and inequalities are proved above; symbolic
checks are supplementary and do not constitute independent receiving review.
