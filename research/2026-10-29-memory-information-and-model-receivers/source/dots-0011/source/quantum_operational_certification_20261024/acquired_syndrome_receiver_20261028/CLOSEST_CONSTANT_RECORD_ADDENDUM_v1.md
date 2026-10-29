# The fixed-record quantity is also distance to the closest constant record

28 October2026. New author addendum to the frozen GOVERNING_BRANCH_RECOVERY_v1.md (SHA256 d09353188b8c2171be328d024b10da3a84826c185e2a7e209626386e7d5a6084). Independent review pending. No preceding numerical result changes.

The frozen source proves ||M_record−K_a||_diamond=L=sum_s||b_s|| for K_a(rho)=Tr(rho)sum_s a_s|s><s|. It conservatively does not assert optimization over constant records. The following short argument establishes that stronger statement without changing the original source.

For an arbitrary probability distribution q, let K_q(rho)=Tr(rho)sum_s q_s|s><s|. Apply M_record−K_q to one half of a normalized Bell state. Its syndrome-s reference block is

    [(a_s−q_s)I+b_s dot sigma]^T/2.

The block eigenvalues are[(a_s−q_s) plus/minus ||b_s||]/2, and its trace norm is

    max(|a_s−q_s|, ||b_s||).

Therefore ||M_record−K_q||_diamond is at least the sum of these maxima, which is at least L for every q. Since q=a attains L by the original theorem,

    min_(constant classical-record channels K) ||M_record−K||_diamond = L.

This proves K_a is a minimizer, not necessarily the unique one. Constants are channels with the SAME classical record alphabet; no larger quantum output or record postprocessing is silently admitted. Combining with the fixed-POVM attainment in the frozen source gives

    max_(instruments E with record POVM F) [F_e(best CPTP receiver)−F_e(best unitary receiver)]
      = (1/4) min_(constant classical-record channels K) ||M_record−K||_diamond.

The maximum is attained by E_s(rho)=Tr(F_s rho)I/2, using reset-to-b_s receivers. The interpretation is an extremal relation between actual qubit record leakage and receiver choice, not an assertion of nonunital advantage for every instrument or of coherent preservation by the attaining erased-output instrument.
