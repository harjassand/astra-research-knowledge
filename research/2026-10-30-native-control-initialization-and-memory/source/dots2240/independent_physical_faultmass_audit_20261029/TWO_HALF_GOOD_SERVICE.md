# Two-half certificate for actual good recovery opportunities
2026-10-29. Lead certificate; no counting ancilla, no normalized clock-path selection.

## Inputs already established
1. Transactional complete terminal/abort reset sends h to good Q_0 for any physical input. Clean evolution preserves that good history sector. A good abort has zero support. Returning from Q_0 to a terminal requires a fresh complete commit A_k→C_0.
2. On a good terminal source the exact forest-gauge instrument is the intended recovery Phi_h (or intended syndrome subinstrument), tensor the controller source/reset CP factor.
3. For buffered separated owner sets U, the actual no-terminal-or-abort-reset instrument has the uniform full-state bound

   ||N_U(t)||diamond ≤ C_0^|U| exp(−r_eff |U| t).

For the clean process r_eff=r>0. For actual independent local CPTP Poisson kicks with sufficiently small incident norm budget, the existing Lyapunov robustness result gives r_eff=r−eta alpha^(−b)>0 with C_0=alpha^(-1). Designated reset channels must remain actual separately recorded channels. No theorem is asserted for a signed perturbation that removes this interface.

## 1. Fewer than two actual resets: two-half union
Fix a deterministic window of length Delta=2tau. If an owner has fewer than two designated resets in the window, it has zero designated resets in at least one of its two halves.

For m buffered separated owners U, assign to each owner one half in which it is required to have no reset. There are 2^m assignments. An assignment partitions U into U_1,U_2. Chronological composition of the actual killed instruments, using their full-state operator bounds, gives

   ||instrument(no U_1 reset in half1 AND no U_2 reset in half2)||diamond
      ≤ C_0^(|U_1|+|U_2|) exp[−r_eff tau (|U_1|+|U_2|)].

The selected instrument maps are CP, so the norm of their event union is at most the sum. Hence

   ||instrument(every h∈U has fewer than two resets)||diamond
      ≤ [2 C_0 exp(−r_eff tau)]^m.

No independence between owners or halves is assumed. No physical latch is needed. Empty U_i causes no difficulty: its full instrument has norm one.

## 2. Spatial packing and many deterministic windows
Let P be a fixed packing number for the existing no-reset Lyapunov witness radius and one interaction-range buffer. Every specified owner set S contains buffered U with |U|≥|S|/P. Put

   q_short=min{1,[2 C_0 exp(−r_eff tau)]^(1/P)}.

Then every finite specified owner set obeys the joint reset-shortfall bound q_short^|S|. Fix ONCE a deterministic grid of nonoverlapping windows [n Delta,(n+1)Delta). Candidates are DISTINCT cells (h,n), with no duplicate tests. For any finite set of these owner/window candidates, apply spatial packing in each window and compose window instruments chronologically. The same parameter holds for the full specified set, uniformly over arbitrary initial physical/reference states.

This is a physical-window statement, not a statement indexed by successful updates or by random waiting intervals. Arbitrary overlapping or repeatedly shifted windows are excluded: nearly duplicate tests would invalidate the exponent. Different windows for the same owner are disjoint; chronological CP composition, not independence, handles their joint shortfall probability.

## 3. Why two resets witness a fresh good DATA operation
If no owner-affecting kick occurs between the first and second resets, the first reset establishes h's good Q_0 state. The second cannot be an abort, and it must have followed a new complete commit. Its DATA instrument is exactly the intended Phi_h.

For conservative record bookkeeping, call a candidate **control-spoiled** if ANY kick in its entire window has system support intersecting support(B_h). This stronger event safely includes every kick that could invalidate the post-regeneration certificate. Kicks outside this support cannot destroy h's good sector. Thus, pathwise in the actual classical kick/reset record,

   {no witnessed good fresh terminal for candidate}
      subset {fewer than two designated resets} UNION {control-spoiled}.

The phrase 'pathwise' refers only to the real jump record and the support/sector invariant, not to resolving coherent Hamiltonian clock excursions. The DATA statement remains the full unnormalized instrument identity on the good terminal source.

A control-spoiling kick need not change a syndrome, logical state or DATA at all. It is charged as a lost availability opportunity. Do NOT hide it inside a claimed syndrome-error increment.

## 4. Explicit Poisson control-spoil law
Assume the declared model of independent local CPTP Poisson kick processes, with fixed state-independent rates. Let Lambda bound the summed rate of kick channels affecting one h history neighborhood. Let P_N be a fixed coloring/packing number such that within a selected color no one kick channel can affect two candidate owners in the same window. This coloring is formed from the ACTUAL physical kick hypergraph: two owner candidates conflict whenever one allowed kick support intersects both history-projector neighborhoods. Coloring only the clean generator graph is not sufficient when physical kicks have a larger range. P_N is finite by the declared bounded noise support and bounded incident kick rate/geometry. Poisson increments in different deterministic windows are independent.

For any finite specified candidate set S, select at least |S|/P_N candidates with disjoint kick-process/time-increment sets. Their spoil events are independent and each has probability ≤1−exp(−Lambda Delta). Therefore

   Pr(all candidates in S are control-spoiled)≤q_spoil^|S|,
   q_spoil=[1−exp(−Lambda Delta)]^(1/P_N)
           ≤ min{1,(Lambda Delta)^(1/P_N)}.

This probability is independent of initial quantum state because the Poisson kick occurrence law is state-independent. The CPTP kick effects may be arbitrary, correlated with retained bath/reference, and need not commute. Only their occurrence processes enter this estimate.

## 5. Joint genuine missed-service law without assuming independence
Reset-shortfall and control-spoil events are generally correlated. For a fixed partition S=A disjoint-union B, the probability of shortfall on A and spoil on B is bounded, for every initial quantum state, by

   min(q_short^|A|,q_spoil^|B|)
      ≤ q_short^(|A|/2) q_spoil^(|B|/2).

Sum over the 2^|S| partitions using the event inclusion above. The actual CP instrument for every specified candidate missing witnessed good service has norm at most

   q_good^|S|,
   q_good=min{1,sqrt(q_short)+sqrt(q_spoil)}.

The same argument applies to retained output states because a CP trace-nonincreasing instrument's diamond norm is the supremum of its event probability, including reference extensions. It does not identify a conditioned event with a normalized fresh-data channel.

More generally, Holder weighting yields q_short^theta+q_spoil^(1−theta) for 0<theta<1; theta=1/2 is a simple sufficient choice.

## 6. Parameter meaning and limitations
Choose tau sufficiently large (a fixed constant independent of volume) to make q_short as small as desired. Then choose the physical kick rate sufficiently small to preserve r_eff>0 and make q_spoil small. Both conditions can hold simultaneously. Alternatively a slowly increasing physical window as noise tends to zero can make both terms vanish, but no particular scaling is needed for this existence statement.

This supplies a genuine all-finite-specified-sets **missed-good-recovery** parameter in deterministic physical windows. It includes actual fresh commitment and intended DATA-channel semantics, rather than counting an abort as recovery. Marked DATA damage from earlier kicks remains a separate charge; regeneration does not make that damage disappear.

The proof still does not establish that an SSF update is always beneficial, that an arbitrary asynchronous sequence implements a particular decoder, or that bounded fault clusters are corrected. Those are the remaining code/decoder correctness obligations. The constants inherited from finite-rate monitors and local Lyapunov witnesses may be extremely pessimistic.

## 7. Positive moment interface for the finite-window witness
For a fixed finite set H of candidate cells, let M_H be its number of conservative record-defined good-service misses. Let E_A be the effect operator of the joint miss event on A⊆H. The proved uniform CP instrument bound is exactly

   0≤E_A≤q_good^|A| I.

For t≥1, expand t^(M_H)=product_(j∈H)[1+(t−1)1_(miss_j)]. Positive coefficients give the operator-valued moment bound

   integral t^(M_H(record)) I(drecord)^*(I)
      =sum_(A⊆H)(t−1)^|A| E_A
      ≤[1+q_good(t−1)]^|H| I.

It holds against arbitrary positive subnormalized initial states without renormalization. Thus the usual independent-no-ring moment in a fixed-set SSF witness can be replaced by this genuine actual-good-service moment; independence of the missed indicators is unnecessary.

If this moment is multiplied by a primitive Poisson fault-count moment from the same window, do not factor their expectations. For example, if N is a dominating Poisson count of mean mu and t,u≥1, ordinary Cauchy–Schwarz on the actual joint record measure gives uniformly

   E[t^M_H u^N]
      ≤ [1+q_good(t²−1)]^(|H|/2)
         exp[(mu/2)(u²−1)].

For a positive subnormalized input the same scalar factor multiplies its trace. This pays explicitly for correlation between control misses and noise records. It is only a moment interface; it does not replace the separate localization of delayed malformed DATA emissions or the deterministic SSF witness proof.
