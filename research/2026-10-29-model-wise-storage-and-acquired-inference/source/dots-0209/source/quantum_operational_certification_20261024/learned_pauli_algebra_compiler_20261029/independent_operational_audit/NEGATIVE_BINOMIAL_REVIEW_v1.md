# Independent review: negative-binomial tail of the keyed adaptive fault comb
2026-10-29. **Accepted at the previously reviewed private-pad comb scope.** This receipt does not automatically extend to an unkeyed resource's full density operator.

The exact private-pad instrument permits a generative order that first draws a memory Kraus/physical-label branch, then uses the private role coin. The opportunity predicate v outside the actual learned span is therefore determined before that coin. This statement needs equality of the full memory instruments, not merely equality of marginal probabilities in an unrelated process.

A rigorous coupling avoids any ambiguity about whether opportunities eventually cease. Prepare two independent infinite Bernoulli(p) streams U,V, where p=1-q. At each actual call, first determine whether it is an opportunity. If yes, consume the next unused U coin; otherwise consume the next unused V coin. The next coin used is independent of the full past and current opportunity predicate, so this has exactly the original iid role law. Stopping or deciding to wait arbitrarily long for another opportunity does not change that fact.

Every U-success on a consumed opportunity adds one independent actual probe label. At most m*=dim(S*) such successes can occur; once m* successes have occurred, the learned span equals S* and no further real opportunity is possible. Every actual service fault is a U-failure, though not every U-failure must be a logical fault. Hence on this coupling the number of real faults is no larger than the number of failures before the m*th success in the complete U stream. If the real process stops early or opportunities cease, the already defined unused U coins complete the comparison without requiring a stopping-time test for 'no future opportunities'. The same domination holds with m>=m*, including m=2g. The zero-rank case has no faults.

For F distributed as failures before m successes,

    Pr(F>t)=Pr(Binomial(m+t,p)<=m-1),  t>=0.

The indexing is correct: the mth success occurs after trial m+t exactly when more than t failures precede it. For mu=p(m+t)>=2m, the event is contained in X<=mu/2, so the usual exponential-moment lower-tail bound gives exp(-mu/8). Requiring also mu>=8 ln(1/epsilon) gives the claimed conservative error bound. Thus correction budget O((m+log(1/epsilon))/p), rather than O(m/(p epsilon)), is sufficient.

For a true outer decoder correcting all <=t faulty whole blocks, the received input-independent Pauli-comb factorization turns this tail directly into reduced half-diamond error; no independence between source errors is used. Grouping consecutive service slots into a larger symbol cannot increase their count of bad groups above the number of bad slots. Finite source/probe caps truncate real opportunities; their explicit fallback failure charges remain additional.

`check_negative_binomial_v1.py` confirms the NB/binomial identity in441 exact rational cases and the domination in27 exact finite stopped-policy tail checks with opportunity schedules depending on prior roles. These checks are not the general proof. The two-stream coupling is the proof.

Current-role leakage, later key disclosure during continuing source interaction, or inserting fictitious labels into an unproved coherent channel would invalidate the prerequisite. Known physical frame, common joint algebra, trusted acquisition and outer implementation remain required. No new coding theorem, hardware result or historical novelty is asserted.
