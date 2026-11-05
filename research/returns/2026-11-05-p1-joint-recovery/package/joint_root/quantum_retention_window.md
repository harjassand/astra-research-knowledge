# A joint angle/error lower bound on quantum retention time

5 November 2026. Corollary of the arbitrary-receiver positive acquisition ledger.
This lower bound concerns the duration/probability of nonzero quantum memory;
it does not solve the maximum quantum width. All histories are weighted by the
physical Bell-input experiment, as in the accepted peer memory-tail converse.

Let r=1-sin(theta)^4, and suppose the complete receiver achieves half-diamond
error <=epsilon<1/2. Put

  A_epsilon=(1-4epsilon/3)^2,
  C_epsilon=(3/2)(1-A_epsilon)=4epsilon-(8/3)epsilon^2.

At cut j, write pi_j for the Bell-input probability that the retained quantum
memory has dimension at least two; arbitrary classical history is free. The
ledger yields the universal branch-occupancy bound

  pi_j >= [1-C_epsilon r^(-(N-j))]_+ .                       (1)

This is nonvacuous when epsilon is sufficiently small that C_epsilon<1, and
applies to any declared receiver width, controls, initialized workspace, and
feedback. It also lower bounds expected occupied qubits at that cut.

## Proof

For any qubit-input channel with classical history x, its Petz entanglement
fidelity splits into nonnegative branch contributions. A branch with memory
dimension one has the form E_x(rho)=Tr(E_x rho), where E_x>=0 is an effect, and
its physical probability on the maximally mixed input is p_x=Tr(E_x)/2. Its
Petz contribution is

  F_(P,x)=(1/4) Tr(E_x^2)/Tr(E_x) <= p_x/2.

A general branch has contribution <=p_x: its Petz decoder is trace preserving
on the branch support, so its Bell overlap is at most the trace p_x of its
subnormalized Choi state. Summing all branches gives

  F_(P,j) <=(1-pi_j)/2+pi_j=(1+pi_j)/2.

Since the exact ledger identifies F_(P,j)=(1+3a_j)/4,

  pi_j >=(3a_j-1)/2.                                      (2)

The loss equations imply a_j+q_j<=1. Even granting zero future receiver loss,
the remaining N-j collisions can add at most (1-r^(N-j))q_j to a_j. Hence

  a_N <=a_j+(1-r^(N-j))q_j
      <=1-r^(N-j)(1-a_j).

The decoder converse forces a_N>=A_epsilon. Therefore

  a_j >=1-(1-A_epsilon)r^(-(N-j)).

Combine this with (2) and nonnegativity to obtain (1). No carrier-erasure model
is used. A retained register that happens to be unused can only increase the
capacity being counted, so the bound also applies when a receiver minimizes its
actual physical occupancy.

## No late restart from purely classical memory

If every branch has only classical memory at cut j, pi_j=0. Equation (1) gives

  r^(N-j) <= C_epsilon,
  N-j >= log(1/C_epsilon)/[-log r]                         (3)

when C_epsilon<1. Thus an accurate receiver cannot discard all its coherent
memory and start a new quantum episode shortly before the final deadline. The
necessary remaining episode has the full quartic weak-angle order
Theta(theta^-4 log(1/epsilon)). This is a statement about a quantum-free cut;
it does not assert that every individual history has the same last reset time.

## Memory-time with an explicit physical clock

If the physical duration after cut j until the next carrier is Delta_j>=0,

  E[quantum memory-time] >=
    sum_(j=1)^(N-1) Delta_j [1-C_epsilon r^(-(N-j))]_+.     (4)

This bound holds pointwise throughout each interarrival interval: insert every
receiver-only operation as a step with zero acquisition, and use the same
number N-j of remaining source encounters. Integrating the resulting occupancy
bound proves (4), without assuming that memory stays unchanged between arrivals.
The accounting includes any recovered output already produced but still held
until the declared final handoff. If the task ends earlier, its actual handoff
time and actual number of used encounters replace that later deadline.

For equal interarrival duration Delta, put ell=-log r. When the horizon is long
enough to contain the nonzero part of (1), the discrete sum obeys

  sum_(k>=1) [1-C_epsilon exp(ell k)]_+
    = [log(1/C_epsilon)-1+C_epsilon]/ell + O(1),            (5)

where the error between the sum and the integral is bounded by one. Therefore,
simultaneously for small angle and high accuracy, the receiver pays at least
order Delta theta^-4 log(1/epsilon) qubit-time. If Delta itself depends on theta,
that dependence remains explicit; no source clock or receiver speed is assumed.

An earlier result already requires the quartic collision count. This corollary
adds a statement about persistent quantum occupancy even with arbitrary classical
histories and initialized workspace. It is weaker than a sought joint peak-width
law and is not substituted for that unresolved endpoint.
