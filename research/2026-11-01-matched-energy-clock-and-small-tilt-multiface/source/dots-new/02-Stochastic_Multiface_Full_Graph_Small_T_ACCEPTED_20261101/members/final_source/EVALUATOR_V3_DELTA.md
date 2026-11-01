# Additive v3 delta from receiving repair18bd0a2b

Mathematical theorem and constructor are unchanged, respectively dc96226443a99ee0a8541f03cce5af28ff735a95c6855053d223cf87d5001327 and e4f41d32797930155a4e017196636da4ad5968b8ad5519baa5361ad24834fff2.

The v2 evaluator guarded expression structure iteratively but then evaluated it
recursively. A caller could raise max_depth to3000, causing a valid1,100-deep
expression to pass the guard and then hit Python's recursion limit. This is a
real receiving boundary failure, not a mathematical counterexample.

V3 replaces expression arithmetic by iterative visit/multiply/power frames and
a value stack. Guarded input-tree nodes bound these stacks up to a fixed factor;
no recursion limit is assumed even when the explicit depth budget is raised.
Hex tags, exact rational domains and conservative power-bit refusal are retained.

`check_iterative_expression.py` passes17 regressions including1,100/3,000-deep
valid trees,5,000-wide multiplication, default-depth and node refusals, exact
mixed postorder arithmetic and invalid domains. All receiving, guard, API and
repair suites were rerun. The unchanged constructor's component and large-tier
results are retained at their exact e4f41d32 binding. V3 still awaits independent
receiving; neither the v2 freeze nor the separate scalar corollary was overwritten.
