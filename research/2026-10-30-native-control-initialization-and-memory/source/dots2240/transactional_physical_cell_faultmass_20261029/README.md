# Delayed transactional emissions: physical-window CP faultmass

- `ANCESTOR_WITNESS_THEOREM.md`: binary local-stochastic marked-emission cells via actual last-kick ancestors, time-dependent local Lyapunov products, Poisson factorial expansion, and summable witness kernels.
- `MULTIPLICITY_AND_INITIAL_MARKS.md`: stronger factorial/exponential moments, arbitrary per-cell count thresholds, direct physical-kick mass, and initial-mark/burn-in terms. Includes an explicit repeated-owner/repeated-cell integrand check.
- `check_ancestor_counts.py` / `.json`: 36 tilted classical CTMC mgf checks, 1,000 generated records, 51,340 same-owner interval checks including 3,381 repeated-owner/same-cell checks. These are regressions, not a substitute for the quantum operator proof.

Core envelope: for initially zero marks, actual physical Poisson kick rate scale epsilon, and bounded geometry, the total marked-reset emission count Y_V in any finite set of fixed-width physical cells satisfies

E exp(theta Y_V) <= exp[epsilon H |V| (exp(B theta)-1)],

with fixed H=C_A/P and B=bP. Adding direct kick mass preserves this form with a finite Holder power loss. Prescribed cell multiplicities totaling m therefore have CP event-instrument norm at most [e(epsilon H)^(1/B)]^m. Delays can depend on all intervening kicks; no independent delay assumption appears.

Prerequisite: the actual finite-support reset-tail witnesses in `producer-workspace/JOINT_LOCAL_LYAPUNOV_TAIL.md`. Designated terminal/abort channels must remain real, separately recorded channels under the added kick generator.

Scope: physical record faultmass only. No DATA-instrument serialization, fault-tolerant circuit reduction, update-index threshold, or logical memory theorem is claimed. Late blocks retain past-kick ancestry; arbitrary conditional restart states need the initial-mark term.
