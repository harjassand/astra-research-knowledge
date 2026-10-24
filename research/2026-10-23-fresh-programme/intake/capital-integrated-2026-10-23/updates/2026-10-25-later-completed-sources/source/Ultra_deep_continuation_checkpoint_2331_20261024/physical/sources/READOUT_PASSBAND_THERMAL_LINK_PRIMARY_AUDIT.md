# Primary-source check: a cryogenic readout passband on the thermal link

Scope: the proposed same-link contract is a 6 GHz carrier, 200 MHz useful
window, and hot/cold resistor terminations near 100 mK. This note compares
measured readout filters and a measured photonic heat valve. It does not claim
that either paper measured the exact combined two-reservoir device.

## Closest measured 200 MHz-scale readout filter

Jeffrey et al., “Fast Scalable State Measurement with Superconducting Qubits,”
PRL 112, 190504 (2014), [arXiv:1401.0257](https://arxiv.org/abs/1401.0257),
is the closest filter-bandwidth match. Its quarter-wave CPW filter is embedded
in the feedline; the paper specifies a filter quality factor `Q_F=30`, with
bandwidth `omega_r/Q_F`, and an operating frequency near 6.8 GHz, giving a
nominal width about 227 MHz. The device has four readout resonators measured at
6.705–6.805 GHz, and the measured chip transmission is shown as `S21`. It uses
a 50-ohm microwave environment and reports 99.8% single-qubit separation
fidelity at 140 ns. The filter is coupled asymmetrically: a small input
capacitor reflects most incident drive power, while the readout signal is
generated inside the filter/resonator system and leaves via the output. Thus
it establishes a real, cryogenic, roughly 200 MHz readout-scale filter, but
does not establish a high-transmission 50-ohm-to-50-ohm thermal link across
both ports. Its reported overall photon collection efficiency is -9 dB, with
loss assigned to the phase-preserving parametric amplifier, infrared filters,
switches, circulators and connectors. This is a reminder that readout fidelity
and end-to-end transmission are not inferred from the filter resonance alone.
The accessible article text does not state a mixing-chamber temperature, so it
does not supply an exact temperature anchor for the 100 mK link.

Primary locations: arXiv HTML §§ “Filter,” “Experimental Set-up,” and
Supplementary Information I.1; especially the bandwidth relation and QF=30
design at 6.8 GHz, the 50-ohm environment model, and the account that most
input signal is reflected: [full text](https://arxiv.org/html/1401.0257).

## Best matched direct two-port comparator

Yan et al., “Broadband Bandpass Purcell Filter for Circuit Quantum
Electrodynamics,” APL 123, 134001 (2023),
[arXiv:2306.06258](https://arxiv.org/html/2306.06258), is a better topology
match for a literal through-link. Its filter synthesis uses 50-ohm source and
load ports. The experimental device is a symmetric, fourth-order
transmission-line bandpass; it was made on two sapphire dies with aluminum
films, flip-chip bonded and cooled to 10 mK. The authors measured port-1 to
port-2 `|S21|`; the design center and bandwidth were 5.70 GHz and 500 MHz,
with small passband ripple attributed possibly to flip-chip integration. The
paper’s theoretical 6 GHz examples are 600 MHz wide. This is strong evidence
that a finite, planar, cryogenic two-port bandpass can be built and measured,
but not a direct demonstration at exactly 6 GHz/200 MHz. A standard synthesis
rescaling to 200 MHz is a reasonable proposed comparator, not an already
measured outcome.

Important scope: the paper’s “20 dB insertion-loss” asymmetric designs lose
power chiefly by input reflection; the circuit model has no dissipative
elements and assumes zero intrinsic resonator loss. That can be useful for
qubit Purcell protection, where readout photons originate in a resonator
coupled partway through the filter. It is not a valid substitute for a
high-`S21` two-terminal signal contract. For the same-link comparison, use its
symmetric nominal 0 dB filter class. The transmission-line implementation
also has higher-frequency replica passbands, so the heat calculation must use
the full measured or simulated spectrum, not only the 6 GHz window.

Primary locations: arXiv HTML §§ design (50-ohm endpoints and reflection
versus dissipative insertion loss), experimental realization (4th-order
filter, S21 and 10 mK), and Supplementary Information V (replica passbands):
[full text](https://arxiv.org/html/2306.06258).

## What the specified passband itself carries

For one matched, lossless bosonic channel, hot/cold endpoint temperatures
`T_h=100 mK`, `T_c=10 mK`, and a required power transmissivity
`mathcal T(f) >= eta` throughout 5.9–6.1 GHz, the unavoidable contribution is

`P_window >= eta * integral_[5.9,6.1 GHz] h f [n(f,T_h)-n(f,T_c)] df`

`= eta * 4.73198e-17 W = eta * 47.3 aW`.

Here `n(f,T)=[exp(hf/kBT)-1]^-1`; at 6 GHz, `n(100 mK)=0.05950`. The window
floor is about 1.01% of the full matched one-mode photon heat flow between the
same reservoirs (4.685 fW). This is a derived ideal-channel floor, not a
device measurement. For a real filter, integrate the measured frequency
dependent transmission. If it absorbs, its own temperature and noise must be
included as another reservoir; `S21` alone then does not describe the full
heat balance. If it is essentially lossless and both endpoints are matched,
`mathcal T=|S21|^2` is the appropriate power transmission.

Meschke et al. explicitly model the two endpoint resistors as the only noise
emitters when the inserted impedance is reactive, and include the matching
factor `4 R1 R2/(R1+R2)^2`; their experiment used nominally equal 200-ohm AuPd
resistors, not 50-ohm ports. Therefore the proposed fixture must state its
actual endpoint resistances and either match them to the filter or carry the
mismatch through the measured two-port calculation.

## Does the flux-tuned photonic valve replace the passive filter?

Meschke, Guichard & Pekola, “Single-mode heat conduction by photons,” Nature
444, 187 (2006), [primary arXiv text](https://arxiv.org/html/cond-mat/0605678v1),
demonstrated tunable photon-mediated heat transfer using two nominally
200-ohm AuPd resistors, 6.6 × 0.8 × 0.015 micrometres each, joined by 20-nm
Al lines and two DC-SQUIDs. The line was about 30 micrometres long; at 100 mK
the thermal wavelength was centimetres, so their model treated it as a lumped
SQUID `LC` impedance, not a distributed 6 GHz filter. They measured resistor
temperature modulation while sweeping flux slowly (about 1 flux quantum per
minute); inferred photonic conductance was about 0.3–0.6 of the quantum over
roughly 60–200 mK and the lowest-temperature modulation was about 6 mK.

That is a real thermal-valve alternative if thermal coupling may be actively
changed, but it neither demonstrates a 6 GHz/200 MHz readout window nor a
fast open-during-readout/closed-between-readouts cycle. Under the stated
continuous same-passive-link requirement, the symmetric passive bandpass
remains the better-matched comparator. The valve would change the winner only
after a pulse-duty-cycle contract and measured switching time/drive overhead
are supplied.

Primary source: Meschke et al., arXiv HTML §§ model, device geometry and
experimental procedure/results: [full text](https://arxiv.org/html/cond-mat/0605678v1).
