# Explicit rare-arming premise for the partial thermal carrier

30 October 2026. This corrects Section 5 of the preserved root input
`UNTUNED_PARTIAL_THERMAL_CARRIER.md`, SHA256
`b37e49509e6fc5e3eb0436f330c24159770be73ebb405f6705670d790ee3eb00`.

Its asserted small arming probability imports the full rare-arming premises
of `RARE_LAW_TYPICAL_LAW_AND_FORCE_LIMITS.md`: **phi(t,0)=0 for every t**, an
unforced native aggregate martingale, actual zero-force operation before the
trigger, and a whole-horizon observation/evaluation error o(N^(3/2)log N)
with the stated superexponential failure probability. These hypotheses must
be stated explicitly rather than inferred from the word "unforced."

Under them the zero-force auxiliary current is a Gaussian martingale plus
the bounded endpoint, and |Z_N|<=C|B|. The same maximal inequality gives
p_arm<=C exp(-c log^2 N). The actual-work estimate (14) then has the claimed
vanishing consequence. Its displayed bound in terms of a supplied p_arm is
valid independently of how that probability was obtained.

Without phi(t,0)=0, take phi(t,h)=v t with nonzero v. Even unforced native
currents are then assigned a target of order N^2, so the apparatus arms with
probability tending to one and must perform sustained transport. Neither
rare arming nor vanishing force work follows. This is a useful separation
between a fluctuation-protection program and a deliberately driven program.

The full nonlinear tracking theorem, positive mobility, exact noise relation,
finite-response supplier and whole-path law map do not require phi(t,0)=0;
they are unchanged. Only the rare-arming/low-mean-work specialization needs
this additional premise.
