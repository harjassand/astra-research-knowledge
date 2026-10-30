# Explicit first-activation positive source and the O(T) bad drift

30 October 2026. Separate completion for the frozen full closure candidate. Initial-phase-left flag and active-section convention from PROCESSOR_SECTION_CONVENTION.md apply to EVERY kernel below. No frozen source is edited.

## 1. One-power continuation from B=2q-1

Let R_b be the actual seeded/dormant repair to the active section (or residual threshold), retaining the true initial phase b. For b=2q-1, define its positive residual reward

`E[(w(r_return)-w(r_input))_+]`.

The bound needed is

`E[(w_return-w_input)_+] <= C_theta w_input f_1(A_input)`.  (A1)

This holds for either D=0 or D>0, with inactive seeding handled as in the processor.

To prove it, stop the actual graded processor when it first acquires positive rare degree, rather than waiting for degree m. A noncompulsory low immigration spends one power, high activation spends m-1>=1, and high immigration spends m>=1. The degree-zero continuation consists only of ordinary clearings, low activations, compulsory B=0 immigrations, and fast seed/dormant transitions. Every one of these preserves or decreases r. Thus a positive terminal residual is impossible before that first positive-degree event.

The same fixed-counter processor proof applies with counter levels 0 and 1. At level 0, ordinary phase kernels contract in exp(lambda B); positive-D dormant returns are small and their TRUE dormant Green is used. For a dormant starting state, the marked Green at degree one supplies the incoming f_1 factor. This off-section use has bounded initial b=2q-1: its high-A block/half-A proof is unchanged, and bounded A uses the actual finite-head Green. It is not obtained by resetting b to q.

At the first positive-degree event, the actual kernel spends at least one inverse power. Append the already earned ungraded repair, whose cost is bounded in the SAME exp(lambda B) norm. Positive iteration therefore bounds its terminal w reward by C exp(lambda b) w_input f_1(A_input). Since b=2q-1 is fixed, this is (A1). The claim does not multiply a rare-event probability by an unrelated output moment. Paths with no positive-degree event contribute zero to the positive part, even if their seed phases or numbers of ordinary events are unbounded.

The same argument with counter m, from b=0 after a section clearing, gives

`E[(w_return-w_input)_+] <= C_theta w_input f_m(A_input)`.  (C_m)

Here degree-zero phase history starts with its compulsory neutral immigration. The exact phase budget requires at least q-1>=m low races unless a high immigration or the high-activation alternatives occur. True seed phases and counters remain retained. This is the full continuation, not only a seed-interrupted path.

## 2. First-connector decomposition

Start from any active section state B=q. Until the first actual connector event, r and B are constant, although fast dormant/seeded transitions may repeat. Let T be its ACTUAL full physical mean time. The three first-connector branches are disjoint.

- Immigration has probability i T. Its output B=q+1 is a fixed phase and has bounded r displacement. The actual repair norm therefore gives positive reward at most C w T.
- Clearing from B=q is r-neutral and leaves B=0. Its output A=A_pre-m has reward (C_m). Its compensator gives

  `E[f_m(A_out); first connector is clearing]`
  `= d(q)_q E integral_0^tau (A)_m f_m(A-m)dt <= C T`,

  because the falling-factorial/profile product is uniformly bounded on A>=m.
- Activation is r-neutral and leaves B=2q-1. Its output is A_out=A_pre+m-1. Apply (A1). The ACTUAL activation compensator gives

  `E[f_1(A_out); first connector is activation]`
  `= t q E integral_0^tau A/(A+m)dt <= t q T`.

Therefore, without relying on a favorable sign for the activation branch,

`E[(w_next-w)_+] <= C_theta w T`.                       (PT)

In particular `P w-w<=Cw/r` on every positive-D section input, by the earned T<=C/r bound at B=q. For a dormant section input, T<=C f_m(A_in), giving the correct dormant source. This explicitly supplies (S+) and (S0) without replacing T by U times an unspecified o(1) error.

## 3. Relation to the negative margin

The good-input negative activation event in Section 5 of the full candidate is still needed to obtain strict negative drift there. Statement (PT) only bounds its positive part and does not manufacture a negative margin. However, the bad-region O(T) source no longer depends on that separate negative-credit argument. The full candidate's sentence that the remaining activation branch is nonpositive may be replaced, for its BAD-region estimate only, by the exact graded bound and compensator calculation above.

This completion is a synthesis-level proof obligation pending whole review; it does not extend the already accepted local receipts by itself.
