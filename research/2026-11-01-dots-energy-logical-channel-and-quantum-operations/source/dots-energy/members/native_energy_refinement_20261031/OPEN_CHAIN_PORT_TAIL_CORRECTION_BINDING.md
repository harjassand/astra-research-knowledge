# Open-chain port: tail-wording correction binding

31 October 2026. The reviewed original source is preserved as `OPEN_CHAIN_PORT_REVIEWED_be8c4718.md`, SHA `be8c471821bad1bb0e4ae4652984f6ce1f4d7572b7f75af7ae3edb5ff764abdc`. The corrected `OPEN_CHAIN_VARIANCE_NORMALIZED_PORT.md` has SHA `92a63305a6ec512039c784d213bae63a97233002e00f3da8ece10518d35170a6`. I verified both hashes and read the complete diff: only the tail-bound sentence changed.

The original sentence asserted the geometric estimate tstar^(L+1)/(1-tstar) <= eta even when L = n-1 was selected by the minimum. That numerical inequality need not hold in that case. The corrected sentence properly uses S^n = 0 to give an exactly zero tail when L = n-1; when the accuracy cutoff is smaller, the geometric estimate supplies the required error bound.

The earlier independent receipt `OPEN_CHAIN_PORT_INDEPENDENT_REVIEW.md`, SHA `e32303f8f9dea00b383cac324413024fbba7b7fc8a19d38c8bcf14fc17dc62fa`, already explicitly used this two-case justification. Thus its mathematical local PASS binds to the corrected source without any change to the construction, circuit normalization, operation costs or accepted scope. The original wording defect and its correction are preserved rather than erased from the version history.

No whole refined compiler is accepted by this correction note. The separate new receiving body requires its own full audit.
