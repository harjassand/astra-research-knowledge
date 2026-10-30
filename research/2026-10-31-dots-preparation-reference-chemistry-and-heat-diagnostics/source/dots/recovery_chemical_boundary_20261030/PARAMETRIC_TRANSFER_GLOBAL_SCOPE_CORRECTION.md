# Global transfer scope correction: the 2D return edge

30 October 2026. Correction to the frozen PARAMETRIC_INTERFACE_TRANSFER_CANDIDATE. Its raw local bounds permit an absent 2a->2D seed, but its final assertion that every allowed edge belongs to a reaction-cycle return then does NOT hold: the positive 2D->a+D edge would have no directed complex-graph path back to 2D.

For the proposed GLOBAL classwise-positive-recurrence transfer, require BOTH seeds 2a->a+D and 2a->2D to have positive rates, as well as positive 2D->a+D. Together with a+D->2a and strongly connected type conversions, this makes the entire fast complex graph strongly connected; the connector shares the clearing complex, giving the required reaction-cycle returns.

This additional global restriction does not change or invalidate the broader local acquisition results when the second seed is absent. Those results do not assert recurrence of every state or weak reversibility. Without the added edge, the global communicating-class/transient-state conclusion needs separate formulation and proof and is NOT claimed by this transfer bundle. The frozen candidate's word 'optional' is superseded for its global conclusion only; source bytes remain unchanged.
