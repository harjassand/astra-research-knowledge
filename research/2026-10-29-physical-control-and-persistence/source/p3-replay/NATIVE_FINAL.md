**I obtained a matching source-control law and constructed the quantum operation that attains it.** For the inherited noisy source, retaining and replaying a classical preparation record can reduce acquisition from \(\Theta(r^{2})\) ordinary copies to a number independent of \(r\), at fixed accuracy.

The construction yields a broader capability: **a logical interface to an unknown qubit encoding, acquired from noisy quantum programs.** It supports extraction, initialization, readout and logical gates without learning the encoding’s matrix or obtaining its inverse.

These are new working derivations, with executable checks completed, but without a separate independent review or established priority.

## 1. The acquisition law

Partition the source’s \(r\) mixing modes into \(B\) equally sized groups, leaving

\[
s=\frac rB
\]

unresolved modes per group. The additional classical record identifies the group used for the **actual supplied target copy**.

There are two different physical capabilities:

- **Record only:** observe each emission’s group and wait for matching training emissions.
- **Record and replay:** request fresh noisy training emissions from the target’s group.

For reaching the original discrimination target \(13/16\), the matching bounds are:

| Available source interface | Required training emissions |
|---|---:|
| Ordinary unrecorded iid copies | \(\Theta(r^{2})\) |
| Records identifying \(B\) groups; natural emissions only | \(\Theta(r^{2}/B)\) |
| The same records, with selectable group replay | \(\Theta((r/B)^{2})\) |
| Full mode record; natural emissions only | \(\Theta(r)\) |
| Full mode record and replay | \(\Theta(1)\) at fixed accuracy |

The upper bounds hold uniformly over the unknown \(U\). The lower bounds permit arbitrary joint measurements and unlimited computation.

**Discarding the additional record gives exactly the original quantum state**
\[
\rho_U=\frac23J_U+\frac13\tau.
\]
Its global noise floor remains real. Every conditional training program retains the same depolarization strength. The additional resource is the recorded and controllable preparation coordinate; the joint record–source system contains information absent from ordinary copies.

## 2. The physical operation: exchange with the hidden logical qubit

For a selected group, define its unknown encoded Pauli operators
\[
L_a=U(\sigma_a\otimes\Pi_b)U^\dagger,
\qquad a\in\{x,y,z\},
\]
where \(\Pi_b\) selects its \(s\) mixing modes.

Measuring the accessible qubit of a noisy training copy in a known Pauli basis produces a reference-register program
\[
\omega_{a,\pm}=\frac{P_b\pm qL_a}{2s},
\qquad q=\frac23.
\]
Consequently,
\[
\omega_{a,+}-\omega_{a,-}=\frac qsL_a.
\]

This identity lets the receiver build the action of the unknown logical operators without estimating their entries.

Using a clean qubit \(Q\), fresh program registers and known controlled SWAP interactions, I constructed a simulation of
\[
H_b=\sum_{a=x,y,z}\sigma_a^Q\otimes L_a.
\]
On the selected encoded block,
\[
e^{-i(\pi/4)H_b}
=
e^{-i\pi/4}\operatorname{SWAP}_{Q,\text{logical qubit}},
\]
with the gauge factor untouched.

Thus the unknown logical qubit can be exchanged with a trusted qubit. The construction consumes noisy programs and requires no source inverse, purified preparation oracle or assumed unknown logical gate.

The proved complete error bound is
\[
\boxed{
\frac12\left\|\mathcal C_N-\operatorname{Ad}_{e^{-i(\pi/4)H_b}}\right\|_\diamond
\leq
\frac{9\pi^2s^2}{2q^2N}.
}
\]

This includes arbitrary untouched reference systems. For full mode replay, \(s=1\), and **3,198 matched noisy programs suffice for error at most \(1/32\)** under this conservative bound. Applied to the original probe, that guarantees discrimination success at least
\[
\frac78-\frac1{32}=\frac{27}{32}>\frac{13}{16}.
\]

“Constant” therefore has a concrete meaning here; it does not mean one free operation.

### The broader capability

The exchange construction applies to arbitrary unknown qubit isometries
\[
V_z:\mathbb C^2\longrightarrow\mathbb C^D
\]
whenever the target has a correct classical record \(z\) and the source can replay its noisy Choi programs. Different isometries may have overlapping images and nonuniform occurrence probabilities.

At fixed accuracy, the matching-program count is independent of \(D\), the number of branches and the selected branch’s rarity.

The same operation supplies:

| Operation on the encoded qubit | Acquired exchanges |
|---|---:|
| Extraction or readout | One |
| Initialization from a trusted qubit | One, plus an encoded starting register |
| A logical single-qubit gate | Two |
| A joint gate between two separately encoded qubits | Four |

The programs are consumed on each exchange. This is an acquired quantum interface, with no claim of reusable calibrated decoder software.

Unknown-isometry inversion with output-dimension-independent query cost is established prior machinery and was a decisive constructive alternative in choosing this direction. The construction here explicitly accommodates the noisy programs in the source contract. :chatgpt-content-reference{index="0"}

## 3. Why the acquisition costs cannot be removed by a better receiver

I extended the inherited predictive-information argument to the recorded groups, using the retrieved [N1104 entropy-increment source](https://github.com/harjassand/astra-research-knowledge/blob/c64402f357e69975df195c4925cb882f5d4b8177/research/2026-10-27-dot-scientific/source/quantum_operational_certification_20261024/mixed_flag_quadratic_choi_program_lower_bound.md).

For one group with \(s\) unresolved modes and \(m\) matching programs,
\[
I(\text{channel label}:\text{programs, output})
\leq \frac{1024}{81}\frac{m}{s^2}.
\]

With passive records, only \(n/B\) of \(n\) emissions match the target group on average. With selectable replay, all \(n\) can match. Fano’s inequality therefore gives
\[
n_{\rm passive}\geq c_0Bs^2,
\qquad
n_{\rm replay}\geq c_0s^2,
\]
where
\[
c_0=
\frac{81}{1024}\bigl[h(1/4)-h(3/16)\bigr]
\approx0.006308949.
\]

These match the constructive exponents.

For full mode records, there is a stronger direct statement:
\[
p_{\rm succ}
\leq
\frac34+
\frac18\left[1-\left(1-\frac1r\right)^n\right].
\]

If no training emission shares the target’s mode, an unobserved logical-basis rotation erases the channel label while leaving all training data unchanged. Reaching \(13/16\) therefore requires approximately \(r\log 2\) passive emissions.

**A label that can only be found by waiting still carries the waiting cost.**

## 4. What obtaining replay actually requires

A sufficient source realization is explicit:

1. Prepare the noisy Bell resource and a mixing-register basis state \(|j\rangle\).
2. Retain the classical preparation record, or its group label.
3. Apply the fixed unknown \(U\).
4. For replay, prepare fresh mixing registers in the requested mode or group and use the same \(U\).

This requires access to the mixing register’s preparation settings and preservation of the target’s record. It does not require identifying \(U\).

There is also an exact obstruction to treating that interface as something tomography automatically supplies. For every mixing-register unitary \(W\),
\[
\rho_{U(I\otimes W)}=\rho_U,
\]
and the entire memoryless forward channel is unchanged:
\[
\mathcal E_{U(I\otimes W),q}=\mathcal E_{U,q}.
\]

Nevertheless, the corresponding **named recorded instruments and requested-mode outputs can differ maximally**. I constructed a permutation example in which the unrecorded sources are identical and the recorded source states have trace distance one.

Hence even complete knowledge of the forward channel does not determine the source’s actual record-and-replay instrument. This concerns fidelity to the actual named instrument; it does not forbid manufacturing some compatible convention for labels. Ensemble freedom is established mathematics, including the Hughston–Jozsa–Wootters classification. :chatgpt-content-reference{index="1"}

For a task-sufficient substitute, the quantitative obstruction remains: if controls synthesized solely from ordinary iid copies enable success \(13/16\) on the original fresh probe, their total copy acquisition must still satisfy the quadratic lower bound.

The source realization supplies the control through its preparation circuit.

## 5. Scope, predecessors and remaining physical cost

Environment-assisted recovery using classical records is established work. Its fully refined correctable branches are scaled isometries; the new decoder supplies an acquisition procedure from the specified noisy replay programs without identifying those isometries. :chatgpt-content-reference{index="2"} Sample-based Hamiltonian simulation is also established machinery; I proved the collision error estimate directly for this construction. :chatgpt-content-reference{index="3"}

The new working contribution is the **matching record-versus-replay acquisition law, its explicit noisy-program exchange, and the separation between physically supplied replay and controls acquired from passive data**.

Its material limits remain:

- The receiver needs trusted coherent whole-register interactions, clean ancillary qubits and quantum storage while acquiring programs.
- Source preparation, label retention, reset, routing, gate accuracy and holding noise remain paid resources. Dimension-independent copy count does not imply dimension-independent hardware.
- The decoder extracts the logical system with its existing noise. It does not reverse the target’s depolarization.
- The guarantee concerns the resulting physical channel, including its training randomness. Each operation consumes fresh programs.
- The lower bounds retain their state-emission contracts. They do not settle the separate general coherent-adaptive-source-query problem.
- Direct composition gives a program upper bound quadratic in the number of exchanges at fixed total error. A fault-tolerance or scalable-device result has not been established.

The accepted N675 foundations and their scope remain unchanged.

The proof, executable and results are saved in place under `producer-workspace/p3_source_controls_20261029`. **159 floating-point matrix diagnostics passed**, covering the explicit interaction, reference-preserving extraction and instrument counterexample, alongside separately identified exact rational arithmetic checks. These are new executions; the inherited 68 reported checks were not represented as locally reproduced.