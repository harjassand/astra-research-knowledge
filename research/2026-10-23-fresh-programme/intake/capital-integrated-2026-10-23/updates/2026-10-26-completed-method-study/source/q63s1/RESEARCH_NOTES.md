# Scientific development notes

This is the first attempt and its capacity recovery, within the original
useful-work allowance. It was not replaced by another trial or model.

The initial motivation was hidden thermal-network identification with one
boundary sensor. Ordinary one-port transfer measurements admit hidden modes
and realization ambiguity. I considered changing local heat capacities to
label internal states. At a fixed positive Laplace variable a capacity change
is mathematically a diagonal load, but a steady capacity change produces no
signal. Rather than claiming an unavailable material actuator, I separated
the algebraic problem and used calibrated positive shunts at labeled nodes.

A first thought used mixed derivatives of the one-port resolvent with respect
to pairs of loads. Those derivatives recover a product of three Green entries,
but treating derivatives as free data hides precision and acquisition cost.
I replaced them by two finite amplitudes per node and one finite pair load.
This gives exactly the parameter-dimension number of scalar configurations.
The remaining quadratic has two algebraic roots. Simply choosing a positive
root is insufficient; the Schur-complement inverse-M inequality supplies an
admissible interval on which the response is strictly monotone. This was the
main nontrivial step in the reconstruction proof.

The exact rational implementation then recovered 24 matrices in four graph
families. Random floating-point tests unexpectedly rejected two longer paths
even with noiseless supplied responses. Those cases remain in float_checks.csv.
They are consistent with tiny differences in one-port response being rounded
away; exact recovery is not a numerical stability theorem.

The independent incumbent was allowed the full complete graph, nonnegative
leaks and conductances, an analytic Jacobian and eight starts. It received the
identical raw scalar observations. On dense cases its solution coincided with
the direct reconstruction, including noise sensitivity. The formula therefore
does not show a new practical inference capability over this ordinary method.
On noisy sparse cases the unconstrained formula may leave the physical class;
positive offdiagonal entries on the noisy star were explicitly recorded in a
supplementary physical-status file instead of being interpreted as a result.

I then pursued a depth limit, first using a Neumann-series exponential bound
and a Gaussian KL/Pinsker argument. depth_barrier.csv preserves that first
analysis. A stronger argument appeared during recovery: the scalar difference
between a baseline network and an added local leak decreases in *every*
nonnegative shunt coordinate, because inverse entries decrease. This yields an
exact maximum signal at no added load, not merely a loose uniform bound.
Every loaded Gaussian reading can be simulated by attenuating an unloaded one
and adding noise, giving an exact ordinary optimal comparator even against
adaptive control. limits_and_bypass.csv uses this stronger result. It must not
be confused with the initial loose bound or a claim about arbitrary detector
noise.

I attempted the natural bypass: remove pre-existing leaks instead of adding
them. For any connected conductance graph with only port grounding, a unit
port input produces the same steady temperature/voltage at every node. On a
path the fault signal becomes 1/(L+2). Exact rational calculations confirm it.
This removes the depth barrier only by granting an additional physical control.
Standard electronic guarding is an antecedent, and a known switched resistor
test network can do this ordinarily. No source or construction here gives
selective internal thermal-loss removal in an unknown specimen; asserting it
would assume the central operation that needed invention.

Finally I checked whether arbitrary frequency data could self-calibrate those
internal interventions. A diagonal congruence jointly rescales conductances,
capacities and load gains while preserving the port transfer exactly. The
explicit positive-capacity, positive-leak example is in calibration_gauge.json.
This is a structural ambiguity, not insufficient fitting or sample count.
Changing representation to a command-normalized model predicts permitted
commands but cannot give absolute internal physical semantics. No further
unproven representation acquisition is asserted.

The primary-source search showed substantial established inverse-network,
local susceptibility and inverse-decay theory. It did not settle priority of
the exact combined theorem; absence of a matching search result was not used
to certify novelty. These notes preserve the failed mechanism, stronger route,
and remaining operation rather than retelling them as a successful physical
invention.
