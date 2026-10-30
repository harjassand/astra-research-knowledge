# Fully stopped connector-to-head estimate

This replaces the input/cohort split used for estimate (2) in CONNECTOR_MEDIATED_LAUNCH_RETURN_COMPLETION. It avoids extending a cohort estimate across true-F feedback.

Let Q_R be the ACTUAL positive-D-start first-connector law after its fixed-b true-F feedback has been summed. For every finite requested p,s, the earned reset and profile bounds give

    Q_R f_p(A_out) <= C_p n^-eta_p,
    Q_R f_(2s)(A_out) <= C_s f_(2s)(A_in).

For the actual output event E={A_out<=2M},

    Q_R 1_E <= (1+2M)^p C_p n^-eta_p.

Cauchy–Schwarz for this same substochastic output measure therefore yields

    Q_R[f_s(A_out)1_E]
       <= (Q_R 1_E)^(1/2) (Q_R f_(2s)(A_out))^(1/2)
       <= C_(M,p,s) n^(-eta_p/2) f_s(A_in).

This includes mixed D=0 connector outputs and all other output types; restricting to a particular carried face only decreases it. Multiplication by the bounded actual first-connector phase/residual tilt factor is harmless after theta,lambda are fixed. The bound uses neither independent marginal experiments nor a conditioned cohort law.

For M=K(n)=C log²(2+n), the same calculation has only the fixed polylogarithmic factor (1+2K)^(p/2), so it still tends to zero with a positive power after decreasing the exponent. On a retained r-exterior phase state, n>=r-O(1); output cutoffs must nevertheless be evaluated at the actual output when the complete section bad-row inequality is used. The output-sensitive repair from the accepted phase processor is unchanged.

The full first-connector law here is available before this new global phase argument: its only pre-connector boundary feedback is R-to-true-F, whose rate/profile estimates and old dormant seed kernel did not require an initially mixed clock. Mixed holds entered during R are paid by their ingress compensator. This order makes the use of Q_R noncircular.
