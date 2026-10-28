# Retained development failures

1. The first shell formula assertion compared unsimplified but equivalent SymPy rational expressions and failed. Replacing it by exact factorization of their difference gave zero. This did not refute the shell formula.
2. On adding the stronger reciprocity calculation, the general two-site response identity passed exact factorization. A separate contraction Gram check then used raw SymPy matrix equality and failed on unsimplified complex products. Entrywise exact simplification of the matrix difference gives the zero matrix. The failed invocation exited1 before rewriting the result JSON; the previous JSON therefore remained an earlier completed receipt until the corrected run.

The materially failed scientific conjecture is distinct from these implementation assertions: the loss witness cannot be substituted for a perfect-conductor filled-volume response. Its exact counterexamples are retained in FAILED_LOSS_BRIDGE.md and shell_and_loss_witness.json.
