## ASTRA Pro3 — Learning how much slow memory can remain hidden

The continuation has produced a stronger certificate than the previous endpoint-atom calculation. Rather than bounding the possible mass at one particular decay rate, it bounds the total spectral mass across an entire interval of slow modes.

For a positive relaxation spectrum \\(\mu\\) on \\([0,1)\\), define

\\[ W_b=\mu([b,1)),\qquad b=\frac78. \\]

This measures the total response weight assigned to modes retaining at least 87.5% of their amplitude per time step.

### A sharp result from four acquired impulse coefficients

The existing continuum-source experiment acquired

\\[ (m_0,m_1,m_2,m_3) =\left(1,\frac38,\frac3{16},\frac{27}{256}\right). \\]

I derived the exact bound

\\[ \boxed{0\le W\_{7/8}\le\frac6{77}\approx0.0779221.} \\]

The upper bound is sharp over every positive relaxation spectrum compatible with the four readings.

A matching alternative source is

\\[ \mu\_\*= \frac{13}{70}\delta_0+ \frac{81}{110}\delta\_{5/12}+ \frac6{77}\delta\_{7/8}. \\]

It reproduces all four observed moments exactly, while placing \\(6/77\\) of its response weight in the slow spectral region.

The proof is independently certified by the polynomial

\\[ q(x)=\frac{32x(12x-5)^2}{847}. \\]

This polynomial is nonnegative for \\(0\le x<7/8\\) and at least one for \\(7/8\le x\le1\\). Its expectation under every compatible source is exactly \\(6/77\\), and the constructed source attains equality.

This is a classical moment-problem extremal construction used as a new Astra observation operation, not a claim of mathematical priority.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://link.springer.com\&sz=32)

Springer Nature Link



The important distinction is that the learner has bounded all potentially slow modes together, rather than only a possible atom at one decay rate.

### Precision-aware acquisition results

The strongest practical improvement came from changing which experiment was performed, rather than fitting a more elaborate source model.

| Procedure after the original four moments | Additional scalar reactions | Certified total slow-band mass |
| ----------------------------------------- | --------------------------- | ------------------------------ |
| Existing evidence only                    | 0                           | 0.077923                       |
| Acquire three consecutive moments         | 6                           | 0.007311                       |
| Acquire one response at lag 16            | 2                           | 0.004994                       |
| Combine lag 16 with retained observations | 0 more                      | 0.004195                       |

The last procedure improved the late-probe bound by 16% using a sparse polynomial constructed from only five actually observed moments. Exact rational root certificates establish its validity across the entire spectral interval, rather than just the optimization grid.

The delayed experiment takes longer than the consecutive-moment strategy. Its success also depends on the source: the alternative slow-mode source, which shares all four original moments, correctly fails the requested slow-mass threshold.

Under bounded sensor errors, an additional limitation appeared. Higher-degree polynomial certificates eventually amplified noise enough to worsen their own upper bounds. The compiler now retains the best previously certified result and rejects an invalid noisy quadrature proposal rather than inventing extra information.

### A second attack: falsifying the assumed causal law

The most consequential failure concerns linearity itself.

I executed three source models that agree on every possible isolated-pulse response, including all previously acquired moments. One model is linear, another contains a pairwise interaction between consecutive interventions, and a third includes an additional triple interaction.

Two new scalar reaction readings, combined with two retained readings, revealed the pairwise coefficient exactly:

\\[ \beta=\frac1{10}. \\]

Using the acquired impulse history and this coefficient, the compiler correctly predicted eight newly specified multi-pulse programmes without further learner source calls.

However, an alternative source with a cubic interaction remained compatible with the entire acquisition history and changed a later triple-pulse response by exactly \\(1/6250\\) on the reciprocal-reaction scale.

Consequence: A scientifically useful learner cannot infer a complete causal mechanism from successful impulse-response tests alone. It needs experiments that challenge superposition, interaction order and stability of the observation interface.

### Preserved and verified

The new research consists of five executed investigations plus independent verification. All six scripts reproduced their saved outputs byte-for-byte in an isolated directory. The verifier completed 220 exact checks, including positive atomic witnesses, polynomial bounds, raw source reactions, noisy certificates and nonlinear counterexamples.

Complete mathematical proofs and scientific findings

Sharp interval-mass theorem, source witnesses, precision-aware experimental acquisition, nonlinear memory tests and limitations.

Complete reproducible research archive

17 files: governing proof, executable programmes, actual results, native-source dependency, independent verifier and SHA-256 manifest. Archive integrity verified.

Scientific assessment: This strengthens Astra's ability to certify the collective influence of hidden slow processes and design a new experiment when retained information is insufficient. It also adds a direct causal-model falsification procedure.

The strongest unresolved opportunity is a physically implementable band-selective measurement that constrains slow-mode mass without requiring very long waits, while separately testing whether the source genuinely obeys linear positive spectral dynamics.

The mathematics has classical Gauss–Radau, moment-duality and system-identification antecedents.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://dlmf.nist.gov\&sz=32)

dlmf.nist.gov

+1

&#x20;No new physical law or superiority over an equally informed classical method has been established. The research is preserved locally; the Astra GitHub repository was not modified.
