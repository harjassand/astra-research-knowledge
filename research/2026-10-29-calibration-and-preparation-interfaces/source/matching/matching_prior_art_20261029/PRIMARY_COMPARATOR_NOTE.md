# Random matching survival: focused primary-source comparison

Checked 2026-10-29 04:08 UTC. Limited novelty/comparator check, not novelty clearance or theorem review.

## Decision-relevant findings

The exact coefficient (n+2)/(n-1) for a uniform perfect-matching product-singlet channel-survival test was not located in this focused search. Absence is not evidence of priority. Present the operation as an explicit application of established valence-bond Gram spectra and channel verification machinery until historical priority is better established.

1. **The spectral-gap-to-infidelity bridge is established.** Zeng, Zhou and Liu, *Quantum gate verification and its application in property testing*, Phys. Rev. Research 2, 023306 (2020), arXiv:1911.06855, Eq. (10), bounds passing probability by one minus verification-operator gap times entanglement infidelity. Eqs. (21)-(23) give the optimal complex-projective-2-design coefficient (d+1)/d, and g mutually unbiased bases give g/(g-1). In particular **two logical mutually unbiased bases already give coefficient 2**, independent of logical dimension. Section II.3 addresses arbitrarily correlated rounds; Section IV studies memory quantumness. Constant sample complexity, no tomography, and spectral-gap reasoning are not new general principles. The possible distinct contribution is the physical singlet ensemble/interface and exact coefficient, with leakage and sequential extensions separately proved.

Primary passages read: https://arxiv.org/html/1911.06855 , Eqs. (10), (21)-(25), Section IV.

2. **Local gate verification is established.** Zhu and Zhang, *Efficient verification of quantum gates with local operations*, Phys. Rev. A 101, 042316 (2020), arXiv:1910.14032, develops balanced tests and local constructions. Full physical-space identity testing is not equivalent to preserving a restricted singlet code under collective noise: the code can be ideal while the physical channel is far from identity. Logical tests must pay encoder/decoder costs. No blanket superiority follows.

Primary source inspected: https://arxiv.org/html/1910.14032 , abstract and section structure. Detailed balanced-ensemble formulas not independently audited in this note.

3. **Valence-bond states and loop overlaps are old machinery.** Beach and Sandvik, *Some formal results for the valence bond basis*, Nucl. Phys. B 750 (2006), arXiv:cond-mat/0605103: singlet products indexed by pairings span spin zero; overlap magnitude is 2^(loops-n/2). Its square gives the loop Gram kernel. Full spectral evaluation additionally uses Collins–Matsumoto (2009), identified by the construction author.

Primary passage read: https://arxiv.org/html/cond-mat/0605103 , Introduction overlap rule and Section V navigation.

4. **Recent close ensemble work remains an unresolved overlap check.** Lawler, Gyawali and Martin's APS 2026 abstract, *Measuring resources in quantum spin liquids with valence bond shadows*, describes a random-walk measurement yielding perfect-matching-labelled singlets and coherence/entanglement witnesses. Their QSim 2024 poster abstract describes spin-fusion tomography and valence-bond Markov-chain shadows with numerical mixing evidence. These abstracts do not state the channel-survival coefficient. No full preprint was located in the limited title/author searches; this is not proof of absence.

Primary author abstracts read: https://meetings-archive.aps.org/smt/2026/mar-j40/2/ ; https://qsim2024.qsimconference.org/poster-sessions/ (poster 16).

5. **Verification during use with correlated noise is prior work.** Pfister, Rol, Mantri, Tomamichel and Wehner, *Capacity estimation and verification of quantum channels with arbitrarily correlated errors*, Nature Communications 9, 27 (2018), arXiv:1611.05411, lower-bounds one-shot capacity from two single-qubit bases. Protocol 2 randomly mixes tests and data during actual use. It needs no full environment reconstruction. Its capacity conclusion has finite-size/typicality qualifications and does not itself supply this program's learned singlet encoder and actual outer decoder. Equal-target comparisons must not replace an acquired decoder by an existence statement.

Primary passages read through search-returned article text: https://www.nature.com/articles/s41467-017-00961-2 , sections One-shot capacity verification, Measurement calibration and Quantifying typicality. Direct open failed through an inaccessible publisher identity redirect. Primary alternatives: https://arxiv.org/abs/1611.05411 ; https://qutech.nl/wp-content/uploads/2018/01/Nature-Communications-January-2018_-s41467-017-00961-2.pdf .

## Current claim wording

A new-to-this-program explicit constant-sensitivity singlet-subspace preservation witness, subject to proof/review, built from known spectral and verification machinery. Historical novelty unresolved. No general unknown-noise recovery, hardware advantage or invention of model-free verification claimed. Compare against logical two-basis tests as well as two-design tests, pricing encoding, decoding, connectivity, preparation, measurement, privacy and storage equally.
