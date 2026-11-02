# One proper receiver for every high-anchor state with hidden inventory

Author theorem building on HIGH_ANCHOR_ACTUAL_NORMALIZATION.md. This closes
the receiving-value problem for ALL hidden states in that region, not merely
their clock. It still does not close the low-anchor boundary or axis trace.

Use the finite raw constants a,L,D,B0 and the globally defined physical work
Psi from that theorem. For each port define

    h_i=|B_i-C_i|+3min(B_i,C_i)/2+(min(B_i,C_i) mod2)/2,
    g_i=max(A_i-h_i,0).

Choose any fixed positive weights eta_i, H=max eta_i, h=min eta_i. Let

    Q=sum eta_i g_i^2,
    b=a+1,    c0=ceil(8b^2),
    C_core=54H(2H/h+1) max_i sum_(i->j) kappa_ij/alpha_i3,
    C_block=3HD,
    C=8(C_core+C_block+1/B0),
    U=Q+C(Psi+c0)^2.                                   (R1)

Each core edge has source A_i+A_j+2B_i+2C_i and transfers its B,C pair to j.
The constant sums every actual directed edge once. This includes all rates
of the six-species diagnostic and arbitrary finite pair-transfer graphs.

The same U is defined on EVERY physical state, with no signed-profile
choice or external receiving law. Put k_i=|B_i-C_i|+ceil(min(B_i,C_i)/2).
Then k_i<=h_i<=3k_i, K=sum k_i<=Psi, hidden population<=4K, and

    total population <=sum g_i+7Psi.

Thus U is proper and comparable, with raw finite constants, to
(1+total_population)^2. The shift c0 causes no loss of properness.

## All genuine block reactions are paid

While A_i>=L, terminal source3 leaves g_i unchanged exactly: A_i and h_i
both decrease by3. Source2 changes f_i=A_i-h_i by-1 or0. The only positive
changes of g_i come from source0 at r_i<0 and odd minority, or source1 at
r_i>0 and odd minority. Each has delta f_i=+1 and is an OTHER channel in
the frontier classification. Its positive Q increment is at most3H A_i.
The per-port factorial ratio used in the work theorem is H_i<=D/A_i F_i.
Consequently the complete positive block contribution to LQ is at most

    C_block F<=C_block q_nc.                            (R2)

No positive channel or empty-input path is omitted.

## All actual core transfers are paid

A transfer i->j changes f_i by+3 and f_j by-3. Truncation at zero gives

    delta Q<=6 eta_i g_i-6 eta_j g_j+9(eta_i+eta_j).

If this increment is positive, g_j<=(H/h)A_i+3H/h. Since h_j<=3Psi,

    A_j<=(H/h)A_i+3H/h+3Psi.

The positive increment is at most12H A_i because A_i>=3. Multiplying by its
ACTUAL rate kappa_ij A_i A_j u_i, u_i=(B_i)_2(C_i)_2, and using
(A_i)_3>=2A_i^3/9 gives

    [core positive contribution i->j]
       <=54H(kappa_ij/alpha_i3)(2H/h+Psi) lambda_terminal,i
       <=54H(kappa_ij/alpha_i3)(2H/h+1)(1+Psi)
                                      lambda_terminal,i.

Sum the finite directed edge list. Since every donor anchor is>=L, each
charged terminal is genuinely enabled when its core source is enabled.
Therefore

    LQ <=[C_block+C_core(1+Psi)]q_nc.                    (R3)

This charges all core paths at their actual rates. It does not replace the
core by an equilibrium, require a mixing gap, or bound its activity by a
fictitious finite event clock.

## The common physical Foster contract

The work theorem proves L Psi<=-q_nc/8 whenever hidden inventory is nonempty
and all anchors>=L. All its noncore increments are bounded by b; core
increments are zero. Hence

    L(Psi+c0)^2
       <=-(Psi+c0)q_nc/4+b^2 q_nc
       <=-(Psi+c0)q_nc/8.                               (R4)

Combining (R1)--(R4), with Psi+c0>=1+Psi and q_nc>=B0, yields

    L_actual U <=-(Psi+c0)q_nc/B0 <=-1.                  (R5)

This is a quantified actual-generator inequality from EVERY high-anchor
state with any nonempty hidden inventories. It includes arbitrarily large
pair differences, all physical states formerly represented by signed packet
residuals, arbitrary ratios of anchors, and every genuine reaction.

At sigma=first{hidden inventory zero OR some A_i<L}, localization and
nonexplosion earned in the work theorem give the actual SAME-receiver bound

    E_x[sigma+U(X_sigma)]<=U(x).                         (R6)

Thus every low-anchor landing and every joint-axis landing is paid at this
one proper physical U. The construction is finite arithmetic from the raw
list and the displayed freely chosen eta_i. It is an acquired inequality,
not an unevaluated hitting expectation being called a numerical compiler.

## Remaining regions, without composition inflation

The pointwise inequality deliberately excludes the joint anchor axes. There
U=sum eta_i A_i^2+C c0^2, and empty input launches a small borrowed workload.
The previous theorem supplies a complete actual axis busy-period kernel with
uniform physical and noncore-count tails; its inward quadratic drift still
has to be proved for the chosen eta_i.

States with one or more A_i<L also remain. U receives their arrivals, but
this theorem has not supplied their outgoing return operation. The former
central-face/star operations use a different receiver; their statements do
not automatically compose with (R6). A full six-species recurrence theorem
and a broader weak-reversibility principle therefore remain unproved.
