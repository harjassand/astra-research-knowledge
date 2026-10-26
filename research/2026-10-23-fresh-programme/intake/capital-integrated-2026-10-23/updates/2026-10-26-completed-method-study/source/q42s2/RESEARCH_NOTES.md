# Stress, failed strengthening and retained limits

## Strongest competing explanation

The first-stage circulator can look like perfect directionality if a tiny reverse
coefficient is rounded away. It also diverts heat through a third terminal, so an
isolation score is not automatically an improvement in total source cooling.
The first-stage full-cycle comparator already prevents the latter interpretation.
The second stage attacks the former over the full finite positive-network class.

An initially overbroad graph argument would say that every pair in a connected
union graph must transfer heat. This is false when the connecting path passes
through a clamped third terminal. The correct theorem uses terminal-avoiding
paths, exactly as static Kron topology does. The withheld ensemble deliberately
contains many such terminal cuts; it is not restricted to fully coupled examples.

The completed proof shows identical forward/reverse zero patterns and gives an
explicit strictly positive reverse-transfer floor. The proof permits singular,
disconnected individual phases and arbitrary repeated phase ordering. Its
diagonal-capacity assumption is explicit. Stage1's broader constant-SPD matrix
comparison was separately stressed with nonlocal capacity matrices. Two such
cases have positive off-diagonal responses, demonstrating why a generic SPD
storage matrix must not be called an ordinary positive thermal store.

## Withheld tests

The sparse-tree schedule ensemble was defined using seed 202610264201. It uses
3/4/5/6 terminals, 1/2/3/5 internal stores and only one active edge in each phase,
with independently varied contact rates, durations and positive capacities.
Its 80 schedules yield 680 unordered terminal pairs: 318 have an internal-only
path and 362 are blocked by terminal cuts. All support predictions and reverse
floors pass. This is new evidence outside stage1's dense and instantaneously
grounded graph family; the universal statement rests on the proof.

The underflow tests z=12,40,100,500,800 were not selected from stage1's favourable
fixtures. At z=800, Float64 gives reverse coefficient zero. The exact formula at
100-digit precision gives 1.528281076740703e-351, with a finite isolation ratio
2.726374572112567e347. Hot-port extraction is only .001875 of the matched static
star. This is an explicit false-perfect-isolation diagnostic, not a new device.

The matrix-capacity stress uses its separate seed 202610264202, with 64 constant
SPD nonlocal capacity matrices and disconnected single-edge phases. The original
reversal, energy-gap and circle constraints remain satisfied within roundoff.

## Stronger positive mechanisms actually attempted

I constructed two three-body alternatives, each with aggregate capacity one,
mean total conductance one, three modulated contacts at off/on=.001 and three
explicit additional fixed contacts. In one, the terminal contacts are fixed and
internal ring contacts switch cyclically. In the other, an internal ring is fixed
and the terminal contacts switch. Bodies have capacity 1/3 each. No extra detector,
selective reset, capacity modulation, advection or energy source is supplied.

Ordinary numerical design selection optimizes the fixed-vs-switched conductance
allocation and cycle period. It is allowed to reverse orientation. Each candidate
is compared with the competent first-stage one-body controller, at the same total
capacity, mean conductance and number of modulated phases. The additional fixed
connectors are recorded, so a claimed gain could not ignore their physical cost.
Both mechanisms give less directional throughput in the searches actually run.

The gated-port ring's isolation objective reached the initial upper period bound.
It would be invalid to declare its global failure from that truncation. A followup
holds periods 148.4,300,1000,3000,10000 and reoptimizes conductance allocation.
Isolation rises toward the one-body benchmark, from 63.87 to 69.71, while forward
throughput falls from .00675 to .0001003. No gain is established. These searches
do not prove a global optimum over every multi-body architecture, and the
observed approach is not promoted into a proved asymptotic limit.

## Implementation and preservation

Stage2 scripts import the preserved stage1 solver with bytecode writing disabled;
they do not modify it. A before/after content inventory verifies preservation.
The hashes only check file integrity, not scientific correctness.

An initial architecture-search invocation failed because its seed exceeded the
legacy optimizer's 32-bit limit. That traceback is retained in
architecture_stderr_initial.txt; the reproducible corrected code explicitly
reduces the seed modulo 2^32-1. No scientific output was produced by the failed
invocation. Other host floating-point warnings, if any, remain in stderr logs.

The resulting no-perfect-isolation theorem closes a stronger idealization of
the proposed contact mechanism. It does not rule out a useful finite-isolation
device, nor establish that the new formulas are novel. Practical finite-isolation
advantage with complete actuator, storage, connector and clock accounting remains
the unsupplied operation.
