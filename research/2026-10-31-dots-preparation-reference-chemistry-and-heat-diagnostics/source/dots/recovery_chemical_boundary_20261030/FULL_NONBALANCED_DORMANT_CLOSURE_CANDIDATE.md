# Full nonbalanced dormant connector: constructive closure candidate

30 October 2026. PERSONAL WORKING PROOF, NOT independently reviewed. This claims a route through the actual missing complete-cycle interface; it must be checked as a whole before any recurrence upgrade. The local accepted results and their frozen receipts are unchanged.

## 0. Exact target and dependencies

Use the six-fast-reaction, common-seed model in NONBALANCED_DORMANT_EXTENSION_V1.md: a0>=2, m=a0+2, q>m, all rates fixed positive; physical species A,C,D,B; fast residual graph `2a <-> a+d <-> c+d`, with extra `2a -> 2d -> a+d`. Connector `0 -> A+B -> mA+qB -> 0`. Full deficiency is one; unit fast rates are not complex balanced.

Claim sought: nonexplosion and classwise positive recurrence, with every total-count exponential moment under the invariant laws. This is this restricted four-species family, NOT general weakly reversible recurrence, uniform numerical rates, or historical novelty.

New working dependencies, all in this directory:
- ALL_POSITIVE_EXPONENTS_AND_OCCUPATION_GAP.md;
- CONNECTOR_POWER_SPENDING_KERNELS.md;
- SEED_PHASE_BUDGET_AND_FAST_RESET.md;
- DORMANT_GREEN_NONBALANCED_V2.md and SEED_INTERRUPTED_SOURCE_V2.md (now separately scoped reviewed).

The two local accepted foundations are the nonbalanced extension and occupation-normalized return receipts in recovery_chemical_review_20261030. The proof below uses actual values and kernels, never an assumed invariant law for the full network.

Let N=A+C+D, h=q-m, H(0)=0, and H(B)=j(m-1)+v when B=j(q-1)+v, 1<=v<=q-1. Set r=N-H(B). Fast reactions and activation preserve r. Immigration raises r by h only at positive B divisible by q-1. Clearing lowers it by h only when B>=2q-1 and B congruent 1 mod(q-1); otherwise clearing is neutral. These are exact integer identities.

Work killed on r<=r0, with r0 raised as needed. The section S consists of B=q and an enabled fast source. An inactive high entrance is designated for actual seeding, including low immigration wraps. Define the section cycle by the first connector event followed by the next entry to active S; fast reactions at the initial B=q do not count as a return.

## 1. Kernel facts retained with their input laws

At fixed b>=q:

(A) For every fixed s, clearing transports f_s(A)=(1+A)^-s with a constant C_s. Immigration spends m inverse powers and activation spends m-1, as in CONNECTOR_POWER_SPENDING_KERNELS.md. Low noncompulsory immigration spends one power. The constants are used for only finitely many exponents below.

(B) From positive D, the complete local first-connector episode has `(b)_q T<=C/n`, `(b)_q U<=C n^-1/2`, and clearing-output f_m moment at most C/n, where n=N-a0. A first connector's f_m-weighted output is also O(1/n): for activation its compensator integrand A f_m(A+m-1) is bounded, so it is at most CbT; immigration is at most CT. At the initial section b=q these constants are fixed.

(C) From any active input, T/U<=C/(1+A_in). For positive D, the first dormant-entry reward f_m is bounded by C(b)_q(1+A_in)^-2 U_+. Its absolute value is O(1/n). Later dormant A-occupation is at most C/(1+A_in) times U_+, and is O(1/n)/(b)_q absolutely.

(D) Positive-D entrance into D=0 before a connector is small in every fixed incoming profile: at most C n^-1/16 f_s. The dormant Green preserves `exp(theta r+lambda B) f_s` for any fixed lambda>=0. Thus a positive-D-to-dormant-to-seed continuation has arbitrarily small weighted norm after r0 is raised. A dormant section return is a terminal event, not an unpriced restart.

All statements extend to fixed polynomial residual weights `(1+r)^j exp(theta r)` above a raised threshold, using the actual weighted Green/processor proof, not differentiation of a constructed potential.

## 2. The actual phase processor, including unbounded seed B

Fix the finite exponent range needed for m inverse powers and their Cauchy–Schwarz bounds. Choose lambda large enough that EVERY ordinary clearing profile constant in this range satisfies `C_s exp(-lambda)<1/8`. This is paid phase weight, not a cap on B.

A positive-D processor begins at any active high phase, and stops on section return, residual-threshold entry, high immigration, the m-th noncompulsory low immigration, or ANY inactive high entrance. Before the stop:

- An ordinary high clearing decreases B by q. Its profile norm, including exp(lambda B), is at most C_s exp(-lambda q).
- A low activation followed by the next ordinary clearing changes B by -1. Its profile norm is at most C_s exp(-lambda). The low activation is NOT rare.
- A high activation has profile-preserving norm O(r^-1/4) by the uniform positive-D occupation bound and Cauchy–Schwarz at exponent 2s; its fixed exp(lambda(q-1)) multiplier is absorbed by raising r0.
- A positive-D dormant entrance, followed by the ACTUAL dormant Green until seed or section, has norm O(r^-1/16) times a fixed Green constant. Its seed may have arbitrarily large B; the exp(lambda B) budget pays it. This branch therefore also has small continuation norm.
- A low immigration increments a finite counter. Its norm is bounded and spends one inverse power. At most m such counter increments occur before the processor stop.
- B=0 has a compulsory neutral immigration. If the subsequent low activation occurs immediately, it enters B=q and ends the processor. Otherwise a counted low immigration occurs. Thus the compulsory launch does not introduce an uncounted recurrent neutral block.

At a fixed counter level, the sum of the continuing ordinary/error kernel norms is <1/2 after selecting lambda then r0. Its positive Neumann series is therefore finite. There are only m+1 counter levels; multiplying their bounded inter-level kernels proves bounded incoming-profile transport for the entire stopped processor. The same block series pays running physical w-cost and entry rewards. Low waiting times have a positive immigration-rate floor; high waiting costs are controlled by the local profile bounds. No finite phase cap, independent-reset law, or series with uncontrolled exponent C_s growth is used.

The killed residual factors r^-delta can be carried through this argument by the polynomial-weight version of the Green. This preserves their input scaling even when a dormant path decreases r substantially; simply substituting the input r for every later r would be invalid.

## 3. Actual continuation after a designated stop

An inactive high state with D>0 has A<a0, apart from finitely many small-n exceptions excluded by r0. At most a0 immigrations, or an earlier activation when A>=1, seed activity. Their total waiting mean is bounded, their B overshoot is bounded, and their upward r displacement is bounded by a0 h. A low input has an analogous bounded initial approach to an active high phase. These are physical continuations, not instantaneous resets.

From an active positive-D high input, the stopped processor's designated-exit norm is o(1) in its phase/residual weight:
- the initial high immigration is O(1/n);
- the initial high activation is O(n^-1/2) and is handled by the same processor sum;
- after an initial clearing, the actual f_m reset moment is O(1/n); the m low-race event and every inactive entrance are charged to that moment;
- a dormant entrance is O(r^-1/16) in profile norm and its Green is bounded.

Thus all designated exits, including their bounded seed/low approaches, have continuation norm epsilon(r0)<1/2 after raising the threshold. Iterate the ACTUAL processor and these repair branches, then pass from finite truncations by monotone convergence. This proves finite return/threshold time and

`E[w(r_return)+integral_0^return w(r_t)dt] <= C exp(lambda B_in) w(r_in)`

from positive-D inputs, with the corresponding incoming inverse-profile transport. From dormant inputs, first use the actual dormant Green to seed or section; the exp(lambda B_seed) law is already paid. No recurrence of the full network is used in constructing this repair.

The repair also works for fixed polynomial enlargements of w. Its initial exp(lambda B) factor MUST remain in arbitrary-phase cost bounds; it is not silently replaced by a constant. At the section B=q it is constant.

## 4. Complete-cycle source, with seed phase retained

Give degree 1 to noncompulsory low immigration, m-1 to high activation, and m to high immigration. The exact connector phase budget in SEED_INTERRUPTED_SOURCE_V2.md applies also across fast positive-D intervals, since those preserve N,B. A path with positive terminal r before its section return must contain: a high immigration; two high activations; one high activation and a low race; or at least q-1 low races. Its minimum degree is m.

Until that degree is reached, only finitely many counter states and exponents are used. The power-spending kernels, the graded dormant Green, and the processor of Sections 2–3 transport the ACTUAL remaining inverse powers through every seed phase and dormant return. Once degree m is reached, designate and use the actual repair bound. It follows that the complete cycle from a dormant section input has

`E[(w_next-w)_+] <= C w f_m(A_in)`.                       (S0)

This is a complete-cycle source, not just the earlier seed-interrupted source. An off-section seed is followed with its B and degree counters intact; it is never assigned a fresh bounded phase. Histories after reaching the degree threshold are paid by the proven repair, not discarded.

From a positive-D section input, split at first dormant entrance or first connector. Direct dormant entry carries its own f_m reward. A first clearing has f_m output moment <=CT; an immigration has mass iT; an activation's f_m output is <=C T by its compensator. The same graded continuation gives the refined bad-interface bound

`P[ w_next f_m(A_next)] <= C w[T+V_m]`                    (M+)

when the terminal is a low-A or dormant interface; unrestricted high-A section returns are not asserted to satisfy this formula. Here V_m is the initial positive-D dormant-entry reward. In particular the right side is O(w/r) absolutely, and at good incoming A it is at most `C w[T+(1+A)^-2 U]`.

For dormant section inputs the corresponding profile interface is bounded by C w f_m(A_in), with no vanishing-in-r claim. This distinction is the whole reason for the two-block correction.

## 5. The negative activation credit is supplied physically

From the section, first-connector activation moves B=q to 2q-1 without changing r. Its next ordinary clearing decreases r by exactly h. A first clearing from B=q is neutral. The useful activation probability is the ACTUAL compensator kT q U.

For positive-D activation output, the next complete local connector event is clearing with probability 1-o_r(1), and its inactive-output chance tends to zero. Later dormant occupation from an initially good positive-D state is at most C/(1+A_in) of the original occupation; activations made in that later dormant part may be charged as an error of that relative order. For an initially dormant GOOD state, an activation occurring before its first seed has A_out>=A_in+m-1. A seed/clearing pair then precedes another connector birth with probability 1-O(A_in^(1-m)); a seed is followed by a positive-D clearing with probability 1-o_r(1). Direct clearing retains large A. Thus the same physical downward event is earned on good inputs, not assumed for all low-A dormant inputs.

After that downward clearing, undoing its credit requires an immigration race or a designated branch. For positive-D clearing outputs, the f_m moment O(1/r) makes a low race O(r^-1/m) by Holder; the graded/repair bounds pay all later exceptional branches. For a direct dormant clearing from large A, the low-race probability is O(1/A_in), with the dormant graded Green paying later histories. Hence a fixed fraction of the downward factor exp(-theta h)<1 survives for all sufficiently large r and good A.

Consequently on GOOD inputs A>K(r),

`P w-w <= -c_theta U w + C_theta T w + o_K(1) U w`.       (G)

Together with T/U<=C/(1+A_in), this gives a strict negative margin. On BAD positive-D inputs, the possibly inconvenient dormant-activation contribution has absolute size O(1/r); the remaining activation branch still has nonpositive net contribution after its downward credit is paid. Thus

`P w-w <= C w/r` on bad positive-D inputs.                (S+)

On bad dormant inputs use (S0), not a false uniform fast-clearing estimate.

## 6. Actual two-block bad-return correction

Choose K(r)=r^gamma with 0<gamma<1/m. Split bad section states into B0={D=0,A<=K} and B+={D>0,A<=K}. Let weights be

`g0=w f_m(A)` on B0, `g+=w/r` on B+.

The purely dormant B0-return kernel R00 is killed on seed, leaving B0, or residual-threshold entry. Its actual Green is bounded in g0 by DORMANT_GREEN_NONBALANCED_V2.md. This kernel is NOT assumed to have small row mass.

The remaining block bounds follow from the actual processor above:

- Seed-mediated B0->B0 return has g0 norm o(1): it requires a positive-D dormant entrance before completing the cycle, whose profile norm is O(r^-1/16); the graded Green pays its actual seed phase.
- B0->B+ maps g+ into at most `C K^m/r` times g0, since `1_{A<=K}<=C K^m f_m(A)` and the full incoming profile is retained.
- B+->B0 maps g0 into at most C g+, by (M+) and T+V_m=O(1/r).
- B+->B+ maps g+ into at most `C K^m/r` times g+, by the same output moment.

Precondition the first row by the EARNED Green (I-R00)^-1. The resulting positive two-by-two majorant has diagonal entries o(1), O(K^m/r), and off-diagonal product O(K^m/r). Raise r0 so its spectral radius is below one. Truncated positive iteration therefore constructs the actual bad-return correction H with sources D0 g0,D+ g+, for fixed sufficiently large D0,D+, and bounds

`0<=H<=C g0 on B0`, `0<=H<=C g+ on B+`, `H=0 on good`.

Its actual kernel identity on the bad set is PH-H= -D_i g_i. This cancels (S0),(S+) with a strict negative margin. No stationary bad-phase law or supplied barrier is inserted.

On a good positive-D input, (M+) bounds leakage into H by

`C[1+K^m/r][T+(1+A_in)^-2 U]w=o(Uw)`.

On a good dormant input, the leakage is at most `C[1+K^m/r] f_m(A_in)w`; its initial first holding time gives `U>=c A_in^(1-m)` at B=q, so this too is o(Uw). Thus (G) survives the actual correction.

## 7. N-directed stopped cost, with its phase-dependent exterior leakage retained

Repeat the complete construction for `(1+r)^j exp(theta r)`. At the section N=r+H(q), so A<=Cr. The bad dormant margin f_m is at least c r^-m; the bad seeded margin is r^-1; the good occupation has lower bound c r^(-(m-1)) from the local lower-U formula (and the direct dormant first holding time). With j=m, the corrected section drift pays a constant multiple of exp(theta r) per cycle. Section cycle running cost is <=C exp(theta r). Telescoping actual stopped cycles earns finite

`W_r=E integral_0^tau_{r<=r0} exp(theta r_t)dt`.

For arbitrary initial B, the proven initial repair gives only

`W_r <= C exp(lambda B)(1+r)^m exp(theta r)`,

not a B-uniform bound. Inside its domain LW_r=-exp(theta r). Outside, only immigration can enter it, so its positive leakage on the r-threshold cylinder is at most C exp(lambda B). This exponential phase leakage must be paid by the complementary residual; calling it bounded would be false.

## 8. The complementary infinite strip is handled, not capped

Let I be the indicator of an enabled fast source and Z=B-N-hI. Fast reactions preserve I=1. Immigration changes Z by zero or -h, inactive activation is neutral, active activation raises Z by h, and clearing is neutral or lowers Z by h according as it destroys or preserves activity.

For large hidden N, construct actual bounded-event trials:
- Active positive-D input: prescribe clearing with an active output. Its probability is bounded below for large N; competing active activation is O(B^(1-q)).
- Active dormant input: prescribe a seed before clearing, with fixed probability s/(d+s), then positive-D clearing with active output. Competing births are O(B^(1-q)); this yields a down-Z event with fixed positive probability.
- Inactive A>=1 input: prescribe activation before immigration, which makes A>=m and enables the fast graph, then use the preceding trial.
- A=0 input: take its compulsory immigration with constant mean waiting time, then the preceding trial.

Each large-N trial has bounded mean duration and a fixed positive down probability. Only active activation can move Z up; its probability per trial is O(B^(1-q)). The newly dormant inactive face C large,A<m is included explicitly.

For bounded N use the finite graph-path absorption bound, not an infinite-head assumption. Neutral inactive activation followed by clearing lowers N by one. After boundedly many such pairs, A=0 is reached or Z exits downward. At A=0, at most m immigrations enable mA; the at most m-1 noncompulsory races each have probability at least c/Z because N remains bounded. This gives a trial with down probability >=c Z^(-(m-1)), up probability <=C Z^(-(q-1)), and bounded mean time.

Conditional renewal across both regimes yields actual first Z-exit up probability <=C Z^-h and mean time <=C Z^(m-1). Therefore the true stopped value W_Z with running cost exp(theta_Z Z) is finite, polynomial-exponential in Z alone, and LW_Z=-exp(theta_Z Z) above its threshold. Its exterior positive leakage is at most C AB on the complementary threshold cylinder.

## 9. Global comparison and current review boundary

Write alpha=(m-1)/(q-1)<1. We have r=N-alpha B+O(1), Z=B-N+O(1), hence max(r,Z)>=c(N+B)-C. On the r-threshold cylinder, Z=(1-alpha)B+O(1), so choose theta_Z with theta_Z(1-alpha)>lambda to dominate W_r's ACTUAL exp(lambda B) leakage. On the Z-threshold cylinder, r grows linearly with N+B, so exp(theta r) dominates the polynomial AB leakage of W_Z. The sum of the two stopped values is normlike; first-holding lower bounds have only polynomial-rate denominators.

Nonexplosion is independent: fast reactions conserve N,B, and the high-degree clearing absorbs connector AB growth where A>=m,B>=q; on remaining strips AB is at most linear in N+B. Thus a linear Foster bound prevents explosion. The stopped global drift comparison, repeated at sufficiently large residual exponents, would give classwise positive recurrence and every requested exponential total-count occupation/invariant moment.

This is a complete CANDIDATE route, not an accepted theorem. The most important whole-proof checks are Sections 2–6: the actual graded processor, complete dormant source, negative activation credit, and four block bounds must be assessed together. The two local results and the dormant Green/source receipts do not automatically approve this synthesis. A defect in any of those interfaces leaves global recurrence open.
