# Actual Astra machinery checked, not silently imported

Fetched original `updates/P/package/outputs/endotactic_permanence.tex` from Astra commit81919dc2428968e929c865e9f10b88c0605f529a; saved N33_original.tex. The governing packet N33 preserves source/review version distinctions and explicitly forbids automatic stochastic recurrence transfer.

The source's affine lemma constructs a finite family of fixed slopes r and scale-dependent offsets b_r(h), such that active slopes at x_i=h^p_i approximate the exponent vector p to a prescribed positive tolerance. Its deterministic construction uses F_h(x)=min_r[r·x+b_r(h)], a constant plateau M_h, and compact sets K_h={F_h=M_h}. Activity controls the signs of r·reaction vectors; deterministic drift is proved only through that source's own hypotheses and scale argument.

This is genuinely relevant to the missing sector selector, but it does not immediately give a stochastic dual measure:

* The offsets depend on h. Substituting h=h(x) introduces extra fixed-shift terms; they cannot be discarded as constants.
* Minimizing independently over h is not justified: the offsets may diverge, and optimizing them need not select the scale on which their activity guarantee applies.
* A nested-level construction would require proven nesting/regularity and quantitative control of jumps across facets; compact plateaux by themselves do not supply these.
* At bounded population coordinates, monomial approximations and small relative jump errors fail. Deterministic positive-coordinate geometry does not control these discrete strata.

Consequently no N33 global barrier or selector is assumed in the local radial dual proof. A possible receiving theorem must construct the scale/level selector and verify actual adjoint inequalities, rather than cite deterministic permanence as if it implied them. The available source's finite-label and cutoff constants are non-effective in general; no efficient physical compiler follows.
