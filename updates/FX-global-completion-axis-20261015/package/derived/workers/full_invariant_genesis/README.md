# Full invariant completion research packet

The principal independent result is the exact projected theorem in
`REPORT.md` for the distinct acoustic contact (I,e11):

\[
\exists\alpha:\ \alpha H+kw^2+\ell vj+mv^2\text{ is ROC}
\iff\exists\alpha:\ \alpha H+kw^2+\ell vj+mv^2\text{ is QC}
\]

iff k=ell=0,m>=0, or k>0, ell+2m>0, and 2km-k ell-ell^2>0.
Both excluded equality boundaries have exact acoustic countercurves.
The proof provides an explicit finite sufficient alpha and full
all-background W_0^(1,4) quasiconvexity, without using the source heat Gram.
It does not determine the least alpha.

`GENERAL_FLAT_COMPLETION.md` is a subsequent joint generalization proposed
by the root and completed here: in the full nine-dimensional invariant
space, a PSD quadratic support modulo lambda det plus cubic flatness on
its kernel yields a finite H completion. `flat_completion_compiler.py`
checks this sufficient certificate exactly for rational input. Failure is
`UNRESOLVED_BY_THIS_COMPILER`, never a full QC verdict.

`verify_theorem.py` passes 47 exact checks. The generic compiler self-check
passes 11 checks. Their receipts are `EXACT_RECEIPT.json` and
`GENERAL_COMPILER_RECEIPT.json`. They validate algebraic identities and
constant arithmetic; the analytic proofs remain explicitly readable and
are not formal proof verification. Historical priority and external
correctness remain UNKNOWN.

The explicit rational completed example is

\[
113325063H+w^2-vj+\tfrac34v^2.
\]

Its all-background Jensen gap is at least (1/1125) integral |Dphi|^4;
its value at I is -1/4, so it is nonpolyconvex. Its complete acoustic
contact set has no invertible trace-free contact, excluding equality to
any single invertible two-sided transport of an inherited shear-contact
quartic. No positive-sum exclusion is claimed.

Reproduce with the research directory's `.venv/bin/python`:

```
python verify_theorem.py
python flat_completion_compiler.py --self-check
python flat_completion_compiler.py --input EXAMPLE_INPUT.json --output EXAMPLE_COMPILED.json
```

The last command uses a supplied rational support parameter lambda=-3 and
H reserve 5/12, and returns the displayed integer coefficient and margin.
`PROVENANCE.json` records immutable input hashes, primary literature, and
coordination boundaries. The publisher IK PDF is retained under `sources/`.
The three `explore_*.py` scripts are exploratory derivations; they do not
assert the unfinished general-angle classification.
