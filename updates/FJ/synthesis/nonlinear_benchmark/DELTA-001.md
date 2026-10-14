# Delta 001 — correction versus corrected field notation

This note corrects notation in the frozen `REPORT.md`; no frozen artifact is modified.

In the contraction derivation, the report's (e_1=T(0)=(-\Delta+V_{\rm mid})^{-1}r) is the **correction** to the predictor. The corrected field estimate is

\[
u_1(x_q)=v(x_q)+e_1(x_q).
\]

The interval printed in `REPORT.md` at the start of its interval-evaluation paragraph, \([0.992638999524143754\ldots,\,0.992638999524143754\ldots]\), is for (u_1(x_q)), not for the correction (e_1(x_q)). In `deterministic_interval_results.json`, `e1_correction_interval` is the correction interval (near (-0.0000849375266521)); the key `e1_interval` and the local variable named `e1` in `deterministic_interval.py` actually contain (u_1=v+e_1^{\rm corr}). These names are retained in the frozen files.

The reported `u_query_interval_from_contraction` is the enclosure of the exact PDE solution obtained by expanding the (u_1(x_q)) interval by the exact contraction radius (q_Dh=3581253377555617/385382508578611200\approx0.00929272423588759). Since \(\lVert (u-v)-T(0)\rVert_\infty\le q_Dh\), the enclosure and the 1% deterministic conclusion are unchanged. No model, arithmetic, output value, timing, or conclusion changes.
