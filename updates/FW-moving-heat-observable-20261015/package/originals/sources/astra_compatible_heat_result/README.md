# Astra compatible-heat moving-kernel result

Start with **RESEARCH_REPORT.md**. The result is a family-wide theorem on a specified four-coefficient sector, not a solution of the full planar Morrey problem.

## Independent algebraic verification

With Python 3.10+ and SymPy installed:

```sh
python verify_moving_acoustic.py
python verify_structure.py
python reconstruct.py
```

`verify_moving_acoustic.py` reads only `MOVING_ACOUSTIC_CERTIFICATE.json`; it requires no discovery code, repository access, optimizer, floating-point eigensolver, or pickle file. It verifies the universal rational identities and four Bernstein matrices proving positivity for every parameter in the closed interval [-21/8,-5/2].

`verify_structure.py` regenerates the fixed-Gram-support obstruction, checks the moving acoustic kernel, verifies the local-null-form algebra, and checks the exact failed-continuation witness. Its analytic implications are proved in the report.

`reconstruct.py` independently verifies the source coefficients transcribed from the N850 repository certificate. The mathematical identity was checked; the original source byte hash was not recomputed.

The included receipts record executed checks under SymPy 1.14.0. Exact algebra is not independent external review or formal proof verification.

## Optional construction reproduction

The discovery scripts are included as provenance and are not required by the verifiers. From this directory, run:

```sh
python family_analysis.py
python moving_face.py
python export_family.py
python bernstein_family.py
```

These optional scripts generate local intermediate pickle files. No pickle files are included in the package. The additional `acoustic_analysis.py`, `contact_cone.py`, and `nullform_analysis.py` preserve exploratory symbolic calculations.

`FAILED_CONTINUATION_WITNESS.json` disproves positivity of one selected Gram continuation at r=-8/3. It is not a nonquasiconvexity certificate and does not exclude other heat certificates.

No original repository files were changed. `MANIFEST.json` supplies SHA-256 hashes for all packaged files except the manifest itself.
