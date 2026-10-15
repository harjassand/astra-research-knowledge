# Scope correction to the noncompact boundary example

The frozen noncompact proof's final sentence in Section 9 says the example excludes “arbitrary probability noise.” Read that phrase as **arbitrary all-exponential probability noise**. Its displayed proof and theorem have that narrower scope. The unqualified sentence is false.

Indeed, for tau=(1+B)delta_0-eta with eta nonnegative of mass B, the geometric renewal measure

    nu = sum_{n>=0} eta^{*n}/(1+B)^{n+1}

is a probability: its masses sum to one. Absolute total-variation convergence justifies convolution termwise and telescoping gives tau*nu=delta_0. It has infinite moments at g>a, since already the n=1 term has infinite such moment. Thus it does not contradict the proved exclusion of all-exponential regularizers.

This correction was found by the separate laplace_construction_v3 audit. The original proof bytes, its actual mathematical argument, and the review remain preserved. No correction to the main equivalence under weighted hypothesis (W) is needed. External review and historical priority remain unknown.
