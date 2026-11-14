# North Star: finite Ising bbox/flow partial result

**Status: substantive conditional finite bound, not the North Star, not a transition-time predictor.**

At the retained R=200, L=1600, θ=4, βh=.02, original rate-one-per-site heatbath convention, thermal source, soft-sourceκ, and majority target:

- Reconstructed four-corner flow certifies **Cκ/ZA > exp(-6251)**, conditional on its stated geometric/overlap arguments and inherited source model. With the previous cut this recovers **Wold/Cκ < exp(36)**. The missing earlier files were reconstructed, not recovered byte-for-byte.
- A **different trial potential**, based on augmented filled-component bounding boxes with semiperimeter H=795, gives **log(Wbbox/ZA) ≤ -6231.488679881962…** under the explicitly inherited contour/collar/topology interfaces and the supplied bbox-transfer proof.
- Combined: **Wbbox/Cκ < exp(19.511321)**, conservatively **exp(20)**. This is a bound improvement, not a measured speedup. exp(20) is still about485million; successful prediction also needs acquisition, decisions and residence costs not established here.

The engineering-relevant change is that isolated bbox growth pays its actual slow native spin-birth rate, while merger gates, contour entropy, long tails, thermal normalization, majority overrides and source-target overlap remain charged. Dropping those other terms would give a false improvement.

## Reading order

1. `research_notes/flow_resume_20261114/PAID_AUGMENTED_BBOX_TRIAL.md`: new trial, geometry, complete cost terms, H795 certificate.
2. `research_notes/flow_resume_20261114/PUSHFORWARD_RECONSTRUCTION.md`: reconstructed lower flow, explicit fibers, overlap obligations, directed scalar.
3. `research_notes/source_reconstructed_20261114/BBOX_SOURCE_REVIEW.md`: independent source-side assessment and exact torus checks. Its displayed H790 local proof also applies toH795 because both are<L−2 and≤800.
4. `LIMITATIONS.md`: what is and is not established.
5. `DEPENDENCY_MAP.md`: exact source and inherited-input provenance.

`research_notes/flow_resume_20261114/BBOX_ACQUISITION.md`, if present, describes the separate changed-trial acquisition work. Any executable finite toy sampler is NOT an R200 sampler or its complexity theorem.

## Reproduce

Requirements for primary reproduction: Python3 standard library, g++17, IEEE binary long-double directed rounding support. No network, downloaded packages, or external input files required.

```
python reproduce.py
```

The runner makes a temporary copy, verifies the inherited dependency manifest, reruns its standard checks, reconstructs the lower-flow certificate, runs finite combinatorial geometry/fiber checks, compiles the upward-rounded convolution, and regenerates the H795 upper from the included certified magnetic-moment inputs. It verifies the combined exponent<20. It does **not** silently pretend to regenerate those large moment inputs.

```
python reproduce.py --full
```

This additionally recomputes all three inherited perimeter1900 magnetic recurrences, at substantial runtime. The default reproduction receipt records exactly what ran. Underlying recurrence sources and the previous validation/correction history are included. Numerical software assumptions and conditional geometry remain mathematical obligations even when every program passes.

`SHA256SUMS.txt` authenticates the distributed files other than itself. Rerunning reproduce.py updates REPRODUCTION_RECEIPT.json, so its hash may legitimately change after a local run.

## Optional constructive appendices

`source_reconstructed_20261114` includes exact Poisson thermal source acquisition, arbitrary supplied-diagonal support, nonempty/pinned-component conditional samplers, native-clock seed continuation, and an exact infinite-variance warning for overly aggressive importance tilting. Exact source code uses Python random-bit APIs as its ideal-bit interface. Original C5 site-count wording remains unresolved; box convention and augmentation are explicit inputs, not guessed.

`sampler_resume_20261114` contains independent channel/path/occupancy work and finite comparisons. Some optional scripts require NumPy/SciPy; these are not needed by the main reproducibility runner. Each document records its scope. Their inclusion does not upgrade a conditional finite certificate into the full requested breakthrough.
