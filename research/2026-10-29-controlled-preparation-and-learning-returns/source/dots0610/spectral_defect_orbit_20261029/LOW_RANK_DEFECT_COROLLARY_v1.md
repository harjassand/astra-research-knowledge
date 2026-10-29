# Unknown low-rank coherent defects: what permutation encoding actually buys

2026-10-29. Author corollary and finite diagnostic program, independent review pending. Dependency: PHYSICAL_PERMUTATION_TWIRL_v3.md and its actual independent receipt. This is not a general local-noise theorem or historical novelty claim.

## 1. Exact spectral-defect statement

Let P be the full n-qubit spin-zero space, d=binom(n,n/2)/(n/2+1), and let Pi<=P be an unknown rank-r projector. The source is the fixed reflection U=I-2Pi, including identity on the physical orthogonal complement. Encode any fixed K-dimensional logical subcode in P, apply a fresh uniform private physical permutation before U, undo it afterward, retire the permutation key, and apply a TP decoder that inverts the original encoder. Under the governing orbit theorem,

halfdiamond(service,id_K) <= p = 1-|Tr_P U/d|² = 4(r/d)(1-r/d).

No eigenvectors or location of Pi are needed to run this operation. For the full d-dimensional singlet carrier the halfdiamond equals p. For a proper decoded subcode this is an upper bound, not equality. Known rank r is an assumed class promise for this a priori numerical bound; the matching witness can instead test actual source performance but does not certify microscopic rank.

A fixed unrandomized two-dimensional code can fail completely: take its basis vectors e0,e1 and Pi=|e0><e0|. The source restricts to diag(-1,1), so logical entanglement fidelity is zero and halfdiamond from identity is one. The same defect has orbit bound about 4/d, exponentially small in n. The defect dimension is small relative to the FULL explored singlet space, not relative to the two-dimensional input code.

More generally U=I+(exp(i phi)-1)Pi gives p=4 sin²(phi/2)(r/d)(1-r/d). If an arbitrary unitary differs from identity only on an r-dimensional subspace and r/d<=1/2, its normalized trace lies in the disk centered at 1-r/d with radius r/d. Thus p<=4(r/d)(1-r/d), with a reflection extremal. These conclusions concern an actually averaged keyed operation, not each fixed key, and require the defect not to depend on the fresh secret key.

## 2. Explicit finite source and payload interface

Choose e0 to be a product of n/2 singlets on a fixed matching. On its first four spins use the two-dimensional singlet code; all remaining pairs are fixed singlets. This gives one logical qubit with constant-size nontrivial encoding and no full Schur transform. The rank-one reflection about e0 is physically definable without exponentially many parameters: undo its Bell-pair preparation, apply a phase -1 to the all-zero computational string, and restore the preparation. A multi-controlled phase has a polynomial-size decomposition with clean ancillas and a specified reversible-control gate set. This is a global condition on all spins. No native local Hamiltonian or cheap noisy implementation is supplied by writing the projector.

For n divisible by four, alternatively put one payload qubit in EACH four-spin singlet block. Its product code has K=2^(n/4), payload rate 1/4. The orbit corollary applies without any singlet spectators and still uses the full Catalan d denominator. Thus the corollary need not sacrifice rate to 1/n. Trusted local block encoders/decoders and permutation routing are still required; no universal fault-tolerance threshold follows.

The program checks n=4 and n=6 using all 24 and 720 physical permutations, respectively, with a fixed adversarial rank-one defect and a random complex rank-one defect. It forms the actual decoded Choi channel, verifies its residual after subtracting (1-2/d)² identity Choi is positive, verifies residual trace p and the mean-unitary scalar identity. At n=6 the adversarial fixed code has fidelity essentially zero; the orbit-decoded fidelity is 0.525, with rigorous halfdiamond upper bound 0.64. At n=4, d=2 and p=1, so no improvement exists. Larger-n entries are exact-formula evaluations, not full circuit simulations.

## 3. Strong conventional constructions: exponential suppression is not unique

### A. Ordinary logical Pauli randomization on simple block codes

Let Q0 be the product of n/4 four-spin singlet-qubit codes, dimension D0=2^(n/4). Write x=Tr(Q0 Pi)/D0. Encoding every block as payload, applying ordinary logical Pauli gates on the bare payload before encoding, and removing them after TP reset-completed decoding yields a stochastic Pauli channel. Its halfdiamond equals its entanglement infidelity, which is at most

1-|Tr(Q0 U Q0)/D0|² = 4x(1-x),  where 0<=x<=min(r/D0,1).

For r<=D0/2 this is <=4(r/D0)(1-r/D0); universally <=min(1,4r/D0) is safe. Reset completion can only increase fidelity. No permutation gates or mixed spectator ancillas are necessary. It already gives exponential suppression at rate 1/4 and cheap logical Pauli controls. It explores fewer dimensions than the full permutation orbit and has correspondingly weaker worst-case suppression.

Keeping only one payload block and filling all others with maximally mixed logical states gives another comparator. The reduced payload entanglement fidelity is at least the full-block entanglement fidelity: start from the full logical Bell state, trace out spectator input/output reference pairs, and enlarge the Bell projector to Bell_payload tensor I. A subsequent actual payload Pauli twirl gives the same valid bound. For the explicit product rank-one defect, only the all-zero spectator string triggers a payload Z, giving exact halfdiamond 1/A=2/D0, where A=D0/2. This comparator sacrifices rate and is not needed for the rate-1/4 construction above.

### B. Larger block and full-singlet comparisons

An even block size b with K_b=2^floor(log2 Catalan(b/2)) yields D0=K_b^(n/b). Ordinary logical randomization therefore has an exponent approaching n as b grows, with increasingly expensive but fixed-block encoders. There is no general theorem that permutation routing is cheaper than this trade-off.

If a high-rate K=2^floor(log2 d) singlet encoder is available, ordinary logical Pauli twirling already gives <=4r/K<=8r/d in the low-rank regime, within a factor of two of the orbit bound. Full d-dimensional generalized-Weyl randomization gives the same exact p as the permutation orbit. It requires access to the singlet multiplicity register (for example through paid Schur transforms and d-level arithmetic). The orbit's distinct interface is accessing full-singlet randomization using physical permutations from a simple fixed code, not an exclusive ability to suppress low-rank coherent defects.

For a rank-one defect, n=40 gives d=6,564,120,420 and the orbit bound 6.0937e-10. The four-spin block Pauli bound is 0.00390244, at ten payload qubits. This large mathematical difference is not a measured or complete-resource advantage; the high-rate/Weyl comparators narrow it dramatically when their interfaces are affordable.

## 4. Why this is not protection against broad local faults

Hilbert-space rank and spatial locality are unrelated. A single-qubit Pauli acts nontrivially on an exponentially large sector; it is not a rank-one spectral defect. Similarly generic small coherent local rotations can have high-rank deviation from identity. Low-rank projectors with arbitrary eigenvectors may need exponentially complex implementations. The product-singlet reflection is an explicit polynomial-control example, but it remains globally conditioned, finely structured coherent noise. The corollary does not solve generic unknown local noise, source drift depending on leaked keys, or continuous noise during unmodelled routing.

Permutation pre/post control uses up to 2(n-1) all-to-all SWAPs, or quadratic nearest-neighbour SWAP count on a line, plus keys and local encoding/decoding. Gatewise halfdiamond errors add conservatively. To exploit a 6e-10 source bound at n=40 without encoded fault tolerance, the total control error must also be of that scale; 78 SWAPs alone would need a sufficient individual budget around 8e-12 to keep their sum comparable. This is a calibration requirement, not an experimentally available accuracy claim. Exponential ideal-source suppression does not imply exponential physical-memory improvement.

## 5. Closest primary prior art and assessment

Graydon, Skanes-Norman and Wallman, *Designing Stochastic Channels*, arXiv:2201.07156v1, Theorems 1 and 3, directly proves that a unitary-1-design twirl produces a stochastic channel and that its halfdiamond distance from identity equals process infidelity. The full-singlet memory-free irreducible permutation case is an instance of this established result. Read proof: https://arxiv.org/html/2201.07156 , Sections III-IV. The memory, multiplicity-one leakage and moving-subcode extension in the governing Astra document remains a distinct separately proved scope; this source does not establish priority for that extension.

Assessment: a useful explicit example and control-interface separation, not a new general mechanism for exponential error suppression. The strongest next obligation is physical control robustness and fair compiled cost against high-rate block/Schur-Weyl alternatives. Treating the rank promise itself as an acquired model, or equating spectral rarity with local-fault rarity, would overstate the result.

## Reproduction

OPENBLAS_NUM_THREADS=1 python check_defect.py

check_defect.json contains four exhaustive finite orbit fixtures and n=4..100 formula comparisons. Floating-point positivity is a diagnostic, not a rigorous numerical SDP certificate; the theorem is inherited from the exact orbit CP decomposition.
