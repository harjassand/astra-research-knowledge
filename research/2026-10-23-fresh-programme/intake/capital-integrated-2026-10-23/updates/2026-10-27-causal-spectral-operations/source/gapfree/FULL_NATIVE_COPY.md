## ASTRA Pro3 — Spectral memory without a known decay ceiling

The strongest result of this continuation is a revised learning procedure that does not require a known maximum relaxation time.

The previous spectral-memory compiler assumed all decay factors satisfy \\(0\le\lambda\le3/4\\). I replaced that with the weaker assumption that the response is a positive mixture of modes satisfying \\(0\le\lambda<1\\). Individual modes decay, but there is no supplied uniform rate.

### 1. Useful finite-time knowledge still transfers

Using six native scalar reactions, the learner acquired three impulse-response moments from the existing continuum-spectrum source. It then generated sharp bounds for future nonnegative intervention histories under the weaker spectral contract.

A subsequent acquisition of one additional impulse coefficient required two more scalar reactions and one active intervention.

For a normalized step response with a permitted cumulative-response budget of 3:

Three acquired moments

# 16 steps

Longest horizon certified safe

Four acquired moments

# 34 steps

Longest horizon certified safe

The new measurement more than doubles the guaranteed horizon. The bounds are sharp over the declared positive spectral family: compatible sources can approach the unsafe values immediately beyond those horizons.

The executed noisy version, with certified reciprocal-reading errors of \\(10^{-8}\\), retained both horizon guarantees.

This establishes a useful distinction: an agent can warrant finite experiments and finite control programmes even when it cannot warrant their behaviour indefinitely.

### 2. A stronger impossibility theorem

I constructed two different, strictly decaying positive spectral sources that produce exactly the same finite impulse-response record, yet have radically different infinite-horizon gains.

In the strongest executed control:

Identical evidence

# 11 impulse coefficients

22 matching native scalar reactions, not merely matching fitted moments

Original continuum source

# 1.8484

Infinite-horizon response gain

Indistinguishable slow-mode source

# ≥1,000,000

Infinite-horizon response gain

Both spectra have every decay factor strictly below one. The second hides a very small amount of spectral mass at an extraordinarily slow mode, while adjusting the remaining spectral distribution so that all eleven acquired moments agree exactly.

The proof extends to any finite number of exact finite-time polynomial observations and any desired finite lower bound on the hidden long-term gain.

Consequently, no universally valid learner can certify a finite infinite-horizon response gain from such a record alone. An externally justified spectral gap, an exceptional exact-identification certificate, or additional source assumptions are required.

### 3. How much hidden slow memory remains?

The learner can also calculate the maximum spectral mass compatible with its observations at a particular, nearly nondecaying relaxation rate.

For moments through degree \\(2n\\), define the Hankel matrix \\(G_n=(m\_{i+j})\_{i,j=0}^{n}\\) and \\(v_b=(1,b,\ldots,b^n)^\top\\). The exact maximum compatible atom at \\(b\\) is

\\[ \boxed{w_n(b)=\frac{1}{v_b^\top G_n^{-1}v_b}.} \\]

This is the classical Christoffel variational formula, combined with a constructive Gauss–Radau spectral witness.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mathworld.wolfram.com\&sz=32)

mathworld.wolfram.com

+1



Maximum hidden endpoint-mode mass

Same continuum-source moments, evaluated over the compact spectral closure. Every value is exactly certified.

00.030.060.090.12357911

The mass decreases rapidly, but no finite value in this experiment is zero. A sufficiently slow mode can therefore still dominate the infinite-horizon response. The quantity measures possible mass at one specific decay factor, not the entire mass in a neighbourhood of that factor.

There is an important exception. A separate seven-moment, three-mode source produced an exact singular Hankel certificate. That certificate forced all compatible decay factors to be \\(1/8,3/8,5/8\\), establishing a genuine spectral gap of \\(3/8\\) and an exact infinite-horizon gain of \\(632/315\\).

This gives the learner a principled distinction between evidence that identifies a finite relaxation law and evidence that merely approximates one.

### 4. Rejecting an incorrect physical model

I also executed a new experiment to challenge the spectral assumption itself.

Two different causal sources gave identical responses to the first three impulse experiments. Both had positive, decreasing early response coefficients. But the fourth measurement from one source violated the positive-spectrum moment constraints.

## −3/256

Exact determinant of a required positive-semidefinite moment matrix

The negative determinant rules out every positive relaxation mixture consistent with that fourth reading. The rejection survives bounded sensor errors and was verified using actual Schur-response measurements.

This is a meaningful additional acquisition operation: the agent can reject an invalid scientific source contract instead of producing confident predictions from it. Passing the tests, however, does not prove the contract globally.

### 5. Transfer to new feedback programmes

The retained spectra also support later digital-feedback programmes, even though their outputs depend nonlinearly on the unknown spectral measure.

Two previously unspecified 40-step controllers were executed with zero additional learner source measurements.

| Later feedback gain | Interval-width improvement from fourth moment | Independent source check |
| ------------------- | --------------------------------------------- | ------------------------ |
| \\(1/20\\)          | 2.84×                                         | All 40 steps enclosed    |
| \\(1/10\\)          | 3.00×                                         | All 40 steps enclosed    |

These are sharp finite-horizon bounds over the declared source family. They do not establish infinite-time stability or a physical kinetic model.

### Verification and preserved work

The completed investigation includes eight executable research and verification programmes. All eight passed an isolated replay, reproducing eight saved JSON results files byte-for-byte. The independent verifier completed 453 exact checks covering the source measurements, mathematical certificates, counterexamples and future control programmes.

Complete research note and mathematical proofs

Sharp finite-horizon theorems, asymptotic impossibility proof, hidden-mode mass calculation, contract falsification and experimental costs.

Complete reproducible research bundle

21 files containing actual results, executable source, prior native-instrument dependency, verification, isolated replay and SHA-256 manifest. Archive integrity checked.

Scientific assessment: The substantive improvement is an experimental learner that distinguishes what it can warrant over a finite operational horizon from what its observations cannot establish asymptotically. It can acquire evidence to extend that horizon, predict new feedback operations, quantify hidden slow-mode risk, and falsify some incorrect source assumptions.

The mathematics has established moment-theoretic antecedents. An equally informed classical retaining algorithm can reproduce these results, and no new physical law has been demonstrated.

The strongest unresolved research target is a physical observation procedure that constrains the total spectral mass near nondecaying modes, rather than only individual moments or possible point masses, with realistic sensor precision and intervention cost. The work is preserved locally; the Astra GitHub repository was not modified.