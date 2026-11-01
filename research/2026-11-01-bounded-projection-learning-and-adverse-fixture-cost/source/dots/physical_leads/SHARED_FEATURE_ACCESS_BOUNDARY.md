# Shared feature frames: a stronger source, not a free estimator repair

Root construction boundary, 2026-11-01. This is an interface diagnosis, not a new learning theorem or practical advantage.

For deterministic measure-preserving maps with paid reset to the same sampled input x, the actual values y_i(x)=f(T_{w_i}x) are a common feature frame. Averaging y(x)y(x)^T estimates the dictionary Gram by positive semidefinite matrices. Bounded frame norms and leverage enter standard random least-squares / matrix-concentration guarantees. Actual inverse maps, preparation, repeated starts, and evaluating each descriptor remain charged. An arbitrary unknown physical state cannot be copied merely by naming x.

This operation is not supplied by the stochastic scalar-return interface. Write v_i(x)=E[Y_i|x], where Y_i is one endpoint observation after word i. With independent continuations conditioned on x,

 E[YY^T]=G+diag(E Var(Y_i|x)).

Off-diagonal cross products are unbiased, but diagonal squares contain conditional dynamics noise. Replacing that diagonal by separate unbiased returns destroys the pointwise PSD frame property. Two independent vector replicas give an unbiased symmetrized cross outer product, but it can be indefinite. One cannot use a PSD-frame concentration theorem without re-deriving its actual variance bounds.

Explicit extreme example: uniform two-state source, observable f=+/-1, every nonempty primitive completely refreshes the state. All nonempty conditional features v_i are identically zero, so their true Gram is zero. Independent endpoint observations still have E[YY^T]=I. Increasing the number of shared starting states converges to I, not the wanted Gram. More shots remove variance but not this bias.

The deterministic common-input case consequently gives a legitimate stronger source which ordinary EDMD/random least-squares also receives. It does not establish a same-interface improvement of the scalar acquisition theorem, much less a civilisation-level enabling operation. The current programme must either construct and charge that stronger experimental access, or work with the non-PSD, noisy return source it actually has.

Primary prior pointers inspected via abstracts only in this root pass:
- Cohen, Davenport, Leviatan, On the stability and accuracy of least squares approximations, https://arxiv.org/abs/1111.4422. A correction exists; no uninspected precise theorem constants are invoked here.
- Cohen, Migliorati, Optimal weighted least-squares methods, https://arxiv.org/abs/1608.00512. Optimal sampling depends on the approximation space; it is not supplied automatically by an unknown hidden dictionary.

This note supplies the exact elementary covariance identity and counterexample directly. It does not claim a full-text prior-art audit.
