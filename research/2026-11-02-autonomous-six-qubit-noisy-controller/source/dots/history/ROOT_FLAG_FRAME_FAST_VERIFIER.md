# Flag-frame actuation and fast physical verification

Root proposed mechanism, 2026-11-01. Pending independent construction/audit. This changes the implementation problem: Tanner corrections only flip witness bits, so their physical action can be stored in an XOR frame rather than sequenced as a large quantum gate. Actual quantum-check sensing remains an explicit primitive, equally available to the active comparator.

## 1. Physical flags replace collective witness flips

For each fixed candidate witness-flip mask x_j, add a physical bit b_j. Define the virtual witness

 y=a XOR sum_j b_j x_j.

Flipping ONE b_j applies x_j to the virtual witness. The frame map is a product of commuting CNOTs from b_j to the corresponding witness bits. All masks, incidences, gate supports and hardware counts are fixed with the code degree, but may be enormous. Every flag is noisy; no perfect classical record is assumed.

Let W0(s,y) be the previously constructed Tanner witness potential. The enlarged protected subsystem is related by this explicit local Clifford frame to the previous system plus gauge flags. Its distance/locality constants change with the actual frame light cone and must be recomputed. The flag hardware overhead must be included in n-based noise and resource counts.

## 2. Predicate circuits are actual noisy state

Let f_j(s,y) indicate the deterministically selected permitted update. When f_j=1, W0 decreases by at least1 under b_j flip. Selection may be one-hot per original location to preserve the intended total rate. Wrong outputs may be many; their additional hardware/rates cannot be ignored.

Compute these Boolean functions using finite fan-in DAGs of PHYSICAL bit registers. Include XOR construction of y, the selector, and any copies needed to bound fanout. Let e_i be the output-consistency violation of gate i. Choose positive topological weights w_i such that

 w_i >=1+sum_(children of i) w_child.

With E=sum_i w_i e_i, overwriting a wrong gate output with its Boolean value lowers E by at least1, even if it invalidates downstream gates. Thus asynchronous repair at rate gamma per gate gives

 L_repair E <=-gamma E/w_max.

The actual repair jumps touch at most two input bits and one output bit. No global clock or validity/rearm latch is supplied. The circuit may be exponentially large in the fixed Tanner degree; that cost remains explicit.

Quantum syndrome bits are NOT trusted inputs. A sensor bit for a commuting physical check S needs its own constraint (1-S Z_sensor)/2 and actual QND copy/measurement dynamics. This operation has the physical arity of S and is not magically realized by a classical Boolean circuit. Quantum-check sensing can be separated from fast classical processing because witness/flag updates do not change the physical data checks.

## 3. Pay rearm debt in the GENERATOR, not in each transaction

Actuate a flag at rate kappa when its physical permission output c_j is1. This is a two-bit jump. Let B bound the possible change of E under one flag flip, D bound |Delta W0|, and A bound the number of wrong or missing permission outputs chargeable to one circuit violation. These constants must come from the actual finite DAG and its fanout/weights.

Use Q=W0+epsilon E with SMALL epsilon, epsilon B<=1/2. A correct permitted actuation drops Q by at least1/2, including the new consistency debt caused by its changed virtual inputs. A wrong actuation may raise Q by at most D+1/2, but its output cannot disagree with the true predicate unless some circuit constraint is violated.

If the true update count is at least cW0, then

 N_correct_actual >=cW0-AE,
 N_wrong_actual <=AE.

Therefore the slow actuation drift is at most

 -(kappa c/2) W0 + kappa A(D+1)E.

Combining fast repair,

 L*Q <=-(kappa c/2)W0
 -[gamma epsilon/w_max-kappa A(D+1)]E.

Choosing gamma epsilon/w_max sufficiently large gives extensive mean restoring drift. This proposal deliberately does NOT require every wrong actuation to be individually downhill. It therefore avoids the contradictory requirements epsilon<1 for a correct commit and epsilon>1 for a mistaken commit in the simple static-penalty example.

All operators are diagonal functions of commuting physical checks and classical-register Z labels for this drift calculation. Pointwise inequalities, if valid, extend to arbitrary coherent register states. The established local exponential-functional-calculus technique could then lift mean drift to an exponential certificate, but that is a further proof obligation, not automatic acceptance.

## 4. Refinements that must be paid

- Physical syndrome sensors have slower/noisier quantum dynamics than ordinary Boolean gates. Give their constraints separate weights/rates. Correct flag updates do NOT change physical S, so they do not create new sensor inconsistency. Do not accelerate quantum measurement for free to obtain fast classical verification.
- Noise proportional to gamma must be charged. Choosing epsilon proportional to kappa/gamma can keep the weighted classical-noise injection finite, but the full operator admission and physical error model must be derived.
- Computational wire constraints are nonlinear and their ground subspace is not automatically a Pauli stabilizer code. A safer logical argument projects low Q to the previously earned low-W0 component; all new wire operations act only on gauge records, and each flag flip corresponds to a bounded old witness mask. Prove protected flatness with those actual maps, rather than assuming a new stabilizer distance.
- Wrong actuations can be uphill. Reflection at the low-Q boundary must be rechecked. For conditional-Pauli classical jumps, censoring an outgoing upward-Q edge removes a positive exponential drift term and can only help; the channel-comparison bound must now count boundary contributions of ideal actuators as well as external noise.
- If only arbitrary full-patch true-syndrome inputs make the scheme work, the original physical sensing obstacle remains. The honest achieved resource contract would be standard QND-check sensors plus few-bit autonomous classical gates, not a complete native two-body quantum device.

## 5. Mission gate

This is a possible qualitative escape from locks, global sequencing and giant phase qudits, exploiting the special commuting witness-frame action. It is not yet a proven implementation. The strongest active Tanner decoder receives identical parity sensors, Boolean gates, flags, rates, noise, reset and wiring resources. A win must concern the acquired autonomy/robustness or a real resource advantage, not merely hiding the selector in more registers.
