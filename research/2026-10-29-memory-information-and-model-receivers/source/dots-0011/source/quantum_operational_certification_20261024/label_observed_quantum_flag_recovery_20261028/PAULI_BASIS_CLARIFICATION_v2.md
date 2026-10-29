# Full-basis clarification for the X-only specialization

28 October2026. This clarifies §2 of GOVERNING_LABEL_OBSERVED_FLAG_RECOVERY_v1.md without changing its source or records.

The Kraus expansion and the identity sum_x M_x=I_G always use the COMPLETE4^n Pauli basis. For an X-only source, extend p_x by zero to every other Pauli label. Its flag state/feature outside the allowed alphabet can be assigned arbitrarily because its coefficient is zero. Effects assigned to a zero-probability Pauli label contribute nothing. Reassign all such effects to any one allowed correction; positivity of that allowed state's coefficient ensures that the objective does not decrease. Consequently the optimum is attained using only allowed X labels, and the K-feature reduction applies on that allowed alphabet. The training concentration union then needs only2^n labels, because zero probability outside the supplied subgroup is an exact source promise.

It would be incorrect to expand an arbitrary full CPTP decoder Kraus operator using only the X subgroup. No such restricted expansion is used in the corrected proof. This correction was identified during independent review; the full-CPTP conclusion and numerical pilot remain unchanged.
