# Independent checker development history

The first independent diagnostic run aborted with OverflowError at an audit-only `N/2` Python integer true-division expression when the 400-digit test was reached. That expression would have used binary floating arithmetic at smaller inputs. The failed script and stdout/stderr are preserved unchanged under `check_history_v0/`; no result was accepted from that run.

Two such audit-only comparisons were changed to `Fraction(N,2)`. The final check is rerun from scratch with exact symbolic/rational arithmetic. This is a correction to the independent test harness, NOT to either author theorem, author check, or any accepted dependency. No original source was edited and no failed run is hidden. Symbolic and Fraction divisions elsewhere are exact.
