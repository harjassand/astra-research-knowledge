# Implicit-energy, all-future convex-flow compilation

## Main mathematical output

A deterministic approximation scheme for autonomous convex flows whose energies are represented by explicit rational convex quadratic programs with latent variables. It constructs a finite rational polygonal trajectory and a constant minimizer tail, uniformly accurate for all future time. Its complexity is polynomial in input bit length and reciprocal normalized error. It also approximates the equilibrium selected by the dynamics, not merely an arbitrary optimum.

Read `proof_note.md` for the theorem, complete derivation, cost accounting, imported results, exact counterexamples, and limitations.

**Status:** Historical novelty and independent general-proof validation are unresolved. Brézis–Ekeland–Nayroles action, backward-Euler energy-error analysis, Hoffman bounds, and polynomial-time convex QP are credited prior mathematics. The general QP optimizer is not implemented in this package.

## Reproduce the implemented evidence

Use Python 3.10 or newer; no third-party package is required.

```sh
python verify.py
python check_saved_certificate.py
```

The first command generates and verifies a rational all-future certificate for
`F(x,y)=x*x/2+max(0,x-y)` from `(1,0)`, checks sparse QP construction, and regenerates the JSON outputs. The second command independently reloads the saved certificate and checks its rational constraints and objective inequality.

The saved certificate proves error at most `1/200` for the entire infinite future under the action theorem. This is not a comparison only at selected sample times.

## Files

- `proof_note.md`: complete mathematical argument and prior-art/status boundaries.
- `energy_clock.py`: exact sparse-QP compiler, certificate checker, KKT checks, and explicit tail-constant bound. It constructs a QP but does not solve an arbitrary QP.
- `verify.py`: focused exact demonstration using a specialized proximal formula.
- `check_saved_certificate.py`: reload-and-check path independent of generation.
- `hinge_certificate.json.gz`: all rational primal and dual variables for the 535-cell example.
- `action_exact.txt`: exact rational action value.
- `verification_results.json`, `run_log.txt`: executed results, with decimal displays identified as approximate.
- `sources.json`: primary-source metadata and dependency status.

## General construction, not a claim of implemented backend

1. Solve the supplied static convex QP and acquire a rational global KKT witness.
2. Find a feasible lift of the initial observed state and a radius bound relative to a minimizer.
3. Compute the explicit polynomial-bit Hoffman upper bound and the terminal-time bound in the proof.
4. Construct the rational geometric mesh and call `compile_action_qp`.
5. Use a certified rational convex-QP backend to obtain a feasible sufficiently small-action point.
6. Project its terminal observed state onto the minimizer set using the original latent variables.
7. Verify the action bound and terminal-distance bound; replace the final endpoint and append the constant tail.

The proof charges the cost of all these steps. The prototype implements construction and verification and specialized examples, not steps 1/5/6 for general input.

## Exclusions

No physical experiment, continuum PDE discretization, arbitrary future forcing, nonconvex branch selection, persistent oscillation, polynomial dependence on accuracy-bit count, or practical superiority to established solvers is established.
