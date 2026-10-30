# V2 repair: designate every inactive high-phase entrance
Status: explicit repair prompted by independent reviewer. The five-file V1 frozen bundle remains byte-identical. V1's stopping list is incomplete without this addendum.

Reviewer identified the actual branch: for a0>=2, activation-first from B=2q-1 may clear to B=q-1,A=0; the next low-phase immigration wraps to B=q,A=1<a0. This is NOT the active section S={B=q,A>=a0}. Fast chemistry is disabled, so its subsequent high-B activation is not a rare fast competitor. V1's explicit designation of inactive high-B CLEARING outputs did not cover this low-wrap entrance. Its generic physical-seeding continuation alone did not fix the missing stopping rule.

## Corrected stopping rule
In every full-cycle processor and profile enumeration, stop and designate as bad EVERY entrance into an inactive state with B>=q, whatever transition produced it. This includes:
- a clearing output with A_after<a0;
- a low-phase immigration wrap B=q-1->q with A_after<a0;
- an initially inactive high-phase input, which is seeded before entering the active processor and is not called a rare activation event.

A low activation produces at least m A and cannot cause this issue. A fast reaction preserves active A>=a0. Immigration from an already active high state cannot destroy activity. Thus the listed new wrap is the missing internal branch; no other active-to-inactive event type is being omitted.

## Profile cost of the new wrap
At an inactive wrap, A_pre<=a0-2. Therefore

    1_{inactive wrap} <=(a0-1)^m (1+A_pre)^-m.

The actual wrap probability is at most this indicator. Its subkernel is consequently bounded in the same incoming inverse-m profile as a designated fast immigration or an inactive clearing output. The full-cycle moment transport and stage enumeration before this new stop remain valid; they terminate EARLIER and never count the following inactive high activation as rare. Integrating against the first clearing law yields O(t) mass, not an unearned small pointwise race probability.

## Actual continuation and weighted return
From the designated state A<a0, B>=q, at most a0 actual immigrations or an earlier activation seed the fast graph. Waiting times are paid using the positive immigration-rate floor; activation increases A by m-1 and is helpful. The maximum upward r displacement is at most a0 h, so every fixed exponential weight incurs only a fixed multiplier. V1 §3's actual seed repair applies unchanged after the new designation.

Hence the escape/bad bound (E), whole-cycle bad-entry bound (Bentry), and bad-return Neumann correction retain their stated orders and constants after enlarging constants. The new branch may have A-dependent probability1 on a particular observed low state; it is controlled only through the ACTUAL incoming profile law. It is never treated as a rare high activation conditional on that state.

## Exact scope of V2
V2 consists of the five immutable files in producer-workspace/chemical_boundary_profile_candidate_20261030 plus this addendum. Independent review must explicitly assess this closure. Earlier pure-source and A=1 siphon whole-proof receipts are unchanged. This correction is not a general-WR recurrence result or a novelty claim.
