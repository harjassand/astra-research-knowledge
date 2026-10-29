**I developed a computability boundary for quantum measurement comparison:** separable and positive-partial-transpose (PPT) preparations admit a finite decision procedure, while the accepted unrestricted undecidability survives beyond that boundary.

The proof is complete as a working derivation. It has not received independent review, and historical priority remains unestablished.

### The central theorem

Let \(P,Q\) be arbitrary finite, complex POVMs, with \(m\) nonzero outcomes in \(P\). Consider the uniform comparison

\[
D(P\rho\Vert P\sigma)\le c\,D(Q\rho\Vert Q\sigma),
\qquad \rho_R=\sigma_R,\quad c\ge0.
\]

Restrict both hypotheses to separable states, or both to PPT states, while initially allowing an arbitrarily large quantum reference.

**If the comparison fails, it has a faithful counterexample with**
\[
\boxed{\dim R\le m+1.}
\]

The witness can preserve both input marginals. The corresponding conditional-entropy and SLD comparisons obey the same bound. For rational measurement descriptions, I obtain a polynomial-size existential-real description of failure. Consequently, the order problem lies in **co-\(\exists\mathbb R\), hence PSPACE**; the PSPACE implication uses Canny’s classical decision theorem. Every finite optimal comparison coefficient is also a computable real algebraic number. :chatgpt-content-reference{index="0"}

The mechanism combines Astra’s existing resource-preserving Liouville construction with a compression that preserves a violation. After lifting, each numerator outcome contributes one inverse-action vector. Compressing onto their span preserves the numerator exactly and can only decrease the competing denominator. Local compression preserves PPT and separability. One additional reference level converts the compressed quadratic violation into actual entropy hypotheses.

Full derivation: :chatgpt-content-reference{index="2"}[PPT_FINITE_WITNESSES.tex](producer-workspace/PPT_FINITE_WITNESSES.tex).

### The larger consequence

Using the programme-accepted N675 theorem, I pushed this past the finite-witness result:

- **Unrestricted comparison remains coRE-complete even under the promise that every PPT preparation obeys the order.** Thus the remaining undecidable part requires an NPT preparation. The no-computable-reference-cutoff deduction is specifically for SLD testing.
- **Any positive trace-distance allowance around product preparations restores the unrestricted order problem.** An orthogonally flagged rare branch embeds an arbitrary counterexample arbitrarily close to a product state. Its entropy gap scales by the branch probability. A fixed-gap reduction is possible through tensor amplification, with potentially enormous representation costs.

These deductions retain N675’s allowance of unequal reference marginals. The neighborhood result uses a structured flagged construction; it does not establish robustness under generic depolarizing noise. I have not acquired an explicit small numerical measurement pair whose violations require NPT inputs. Provenance and exact claim boundaries are recorded in :chatgpt-content-reference{index="3"}[SOURCE_AND_CLAIM_NOTES.json](producer-workspace/SOURCE_AND_CLAIM_NOTES.json).

### Checks, costs, and the alternative opening

I checked the complex transpose identities and compression on **36 numerical cases**, and constructed one finite PPT entropy witness. Those are floating-point diagnostics supporting the analytic argument. The general real-algebraic decision procedure remains theoretical. The proof explicitly charges spectral conditioning, witness precision, measurement acquisition, tensor expansion, and emitted matrix size; a polynomial reference bound does not imply practical runtime.

The independently examined comparison-learning opening also produced a finished asset: a polynomial-time sampler for distinct pairs sharing an acquired prefix of a quadratic APN permutation, plus a candidate-validation theorem. Exact checks covered 1,065 derivative systems, and the sampler ran at \(n=31\) without enumerating \(2^{31}\) points. It does not yet learn the next hidden coordinate, which is why I selected the computability boundary for sustained work.

Saved alongside the proofs:

- :chatgpt-content-reference{index="4"}[resource_compression_checks.py](producer-workspace/resource_compression_checks.py) and :chatgpt-content-reference{index="5"}[resource_compression_results.json](producer-workspace/resource_compression_results.json)
- :chatgpt-content-reference{index="6"}[APN_DIFFERENTIAL_SAMPLING.tex](producer-workspace/APN_DIFFERENTIAL_SAMPLING.tex) and :chatgpt-content-reference{index="7"}[apn_sampler.py](producer-workspace/apn_sampler.py)

The completed terminal-calibration construction, acquisition bounds, external-deadline counterexample, and earlier computational assets remain preserved.