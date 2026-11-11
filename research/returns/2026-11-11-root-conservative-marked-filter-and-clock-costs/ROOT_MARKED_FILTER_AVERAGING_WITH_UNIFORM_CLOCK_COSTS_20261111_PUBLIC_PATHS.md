Timed marked-path averaging from a bounded conditional filter
ROOT, 11 November 2026 Brisbane

This note constructs the whole-path interface left OPEN in
ROOT_UNIFORM_CONSERVATIVE_KINETIC_LIFT_AND_PATH_INTERFACE_20261111.txt.
It keeps actual continuous event times, original null/parallel marks,
conditional post-event states and physical clock costs. It does not use a
stationary target, a computed partition, a minimum invariant probability,
state enumeration or a Markov assumption on an adversarially faulted marginal.
The conditional-filter calculation is NOMINAL; faults are paid separately.

1. FINITE-FIBRE MARKED MODEL

Let E be a finite fine state space, pi:E->X a projection, and E_x its fibres.
Hidden transitions have generator Q_x and preserve x. They may carry hidden
labels; invisible self-events do not change Q_x. For each OBSERVED label r,
let B_r(u,v)>=0 be its transition kernel, with b_r(u)=sum_v B_r(u,v).
The kernel may include u=v: an observed null event is retained. From E_x it
lands in E_(F_r(x)), where the deterministic map F_r is fixed by that label.
Distinct labels may have the same F_r. Assume
 b(u)=sum_r b_r(u)<=Lambda everywhere.                 (1)
Every hidden fibre has invariant probability mu_x. Its nominal kernel P_x(t)
satisfies the UNIFORM Dobrushin bound
 sup_(u,v in E_x) TV(P_x(t;u,.),P_x(t;v,.))<=alpha(t),
 0<=alpha(t)<=1, integral_0^infinity alpha(t)dt<=a.      (2)
All bounds are independent of fibre size. The initial fine distribution in
its given fibre can be arbitrary. E need not be explicitly enumerated.

Define the averaged observed chain by marked intensities
 bar_b_r(x)=sum_(u in E_x) mu_x(u)b_r(u),               (3)
and decoded update x->F_r(x). This includes genuine null and parallel marks.
Let Y be the observed marked path of the original fine process and Ybar the
averaged marked path, with the same initial x. Then on reference[0,tau],
 TV(Law(Y),Law(Ybar))<=2Lambda a(1+2Lambda tau)
                         <=4Lambda a(1+Lambda tau).   (4)
The claim concerns the ENTIRE timed marked path, not just its endpoint or
an unclocked sequence. No positive lower bound on individual b_r is required.

2. CONDITIONAL LAW BETWEEN ACTUAL OBSERVED EVENTS

Condition on an observed marked history through time s0 immediately after
its last mark (or s0=0). The current decoded state is x. Before the next
observed mark, the unnormalized fine row distribution evolves with
 Q_x-diag(b). The diagonal killing includes ALL observed marks, including
null marks: their absence is information even when they would not change x.
For a normalized conditional distribution nu_t at age t>=0, differentiation
of this finite-dimensional killed evolution gives
 nu_t'=nu_t Q_x+G_t,
 G_t=nu_t(b)nu_t-nu_t diag(b).                         (5)
G_t has total mass zero and signed total-variation norm at most Lambda.
Indeed its l1 norm is sum_u nu_t(u)|nu_t(b)-b(u)|<=2Lambda.
The survival probability is positive at every finite age since b<=Lambda,
so this normalization is legitimate. Its numerical value is never computed
by the compiler or charged as a reciprocal-probability oracle.

Variation of constants gives
 nu_t-mu_x=(nu_0-mu_x)P_x(t)+integral_0^t G_s P_x(t-s)ds.
For any zero-mass signed measure xi, the Dobrushin definition and its positive
and negative parts give ||xi P_x(t)||TV<=alpha(t)||xi||TV.
Consequently
 ||nu_t-mu_x||TV<=alpha(t)+Lambda a.                   (6)
At an observed r event, the posterior is nu_- B_r/nu_-(b_r).
It can be arbitrarily concentrated and the denominator arbitrarily small.
Only that it is a probability is used: restart (5)--(6) with this arbitrary
posterior in the new fibre. Thus no small marked intensity or rare posterior
introduces a reciprocal factor. This also covers F_r(x)=x and self-kernels.

3. FROM FILTERING TO TOTAL-VARIATION OF THE WHOLE MARKED PATH

Relative to its observed filtration, the true next-r intensity is
 lambda_r(s)=nu_s(b_r). The averaged comparator's intensity, while histories
agree, is bar_b_r(x). Let A_s be age since the last observed mark. By (1),(6),
 sum_r |lambda_r(s)-bar_b_r(x_s)|
 <=sum_u |nu_s(u)-mu_(x_s)(u)| sum_r b_r(u)
 <=2Lambda[alpha(A_s)+Lambda a].                      (7)

Construct both observed processes with common marked Poisson thinning until
their first unmatched r event. They then have exactly the same label and
continuous firing time at every matched event, not merely close firing times.
The conditional unmatched intensity is the left side of (7). After mismatch
continue each marginal according to its own intensities. Bounded intensity
and the finite hidden chain justify this construction; alternatively its
sequential conditional waiting-time kernels define the same coupling.
The true marginal is unchanged by the coupling. If N(tau) counts ALL true
observed marks, including null/parallel, then E N(tau)<=Lambda tau and
 integral_0^tau alpha(A_s)ds<=(N(tau)+1)a              (8)
pathwise, by splitting at EVERY observed event. Therefore mismatch probability
is bounded by
 2Lambda a E(N(tau)+1)+2Lambda^2 a tau
 <=2Lambda a(1+2Lambda tau),
which proves (4) by the coupling inequality. The initial layer and every
conditional post-mark layer are paid. There is no omitted internal clock,
tiny-holding-time asymptotic, likelihood-ratio bound or endpoint-only step.

4. THE CONSERVATIVE PREFIX LIFT AND ITS EXACT AVERAGE

Fix D>=3 and ANY labelled input reaction list R, m=|R|, with complexes of
order<=D and positive integer conservation weights omega. Weak reversibility
is unnecessary. Let B=max(1,omega.x0), U=1+B. The prior note gives the exact
private-prefix lift and nonnegative integer decoder P, identity on originals.
All auxiliary columns are nonzero; fine population<=B deterministically.
Every decoded directed edge, canonical lift and actual communicating class
is exact. The network structure depends only on R, not on numerical inputs.

Let M be the number of distinct complexes of order>=2 and S the number of
prefix species. M<=2m, S<=2m(D-1). Set raw first assembly/release coefficients
K theta,K and later assembly/release coefficients K,K, theta<=1.
For fixed decoded x, the tagged-prefix service proof in the prior note gives
 C_D(B)=D[8U]^(D-1),
 theta<=1/[1024(1+M)U^3 C_D(B)],
 h=16B C_D(B)/K,
 alpha(t)<=2^(-floor(t/h)), integral alpha<=2h.        (9)
This is an actual uniform common-atom estimate, not an assumed spectral gap.
If S=0 the fibre is a singleton, and these bounds are simply loose.

Give raw central label r coefficient k_r/theta if its source order>=2,
and k_r otherwise. The EXACT fast-fibre average is
 bar_b_r(x)=k_r(x)_(y_r) q_theta(x-y_r)/q_theta(x),
 q_theta(x)=sum_(c:Ec<=x) theta^|c| (x)_(Ec)/c!,
 1<=q_theta(x)<=exp(S theta B^D).                     (10)
The formula is zero for a disabled source; an empty source has ratio one.
It follows by factorial cancellation, not a partition-evaluation routine.
The prior note proves the invariant weights by detailed balance of the
hidden assembly/release pairs. Formula (10) does not assume the full R is
reversible, complex balanced or irreducible.

All raw central intensities are bounded in sum by
 Lambda=m U/theta.                                  (11)
Apply (4) with a=2h to obtain the complete nominal fine/averaged path bound
 <=8Lambda h(1+Lambda tau).                          (12)
Let zeta=S theta B^D<=1. By (10) the relative difference of averaged and
reference-r intensities is<=2zeta. Ordinary all-mark intensity coupling with
the reference total intensity<=m U^D then gives
 TV(averaged path,reference path)<=2zeta m U^D tau.    (13)
This uses the true fixed conservation class, not a reflected truncation.
The finite state space appears only in the proof and is never enumerated.

An exact three-state illustration shows why observed null marks matter.
For the genuine original null label3A->3A, k=1, x0=3A, the fibre states are
(A,C2,C3)=(3,0,0),(1,1,0),(0,0,1). Fast transitions are6Ktheta,K,K,K along
the two adjacent pairs. Their stationary weights are1/6,theta,theta, giving
q_theta(3)=1+12theta and averaged null-mark intensity6/(1+12theta).
Decoded STATE paths are identically3A at every scale and convey no error.
But an observed mark forces the posterior to C3 with instantaneous marked
intensity1/theta. Equations (5)--(8) pay this actual post-mark layer and its
full time law; a state-only convergence theorem would say nothing about it.

5. ONE EXPLICIT PARAMETER ORDER AND PHYSICAL REALIZATION

Given rational0<epsilon<1/8,tau>0,0<k_r<=1, choose
 theta=min{1,1/[1024(1+M)U^3 C_D(B)],
             epsilon/[32(1+S)(1+m)U^(2D)(1+tau)]},
 Lambda=m U/theta,
 K=max{1,2048(1+Lambda)B C_D(B)(1+Lambda tau)/epsilon},
 H=1+K+theta^-1.                                    (14)
Then (12)<=epsilon/16 and (13)<=epsilon/16.
All quantities are rational, with theta chosen BEFORE K and H.

Divide ALL raw coefficients by H. They are positive and<=1, including
K theta/H,K/H and k_r/(theta H). On physical time Ht the nominal fine law
equals the raw fine law at reference t. This is one constant clock rescaling,
not deletion of internal residence times or an externally scheduled switch.

Let m_f=2S+m be the number of fine labelled channels. Choose
 delta=min{1/2,epsilon/[16(1+m_f)U^2 H(1+tau)]}.        (15)
For arbitrary REAL PREDICTABLE multipliers in[1-delta,1+delta], couple the
faulted and nominal FINE processes, flagging every mismatched fine mark even
when its decoded change is zero. Until that first mismatch the entire fine
history is shared; arbitrary coordinated fault dependence on that history
and external randomness remains predictable. The unmatched intensity is
<=delta m_f U^2 since normalized coefficients<=1 and reactant order<=2.
Hence their fine-path mismatch probability on physical[0,H tau] is
 <=delta m_f U^2 H tau<=epsilon/16.                   (16)
This argument does NOT regard the faulted marginal or its observed filter
as Markov. The nominal filtering theorem is applied only after this separate
fine-path coupling. Canonical initialization and hidden labels are preserved.

By triangle inequality (12),(13),(16), the ENTIRE decoded timed original-
labelled path, keeping original null/parallel marks, differs from the original
reaction path by at most3epsilon/16<epsilon in TOTAL VARIATION. Arbitrary
initial auxiliary equilibria, warm start, state sampling and external
controllers are not used. Nonexplosion is immediate here from the finite
conserved fine state set and its uniformly bounded hazard, including faults.

6. UNIFORM PHYSICAL AND BINARY COSTS

Let L be complete binary input length and
 W=2+d+m+B+tau+tau^-1+epsilon^-1+sum_r k_r^-1.
The construction needs no constants depending on the reaction graph, a gap,
minimum invariant probability or an enumerated class. Put c_D=D8^(D-1),
 C0=1+3072c_D+128(2D+1),
 CK=1+2048(1+C0)^2 c_D, CH=1+CK+C0.
Directly from (14), since U<=W,
 theta^-1<=C0 W^(2D+4),
 Lambda<=C0 W^(2D+6),
 K<=CK W^(5D+14), H<=CH W^(5D+14),
 H tau<=CH W^(5D+15).                               (17)
Also m_f<=4Dm, so (15) gives
 delta^-1<=[2+32(4D+1)CH]W^(5D+19).                  (18)
The reciprocal of every positive normalized coefficient is at most
 H max(theta^-1,max_r k_r^-1)
 <=CH(1+C0)W^(7D+18).                               (19)
An empty maximum is zero; the m=0 case can be emitted directly with H=1.

All fine populations are<=B for EVERY physical time and fault history.
Expected ALL fine firing count by physical t is<=1.5m_f U^2 t;
by physical H tau it is<=6DCH W^(5D+18).              (20)
Every assembly/release/failed attempt/hidden/null/parallel firing is counted.
The prior null-label example still forces H>=c'_D N^(D-2)/m_f for large N,
so these polynomial slowdown costs cannot simply be suppressed.

For fixed D, list all private prefixes by a deterministic order of each
input complex, compare complex lists, and emit the O(Dm) species/channels,
decoder and label map. No graph/class enumeration or Grobner preprocessing
occurs. B is a sum of input integer products. Constructing (14)--(15) needs
only rational sums/products/minima/maxima and fixed integer powers O(D),
with rational coefficient bit lengths O_D(1+L). Grade-school integer
arithmetic and explicit dense decoder output take at most a computable
constant depending only on D times(1+L)^8 operations/bits/memory. A generous
single choice covering this implementation and (17)--(20) is
 p_D=7D+24, A_D=2^[100(D+1)^2].                       (21)
For example the displayed rational arithmetic uses O_D((1+L)^2) elementary
operations on O_D(1+L)-bit integers; dense description construction is
O_D((1+L)^3), and straightforward multiplication/division bounds fit the
stated eighth power. The explicit constants above and polynomial factors in
D are dominated by A_D. Output numerical magnitudes may be large, but their
binary descriptions and all physical time/rate/firing costs are charged.

7. SCOPE

Equations (4)--(21), with the prior note's actual graph/service construction,
give a full uniform bounded-order conservative kinetic-trajectory compiler
under precisely this ideal unit-volume mass-action resource model. Fixed D,
positive integer conservation, supplied rational rates and numerical capacity
B/horizon/accuracy costs are premises. This is not uniform polynomial physical
complexity for VARIABLE D, arbitrary unbounded open networks, detailed-balance
thermodynamic realizability, a practical DNA implementation, fuel/energy
accounting or an arbitrary efficient equilibrium sampler. The original
reaction event count itself can obstruct stronger clock claims.

This independent ROOT derivation is mathematical preparation for a natural
completed boundary. It does not alter an already posted scientific body,
interrupt productive work or assert native retrieval. Earlier primary-source
contracts and every known/unknown source/access/transfer hold are unchanged;
no new source access or recovery was used for this derivation.
