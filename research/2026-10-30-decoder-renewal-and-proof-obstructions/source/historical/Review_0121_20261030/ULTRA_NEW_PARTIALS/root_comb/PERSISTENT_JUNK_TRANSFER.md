# A positive escape changes the joint source, not its one-use formula

30 October2026. Root construction from A's independent source-memory control
and the admitted ordinary four-query qubit-isometry inverse. This is a
conditional physical operation and a discriminating-test design. The required
source memory has NOT been acquired; no source or physical experiment was run.

## 1. The stronger, precise source process

Let U:C^2 tensor C^r -> C^D be unknown isometric and U_j psi=U(psi tensor|j>).
An input-independent CLASSICAL source memory selects labels j_0,...,j_4.
Conditioned on that sequence, the payload is U_j0 rho U_j0* and the four
subsequent forward calls are the isometries U_j1,...,U_j4 on arbitrary
adaptive/entangled logical inputs. Every U_j remains unknown to the user.
Labels are not revealed or coherently selectable. The source memory is
nevertheless a supplied JOINT process, not five memoryless uses of its
averaged marginal.

If each label has marginal p, each individual use still has exactly

    N_U(X)=sum_j p_j U_j X U_j*.

That one-use equality does not distinguish fresh labels from one persistent
hidden label, and cannot justify substituting one joint process for another.
The preceding exact-heralding theorem explicitly assumes a memoryless source;
this alternative changes that assumption and is not a counterexample.

## 2. Literal recovery and complete error bound

Apply the established exact deterministic four-forward-query inverse for an
unknown qubit isometry (2401.10137v3, Section3.3/Corollary6), with the incoming
physical payload as its input and the next four source uses as its four slots.
All four calls occur ONLINE after the payload in this construction. Known
controller gates and protected storage are additional paid resources.

On the event G={j_0=...=j_4}, the entire experiment is precisely the pure
unknown-isometry experiment for U_j. The ordinary protocol therefore returns
rho exactly, including its arbitrary reference, for EVERY unknown U_j.
Conditional on any other label sequence it still defines a CPTP channel.
The labels' law is independent of the logical input, so averaging gives

    Lambda =Pr(G) id +[1-Pr(G)] Lambda_bad,
    (1/2)||Lambda-id||_diamond <=1-Pr(G).                 (P1)

No flag observation or heralding was used. This is throughput one. An internal
source frame does not need to be learned, and the rank r does not enter(P1).

For a stationary hidden Markov chain with transitions P and P_jj>=1-lambda
for every j,

    Pr(G)=sum_j p_j P_jj^4 >=(1-lambda)^4,
    complete error <=1-(1-lambda)^4 <=4lambda.            (P2)

More generally an input-independent label process with adjacent-change
probabilities at the actual five-slot schedule at most lambda_t obeys
complete error<=sum_(t=0)^3 lambda_t by the ordinary union bound. Markov or
independent-change events are not needed for that weaker statement. A known
whole-controller implementation error delta adds by channel telescoping.
The conditional pure-source oracle must remain the SAME isometry through
the scheduled gates; drift of U itself is an additional process error.

The ordinary primary's displayed generic CG implementation cost is polynomial
in the physical output dimension D, its slot count and log inverse precision;
it is not credited as poly(log D). Source latency, actual controller gate
depth, source memory retention over that time, and payload coherence must be
acquired. Four query slots alone are not a physical speed or practicality claim.

## 3. A frame-free experiment can discriminate the relevant source assumption

There is a simple known operation to test one consequence of this process
model. Prepare the SAME known pure logical probe psi on two scheduled source
calls, retain their full physical outputs, and measure their SWAP. No unknown
frame, environment label or support projector is needed. Orthogonality gives

    <U_j psi|U_l psi>=delta_jl,
    E[SWAP]=Pr(j_1=j_2).                                 (P3)

For fresh uniform labels this mean is1/r. For one perfectly persistent label
it is1. In the stationary classical Markov model it is sum_j p_j P_jj.
The probability of the antisymmetric outcome is exactly

    Pr(SWAP=-1)=[1-Pr(j_1=j_2)]/2.                        (P4)

This gives a concrete process diagnostic rather than calling rank-r one-use
outputs pure. It consumes two probe calls per trial and requires protection
of both D-level outputs plus known O(log D) controlled-SWAP gates. Independent
repeated trials require an acquired reset/independence contract; no iid
confidence interval is inferred from a drifting single source trace.

A Bell-query variant retains the two known logical reference halves and
measures SWAP of the ENTIRE reference-plus-physical-output programmes. The
conditional pure Choi vectors of U_j and U_l have overlap
Tr(U_j*U_l)/2=delta_jl, so(P3)--(P4) remain exact. This diagnostic includes
the known reference correlations and costs the same two source calls plus
the two reference qubits. One scalar Bell-SWAP statistic still does not
determine an arbitrary sequential process on all adaptive inputs.

For a stationary classical source and a fixed repeated inter-call gap, let
lambda_bar=Pr(j_1!=j_2). If INDEPENDENT source-reset trials have been
acquired, n probe pairs giving zero antisymmetric outcomes imply, at
confidence1-delta,

    lambda_bar <=2(1-delta^(1/n)) <=2 log(1/delta)/n.      (P5)

Indeed each antisymmetric indicator is Bernoulli(lambda_bar/2), and the
probability of all zeros is(1-lambda_bar/2)^n. If the four actual decoder
gaps have this same stationary law, their union-bound error is at most
4lambda_bar. Thus n>=ceil[8 log(1/delta)/epsilon] zero-event pairs supply
the stated retention contribution epsilon, CONDITIONAL on that process
and reset model. This is2n probe calls plus paid resets, storage and
measurement gates, in addition to four online decoder calls. Different
gaps need separately valid bounds/confidence allocation. No trials or
zero-event observation have been made here.

Within the declared input-independent classical-label model, pairwise stay
probabilities at the decoder's actual adjacent time gaps feed the union bound
in(P1). Outside that model a single known-probe statistic cannot certify the
process on arbitrary entangled feedback inputs. It also cannot by itself
certify U stability, a full process-diamond bound or the four-call decoder's
physical accuracy. Those are separate source/interface obligations.

## 4. Strategic meaning and actual acquisition boundary

This is a short route to a strong quantum operation if a persistent hidden
mode already exists or can be supplied: (i) establish the joint source model,
(ii) measure/justify retention over the required call schedule, (iii) admit
the paid ordinary isometry controller and its coherence budget. The result
would then be high-accuracy arbitrary-payload recovery with four online
source calls, under(P1), instead of a memoryless rank-dependent programme.

It is NOT a faster algorithm for the original iid-junk source. Correlating
the junk preparations is a stronger physical resource; it is not obtained
by observing an ordinary marginal, relabeling RDS's common latent frame, or
silently retrying unknown inputs. No existing hardware in this campaign has
been shown to supply it. Current source-memory acquisition is UNKNOWN.

The pure four-query inverse is established prior, fully credited. The present
construction is its explicit joint-process transfer, complete error contract
and frame-free discriminatory operation. Public priority is UNKNOWN. The
mathematical protocol/test design is completed; no experiment is authorized
or claimed as having occurred.
