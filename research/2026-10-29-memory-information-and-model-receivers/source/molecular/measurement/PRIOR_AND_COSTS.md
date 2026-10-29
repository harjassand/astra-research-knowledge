# Prior, acquisition and full-cycle decision

29 October 2026. Governing construction: `MODEL_AND_RECEIVER.md`.

## Closest existing operations and what is actually inherited

The then-current N796 capsule, full technology packet, continuations and named
parking/reference corrections were read before model construction. Entry pin,
ranges and original source identifiers are in `ENTRY_RECEIPT.json`; complete
selected source strings and readable caches are retained. The served snapshot
was d6672151ce8e86d4af3e74b3b880abcdc82ae304, input9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef,
verified at the recorded intake time. This does not assert permanent currency.
N799 is prior/navigation and a correction source, not an acquired device input.

* [Schindler2019, Ultrafast infrared spectroscopy with single molecular ions](https://arxiv.org/html/1809.06776)
  already proposes cat-enhanced single-molecule recoil detection and ultrafast
  pump--probe/redistribution measurements. Generic recoil pump--probe is not
  invented here. Its detection regime and preparation assumptions still apply.
* [Wu et al.2026, single-polyatomic-ion absorption experiment](https://arxiv.org/html/2511.19687v2)
  demonstrates Ca+/CaOH+ recoil-cat absorption. Its fitted contrast and measured
  noise concern its original protocol. The paper does not demonstrate the
  added ground-span parking, a coherent four-pulse molecular history query, or
  the complete instrument error budget constructed here. Its optical pulse
  train was not phase stabilized for this purpose. No lifetime or optical
  repetition rate is silently converted to coherent full-trial throughput.
* [Public author model/data](https://github.com/quantum-molecules/absorption-spectroscopy/tree/b083acdaa181549ca591d76d86c283da013ed651)
  supplies the finite-source parameters and non-Lamb--Dicke cat model. This is
  an exact source pin, not physical validation of our extended Hamiltonian.
* [Kurz et al.2014, Nat Commun5,5527](https://www.nature.com/articles/ncomms6527)
  demonstrates direct Ca+ RF and729nm operations. The2.8us RF preparation is
  pi/2, not pi. Its magnetic field/frequencies are not assigned to Wu's setup.
  The proposed Zeeman encoding and ground-RF addition remain explicit inputs.
* [Cummins, Llewellyn and Jones2003](https://arxiv.org/abs/quant-ph/0208092)
  is the established BB1 composite-control incumbent. Its static-amplitude
  robustness does not by itself control sidebands on a large recoil cat.
* [Sorensen et al.2006, NJP8,261](https://phys.au.dk/fileadmin/site_files/forskning/iontrap/pdfs/Efficient_Sorensen_NJP_8_2006.pdf)
  demonstrates a different optical Ca+ STIRAP transfer. It does not acquire
  the RF-D-chain dark path or finite-time large-cat transfer in our preview.
* [Ma, McCaslin and Fournier2025, JACS147,9556--9565](https://pubs.acs.org/doi/10.1021/jacs.4c17464)
  demonstrates coherent vibrational dynamics of cryogenically isolated peptide
  ions using2D IR. Its supporting information uses an8-step phase cycle with
  stated pathway qualifications. Thus a meaningful incumbent already extracts
  nonlinear coherence pathways from isolated molecular systems. It uses a
  different preparation/readout regime, not nondestructive one-ion recoil.

The result is neither first phase-sensitive spectroscopy nor a generic new
interferometer. Ramsey/controlled-history readout, composite pulses, coherent
Gram matrices, Toeplitz constraints and semidefinite certificates are existing
operations. The constructed missing link is a source-specific complete
parking/return/analysis consumer together with a uniform finite-history
receiver that asks a weaker, relevant control question. Historical priority
of this combined application is UNKNOWN. A's independent derivation of the
same Gram quotient is not external historical novelty evidence.

## Strong ordinary comparator and the preserved failures

The ordinary route is selective RF swap plus an allowed optical shelf, with
the same initial packets, peak85kHz drive, added RF assumption, oscillator,
return commands and physical fluorescence. It receives all information given
to the proposed dark-transfer alternative. Smooth BB1 is adopted from ordinary
control after the RF-D path loses the bounded finite-time comparison.

| Control/representation | Discriminator | Outcome in this model |
|---|---|---|
| carrier-RWA BB1 | standalone hot-code error | .000823; misleading alone |
| all-sideband square BB1 | same code,85kHz | .0881; sideband failure retained |
| smooth BB1 | same peak, full mode | .03136 standalone; complete consumer much better |
| isolated-lambda dark path | prescribed240us | .0413; insufficient full graph |
| full six-D RF dark path | same240us | .1751; local schedule .1643, no escalation |
| bare shelving | actual return/readout | shorter, materially larger kernel error |
| smooth-BB1 shelving | same complete consumer | positive conditional model result |

The unique asymptotic dark state survives the six-D graph, as A independently
derives. Its finite-time gap/metric and required RF/Zeeman resources are not
free. A single-kick reference also does not certify marked cross-history
coherences; the finite-history kernel is the actual consumer. The tiny X
channel is excluded because it carries no ideal science signal.

No comparison here establishes advantage over an optimized physical Ca+ pulse
sequence, a fully calibrated ordinary spectroscopy setup, or efficient2D IR
on the best compatible sample. Existing optical shelving plus informed
control is the winning algorithmic operation, not a defeated straw baseline.

## Local computation and retained cost

All runs were local CPU, one BLAS thread, using an existing Python environment.
No packages, paid compute, physical shots or external writes were used. The
wall numbers below are measured run receipts, not total project labor time.
They exclude model derivation, retrieval, human/agent analysis and reading.

| Program/run | Retained measured seconds | Scope |
|---|---:|---|
| initial parking preview | .12014 process; .04787 internal | source-code/RWA/full-mode discriminator |
| added common-rotation preview | .51202 process; .070879 internal | no meaningful repair |
| smooth-carrier refinement | .498807 process; .310989 internal |100/120 cutoff/tolerance diagnostic |
| first dark-path preview | .90755 process; .227512 internal | isolated vs full graph |
| local dark-path schedule |1.214669 internal | still fails bounded target |
| complete one-kick return |1.336256 internal | no claim of molecular transfer |
| full nine-word kernels | .864945 internal | frozen input to A |
| null-science control | .18866 process | Z/Y useful, X excluded |

A's independent final exact-rational kernel consumer reports about5.36s after
imports; an initial roughly5.42s rounded-input version is retained separately
and superseded by the original-binary64-reference certificate. Its word
examples add about.052s. These are tiny-kernel computations, not another pulse
propagation, a new molecular simulation or device acquisition. Original native
author experimental/analysis costs are not remeasured by these timings.
The later integer-phase exact non-null consumer adds.0278s, again with no
propagation. Its exact same-input errors are3.20e-7(Z)/2.19e-7(Y) or smaller.

`noisy_kernel_model.py` is an UNEXECUTED exploratory scenario library. It is
not part of the positive dynamic result. Its current constructor requires the
magnetic fraction and additional ground-dephasing rate explicitly. No fixed
favorable noise embedding or new noisy performance number is claimed.

## Full physical bill and decision

Added modeled control is182.642us; cat/uncat350us and analysis about5.9us give
roughly0.539ms Hamiltonian duration before science delay and all overhead.
Actual molecule formation/reordering, cooling, internal recovery, failed
attempts, phase-reference delivery, detection/reset and survival determine the
complete rate. None is paid by100kHz laser repetition or the source contrast.

Unknowns remain: actual Zeeman encoding/field, added RF strength/selectivity,
quadrupole polarization/mirrored edges, all motional modes, phase/amplitude
control noise, full pulse analysis and fluorescence confusion, marked-history
kernel acquisition, loaded noise on the parked span, a finite supported
molecular science band, coherent pulse replicas and their true molecular
signal/loss, and affordable shot count at desired resolution. Pure E2 q=-2
is not automatically supplied by one travelling-wave polarization; ordinary
frequency resolution is an alternative only with a qualified field/geometry.

The useful output is a constructive conditional operation and its exact
acquisition contract. It removes an unnecessary hot-Hadamard prerequisite and
replaces scalar visibility borrowing by a complete coherent-history receiver.
It does NOT establish that a present apparatus economically performs the new
query. Further physics is not replaced with a favorable unspecified noise
model, a small calibration set, or a guessed molecular coefficient. Finish
this bounded wave here, with the physical discovery-multiplier claim UNKNOWN.
