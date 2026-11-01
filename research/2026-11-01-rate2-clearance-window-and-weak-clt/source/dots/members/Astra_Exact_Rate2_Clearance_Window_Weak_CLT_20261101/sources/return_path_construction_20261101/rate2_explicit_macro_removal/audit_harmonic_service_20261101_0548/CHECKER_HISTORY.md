# Independent checker development history

The first independent diagnostic run passed its generator/mark cases but failed the audit-only final Freedman exponent equality: its `threshold/3` used Python integer true division, producing an inexact floating value. No output from that incomplete run is accepted. The exact failed script and logs remain unchanged in `check_history_v0/`.

The final script replaces that subexpression by `Fraction(threshold,3)` and reruns the complete suite from scratch. All remaining divisions operate on SymPy or Fraction values. This is an independent test-harness correction, not a defect or change in the author theorem, checker, or frozen bytes. The final result is exact rational/symbolic arithmetic; historical failure is retained explicitly.
