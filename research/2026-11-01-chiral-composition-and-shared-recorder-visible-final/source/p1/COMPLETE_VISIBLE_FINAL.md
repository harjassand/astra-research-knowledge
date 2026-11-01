## Result

**I constructed a microscopic route from molecular handedness to a shared physical composition record, together with a product-selection operation. I did not establish economical complete recovery of rare material.**

The strongest construction uses a molecular cycle that returns an unknown internal state while accumulating a handedness-dependent phase. I then derived a way for a retained quantum recorder to control that cycle through an actual quantized dipole interaction. This supplies a physical mechanism for collective information acquisition; it does not assume a useful collective predicate as a native rate.

The complete-task comparison substantially limits the claim. An ordinary coherent separator given the same controls can also avoid internal-state cooling. Moreover, returning the molecule or interaction resonator does not establish restoration of its driving fields or erase information carried away by lost photons.

The established collective laws and all earlier research are preserved byte-for-byte in the new archive.

## 1. The question and the molecular interaction

I chose this question:

> **Can a physical machine transfer the composition of a molecular packet into one shared record while returning its unknown internal states—and can that operation support economical separation?**

The concrete family is stable chiral asymmetric molecules. Opposite enantiomers have the same field-free rotational spectrum and dipole magnitudes, but the sign of the closed-loop product
\[
\mu_a\mu_b\mu_c
\]
reverses. That sign survives changes of phase convention for the individual internal states. Electric-dipole cyclic transitions and their rotational selection rules provide the physical ingredient. :chatgpt-content-reference{index="0"}

I started from
\[
H_s(t)=h(AJ_a^2+BJ_b^2+CJ_c^2)
-\mathbf E(t)\cdot\boldsymbol\mu_s,
\]
with the handedness sign \(s\) placed in one body-frame dipole component.

For a numerical bridge, I used public spectroscopic data for the **gG′a conformer of 1,2-propanediol**. Its dipole components are \(2.496,\ 0.309,\ 0.450\) D. Angular-momentum algebra produces the actual three driven matrix elements \(1.4411,\ 0.2598,\ 0.1545\) D, at approximately \(6.427,\ 12.042,\ 5.615\) GHz. These are derived couplings, not fitted discrimination rates. This conformer lies above the lowest-energy conformer, so the calculations explicitly condition on it. :chatgpt-content-reference{index="1"}

### The first useful failure

An isolated three-state loop has a particularly attractive exact revival: after a finite pulse, every internal state returns and only a handedness-dependent scalar phase remains.

The physical molecule also has magnetic spectator states. Those spectators acquire misleading phases under the naïve pulse, contaminating the output. The three-level revival alone therefore fails as a device construction.

I repaired this with an exact spectator echo. In the relevant seven-state manifold, the signed physical generator contains both
\[
sX_{13}\quad\text{and}\quad -sX_{45}.
\]
A common \(2\pi\) pulse reverses the active contribution while preserving the spectator contribution. A four-pulse combination retains the desired signed rotation and cancels the spectator exactly.

Together with the physically available transitions from the \(J=0\) hub, this gives an explicit finite word satisfying
\[
W_+=I_7,\qquad W_-=e^{i\phi}I_7,
\qquad \phi=\frac{4\pi}{7}.
\]

The word has 104 pulses. It preserves **every density matrix on those seven states**, including coherences and a maximally mixed state. Higher rotational manifolds do not automatically inherit individually addressable transitions; I have not treated the seven-state construction as an all-rotor result.

## 2. The stronger construction: acquiring a shared physical record

A scalar phase is invisible if the molecule is considered alone. A controlled version of its evolution is an additional physical operation that must be built.

The stronger route uses a resonator and a recorder qubit. Let
\[
A=\sum_{i=1}^{M}s_i\bigl(X_{13}^{(i)}-X_{45}^{(i)}\bigr)
\]
be the actual signed dipole generator of a packet.

Quantizing the electric field gives ordinary Jaynes–Cummings couplings between the resonator, the molecules and the recorder. Under resonant dressing, these yield a force of the form
\[
H_F/\hbar
=
(\lambda_bX_b+\lambda_mA)
\left(ae^{-i\delta t}+a^\dagger e^{i\delta t}\right).
\]
Here \(X_b\) is the recorder observable, and the \(\lambda\)'s come from physical dipole couplings. Driven-cavity force gates are established machinery; the contribution here is connecting them to the derived molecular generator while retaining its spectators and control costs. :chatgpt-content-reference{index="2"}

### Exact two-circle operation

Run a complete oscillator circle at detuning \(-\delta\), flip the recorder, run a circle at \(+\delta\), and flip the recorder back. In the force model,
\[
\boxed{
U_{\mathrm{pair}}
=
\exp\!\left[
-\frac{8\pi i\lambda_b\lambda_m}{\delta^2}X_bA
\right]\otimes I_{\mathrm{osc}}.
}
\]

The proof is ordinary operator algebra. One circle produces a phase proportional to
\[
F^2,\qquad F=\lambda_bX_b+\lambda_mA.
\]
The recorder flip changes the sign of its term. Subtracting the two squares cancels both the unwanted molecule–molecule term \(A^2\) and the recorder-only term, leaving the desired \(X_bA\) interaction.

**The oscillator return is exact on its infinite-dimensional Hilbert space in this force model.** It does not require an initially pure oscillator.

Choosing
\[
\delta^2=\frac{16\pi\lambda_b\lambda_m}{\theta}
\]
implements the actual signed dipole pulse with opposite signs on the recorder’s two branches. Replacing the signed pulses in the molecular word consequently makes one branch apply \(W\), the other its physical phase-reversed reference \(R\).

The recorder acquires the relative phase
\[
\phi(2n_{\mathrm{target}}-M).
\]

This is a physical Fourier component of composition. With known total occupancy \(M\), it also encodes target count. **One qubit is not a deterministic modulo-count oracle**; a larger record or further queries, readout and restoration would be required.

### The underlying interaction was tested

The executable propagates the native quantized coupling with finite dressing, rather than only the averaged force Hamiltonian. It includes the full seven-state signed molecular generator.

For a normalized test with \(g_b=g_m=1\):

| Dressing strength \(\Omega/g\) | Joint gate infidelity |
|---:|---:|
| 18 | \(2.38\times10^{-2}\) |
| 70 | \(1.49\times10^{-3}\) |
| 258 | \(1.08\times10^{-4}\) |
| 1026 | \(6.81\times10^{-6}\) |

Both chiral signs work. A separate two-molecule test uses one invariant transition pair per molecule. A nonvacuum oscillator test was also checked against a larger Fock cutoff.

A particularly useful failure was preserved: **without cancelling the unwanted dressing rotation, the gate infidelity was approximately \(0.980\), even though oscillator-return failure was only \(5.4\times10^{-5}\).** The carrier nearly returned while the intended operation was almost completely wrong. A dressing-sign echo repairs that failure.

The executable and complete numerical record are included in the archive.

## 3. Turning the molecular response into a product port

For spatial recovery, I developed a balanced three-history filter. Its paths receive
\[
RR,\qquad RW,\qquad WW,
\]
so every path receives two complete words.

The reference \(R\) is the same physical pulse sequence with the signed carrier’s phase reversed. It is **not** an assumed inverse of the full molecular dynamics.

Suppose the controlled subspace receives the desired scalar phase, while the two complete words have the same response on untouched material. A normalized three-path preparation and recombiner then implement
\[
K_s=
\frac{\zeta R_s^2-(1+\zeta)W_sR_s+W_s^2}
{2+2\cos(\phi/2)},
\qquad \zeta=e^{-i\phi}.
\]

This product port rejects both the opposite handedness and untouched states, including arbitrary common spectator phases. On the target subspace, acceptance is
\[
\eta(\phi)=16c^2(1-c)^2,
\qquad c=\cos(\phi/2).
\]

For the seven-state word,
\[
\boxed{\eta(4\pi/7)=0.8817230195.}
\]

I proved that this acceptance is optimal **within these three histories and this acceptance interface**. It is not an optimum over all physical separators.

### Why balanced exposure matters

The larger molecular calculation found that transitions with very little population transfer can still accumulate substantial phases. Unequal exposure lets those phases leak into the product port.

Using all retained electric-dipole transitions, counterrotating terms and actual carrier timing in a 165-state rigid-rotor model, the background contribution changed as follows:

| Calculation | Background acceptance contribution |
|---|---:|
| Unequal exposure, one cell | \(2.32\times10^{-4}\) |
| Balanced exposure, one cell | \(8.46\times10^{-8}\) |
| Two balanced cells at their actual arrival times | \(1.72\times10^{-14}\) |

The last calculation corrected another failed interpretation: repeating a pulse program does not automatically repeat the same interaction-picture map. The second cell was propagated at its actual time.

These values demonstrate a cancellation mechanism in the specified model. **They do not certify physical rare-product purity.** The calculation omits \(2.65\%\) of the conditional \(1\) K rotational population, and omitted states can also change virtual phases. The controlled seven states contain only \(25.58\%\) of that conditional ensemble. Conformers, motion, collisions, field noise and collection remain outside this calculation.

I also derived a harmonic near-field profile that supplies the required carrier signs at three beam positions. Only the signed carrier needs spatial variation; the common controls can be shared. Its finite-width error and full field-energy inventory are accounted for. This earns a field profile, while the transmitting molecular splitter and recombiner remain unacquired.

## 4. The strongest ordinary separator changes the conclusion

A comparison against population-only state transfer would have been misleading. Enantiomer-selective controllability is established, and prior chiral matter-wave work already addresses thermally rotating molecules. :chatgpt-content-reference{index="3"}

The independent comparator uses the **same acquired control types**:

- Global common molecular transitions.
- Path-dependent \(0/\pi\) phase reversal of the same signed carrier.
- Ordinary spatial interference.

Two signed-carrier \(\pi\) pulses produce a chirality-independent controlled reflection. Common molecular rotations and interference turn that reflection into internal-state-dependent routing. The ordinary construction can therefore transfer unknown internal entropy into temporary paths, perform ordinary enantiomer-selective state transfer, route the product, and reverse the transfer.

It restores the original internal state and blank memory without internal cooling.

| Explicit construction | Ordinary state-transfer/memory separator | Balanced phase filter |
|---|---:|---:|
| Maximum joint path modes | 16 | 3 |
| Microwave pulse layers | 164 | 208 |
| Maximum pulse action | \(152\pi\) | \(197.71\pi\) |
| Ideal acceptance on the controlled seven states | 1 | 0.881723 |

These are constructive upper bounds, not optimized economic rankings.

The phase filter retains two useful properties: a smaller explicit path network and cancellation based on agreement of the **complete words**, rather than agreement of each controlled substep. The ordinary circuit has not received the same full-rotor numerical assessment, so its shorter pulse count is not a matched physical-fidelity result.

For the shared-recorder route, the fair comparator includes ordinary Ramsey readout and modern driven-cavity gates supplied with the same interactions. Those architectures can use the composition phase too. Their logical-state occupation operators must not simply be renamed “unknown chemical label”; acquiring that molecular connection is the substantive step. :chatgpt-content-reference{index="4"}

## 5. What the complete cost reveals

The classical microwave rotation is fast because a large field supplies its amplitude. Coherently conditioning that rotation on one retained quantum recorder introduces a separate coupling and backaction problem.

For the measured \(0.1545\) D transition dipole,
\[
g_m=\frac{d_b}{\hbar}
\sqrt{\frac{\hbar\omega}{2\epsilon_0V_{\mathrm{eff}}}}.
\]
At an illustrative mode volume of \(1\,\mathrm{cm}^3\), this gives only
\[
g_m/(2\pi)=0.3565\ \mathrm{Hz}.
\]

With an assumed recorder coupling of \(1\) kHz, the twelve required controlled signed pulses take approximately **0.340 seconds**, before common pulses, ramps and readout.

Increasing the assumed recorder coupling to \(10\) MHz appears to make the operation fast. But that choice produces about two million displacement photons even for one molecule; the resulting coupling scale is roughly **14.15 GHz**, invalidating the \(5.6\) GHz rotating-wave construction used to obtain the estimate. That attractive parameter choice is a preserved failure, not an operating point. Other cavity architectures remain possible.

### Return does not erase emitted records

For initially coherent conditional oscillator trajectories in a vacuum-loss model, escaped photons retain distinguishability according to
\[
\left|\langle e_{h'}|e_h\rangle\right|
=
\exp\!\left[
-\frac{\kappa}{2}
\int|\alpha_h(t)-\alpha_{h'}(t)|^2\,dt
\right].
\]

Closing the final oscillator trajectory cannot retrieve those photons. Other oscillator input states require their corresponding noise calculation; the simple loss expression does not inherit the unrestricted scope of the ideal return theorem. Oscillator-mediated gate losses are an established concern, which the present resource accounting retains explicitly. :chatgpt-content-reference{index="5"}

The same accounting includes finite common-star and dressing fields. Their absolute pulse action remains a resource even when their net rotation cancels.

For the material task, the report keeps product and rejects at declared thermodynamic endpoints. Perfect ideal-mixture separation at restored density requires \(NkT H(f)\); preparation, irreversible losses and machine restoration add their actual costs. Passive rethermalization of inactive molecules has an explicit reset cost and can restore a bulk-processing penalty. Reversible recovery requires an additional constructed operation.

**No inequality showing lower complete cost than the equally informed ordinary separator has been earned.**

## What this run establishes

The substantive return is a physical chain:

**chiral dipole invariant → finite internal-state-preserving cycle → spatial acceptance or shared quantum record.**

Its useful failures locate the remaining obstacle more precisely. A retained coherent interaction can replace microscopic label identification in the controlled manifold, but its preparation, field restoration, escaped records, population coverage and material routing determine whether that change of representation improves recovery economics.

The collective iid law, known-count exchange-graph proof and passive sensitivity bound remain established at their previous scope. This work neither extends them to all physics nor claims that crossing their resource boundary automatically yields an economical separator.

The report contains the ordinary proofs, physical derivations, complete cost ledger and comparisons.

:chatgpt-content-reference{index="8"}

:chatgpt-content-reference{index="7"}[Download the complete research archive](producer-workspace/physical_discrimination_and_shared_records.zip). It contains the runnable models, pulse lists, numerical results, independent audits, failed constructions, source provenance, checksums and the byte-identical previous research archive.

*Persistent saving remains blocked by the earlier automatic approval decision requiring explicit authorization to transfer unpublished research. The downloadable files are complete. May I save these two finished files to your ChatGPT Library?*