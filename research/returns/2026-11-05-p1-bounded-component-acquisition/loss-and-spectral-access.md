# First-ingress loss and aggregate spectral-access limits

These are separate source-specific converses alongside the [positive bounded-component receiver](README.md). Read the complete [first-ingress loss and ordinary-emitter proof](package/construction/first_ingress_bandwidth_loss_converse.txt), [actual-Weyl hard-band audit](package/construction/same_weyl_hard_bandwidth_audit.txt) and [integrated report](package/Astra_P1_Bounded_Component_Acquisition.pdf). Diamond distance and trace norm are **unhalved**; Bell fidelity is overlap with the normalized Bell target.

## Actual Weyl ports with physical collection loss

Take `n` independent unknown unencoded qubits, `H=0`, with actual pure-vacuum ports `L_x=sqrt(r)X/2`, `L_y=sqrt(r)Y/2`, `L_z=sqrt(r)Z/2`. Each output passes an ingress beam splitter of efficiency `eta`; lost fields and the remaining source are inaccessible. No control changes the source. The receiver can jointly process every collected field with arbitrary independent ancillas and later computation.

For every finite acquisition time, even after arbitrary collective recovery,

```text
F_Bell,opt <= [1-c_L(1-eta)^2]^n,
c_L=(1-exp(-2))^2/256.
```

The same right-hand side bounds `s F_Bell,conditional` for any heralded decoder, with Bell-input success `s`. Input-independent success is not assumed. A bounded-time causal stop is covered by granting the entire field through its latest possible stop. The resulting deterministic full-channel diamond error is at least `2{1-[1-c_L(1-eta)^2]^n}`. Necessary high-fidelity scaling therefore includes `1-eta=O(sqrt(epsilon/n))`; it is not an optimized or sufficient loss threshold.

An early lost Z-field mode already distinguishes the two initial Z inputs. A source-independent second-moment bound converts its mean separation into lost-environment trace distance; Uhlmann/information-disturbance bounds Bell recovery. At shorter acquisition times, the inaccessible remaining source supplies a stronger obstruction. Exact primal/dual Bell-recovery SDP tensorization includes collective decoding, with trace-class finite-rank approximation for finite-time continuous fields. Completing a success map to a deterministic channel gives the heralded bound. These established recovery tools are credited; the source-specific moment calculation and resource boundary remain explicit.

## Same Weyl source with a permanently inaccessible frequency complement

Restrict output to a finite interval `[0,T]`, append independent vacuum outside it, and then grant the receiver **all** Fourier modes with `|omega|<=B`, noncausally and before any receiver operation. The orthogonal frequency complement and remaining source are unavailable. This is a generous information-theoretic model, not a causal brick-wall filter. Restricting an ongoing field after projecting it is not silently substituted for this time-restriction/vacuum-padding order.

With `h_B=1-(2/pi)atan(B/r)` and `c_B=(1-exp(-1))^4/256`, every collective decoder obeys

```text
F_Bell,opt <= [1-c_B h_B^2]^n,
s F_Bell,conditional <= [1-c_B h_B^2]^n.
```

The deterministic unhalved diamond lower bound is twice one minus that product. For high fidelity, necessary aggregate half-bandwidth grows as `Omega(r sqrt(n/epsilon))`. Fixed individual linewidth/actuator poles do not imply this fixed aggregate inaccessible subspace: a growing coherent array can change total acceptance while each local component stays bounded, paying hardware and real transport. The positive receiver is compatible with this converse and does not establish a microscopic all-frequency material model.

## Distinct sharp ordinary amplitude-emission comparison

For the different source emitting `|0> -> |vac>` and `|1> -> |1_f>`, retaining squared mode fraction `eta` yields amplitude damping. Its exact best deterministic Bell fidelity is `[(1+sqrt(eta))^2/4]^n`, attained by the ordinary identity decoder; arbitrary collective correction cannot improve this metric. The same expression bounds heralded success times conditional Bell fidelity. For a Lorentzian spontaneous-emission mode, the corresponding necessary hard-band scaling is `Omega(n gamma/epsilon)`. That stronger dependence belongs to this amplitude-emission source; it is not assigned to the actual Weyl source.

## Attainable perturbation of the same receiver

Uniform attenuation **before capture** also has a sufficient full-channel allowance. For actual total physical Weyl photon rate `R_p` and complete active capture window `A`, the same deterministic bounded-component receiver adds at most

```text
2 sqrt(1-exp[-2 R_p A(1-sqrt(eta))]).
```

This follows from the scalar overlap `V_A^dagger eta^(N_ph/2)V_A=exp[-R_p A(1-sqrt(eta))]I`. It includes arbitrary input/reference and receiver postprocessing. Internal loss after partial loading needs its own physical error budget. This attainable allowance and the converse leave a gap; no optimal loss threshold is asserted.

These statements concern an already unknown unencoded input with missing first-interface information. They do not prove zero coded/assisted capacity, forbid encoding before loss or grant later error correction the absent field. No device, physical validation or new Capital science execution is claimed. [Supplied audits and original hashes](SOURCES.json).
