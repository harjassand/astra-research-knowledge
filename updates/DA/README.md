# DA — Strong structured-constraint sampling

One coherent research package is preserved at [`package/stronger_structured_sampling`](package/stronger_structured_sampling/README.md). It is intentionally not decomposed into frontier cards.

The source reports an entropy-contractive Gaussian-auxiliary sampler for binary quadratic targets when a tractable constrained base has a uniform covariance bound. Two reported structured classes are laminar log-concave count constraints, including hard quotas, and weighted matroid bases, including spanning trees. The source states a sufficient residual-coupling condition `||K||_op < 1/2` for those classes and reports finite-size examples and implementation benchmarks.

No historic-scale breakthrough is claimed. The reported proofs have not been independently reconstructed here; the reported implementation uses floating-point arithmetic and has no certified end-to-end total-variation guarantee. The exact linked proof/evidence files and original handoff ZIP were not available at intake. See the package README and source manifest for scope and preservation details.

The theoretical-pro branch handoff is [`state/checkpoints/theoretical-pro/2026-10-11-stronger-structured-sampling.json`](../../state/checkpoints/theoretical-pro/2026-10-11-stronger-structured-sampling.json); it records source claims and unresolved verification work, not scientific certification.
