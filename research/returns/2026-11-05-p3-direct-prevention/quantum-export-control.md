# Quantum export with additional physical source control

The supplied [control-for-calibration construction](package/next6_physical/CONTROL_FOR_CALIBRATION.md), [README](package/next6_physical/README.txt), [status](package/next6_physical/STATUS.txt) and [source provenance](package/next6_physical/source_provenance.json) give a conditional arbitrary-input/reference quantum export protocol. It adds actual calibrated control on the source, in addition to pure coherent output ports. This is a different access model from output-only calibration.

## Physical access and guarantee

There are n source qubits with an unknown predetermined H(t), after removal of a scalar, satisfying operator norm at most Lambda. Fresh random control frames are independent of the current drift. The drift cannot adapt after observing the current private frame.

Each qubit has three known pure-vacuum coherent Weyl ports L_i,a=sqrt(r) sigma_i,a/2, with all outputs retained coherently at known phase and without unbudgeted loss. The calibrated rate r is positive and the photon intensity is 3nr/4. Classical jump records, a mixed bath without its purifier, or one commuting output port do not supply this access.

Local X/Y/Z rotations act physically on the source. Their strengths, slew, action and error are paid. A frame-dependent port-phase correction gives covariance of the full source-plus-output dilation; decoupling only the reduced source channel would not establish export recovery.

For B_frames blocks over total duration T and discarded pulse/guard duration tau_disc, the stated **unhalved diamond-error** bound is

```
2n exp(-rT) + 2 Lambda^2 T^2 / B_frames
 + 2 (Lambda + nr) tau_disc
 + controller, receiver, memory and port errors.
```

The fresh key is used to correct the coherent output and is then discarded from the target. The quadratic averaging claim is not a per-key or key-plus-payload guarantee; the supplied counterexample makes that distinction explicit. Random dynamical decoupling and quadratic improvements have established precedents, which the source credits. The full output/receiver join is not a claim to invent dynamical decoupling.

## Costs, receiver and evidence

The noise-only reset/export instrument uses the accepted coherent-port receiver. The construction retains that receiver's potentially large field array, propagation, precision, protected storage, factory and calibration costs. It does not replace the receiver with a cheap buffer. Smooth finite pulses require increasing strength and slew as size or accuracy demands grow; there is no promise for arbitrary size/error at a fixed installed control strength.

A microscopic Markov or finite-passband bath is not constructed, and the protocol does not calibrate its own physical ports. No hardware run, same-access minimax advantage or historical priority is established. The [boundary comparator](package/next6_physical/BOUNDARY_COMPARATOR.md) retains the changed source-control access and comparison limits.

The saved [audit results](package/next6_physical/audit_results.json) cover 12 finite pure-collision dilation points with one or two qubits, normalized Choi states retaining source and environment, kept/discarded-key identities, and sufficient schedules for n=1,4,16,64. These are supplied finite diagnostics, not a continuous-field/full-receiver simulation or hardware validation. Three original receiver/source files are retained with hashes. Capital published these bytes without rerunning the program or adding a new scientific audit.

The [main direct-prevention theorem](README.md) concerns a classical rare-catastrophe mean under reciprocal controls; this quantum companion is a separate operation with its own stronger physical interfaces.
