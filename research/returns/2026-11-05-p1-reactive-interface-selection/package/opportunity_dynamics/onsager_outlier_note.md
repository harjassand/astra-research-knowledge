# Independent check of one Onsager matrix export

## Conclusion

The Ba4Ti13O30, 1000 K exported mean is indeed strongly indefinite. This is not a sign-selection or sheet-joining mistake. However, the linked coefficient archive reports substantially larger standard deviations than the workbook's displayed error bars. An explicit positive semidefinite matrix with the correct mass-weighted center-of-mass null vector lies within **0.760 archived standard deviations of every coefficient**. Thus the supplied evidence does not distinguish a noisy unconstrained estimate from a physical underlying matrix, and does not establish a failure of the transport model.

The outlying mean also occurs in the archived CSV, so an isolated XLSX transcription/export typo is not supported. The narrow issue demonstrated here is that the displayed `yerr` fields are not unmodified copies of the archived standard deviations. No molecular-dynamics replication or numerical optimization was performed.

## Sources and extraction

- Article: *Ion correlations explain kinetic selectivity in diffusion-limited solid-state synthesis reactions*, DOI https://doi.org/10.1038/s41563-026-02596-5 . Definitions checked in the locally acquired article XML, equations 1–4.
- Source workbook: `opportunity_root/41563_2026_2596_MOESM2_ESM.xlsx`, SHA-256 `34318423d4e4f4773ecb0765baa621d2ab86a2164bf423aad35c2afbd6ed55e8`.
- SI: `opportunity_root/kinetic_selectivity_supplement.txt`, section S4, equation S4; the PDF's figure captions are S9 and S10, while workbook sheet names are Figure_S8 and Figure_S9. This numbering mismatch does not affect coefficient identification because the sheets explicitly label each species pair.
- Linked archive: https://doi.org/10.6084/m9.figshare.28207292 . The 9,187-byte file `BTO_Transport_Coefficients.csv` was obtained from https://ndownloader.figshare.com/files/51681254 . SHA-256 `61fc3b785fd9b11b7788347e04c87fb170f9c71b8670faf57d962888c196237d`.

The independent script identifies the six entries using species-pair labels, phase, and temperature. It reads **signed `y_raw`**, not the nonnegative plotting coordinate `y`. Workbook locations are Figure_S8 rows 18, 63, 108 and Figure_S9 rows 18, 63, 108.

## Exact numerical diagnosis

In species order (Ba, Ti, O), dividing the exported values by 10^18 gives

\[
L=\begin{pmatrix}
0.22284&-0.36634&-9.7442\\
-0.36634&0.7544&0.94592\\
-9.7442&0.94592&3.176
\end{pmatrix}.
\]

Its eigenvalues are (-8.168964, 0.683318, 11.638886) in the same scale. The minimum/maximum eigenvalue ratio is -0.701868; the Ba–O normalized cross-coefficient is -11.582688. The Ba–O principal minor alone violates the positive-semidefinite requirement \(L_{BaO}^2\leq L_{BaBa}L_{OO}\).

Neither a common unit conversion nor a consistent change from number-normalized to mass-normalized conjugate variables can repair this sign violation: common positive scalings and invertible congruences preserve positive semidefiniteness.

## The error-bar distinction changes the interpretation

| Coefficient | XLSX signed mean | XLSX displayed yerr | Archived mean | Archived standard deviation |
|---|---:|---:|---:|---:|
| Ba–Ba | 2.2284e17 | 1.6164e17 | 2.23e17 | 1.62e17 |
| Ba–Ti | -3.6634e17 | 1.8317e17 | -3.66e17 | 3.77e17 |
| Ba–O | -9.7442e18 | 4.8721e18 | -9.74e18 | 2.04e19 |
| Ti–Ti | 7.544e17 | 4.1549e17 | 7.54e17 | 4.15e17 |
| Ti–O | 9.4592e17 | 8.6726e17 | 9.46e17 | 8.67e17 |
| O–O | 3.176e18 | 1.5810e18 | 3.18e18 | 1.58e18 |

The archived means match the XLSX means to the archive's rounding. Across the complete workbook, **all 99 negative entries have yerr exactly one half of the absolute mean**. Only 14 of 171 positive entries have that exact ratio. This pattern and the direct CSV comparison show that the plotted errors cannot be treated as the raw standard deviations. The responsible plotting/export operation was not identified and is not inferred here.

Within a componentwise ±1 displayed-yerr box, PSD is impossible: the smallest admissible absolute Ba–O entry is 4.8721, while the largest possible square root of the Ba–Ba/O–O diagonal product is only 1.35240, in units of 10^18. This is an interval statement about altered display scales, not a statistical rejection.

Conversely, the archived standard deviations permit a physical completion even inside the componentwise ±1-SD box. Let \(m=(137.327,47.867,15.999)^T\) and retain the archive's Ba/Ti principal block \(H\). Define

\[
B=\begin{pmatrix}1&0\\0&1\\-m_{Ba}/m_O&-m_{Ti}/m_O\end{pmatrix},
\qquad L_* = BHB^T.
\]

The retained block is positive definite, so \(L_*\succeq0\), and \(B^Tm=0\) gives \(L_*m=0\) exactly. Numerically,

\[
L_*/10^{18}=\begin{pmatrix}
0.223&-0.366&-0.81908863\\
-0.366&0.754&0.88567810\\
-0.81908863&0.88567810&4.38078821
\end{pmatrix}.
\]

Only the oxygen row/column changes. Changes are 0.43730 archived SD for Ba–O, 0.06958 for Ti–O, and 0.75999 for O–O. This is a constructive feasibility witness, not an estimate of the true matrix. The six marginal SDs and five-replicate description do not supply a joint confidence region or determine the sampling law. The SI's thresholds on within-trajectory linear-fit uncertainty are also distinct from between-trajectory SDs; their numerical sizes need not match.

## Center-of-mass constraint and dimensions

The article defines the species collective displacement by an unweighted sum of particle displacements, \(D_i(t)=\sum_{\alpha\in i}\Delta r_\alpha(t)\), and obtains \(L\) from the common prefactor times the long-time derivative of \(\langle D_i\cdot D_j\rangle\). In the physical mass-center frame,

\[
\sum_i m_iD_i(t)=0.
\]

Therefore \(Cm=0\) for the covariance matrix at every lag, and the exact transport coefficient satisfies \(Lm=0\), equivalently \(m^TL=0\) by symmetry. The SI's unweighted \(\sum_i L_{ij}=0\) does not follow for the number-flux convention of equations 1–4. An unweighted null vector would instead fit a suitably mass-normalized flux/force convention—for example \(L^{(m)}=MLM\), conjugate to gradients of chemical potential per unit mass—or a different reference velocity. It cannot be substituted into the stated number-displacement formula without that change of variables.

With displacement measured in cm, volume in cm^3, time in s, and kBT in eV, equation 2 gives dimensions **1/(eV cm s)**. Equation 4, \(L_{ii}^{self}=D_ic_i/(k_BT)\), gives the same result. The figure captions' 1/(eV cm^3 s) omit the displacement-squared factor relative to these definitions. This is a convention/label consistency check, not evidence that the actual implementation used incorrect conversion factors.

For a correctly centered trajectory, applying the same linear fitting functional to every covariance entry preserves the mass-null identity even at finite sample size. Independent entry-wise windows, rejected replicate subsets, or unconstrained fitting can break it. A finite-time derivative estimate can also be indefinite although the covariance itself is PSD. The exact long-time transport limit is PSD. Which numerical step generated this example cannot be determined from the means and SDs alone.

## Consequence for the research selection

Do not use this outlier as an empirical discovery or as evidence against the paper's qualitative kinetic-selectivity mechanism. The defensible mathematical requirement for composing physical transport laws is explicit: use conjugate variables consistently, conserve mass in the chosen frame, and preserve a positive-semidefinite dissipative response. These exact requirements remain relevant independently of this export, and a constrained joint estimator could enforce them. Establishing that such an estimator improves synthesis predictions would require a separate controlled comparison that was not undertaken here.

Reproduce with the scientific Python runtime and `opportunity_dynamics/audit_onsager_outlier.py`. Detailed numerical results and source-cell provenance are in `onsager_outlier_countercheck.json`. Source files were left unchanged.
