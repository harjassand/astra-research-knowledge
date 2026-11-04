# Exact output-only partial-SWAP recovery and two information clocks

The complete [standalone construction](package/partial_swap_theory.txt), [independent proof supplement](package/theory_converse.txt) and [integrated report](package/tracial_acquisition.pdf) give an executable receiver for the [fresh-tracial one-pass architecture](README.md). Errors here are half diamond distance. The unknown initial state can be entangled with an inaccessible reference; no source survives as an accessible output and no bath purifier is supplied.

## Receiver and exact recovered channel

Each fresh `d`-level bath register starts independently in `I/d` and encounters the source through `U_j=exp(i theta_j SWAP)`. Arbitrary known source rotations may be interspersed. Keep all `N` physical outputs with their correlations. Prepare one independent dummy source in `I/d`, reverse the complete known collision/rotation circuit on dummy and outputs in reverse chronological order, discard consumed outputs and return the dummy. All reversal acts in the receiver; the emitted particles do not revisit the actual source.

The resulting physical channel is exactly

```text
D C=(1-r)id+r Tr(.)I/d,
r=product_j(1-sin^4(theta_j)),
delta(D C,id)=(1-d^-2)r.
```

For `c=1-d^-2`, every final receiver decoder obeys `c(1-sqrt(1-r))<=epsilon_opt<=c r`. Thus this explicit maximally mixed-dummy/Petz decoder is within a factor two of the optimum. The exact quartic recursion and source-discarded receiver matter: full source-plus-bath reversal would supply an unavailable register. Petz/inverse recovery and existing near-optimality inequalities are credited prior machinery.

For `m` independent product emission modules, arbitrary entanglement across inputs/reference and unrestricted collective final decoding remain allowed. With `V=product_i(1-c_i r_i)`, the actual product reverse receiver has error `1-V`; every collective decoder has error at least `1-sqrt(V)`, with a stronger centered finite-dimension bound in the supplement. At fixed `d` and weak constant `theta`, `N=Theta(theta^-4 log(m/epsilon))` per module and total quartic action is `Theta(m log(m/epsilon))`. Cross-module active control or shared memories that destroy product emission do not inherit this product law.

## Forgetting is a different clock

The reduced source visibility is `beta=product_j cos^2(theta_j)`. At weak fixed action, source forgetting takes order `theta^-2 log(1/epsilon)` collisions, but reference-preserving output-only recovery takes order `theta^-4 log(1/epsilon)`. The complete physical output contains less accessible information than an assumed pure complementary environment.

Choose `cos^2(theta)=exp(-gamma Delta)`. At every grid time `T=N Delta` the source channel is **exactly** depolarization with visibility `exp(-gamma T)`, while

```text
r=[1-(1-exp(-gamma Delta))^2]^(T/Delta),
alpha=1-r=gamma^2 T Delta+O(Delta^2)  (fixed gamma,T).
```

The entire physical bath approaches a constant-output replacer as `Delta` tends to zero at fixed source evolution time. A coarse strong collision and many fresh weak collisions can therefore agree on the exact source channel at every coarse time yet have different output acquisition clocks. This is a finite accessible-output statement, not an identification of all dilations from a reduced generator.

Fixed `gamma` in that limit requires peak interaction strength of order `sqrt(gamma/Delta)`. At bounded source coupling `J`, with `theta=J Delta`, source-forgetting time instead scales as `(J^2 Delta)^-1` and collection time as `(J^4 Delta^3)^-1`, with accuracy logarithms. There is no free fixed-strength continuum clock. Delivery, routing, decoding and protection add to native collision time.

## Evaluated resource point and finite evidence

The [final resource table](package/resource_counts.json), using the stronger centered converse, gives for `d=2`, `theta=0.1`, target ideal error `0.01`: 432 source-forgetting collisions, at least **36,552** encounters for any decoder, and **43,462** for the explicit receiver. The supplied local junction then needs 944,450,991 capture-routing SWAPs and 944,581,376 total two-qubit gates, before preparation/calibration/protection. For 1,000 modules at the same total target, the ideal receiver uses 112,948 outputs per module, 112,948,000 retained output qubits. Reserving physical error budgets increases the required intrinsic collision count further.

These large counts are exact formula evaluations, not full-bath simulations. Earlier necessary-count rows in [matrix diagnostics](package/hot_bath_checks.json) use a simpler valid bound, while the standalone construction also retains earlier conservative estimates; the final table's 36,552 is not a contradictory measured optimum. Actual small-matrix checks are listed on the [main result page](README.md), with the [original program](package/check_hot_bath.py) retained unexecuted by Capital.

The [finite-interface result](finite-interface.md) specifies a schedule with `N+2` operation qubits, finite gate/latency costs, growing routing, memory space-time and qualification. It does not establish optimum memory or optimum wall time. If a source encounter can simply be extended to a full SWAP, that stronger ordinary access exports the payload in one operation; weak one-pass maximum encounter windows are an actual premise. [Original package and provenance](SOURCES.json).
