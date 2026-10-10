# CD — Polynomial-orbit bounds and finite determination

This intake combines two overlapping submissions into three distinct result cards:

- [N571](../../frontier/dossiers/N571.txt): coefficient-uniform primitive-recursive upper horizon for the initial zero block of one polynomial orbit.
- [N572](../../frontier/dossiers/N572.txt): rational quadratic/carry maps with small coefficients and exponential delay.
- [N573](../../frontier/dossiers/N573.txt): algebraic-coefficient cubic maps with tower-height delay from rational Boolean starts.

The two upper-bound packages contain the same 140-line proof candidate; both original directories and their different comparison/reproduction records remain intact. The upper proof's focused internal review does not cover the later lower constructions.

The upper claim concerns only the first nonzero value of `h(F^t(a))` for one fixed polynomial map. It is not the Skolem problem of detecting an arbitrary later zero. The quadratic example has rational coefficients in `{−2,−1,0,1,2}` and first nonzero index `2^(m+1)−2`; it gives exponential delay, not a tower or a lower bound against elementary horizons. The tower example uses algebraic coefficients whose representation degree grows rapidly; it does not establish an elementary-bit lower bound for rational inputs. No source comparison establishes historical priority.

The source checks were not run during intake. All three cards remain `source_derived_unreviewed`; see [source hashes](INTEGRITY.json) and [intake validation](VALIDATION.json).
