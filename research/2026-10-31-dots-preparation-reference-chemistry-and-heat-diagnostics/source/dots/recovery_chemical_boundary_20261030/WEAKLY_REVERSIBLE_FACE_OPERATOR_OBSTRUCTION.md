# Weakly reversible variant: a non-small face transition

30 October 2026. Exact diagnostic, not a new recurrence result. It supplements NON_A_BIRTH_FAILURE_CERTIFICATE, whose simplest birth addition was not itself weakly reversible.

Keep the irreducible conversion cycle C+D->E+D->a+D->C+D and the original bidirectional seed/clear core. Add the reversible pair

    C+D -> C+E   at rate beta C D,
    C+E -> C+D   at rate gamma C E,

under the same common physical factor. The added complex C+E is linked reversibly to the old C+D complex, so weak reversibility is preserved.

At residual input a=E=0, C=n, D=1, the only enabled fast reactions are C+D->E+D at rate lambda n and C+D->C+E at rate beta n. The common physical factor cancels in their race. Thus the probability the FIRST fast jump is the new birth is exactly

    beta/(beta+lambda)>0.

That jump produces a=0,E=1,C=n,D=0, leaving physical A unchanged. Adding the fixed connector races changes this probability by only O(1/n). Therefore the positive-D-to-D=0 outgoing f_s kernel has a nonvanishing incoming-profile norm. The scalar small-return premise is false even within a weakly reversible extension.

But D=0 is now NOT the old dormant face: C+E->C+D is active there, with rate gamma n at this output. Its next fast return to positive D can occur with unchanged A and no old seed mark. Hence the old dormant Green is the wrong operator, not merely an estimate with a worse exponent. The first extension must include this C+E source in a coupled face state and pay its actual return law.

This example does not show recurrence failure, nor say such a coupled Green diverges. It supplies an exact structural rejection test for the existing compiler and identifies the new operator one would have to construct. The paired addition adds one complex without changing the full stoichiometric rank, so it also leaves the current deficiency-one template: its deficiency increases by one. Thus this is a genuine architecture boundary, not another arbitrary longer conversion path inside the already acquired class.
